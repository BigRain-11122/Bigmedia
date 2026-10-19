"""Unit tests for the AIHOT one-key recovery runbook
(tools/aihot_restart.py). tech#238.

Hermetic pure-core fixtures: decide() / parse_env_ports() /
read_recent_heal() / build_wmi_snippet() run against injected
topology dicts and ledger text -- no live stack is mutated. One
read-only smoke case runs the real script with --dry-run against the
live stack and asserts only the rc contract and plan shape, never a
live verdict (the stack may legitimately be mid-heal).

Anchor case (2026-10-19): the multi-node kill healed by the watchdog
across three PT5M cycles (10:20:30 pg+api / 10:25:29 proxy /
10:30:28 worker) while R2381 ran a redundant manual recovery -- the
standoff law and the multi-face roles-dict derivation below are the
fix.

Run:
    python tests/test_aihot_restart.py
"""
import datetime
import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tools.aihot_restart as ar


def topo(verdict, api=None, proxy=None, worker=None, status="ok", rc=1,
         notes=None):
    return {"status": status, "rc": rc, "verdict": verdict,
            "roles": {"api": api, "proxy": proxy, "worker": worker},
            "notes": list(notes or []), "evidence": []}


def heal_line(ts, actions=("proxy",)):
    return json.dumps({"event": "heal", "actions": list(actions), "ts": ts})


class ParseEnvPortsTests(unittest.TestCase):
    def test_full_derivation(self):
        text = ("API_PORT=4101\nWEB_PORT=4100\n"
                "DATABASE_URL=postgres://u:secret@127.0.0.1:65532/aihot\n")
        ports, notes = ar.parse_env_ports(text)
        self.assertEqual(ports, {"api": 4101, "web": 4100, "pg": 65532})
        self.assertEqual(notes, [])

    def test_fallback_defaults_with_notes(self):
        ports, notes = ar.parse_env_ports("")
        self.assertEqual(ports["api"], ar.DEFAULT_API_PORT)
        self.assertEqual(ports["web"], ar.DEFAULT_WEB_PORT)
        self.assertEqual(ports["pg"], ar.PG_PORT)
        self.assertEqual(len(notes), 3)  # one drift note per defaulted port

    def test_bad_values_fall_back_with_note(self):
        text = "API_PORT=abc\nWEB_PORT=3100\nDATABASE_URL=postgres://x@h/db\n"
        ports, notes = ar.parse_env_ports(text)
        self.assertEqual(ports["api"], ar.DEFAULT_API_PORT)
        self.assertEqual(ports["web"], 3100)
        self.assertEqual(ports["pg"], ar.PG_PORT)
        self.assertTrue(any("API_PORT" in note for note in notes))


class ReadRecentHealTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime(2026, 10, 19, 11, 30, 0)

    def test_fresh_heal_row_found(self):
        text = (heal_line("2026-10-19 11:25:29") + "\n"
                + json.dumps({"event": "heartbeat",
                              "ts": "2026-10-19 11:30:01"}) + "\n")
        row, age = ar.read_recent_heal(text, self.now, window_s=420)
        self.assertIsNotNone(row)
        self.assertEqual(row.get("ts"), "2026-10-19 11:25:29")
        self.assertAlmostEqual(age, 271.0)

    def test_stale_heal_ignored(self):
        row, age = ar.read_recent_heal(heal_line("2026-10-19 10:30:28"),
                                       self.now, 420)
        self.assertIsNone(row)
        self.assertIsNone(age)

    def test_nonheal_rows_only(self):
        text = json.dumps({"event": "heartbeat", "ts": "2026-10-19 11:29:00"})
        row, age = ar.read_recent_heal(text + "\n", self.now, 420)
        self.assertIsNone(row)
        self.assertIsNone(age)

    def test_future_row_counts_as_fresh(self):
        row, age = ar.read_recent_heal(heal_line("2026-10-19 11:35:00"),
                                        self.now, 420)
        self.assertIsNotNone(row)
        self.assertEqual(age, 0.0)


