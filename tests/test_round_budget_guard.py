"""Unit tests for src/os/round_budget_guard.ps1 (tech#217 v2 liveness budget).

Drives the REAL PowerShell engine against real child processes in a temp
dir, so each case doubles as a live proof of the evidence-kill contract
ported from the BigMoney canonical v2 (945c3f60, 2026-10-18 root-cure):

  budget=finished      a streaming round that runs LONGER than the silence
                       window is never killed - activity resets the clock
                       (the retired 25-min wall-clock guillotine killed
                       exactly these rounds; that is the dead-window bug)
  budget=silence-kill  a silent hang is tree-killed at the silence gate
  budget=hard-cap-kill a round that streams FOREVER is killed ONLY at the
                       hard cap - never by the silence gate
  tree sweep           the kill takes the grandchildren down too
  immediate exit       a body that dies before the first poll = finished

Plus wiring/vocabulary regression locks: the launcher must carry the v2
param faces, the retired wall-clock log line must stay retired, the task
definition must hold a cap above the script cap, loop_health bounds must
ride the v2 budget, and the classify() bucket must keep counting the new
"round killed (...)" beats (and the historical timeout face) as kills.
"""
import re
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GUARD = REPO / "src" / "os" / "round_budget_guard.ps1"
LAUNCHER = REPO / "src" / "os" / "iteration_loop.ps1"
REGISTER = REPO / "src" / "os" / "register_loop_task.ps1"
PS = "powershell.exe"


def run_guard(proc_id, out_file, err_file, silence_min, hard_cap_min,
              poll_ms=500, timeout_s=90):
    cmd = [
        PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(GUARD),
        "-ProcId", str(proc_id), "-OutFile", str(out_file),
        "-ErrFile", str(err_file),
        "-SilenceMinutes", str(silence_min),
        "-HardCapMinutes", str(hard_cap_min),
        "-PollMillis", str(poll_ms),
    ]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout_s,
        encoding="utf-8", errors="replace",
    )
    return proc.returncode, proc.stdout.strip()


def pid_alive(pid):
    out = subprocess.run(
        ["tasklist", "/FI", "PID eq %d" % pid],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=30,
    ).stdout
    return str(pid) in out and "No tasks" not in out


