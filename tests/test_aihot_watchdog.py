# -*- coding: utf-8 -*-
"""Hermetic tests for the AIHOT autoheal watchdog (tech#127).

Seams: topology_runner / pg_runner / spawn / clock / wait are injected;
nothing here touches the real stack, the scheduled task, or any bat.
"""
import datetime
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "os"))

import aihot_watchdog as wd


def topo_result(rc, verdict):
    return {"rc": rc, "verdict": verdict, "roles": {}}


class FakeClock(object):
    def __init__(self, start="2026-10-12 12:00:00"):
        self.now = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")

    def advance(self, **kw):
        self.now += datetime.timedelta(**kw)

    def __call__(self):
        return self.now


class TmpBase(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = Path(tempfile.mkdtemp(prefix="wd-t127-"))
        self.state_path = self.tmp / "state.json"
        self.ledger_path = self.tmp / "ledger.jsonl"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_state(self, state):
        self.state_path.write_text(
            json.dumps(state, ensure_ascii=True), encoding="ascii")

    def read_rows(self):
        if not self.ledger_path.exists():
            return []
        rows = []
        for line in self.ledger_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    def run_cycle(self, topo, pg_ok=True, pause_state=None, spawn=None,
                  clock=None):
        # pause flag models reality: set ONCE by an external hand; the
        # watchdog preserves it across cycles (re-writing it each cycle
        # would clobber the throttle bookkeeping it owns).
        if pause_state is not None and not self.state_path.exists():
            self.write_state(pause_state)
        calls = {"spawned": []}

        def fake_spawn(bat):
            calls["spawned"].append(Path(bat).name)
            return True

        runner = topo if callable(topo) else (lambda: topo)
        rc = wd.run_once(
            topology_runner=runner, pg_runner=(lambda: pg_ok),
            spawn=spawn or fake_spawn,
            state_path=self.state_path, ledger_path=self.ledger_path,
            clock=clock or FakeClock(), wait=lambda s: None)
        return rc, calls["spawned"]


class TestDecideActions(unittest.TestCase):
    def test_healthy_noop(self):
        actions, skip = wd.decide_actions(topo_result(0, "complete"), True, False)
        self.assertEqual(actions, [])
        self.assertIsNone(skip)

    def test_pg_down_always_heals_even_when_topo_complete(self):
        actions, skip = wd.decide_actions(topo_result(0, "complete"), False, False)
        self.assertEqual([k for k, _ in actions], ["pg"])
        self.assertIsNone(skip)

    def test_missing_api_maps_api_bat(self):
        actions, _ = wd.decide_actions(topo_result(1, "missing-api"), True, False)
        self.assertEqual(actions, [("api", wd.ROLE_BATS["api"])])

    def test_missing_proxy_maps_web_bat(self):
        actions, _ = wd.decide_actions(topo_result(1, "missing-proxy"), True, False)
        self.assertEqual(actions, [("proxy", wd.ROLE_BATS["proxy"])])

    def test_missing_worker_heals_when_not_paused(self):
        actions, _ = wd.decide_actions(topo_result(1, "missing-worker"), True, False)
        self.assertEqual(actions, [("worker", wd.ROLE_BATS["worker"])])

    def test_missing_worker_skips_when_paused(self):
        actions, skip = wd.decide_actions(topo_result(1, "missing-worker"), True, True)
        self.assertEqual(actions, [])
        self.assertEqual(skip, "pause")

    def test_probe_error_fail_closed(self):
        actions, skip = wd.decide_actions(topo_result(2, None), True, False)
        self.assertEqual(actions, [])
        self.assertIsNone(skip)
        actions, _ = wd.decide_actions(None, True, False)
        self.assertEqual(actions, [])

    def test_probe_error_plus_pg_down_heals_pg_only(self):
        # fail-closed applies to NODE roles only; PG is a light service
        actions, _ = wd.decide_actions(topo_result(2, None), False, False)
        self.assertEqual([k for k, _ in actions], ["pg"])


class TestPauseFace(unittest.TestCase):
    def test_absent_flag_inactive(self):
        active, note = wd.pause_face({})
        self.assertFalse(active)
        self.assertIsNone(note)

    def test_active_flag(self):
        state = {"pause": {"worker_restart_paused": True,
                           "ts": "2026-10-12 11:40:00",
                           "reason": "O-20261012-1115 CEO yield pause"}}
        active, note = wd.pause_face(state)
        self.assertTrue(active)
        self.assertIn("O-20261012-1115", note)

    def test_stale_flag_note(self):
        state = {"pause": {"worker_restart_paused": True,
                           "ts": "2026-10-08 00:00:00", "reason": "old"}}
        active, note = wd.pause_face(state)
        self.assertTrue(active)
        self.assertIn("STALE", note)

    def test_malformed_flag_fails_closed(self):
        active, note = wd.pause_face({"pause": "yes"})
        self.assertTrue(active)
        self.assertIn("fail-closed", note)

    def test_flag_false_inactive(self):
        active, _ = wd.pause_face(
            {"pause": {"worker_restart_paused": False}})
        self.assertFalse(active)


class TestRunOnce(TmpBase):
    def test_heartbeat_once_per_day(self):
        clock = FakeClock()
        rc, spawned = self.run_cycle(topo_result(0, "complete"), clock=clock)
        self.assertEqual(rc, 0)
        self.assertEqual(spawned, [])
        self.assertEqual([r["event"] for r in self.read_rows()],
                         ["heartbeat"])
        # same day: no second heartbeat
        clock.advance(hours=1)
        self.run_cycle(topo_result(0, "complete"), clock=clock)
        self.assertEqual(len(self.read_rows()), 1)
        # next day: one more
        clock.advance(days=1)
        self.run_cycle(topo_result(0, "complete"), clock=clock)
        self.assertEqual([r["event"] for r in self.read_rows()],
                         ["heartbeat", "heartbeat"])

    def test_pause_skip_throttled_6h(self):
        pause = {"pause": {"worker_restart_paused": True,
                           "ts": "2026-10-12 11:40:00",
                           "reason": "O-20261012-1115 CEO yield pause"}}
        clock = FakeClock()
        rc, spawned = self.run_cycle(topo_result(1, "missing-worker"),
                                      pause_state=pause, clock=clock)
        self.assertEqual(rc, 0)
        self.assertEqual(spawned, [])  # the whole point: no worker restart
        self.assertEqual([r["event"] for r in self.read_rows()],
                         ["skip-pause"])
        # 1h later: throttled, no new row
        clock.advance(hours=1)
        self.run_cycle(topo_result(1, "missing-worker"),
                       pause_state=pause, clock=clock)
        self.assertEqual(len(self.read_rows()), 1)
        # 7h after the first row: logs again
        clock.advance(hours=6)
        self.run_cycle(topo_result(1, "missing-worker"),
                       pause_state=pause, clock=clock)
        self.assertEqual([r["event"] for r in self.read_rows()],
                         ["skip-pause", "skip-pause"])

    def test_heal_api_flow_recovers(self):
        runner = [topo_result(1, "missing-api"), topo_result(0, "complete")]
        rc, spawned = self.run_cycle(
            lambda: runner.pop(0) if runner else topo_result(0, "complete"))
        self.assertEqual(rc, 0)
        self.assertEqual(spawned, ["api-restart.bat"])
        rows = self.read_rows()
        self.assertEqual(rows[-1]["event"], "heal")
        self.assertEqual(rows[-1]["actions"], ["api"])
        self.assertEqual(rows[-1]["before"]["verdict"], "missing-api")
        self.assertEqual(rows[-1]["after"]["verdict"], "complete")

    def test_heal_verify_failed_rc1(self):
        runner = [topo_result(1, "missing-api"), topo_result(1, "missing-api")]
        rc, spawned = self.run_cycle(
            lambda: runner.pop(0) if runner else topo_result(1, "missing-api"))
        self.assertEqual(rc, 1)
        self.assertEqual(spawned, ["api-restart.bat"])

    def test_probe_error_throttled_rc2(self):
        clock = FakeClock()
        rc, _ = self.run_cycle(topo_result(2, None), clock=clock)
        self.assertEqual(rc, 2)
        self.assertEqual([r["event"] for r in self.read_rows()],
                         ["probe-error"])
        clock.advance(minutes=30)
        rc, _ = self.run_cycle(topo_result(2, None), clock=clock)
        self.assertEqual(rc, 2)
        self.assertEqual(len(self.read_rows()), 1)  # 1h throttle
        clock.advance(minutes=31)
        rc, _ = self.run_cycle(topo_result(2, None), clock=clock)
        self.assertEqual(len(self.read_rows()), 2)

    def test_fresh_lock_skips(self):
        clock = FakeClock()
        self.write_state(
            {"lock_ts": (clock.now + datetime.timedelta(minutes=1))
             .strftime("%Y-%m-%d %H:%M:%S")})
        rc, spawned = self.run_cycle(topo_result(1, "missing-api"),
                                     clock=clock)
        self.assertEqual(rc, 0)
        self.assertEqual(spawned, [])
        self.assertEqual([r["event"] for r in self.read_rows()],
                         ["lock-skip"])

    def test_spawn_failure_still_verifies(self):
        runner = [topo_result(1, "missing-api"), topo_result(0, "complete")]
        rc, spawned = self.run_cycle(
            lambda: runner.pop(0) if runner else topo_result(0, "complete"),
            spawn=lambda bat: False)
        self.assertEqual(spawned, [])
        self.assertEqual(rc, 0)  # nothing spawned -> no wait/verify branch


class TestRepoReality(unittest.TestCase):
    def test_canonical_bats_exist(self):
        for bat in (wd.PG_BAT, wd.ROLE_BATS["api"],
                    wd.ROLE_BATS["proxy"], wd.ROLE_BATS["worker"]):
            self.assertTrue(bat.exists(), "missing canonical bat: %s" % bat)

    def test_spawn_uses_create_no_window_not_detached(self):
        src = Path(wd.__file__).read_text(encoding="utf-8")
        marker = ("creationflags=CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP)")
        self.assertIn(marker, src)
        self.assertNotIn("0x00000008", src)  # DETACHED_PROCESS forbidden

    def test_python_child_never_flash(self):
        src = Path(wd.__file__).read_text(encoding="utf-8")
        self.assertIn("creationflags=CREATE_NO_WINDOW)",
                      src.split("def _real_topology_runner")[1]
                         .split("def ")[0])

    def test_pause_flag_lives_in_repo_local_state(self):
        self.assertIn("data", wd.STATE_PATH.parts)
        self.assertIn("pipeline", wd.STATE_PATH.parts)


if __name__ == "__main__":
    unittest.main()
