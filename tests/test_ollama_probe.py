# -*- coding: utf-8 -*-
"""Tests for the fixed ollama generation probe (state/queue/tech#51, R1881).

Covers the two trap families the probe retires:
- 503 saturation vs other HTTP errors (rc 1 vs rc 2 differentiation saved),
- a genuine 400 observed through the clean urllib client is rc 2 (the
  historical 400 was a PS inline-quoting transport artifact, R1880),
plus CLI surface (--model/--timeout/--json) and the main-guard import
safety (no probe flight on import).

tech#52 (R1883): --ledger JSONL append face -- opt-in only (no flag = no
append anywhere), one row per real probe flight, best-effort WARN on write
failure with the probe exit code untouched, bad-timeout writes no row.

tech#54 (R1888): ledger rows carry gpu_util/gpu_mem context columns
(best-effort nvidia-smi read; failure -> NONE markers, probe rc untouched).

tech#55 (R1889): advisory `face` column -- three-face reading discipline
(503+idle=slot-wedged / 503+busy=saturated-busy / timeout+busy=
busy-contended / timeout+idle=service-anomaly). Advisory only: rc 0/1/2
semantics never move. Face lands on --json, human line (non-ok) and every
--ledger row. GPU busy threshold util>=80 (tech#44 defer threshold).

tech#56 (R1890): cold-reload face -- timeout + GPU idle + gpu_mem below
the 4000MiB residency line (smallest probed model ~4.7GB) = the probe
itself started a cold load that outran the request cap; not a service
fault (R1889 11:28:48 anchor). Busy generation still wins (busy-contended);
unreadable mem stays the conservative service-anomaly face; 503 saturation
semantics untouched (slot-wedged family).
"""

import io
import json
import os
import shutil
import sys
import tempfile
import unittest
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src", "os"))

import ollama_probe as op  # noqa: E402


class _FakeResp(object):
    def __init__(self, payload):
        self._bytes = payload

    def read(self):
        return self._bytes

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _http_error(code, detail):
    return urllib.error.HTTPError(
        "http://localhost:11434/api/generate", code, "err", None,
        io.BytesIO(detail.encode("utf-8")))


SATURATION_DETAIL = '{"error":"server busy, please try again.  maximum pending requests exceeded"}'


class BuildBodyTests(unittest.TestCase):
    def test_body_is_valid_json_with_model(self):
        body = json.loads(op.build_request_body("qwen2.5:14b-8k").decode("utf-8"))
        self.assertEqual(body["model"], "qwen2.5:14b-8k")
        self.assertEqual(body["prompt"], "hi")
        self.assertFalse(body["stream"])

    def test_no_shell_quoting_surface(self):
        # The R1880 trap: inline PS JSON lost quotes -> 400 fake signal.
        # Body built inside Python must round-trip through json.loads.
        raw = op.build_request_body("m:1").decode("utf-8")
        self.assertEqual(raw, json.dumps(json.loads(raw)))


class ClassifyTests(unittest.TestCase):
    def test_503_code_is_saturated(self):
        self.assertEqual(op.classify(503, "anything"), 1)

    def test_saturation_message_is_saturated(self):
        self.assertEqual(op.classify(400, SATURATION_DETAIL), 1)

    def test_other_http_is_error_rc2(self):
        self.assertEqual(op.classify(400, '{"error":"bad request"}'), 2)
        self.assertEqual(op.classify(500, "boom"), 2)
        self.assertEqual(op.classify(400, None), 2)
        self.assertEqual(op.classify(404, ""), 2)


