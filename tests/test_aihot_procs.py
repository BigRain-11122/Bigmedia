"""Unit tests for the AIHOT stack process-topology probe
(src/os/aihot_procs.py). tech#125.

All fixtures are hermetic (pure-core + injected runners); the R2038
live topology (proxy 65752 'server.ts' / worker 4576 / api 73084, the
latter two same-shape 'src/main.ts' cmdline) is the anchor case the
misread-killed-API gap was proven on. One read-only smoke case runs
the real probe against the live stack and asserts only the rc
contract (never the live verdict -- the stack may legitimately be
restarting during a test run).

Run:
    python tests/test_aihot_procs.py
"""
import io
import json
import tempfile
import contextlib
import unittest
from pathlib import Path
from unittest import mock

import src.os.aihot_procs as ap


def ps_json(rows):
    """[(pid, cmd)] -> ConvertTo-Json -Compress shape (list for >1,
    bare dict for exactly 1 -- the PS quirk parse_ps_procs handles)."""
    items = [{"ProcessId": pid, "CommandLine": cmd} for pid, cmd in rows]
    if len(items) == 1:
        return json.dumps(items[0])
    return json.dumps(items)


# R2038 anchor: the live topology as measured 10-12 08:2x (netstat
# 3100->65752 / 3101->73084; worker 4576 unbound same-shape).
R2038_PROCS = [
    (65752, "node  --env-file-if-exists=../../.env server.ts"),
    (4576, "node  --env-file-if-exists=../../.env src/main.ts"),
    (73084, "node  --env-file-if-exists=../../.env src/main.ts"),
]
R2038_OWNERS = {3100: [65752], 3101: [73084]}

NETSTAT_SAMPLE = (
    "\n  TCP    127.0.0.1:3100         0.0.0.0:0              LISTENING       65752\n"
    "  TCP    127.0.0.1:3101         0.0.0.0:0              LISTENING       73084\n"
    "  TCP    127.0.0.1:31010        0.0.0.0:0              LISTENING       11111\n"
    "  TCP    127.0.0.1:8188         0.0.0.0:0              ESTABLISHED     22222\n"
    "  UDP    127.0.0.1:3101         *:*                                    33333\n"
)


class TestParsePsProcs(unittest.TestCase):
    def test_list_shape(self):
        out = ap.parse_ps_procs(ps_json(R2038_PROCS))
        self.assertEqual(sorted(out), sorted(R2038_PROCS))

    def test_single_dict_shape(self):
        out = ap.parse_ps_procs(ps_json([(4576, "node x src/main.ts")]))
        self.assertEqual(out, [(4576, "node x src/main.ts")])

    def test_empty_stdout_means_zero_procs(self):
        self.assertEqual(ap.parse_ps_procs("   \n"), [])

    def test_junk_is_none(self):
        self.assertIsNone(ap.parse_ps_procs("not json {"))

    def test_missing_key_is_none(self):
        self.assertIsNone(ap.parse_ps_procs(json.dumps([{"Other": 1}])))


class TestParseNetstat(unittest.TestCase):
    def test_listeners_only(self):
        owners = ap.parse_netstat_listeners(NETSTAT_SAMPLE, (3101, 3100))
        self.assertEqual(owners, {3100: [65752], 3101: [73084]})

    def test_port_boundary_no_prefix_match(self):
        # 31010 must NOT count as 3101 (colon boundary law).
        owners = ap.parse_netstat_listeners(NETSTAT_SAMPLE, (3101,))
        self.assertEqual(owners, {3101: [73084]})

    def test_udp_rows_ignored(self):
        # The UDP :3101 row (no LISTENING state) must not leak in.
        owners = ap.parse_netstat_listeners(NETSTAT_SAMPLE, (3100, 3101))
        self.assertNotIn(33333, owners[3101])

    def test_junk_pid_on_listening_row_is_none(self):
        bad = "  TCP    127.0.0.1:3101    0.0.0.0:0    LISTENING       notapid\n"
        self.assertIsNone(ap.parse_netstat_listeners(bad, (3101,)))


