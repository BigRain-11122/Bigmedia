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
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "os"))

import loop_health  # noqa: E402

# tech#58: the AIHOT liveness face probes real localhost HTTP by design
# (production names a dead stack within one round). The suite must stay
# deterministic regardless of the live stack state, so tests stub the
# probe module-wide; the real probe path is covered by injected-_urlopen
# unit tests below plus every production round run.
_REAL_PROBE_HTTP_FACE = loop_health.probe_http_face
loop_health.probe_http_face = lambda url, timeout_s=4.0: (True, "{}")


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

    def test_account_drift_within_adjudicated_baseline_warns(self):
        """done beats == tick + adjudicated drift: explicit WARN, no FAIL
        (broken-round double-body history is not the R4/R5 bug)."""
        spec = [(30, "round done exit=0"), (10, "round done exit=0")]
        state = make_state(tick=1)
        state["account_drift_adjudicated"] = 1
        root = make_repo(self, spec, state, BOARD)
        rc, out = self.run_cli(root)
        self.assertEqual(rc, 0)
        self.assertIn("account-drift-adjudicated", out)
        self.assertIn("1 beat(s) within", out)
        self.assertNotIn("account-lag", out)

    def test_account_drift_beyond_adjudicated_baseline_fails(self):
        """New drift past the documented baseline still trips the gate."""
        spec = [(40, "round done exit=0"), (30, "round done exit=0"),
                (10, "round done exit=0")]
        state = make_state(tick=1)
        state["account_drift_adjudicated"] = 1
        root = make_repo(self, spec, state, BOARD)
        rc, out = self.run_cli(root)
        self.assertEqual(rc, 1)
        self.assertIn("account-lag", out)
        self.assertIn("done beats=3 > tick=1 + adjudicated=1", out)

    def test_account_drift_invalid_baseline_falls_back_strict(self):
        """Non-int/negative/bool baseline values are treated as 0 -
        malformed adjudication data must never widen the gate."""
        for bad in (-3, True, "7", None):
            spec = [(30, "round done exit=0"), (10, "round done exit=0")]
            state = make_state(tick=1)
            state["account_drift_adjudicated"] = bad
            root = make_repo(self, spec, state, BOARD)
            rc, out = self.run_cli(root)
            self.assertEqual(rc, 1, "bad baseline %r must stay strict" % (bad,))
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


