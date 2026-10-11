"""Tests for src/os/fire_consume.py (tech#112; R1999 delivery).

All hermetic: the card runner and the launcher are injected seams. No
real card cycle, no real subprocess dispatch, no GPU. CLI tests patch
real_run_card/real_launch/append_ledger_row at module level (main()
resolves them as module globals).
"""

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "fire_consume",
    os.path.join(os.path.dirname(__file__), "..", "src", "os",
                 "fire_consume.py"),
)
consumer = importlib.util.module_from_spec(_SPEC)
sys.modules["fire_consume"] = consumer
_SPEC.loader.exec_module(consumer)


def _fire_card(expires_at=9999999999):
    return {"card": "fire_window_card", "verdict": "fire",
            "path": "B-eviction-credit", "reasons": [],
            "expires_at": expires_at, "ts": "2026-10-11 20:34:07"}


class DecideTests(unittest.TestCase):
    def test_error_verdict_fail_closed(self):
        action, reason, rc = consumer.decide(
            {"verdict": "error", "reasons": ["child failed"]}, 100)
        self.assertEqual((action, rc), ("error", 2))
        self.assertIn("error", reason)

    def test_missing_verdict_fail_closed(self):
        action, _, rc = consumer.decide({}, 100)
        self.assertEqual((action, rc), ("error", 2))

    def test_no_fire_card_cites_reasons(self):
        action, reason, rc = consumer.decide(
            {"verdict": "no-fire", "reasons": ["gate-static-no-go"]},
            100)
        self.assertEqual((action, rc), ("no-fire", 1))
        self.assertIn("gate-static-no-go", reason)

    def test_fire_without_expires_at_fail_closed(self):
        card = _fire_card()
        del card["expires_at"]
        action, reason, rc = consumer.decide(card, 100)
        self.assertEqual((action, rc), ("error", 2))
        self.assertIn("expires_at", reason)

    def test_fire_at_expiry_is_stale_never_launches(self):
        # expires_at - margin == now -> stale (margin never negative)
        card = _fire_card(expires_at=102)
        action, reason, rc = consumer.decide(card, 100)
        self.assertEqual((action, rc), ("stale", 1))

    def test_fire_inside_margin_is_stale(self):
        # now + margin >= expires_at: only 1s of window left -> stale
        card = _fire_card(expires_at=103)
        action, _, rc = consumer.decide(card, 101)
        self.assertEqual((action, rc), ("stale", 1))

    def test_fire_fresh_launches(self):
        card = _fire_card(expires_at=10000)
        action, reason, rc = consumer.decide(card, 100)
        self.assertEqual((action, rc), ("launch", 0))
        self.assertEqual(reason, "fire-fresh")


class LedgerRowTests(unittest.TestCase):
    def test_appends_jsonl_and_creates_parents(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "deep" / "ledger.jsonl"
            consumer.append_ledger_row(path, {"a": 1})
            consumer.append_ledger_row(path, {"b": "值"})
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[0]), {"a": 1})
            self.assertEqual(json.loads(lines[1])["b"], "值")

    def test_ledger_failure_never_raises(self):
        # a FILE blocks the ledger's parent dir -> mkdir raises OSError
        # -> WARN to stderr, no exception escapes to the caller
        with tempfile.TemporaryDirectory() as tmp:
            blocker = Path(tmp) / "blocker"
            blocker.write_text("x", encoding="utf-8")
            consumer.append_ledger_row(
                blocker / "sub" / "ledger.jsonl", {"a": 1})


