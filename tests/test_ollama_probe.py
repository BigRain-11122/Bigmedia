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

tech#77 (R1928): /api/ps residency pre-check -- skip only the pathological
cold flight (ps-confirmed not resident + free VRAM < model footprint =
CPU-offload crawl, R1927 anchor), face=not-resident (rc=2, status=
skipped-not-resident, no generation flight at all); every unreadable piece
falls back to the legacy flight; a not-resident cold-run timeout gets the
probe-coldload face (our own load is the load) instead of busy-contended.
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
        orig_ps = op._http_get_ps
        op._http_post = lambda base_url, body, timeout: (_ for _ in ()).throw(
            TimeoutError("timed out"))
        op._nvidia_smi_query = lambda: "100, 11348\n"
        # tech#77: main() pre-checks /api/ps before any flight -> hermetic.
        op._http_get_ps = lambda base_url, timeout: (_ for _ in ()).throw(
            urllib.error.URLError("connection refused"))
        try:
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = op.main(["--json"])
        finally:
            op._http_post = orig_http
            op._nvidia_smi_query = orig_smi
            op._http_get_ps = orig_ps
        self.assertEqual(rc, 2)  # rc semantics untouched by the advisory face
        line = json.loads(buf.getvalue().strip())
        self.assertEqual(line["face"], "busy-contended")
        self.assertEqual(line["gpu_util"], "100")
        self.assertEqual(line["gpu_mem"], "11348")
        self.assertTrue(line["timeout"])

    def test_human_line_carries_face_on_non_ok(self):
        orig_http = op._http_post
        orig_smi = op._nvidia_smi_query
        orig_ps = op._http_get_ps
        op._http_post = lambda base_url, body, timeout: (_ for _ in ()).throw(
            TimeoutError("timed out"))
        op._nvidia_smi_query = lambda: "100, 11348\n"
        op._http_get_ps = lambda base_url, timeout: (_ for _ in ()).throw(
            urllib.error.URLError("connection refused"))
        try:
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = op.main([])
        finally:
            op._http_post = orig_http
            op._nvidia_smi_query = orig_smi
            op._http_get_ps = orig_ps
        self.assertEqual(rc, 2)
        self.assertIn("GEN-ERROR", buf.getvalue())
        self.assertIn("face=busy-contended", buf.getvalue())

    def test_human_line_ok_has_no_face_noise(self):
        orig_http = op._http_post
        orig_ps = op._http_get_ps
        op._http_post = lambda base_url, body, timeout: _FakeResp(
            json.dumps({"done_reason": "stop"}).encode("utf-8"))
        op._http_get_ps = lambda base_url, timeout: (_ for _ in ()).throw(
            urllib.error.URLError("connection refused"))
        try:
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = op.main([])
        finally:
            op._http_post = orig_http
            op._http_get_ps = orig_ps
        self.assertEqual(rc, 0)
        self.assertIn("GEN-OK", buf.getvalue())
        self.assertNotIn("face=", buf.getvalue())


