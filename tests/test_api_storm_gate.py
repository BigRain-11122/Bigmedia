"""Unit tests for src/os/api_storm_gate.ps1 (tech#205 API 503-storm preflight).

Drives the real PowerShell engine against synthetic flag/err/ledger files in
a temp dir, so each case doubles as a live proof of the gate decision table:
  Arm:  armed (err signature hits >= threshold) | noarm (below / err missing)
  Gate: ignite no-flag (fast path, zero probe cost) |
        ignite flag-expired (stuck probe can never starve the loop) |
        ignite probe-pass (disarm, flag cleared, zero ledger noise) |
        defer probe-fail (flag kept, API_STORM_DEFER ledger line) |
        defer probe-timeout (probe tree force-killed, pid proven gone) |
        ignite fail-open (probe exe missing; flag kept for next slot)
"""
import os
import re
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GATE = REPO / "src" / "os" / "api_storm_gate.ps1"
PS = "powershell.exe"


def run_gate(extra):
    cmd = [PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(GATE)] + extra
    proc = subprocess.run(
        cmd, capture_output=True, text=True, timeout=90,
        encoding="utf-8", errors="replace",
    )
    return proc.returncode, proc.stdout.strip()


def write_err(directory, n_503):
    """Synthetic killed-round stderr mirroring round_20261018_005202.err:
    each storm line carries both family signatures (503 + generateJson)."""
    err = Path(directory) / "round.err"
    lines = []
    for _ in range(n_503):
        lines.append(
            "Error generating JSON content via API. Full report available at: "
            "gemini-client-error-generateJson-api.log 503 Service Unavailable"
        )
    lines.append("WARNING: benign stderr line")
    err.write_text("\n".join(lines) + "\n", encoding="ascii")
    return err


