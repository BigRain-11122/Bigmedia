"""Tests for src/os/comfy_activity.py (tech#106; R1987 delivery).

All hermetic: the powershell runner, queue fetcher, and sleeper are
injected seams. No real PS query, no HTTP, no GPU. CLI tests patch
run_probe/append_ledger_row at module level (main() resolves them as
module globals).
"""

import contextlib
import datetime
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "comfy_activity",
    os.path.join(os.path.dirname(__file__), "..", "src", "os",
                 "comfy_activity.py"),
)
probe = importlib.util.module_from_spec(_SPEC)
sys.modules["comfy_activity"] = probe
_SPEC.loader.exec_module(probe)


def _ps_stdout(pid, k, u):
    return json.dumps({"ProcessId": pid, "KernelModeTime": k,
                       "UserModeTime": u})


class ParsePsCpuTests(unittest.TestCase):
    def test_single_object(self):
        self.assertEqual(probe.parse_ps_cpu(_ps_stdout(58200, 100, 50)),
                         {58200: 150})

    def test_array_two_processes(self):
        raw = "[%s, %s]" % (_ps_stdout(1, 10, 5), _ps_stdout(2, 20, 5))
        self.assertEqual(probe.parse_ps_cpu(raw), {1: 15, 2: 25})

    def test_empty_stdout_means_zero_processes(self):
        self.assertEqual(probe.parse_ps_cpu("  \n"), {})

    def test_junk_is_unreadable(self):
        self.assertIsNone(probe.parse_ps_cpu("not json"))
        self.assertIsNone(probe.parse_ps_cpu("[1,2,3]"))

    def test_missing_keys_are_unreadable(self):
        self.assertIsNone(probe.parse_ps_cpu(json.dumps({"ProcessId": 1})))
        self.assertIsNone(probe.parse_ps_cpu(
            json.dumps({"ProcessId": "x", "KernelModeTime": 1,
                        "UserModeTime": 1})))

    def test_none_is_unreadable(self):
        self.assertIsNone(probe.parse_ps_cpu(None))


class CpuFaceTests(unittest.TestCase):
    def _runner_script(self, outputs):
        calls = []

        def run(cmd):
            calls.append(cmd)
            return outputs[len(calls) - 1]

        return run, calls

    def test_delta_over_intersection(self):
        run, calls = self._runner_script([
            (True, _ps_stdout(58200, 10000000, 5000000)),
            (True, _ps_stdout(58200, 10030000, 5002000)),
        ])
        face = probe.read_cpu_face(runner=run, sleeper=lambda s: None)
        self.assertEqual(face["status"], "ok")
        # delta = (10030000+5002000) - (10000000+5000000) = 32000 x100ns
        self.assertEqual(face["delta_ms"], 3.2)
        self.assertEqual(face["pids"], [58200])
        self.assertFalse(face["pid_change"])

    def test_pid_set_change_annotated(self):
        run, _ = self._runner_script([
            (True, _ps_stdout(1, 10, 10)),
            (True, "[%s, %s]" % (_ps_stdout(1, 15, 10), _ps_stdout(7, 0, 0))),
        ])
        face = probe.read_cpu_face(runner=run, sleeper=lambda s: None)
        self.assertEqual(face["status"], "ok")
        self.assertTrue(face["pid_change"])
        self.assertEqual(face["pids"], [1, 7])

    def test_both_empty_is_server_down(self):
        run, _ = self._runner_script([(True, ""), (True, "")])
        face = probe.read_cpu_face(runner=run, sleeper=lambda s: None)
        self.assertEqual(face["status"], "empty")

    def test_runner_failure_is_unreadable(self):
        run, _ = self._runner_script([(False, ""), (True, "")])
        face = probe.read_cpu_face(runner=run, sleeper=lambda s: None)
        self.assertEqual(face["status"], "unreadable")

    def test_second_parse_failure_is_unreadable(self):
        run, _ = self._runner_script([(True, _ps_stdout(1, 1, 1)),
                                      (True, "junk")])
        face = probe.read_cpu_face(runner=run, sleeper=lambda s: None)
        self.assertEqual(face["status"], "unreadable")

    def test_sleeper_gets_interval(self):
        got = []
        run, _ = self._runner_script([(True, ""), (True, "")])
        probe.read_cpu_face(runner=run, sleeper=got.append, interval=7)
        self.assertEqual(got, [7])


