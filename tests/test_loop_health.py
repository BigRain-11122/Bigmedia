"""Unit tests for the OS-loop health probe (src/os/loop_health.py).

Runtime-made trees are pure ASCII per the encoding rule; the real repo
sources (logs/probe-heartbeat.txt, src/os/state.json, src/os/backlog.md)
are only read by one read-only smoke case. Fixture beat timestamps are
computed from the real clock (minutes-ago) so staleness logic is tested
against genuine now() without clock injection.

Run:
    python tests/test_loop_health.py
"""
import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "os"))

import loop_health  # noqa: E402


def fail_codes(findings):
    return {code for sev, code, _ in findings if sev == "FAIL"}


def warn_codes(findings):
    return {code for sev, code, _ in findings if sev == "WARN"}


def make_dir(case, prefix):
    d = Path(tempfile.mkdtemp(prefix=prefix))
    case.addCleanup(shutil.rmtree, d, ignore_errors=True)
    return d


def beat_lines(spec):
    """spec = [(minutes_ago, message)] -> heartbeat log text."""
    now = datetime.now()
    lines = []
    for ago, msg in sorted(spec, key=lambda t: -t[0]):
        ts = (now - timedelta(minutes=ago)).strftime("%Y-%m-%d %H:%M:%S")
        lines.append("%s osloop: %s" % (ts, msg))
    return "\n".join(lines) + "\n"


def make_state(tick=2, production="paused", log=None, ts=None, task="R-test ok"):
    state = {"company": "BigStream", "loop": "BigStream-OSLoop",
             "mode": "o-test", "production": production,
             "installed": "2026-09-23", "tick": tick, "mandate": "x",
             "protocol": "y", "backlog": "z",
             "log": log if log is not None else
             ["2026-09-23 15:00 r1 ok", "2026-09-23 15:10 r2 ok"]}
    if ts is None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state["ts"] = ts
    state["task"] = task
    return state


def make_repo(case, spec, state=None, board=None):
    """Assemble a fake repo tree -> root Path."""
    root = make_dir(case, "bs-health-root-")
    (root / "logs").mkdir()
    (root / "src" / "os").mkdir(parents=True)
    (root / "logs" / "probe-heartbeat.txt").write_text(beat_lines(spec), encoding="utf-8")
    if state is not None:
        (root / "src" / "os" / "state.json").write_text(
            json.dumps(state, ensure_ascii=True), encoding="utf-8")
    if board is not None:
        (root / "src" / "os" / "backlog.md").write_text(board, encoding="utf-8")
    return root


BOARD = "0. [done 2026-09-23] settled item\n1. open work item\n"


class BeatParseTests(unittest.TestCase):
    def test_missing_heartbeat_fails(self):
        _, findings = loop_health.parse_beats(Path("no-such-heart.txt"))
        self.assertEqual(fail_codes(findings), {"heartbeat-file"})

    def test_unparseable_line_fails(self):
        d = make_dir(self, "bs-health-beat-")
        p = d / "heart.txt"
        p.write_text("garbage line without beat shape\n", encoding="utf-8")
        _, findings = loop_health.parse_beats(p)
        # the bad line is flagged AND the file yields no usable beats
        self.assertEqual(fail_codes(findings), {"heartbeat-line", "heartbeat-file"})

    def test_backwards_beats_fail_order(self):
        d = make_dir(self, "bs-health-beat-")
        p = d / "heart.txt"
        p.write_text("2026-09-23 10:05:00 osloop: round done exit=0\n"
                     "2026-09-23 10:01:00 osloop: round done exit=0\n", encoding="utf-8")
        beats, findings = loop_health.parse_beats(p)
        self.assertEqual(len(beats), 2)
        self.assertEqual(fail_codes(findings), {"heartbeat-order"})

    def test_clean_beats_pass(self):
        d = make_dir(self, "bs-health-beat-")
        p = d / "heart.txt"
        p.write_text(beat_lines([(30, "round done exit=0"), (5, "round done exit=0")]),
                     encoding="utf-8")
        beats, findings = loop_health.parse_beats(p)
        self.assertEqual(findings, [])
        self.assertEqual(len(beats), 2)

    def test_bom_heartbeat_still_parses(self):
        """Regression lock: PowerShell 5.1 Add-Content writes a UTF-8 BOM
        (the real heartbeat carries one); first line must still parse."""
        d = make_dir(self, "bs-health-beat-")
        p = d / "heart.txt"
        p.write_bytes(b"\xef\xbb\xbf" + beat_lines([(5, "round done exit=0")])
                      .encode("utf-8"))
        beats, findings = loop_health.parse_beats(p)
        self.assertEqual(findings, [])
        self.assertEqual(len(beats), 1)