class TestRoundBudgetGuard(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="bs-budget-guard-")
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)
        self.out = self.dir / "round.out"
        self.err = self.dir / "round.err"
        self._children = []
        self._files = []
        self.addCleanup(self._reap)

    def _reap(self):
        for proc in self._children:
            if proc.poll() is None:
                proc.kill()
                try:
                    proc.wait(timeout=10)
                except Exception:
                    pass
        for fh in self._files:
            try:
                fh.close()
            except Exception:
                pass

    def _spawn(self, cmd):
        out = open(self.out, "wb")
        err = open(self.err, "wb")
        self._files.extend([out, err])
        proc = subprocess.Popen(cmd, stdout=out, stderr=err)
        self._children.append(proc)
        return proc

    def test_silence_kill_hang_is_tree_killed(self):
        # A truly silent hang: no output bytes at all. The silence gate
        # (25 min in production; 6 s here) is the ONLY wall-clock-ish kill
        # left in the fleet, and it demands evidence: zero output.
        proc = self._spawn([PS, "-NoProfile", "-Command",
                            "Start-Sleep -Seconds 120"])
        rc, verdict = run_guard(proc.pid, self.out, self.err,
                                silence_min=0.1, hard_cap_min=5)
        self.assertTrue(verdict.startswith("budget=silence-kill"), verdict)
        self.assertEqual(rc, 3)
        # child is dead and stays dead
        deadline = time.time() + 10
        while proc.poll() is None and time.time() < deadline:
            time.sleep(0.2)
        self.assertIsNotNone(proc.poll())

    def test_streaming_round_survives_past_silence_window(self):
        # The dead-window regression lock: a round that keeps producing
        # output LONGER than the silence window (20 x 300ms = 6 s vs a
        # 4.8 s window) must FINISH ON ITS OWN. The retired v1 wall clock
        # killed exactly this class of round at 25 min mid-flight.
        # Activity source = direct appends to the watched out-file
        # (deterministic growth; the production face is codely's own
        # stdout streaming, covered live by every real round).
        cmd = ("1..20 | ForEach-Object { Add-Content -LiteralPath '%s' "
               "-Value ('tick' + $_); Start-Sleep -Milliseconds 300 }"
               % str(self.out))
        proc = subprocess.Popen([PS, "-NoProfile", "-Command", cmd],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
        self._children.append(proc)
        rc, verdict = run_guard(proc.pid, self.out, self.err,
                                silence_min=0.08, hard_cap_min=5)
        self.assertEqual(verdict, "budget=finished")
        self.assertEqual(rc, 0)
        self.assertEqual(proc.wait(timeout=30), 0)
        self.assertGreater(self.out.stat().st_size, 0)

    def test_hard_cap_kill_never_triggered_by_silence(self):
        # A round that streams FOREVER is never silence-killed: the only
        # thing that stops it is the hard cap (240 min in production;
        # ~7 s here). This is the discrimination proof that continuous
        # output resets the silence clock every poll.
        cmd = ("for($i=0;$i -lt 200;$i++){ Add-Content -LiteralPath '%s' "
               "-Value ('tick' + $i); Start-Sleep -Milliseconds 300 }"
               % str(self.out))
        proc = subprocess.Popen([PS, "-NoProfile", "-Command", cmd],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
        self._children.append(proc)
        rc, verdict = run_guard(proc.pid, self.out, self.err,
                                silence_min=0.05, hard_cap_min=0.12)
        self.assertTrue(verdict.startswith("budget=hard-cap-kill"), verdict)
        self.assertEqual(rc, 4)
        deadline = time.time() + 10
        while proc.poll() is None and time.time() < deadline:
            time.sleep(0.2)
        self.assertIsNotNone(proc.poll())
        # activity really flowed across the whole run
        self.assertGreater(self.out.stat().st_size, 0)

    def test_tree_kill_sweeps_grandchild(self):
        # The evidence kill takes the process TREE down: the body spawns
        # a grandchild, then hangs silently -> both die with the body.
        gc_file = self.dir / "gc.pid"
        cmd = ("$gc = Start-Process powershell -ArgumentList "
               "'-NoProfile','-Command','Start-Sleep -Seconds 120' "
               "-WindowStyle Hidden -PassThru; "
               "Add-Content -LiteralPath '%s' -Value $gc.Id; "
               "Start-Sleep -Seconds 120" % str(gc_file))
        proc = self._spawn([PS, "-NoProfile", "-Command", cmd])
        deadline = time.time() + 10
        while not gc_file.exists() and time.time() < deadline:
            time.sleep(0.2)
        self.assertTrue(gc_file.exists(), "grandchild pid file never appeared")
        gc_pid = int(gc_file.read_text().strip())
        self.assertTrue(pid_alive(gc_pid))
        rc, verdict = run_guard(proc.pid, self.out, self.err,
                                silence_min=0.08, hard_cap_min=5)
        self.assertTrue(verdict.startswith("budget=silence-kill"), verdict)
        self.assertEqual(rc, 3)
        deadline = time.time() + 10
        while pid_alive(gc_pid) and time.time() < deadline:
            time.sleep(0.2)
        self.assertFalse(pid_alive(gc_pid), "grandchild survived the tree kill")

    def test_immediate_exit_is_finished(self):
        # Body dies before the first poll: guard must report finished,
        # never misfire a kill on a PID it never saw alive.
        proc = self._spawn([PS, "-NoProfile", "-Command", "exit 7"])
        proc.wait(timeout=30)
        rc, verdict = run_guard(proc.pid, self.out, self.err,
                                silence_min=0.05, hard_cap_min=5,
                                poll_ms=300)
        self.assertEqual(verdict, "budget=finished")
        self.assertEqual(rc, 0)


class TestV2WiringLocks(unittest.TestCase):
    """tech#217 regression locks: the v2 faces must stay wired."""

    def test_launcher_params_and_wiring(self):
        s = LAUNCHER.read_text(encoding="ascii")
        self.assertIn("[int]$RoundTimeoutMinutes = 240", s)
        self.assertIn("[int]$RoundSilenceMinutes = 25", s)
        self.assertIn("[int]$LockMaxAgeMinutes = 0", s)  # auto = 1.2 x cap
        self.assertIn("round_budget_guard.ps1", s)
        self.assertIn("budget=finished", s)
        # the retired 25-min guillotine log line must never come back
        self.assertNotIn("ROUND TIMEOUT after", s)

    def test_register_task_cap_above_script_cap(self):
        s = REGISTER.read_text(encoding="ascii")
        self.assertIn("(New-TimeSpan -Minutes 250)", s)
        self.assertNotIn("(New-TimeSpan -Minutes 35)", s)

    def test_loop_health_bounds_ride_v2_budget(self):
        sys.path.insert(0, str(REPO / "src" / "os"))
        try:
            import loop_health
        finally:
            sys.path.pop(0)
        self.assertEqual(loop_health.LOCK_AGE_MIN, 288)

    def test_classify_counts_v2_kill_beats(self):
        sys.path.insert(0, str(REPO / "src" / "os"))
        try:
            import loop_health
        finally:
            sys.path.pop(0)
        beats = [
            ("2026-10-18 12:00:00", "round done exit=0"),
            ("2026-10-18 12:10:00",
             "round killed (budget=silence-kill silent=25min total=26min)"),
            ("2026-10-18 12:40:00", "round hard-cap killed (backstop, age over 240min)"),
            ("2026-10-18 13:00:00", "round timeout killed (age over 25min)"),
            ("2026-10-18 13:05:00", "skip (round in flight)"),
        ]
        done, skip_n, timeout_n, error_n = loop_health.classify(
            [(ts, msg) for ts, msg in beats])
        self.assertEqual([d[1] for d in done], ["round done exit=0"])
        self.assertEqual(skip_n, 1)
        self.assertEqual(timeout_n, 3)  # v2 kills + historical timeout face
        self.assertEqual(error_n, 0)


if __name__ == "__main__":
    unittest.main()