class CliTests(unittest.TestCase):
    def setUp(self):
        self._orig = op._http_post
        self._orig_smi = op._nvidia_smi_query
        self._orig_ps = op._http_get_ps
        # main() reads GPU context once per flight (tech#55 face) -> hermetic.
        op._nvidia_smi_query = lambda: "1, 3328\n"
        # tech#77: main() pre-checks /api/ps before any flight -> hermetic
        # (ps unavailable -> legacy flight, existing rc semantics exercised).
        op._http_get_ps = lambda base_url, timeout: (_ for _ in ()).throw(
            urllib.error.URLError("connection refused"))

    def tearDown(self):
        op._http_post = self._orig
        op._nvidia_smi_query = self._orig_smi
        op._http_get_ps = self._orig_ps

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
        self._orig_ps = op._http_get_ps
        self.tmp = tempfile.mkdtemp(prefix="bs-ollama-ledger-")
        op.DEFAULT_LEDGER = self._path("default-ledger.jsonl")
        # Hermetic GPU context (tech#55: main() reads GPU once per flight).
        op._nvidia_smi_query = lambda: "1, 3328\n"
        # tech#77: /api/ps pre-check -> hermetic (ps unavailable -> legacy flight).
        op._http_get_ps = lambda base_url, timeout: (_ for _ in ()).throw(
            urllib.error.URLError("connection refused"))
        # Hermetic _http_post for the default ledger paths: 503 saturation.
        def fake(base_url, body, timeout):
            raise _http_error(503, SATURATION_DETAIL)
        op._http_post = fake

    def tearDown(self):
        op._http_post = self._orig
        op._nvidia_smi_query = self._orig_smi
        op._http_get_ps = self._orig_ps
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
        self._orig_ps = op._http_get_ps
        self.tmp = tempfile.mkdtemp(prefix="bs-ollama-gpu-")

        def fake(base_url, body, timeout):
            raise _http_error(503, SATURATION_DETAIL)
        op._http_post = fake
        # tech#77: /api/ps pre-check -> hermetic (ps unavailable -> legacy flight).
        op._http_get_ps = lambda base_url, timeout: (_ for _ in ()).throw(
            urllib.error.URLError("connection refused"))

    def tearDown(self):
        op._http_post = self._orig
        op._nvidia_smi_query = self._orig_smi
        op._http_get_ps = self._orig_ps
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


