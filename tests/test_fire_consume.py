"""Tests for src/os/fire_consume.py (tech#112; R1999 delivery).

All hermetic: the card runner and the launcher are injected seams. No
real card cycle, no real subprocess dispatch, no GPU. CLI tests patch
real_run_card/real_launch/append_ledger_row at module level (main()
resolves them as module globals).
"""

import datetime
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


# Fixed wall-clock for CLI hermeticity: Sunday 2026-10-11 noon -- the
# workday block is inactive on weekends, so card-flow tests exercise
# their intended paths regardless of when the suite runs (the block
# check would otherwise swallow every CLI test on a weekday).
SUNDAY_NOON = datetime.datetime(2026, 10, 11, 12, 0, 0)
MONDAY_NOON = datetime.datetime(2026, 10, 12, 12, 0, 0)


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


class WorkdayBlockTests(unittest.TestCase):
    """tech#137: bm-a workday-hours zero-dispatch + CEO-off-work flag
    reconciliation (O-20261012-2025 early-open family)."""

    def test_weekends_always_eligible(self):
        saturday = datetime.datetime(2026, 10, 10, 14, 0, 0)
        sunday = datetime.datetime(2026, 10, 11, 23, 59, 0)
        self.assertFalse(consumer.workday_dispatch_blocked(saturday))
        self.assertFalse(consumer.workday_dispatch_blocked(sunday))

    def test_night_window_boundary_strict(self):
        before = datetime.datetime(2026, 10, 12, 7, 59, 59)
        at = datetime.datetime(2026, 10, 12, 8, 0, 0)
        self.assertFalse(consumer.workday_dispatch_blocked(before))
        self.assertTrue(consumer.workday_dispatch_blocked(at))

    def test_weekday_evening_blocked_without_flag(self):
        self.assertTrue(consumer.workday_dispatch_blocked(MONDAY_NOON))
        self.assertTrue(consumer.workday_dispatch_blocked(
            datetime.datetime(2026, 10, 12, 23, 59, 0)))

    def test_same_date_flag_lifts_block(self):
        declared = datetime.datetime(2026, 10, 12, 20, 50, 0)
        self.assertFalse(consumer.workday_dispatch_blocked(
            MONDAY_NOON, declared))

    def test_yesterday_flag_does_not_lift(self):
        declared = datetime.datetime(2026, 10, 11, 20, 50, 0)
        self.assertTrue(consumer.workday_dispatch_blocked(
            MONDAY_NOON, declared))

    def test_flag_parse_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "flag.json"
            path.write_text(json.dumps(
                {"declared_ts": "2026-10-12 20:50:00"}),
                encoding="utf-8")
            self.assertEqual(consumer.read_ceo_off_work_flag(path),
                             datetime.datetime(2026, 10, 12, 20, 50, 0))

    def test_flag_missing_corrupt_malformed_all_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "absent.json"
            self.assertIsNone(consumer.read_ceo_off_work_flag(missing))
            corrupt = Path(tmp) / "corrupt.json"
            corrupt.write_text("{not json", encoding="utf-8")
            self.assertIsNone(consumer.read_ceo_off_work_flag(corrupt))
            malformed = Path(tmp) / "malformed.json"
            malformed.write_text(
                json.dumps({"declared_ts": "2026/10/12 20:50"}),
                encoding="utf-8")
            self.assertIsNone(consumer.read_ceo_off_work_flag(malformed))
            empty = Path(tmp) / "empty.json"
            empty.write_text("{}", encoding="utf-8")
            self.assertIsNone(consumer.read_ceo_off_work_flag(empty))


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
        self._real_now_fn = consumer.NOW_FN
        self._real_flag_reader = consumer.read_ceo_off_work_flag
        self._real_probe = consumer.real_throughput_probe
        consumer.NOW_FN = lambda: SUNDAY_NOON
        consumer.read_ceo_off_work_flag = lambda path=None: None
        # tech#135: every CLI test gets a HEALTHY probe by default so
        # no test ever touches the real ollama (a real probe would
        # load 14b onto the GPU mid-window); probe-specific tests
        # override this seam per-case.
        consumer.real_throughput_probe = (
            lambda model=None, cap_s=None: self._probe_ok())
        self.tmp = tempfile.TemporaryDirectory()
        self.launch = Path(self.tmp.name) / "staged.py"
        self.launch.write_text("print('x')\n", encoding="utf-8")
        self.ledger = Path(self.tmp.name) / "ledger.jsonl"
        self.rows = []
        consumer.append_ledger_row = \
            lambda path, row: self.rows.append(row)

    @staticmethod
    def _probe_ok():
        return {"verdict": "ok", "model": "qwen2.5:14b",
                "rate_tps": 30.0, "eta_s": 230, "cap_s": 90}

    def tearDown(self):
        consumer.real_run_card = self._real_card
        consumer.real_launch = self._real_launch
        consumer.append_ledger_row = self._real_append
        consumer.NOW_FN = self._real_now_fn
        consumer.read_ceo_off_work_flag = self._real_flag_reader
        consumer.real_throughput_probe = self._real_probe
        self.tmp.cleanup()

    def _run(self, extra=None):
        argv = ["--launch", str(self.launch),
                "--ledger", str(self.ledger)] + (extra or [])
        return consumer.main(argv)

    def test_workday_block_refuses_before_card_run(self):
        consumer.NOW_FN = lambda: MONDAY_NOON
        consumer.read_ceo_off_work_flag = lambda path=None: None

        def must_not_run():
            raise AssertionError("card must not run while blocked")
        consumer.real_run_card = must_not_run
        rc = self._run()
        self.assertEqual(rc, 1)
        self.assertEqual(self.rows[0]["reason"],
                         "bm-a-workday-hours-zero-dispatch")
        self.assertFalse(self.rows[0]["launched"])

    def test_ceo_off_work_flag_lifts_block_card_flow_reached(self):
        consumer.NOW_FN = lambda: MONDAY_NOON
        consumer.read_ceo_off_work_flag = lambda path=None: \
            datetime.datetime(2026, 10, 12, 20, 50, 0)
        consumer.real_run_card = lambda: {
            "verdict": "no-fire", "reasons": ["gate-static-no-go"],
            "ts": "t"}
        rc = self._run()
        self.assertEqual(rc, 1)
        # the card actually ran -> the block was lifted, no-fire came
        # from the card itself, not from the dispatch block
        self.assertIn("card-no-fire", self.rows[0]["reason"])

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

    # -- tech#135 (P-7 pilot): throughput pre-probe wiring ---------

    def test_starved_probe_demotes_to_no_fire_rc1(self):
        consumer.real_run_card = lambda: _fire_card(expires_at=10 ** 12)
        consumer.real_throughput_probe = (
            lambda model=None, cap_s=None:
            {"verdict": "ok", "model": model, "rate_tps": 1.2,
             "eta_s": 5750, "cap_s": 90})

        def must_not_launch(script):
            raise AssertionError("starved window must not dispatch")
        consumer.real_launch = must_not_launch
        rc = self._run()
        self.assertEqual(rc, 1)
        row = self.rows[0]
        self.assertFalse(row["launched"])
        self.assertEqual(row["action"], "no-fire")
        self.assertIn("throughput-starved", row["reason"])
        self.assertIn("5750", row["reason"])
        self.assertEqual(row["throughput_probe"]["eta_s"], 5750)
        self.assertEqual(row["card_verdict"], "fire")

    def test_probe_timeout_demotes_no_fire(self):
        consumer.real_run_card = lambda: _fire_card(expires_at=10 ** 12)
        consumer.real_throughput_probe = (
            lambda model=None, cap_s=None:
            {"verdict": "timeout", "model": model, "cap_s": 90,
             "error": "timed out"})

        def must_not_launch(script):
            raise AssertionError("timeout window must not dispatch")
        consumer.real_launch = must_not_launch
        rc = self._run()
        self.assertEqual(rc, 1)
        self.assertFalse(self.rows[0]["launched"])
        self.assertIn("throughput-starved", self.rows[0]["reason"])
        self.assertIn("timeout", self.rows[0]["reason"])

    def test_probe_error_fail_closed_defers(self):
        consumer.real_run_card = lambda: _fire_card(expires_at=10 ** 12)
        consumer.real_throughput_probe = (
            lambda model=None, cap_s=None:
            {"verdict": "error", "model": model, "cap_s": 90,
             "error": "ConnectionRefusedError: no ollama"})
        rc = self._run()
        self.assertEqual(rc, 1)
        self.assertFalse(self.rows[0]["launched"])
        self.assertIn("throughput-probe-error",
                      self.rows[0]["reason"])

    def test_probe_pass_dispatches_and_ledgers_probe_row(self):
        consumer.real_run_card = lambda: _fire_card(expires_at=10 ** 12)
        consumer.real_throughput_probe = (
            lambda model=None, cap_s=None:
            {"verdict": "ok", "model": model, "rate_tps": 30.0,
             "eta_s": 230, "cap_s": 90})
        consumer.real_launch = lambda script: 4242
        rc = self._run()
        self.assertEqual(rc, 0)
        row = self.rows[0]
        self.assertTrue(row["launched"])
        self.assertEqual(row["launch_pid"], 4242)
        self.assertEqual(row["throughput_probe"]["eta_s"], 230)

    def test_no_fire_card_never_runs_probe(self):
        # zero-cost law: no-fire rounds must never pay for a probe
        consumer.real_run_card = lambda: {
            "verdict": "no-fire", "reasons": ["gate-static-no-go"],
            "ts": "t"}

        def must_not_probe(model=None, cap_s=None):
            raise AssertionError("probe must not run on no-fire card")
        consumer.real_throughput_probe = must_not_probe
        rc = self._run()
        self.assertEqual(rc, 1)
        self.assertNotIn("throughput_probe", self.rows[0])

    def test_eta_starved_s_cli_override_lower_line_starves(self):
        consumer.real_run_card = lambda: _fire_card(expires_at=10 ** 12)
        consumer.real_launch = lambda script: 99

        def must_not_launch(script):
            raise AssertionError("lowered line must starve the GO")
        consumer.real_launch = must_not_launch
        rc = self._run(extra=["--eta-starved-s", "200"])
        self.assertEqual(rc, 1)
        self.assertIn("throughput-starved", self.rows[0]["reason"])

    def test_post_probe_staleness_recheck_demotes(self):
        # fire card expiring 4s out passes decide (margin 2s, even
        # with a full-second slip) but a probe that eats 2s pushes the
        # dispatch past expiry -- the post-probe re-check must catch
        # it (staleness law). expires_at must be an int (card
        # contract); the 4s/2s pair keeps both sides deterministic.
        import time
        now0 = int(datetime.datetime.now().timestamp())
        soon = now0 + 4

        def slow_probe(model=None, cap_s=None):
            time.sleep(2.0)
            return self._probe_ok()
        consumer.real_run_card = lambda: _fire_card(expires_at=soon)
        consumer.real_throughput_probe = slow_probe
        consumer.real_launch = lambda script: 77
        rc = self._run()
        self.assertEqual(rc, 1)
        self.assertFalse(self.rows[0]["launched"])
        self.assertIn("expired-after-probe", self.rows[0]["reason"])


