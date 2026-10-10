# -*- coding: utf-8 -*-
"""Tests for expert_retry_loop (state/queue/tech#91, R1949).

Hermetic throughout: the subprocess runner, sleeper and log sink are all
injected; no real call_expert flight, no real sleep, no GPU contact.

Anchors:
- R1948 ps1 production shape: defer attempts sweep an interval, first
  non-DEFER breaks the loop and propagates its exit code;
- exhaustion exits 4 (LOOP-EXHAUSTED), a distinct space from call_expert
  codes (0 success / 2 usage / 3 call-fail / 5 defer);
- usage-class failures (rc=2, e.g. unknown expert / missing material) stop
  the loop immediately -- never retried;
- no sleep after the final attempt (defer or not).
"""
import io
import os
import sys
import unittest
import unittest.mock  # noqa: F401  (patch used in CLI tests)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src", "os"))

import expert_retry_loop as erl  # noqa: E402


class _Recorder(object):
    """Fake runner/sleep/log triple capturing loop behavior."""

    def __init__(self, rcs):
        self._rcs = list(rcs)
        self.calls = []
        self.sleeps = []
        self.lines = []

    def runner(self, argv):
        self.calls.append(list(argv))
        rc = self._rcs.pop(0) if self._rcs else 0
        return rc, "verdict text" if rc != erl.DEFER_RC else "DEFER reason"

    def sleeper(self, seconds):
        self.sleeps.append(seconds)

    def log(self, line):
        self.lines.append(line)


class ArgvTests(unittest.TestCase):
    def test_guard_on_and_timeout_explicit(self):
        argv = erl.build_argv("E4-audience", "m.md", 1500, "src/call_expert.py")
        self.assertIn("--gpu-guard", argv)
        self.assertIn("--timeout", argv)
        self.assertIn("1500", argv)
        self.assertIn("E4-audience", argv)
        self.assertIn("m.md", argv)


class LoopCoreTests(unittest.TestCase):
    def test_first_attempt_lands_propagates_rc(self):
        rec = _Recorder([0])
        rc = erl.retry_loop("E", "m.md", 1500, 45.0, 24,
                            runner=rec.runner, sleeper=rec.sleeper, log=rec.log)
        self.assertEqual(rc, 0)
        self.assertEqual(len(rec.calls), 1)       # no retry after landing
        self.assertEqual(rec.sleeps, [])          # no sleep after landing
        self.assertTrue(any("non-defer rc=0" in ln for ln in rec.lines))
        self.assertTrue(any("verdict text" in ln for ln in rec.lines))

    def test_defers_then_lands(self):
        rec = _Recorder([5, 5, 5, 0])
        rc = erl.retry_loop("E", "m.md", 1500, 45.0, 24,
                            runner=rec.runner, sleeper=rec.sleeper, log=rec.log)
        self.assertEqual(rc, 0)
        self.assertEqual(len(rec.calls), 4)
        self.assertEqual(rec.sleeps, [45.0, 45.0, 45.0])
        self.assertEqual(sum(1 for ln in rec.lines if "DEFER" in ln), 3)

    def test_exhausted_rc4_distinct_space(self):
        rec = _Recorder([5, 5, 5])
        rc = erl.retry_loop("E", "m.md", 1500, 45.0, 3,
                            runner=rec.runner, sleeper=rec.sleeper, log=rec.log)
        self.assertEqual(rc, erl.EXHAUSTED_RC)
        self.assertEqual(rc, 4)
        self.assertNotIn(rc, (0, 2, 3, 5))        # distinct from call_expert codes
        self.assertEqual(len(rec.calls), 3)
        self.assertEqual(rec.sleeps, [45.0, 45.0])  # no sleep after final attempt
        self.assertTrue(any("exhausted" in ln for ln in rec.lines))

    def test_usage_error_stops_immediately_no_retry(self):
        rec = _Recorder([2])
        rc = erl.retry_loop("E", "m.md", 1500, 45.0, 24,
                            runner=rec.runner, sleeper=rec.sleeper, log=rec.log)
        self.assertEqual(rc, 2)
        self.assertEqual(len(rec.calls), 1)       # never retried
        self.assertEqual(rec.sleeps, [])

    def test_call_fail_rc3_stops_and_propagates(self):
        rec = _Recorder([3])
        rc = erl.retry_loop("E", "m.md", 1500, 45.0, 24,
                            runner=rec.runner, sleeper=rec.sleeper, log=rec.log)
        self.assertEqual(rc, 3)

    def test_zero_interval_allowed_no_sleep_call(self):
        rec = _Recorder([5, 0])
        rc = erl.retry_loop("E", "m.md", 1500, 0.0, 24,
                            runner=rec.runner, sleeper=rec.sleeper, log=rec.log)
        self.assertEqual(rc, 0)
        self.assertEqual(rec.sleeps, [0.0])


class CliTests(unittest.TestCase):
    def _main(self, argv):
        buf = io.StringIO()
        stdout = sys.stdout
        sys.stdout = buf
        try:
            try:
                erl.main(argv)
            except SystemExit as exc:
                return exc.code, buf.getvalue()
            return 0, buf.getvalue()
        finally:
            sys.stdout = stdout

    def test_missing_required_args_rc2(self):
        rc, _ = self._main([])
        self.assertEqual(rc, 2)

    def test_bad_max_rc2_no_runner_flight(self):
        with unittest.mock.patch.object(erl, "retry_loop") as rl:  # noqa: F841
            rc, _ = self._main(["--expert", "E", "--material", "m.md", "--max", "0"])
        self.assertEqual(rc, 2)

    def test_bad_interval_rc2(self):
        rc, _ = self._main(["--expert", "E", "--material", "m.md", "--interval", "-1"])
        self.assertEqual(rc, 2)

    def test_cli_wires_seam_and_propagates(self):
        seen = {}

        def fake_loop(expert, material, timeout_s, interval_s, max_attempts):
            seen.update(expert=expert, material=material, timeout_s=timeout_s,
                        interval_s=interval_s, max_attempts=max_attempts)
            return 7

        orig = erl.retry_loop
        erl.retry_loop = fake_loop
        try:
            rc, _ = self._main(["--expert", "E4-audience", "--material", "m.md",
                                "--timeout", "900", "--interval", "10", "--max", "5"])
        finally:
            erl.retry_loop = orig
        self.assertEqual(rc, 7)
        self.assertEqual(seen["expert"], "E4-audience")
        self.assertEqual(seen["timeout_s"], 900)
        self.assertEqual(seen["interval_s"], 10.0)
        self.assertEqual(seen["max_attempts"], 5)


if __name__ == "__main__":
    unittest.main()
