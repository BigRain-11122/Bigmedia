"""Unit tests for tools/run_suite.ps1 (tech#33: true suite exit-code capture).

Root defect (R1839): piping `python -m unittest ... 2>&1` through PS 5.1
cmdlets wraps native stderr in ErrorRecords and can surface a pseudo-rc to
the caller (a green suite read as red). The wrapper must always report and
propagate the real python exit code, capture both streams to files, and emit
machine-readable SUITE_* summary lines.
"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WRAPPER = REPO / "tools" / "run_suite.ps1"
PS = "powershell.exe"


def run_wrapper(module=None, log=None, timeout=300):
    cmd = [PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(WRAPPER)]
    if module:
        cmd += ["-Module", module]
    if log:
        cmd += ["-Log", log]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout,
        encoding="utf-8", errors="replace", cwd=str(REPO),
    )
    return proc.returncode, proc.stdout


class RunSuiteWrapperTests(unittest.TestCase):
    def test_green_module_rc_zero_and_summary(self):
        rc, out = run_wrapper(module="tests.test_board_check")
        self.assertEqual(0, rc)
        self.assertIn("SUITE_RC=0", out)
        self.assertRegex(out, r"SUITE_RAN=Ran \d+ tests?")
        self.assertRegex(out, r"SUITE_RESULT=OK")

    def test_failing_module_propagates_nonzero_rc(self):
        rc, out = run_wrapper(module="tests.test_definitely_missing_module_xyz")
        self.assertNotEqual(0, rc)
        # the real python rc is surfaced, not a pipeline pseudo-rc
        m = [line for line in out.splitlines() if line.startswith("SUITE_RC=")]
        self.assertEqual(1, len(m))
        self.assertNotEqual("SUITE_RC=0", m[0])
        # stderr captured to a log file for the human reader
        self.assertRegex(out, r"SUITE_LOG_ERR=")

    def test_custom_log_path_honored(self):
        with tempfile.TemporaryDirectory() as td:
            log = os.path.join(td, "custom.log")
            rc, out = run_wrapper(module="tests.test_board_check", log=log)
            self.assertEqual(0, rc)
            self.assertTrue(os.path.exists(log + ".out"))
            self.assertTrue(os.path.exists(log + ".err"))

    def test_stale_log_not_contaminated_into_new_run(self):
        # Start-Process redirect opens without truncating: a stale summary
        # left in the log must never be readable as this run's result.
        with tempfile.TemporaryDirectory() as td:
            log = os.path.join(td, "stale.log")
            with open(log + ".err", "w", encoding="utf-8") as f:
                f.write("Ran 999 tests in 9.9s\n\nOK\nSTALE-MARKER\n")
            rc, out = run_wrapper(module="tests.test_board_check", log=log)
            self.assertEqual(0, rc)
            with open(log + ".err", encoding="utf-8", errors="replace") as f:
                err_txt = f.read()
            self.assertNotIn("STALE-MARKER", err_txt)
            self.assertNotIn("Ran 999 tests", err_txt)
            self.assertRegex(err_txt, r"Ran \d+ tests?")


if __name__ == "__main__":
    unittest.main()