class QueueFaceTests(unittest.TestCase):
    def _fetch_ok(self, running=0, pending=0):
        body = json.dumps({"queue_running": [None] * running,
                           "queue_pending": [None] * pending}).encode()
        return lambda url, timeout: (200, body)

    def test_counts(self):
        face = probe.read_queue_face(fetcher=self._fetch_ok(1, 2))
        self.assertEqual(face, {"status": "ok", "running": 1, "pending": 2})

    def test_empty_queue(self):
        face = probe.read_queue_face(fetcher=self._fetch_ok(0, 0))
        self.assertEqual(face, {"status": "ok", "running": 0, "pending": 0})

    def test_transport_failure_unreadable(self):
        def boom(url, timeout):
            raise ConnectionRefusedError
        self.assertEqual(
            probe.read_queue_face(fetcher=boom)["status"], "unreadable")

    def test_non_200_unreadable(self):
        self.assertEqual(probe.read_queue_face(
            fetcher=lambda u, t: (404, b"{}"))["status"], "unreadable")

    def test_bad_shape_unreadable(self):
        for body in (b"not json", b"[1]", b'{"queue_running": 3}',
                     b'{"queue_running": "x", "queue_pending": []}'):
            self.assertEqual(probe.read_queue_face(
                fetcher=lambda u, t: (200, body))["status"], "unreadable")