class StateParseTests(unittest.TestCase):
    def setUp(self):
        self.d = make_dir(self, "bs-health-state-")
        self.p = self.d / "state.json"

    def test_missing_state_fails(self):
        _, _, findings = loop_health.parse_state(Path("no-such-state.json"))
        self.assertEqual(fail_codes(findings), {"state-file"})

    def test_invalid_json_fails(self):
        self.p.write_text("{not json", encoding="utf-8")
        _, _, findings = loop_health.parse_state(self.p)
        self.assertEqual(fail_codes(findings), {"state-file"})

    def test_missing_keys_fail_schema(self):
        self.p.write_text('{"tick": 1}', encoding="utf-8")
        state, _, findings = loop_health.parse_state(self.p)
        self.assertEqual(fail_codes(findings), {"state-schema"})
        self.assertEqual(state, {"tick": 1})

    def test_unknown_regime_fails(self):
        self.p.write_text(json.dumps(make_state(production="turbo")), encoding="utf-8")
        _, _, findings = loop_health.parse_state(self.p)
        self.assertEqual(fail_codes(findings), {"state-production"})

    def test_bad_tick_fails(self):
        self.p.write_text(json.dumps(make_state(tick="six")), encoding="utf-8")
        _, _, findings = loop_health.parse_state(self.p)
        self.assertEqual(fail_codes(findings), {"state-tick"})

    def test_entry_without_timestamp_fails(self):
        self.p.write_text(json.dumps(make_state(log=["no ts prefix"])), encoding="utf-8")
        _, _, findings = loop_health.parse_state(self.p)
        self.assertEqual(fail_codes(findings), {"log-ts"})

    def test_approximate_minute_x_tolerated(self):
        log = ["2026-09-23 17:2x R7 work", "2026-09-23 17:45 R8 work"]
        self.p.write_text(json.dumps(make_state(tick=2, log=log)), encoding="utf-8")
        _, stamps, findings = loop_health.parse_state(self.p)
        self.assertEqual(fail_codes(findings), set())
        self.assertEqual(warn_codes(findings), set())
        self.assertEqual(len(stamps), 2)

    def test_backwards_narrative_warns(self):
        log = ["2026-09-23 17:45 R8 work", "2026-09-23 17:25 R9 work"]
        self.p.write_text(json.dumps(make_state(tick=2, log=log)), encoding="utf-8")
        _, _, findings = loop_health.parse_state(self.p)
        self.assertEqual(warn_codes(findings), {"log-order"})
        self.assertEqual(fail_codes(findings), set())

    def test_fewer_entries_than_ticks_warns(self):
        self.p.write_text(json.dumps(make_state(tick=5)), encoding="utf-8")
        _, _, findings = loop_health.parse_state(self.p)
        self.assertEqual(warn_codes(findings), {"log-gap"})

    def test_clean_state_passes(self):
        self.p.write_text(json.dumps(make_state(tick=2)), encoding="utf-8")
        _, _, findings = loop_health.parse_state(self.p)
        self.assertEqual(findings, [])


class BacklogTests(unittest.TestCase):
    def test_missing_board_warns(self):
        (counts, findings) = loop_health.parse_backlog(Path("no-such-board.md"))
        self.assertEqual(counts, (0, 0))
        self.assertEqual(warn_codes(findings), {"backlog-file"})

    def test_burn_rate_counted(self):
        d = make_dir(self, "bs-health-board-")
        p = d / "backlog.md"
        p.write_text(BOARD, encoding="utf-8")
        (total, done), findings = loop_health.parse_backlog(p)
        self.assertEqual((total, done), (2, 1))
        self.assertEqual(findings, [])


class ClassifyTests(unittest.TestCase):
    def test_beat_classes_counted(self):
        spec = [(40, "round done exit=0"), (30, "round done exit=1"),
                (20, "skip (round in flight)"), (10, "round timeout killed (over 25min)")]
        beats, _ = loop_health.parse_beats(
            make_repo(self, spec, state=None) / "logs" / "probe-heartbeat.txt")
        done, skip_n, timeout_n, error_n = loop_health.classify(beats)
        self.assertEqual(len(done), 2)
        self.assertEqual(skip_n, 1)
        self.assertEqual(timeout_n, 1)
        self.assertEqual(error_n, 0)