class TestClassifyTopology(unittest.TestCase):
    def test_complete_r2038_anchor(self):
        topo = ap.classify_topology(R2038_PROCS, R2038_OWNERS)
        self.assertEqual(topo["verdict"], "complete")
        self.assertEqual(topo["roles"],
                         {"proxy": 65752, "api": 73084, "worker": 4576})

    def test_missing_api_when_no_binding(self):
        topo = ap.classify_topology(R2038_PROCS, {3100: [65752]})
        self.assertEqual(topo["verdict"], "missing-api")
        self.assertIsNone(topo["roles"]["api"])
        # Same-shape pids stay unproven for the worker too.
        self.assertIsNone(topo["roles"]["worker"])

    def test_stale_port_owner_not_in_procs(self):
        owners = {3100: [65752], 3101: [99999]}
        topo = ap.classify_topology(R2038_PROCS, owners)
        self.assertEqual(topo["verdict"], "missing-api")

    def test_missing_worker(self):
        procs = [R2038_PROCS[0], R2038_PROCS[2]]
        topo = ap.classify_topology(procs, R2038_OWNERS)
        self.assertEqual(topo["verdict"], "missing-worker")

    def test_ambiguous_worker_refuses(self):
        procs = R2038_PROCS + [(111, "node --env-file-if-exists=../../.env src/main.ts")]
        owners = {3100: [65752], 3101: [73084]}
        topo = ap.classify_topology(procs, owners)
        self.assertEqual(topo["verdict"], "missing-worker")
        self.assertIsNone(topo["roles"]["worker"])
        self.assertIn(111, topo["worker_candidates"])
        self.assertTrue(any("ambiguous" in n for n in topo["notes"]))

    def test_multiple_api_owners_refused(self):
        owners = {3100: [65752], 3101: [73084, 999]}
        procs = R2038_PROCS + [(999, "node --env-file-if-exists=../../.env src/main.ts")]
        topo = ap.classify_topology(procs, owners)
        self.assertEqual(topo["verdict"], "missing-api")
        self.assertIsNone(topo["roles"]["api"])
        self.assertTrue(any("multiple" in n for n in topo["notes"]))

    def test_proxy_shape_fallback_when_unbound(self):
        owners = {3101: [73084]}
        topo = ap.classify_topology(R2038_PROCS, owners)
        self.assertEqual(topo["verdict"], "complete")
        self.assertEqual(topo["roles"]["proxy"], 65752)
        self.assertTrue(any("shape" in e for e in topo["evidence"]
                            if "proxy" in e))

    def test_api_outranks_worker_shape(self):
        # api pid owns 3101 AND carries the src/main.ts shape; it must
        # never be classified as the worker.
        topo = ap.classify_topology(R2038_PROCS, R2038_OWNERS)
        self.assertEqual(topo["roles"]["worker"], 4576)
        self.assertNotEqual(topo["roles"]["api"], 4576)


class TestRunProbe(unittest.TestCase):
    def test_complete_via_injected_runners(self):
        result = ap.run_probe(
            ps_runner=lambda cmd: (True, ps_json(R2038_PROCS)),
            netstat_runner=lambda: (True, NETSTAT_SAMPLE))
        self.assertEqual(result["rc"], ap.RC_COMPLETE)
        self.assertEqual(result["verdict"], "complete")
        self.assertEqual(result["roles"]["worker"], 4576)

    def test_ps_face_failure_fail_closed(self):
        result = ap.run_probe(ps_runner=lambda cmd: (False, ""),
                              netstat_runner=lambda: (True, NETSTAT_SAMPLE))
        self.assertEqual(result["rc"], ap.RC_ERROR)
        self.assertIsNone(result["verdict"])

    def test_ps_junk_fail_closed(self):
        result = ap.run_probe(ps_runner=lambda cmd: (True, "junk{"),
                              netstat_runner=lambda: (True, NETSTAT_SAMPLE))
        self.assertEqual(result["rc"], ap.RC_ERROR)

    def test_netstat_face_failure_fail_closed(self):
        result = ap.run_probe(ps_runner=lambda cmd: (True, ps_json(R2038_PROCS)),
                              netstat_runner=lambda: (False, ""))
        self.assertEqual(result["rc"], ap.RC_ERROR)

    def test_anomaly_rc_one(self):
        result = ap.run_probe(
            ps_runner=lambda cmd: (True, ps_json([R2038_PROCS[0], R2038_PROCS[2]])),
            netstat_runner=lambda: (True, NETSTAT_SAMPLE))
        self.assertEqual(result["rc"], ap.RC_ANOMALY)
        self.assertEqual(result["verdict"], "missing-worker")