class RunProbeTests(unittest.TestCase):
    def setUp(self):
        self._orig = op._http_post

    def tearDown(self):
        op._http_post = self._orig

    def _patch(self, raiser=None, resp=None):
        def fake(base_url, body, timeout):
            if raiser is not None:
                raise raiser
            return resp
        op._http_post = fake

    def test_rc0_on_200(self):
        resp = _FakeResp(json.dumps({"done_reason": "stop"}).encode("utf-8"))
        self._patch(resp=resp)
        result = op.run_probe()
        self.assertEqual(result["rc"], 0)
        self.assertEqual(result["status"], "ok")

    def test_rc1_on_503_saturation(self):
        self._patch(raiser=_http_error(503, SATURATION_DETAIL))
        result = op.run_probe()
        self.assertEqual(result["rc"], 1)
        self.assertEqual(result["status"], "saturated")
        self.assertEqual(result["http_status"], 503)

    def test_rc1_on_503_with_unreadable_detail(self):
        err = _http_error(503, "")
        err.read = None  # detail read fails -> empty string, code still classifies
        self._patch(raiser=err)
        result = op.run_probe()
        self.assertEqual(result["rc"], 1)

    def test_rc2_on_genuine_400(self):
        self._patch(raiser=_http_error(400, '{"error":"bad request"}'))
        result = op.run_probe()
        self.assertEqual(result["rc"], 2)
        self.assertEqual(result["status"], "error")

    def test_rc2_on_transport_error(self):
        self._patch(raiser=urllib.error.URLError("connection refused"))
        result = op.run_probe()
        self.assertEqual(result["rc"], 2)
        self.assertEqual(result["status"], "error")
        self.assertIn("connection refused", result["detail"])