class OutputFaceTests(unittest.TestCase):
    """tech#136 wave-gap face: fresh entries in the ComfyUI output
    tree attest a live client iteration loop (R2075: queue 0/0 +
    cpu-quiet at 20:44 while output took 34 files in three waves)."""

    NOW = datetime.datetime(2026, 10, 12, 20, 44, 0)

    def _touch(self, path, age_s):
        path.write_text("x", encoding="utf-8")
        stamp = self.NOW.timestamp() - age_s
        os.utime(path, (stamp, stamp))

    def test_fresh_file_attests_recent(self):
        with tempfile.TemporaryDirectory() as td:
            self._touch(Path(td) / "kf_00045.png", 240)
            face = probe.read_output_face(td, recency_s=900, now=self.NOW)
            self.assertEqual(face["status"], "ok")
            self.assertEqual(face["recent"], 1)
            self.assertEqual(face["newest_age_s"], 240.0)

    def test_cold_file_zero_recent_with_age(self):
        with tempfile.TemporaryDirectory() as td:
            self._touch(Path(td) / "old.png", 3600)
            face = probe.read_output_face(td, recency_s=900, now=self.NOW)
            self.assertEqual(face["status"], "ok")
            self.assertEqual(face["recent"], 0)
            self.assertEqual(face["newest_age_s"], 3600.0)

    def test_fresh_subdir_mtime_carries_wave_signal(self):
        # live shape: batch writes output/kf_bma/*.png; the top-level
        # files stay cold, the subdir mtime is what goes fresh
        with tempfile.TemporaryDirectory() as td:
            self._touch(Path(td) / "old_top.png", 7200)
            sub = Path(td) / "kf_bma"
            sub.mkdir()
            (sub / "shot_01.png").write_text("x", encoding="utf-8")
            # explicit dir-mtime stamp: the OS would stamp it with the
            # real wall clock, but the face reads it against self.NOW
            stamp = self.NOW.timestamp() - 300
            os.utime(sub, (stamp, stamp))
            face = probe.read_output_face(td, recency_s=900, now=self.NOW)
            self.assertEqual(face["status"], "ok")
            self.assertEqual(face["recent"], 1)
            self.assertEqual(face["newest_age_s"], 300.0)

    def test_empty_dir_ok_recent_zero_no_age(self):
        with tempfile.TemporaryDirectory() as td:
            face = probe.read_output_face(td, recency_s=900, now=self.NOW)
            self.assertEqual(face["status"], "ok")
            self.assertEqual(face["recent"], 0)
            self.assertIsNone(face["newest_age_s"])

    def test_missing_dir_unreadable(self):
        face = probe.read_output_face(
            Path(tempfile.gettempdir()) / "no-such-comfy-tree-xyz",
            recency_s=900, now=self.NOW)
        self.assertEqual(face["status"], "unreadable")

    def test_none_dir_unreadable(self):
        self.assertEqual(probe.read_output_face(None)["status"],
                         "unreadable")

    def test_recency_boundary_strict(self):
        with tempfile.TemporaryDirectory() as td:
            # exactly at recency -> fresh (<=); one second older -> not
            self._touch(Path(td) / "a.png", 900)
            self._touch(Path(td) / "b.png", 901)
            face = probe.read_output_face(td, recency_s=900, now=self.NOW)
            self.assertEqual(face["recent"], 1)

    def _stamp(self, path, age_s):
        stamp = self.NOW.timestamp() - age_s
        os.utime(path, (stamp, stamp))

    def test_two_deep_fresh_dir_top_cold_attests(self):
        # tech#138 live shape (MV i2v lane): output/<a>/<b>/file bumps
        # only <b>; top-level <a> stays cold -- one-level descent into
        # cold top dirs recovers the wave signal
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._touch(root / "old_top.png", 7200)
            a = root / "bmc"; a.mkdir()
            b = a / "i2v"; b.mkdir()
            (b / "clip_01.mp4").write_text("x", encoding="utf-8")
            self._stamp(a, 7200)
            self._stamp(b, 300)
            face = probe.read_output_face(td, recency_s=900, now=self.NOW)
            self.assertEqual(face["status"], "ok")
            self.assertEqual(face["recent"], 1)
            self.assertEqual(face["newest_age_s"], 300.0)

    def test_two_deep_fresh_file_under_cold_dir_attests(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            a = root / "wave"; a.mkdir()
            (a / "shot_07.png").write_text("x", encoding="utf-8")
            self._stamp(a, 7200)
            self._stamp(a / "shot_07.png", 240)
            face = probe.read_output_face(td, recency_s=900, now=self.NOW)
            self.assertEqual(face["status"], "ok")
            self.assertEqual(face["recent"], 1)
            self.assertEqual(face["newest_age_s"], 240.0)

    def test_two_deep_all_cold_no_recent(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            a = root / "bmc"; a.mkdir()
            b = a / "i2v"; b.mkdir()
            self._stamp(b, 3600)
            self._stamp(a, 5000)
            face = probe.read_output_face(td, recency_s=900, now=self.NOW)
            self.assertEqual(face["recent"], 0)
            self.assertEqual(face["newest_age_s"], 3600.0)

    def test_fresh_top_dir_not_descended_regression_lock(self):
        # design lock (tech#138): a FRESH top-level dir attests on its
        # own mtime and is not descended (wave-time cost cap) -- a
        # fresher child must not change the read
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sub = root / "kf_bma"; sub.mkdir()
            (sub / "shot_01.png").write_text("x", encoding="utf-8")
            self._stamp(sub, 300)
            self._stamp(sub / "shot_01.png", 60)
            face = probe.read_output_face(td, recency_s=900, now=self.NOW)
            self.assertEqual(face["recent"], 1)
            self.assertEqual(face["newest_age_s"], 300.0)


class VerdictTests(unittest.TestCase):
    def _q(self, status="ok", running=0, pending=0):
        return {"status": status, "running": running, "pending": pending}

    def _c(self, status="ok", delta=0.0):
        return {"status": status, "delta_ms": delta}

    def test_queue_running_is_active(self):
        v, notes = probe.compute_verdict(self._q(running=1),
                                         self._c(delta=500.0))
        self.assertEqual(v, "active")
        self.assertEqual(notes, [])

    def test_queue_pending_is_active(self):
        v, _ = probe.compute_verdict(self._q(pending=2), self._c())
        self.assertEqual(v, "active")

    def test_stale_render_candidate_note(self):
        v, notes = probe.compute_verdict(self._q(running=1),
                                         self._c(delta=5.0))
        self.assertEqual(v, "active")
        self.assertEqual(notes, ["stale-render-candidate"])

    def test_active_running_with_healthy_cpu_no_stale_note(self):
        v, notes = probe.compute_verdict(self._q(running=1),
                                         self._c(delta=500.0))
        self.assertEqual(v, "active")
        self.assertEqual(notes, [])

    def test_pending_only_no_stale_note(self):
        v, notes = probe.compute_verdict(self._q(pending=3),
                                         self._c(delta=5.0))
        self.assertEqual(v, "active")
        self.assertEqual(notes, [])

    def test_cpu_delta_over_threshold_is_active(self):
        v, _ = probe.compute_verdict(self._q(), self._c(delta=300.0))
        self.assertEqual(v, "active")

    def test_cpu_empty_is_quiet_server_down(self):
        v, notes = probe.compute_verdict(self._q(), {"status": "empty"})
        self.assertEqual(v, "quiet")
        self.assertEqual(notes, ["server-down"])

    def test_cpu_empty_overrides_unreadable_queue(self):
        v, notes = probe.compute_verdict(self._q(status="unreadable"),
                                         {"status": "empty"})
        self.assertEqual(v, "quiet")
        self.assertEqual(notes, ["server-down"])

    def test_coherent_idle_is_quiet(self):
        v, notes = probe.compute_verdict(self._q(), self._c(delta=10.0))
        self.assertEqual(v, "quiet")
        self.assertEqual(notes, [])

    def test_small_delta_with_unreadable_queue_is_error(self):
        v, _ = probe.compute_verdict(self._q(status="unreadable"),
                                     self._c(delta=10.0))
        self.assertIsNone(v)

    def test_unreadable_cpu_with_idle_queue_is_error(self):
        v, _ = probe.compute_verdict(self._q(), {"status": "unreadable"})
        self.assertIsNone(v)

    def test_unreadable_cpu_with_active_queue_still_active(self):
        v, _ = probe.compute_verdict(self._q(running=1),
                                     {"status": "unreadable"})
        self.assertEqual(v, "active")

    def test_both_unreadable_is_error(self):
        v, _ = probe.compute_verdict(self._q(status="unreadable"),
                                     {"status": "unreadable"})
        self.assertIsNone(v)

    def test_threshold_boundary_strict(self):
        # at threshold = active (>=), below = falls through
        v, _ = probe.compute_verdict(self._q(), self._c(delta=299.999))
        self.assertEqual(v, "quiet")
        v, _ = probe.compute_verdict(self._q(), self._c(delta=300.0))
        self.assertEqual(v, "active")

    def _o(self, status="ok", recent=0):
        return {"status": status, "recent": recent}

    def test_fresh_output_flips_quiet_to_active_wave_gap(self):
        # tech#136 live shape: queue 0/0 + cpu-quiet + fresh output =
        # the client iteration loop is alive in a wave gap
        v, notes = probe.compute_verdict(self._q(), self._c(delta=10.0),
                                         output_face=self._o(recent=3))
        self.assertEqual(v, "active")
        self.assertEqual(notes, ["wave-gap-recent-output"])

    def test_cold_output_keeps_two_face_quiet(self):
        v, notes = probe.compute_verdict(self._q(), self._c(delta=10.0),
                                         output_face=self._o(recent=0))
        self.assertEqual(v, "quiet")
        self.assertEqual(notes, [])

    def test_unreadable_output_keeps_two_face_quiet(self):
        # other-lane installs (no such output dir) must not fail-closed
        v, _ = probe.compute_verdict(self._q(), self._c(delta=10.0),
                                     output_face=self._o(status="unreadable"))
        self.assertEqual(v, "quiet")

    def test_none_output_face_keeps_two_face_quiet(self):
        v, _ = probe.compute_verdict(self._q(), self._c(delta=10.0),
                                     output_face=None)
        self.assertEqual(v, "quiet")

    def test_fresh_output_beats_server_down_empty_cpu(self):
        # R1986 family: GO consumed at a server-down instant, wave
        # re-ignited seconds later. Fresh output + cpu empty = the loop
        # restarts its server mid-wave -> conservative active.
        v, notes = probe.compute_verdict(
            self._q(), {"status": "empty"},
            output_face=self._o(recent=1))
        self.assertEqual(v, "active")
        self.assertEqual(notes, ["wave-gap-recent-output"])

    def test_fresh_output_active_even_with_unreadable_cpu(self):
        # single positive attestation stands alone (family law)
        v, _ = probe.compute_verdict(
            self._q(status="unreadable"), {"status": "unreadable"},
            output_face=self._o(recent=2))
        self.assertEqual(v, "active")


class RunProbeTests(unittest.TestCase):
    def test_composition_and_rc(self):
        result = probe.run_probe(
            queue_fetcher=lambda u, t: (200, json.dumps(
                {"queue_running": [], "queue_pending": []}).encode()),
            ps_runner=lambda cmd: (True, ""),
            sleeper=lambda s: None)
        self.assertEqual(result["verdict"], "quiet")
        self.assertEqual(result["rc"], 0)
        self.assertEqual(result["probe"], "comfy_activity")
        self.assertIn("queue", result["faces"])
        self.assertIn("cpu", result["faces"])
        # hermeticity: default output_dir=None never touches the real
        # ComfyUI tree (a live MV batch would otherwise flip this
        # verdict to active and make the suite flaky)
        self.assertNotIn("output", result["faces"])

    def test_output_dir_face_wired_when_passed(self):
        with tempfile.TemporaryDirectory() as td:
            fresh = Path(td) / "kf_00046.png"
            fresh.write_text("x", encoding="utf-8")
            result = probe.run_probe(
                queue_fetcher=lambda u, t: (200, json.dumps(
                    {"queue_running": [], "queue_pending": []}).encode()),
                ps_runner=lambda cmd: (True, ""),
                sleeper=lambda s: None,
                output_dir=td)
            self.assertIn("output", result["faces"])
            self.assertEqual(result["faces"]["output"]["recent"], 1)
            self.assertEqual(result["verdict"], "active")
            self.assertIn("wave-gap-recent-output", result["notes"])

    def test_active_composition_rc(self):
        result = probe.run_probe(
            queue_fetcher=lambda u, t: (200, json.dumps(
                {"queue_running": [{}], "queue_pending": []}).encode()),
            ps_runner=lambda cmd: (True, ""),
            sleeper=lambda s: None)
        self.assertEqual(result["verdict"], "active")
        self.assertEqual(result["rc"], 1)

    def test_error_composition_rc(self):
        def boom(url, timeout):
            raise OSError
        result = probe.run_probe(queue_fetcher=boom,
                                 ps_runner=lambda cmd: (False, ""),
                                 sleeper=lambda s: None)
        self.assertIsNone(result["verdict"])
        self.assertEqual(result["rc"], 2)


class LedgerTests(unittest.TestCase):
    def test_row_lands_with_field_set(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sub" / "ledger.jsonl"
            result = probe.run_probe(
                queue_fetcher=lambda u, t: (200, json.dumps(
                    {"queue_running": [], "queue_pending": []}).encode()),
                ps_runner=lambda cmd: (True, ""),
                sleeper=lambda s: None)
            probe.append_ledger_row(path, result)
            row = json.loads(path.read_text(encoding="utf-8").strip())
            self.assertEqual(sorted(row.keys()), sorted(
                ["ts", "verdict", "rc", "running", "pending",
                 "cpu_delta_ms", "pids", "output_recent"]))
            self.assertEqual(row["verdict"], "quiet")
            self.assertEqual(row["rc"], 0)
            self.assertEqual(row["running"], 0)
            self.assertEqual(row["pids"], [])
            self.assertIsNone(row["output_recent"])

    def test_error_row_still_lands_with_nulls(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            result = probe.run_probe(
                queue_fetcher=lambda u, t: (_ for _ in ()).throw(OSError),
                ps_runner=lambda cmd: (False, ""),
                sleeper=lambda s: None)
            probe.append_ledger_row(path, result)
            row = json.loads(path.read_text(encoding="utf-8").strip())
            self.assertIsNone(row["verdict"])
            self.assertEqual(row["rc"], 2)
            self.assertIsNone(row["running"])
            self.assertIsNone(row["cpu_delta_ms"])

    def test_no_flag_zero_writes(self):
        # ledger only writes via append_ledger_row call sites; probe run
        # alone must never touch the default ledger path.
        before = probe.DEFAULT_LEDGER.exists()
        probe.run_probe(
            queue_fetcher=lambda u, t: (200, b"{}"),   # unreadable shape
            ps_runner=lambda cmd: (True, ""),
            sleeper=lambda s: None)
        self.assertEqual(probe.DEFAULT_LEDGER.exists(), before)


class CliTests(unittest.TestCase):
    @contextlib.contextmanager
    def _patch(self, result, rows):
        def _run_probe(**kwargs):
            return result

        rows.appended = []
        orig = (probe.run_probe, probe.append_ledger_row)
        probe.run_probe = _run_probe
        probe.append_ledger_row = \
            lambda path, res: rows.appended.append(path)
        try:
            yield
        finally:
            probe.run_probe, probe.append_ledger_row = orig

    def test_json_line_and_rc_quiet(self):
        rows = type("R", (), {})()
        result = probe.run_probe(
            queue_fetcher=lambda u, t: (200, json.dumps(
                {"queue_running": [], "queue_pending": []}).encode()),
            ps_runner=lambda cmd: (True, ""),
            sleeper=lambda s: None)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            with contextlib.ExitStack() as stack:
                stack.enter_context(self._patch(result, rows))
                rc = probe.main(["--json"])
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["verdict"], "quiet")

    def test_ledger_flag_appends(self):
        rows = type("R", (), {})()
        result = probe.run_probe(
            queue_fetcher=lambda u, t: (200, json.dumps(
                {"queue_running": [{}], "queue_pending": []}).encode()),
            ps_runner=lambda cmd: (True, ""),
            sleeper=lambda s: None)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            with contextlib.ExitStack() as stack:
                stack.enter_context(self._patch(result, rows))
                rc = probe.main(["--ledger", "x.jsonl"])
        self.assertEqual(rc, 1)
        self.assertEqual(rows.appended, ["x.jsonl"])

    def test_bad_sample_interval_rejected(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), \
                contextlib.redirect_stderr(io.StringIO()):
            rc = probe.main(["--sample-interval", "-1"])
        self.assertEqual(rc, 2)

    def test_bad_output_recency_rejected(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), \
                contextlib.redirect_stderr(io.StringIO()):
            rc = probe.main(["--output-recency-s", "-5"])
        self.assertEqual(rc, 2)

    def test_human_output_notes_line(self):
        result = {
            "probe": "comfy_activity", "ts": "t", "verdict": "active",
            "rc": 1, "sample_interval_s": 4, "cpu_threshold_ms": 300,
            "stale_threshold_ms": 100,
            "notes": ["stale-render-candidate"],
            "faces": {"queue": {"status": "ok", "running": 1, "pending": 0},
                      "cpu": {"status": "ok", "delta_ms": 5.0,
                              "pids": [58200], "pid_change": False}},
        }
        rows = type("R", (), {})()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            with contextlib.ExitStack() as stack:
                stack.enter_context(self._patch(result, rows))
                rc = probe.main([])
        self.assertEqual(rc, 1)
        self.assertIn("stale-render-candidate", buf.getvalue())
        self.assertIn("running=1", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