class TestLedgerRow(unittest.TestCase):
    def test_row_shape(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sub" / "ledger.jsonl"
            result = {"ts": "2026-10-12 09:00:00", "verdict": "complete",
                      "rc": 0,
                      "roles": {"proxy": 65752, "api": 73084, "worker": 4576}}
            ap.append_ledger_row(path, result)
            rows = [json.loads(l) for l in
                    path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["api_pid"], 73084)
        self.assertEqual(rows[0]["worker_pid"], 4576)
        self.assertEqual(rows[0]["verdict"], "complete")

    def test_bad_path_never_raises(self):
        result = {"ts": "t", "verdict": None, "rc": 2, "roles": {}}
        with contextlib.redirect_stderr(io.StringIO()) as captured:
            ap.append_ledger_row("Z:\\no\\such\\dir\\x.jsonl", result)
        self.assertIn("WARN", captured.getvalue())


class TestCli(unittest.TestCase):
    def test_json_and_rc_propagation(self):
        payload = {"ts": "t", "status": "ok", "rc": 0,
                   "verdict": "complete",
                   "roles": {"proxy": 1, "api": 2, "worker": 3},
                   "evidence": [], "notes": [], "worker_candidates": []}
        with mock.patch.object(ap, "run_probe", return_value=payload), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            rc = ap.main(["--json"])
        self.assertEqual(rc, 0)
        data = json.loads(out.getvalue())
        self.assertEqual(data["roles"]["worker"], 3)

    def test_anomaly_rc_propagation_and_judgment_law(self):
        payload = {"ts": "t", "status": "ok", "rc": 1,
                   "verdict": "missing-worker",
                   "roles": {"proxy": 1, "api": 2, "worker": None},
                   "evidence": [], "notes": ["ambiguous x"],
                   "worker_candidates": [9, 10]}
        with mock.patch.object(ap, "run_probe", return_value=payload), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            rc = ap.main([])
        self.assertEqual(rc, 1)
        self.assertIn("do NOT", out.getvalue())

    def test_ledger_flag_writes_row(self):
        payload = {"ts": "t", "status": "ok", "rc": 0,
                   "verdict": "complete",
                   "roles": {"proxy": 1, "api": 2, "worker": 3},
                   "evidence": [], "notes": [], "worker_candidates": []}
        with tempfile.TemporaryDirectory() as td, \
                mock.patch.object(ap, "run_probe", return_value=payload), \
                contextlib.redirect_stdout(io.StringIO()):
            rc = ap.main(["--ledger", str(Path(td) / "l.jsonl")])
            rows_written = len(list(Path(td).glob("l.jsonl")))
        self.assertEqual(rc, 0)
        self.assertEqual(rows_written, 1)


class TestLiveSmoke(unittest.TestCase):
    """Read-only smoke: the real probe must honor the rc contract
    against the live stack (whatever its current state is)."""

    def test_live_probe_rc_contract(self):
        result = ap.run_probe()
        self.assertIn(result["rc"], (ap.RC_COMPLETE, ap.RC_ANOMALY,
                                     ap.RC_ERROR))
        if result["rc"] == ap.RC_COMPLETE:
            self.assertEqual(result["verdict"], "complete")
            self.assertTrue(all(result["roles"].values()))


if __name__ == "__main__":
    unittest.main()