class FaceTests(unittest.TestCase):
    """tech#55: advisory three-face discipline; rc semantics never move."""

    def test_timeout_detection_bare_timeouterror(self):
        self.assertTrue(op._is_timeout(TimeoutError("timed out")))

    def test_timeout_detection_urlerror_wrapped_socket_timeout(self):
        import socket as _socket
        self.assertTrue(op._is_timeout(
            urllib.error.URLError(_socket.timeout("timed out"))))

    def test_timeout_detection_message_fallback(self):
        self.assertTrue(op._is_timeout(
            urllib.error.URLError("something timed out mid-request")))

    def test_non_timeout_transport_is_not_timeout(self):
        self.assertFalse(op._is_timeout(
            urllib.error.URLError("connection refused")))
        self.assertFalse(op._is_timeout(ConnectionResetError("reset")))

    def test_run_probe_flags_timeout_on_transport_timeout(self):
        orig = op._http_post

        def fake(base_url, body, timeout):
            raise TimeoutError("timed out")
        op._http_post = fake
        try:
            result = op.run_probe()
        finally:
            op._http_post = orig
        self.assertEqual(result["rc"], 2)
        self.assertTrue(result["timeout"])

    def test_run_probe_no_timeout_flag_on_503(self):
        orig = op._http_post

        def fake(base_url, body, timeout):
            raise _http_error(503, SATURATION_DETAIL)
        op._http_post = fake
        try:
            result = op.run_probe()
        finally:
            op._http_post = orig
        self.assertEqual(result["rc"], 1)
        self.assertFalse(result["timeout"])

    def _face(self, rc, util, timeout=False, status="error", mem="3246"):
        return op.compute_face(
            {"rc": rc, "status": status, "timeout": timeout},
            {"gpu_util": util, "gpu_mem": mem})

    def test_face_table(self):
        # ① 503 + GPU idle = wedged-slot face (R1883-85 family).
        self.assertEqual(self._face(1, "1", status="saturated"), "slot-wedged")
        self.assertEqual(self._face(1, "79", status="saturated"), "slot-wedged")
        # 503 + GPU busy = genuine queue-full saturation.
        self.assertEqual(self._face(1, "80", status="saturated"), "saturated-busy")
        self.assertEqual(self._face(1, "100", status="saturated"), "saturated-busy")
        # ② timeout + GPU busy = busy-contended (yield, not broken) --
        #    the R1888 10:59 flight (rc2 + util 100) is this face.
        self.assertEqual(self._face(2, "100", timeout=True), "busy-contended")
        # ③ timeout + GPU idle + model resident = genuine service-anomaly
        #    face (tech#56 split the old idle branch: low-mem reads are
        #    cold-reload, so the anomaly case needs a resident-model mem).
        self.assertEqual(self._face(2, "1", timeout=True, mem="11348"), "service-anomaly")
        # rc=2 non-timeout stays a plain error face.
        self.assertEqual(self._face(2, "100", timeout=False), "error")
        # rc=0 is ok regardless of GPU state.
        self.assertEqual(self._face(0, "100", status="ok"), "ok")
        self.assertEqual(self._face(0, "1", status="ok"), "ok")

    def test_cold_reload_face(self):
        # tech#56: timeout + GPU idle + gpu_mem below the smallest model's
        # footprint = cold-reload, not service-anomaly (R1889 11:28:48
        # anchor: rc2/gpu_mem=2012, 13 min after a clean GEN-OK).
        self.assertEqual(self._face(2, "1", timeout=True, mem="2012"), "cold-reload")
        # Default helper mem (3246) also sits under the 4000MiB line.
        self.assertEqual(self._face(2, "1", timeout=True), "cold-reload")
        # Boundary: strictly below the line is cold; at/above = anomaly.
        self.assertEqual(self._face(2, "1", timeout=True, mem="3999"), "cold-reload")
        self.assertEqual(self._face(2, "1", timeout=True, mem="4000"), "service-anomaly")
        # Busy generation wins regardless of mem: contended, not cold.
        self.assertEqual(self._face(2, "100", timeout=True, mem="2012"), "busy-contended")
        # Unreadable mem stays the conservative anomaly face.
        self.assertEqual(self._face(2, "1", timeout=True, mem="NONE"), "service-anomaly")
        self.assertEqual(self._face(2, "1", timeout=True, mem="[N/A]"), "service-anomaly")
        # Cold-reload is a timeout-only face: 503 with low mem stays
        # slot-wedged (R1883-85 family semantics untouched).
        self.assertEqual(self._face(1, "1", status="saturated", mem="2012"), "slot-wedged")

    def test_face_gpu_context_unavailable(self):
        self.assertEqual(self._face(1, "NONE", status="saturated"), "gpu-ctx-none")
        self.assertEqual(self._face(2, "NONE", timeout=True), "gpu-ctx-none")
        self.assertEqual(
            op.compute_face({"rc": 1, "status": "saturated"}, {}),
            "gpu-ctx-none")
        # Unparseable util (e.g. "[Not Supported]") also can't judge.
        self.assertEqual(self._face(1, "[N/A]", status="saturated"), "gpu-ctx-none")

    def test_cli_json_carries_face_and_gpu_columns(self):
        orig_http = op._http_post
        orig_smi = op._nvidia_smi_query
        op._http_post = lambda base_url, body, timeout: (_ for _ in ()).throw(
            TimeoutError("timed out"))
        op._nvidia_smi_query = lambda: "100, 11348\n"
        try:
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = op.main(["--json"])
        finally:
            op._http_post = orig_http
            op._nvidia_smi_query = orig_smi
        self.assertEqual(rc, 2)  # rc semantics untouched by the advisory face
        line = json.loads(buf.getvalue().strip())
        self.assertEqual(line["face"], "busy-contended")
        self.assertEqual(line["gpu_util"], "100")
        self.assertEqual(line["gpu_mem"], "11348")
        self.assertTrue(line["timeout"])

    def test_human_line_carries_face_on_non_ok(self):
        orig_http = op._http_post
        orig_smi = op._nvidia_smi_query
        op._http_post = lambda base_url, body, timeout: (_ for _ in ()).throw(
            TimeoutError("timed out"))
        op._nvidia_smi_query = lambda: "100, 11348\n"
        try:
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = op.main([])
        finally:
            op._http_post = orig_http
            op._nvidia_smi_query = orig_smi
        self.assertEqual(rc, 2)
        self.assertIn("GEN-ERROR", buf.getvalue())
        self.assertIn("face=busy-contended", buf.getvalue())

    def test_human_line_ok_has_no_face_noise(self):
        orig_http = op._http_post
        op._http_post = lambda base_url, body, timeout: _FakeResp(
            json.dumps({"done_reason": "stop"}).encode("utf-8"))
        try:
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = op.main([])
        finally:
            op._http_post = orig_http
        self.assertEqual(rc, 0)
        self.assertIn("GEN-OK", buf.getvalue())
        self.assertNotIn("face=", buf.getvalue())


