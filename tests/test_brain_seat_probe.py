"""Unit tests for the brain seat probe (src/os/brain_seat_probe.py).

tech#378 (R2429): the seat's supervisor reports success while the seat
is dead, so the probe must answer three questions on its own - is the
wire alive, are the launcher's inputs on disk, is a CEO pause flag
explaining the silence - and leave one JSONL row per run. Nothing here
touches the network: health_ok is replaced by an injected result, and
the readiness side reads a temp ledger.

Run:
    python tests/test_brain_seat_probe.py
"""
import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "os"))

import brain_seat_probe as bsp  # noqa: E402
import readiness  # noqa: E402


def make_dir(case, prefix):
    d = Path(tempfile.mkdtemp(prefix=prefix))
    case.addCleanup(shutil.rmtree, d, ignore_errors=True)
    return d


def run_main(argv, alive, case):
    """Call bsp.main with a stubbed wire; returns (rc, stdout)."""
    original = bsp.health_ok
    bsp.health_ok = lambda *a, **k: alive
    case.addCleanup(setattr, bsp, "health_ok", original)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = bsp.main(["brain_seat_probe.py"] + argv)
    return rc, buf.getvalue()


class TestHealth(unittest.TestCase):
    def test_unreachable_is_not_an_exception(self):
        # a closed port must read as down, never raise
        self.assertFalse(bsp.health_ok("http://127.0.0.1:9/health", 0.2))


class TestMissingInputs(unittest.TestCase):
    def test_all_present(self):
        d = make_dir(self, "bs-seat-")
        a = d / "a.bin"
        a.write_bytes(b"x")
        self.assertEqual(bsp.missing_inputs([("model", str(a))]), [])

    def test_absent_named(self):
        d = make_dir(self, "bs-seat-")
        missing = bsp.missing_inputs(
            [("model", str(d / "nope.gguf")), ("exe", str(d / "nope.exe"))])
        self.assertEqual(missing, ["model", "exe"])


class TestClassify(unittest.TestCase):
    def test_alive_wins_over_everything(self):
        self.assertEqual(bsp.classify(True, ["model"], True),
                         bsp.REASON_ALIVE)

    def test_provisioning_before_pause(self):
        # a paused seat with missing files still wants the human action
        # named first: the pause flag alone would read as legitimate.
        self.assertIn("model", bsp.classify(False, ["model"], True))

    def test_pause_is_its_own_reason(self):
        self.assertEqual(bsp.classify(False, [], True), bsp.REASON_PAUSED)

    def test_plain_health(self):
        self.assertEqual(bsp.classify(False, [], False), bsp.REASON_HEALTH)


class TestLedger(unittest.TestCase):
    def test_row_shape(self):
        row = json.loads(bsp.probe_row(False, "health unreachable",
                                      ts="2026-10-24 06:00:00",
                                      missing=["model"], paused=False))
        self.assertFalse(row["alive"])
        self.assertEqual(row["ts"], "2026-10-24 06:00:00")
        self.assertEqual(row["reason"], "health unreachable")
        self.assertEqual(row["missing"], ["model"])
        self.assertIn("health_url", row)
        self.assertIn("paused", row)

    def test_latest_row_skips_noise(self):
        d = make_dir(self, "bs-seat-")
        p = d / "probe.jsonl"
        p.write_text('not json\n'
                     '{"alive": true, "reason": "alive"}\n'
                     '{"alive": false, "reason": "health unreachable"}\n',
                     encoding="utf-8")
        latest = bsp.latest_row(p)
        self.assertFalse(latest["alive"])

    def test_latest_row_missing_file(self):
        d = make_dir(self, "bs-seat-")
        self.assertIsNone(bsp.latest_row(d / "absent.jsonl"))


class TestMain(unittest.TestCase):
    def setUp(self):
        self.ledger = make_dir(self, "bs-seat-") / "probe.jsonl"
        self._orig = bsp.PROBE_LEDGER
        bsp.PROBE_LEDGER = self.ledger
        self.addCleanup(setattr, bsp, "PROBE_LEDGER", self._orig)

    def test_down_exits_2_and_writes_row(self):
        rc, out = run_main([], alive=False, case=self)
        self.assertEqual(rc, 2)
        self.assertIn("DOWN", out)
        rows = [json.loads(x) for x in
                self.ledger.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(rows), 1)
        self.assertFalse(rows[0]["alive"])

    def test_up_exits_0(self):
        rc, out = run_main([], alive=True, case=self)
        self.assertEqual(rc, 0)
        self.assertIn("UP", out)

    def test_json_face_is_parseable(self):
        rc, out = run_main(["--json"], alive=True, case=self)
        self.assertEqual(rc, 0)
        self.assertTrue(json.loads(out.strip())["alive"])

    def test_no_write(self):
        rc, _ = run_main(["--no-write"], alive=False, case=self)
        self.assertEqual(rc, 2)
        self.assertFalse(self.ledger.exists())


class TestReadinessFace(unittest.TestCase):
    def test_missing_ledger_is_silent(self):
        d = make_dir(self, "bs-seat-")
        self.assertIsNone(readiness.parse_seat_probe(d / "absent.jsonl"))

    def test_alive_row_reports_nothing(self):
        d = make_dir(self, "bs-seat-")
        p = d / "probe.jsonl"
        p.write_text('{"alive": true, "reason": "alive", "ts": "t"}\n',
                     encoding="utf-8")
        self.assertIsNone(readiness.parse_seat_probe(p))

    def test_down_row_names_reason_and_ts(self):
        d = make_dir(self, "bs-seat-")
        p = d / "probe.jsonl"
        p.write_text('{"alive": false, "reason": "provisioning inputs '
                     'missing: model, exe", "ts": "2026-10-24 05:40:00"}\n',
                     encoding="utf-8")
        reason, ts = readiness.parse_seat_probe(p)
        self.assertIn("exe", reason)
        self.assertEqual(ts, "2026-10-24 05:40:00")

    def test_blocker_carries_seat_when_review_never_ran(self):
        gates = {"a.md": "PENDING"}
        blockers = readiness.build_blockers(
            [], [], gates, [], {"a.md": {}},
            ("provisioning inputs missing: model", "2026-10-24 05:40:00"))
        self.assertIn("seat: provisioning inputs missing: model",
                      blockers[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)