class PrecheckTests(unittest.TestCase):
    """tech#77: /api/ps residency pre-check (probe-gate order
    contamination, R1927 anchor).

    Skip only the pathological cold flight (ps-confirmed not resident +
    free VRAM < model footprint = CPU-offload crawl that burns the cap and
    self-pollutes util); every unreadable piece stays permissive (legacy
    flight). probe-coldload face annotates the remaining cold-run timeout
    (our own load is the load) -- R1927/R1928-pre-fix readings were
    partially self-load misattributed to the MV lane as busy-contended.
    """

    def setUp(self):
        self._orig_ps = op._http_get_ps
        self._orig_http = op._http_post
        self._orig_smi = op._nvidia_smi_query
        self._orig_smi_free = op._nvidia_smi_free_query
        self.tmp = tempfile.mkdtemp(prefix="bs-ollama-precheck-")
        op._nvidia_smi_query = lambda: "100, 1867\n"

    def tearDown(self):
        op._http_get_ps = self._orig_ps
        op._http_post = self._orig_http
        op._nvidia_smi_query = self._orig_smi
        op._nvidia_smi_free_query = self._orig_smi_free
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _ps(self, models):
        payload = json.dumps(
            {"models": [{"name": n} for n in models]}).encode("utf-8")
        op._http_get_ps = lambda base_url, timeout: _FakeResp(payload)

    def _ps_fail(self):
        op._http_get_ps = lambda base_url, timeout: (_ for _ in ()).throw(
            urllib.error.URLError("connection refused"))

    def _flight_timeout(self, calls):
        def fake(base_url, body, timeout):
            calls["flights"] += 1
            raise TimeoutError("timed out")
        op._http_post = fake

    def _flight_ok(self, calls):
        def fake(base_url, body, timeout):
            calls["flights"] += 1
            return _FakeResp(json.dumps({"done_reason": "stop"}).encode("utf-8"))
        op._http_post = fake

    def _run(self, argv):
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            return op.main(argv), buf.getvalue()

    # ---- classify_precheck pure decisions -------------------------------

    def test_decide_ps_unavailable_runs(self):
        proceed, reason = op.classify_precheck(False, False, 100, 9000)
        self.assertTrue(proceed)
        self.assertEqual(reason, "ps-unavailable")

    def test_decide_resident_runs(self):
        proceed, reason = op.classify_precheck(True, True, 100, 9000)
        self.assertTrue(proceed)
        self.assertEqual(reason, "resident")

    def test_decide_no_estimate_runs(self):
        # Unknown model: no footprint entry -> cannot pre-judge -> legacy flight.
        self.assertTrue(op.classify_precheck(False, True, 100, 0)[0])
        self.assertEqual(op.classify_precheck(False, True, 100, 0)[1], "no-estimate")

    def test_decide_free_unknown_runs(self):
        # nvidia-smi unreadable -> tech#56 cold-reload face catches it after
        # the fact; the pre-check never gates on missing data.
        proceed, reason = op.classify_precheck(False, True, None, 9000)
        self.assertTrue(proceed)
        self.assertEqual(reason, "free-unknown")

    def test_decide_cold_skip_below_footprint(self):
        # R1927 anchor shape: not resident + free 4.2GB < 14b-8k ~9GB ->
        # partial CPU-offload crawl. Skip, report the scheduling fact.
        proceed, reason = op.classify_precheck(False, True, 4200, 9000)
        self.assertFalse(proceed)
        self.assertIn("cold-skip", reason)
        self.assertIn("4200", reason)
        self.assertIn("9000", reason)

    def test_decide_cold_run_at_or_above_footprint(self):
        # Boundary strictly at the footprint -> full-VRAM cold load -> run.
        proceed, reason = op.classify_precheck(False, True, 9000, 9000)
        self.assertTrue(proceed)
        self.assertEqual(reason, "cold-run free=9000MB>=model=9000MB")
        proceed, _ = op.classify_precheck(False, True, 8999, 9000)
        self.assertFalse(proceed)

    # ---- /api/ps payload handling ---------------------------------------

    def test_ps_resident_name_forms(self):
        payload = {"models": [{"name": "qwen2.5:14b-8k:latest"},
                              {"model": "other:7b"}]}
        self.assertTrue(op._ps_resident(payload, "qwen2.5:14b-8k"))
        self.assertTrue(op._ps_resident(payload, "other:7b"))
        self.assertFalse(op._ps_resident(payload, "qwen2.5:7b"))

    def test_ps_resident_tolerates_junk_entries(self):
        payload = {"models": ["junk", {"nope": 1}, {"name": "qwen2.5:7b"}]}
        self.assertTrue(op._ps_resident(payload, "qwen2.5:7b"))
        self.assertFalse(op._ps_resident(payload, "qwen2.5:14b-8k"))

    def test_get_ps_shape_gates(self):
        # Bad JSON / non-dict / models-not-a-list all read as (None, False)
        # -- the pre-check is never a gate, unreadable -> legacy flight.
        orig = op._http_get_ps
        try:
            op._http_get_ps = lambda base_url, timeout: _FakeResp(b"not json")
            self.assertEqual(op._get_ps("http://x"), (None, False))
            op._http_get_ps = lambda base_url, timeout: _FakeResp(b'{"models": "nope"}')
            self.assertEqual(op._get_ps("http://x"), (None, False))
            op._http_get_ps = lambda base_url, timeout: _FakeResp(b'[]')
            self.assertEqual(op._get_ps("http://x"), (None, False))
            op._http_get_ps = lambda base_url, timeout: (_ for _ in ()).throw(
                urllib.error.URLError("refused"))
            self.assertEqual(op._get_ps("http://x"), (None, False))
            good = {"models": [{"name": "m:1"}]}
            op._http_get_ps = lambda base_url, timeout: _FakeResp(
                json.dumps(good).encode("utf-8"))
            self.assertEqual(op._get_ps("http://x"), (good, True))
        finally:
            op._http_get_ps = orig

    def test_read_gpu_free_mb(self):
        orig = op._nvidia_smi_free_query
        try:
            op._nvidia_smi_free_query = lambda: "12288, 7547\n"
            self.assertEqual(op.read_gpu_free_mb(), 4741)
            op._nvidia_smi_free_query = lambda: "garbage csv\n"
            self.assertIsNone(op.read_gpu_free_mb())

            def boom():
                raise RuntimeError("nvidia-smi missing")
            op._nvidia_smi_free_query = boom
            self.assertIsNone(op.read_gpu_free_mb())
        finally:
            op._nvidia_smi_free_query = orig

    # ---- probe-coldload face (tech#77 candidate ③) ---------------------

    def _timeout_result(self):
        return {"rc": 2, "status": "error", "timeout": True}

    def test_face_probe_coldload_only_with_not_resident_evidence(self):
        gpu = {"gpu_util": "100", "gpu_mem": "1867"}
        # ps saw the model NOT resident -> the busy GPU includes our own
        # cold load (R1927 misattribution anchor) -> probe-coldload.
        self.assertEqual(op.compute_face(
            self._timeout_result(), gpu,
            {"ps_ok": True, "resident": False}), "probe-coldload")
        # ps saw it resident -> the busy-ness is other lanes -> legacy face.
        self.assertEqual(op.compute_face(
            self._timeout_result(), gpu,
            {"ps_ok": True, "resident": True}), "busy-contended")
        # ps unavailable / no pre-check -> honest unknown, legacy face.
        self.assertEqual(op.compute_face(
            self._timeout_result(), gpu,
            {"ps_ok": False, "resident": False}), "busy-contended")
        self.assertEqual(op.compute_face(self._timeout_result(), gpu), "busy-contended")

    def test_face_not_resident_for_skip_status(self):
        gpu = {"gpu_util": "100", "gpu_mem": "1867"}
        self.assertEqual(op.compute_face(
            {"rc": 2, "status": "skipped-not-resident", "timeout": False},
            gpu, {"ps_ok": True, "resident": False}), "not-resident")

    # ---- main() skip / proceed / flag surfaces --------------------------

    def test_main_skips_pathological_cold_flight(self):
        calls = {"flights": 0}
        self._flight_timeout(calls)
        self._ps([])  # model not resident
        op._nvidia_smi_free_query = lambda: "12288, 7547\n"  # free 4741 < 9000
        path = os.path.join(self.tmp, "skip-ledger.jsonl")
        rc, out = self._run(["--json", "--ledger", path])
        self.assertEqual(rc, 2)
        line = json.loads(out.strip())
        self.assertEqual(line["status"], "skipped-not-resident")
        self.assertEqual(line["face"], "not-resident")
        self.assertTrue(line["skipped"])
        self.assertEqual(line["gpu_free_mb"], 4741)
        self.assertIn("cold-skip", line["precheck"])
        # The whole point: no generation flight, no cold load, no pollution.
        self.assertEqual(calls["flights"], 0)
        with open(path, encoding="utf-8") as fh:
            row = json.loads(fh.read().splitlines()[0])
        self.assertEqual(row["status"], "skipped-not-resident")
        self.assertEqual(row["face"], "not-resident")
        self.assertEqual(row["rc"], 2)

    def test_main_skip_human_line(self):
        calls = {"flights": 0}
        self._flight_timeout(calls)
        self._ps([])
        op._nvidia_smi_free_query = lambda: "12288, 7547\n"
        rc, out = self._run([])
        self.assertEqual(rc, 2)
        self.assertIn("GEN-SKIP not-resident", out)
        self.assertIn("face=not-resident", out)
        self.assertEqual(calls["flights"], 0)

    def test_main_resident_proceeds_with_flight(self):
        calls = {"flights": 0}
        self._flight_ok(calls)
        self._ps([op.DEFAULT_MODEL])
        rc, out = self._run(["--json"])
        self.assertEqual(rc, 0)
        line = json.loads(out.strip())
        self.assertEqual(line["status"], "ok")
        self.assertEqual(line["face"], "ok")
        self.assertEqual(line["precheck"], "resident")
        self.assertEqual(calls["flights"], 1)

    def test_main_ps_failure_runs_legacy_flight(self):
        calls = {"flights": 0}
        self._flight_ok(calls)
        self._ps_fail()
        free_calls = {"n": 0}

        def free_query():
            free_calls["n"] += 1
            return "12288, 7547\n"
        op._nvidia_smi_free_query = free_query
        rc, out = self._run(["--json"])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out.strip())["precheck"], "ps-unavailable")
        self.assertEqual(calls["flights"], 1)
        # Lazy free read: ps unavailable -> the nvidia-smi free query never
        # runs (the decision does not consume it).
        self.assertEqual(free_calls["n"], 0)

    def test_main_no_precheck_flag_never_touches_ps(self):
        calls = {"flights": 0, "ps": 0}
        self._flight_ok(calls)

        def ps_spy(base_url, timeout):
            calls["ps"] += 1
            raise AssertionError("ps must not be queried under --no-precheck")
        op._http_get_ps = ps_spy
        rc, out = self._run(["--json", "--no-precheck"])
        self.assertEqual(rc, 0)
        self.assertNotIn("precheck", json.loads(out.strip()))
        self.assertEqual(calls, {"flights": 1, "ps": 0})

    def test_main_cold_skip_disabled_by_zero_override(self):
        calls = {"flights": 0}
        self._flight_ok(calls)
        self._ps([])
        op._nvidia_smi_free_query = lambda: "12288, 7547\n"
        rc, _ = self._run(["--json", "--cold-skip-free-mb", "0"])
        self.assertEqual(rc, 0)
        self.assertEqual(calls["flights"], 1)

    def test_main_cold_run_timeout_gets_probe_coldload_face(self):
        # Not resident but free >= footprint -> full-VRAM cold load runs;
        # a timeout there is OUR OWN load in flight (probe-coldload), no
        # longer misattributed to the other lanes (R1927 anchor).
        calls = {"flights": 0}
        self._flight_timeout(calls)
        self._ps([])
        op._nvidia_smi_free_query = lambda: "12288, 3000\n"  # free 9288 >= 9000
        rc, out = self._run(["--json"])
        self.assertEqual(rc, 2)
        line = json.loads(out.strip())
        self.assertEqual(line["face"], "probe-coldload")
        self.assertTrue(line["timeout"])
        self.assertEqual(line["precheck"], "cold-run free=9288MB>=model=9000MB")
        self.assertEqual(calls["flights"], 1)