class LoopModeTests(unittest.TestCase):
    """--loop routine face (tech#11/#20): same analysis, compact output -
    FAILs always print, dated WARNs older than the cutoff fold into
    one suppression count, dateless WARNs stay visible, and dense
    in-window same-code WARN groups (>= --fold-dense, default 5)
    collapse into one count line (occurrences + date span + magnitude
    band + audit-face pointer)."""

    def run_cli(self, root, extra):
        argv = ["loop_health.py", "--root", str(root)] + extra
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(argv)
        return rc, buf.getvalue()

    def test_warn_is_recent_unit(self):
        self.assertTrue(loop_health.warn_is_recent("drift baseline note", "2026-10-06"))
        self.assertFalse(loop_health.warn_is_recent(
            "backwards: 2026-09-23 17:45 -> 2026-09-23 17:25", "2026-10-06"))
        # any fresh date rescues the line (pair spans the cutoff)
        self.assertTrue(loop_health.warn_is_recent(
            "gap (2026-09-23 17:45 -> 2026-10-09 13:54)", "2026-10-06"))
        self.assertTrue(loop_health.warn_is_recent(
            "gap (2026-10-06 -> 2026-10-09 13:54)", "2026-10-06"))

    def test_loop_mode_suppresses_old_dated_warn_keeps_fail(self):
        old_log = ["2026-01-01 10:0x r1 ok", "2026-01-01 09:5x r2 ok"]
        spec = [(30, "round done exit=0"), (10, "round done exit=0")]
        root = make_repo(self, spec, make_state(tick=1, log=old_log), BOARD)
        rc, out = self.run_cli(root, ["--loop"])
        self.assertEqual(rc, 1)  # account-lag FAIL survives the compact face
        self.assertIn("account-lag", out)
        self.assertIn("suppressed: 1 historical WARN", out)
        self.assertNotIn("log-order", out)  # old dated WARN folded away
        self.assertNotIn("loop health probe:", out)  # header line dropped
        # default face unchanged: same tree, full output
        rc2, out2 = self.run_cli(root, [])
        self.assertEqual(rc2, 1)
        self.assertIn("log-order", out2)
        self.assertIn("loop health probe:", out2)
        self.assertNotIn("suppressed:", out2)

    def test_loop_mode_keeps_recent_and_dateless_warns(self):
        spec = [(35, "round done exit=0"), (10, "round done exit=0")]
        state = make_state(tick=1)
        state["account_drift_adjudicated"] = 1
        root = make_repo(self, spec, state, BOARD)
        rc, out = self.run_cli(root, ["--loop"])
        self.assertEqual(rc, 0)
        self.assertIn("heartbeat-gap", out)      # fresh dated WARN visible
        self.assertIn("account-drift-adjudicated", out)  # dateless WARN visible
        self.assertNotIn("suppressed:", out)

    def test_dense_fold_unit(self):
        gap = ("beat gap 21 min (2026-10-09 01:00 -> 2026-10-09 01:21) "
               "over 20 min comm SLA - long rounds may breach legitimately")
        shown = [("WARN", "heartbeat-gap", gap)] * 6
        folded = loop_health.dense_fold(shown, 5)
        self.assertEqual(len(folded), 1)
        self.assertIn("6 occurrence(s)", folded[0][2])
        self.assertIn("2026-10-09", folded[0][2])
        self.assertIn("gaps 21-21 min", folded[0][2])
        self.assertIn("dense-window fold", folded[0][2])
        # FAILs interleave untouched and never fold
        shown2 = shown[:5] + [("FAIL", "account-lag", "boom")] + shown[5:]
        folded2 = loop_health.dense_fold(shown2, 5)
        self.assertEqual(len(folded2), 2)
        self.assertEqual({c for _, c, _ in folded2},
                         {"heartbeat-gap", "account-lag"})
        # below threshold and 0-disable stay verbatim
        sparse = shown[:3]
        self.assertIs(loop_health.dense_fold(sparse, 5), sparse)
        self.assertIs(loop_health.dense_fold(shown, 0), shown)

    def test_dense_same_code_warns_fold_to_one_count_line(self):
        spec = [(21 * i, "round done exit=0") for i in range(7)]  # 6 x 21-min gaps
        log = ["2026-09-23 15:%02d r%d ok" % (i, i) for i in range(7)]
        root = make_repo(self, spec, make_state(tick=7, log=log), BOARD)
        rc, out = self.run_cli(root, ["--loop"])
        self.assertEqual(rc, 0)
        self.assertEqual(out.count("over 20 min comm SLA"), 0)  # verbatim lines gone
        self.assertIn("6 occurrence(s)", out)      # count preserved
        self.assertIn("gaps 21-21 min", out)        # magnitude band preserved
        self.assertIn("dense-window fold", out)     # audit-face pointer preserved
        self.assertIn("(0 fail, 6 warn)", out)       # verdict counts full findings
        rc2, out2 = self.run_cli(root, [])           # audit face keeps all lines
        self.assertEqual(out2.count("over 20 min comm SLA"), 6)

    def test_dense_fold_disabled_by_flag(self):
        spec = [(21 * i, "round done exit=0") for i in range(7)]
        root = make_repo(self, spec, make_state(tick=7), BOARD)
        rc, out = self.run_cli(root, ["--loop", "--fold-dense", "0"])
        self.assertEqual(rc, 0)
        self.assertEqual(out.count("over 20 min comm SLA"), 6)
        self.assertNotIn("dense-window fold", out)

    def test_sparse_warns_stay_verbatim_under_threshold(self):
        spec = [(21 * i, "round done exit=0") for i in range(4)]  # 3 gaps < 5
        root = make_repo(self, spec, make_state(tick=4), BOARD)
        rc, out = self.run_cli(root, ["--loop"])
        self.assertEqual(rc, 0)
        self.assertEqual(out.count("over 20 min comm SLA"), 3)
        self.assertNotIn("dense-window fold", out)

    def test_dense_fail_group_never_folds(self):
        spec = [(45 * i, "round done exit=0") for i in range(6)]  # 5 x 45-min outages
        root = make_repo(self, spec, make_state(tick=6), BOARD)
        rc, out = self.run_cli(root, ["--loop"])
        self.assertEqual(rc, 1)
        self.assertEqual(out.count("exceeds lock age"), 5)  # FAILs print in full

    def test_bad_fold_dense_flag_exits_two(self):
        for bad in (["--fold-dense", "-1"], ["--fold-dense", "x"]):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = loop_health.main(
                    ["loop_health.py", "--loop"] + bad)
            self.assertEqual(rc, 2)

    def test_loop_mode_real_repo_smoke(self):
        """Read-only smoke: compact face runs end-to-end on the real
        repo and keeps the verdict line shape."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(["loop_health.py", "--loop"])
        self.assertIn(rc, (0, 1))
        out = buf.getvalue()
        self.assertIn("summary: tick=", out)
        self.assertIn("loop health:", out)
        self.assertNotIn("loop health probe:", out)

    def test_bad_loop_flag_exits_two(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(["loop_health.py", "--recent-days", "0", "--loop"])
        self.assertEqual(rc, 2)


class RootLitterTests(unittest.TestCase):
    """tech#22: root-level r<digits>* probe/temp leftover guard."""

    BEAT_SPEC = [(0, "round done exit=0"), (5, "round done exit=0")]

    def _repo(self):
        return make_repo(self, self.BEAT_SPEC, make_state(tick=2), BOARD)

    def test_clean_root_passes(self):
        root = self._repo()
        findings = []
        loop_health.check_root_litter(root, findings)
        self.assertEqual(findings, [])

    def test_one_or_two_leftovers_warn(self):
        for n in (1, 2):
            root = self._repo()
            for i in range(n):
                (root / ("r18xx_probe%d.py" % i)).write_text("x", encoding="utf-8")
            findings = []
            loop_health.check_root_litter(root, findings)
            self.assertEqual(warn_codes(findings), {"root-probe-litter"})
            self.assertNotIn("root-probe-litter", fail_codes(findings))
            self.assertIn("%d root-level" % n, findings[0][2])

    def test_three_leftovers_fail(self):
        root = self._repo()
        for name in ("r_cur_check.py", "r_cur_probe1.py", "r1776_close.py"):
            (root / name).write_text("x", encoding="utf-8")
        findings = []
        loop_health.check_root_litter(root, findings)
        self.assertIn("root-probe-litter", fail_codes(findings))

    def test_repo_files_never_match(self):
        root = self._repo()
        for name in ("README.md", "readme.md", "release", "requirements.txt"):
            (root / name).write_text("x", encoding="utf-8")
        findings = []
        loop_health.check_root_litter(root, findings)
        self.assertEqual(findings, [])

    def test_subdirectory_files_not_scanned(self):
        root = self._repo()
        sub = root / "tools"
        sub.mkdir()
        for i in range(5):
            (sub / ("r19xx_probe%d.py" % i)).write_text("x", encoding="utf-8")
        findings = []
        loop_health.check_root_litter(root, findings)
        self.assertEqual(findings, [])

    def test_cli_wired_into_verdict(self):
        root = self._repo()
        for i in range(3):
            (root / ("r%d_probe.py" % i)).write_text("x", encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(["loop_health.py", "--root", str(root)])
        self.assertEqual(rc, 1)
        self.assertIn("root-probe-litter", buf.getvalue())


class StaleDirtyTests(unittest.TestCase):
    """tech#31: sediment-dirty naming guard (C-20261009-03 dirty-face
    split law - in-flight files are naturally fresh, sediment >7d named)."""

    BEAT_SPEC = [(0, "round done exit=0"), (5, "round done exit=0")]

    def _repo(self):
        return make_repo(self, self.BEAT_SPEC, make_state(tick=2), BOARD)

    def test_fresh_files_never_flag(self):
        now = datetime.now()
        entries = [("src/a.py", now - timedelta(days=1)),
                   ("data/b.txt", now),
                   ("src/c.py", now - timedelta(days=6, hours=23))]
        self.assertEqual(loop_health.classify_stale_dirty(entries, now), [])

    def test_stale_flagged_and_sorted(self):
        now = datetime.now()
        entries = [("zz/old.txt", now - timedelta(days=9)),
                   ("aa/older.txt", now - timedelta(days=30))]
        self.assertEqual(loop_health.classify_stale_dirty(entries, now),
                         ["aa/older.txt", "zz/old.txt"])

    def test_seven_day_boundary(self):
        now = datetime.now()
        self.assertEqual(loop_health.classify_stale_dirty(
            [("x/exactly7.txt", now - timedelta(days=7))], now), [])
        self.assertEqual(loop_health.classify_stale_dirty(
            [("x/just_over.txt", now - timedelta(days=7, hours=2))], now),
            ["x/just_over.txt"])

    def test_whitelist_and_deleted_skip(self):
        now = datetime.now()
        entries = [("data/storylines/drama/mv0001/PRODUCTION.md",
                    now - timedelta(days=30)),
                   ("data/sources/mv001/song.ape", now - timedelta(days=30)),
                   ("src/deleted.py", None),
                   ("src/gone.txt", now - timedelta(days=30))]
        self.assertEqual(loop_health.classify_stale_dirty(entries, now),
                         ["src/gone.txt"])

    def test_parse_porcelain_z(self):
        data = (b" M src/render/a.py\x00"
                b"?? .c3-tmp/r19_probe.py\x00"
                b"R  docs/new.txt\x00docs/old.txt\x00"
                b" D src/gone.py\x00"
                b"?? data/pic/\xe5\x91\xa8.txt\x00")
        self.assertEqual(
            loop_health._parse_porcelain_z(data),
            ["src/render/a.py", ".c3-tmp/r19_probe.py",
             "docs/new.txt", "src/gone.py", "data/pic/周.txt"])

    def test_check_skips_non_git_tree(self):
        root = self._repo()
        (root / "src" / "old.py").write_text("x", encoding="utf-8")
        findings = []
        loop_health.check_stale_dirty(root, datetime.now(), findings)
        self.assertEqual(findings, [])

    def test_cli_wired_no_crash_on_fake_repo(self):
        root = self._repo()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(["loop_health.py", "--root", str(root)])
        self.assertIn("loop health:", buf.getvalue())
        self.assertNotIn("stale-dirty", buf.getvalue())
        self.assertEqual(rc, 0)


class CodexFreshnessTests(unittest.TestCase):
    """tech#37: codex supply-freshness naming guard (R1844 arrears anchor -
    the "refresh every batch" discipline gets machine teeth)."""

    BEAT_SPEC = [(0, "round done exit=0"), (5, "round done exit=0")]

    def _repo(self):
        return make_repo(self, self.BEAT_SPEC, make_state(tick=2), BOARD)

    def _codex(self, root):
        d = root / "data" / "storylines" / "codex"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _touch_stale(self, d, name, days):
        p = d / name
        p.write_text("x", encoding="utf-8")
        old = time.time() - days * 86400
        os.utime(p, (old, old))

    def test_fresh_batch_never_flags(self):
        now = datetime.now()
        entries = [(name, now - timedelta(days=i)) for i, name in
                   enumerate(loop_health.CODEX_DIMENSIONS)]
        self.assertEqual(loop_health.classify_codex_freshness(entries, now),
                         [])

    def test_stale_named_and_sorted(self):
        now = datetime.now()
        entries = [("city-culture.md", now - timedelta(days=12)),
                   ("city-chronicle.md", now - timedelta(days=1)),
                   ("city-residents.md", now - timedelta(days=11))]
        self.assertEqual(loop_health.classify_codex_freshness(entries, now),
                         ["city-culture.md", "city-residents.md"])

    def test_seven_day_boundary(self):
        now = datetime.now()
        self.assertEqual(loop_health.classify_codex_freshness(
            [("city-spirit.md", now - timedelta(days=7))], now), [])
        self.assertEqual(loop_health.classify_codex_freshness(
            [("city-spirit.md", now - timedelta(days=7, hours=2))], now),
            ["city-spirit.md"])

    def test_missing_file_never_flags(self):
        now = datetime.now()
        entries = [(name, None) for name in loop_health.CODEX_DIMENSIONS]
        self.assertEqual(loop_health.classify_codex_freshness(entries, now),
                         [])

    def test_check_silent_without_codex_dir(self):
        root = self._repo()  # no codex dir at all -> no face, no finding
        findings = []
        loop_health.check_codex_freshness(root, datetime.now(), findings)
        self.assertEqual(findings, [])

    def test_check_names_real_stale_files_only(self):
        root = self._repo()
        d = self._codex(root)
        self._touch_stale(d, "city-culture.md", 12)
        (d / "city-chronicle.md").write_text("x", encoding="utf-8")  # fresh
        findings = []
        loop_health.check_codex_freshness(root, datetime.now(), findings)
        self.assertEqual(warn_codes(findings), {"codex-stale"})
        self.assertIn("city-culture.md", findings[0][2])
        self.assertNotIn("city-chronicle.md", findings[0][2])

    def test_cli_wired_warn_not_fail(self):
        root = self._repo()
        d = self._codex(root)
        self._touch_stale(d, "city-residents.md", 11)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(["loop_health.py", "--root", str(root)])
        self.assertIn("codex-stale", buf.getvalue())
        self.assertEqual(rc, 0)  # WARN verdict, never a probe-break FAIL


class AihotStackTests(unittest.TestCase):
    """tech#58: AIHOT stack liveness guard - probe, classify and CLI
    wiring. Real HTTP never runs inside the suite (module-level stub);
    the probe core is tested through the _urlopen injection seam."""

    class _Resp:
        def __init__(self, status=200, body=b"{}"):
            self.status = status
            self._body = body

        def read(self, n=-1):
            return self._body

        def getcode(self):
            return self.status

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def _probe(self, resp_or_exc):
        if isinstance(resp_or_exc, Exception):
            def _boom(url, timeout):
                raise resp_or_exc
            return _REAL_PROBE_HTTP_FACE("http://test/", _urlopen=_boom)
        return _REAL_PROBE_HTTP_FACE("http://test/",
                                     _urlopen=lambda u, timeout: resp_or_exc)

    def test_probe_200_ok_with_body(self):
        ok, detail = self._probe(self._Resp(200, b'{"ok":true}'))
        self.assertTrue(ok)
        self.assertEqual(detail, '{"ok":true}')

    def test_probe_non_200_flags(self):
        ok, detail = self._probe(self._Resp(503, b""))
        self.assertFalse(ok)
        self.assertIn("503", detail)

    def test_probe_timeout_never_raises(self):
        ok, detail = self._probe(TimeoutError("timed out"))
        self.assertFalse(ok)
        self.assertIn("TimeoutError", detail)

    def test_probe_refused_never_raises(self):
        ok, detail = self._probe(ConnectionRefusedError("refused"))
        self.assertFalse(ok)
        self.assertIn("ConnectionRefusedError", detail)

    def test_probe_status_none_falls_back_to_getcode(self):
        class _OldResp:
            # py<3.9-style response object: no .status attribute at
            # all, status only reachable via getcode().
            def __init__(self):
                self.code = 200

            def read(self, n=-1):
                return b"{}"

            def getcode(self):
                return self.code

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False
        ok, detail = self._probe(_OldResp())
        self.assertTrue(ok)

    def test_classify_healthy_silent(self):
        findings = loop_health.classify_aihot_faces(
            (True, '{"ok":true,"db":"ok"}'), (True, "<html>200</html>"))
        self.assertEqual(findings, [])

    def test_classify_both_down_names_both_faces(self):
        findings = loop_health.classify_aihot_faces(
            (False, "ConnectionRefusedError: refused"),
            (False, "HTTP 502"))
        self.assertEqual(len(findings), 1)
        sev, code, msg = findings[0]
        self.assertEqual((sev, code), ("WARN", "aihot-stack"))
        self.assertIn("api down/unreachable", msg)
        self.assertIn("web down/unreachable", msg)
        self.assertIn("R1891", msg)  # recovery runbook pointer

    def test_classify_db_face_flagged(self):
        findings = loop_health.classify_aihot_faces(
            (True, '{"ok":true,"db":"fail"}'), (True, "<html>"))
        self.assertEqual(warn_codes(findings), {"aihot-stack"})
        self.assertIn("db face 'fail'", findings[0][2])

    def test_classify_db_missing_or_ok_never_flags(self):
        self.assertEqual(loop_health.classify_aihot_faces(
            (True, '{"ok":true}'), (True, "<html>")), [])
        self.assertEqual(loop_health.classify_aihot_faces(
            (True, '{"ok":true,"db":"ok"}'), (True, "<html>")), [])

    def test_classify_api_body_unparseable_ignored(self):
        self.assertEqual(loop_health.classify_aihot_faces(
            (True, "not json at all"), (True, "<html>")), [])

    def test_classify_web_only_down(self):
        findings = loop_health.classify_aihot_faces(
            (True, '{"ok":true,"db":"ok"}'), (False, "HTTP 502"))
        self.assertEqual(len(findings), 1)
        self.assertIn("web down/unreachable", findings[0][2])
        self.assertNotIn("api down", findings[0][2])

    def _run_cli(self, root):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(["loop_health.py", "--root", str(root)])
        return rc, buf.getvalue()

    def _healthy_repo(self):
        spec = [(30, "round done exit=0"), (10, "round done exit=0")]
        return make_repo(self, spec, make_state(tick=2), BOARD)

    def test_cli_wiring_down_stack_named(self):
        root = self._healthy_repo()
        old = loop_health.probe_http_face
        loop_health.probe_http_face = lambda url, timeout_s=4.0: (
            False, "ConnectionRefusedError: refused")
        try:
            rc, out = self._run_cli(root)
        finally:
            loop_health.probe_http_face = old
        self.assertEqual(rc, 0)  # WARN verdict, never a probe-break FAIL
        self.assertIn("aihot-stack", out)

    def test_cli_wiring_healthy_stack_silent(self):
        root = self._healthy_repo()
        rc, out = self._run_cli(root)
        self.assertEqual(rc, 0)
        self.assertNotIn("aihot-stack", out)

    def test_check_env_url_override(self):
        seen = []

        def fake_probe(url, timeout_s):
            seen.append(url)
            return (True, '{"ok":true,"db":"ok"}')

        findings = []
        old = os.environ.get("AIHOT_API_URL")
        os.environ["AIHOT_API_URL"] = "http://127.0.0.1:9/api/health"
        try:
            loop_health.check_aihot_stack(findings, probe=fake_probe)
        finally:
            if old is None:
                os.environ.pop("AIHOT_API_URL", None)
            else:
                os.environ["AIHOT_API_URL"] = old
        self.assertEqual(findings, [])
        self.assertIn("http://127.0.0.1:9/api/health", seen)
        self.assertIn(loop_health.AIHOT_WEB_URL, seen)


class QueueGlueTests(unittest.TestCase):
    """tech#60: queue entry-glue guard - pure core, check face and CLI
    wiring. The R1891 anchor form (seed entry 58 glued to entry 57's
    tail without a leading newline - 'v1.65' + '58. [' direct join)
    must be named; the split clean baseline must stay silent."""

    def test_clean_split_lines_never_flag(self):
        files = {"tech.md":
                 "57. [R1890 ok] delivered, C-37 v1.65\n"
                 "58. [R1891 ok] seed\n"}
        self.assertEqual(loop_health.classify_queue_glue(files), [])

    def test_r1891_anchor_form_named(self):
        glued = ("57. [R1890 ok] delivered, C-37 v1.65"
                 "58. [R1891 seed] queue entry glue guard\n")
        findings = loop_health.classify_queue_glue({"tech.md": glued})
        self.assertEqual(warn_codes(findings), {"queue-glue"})
        msg = findings[0][2]
        self.assertIn("tech.md", msg)
        self.assertIn("1 glued queue entry head(s)", msg)
        self.assertIn("line 1", msg)
        self.assertIn("R1891", msg)
        # the version digits bleed into the matched head (v1.65 + 58. [)
        self.assertIn("558. [", msg)

    def test_done_style_head_glue_also_named(self):
        glued = "55. [done 2026-10-10 R1889] face table, C-36 v1.6456. [R1891 seed] next\n"
        findings = loop_health.classify_queue_glue({"tech.md": glued})
        self.assertEqual(warn_codes(findings), {"queue-glue"})
        self.assertIn("line 1", findings[0][2])

    def test_mid_line_only_head_flags(self):
        """A glued head on a continuation line (no head at col 0) is
        the same disease - the entry was still written without its
        leading newline."""
        glued = ("continuation text of entry 57, C-37 v1.65"
                 "58. [R1891 seed] glue\n")
        findings = loop_health.classify_queue_glue({"tech.md": glued})
        self.assertEqual(warn_codes(findings), {"queue-glue"})

    def test_per_file_findings_and_show_cap(self):
        lines = ["%d. [R1900 ok] tail, v1.6 %d. [R1901 seed] glue"
                 % (i, i + 1) for i in range(1, 6)]
        files = {"tech.md": "\n".join(lines) + "\n",
                 "main.md": "1. [R1900 ok] clean\n"}
        findings = loop_health.classify_queue_glue(files)
        self.assertEqual([f[1] for f in findings], ["queue-glue"])
        self.assertIn("tech.md", findings[0][2])
        self.assertIn("5 glued queue entry head(s)", findings[0][2])
        self.assertIn("(+2 more)", findings[0][2])
        self.assertNotIn("main.md", findings[0][2])  # clean file not named

    def test_check_face_missing_dir_silent(self):
        root = make_dir(self, "bs-glue-nodir-")
        findings = []
        loop_health.check_queue_glue(root, findings)
        self.assertEqual(findings, [])

    def test_check_face_reads_only_md_files(self):
        root = make_dir(self, "bs-glue-mixed-")
        qdir = root / "state" / "queue"
        qdir.mkdir(parents=True)
        (qdir / "notes.txt").write_text(
            "57. [R1890 ok] tail v1.65 58. [R1891 seed] glue\n",
            encoding="utf-8")
        findings = []
        loop_health.check_queue_glue(root, findings)
        self.assertEqual(findings, [])

    def test_check_face_names_glued_queue_file(self):
        root = make_dir(self, "bs-glue-real-")
        qdir = root / "state" / "queue"
        qdir.mkdir(parents=True)
        (qdir / "tech.md").write_text(
            "57. [R1890 ok] delivered, C-37 v1.65"
            "58. [R1891 seed] queue entry glue guard\n",
            encoding="utf-8")
        findings = []
        loop_health.check_queue_glue(root, findings)
        self.assertEqual(warn_codes(findings), {"queue-glue"})
        self.assertIn("tech.md", findings[0][2])

    def test_cli_wiring_glue_warns_never_fails(self):
        spec = [(30, "round done exit=0"), (10, "round done exit=0")]
        root = make_repo(self, spec, make_state(tick=2), BOARD)
        qdir = root / "state" / "queue"
        qdir.mkdir(parents=True)
        (qdir / "tech.md").write_text(
            "57. [R1890 ok] delivered, C-37 v1.65"
            "58. [R1891 seed] queue entry glue guard\n",
            encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(["loop_health.py", "--root", str(root)])
        self.assertEqual(rc, 0)  # WARN verdict, never a probe-break FAIL
        self.assertIn("queue-glue", buf.getvalue())

    def test_cli_wiring_clean_queue_silent(self):
        spec = [(30, "round done exit=0"), (10, "round done exit=0")]
        root = make_repo(self, spec, make_state(tick=2), BOARD)
        qdir = root / "state" / "queue"
        qdir.mkdir(parents=True)
        for name, text in (("main.md", "1. [R1900 ok] clean\n"),
                           ("tech.md", "2. [R1900 ok] clean\n"),
                           ("explore.md", "3. [R1900 ok] clean\n")):
            (qdir / name).write_text(text, encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(["loop_health.py", "--root", str(root)])
        self.assertEqual(rc, 0)
        self.assertNotIn("queue-glue", buf.getvalue())

    def test_real_repo_clean_baseline_smoke(self):
        """Judgement criterion 1: the real state/queue/*.md files (the
        R1893 split left them clean) must produce zero queue-glue
        findings - read-only smoke through the pure core."""
        files = {}
        for path in sorted((REPO / "state" / "queue").glob("*.md")):
            files[path.name] = path.read_text(
                encoding="utf-8-sig", errors="replace")
        self.assertEqual(loop_health.classify_queue_glue(files), [])


@unittest.skipIf(shutil.which("git") is None, "git binary not available")
class AccountUncommittedTests(unittest.TestCase):
    """tech#61: round accounting-chain completeness guard - pure core,
    HEAD-read seam, check face and CLI wiring. The R1893 anchor form
    (closing stage-2 wrote the tick to disk, the round died before the
    accounting commit) must be named; the committed clean tree, the
    same-tick closing transient and every unreadable side stay silent."""

    BEAT_SPEC = [(0, "round done exit=0"), (5, "round done exit=0")]

    def _repo(self):
        return make_repo(self, self.BEAT_SPEC, make_state(tick=1892), BOARD)

    def _git_repo(self, head_tick=1892, disk_tick=1893):
        """Real-git fixture reproducing the R1893 form: state.json
        committed at head_tick, then the on-disk copy bumped to
        disk_tick and left uncommitted (the died-before-commit form)."""
        root = self._repo()
        state_path = root / "src" / "os" / "state.json"
        state_path.write_text(
            json.dumps(make_state(tick=head_tick), ensure_ascii=True),
            encoding="utf-8")
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                   GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        for args in (["init", "-q"], ["add", "src/os/state.json"],
                     ["commit", "-q", "-m", "state"]):
            p = subprocess.run(["git"] + args, cwd=str(root), env=env,
                               capture_output=True, timeout=30)
            if p.returncode != 0:
                self.skipTest(
                    "git fixture unavailable: %.60s"
                    % p.stderr.decode("utf-8", "replace"))
        state_path.write_text(
            json.dumps(make_state(tick=disk_tick), ensure_ascii=True),
            encoding="utf-8")
        return root

    def _disk_state(self, root):
        return json.loads(
            (root / "src" / "os" / "state.json").read_text(encoding="utf-8"))

    def test_r1893_anchor_form_named(self):
        findings = loop_health.classify_account_uncommitted(1892, 1893, True)
        self.assertEqual(warn_codes(findings), {"account-uncommitted"})
        msg = findings[0][2]
        self.assertIn("tick=1893", msg)
        self.assertIn("HEAD tick=1892", msg)
        self.assertIn("R1893", msg)

    def test_committed_tree_and_same_tick_transient_silent(self):
        # accounting committed: clean tree - judgement criterion 2
        self.assertEqual(
            loop_health.classify_account_uncommitted(1893, 1893, False), [])
        # closing transient: same tick, file dirty - not the seed form
        self.assertEqual(
            loop_health.classify_account_uncommitted(1893, 1893, True), [])

    def test_unreadable_or_backward_sides_silent(self):
        self.assertEqual(
            loop_health.classify_account_uncommitted(None, 1893, True), [])
        self.assertEqual(
            loop_health.classify_account_uncommitted(1892, None, True), [])
        # HEAD ahead of disk is another face's disease - scope stays tight
        self.assertEqual(
            loop_health.classify_account_uncommitted(1895, 1893, True), [])

    def test_read_head_tick_seam(self):
        root = self._repo()

        def ok(_root):
            return json.dumps(make_state(tick=1892)).encode()

        def bad_rc(_root):
            return None

        def garbage(_root):
            return b"not json"
        self.assertEqual(
            loop_health.read_head_state_tick(root, show=ok), 1892)
        self.assertIsNone(
            loop_health.read_head_state_tick(root, show=bad_rc))
        self.assertIsNone(
            loop_health.read_head_state_tick(root, show=garbage))

    def test_check_face_non_git_tree_silent(self):
        # temp tree without .git: HEAD read yields None -> advisory skip
        root = self._repo()
        findings = []
        loop_health.check_account_uncommitted(
            root, make_state(tick=1893), findings)
        self.assertEqual(findings, [])

    def test_git_fixture_check_face_names(self):
        # judgement criterion 1 at the check-face level: the committed-
        # 1892 / disk-1893-dirty form is named
        root = self._git_repo(head_tick=1892, disk_tick=1893)
        findings = []
        loop_health.check_account_uncommitted(
            root, self._disk_state(root), findings)
        self.assertEqual(warn_codes(findings), {"account-uncommitted"})

    def test_git_fixture_committed_silent(self):
        # judgement criterion 2 at the check-face level: committed tree
        # (HEAD == disk, clean) yields no finding
        root = self._git_repo(head_tick=1893, disk_tick=1893)
        findings = []
        loop_health.check_account_uncommitted(
            root, self._disk_state(root), findings)
        self.assertEqual(findings, [])

    def test_cli_wired_on_git_fixture(self):
        root = self._git_repo(head_tick=1892, disk_tick=1893)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = loop_health.main(["loop_health.py", "--root", str(root)])
        self.assertIn("account-uncommitted", buf.getvalue())
        self.assertEqual(rc, 0)  # WARN-level face never fails the probe

    def test_real_repo_clean_baseline_smoke(self):
        """Judgement criterion 3 (round-start face): in the real repo the
        accounting is committed at round open (disk tick == HEAD tick),
        so the guard must stay silent on the committed clean baseline.
        Read-only: if a concurrent window is mid-closing (disk ahead),
        the WARN is the guard working as designed - assert only that the
        face never FAILs the probe and never crashes."""
        findings = []
        loop_health.check_account_uncommitted(
            REPO, json.loads((REPO / "src" / "os" / "state.json").read_text(
                encoding="utf-8-sig", errors="replace")), findings)
        self.assertNotIn("account-uncommitted", fail_codes(findings))


if __name__ == "__main__":
    unittest.main(verbosity=2)