class CliTests(unittest.TestCase):
    def setUp(self):
        self._orig = op._http_post
        self._orig_smi = op._nvidia_smi_query
        # main() reads GPU context once per flight (tech#55 face) -> hermetic.
        op._nvidia_smi_query = lambda: "1, 3328\n"

    def tearDown(self):
        op._http_post = self._orig
        op._nvidia_smi_query = self._orig_smi

    def _patch_saturation(self):
        def fake(base_url, body, timeout):
            raise _http_error(503, SATURATION_DETAIL)
        op._http_post = fake

    def test_human_line_saturation(self):
        self._patch_saturation()
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = op.main([])
        self.assertEqual(rc, 1)
        self.assertIn("GEN-SATURATED", buf.getvalue())
        self.assertIn("503", buf.getvalue())

    def test_json_line_matches_rc(self):
        self._patch_saturation()
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = op.main(["--json"])
        line = buf.getvalue().strip()
        self.assertEqual(json.loads(line)["rc"], rc)
        self.assertEqual(json.loads(line)["status"], "saturated")
        self.assertIn("ts", json.loads(line))

    def test_bad_timeout_rejected(self):
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = op.main(["--timeout", "0"])
        self.assertEqual(rc, 2)
        self.assertIn("bad-timeout", buf.getvalue())

    def test_model_passed_through(self):
        captured = {}

        def fake(base_url, body, timeout):
            captured["body"] = body
            return _FakeResp(json.dumps({"done_reason": "stop"}).encode("utf-8"))
        op._http_post = fake
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = op.main(["--model", "probe-model:1b"])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(captured["body"])["model"], "probe-model:1b")

    def test_import_does_not_fly(self):
        # main-guard safety: importing the module must not run a probe
        # (importing must not raise or print; 2026-10-09 hairera lesson).
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            import importlib
            importlib.reload(op)
        self.assertEqual(buf.getvalue(), "")


class LedgerTests(unittest.TestCase):
    """tech#52 --ledger JSONL append face: opt-in, best-effort, one row per flight."""

    def setUp(self):
        self._orig = op._http_post
        self._orig_smi = op._nvidia_smi_query
        self._orig_default_ledger = op.DEFAULT_LEDGER
        self.tmp = tempfile.mkdtemp(prefix="bs-ollama-ledger-")
        op.DEFAULT_LEDGER = self._path("default-ledger.jsonl")
        # Hermetic GPU context (tech#55: main() reads GPU once per flight).
        op._nvidia_smi_query = lambda: "1, 3328\n"

        def fake(base_url, body, timeout):
            raise _http_error(503, SATURATION_DETAIL)
        op._http_post = fake

    def tearDown(self):
        op._http_post = self._orig
        op._nvidia_smi_query = self._orig_smi
        op.DEFAULT_LEDGER = self._orig_default_ledger
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _path(self, name="probe-ledger.jsonl"):
        return os.path.join(self.tmp, name)

    def _rows(self, path):
        with open(path, encoding="utf-8") as fh:
            return [json.loads(line) for line in fh.read().splitlines() if line]

    def _run(self, argv):
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            return op.main(argv)

    def test_ledger_row_appended(self):
        path = self._path()
        rc = self._run(["--ledger", path])
        self.assertEqual(rc, 1)
        rows = self._rows(path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["rc"], 1)
        self.assertEqual(rows[0]["status"], "saturated")
        self.assertEqual(rows[0]["http_status"], 503)
        self.assertEqual(rows[0]["model"], op.DEFAULT_MODEL)
        self.assertTrue(rows[0]["ts"])

    def test_row_fields_exact(self):
        path = self._path()
        self._run(["--ledger", path])
        self.assertEqual(
            set(self._rows(path)[0].keys()),
            {"ts", "rc", "status", "http_status", "model",
             "gpu_util", "gpu_mem", "face"})

    def test_ledger_row_carries_face(self):
        # tech#55: saturation + GPU idle (patched "1") = slot-wedged face
        # readable straight off the ledger row.
        path = self._path()
        self._run(["--ledger", path])
        row = self._rows(path)[0]
        self.assertEqual(row["rc"], 1)
        self.assertEqual(row["gpu_util"], "1")
        self.assertEqual(row["face"], "slot-wedged")

    def test_two_flights_two_lines(self):
        path = self._path()
        self._run(["--ledger", path])
        self._run(["--ledger", path])
        self.assertEqual(len(self._rows(path)), 2)

    def test_bare_flag_uses_default_path(self):
        rc = self._run(["--ledger"])
        self.assertEqual(rc, 1)
        self.assertEqual(len(self._rows(self._path("default-ledger.jsonl"))), 1)

    def test_default_off_writes_nothing(self):
        # Existing call surface untouched: no --ledger -> no append anywhere.
        rc = self._run([])
        self.assertEqual(rc, 1)
        self.assertFalse(os.path.exists(self._path("default-ledger.jsonl")))

    def test_bad_timeout_writes_no_row(self):
        # No probe flight -> no row (one row per real flight only).
        path = self._path()
        rc = self._run(["--timeout", "0", "--ledger", path])
        self.assertEqual(rc, 2)
        self.assertFalse(os.path.exists(path))

    def test_append_failure_is_best_effort(self):
        # Parent path is a regular file -> OSError -> WARN, rc unchanged.
        blocker = os.path.join(self.tmp, "blocker")
        with open(blocker, "w") as fh:
            fh.write("x")
        bad = os.path.join(blocker, "row.jsonl")
        import contextlib
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = self._run(["--ledger", bad])
        self.assertEqual(rc, 1)  # probe verdict untouched by ledger failure
        self.assertIn("WARN", err.getvalue())