class TestApiStormGate(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="bs-storm-gate-")
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)
        self.flag = self.dir / "api-storm.flag"
        self.ledger = self.dir / "cloud-cap-ledger.txt"
        self.outdir = self.dir / "probes"

    # ---------- Arm ----------

    def test_arm_signature_writes_flag(self):
        err = write_err(self.dir, 15)
        rc, out = run_gate(["-Verb", "Arm", "-ErrFile", str(err), "-FlagPath", str(self.flag)])
        self.assertEqual(rc, 0)
        self.assertIn("decision=armed", out)
        self.assertIn("hits=15", out)
        self.assertTrue(self.flag.exists())
        self.assertIn("armed", self.flag.read_text(encoding="ascii"))

    def test_arm_threshold_boundary_arms(self):
        err = write_err(self.dir, 5)
        rc, out = run_gate(["-Verb", "Arm", "-ErrFile", str(err), "-FlagPath", str(self.flag)])
        self.assertEqual(rc, 0)
        self.assertIn("decision=armed", out)
        self.assertTrue(self.flag.exists())

    def test_arm_below_threshold_noarm(self):
        err = write_err(self.dir, 2)
        rc, out = run_gate(["-Verb", "Arm", "-ErrFile", str(err), "-FlagPath", str(self.flag)])
        self.assertEqual(rc, 0)
        self.assertIn("decision=noarm", out)
        self.assertFalse(self.flag.exists())

    def test_arm_missing_err_fail_open_noarm(self):
        rc, out = run_gate([
            "-Verb", "Arm", "-ErrFile", str(self.dir / "nope.err"),
            "-FlagPath", str(self.flag),
        ])
        self.assertEqual(rc, 0)
        self.assertIn("decision=noarm", out)
        self.assertFalse(self.flag.exists())

    # ---------- Gate ----------

    def _arm_flag(self, age_minutes=None):
        self.flag.write_text("20261018_000000 armed hits=15", encoding="ascii")
        if age_minutes is not None:
            past = time.time() - age_minutes * 60
            os.utime(self.flag, (past, past))

    def test_gate_no_flag_ignites_without_probe(self):
        rc, out = run_gate([
            "-Verb", "Gate", "-FlagPath", str(self.flag), "-ProbeExe", sys.executable,
        ])
        self.assertEqual(rc, 0)
        self.assertIn("decision=ignite", out)
        self.assertIn("reason=no-flag", out)
        # fast path must not even create the probe out dir
        self.assertFalse(self.outdir.exists())

    def test_gate_expired_flag_ignites_and_clears(self):
        self._arm_flag(age_minutes=120)
        rc, out = run_gate([
            "-Verb", "Gate", "-FlagPath", str(self.flag), "-ProbeExe", sys.executable,
            "-FlagMaxAgeMinutes", "90",
        ])
        self.assertEqual(rc, 0)
        self.assertIn("decision=ignite", out)
        self.assertIn("reason=flag-expired", out)
        self.assertFalse(self.flag.exists())

    def test_gate_probe_pass_disarms_silent(self):
        self._arm_flag()
        rc, out = run_gate([
            "-Verb", "Gate", "-FlagPath", str(self.flag),
            "-ProbeExe", sys.executable, "-ProbeArgs", '-c "pass"',
            "-WorkDir", str(self.dir), "-OutDir", str(self.outdir),
            "-LedgerFile", str(self.ledger),
        ])
        self.assertEqual(rc, 0)
        self.assertIn("decision=ignite", out)
        self.assertIn("reason=probe-pass", out)
        self.assertFalse(self.flag.exists())
        # a healthy backend must not add ledger noise
        self.assertFalse(self.ledger.exists())

    def test_gate_probe_fail_defers_keeps_flag_and_ledgers(self):
        self._arm_flag()
        rc, out = run_gate([
            "-Verb", "Gate", "-FlagPath", str(self.flag),
            "-ProbeExe", sys.executable, "-ProbeArgs", '-c "import sys; sys.exit(3)"',
            "-WorkDir", str(self.dir), "-OutDir", str(self.outdir),
            "-LedgerFile", str(self.ledger),
        ])
        self.assertEqual(rc, 0)
        self.assertIn("decision=defer", out)
        self.assertIn("reason=probe-fail", out)
        self.assertIn("exit=3", out)
        # defer keeps the flag armed for the next slot and writes the evidence
        self.assertTrue(self.flag.exists())
        self.assertTrue(self.ledger.exists())
        self.assertIn("API_STORM_DEFER", self.ledger.read_text(encoding="utf-8"))

    def test_gate_probe_timeout_defers_and_kills_tree(self):
        self._arm_flag()
        rc, out = run_gate([
            "-Verb", "Gate", "-FlagPath", str(self.flag),
            "-ProbeExe", sys.executable, "-ProbeArgs", '-c "import time; time.sleep(120)"',
            "-WorkDir", str(self.dir), "-OutDir", str(self.outdir),
            "-LedgerFile", str(self.ledger), "-ProbeTimeoutSec", "5",
        ])
        self.assertEqual(rc, 0)
        self.assertIn("decision=defer", out)
        self.assertIn("reason=probe-timeout", out)
        m = re.search(r"probe_pid=(\d+)", out)
        self.assertTrue(m, out)
        pid = int(m.group(1))
        # the force-killed probe must really be gone (no orphan retry burner).
        # tech#198 encoding-hole family: tasklist emits host-locale bytes
        # (GBK on zh-CN), and the suite runs python under -X utf8, so bare
        # text=True strict-decodes and kills the reader thread (stdout=None).
        # errors="replace" keeps the pid-digit assertion deterministic.
        time.sleep(1)
        check = subprocess.run(
            ["tasklist", "/FI", "PID eq %d" % pid],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        self.assertNotIn(str(pid), check.stdout)
        self.assertTrue(self.ledger.exists())

    def test_gate_missing_probe_exe_fail_open_ignites(self):
        self._arm_flag()
        rc, out = run_gate([
            "-Verb", "Gate", "-FlagPath", str(self.flag),
            "-ProbeExe", str(self.dir / "no-such-probe.exe"),
            "-OutDir", str(self.outdir), "-LedgerFile", str(self.ledger),
        ])
        self.assertEqual(rc, 0)
        self.assertIn("decision=ignite", out)
        self.assertIn("fail-open", out)
        # flag kept: next slot retries the probe
        self.assertTrue(self.flag.exists())


if __name__ == "__main__":
    unittest.main()
