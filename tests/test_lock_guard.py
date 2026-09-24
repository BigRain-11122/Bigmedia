"""Unit tests for src/os/lock_guard.ps1 (D-20260925-03 single-instance lock).

Drives the real PowerShell engine against synthetic lock files in a temp
dir, so each case doubles as a live proof of the guard decision table:
  own=create-new | skip=pid-alive | skip=dead-pid-debounce |
  skip=legacy-lock-debounce | own=pid-dead-takeover |
  own=legacy-stale-takeover | own=hard-cap (pid-reuse suspicion)
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
GUARD = REPO / "src" / "os" / "lock_guard.ps1"
PS = "powershell.exe"


def run_guard(lock_path, takeover=30, hard_cap=40):
    cmd = [
        PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(GUARD),
        "-LockPath", str(lock_path),
        "-TakeoverMinMinutes", str(takeover),
        "-HardCapMinutes", str(hard_cap),
    ]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, timeout=60,
        encoding="utf-8", errors="replace",
    )
    return proc.returncode, proc.stdout.strip()


def spawn_alive_pid():
    proc = subprocess.Popen(
        ["ping", "-n", "60", "127.0.0.1"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return proc


def spawn_dead_pid():
    proc = subprocess.Popen(
        ["ping", "-n", "60", "127.0.0.1"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    proc.kill()
    proc.wait(timeout=10)
    return proc.pid


def write_lock(directory, content, age_minutes=None):
    lock = Path(directory) / "round.lock"
    lock.write_text(content, encoding="ascii")
    if age_minutes is not None:
        past = time.time() - age_minutes * 60
        os.utime(lock, (past, past))
    return lock


class TestLockGuard(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="bs-lock-guard-")
        self.addCleanup(self._tmp.cleanup)
        self.dir = self._tmp.name
        self.lock = Path(self.dir) / "round.lock"
        self._children = []
        self.addCleanup(self._reap)

    def _reap(self):
        for proc in self._children:
            if proc.poll() is None:
                proc.kill()

    def _alive_pid(self):
        proc = spawn_alive_pid()
        self._children.append(proc)
        return proc.pid

    # -- acquisition on empty slot --

    def test_own_when_no_lock(self):
        rc, out = run_guard(self.lock)
        self.assertEqual(rc, 0, out)
        self.assertRegex(out, r"^decision=own reason=create-new pid=\d+$")
        self.assertTrue(self.lock.exists())

    def test_lock_content_carries_pid_and_stamp(self):
        rc, out = run_guard(self.lock)
        self.assertEqual(rc, 0, out)
        body = self.lock.read_text(encoding="ascii").strip()
        self.assertRegex(body, r"^\d+ \d{8}_\d{6}$")  # "<pid> <stamp>"

    # -- holder alive: trust the probe --

    def test_skip_alive_pid(self):
        pid = self._alive_pid()
        write_lock(self.dir, f"{pid} 20260925_000000")
        rc, out = run_guard(self.lock)
        self.assertEqual(rc, 0, out)
        self.assertRegex(out, r"^decision=skip reason=pid-alive \(holder \d+ running\)")

    def test_takeover_alive_pid_past_hard_cap(self):
        # PID-reuse suspicion: probe says alive but lock is far past the cap.
        pid = self._alive_pid()
        write_lock(self.dir, f"{pid} 20260925_000000", age_minutes=45)
        rc, out = run_guard(self.lock)
        self.assertEqual(rc, 0, out)
        self.assertRegex(out, r"^decision=own reason=hard-cap .* suspect pid reuse")
        body = self.lock.read_text(encoding="ascii").strip()
        self.assertNotEqual(body.split()[0], str(pid))  # rewritten to new holder

    # -- holder dead: debounce floor before takeover --

    def test_skip_dead_pid_within_debounce_floor(self):
        pid = spawn_dead_pid()
        write_lock(self.dir, f"{pid} 20260925_000000")  # fresh age
        rc, out = run_guard(self.lock)
        self.assertEqual(rc, 0, out)
        self.assertRegex(out, r"^decision=skip reason=dead-pid-debounce \(holder \d+ gone\)")

    def test_takeover_dead_pid_after_floor(self):
        pid = spawn_dead_pid()
        write_lock(self.dir, f"{pid} 20260925_000000", age_minutes=35)
        rc, out = run_guard(self.lock)
        self.assertEqual(rc, 0, out)
        self.assertRegex(out, r"^decision=own reason=pid-dead-takeover \(holder \d+ gone\)")

    # -- legacy locks (old format: stamp only, no PID on record) --

    def test_skip_legacy_lock_within_floor(self):
        write_lock(self.dir, "20260924_120000")  # fresh age
        rc, out = run_guard(self.lock)
        self.assertEqual(rc, 0, out)
        self.assertRegex(out, r"^decision=skip reason=legacy-lock-debounce \(no pid on record\)")

    def test_takeover_legacy_lock_after_floor(self):
        write_lock(self.dir, "20260924_120000", age_minutes=35)
        rc, out = run_guard(self.lock)
        self.assertEqual(rc, 0, out)
        self.assertRegex(out, r"^decision=own reason=legacy-stale-takeover \(no pid on record\)")


if __name__ == "__main__":
    unittest.main()