class CrossCheckTests(unittest.TestCase):
    def check(self, spec, state, max_age=40, max_gap=20):
        root = make_repo(self, spec, state, BOARD)
        beats, _ = loop_health.parse_beats(root / "logs" / "probe-heartbeat.txt")
        done, _, _, _ = loop_health.classify(beats)
        findings = []
        loop_health.cross_check(beats, state, done, datetime.now(), max_age, max_gap, findings)
        return beats, findings

    def test_stale_heartbeat_fails(self):
        _, findings = self.check([(60, "round done exit=0")], make_state(tick=1))
        self.assertEqual(fail_codes(findings), {"heartbeat-stale"})

    def test_fresh_heartbeat_passes(self):
        _, findings = self.check([(5, "round done exit=0")], make_state(tick=1))
        self.assertEqual(findings, [])

    def test_gap_over_sla_warns(self):
        _, findings = self.check([(30, "round done exit=0"), (5, "round done exit=0")],
                                 make_state(tick=2))
        self.assertEqual(warn_codes(findings), {"heartbeat-gap"})
        self.assertEqual(fail_codes(findings), set())

    def test_gap_beyond_lock_age_fails_outage(self):
        _, findings = self.check([(50, "round done exit=0"), (5, "round done exit=0")],
                                 make_state(tick=2))
        self.assertEqual(fail_codes(findings), {"heartbeat-outage"})

    def test_done_beats_over_tick_fail_lag(self):
        spec = [(30, "round done exit=0"), (5, "round done exit=0")]
        _, findings = self.check(spec, make_state(tick=1))
        self.assertEqual(fail_codes(findings), {"account-lag"})

    def test_tick_over_done_beats_warns_ahead(self):
        spec = [(30, "round done exit=0")]
        _, findings = self.check(spec, make_state(tick=2))
        self.assertEqual(warn_codes(findings), {"account-ahead"})
        self.assertEqual(fail_codes(findings), set())

    # ---- PT-20260925-02 writer-face locks: state.ts is the machine-readable
    # heartbeat stamp (beats file is gitignored; state.json is the only
    # aliveness face a remote clone can verify). Missing/malformed = FAIL,
    # stale over lock age / future-stamped = WARN. ----

    def test_state_ts_missing_fails(self):
        state = make_state(tick=1)
        del state["ts"]
        _, findings = self.check([(5, "round done exit=0")], state)
        self.assertEqual(fail_codes(findings), {"state-ts"})

    def test_state_ts_malformed_fails(self):
        _, findings = self.check([(5, "round done exit=0")],
                                 make_state(tick=1, ts="2026-09-25 noon"))
        self.assertEqual(fail_codes(findings), {"state-ts"})

    def test_state_ts_stale_warns(self):
        stale = (datetime.now() - timedelta(minutes=50)).strftime("%Y-%m-%d %H:%M:%S")
        _, findings = self.check([(5, "round done exit=0")], make_state(tick=1, ts=stale))
        self.assertEqual(warn_codes(findings), {"state-ts-stale"})
        self.assertEqual(fail_codes(findings), set())

    def test_state_ts_future_warns(self):
        ahead = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        _, findings = self.check([(5, "round done exit=0")], make_state(tick=1, ts=ahead))
        self.assertEqual(warn_codes(findings), {"state-ts-future"})
        self.assertEqual(fail_codes(findings), set())

    def test_state_ts_fresh_passes(self):
        _, findings = self.check([(5, "round done exit=0")], make_state(tick=1))
        self.assertEqual(findings, [])


class CliTests(unittest.TestCase):
    def run_cli(self, root):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(["loop_health.py", "--root", str(root)])
        return rc, buf.getvalue()

    def test_healthy_tree_exits_zero(self):
        spec = [(30, "round done exit=0"), (10, "round done exit=0")]
        root = make_repo(self, spec, make_state(tick=2), BOARD)
        rc, out = self.run_cli(root)
        self.assertEqual(rc, 0)
        self.assertIn("loop health: PASS (0 fail, 0 warn)", out)
        self.assertIn("backlog=2 items 1 done (50% burn)", out)

    def test_account_lag_tree_exits_one(self):
        spec = [(30, "round done exit=0"), (10, "round done exit=0")]
        root = make_repo(self, spec, make_state(tick=1), BOARD)
        rc, out = self.run_cli(root)
        self.assertEqual(rc, 1)
        self.assertIn("FAIL", out)
        self.assertIn("account-lag", out)

    def test_bad_flag_exits_two(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(["loop_health.py", "--bogus"])
        self.assertEqual(rc, 2)

    def test_real_repo_smoke(self):
        """Read-only smoke on the real repo: any verdict is honest, but
        the probe must run end-to-end and produce a summary line."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(["loop_health.py"])
        self.assertIn(rc, (0, 1))
        out = buf.getvalue()
        self.assertIn("summary: tick=", out)
        self.assertIn("loop health:", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