class ThroughputProbeTests(unittest.TestCase):
    """tech#135 (P-7): pure cores of the card-GO throughput probe.

    The network seam (real_throughput_probe) is deliberately NOT
    exercised here -- a real probe would hit the resident brain
    server; the parse math is split into compute_rate so the whole
    probe pipeline is covered without any network (tech#186 leg-4:
    the probe flies the brain wire -- usage tokens over request
    wall-clock, the wire exposes no server-side eval counters)."""

    def test_compute_rate_from_wire_usage_and_wall_clock(self):
        # 20 prompt + 96 completion tokens over a 2.9s request
        rate, eta = consumer.compute_rate({
            "usage": {"prompt_tokens": 20, "completion_tokens": 96},
        }, 2.9)
        self.assertAlmostEqual(rate, 116 / 2.9, places=3)
        self.assertAlmostEqual(
            eta,
            (consumer.ETA_PROMPT_TOKENS
             + consumer.ETA_OUTPUT_TOKENS) * 2.9 / 116,
            places=3)

    def test_compute_rate_missing_or_zero_counters_none(self):
        self.assertIsNone(consumer.compute_rate({}, 2.9))
        self.assertIsNone(consumer.compute_rate({
            "usage": {"prompt_tokens": 0, "completion_tokens": 0}},
            2.9))
        self.assertIsNone(consumer.compute_rate({
            "usage": {"prompt_tokens": 5, "completion_tokens": 7}}, 0))
        self.assertIsNone(consumer.compute_rate(None, 2.9))

    def test_classify_ok_under_line(self):
        ok, reason = consumer.classify_throughput(
            {"verdict": "ok", "rate_tps": 30.0, "eta_s": 230})
        self.assertTrue(ok)
        self.assertIn("throughput-ok", reason)
        self.assertIn("230", reason)

    def test_classify_eta_exactly_at_line_passes(self):
        # boundary: eta == line is NOT starved (strictly greater is)
        ok, _ = consumer.classify_throughput(
            {"verdict": "ok", "rate_tps": 5.75, "eta_s": 1200})
        self.assertTrue(ok)

    def test_classify_eta_over_line_starved(self):
        ok, reason = consumer.classify_throughput(
            {"verdict": "ok", "rate_tps": 1.2, "eta_s": 5750})
        self.assertFalse(ok)
        self.assertIn("throughput-starved", reason)
        self.assertIn("5750", reason)
        self.assertIn("1.2", reason)

    def test_classify_custom_line_respected(self):
        ok, reason = consumer.classify_throughput(
            {"verdict": "ok", "rate_tps": 30.0, "eta_s": 230},
            eta_starved_s=200)
        self.assertFalse(ok)
        self.assertIn("throughput-starved", reason)

    def test_classify_timeout_is_starved_hard_case(self):
        ok, reason = consumer.classify_throughput(
            {"verdict": "timeout", "cap_s": 90})
        self.assertFalse(ok)
        self.assertIn("throughput-starved", reason)
        self.assertIn("timeout", reason)

    def test_classify_error_fail_closed(self):
        ok, reason = consumer.classify_throughput(
            {"verdict": "error", "error": "URLError: refused"})
        self.assertFalse(ok)
        self.assertIn("throughput-probe-error", reason)
        self.assertIn("URLError", reason)

    def test_classify_malformed_and_missing_eta_fail_closed(self):
        for bad in (None, {}, {"verdict": None}, {"verdict": "ok"},
                    {"verdict": "ok", "eta_s": 0},
                    {"verdict": "ok", "eta_s": "fast"}):
            ok, reason = consumer.classify_throughput(bad)
            self.assertFalse(ok, bad)
            self.assertIn("throughput-probe-error", reason)


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