class DecideTests(unittest.TestCase):
    def test_healthy_noop(self):
        plan = ar.decide(topo("complete", api=111, proxy=222, worker=333,
                              rc=0), True)
        self.assertEqual(plan["terminal"], "healthy")
        self.assertEqual(plan["actions"], [])

    def test_multiface_from_roles(self):
        # verdict is a single enum (missing-api) but the proxy is down
        # too; the roles dict carries the full multi-face truth.
        plan = ar.decide(topo("missing-api", api=None, proxy=None,
                              worker=333), False)
        self.assertEqual(plan["terminal"], "heal")
        self.assertEqual(plan["actions"], ["pg", "api", "proxy"])

    def test_worker_only(self):
        plan = ar.decide(topo("missing-worker", api=1, proxy=2, worker=None),
                         True)
        self.assertEqual(plan["actions"], ["worker"])

    def test_standoff_blocks_action(self):
        heal = {"ts": "2026-10-19 11:25:29"}
        plan = ar.decide(topo("missing-proxy", api=1, proxy=None, worker=2),
                         True, heal_row=heal, heal_age=120.0)
        self.assertEqual(plan["terminal"], "standoff")
        self.assertEqual(plan["actions"], [])

    def test_force_overrides_standoff(self):
        heal = {"ts": "2026-10-19 11:25:29"}
        plan = ar.decide(topo("missing-proxy", api=1, proxy=None, worker=2),
                         True, heal_row=heal, heal_age=120.0, force=True)
        self.assertEqual(plan["terminal"], "heal")
        self.assertEqual(plan["actions"], ["proxy"])

    def test_probe_error_refused(self):
        for bad in (None, {"status": "error", "rc": 2, "verdict": None}):
            plan = ar.decide(bad, True)
            self.assertEqual(plan["terminal"], "refused")
            self.assertEqual(plan["actions"], [])

    def test_pause_law_gates_worker_only(self):
        plan = ar.decide(topo("missing-worker", api=1, proxy=2, worker=None),
                         True, pause_active=True)
        self.assertEqual(plan["terminal"], "pause")
        self.assertEqual(plan["actions"], [])

    def test_pause_law_keeps_other_faces(self):
        plan = ar.decide(topo("missing-api", api=None, proxy=None,
                              worker=None), True, pause_active=True)
        self.assertEqual(plan["actions"], ["api", "proxy"])


class BuildWmiSnippetTests(unittest.TestCase):
    def test_snippet_shape(self):
        snippet = ar.build_wmi_snippet(
            r"C:\repo\data\assets\aihot-poc\web-restart.bat")
        self.assertIn("Win32_Process", snippet)
        self.assertIn("web-restart.bat", snippet)
        self.assertIn("cmd /c", snippet)
        self.assertIn("ReturnValue", snippet)

    def test_quote_in_path_refused(self):
        with self.assertRaises(ValueError):
            ar.build_wmi_snippet('C:\\bad"quote\\web.bat')


class LiveDryRunSmoke(unittest.TestCase):
    """Read-only: run --dry-run --json; assert the rc contract and
    plan shape only (the stack may legitimately be mid-heal)."""

    def test_dry_run_contract(self):
        root = Path(__file__).resolve().parents[1]
        proc = subprocess.run(
            [sys.executable, str(root / "tools" / "aihot_restart.py"),
             "--dry-run", "--json"],
            capture_output=True, timeout=180)
        self.assertIn(proc.returncode, (0, 1, 2))
        payload = json.loads(
            proc.stdout.decode("utf-8", "replace").strip().splitlines()[-1])
        self.assertIn("plan", payload)
        self.assertIn(payload["plan"]["terminal"],
                      ("healthy", "standoff", "pause", "plan", "refused"))
        self.assertIn("rc", payload)


if __name__ == "__main__":
    unittest.main()