class CliTests(unittest.TestCase):
    def setUp(self):
        self._real_card = consumer.real_run_card
        self._real_launch = consumer.real_launch
        self._real_append = consumer.append_ledger_row
        self.tmp = tempfile.TemporaryDirectory()
        self.launch = Path(self.tmp.name) / "staged.py"
        self.launch.write_text("print('x')\n", encoding="utf-8")
        self.ledger = Path(self.tmp.name) / "ledger.jsonl"
        self.rows = []
        consumer.append_ledger_row = \
            lambda path, row: self.rows.append(row)

    def tearDown(self):
        consumer.real_run_card = self._real_card
        consumer.real_launch = self._real_launch
        consumer.append_ledger_row = self._real_append
        self.tmp.cleanup()

    def _run(self, extra=None):
        argv = ["--launch", str(self.launch),
                "--ledger", str(self.ledger)] + (extra or [])
        return consumer.main(argv)

    def test_no_fire_rc1_no_launch_no_row(self):
        consumer.real_run_card = lambda: {
            "verdict": "no-fire", "reasons": ["gate-static-no-go"],
            "ts": "t"}
        rc = self._run()
        self.assertEqual(rc, 1)
        self.assertEqual(len(self.rows), 1)
        self.assertFalse(self.rows[0]["launched"])

    def test_fire_fresh_dispatches_and_ledgers_pid(self):
        consumer.real_run_card = lambda: _fire_card(expires_at=10 ** 12)
        consumer.real_launch = lambda script: 4242
        rc = self._run()
        self.assertEqual(rc, 0)
        row = self.rows[0]
        self.assertTrue(row["launched"])
        self.assertEqual(row["launch_pid"], 4242)
        self.assertEqual(row["card_verdict"], "fire")

    def test_card_error_rc2(self):
        def boom():
            raise consumer.CardError("card failed: timeout")
        consumer.real_run_card = boom
        rc = self._run()
        self.assertEqual(rc, 2)
        self.assertEqual(self.rows, [])

    def test_launch_failure_rc2_fail_closed(self):
        consumer.real_run_card = lambda: _fire_card(expires_at=10 ** 12)

        def boom(script):
            raise OSError("no dice")
        consumer.real_launch = boom
        rc = self._run()
        self.assertEqual(rc, 2)
        self.assertEqual(self.rows[0]["action"], "error")
        self.assertFalse(self.rows[0]["launched"])

    def test_missing_launch_file_rc2_usage(self):
        rc = consumer.main(["--launch",
                            str(Path(self.tmp.name) / "nope.py")])
        self.assertEqual(rc, 2)

    def test_non_py_launch_file_rc2_usage(self):
        bad = Path(self.tmp.name) / "staged.ps1"
        bad.write_text("echo x", encoding="utf-8")
        rc = consumer.main(["--launch", str(bad)])
        self.assertEqual(rc, 2)

    def test_json_flag_single_line(self):
        import contextlib
        import io
        consumer.real_run_card = lambda: {
            "verdict": "no-fire", "reasons": [], "ts": "t"}
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = self._run(extra=["--json"])
        self.assertEqual(rc, 1)
        payload = json.loads(buf.getvalue().strip())
        self.assertEqual(payload["tool"], "fire_consume")
        self.assertEqual(payload["card_verdict"], "no-fire")


class StagedLauncherContractTests(unittest.TestCase):
    """The SC-005-06 staged launcher must stay turnkey: correct repo
    depth, correct material path, gpu-guard on, 1500s window (the
    next GO's consumption depends on none of these drifting)."""

    LAUNCHER = Path(__file__).resolve().parents[1].joinpath(
        "data", "storylines", "audio", "sc005-06-v1-tmp", "s1_call.py")

    def test_launcher_exists_and_points_at_06_material(self):
        text = self.LAUNCHER.read_text(encoding="utf-8")
        self.assertIn("SC-005-06-v1-s1-material.md", text)
        self.assertIn("--gpu-guard", text)
        self.assertIn('"1500"', text)
        self.assertIn("S1-script", text)

    def test_launcher_repo_depth_is_four_up(self):
        # data/storylines/audio/sc005-06-v1-tmp/s1_call.py -> repo root
        self.assertEqual(
            self.LAUNCHER.resolve().parents[4].name, "BigStream")


if __name__ == "__main__":
    unittest.main()