class _FakeHttpResp:
    def __init__(self, body):
        self._body = body

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class CpuLaneTests(unittest.TestCase):
    """tech#169: --cpu-lane path. The workday zero-dispatch block is
    NOT applied on this lane (O-20260913-2215 explicitly repealed the
    rule's CPU portion -- CPU face 24/7, new-order-overrides tech#137),
    the GPU card never runs, the gate is one CPU-pinned throughput
    probe, and a GPU-wired launcher is refused loudly (a GPU launcher
    on the CPU lane would fly outside every gate)."""

    def setUp(self):
        self._real_card = consumer.real_run_card
        self._real_launch = consumer.real_launch
        self._real_append = consumer.append_ledger_row
        self._real_now_fn = consumer.NOW_FN
        self._real_flag_reader = consumer.read_ceo_off_work_flag
        self._real_probe = consumer.real_throughput_probe
        consumer.NOW_FN = lambda: SUNDAY_NOON
        consumer.read_ceo_off_work_flag = lambda path=None: None
        self.probe_calls = []

        def _probe(model=None, cap_s=None, cpu_lane=False):
            self.probe_calls.append(
                {"model": model, "cap_s": cap_s, "cpu_lane": cpu_lane})
            return self.probe_row()

        consumer.real_throughput_probe = _probe
        self.tmp = tempfile.TemporaryDirectory()
        self.launch_cpu = Path(self.tmp.name) / "e4_call_cpu.py"
        self.launch_cpu.write_text("print('x')\n", encoding="utf-8")
        self.launch_gpu = Path(self.tmp.name) / "staged.py"
        self.launch_gpu.write_text("print('x')\n", encoding="utf-8")
        self.ledger = Path(self.tmp.name) / "ledger.jsonl"
        self.rows = []
        consumer.append_ledger_row = \
            lambda path, row: self.rows.append(row)
        self.launched = []
        consumer.real_launch = \
            lambda p: (self.launched.append(str(p)) or 4242)

    @staticmethod
    def probe_row():
        return {"verdict": "ok", "model": "qwen2.5:14b",
                "rate_tps": 8.5, "eta_s": 812, "cap_s": 180}

    def tearDown(self):
        consumer.real_run_card = self._real_card
        consumer.real_launch = self._real_launch
        consumer.append_ledger_row = self._real_append
        consumer.NOW_FN = self._real_now_fn
        consumer.read_ceo_off_work_flag = self._real_flag_reader
        consumer.real_throughput_probe = self._real_probe
        self.tmp.cleanup()

    def _run(self, launch, extra=None):
        argv = ["--launch", str(launch), "--cpu-lane",
                "--ledger", str(self.ledger)] + (extra or [])
        return consumer.main(argv)

    def test_workday_block_bypassed_card_never_runs(self):
        # O-20260913-2215: weekday noon would hard-block the GPU path;
        # the CPU lane must proceed to the probe and dispatch.
        consumer.NOW_FN = lambda: MONDAY_NOON

        def must_not_run():
            raise AssertionError("GPU card must not run on the CPU lane")
        consumer.real_run_card = must_not_run
        rc = self._run(self.launch_cpu)
        self.assertEqual(rc, 0)
        self.assertEqual(len(self.launched), 1)
        self.assertEqual(self.rows[0]["lane"], "cpu")
        self.assertEqual(self.rows[0]["action"], "launch")
        self.assertTrue(self.rows[0]["launched"])

    def test_miswired_gpu_launcher_refused_rc2(self):
        rc = self._run(self.launch_gpu)
        self.assertEqual(rc, 2)
        self.assertEqual(self.probe_calls, [])  # refused before probing
        self.assertEqual(self.launched, [])
        self.assertEqual(self.rows, [])

    def test_starved_probe_demotes_to_no_fire_rc1(self):
        self.probe_row = staticmethod(lambda: {
            "verdict": "ok", "model": "qwen2.5:14b",
            "rate_tps": 2.0, "eta_s": 3450, "cap_s": 180})
        rc = self._run(self.launch_cpu)
        self.assertEqual(rc, 1)
        self.assertEqual(self.launched, [])
        self.assertFalse(self.rows[0]["launched"])
        self.assertIn("throughput-starved", self.rows[0]["reason"])

    def test_probe_error_fail_closed_no_fire_rc1(self):
        self.probe_row = staticmethod(lambda: {
            "verdict": "error", "model": "qwen2.5:14b",
            "cap_s": 180, "error": "HTTP 404 model not found"})
        rc = self._run(self.launch_cpu)
        self.assertEqual(rc, 1)
        self.assertEqual(self.launched, [])
        self.assertIn("throughput-probe-error", self.rows[0]["reason"])

    def test_probe_is_pinned_to_cpu_lane(self):
        rc = self._run(self.launch_cpu)
        self.assertEqual(rc, 0)
        self.assertEqual(len(self.probe_calls), 1)
        self.assertTrue(self.probe_calls[0]["cpu_lane"])
        self.assertEqual(self.probe_calls[0]["cap_s"],
                         consumer.CPU_PROBE_CAP_S)

    def test_real_probe_cpu_payload_carries_wire_contract(self):
        # tech#186 leg-4: on the brain wire the CPU-lane call form
        # carries NO lane-pinning options at all -- num_gpu/
        # num_thread belong to the resident server, not the client
        # payload (moot, same doctrine as the e4 launcher templates).
        # The payload lock: OpenAI chat shape + thinking off + the
        # CPU cap override stays call-site-explicit.
        captured = {}

        def _fake_urlopen(request, timeout=None):
            captured["data"] = json.loads(
                request.data.decode("utf-8"))
            captured["timeout"] = timeout
            return _FakeHttpResp(json.dumps({
                "usage": {"prompt_tokens": 48,
                          "completion_tokens": 96},
            }).encode("utf-8"))

        orig_urlopen = consumer.urllib.request.urlopen
        consumer.urllib.request.urlopen = _fake_urlopen
        try:
            # mirror main()'s call form: the CPU cap override is
            # call-site-explicit (cap_s=CPU_PROBE_CAP_S, cpu_lane=True)
            row = self._real_probe(cap_s=consumer.CPU_PROBE_CAP_S,
                                   cpu_lane=True)
        finally:
            consumer.urllib.request.urlopen = orig_urlopen
        self.assertEqual(row["verdict"], "ok")
        self.assertNotIn("options", captured["data"])
        self.assertNotIn("num_gpu", captured["data"])
        self.assertNotIn("num_thread", captured["data"])
        self.assertNotIn("num_predict", captured["data"])
        self.assertNotIn("prompt", captured["data"])
        self.assertEqual(
            captured["data"]["chat_template_kwargs"]["enable_thinking"],
            False)
        self.assertEqual(captured["data"]["max_tokens"],
                         consumer.PROBE_TOKENS)
        self.assertEqual(captured["data"]["stream"], False)
        self.assertEqual(captured["timeout"],
                         consumer.CPU_PROBE_CAP_S)

    def test_real_probe_wire_payload_has_no_ollama_faces(self):
        # regression lock (tech#186 leg-4): the wire probe payload
        # must never regress to the retired local-ollama generate
        # face -- no options block, no ollama prompt field, and the
        # default-flight call stays on the brain wire contract.
        captured = {}

        def _fake_urlopen(request, timeout=None):
            captured["data"] = json.loads(
                request.data.decode("utf-8"))
            return _FakeHttpResp(json.dumps({
                "usage": {"prompt_tokens": 48,
                          "completion_tokens": 96},
            }).encode("utf-8"))

        orig_urlopen = consumer.urllib.request.urlopen
        consumer.urllib.request.urlopen = _fake_urlopen
        try:
            row = self._real_probe()
        finally:
            consumer.urllib.request.urlopen = orig_urlopen
        self.assertEqual(row["verdict"], "ok")
        self.assertNotIn("options", captured["data"])
        self.assertNotIn("prompt", captured["data"])
        self.assertNotIn("think", captured["data"])
        self.assertIn("messages", captured["data"])


if __name__ == "__main__":
    unittest.main()