class SizeVramTests(unittest.TestCase):
    """tech#78: consume the /api/ps size_vram reading (R1928 dogfood anchor).

    ps reported the model loaded (resident) but generation crawled at
    gpu_mem 1843 << the 9000MB envelope -- mostly CPU-offloaded -- and the
    probe burned its 60s cap to learn what the pre-check payload already
    knew. The reading now lands on --json and --ledger rows as advisory
    columns; skip semantics, rc and face never move (a loaded model may
    still generate successfully, 免烧属判断位面非闸面).
    """

    # 1843 MiB in bytes (the R1928 offloaded shape).
    OFFLOADED_BYTES = 1843 * 1024 * 1024
    # ~9216 MiB in bytes (fully VRAM-resident 14b-8k shape).
    RESIDENT_BYTES = 9216 * 1024 * 1024

    def setUp(self):
        self._orig_ps = op._http_get_ps
        self._orig_http = op._http_post
        self._orig_smi = op._nvidia_smi_query
        self._orig_smi_free = op._nvidia_smi_free_query
        self.tmp = tempfile.mkdtemp(prefix="bs-ollama-sizevram-")
        op._nvidia_smi_query = lambda: "100, 1867\n"

    def tearDown(self):
        op._http_get_ps = self._orig_ps
        op._http_post = self._orig_http
        op._nvidia_smi_query = self._orig_smi
        op._nvidia_smi_free_query = self._orig_smi_free
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _ps_entry(self, size_vram):
        payload = json.dumps({"models": [
            {"name": op.DEFAULT_MODEL, "size_vram": size_vram}]}).encode("utf-8")
        op._http_get_ps = lambda base_url, timeout: _FakeResp(payload)

    def _ps_resident_no_size(self):
        payload = json.dumps(
            {"models": [{"name": op.DEFAULT_MODEL}]}).encode("utf-8")
        op._http_get_ps = lambda base_url, timeout: _FakeResp(payload)

    def _flight_timeout(self, calls):
        def fake(base_url, body, timeout):
            calls["flights"] += 1
            raise TimeoutError("timed out")
        op._http_post = fake

    def _run(self, argv):
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            return op.main(argv), buf.getvalue()

    # ---- _ps_size_vram extraction ---------------------------------------

    def test_ps_size_vram_bytes_to_mib(self):
        payload = {"models": [{"name": "qwen2.5:14b-8k",
                               "size_vram": self.OFFLOADED_BYTES}]}
        self.assertEqual(op._ps_size_vram(payload, "qwen2.5:14b-8k"), 1843)
        # Tag-suffix manifest matches the same entry (shared matcher).
        payload2 = {"models": [{"name": "qwen2.5:14b-8k:latest",
                                "size_vram": self.RESIDENT_BYTES}]}
        self.assertEqual(op._ps_size_vram(payload2, "qwen2.5:14b-8k"), 9216)

    def test_ps_size_vram_missing_or_junk(self):
        # Model not loaded -> None; entry without the field -> None;
        # unparseable value -> None (advisory never fires on doubt).
        self.assertIsNone(op._ps_size_vram({"models": []}, "qwen2.5:14b-8k"))
        self.assertIsNone(op._ps_size_vram(
            {"models": [{"name": "qwen2.5:14b-8k"}]}, "qwen2.5:14b-8k"))
        self.assertIsNone(op._ps_size_vram(
            {"models": [{"name": "qwen2.5:14b-8k", "size_vram": "garbage"}]},
            "qwen2.5:14b-8k"))
        self.assertIsNone(op._ps_size_vram(
            {"models": [{"name": "qwen2.5:14b-8k", "size_vram": None}]},
            "qwen2.5:14b-8k"))

    # ---- compute_offloaded pure advisory ---------------------------------

    def test_compute_offloaded_table(self):
        # R1928 anchor shape: resident, 1843 MiB vs 9000 envelope -> True.
        self.assertTrue(op.compute_offloaded(True, 1843, 9000))
        # Fully resident: at/above half the footprint -> False.
        self.assertFalse(op.compute_offloaded(True, 9216, 9000))
        # Boundary is strict: 4499 < 4500 -> True; exactly 4500 -> False.
        self.assertTrue(op.compute_offloaded(True, 4499, 9000))
        self.assertFalse(op.compute_offloaded(True, 4500, 9000))
        # Not resident / unreadable size / unknown footprint -> False.
        self.assertFalse(op.compute_offloaded(False, 1843, 9000))
        self.assertFalse(op.compute_offloaded(True, None, 9000))
        self.assertFalse(op.compute_offloaded(True, 1843, 0))

    # ---- main() json surfaces --------------------------------------------

    def test_main_json_offloaded_resident_reading(self):
        calls = {"flights": 0}
        self._flight_timeout(calls)
        self._ps_entry(self.OFFLOADED_BYTES)
        rc, out = self._run(["--json"])
        self.assertEqual(rc, 2)
        line = json.loads(out.strip())
        # Advisory columns carry the reading the pre-check already had...
        self.assertEqual(line["ps_size_vram"], 1843)
        self.assertTrue(line["offloaded_resident"])
        # ...while flight/face semantics stay exactly where they were.
        self.assertEqual(line["face"], "busy-contended")
        self.assertEqual(line["precheck"], "resident")
        self.assertEqual(calls["flights"], 1)  # skip semantics untouched

    def test_main_json_full_resident_not_offloaded(self):
        calls = {"flights": 0}
        self._flight_timeout(calls)
        self._ps_entry(self.RESIDENT_BYTES)
        rc, out = self._run(["--json"])
        self.assertEqual(rc, 2)
        line = json.loads(out.strip())
        self.assertEqual(line["ps_size_vram"], 9216)
        self.assertFalse(line["offloaded_resident"])
        self.assertEqual(line["precheck"], "resident")

    def test_main_json_resident_entry_without_size_is_null_not_offloaded(self):
        calls = {"flights": 0}
        self._flight_timeout(calls)
        self._ps_resident_no_size()
        rc, out = self._run(["--json"])
        self.assertEqual(rc, 2)
        line = json.loads(out.strip())
        self.assertIsNone(line["ps_size_vram"])
        self.assertFalse(line["offloaded_resident"])
        self.assertEqual(line["precheck"], "resident")

    def test_main_offloaded_advisory_ignores_cold_skip_override(self):
        # The --cold-skip-free-mb knob owns the skip decision only; the
        # advisory always uses the per-model footprint estimate.
        calls = {"flights": 0}
        self._flight_timeout(calls)
        self._ps_entry(self.OFFLOADED_BYTES)
        rc, out = self._run(["--json", "--cold-skip-free-mb", "99999"])
        self.assertEqual(rc, 2)
        self.assertTrue(json.loads(out.strip())["offloaded_resident"])

    def test_main_no_precheck_json_has_no_ps_columns(self):
        # Legacy call surface: --no-precheck runs no /api/ps read at all,
        # so no precheck-derived fields appear (existing contract).
        calls = {"flights": 0}
        self._flight_timeout(calls)

        def ps_spy(base_url, timeout):
            raise AssertionError("ps must not be queried under --no-precheck")
        op._http_get_ps = ps_spy
        rc, out = self._run(["--json", "--no-precheck"])
        self.assertEqual(rc, 2)
        line = json.loads(out.strip())
        self.assertNotIn("precheck", line)
        self.assertNotIn("ps_size_vram", line)
        self.assertNotIn("offloaded_resident", line)

    def test_main_skip_path_json_carries_null_evidence_columns(self):
        # Schema-uniform: the cold-skip path (ps confirmed not resident)
        # also carries the columns, honestly null/false.
        calls = {"flights": 0}
        self._flight_timeout(calls)
        op._http_get_ps = lambda base_url, timeout: _FakeResp(
            json.dumps({"models": []}).encode("utf-8"))
        op._nvidia_smi_free_query = lambda: "12288, 7547\n"  # free 4741 < 9000
        rc, out = self._run(["--json"])
        self.assertEqual(rc, 2)
        line = json.loads(out.strip())
        self.assertEqual(line["status"], "skipped-not-resident")
        self.assertIsNone(line["ps_size_vram"])
        self.assertFalse(line["offloaded_resident"])
        self.assertEqual(calls["flights"], 0)

    # ---- ledger row surfaces ---------------------------------------------

    def test_ledger_row_carries_ps_evidence_columns(self):
        calls = {"flights": 0}
        self._flight_timeout(calls)
        self._ps_entry(self.OFFLOADED_BYTES)
        path = os.path.join(self.tmp, "size-ledger.jsonl")
        rc, _ = self._run(["--ledger", path])
        self.assertEqual(rc, 2)
        with open(path, encoding="utf-8") as fh:
            row = json.loads(fh.read().splitlines()[0])
        self.assertEqual(row["ps_size_vram"], 1843)
        self.assertTrue(row["offloaded_resident"])
        self.assertEqual(row["face"], "busy-contended")

    def test_ledger_row_ps_unavailable_keeps_exact_shape(self):
        # tech#52 exact-shape contract: rows without a real ps read stay
        # byte-stable (no advisory columns bolted on).
        calls = {"flights": 0}
        self._flight_timeout(calls)
        op._http_get_ps = lambda base_url, timeout: (_ for _ in ()).throw(
            urllib.error.URLError("connection refused"))
        path = os.path.join(self.tmp, "nops-ledger.jsonl")
        rc, _ = self._run(["--ledger", path])
        self.assertEqual(rc, 2)
        with open(path, encoding="utf-8") as fh:
            row = json.loads(fh.read().splitlines()[0])
        self.assertEqual(
            set(row.keys()),
            {"ts", "rc", "status", "http_status", "model",
             "gpu_util", "gpu_mem", "face"})


if __name__ == "__main__":
    unittest.main()
