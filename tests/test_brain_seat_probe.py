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


def run_main(argv, alive, case, task_result=None):
    """Call bsp.main with stubbed wire and supervisor; (rc, stdout)."""
    original = bsp.health_ok
    bsp.health_ok = lambda *a, **k: alive
    case.addCleanup(setattr, bsp, "health_ok", original)
    original_task = bsp.supervisor_last_result
    bsp.supervisor_last_result = lambda *a, **k: task_result
    case.addCleanup(setattr, bsp, "supervisor_last_result", original_task)
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


class TestTaskResult(unittest.TestCase):
    """D-20261024-01: a success-looking task over an empty disk is a
    FAKE-GREEN, so the probe must read the scheduler's last result."""

    def test_english_header_zero(self):
        csv_text = ('"TaskName","Status","Last Result"\n'
                    '"bm-a-CoderServe","Ready","0"\n')
        self.assertEqual(bsp.parse_task_result(csv_text), 0)

    def test_localized_header_hex_zero(self):
        csv_text = ('"任务名","下次运行时间","上次结果"\n'
                    '"bm-a-CoderServe","N/A","0x0"\n')
        self.assertEqual(bsp.parse_task_result(csv_text), 0)

    def test_nonzero_result(self):
        csv_text = ('"TaskName","Last Result"\n'
                    '"bm-a-CoderServe","2"\n')
        self.assertEqual(bsp.parse_task_result(csv_text), 2)

    def test_unknown_is_none_not_alarm(self):
        self.assertIsNone(bsp.parse_task_result(""))
        self.assertIsNone(bsp.parse_task_result('"TaskName"\n"x"\n'))
        self.assertIsNone(bsp.parse_task_result(
            '"TaskName","Last Result"\n"x","N/A"\n'))

    def test_runner_is_injectable(self):
        task_result = bsp.supervisor_last_result(
            task="bm-a-CoderServe",
            runner=lambda cmd: b'"TaskName","Last Result"\n"x","0"\n')
        self.assertEqual(task_result, 0)


class TestResolveModel(unittest.TestCase):
    def test_official_quant_found(self):
        d = make_dir(self, "bs-seat-model-")
        p = d / "Qwen3.5-35B-A3B-Q4_K_M.gguf"
        p.write_text("x", encoding="utf-8")
        self.assertEqual(bsp.resolve_model([d]), p)

    def test_community_variant_ignored(self):
        d = make_dir(self, "bs-seat-model-")
        (d / "Qwen3.6-35B-A3B-UD-IQ4_XS.gguf").write_text("x", encoding="utf-8")
        got = bsp.resolve_model([d])
        self.assertFalse(got.exists())

    def test_env_override_wins(self):
        d = make_dir(self, "bs-seat-model-")
        p = d / "explicit.gguf"
        self.assertEqual(bsp.resolve_model([d], override=str(p)), p)


class TestFakeGreen(unittest.TestCase):
    def test_success_plus_missing_is_fake_green(self):
        reason = bsp.classify(False, ["model"], False, True)
        self.assertIn("FAKE-GREEN", reason)
        self.assertIn("model", reason)

    def test_fake_green_needs_missing_inputs(self):
        # a seat that reports success with all inputs present is just down
        self.assertEqual(bsp.classify(False, [], False, True),
                         bsp.REASON_HEALTH)

    def test_row_carries_fake_green(self):
        row = json.loads(bsp.probe_row(
            False, "x", missing=["model"], fake_green=True, task_result=0))
        self.assertTrue(row["fake_green"])
        self.assertEqual(row["task_result"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)