class GpuContextTests(unittest.TestCase):
    """tech#54: gpu_util/gpu_mem ledger columns, best-effort NONE on failure."""

    def setUp(self):
        self._orig = op._http_post
        self._orig_smi = op._nvidia_smi_query
        self.tmp = tempfile.mkdtemp(prefix="bs-ollama-gpu-")

        def fake(base_url, body, timeout):
            raise _http_error(503, SATURATION_DETAIL)
        op._http_post = fake

    def tearDown(self):
        op._http_post = self._orig
        op._nvidia_smi_query = self._orig_smi
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _path(self):
        return os.path.join(self.tmp, "gpu-ledger.jsonl")

    def _rows(self):
        with open(self._path(), encoding="utf-8") as fh:
            return [json.loads(line) for line in fh.read().splitlines() if line]

    def _run(self, argv):
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            return op.main(argv)

    def test_gpu_context_parsed_from_csv(self):
        # Multi-GPU rows: only the first CSV row is the context face.
        op._nvidia_smi_query = lambda: "5, 3246\n91, 11737\n"
        ctx = op.read_gpu_context()
        self.assertEqual(ctx, {"gpu_util": "5", "gpu_mem": "3246"})

    def test_gpu_read_failure_is_none_and_rc_untouched(self):
        # Wedged-slot diagnosis gap anchor: any nvidia-smi failure must land
        # as NONE markers without touching the probe verdict.
        def boom():
            raise RuntimeError("nvidia-smi missing")
        op._nvidia_smi_query = boom
        self.assertEqual(op.read_gpu_context(),
                         {"gpu_util": "NONE", "gpu_mem": "NONE"})
        rc = self._run(["--ledger", self._path()])
        self.assertEqual(rc, 1)
        rows = self._rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["gpu_util"], "NONE")
        self.assertEqual(rows[0]["gpu_mem"], "NONE")

    def test_unparseable_csv_is_none(self):
        op._nvidia_smi_query = lambda: "no csv headers here\n"
        self.assertEqual(op.read_gpu_context(),
                         {"gpu_util": "NONE", "gpu_mem": "NONE"})

    def test_ledger_row_carries_gpu_context(self):
        # Judgement face: a saturation row shows the GPU state at probe time.
        op._nvidia_smi_query = lambda: "1, 3328\n"
        rc = self._run(["--ledger", self._path()])
        self.assertEqual(rc, 1)
        row = self._rows()[0]
        self.assertEqual(row["status"], "saturated")
        self.assertEqual(row["gpu_util"], "1")
        self.assertEqual(row["gpu_mem"], "3328")


if __name__ == "__main__":
    unittest.main()
