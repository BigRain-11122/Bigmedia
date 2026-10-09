"""Unit tests for tools/run_suite.ps1 (tech#33: true suite exit-code capture).

Root defect (R1839): piping `python -m unittest ... 2>&1` through PS 5.1
cmdlets wraps native stderr in ErrorRecords and can surface a pseudo-rc to
the caller (a green suite read as red). The wrapper must always report and
propagate the real python exit code, capture both streams to files, and emit
machine-readable SUITE_* summary lines.

tech#35 (R1841): PS 5.1 Start-Process -Redirect* artifacts can carry NUL
padding -- raw consumer reads hit binary rejection (R1840 double evidence).
The <Log>.result file written by the wrapper itself is the canonical consumer
surface: exact-length UTF-8 (no BOM), zero NUL bytes, rc/summary truth intact.
"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WRAPPER = REPO / "tools" / "run_suite.ps1"
PS = "powershell.exe"


def run_wrapper(module=None, log=None, result_file=None, timeout=300):
    cmd = [PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(WRAPPER)]
    if module:
        cmd += ["-Module", module]
    if log:
        cmd += ["-Log", log]
    if result_file:
        cmd += ["-ResultFile", result_file]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout,
        encoding="utf-8", errors="replace", cwd=str(REPO),
    )
    return proc.returncode, proc.stdout


def _read_raw(path):
    with open(path, "rb") as f:
        return f.read()


class RunSuiteWrapperTests(unittest.TestCase):
    def test_green_module_rc_zero_and_summary(self):
        # isolated -Log: never touch the shared default log path (a
        # concurrent wrapper run, e.g. a live full-suite validation, would
        # be clobbered by the stale-log guard - R1840 operational red)
        with tempfile.TemporaryDirectory() as td:
            rc, out = run_wrapper(module="tests.test_board_check",
                                  log=os.path.join(td, "green.log"))
        self.assertEqual(0, rc)
        self.assertIn("SUITE_RC=0", out)
        self.assertRegex(out, r"SUITE_RAN=Ran \d+ tests?")
        self.assertRegex(out, r"SUITE_RESULT=OK")

    def test_failing_module_propagates_nonzero_rc(self):
        with tempfile.TemporaryDirectory() as td:
            rc, out = run_wrapper(module="tests.test_definitely_missing_module_xyz",
                                  log=os.path.join(td, "fail.log"))
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

    def test_result_file_canonical_nul_free(self):
        # tech#35 core: the <Log>.result file is the canonical consumer
        # surface -- written by the wrapper itself, so it must be exact-length
        # UTF-8 without BOM and carry zero NUL bytes (the consumer never
        # filters), with rc/ran/result truth intact.
        with tempfile.TemporaryDirectory() as td:
            log = os.path.join(td, "res.log")
            rc, out = run_wrapper(module="tests.test_board_check", log=log)
            self.assertEqual(0, rc)
            rpath = log + ".result"
            self.assertTrue(os.path.exists(rpath))
            raw = _read_raw(rpath)
            self.assertNotIn(b"\x00", raw)                       # zero NUL burden
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))    # no BOM
            txt = raw.decode("utf-8")
            self.assertIn("SUITE_RC=0", txt)
            self.assertRegex(txt, r"SUITE_RAN=Ran \d+ tests?")
            self.assertRegex(txt, r"SUITE_RESULT=OK")
            # stdout advertises the canonical surface
            self.assertIn("SUITE_RESULT_FILE=", out)

    def test_result_file_custom_path_honored(self):
        with tempfile.TemporaryDirectory() as td:
            rpath = os.path.join(td, "custom.result")
            rc, out = run_wrapper(module="tests.test_board_check",
                                  log=os.path.join(td, "l.log"),
                                  result_file=rpath)
            self.assertEqual(0, rc)
            self.assertTrue(os.path.exists(rpath))
            txt = _read_raw(rpath).decode("utf-8")
            self.assertIn("SUITE_RC=0", txt)
            self.assertIn("SUITE_RESULT_FILE=" + rpath, txt)

    def test_result_file_reflects_failure_rc(self):
        # the canonical file must carry the real (nonzero) rc on failure too
        with tempfile.TemporaryDirectory() as td:
            log = os.path.join(td, "failres.log")
            rc, out = run_wrapper(module="tests.test_definitely_missing_module_xyz",
                                  log=log)
            self.assertNotEqual(0, rc)
            txt = _read_raw(log + ".result").decode("utf-8")
            lines = [l for l in txt.splitlines() if l.startswith("SUITE_RC=")]
            self.assertEqual(1, len(lines))
            self.assertNotEqual("SUITE_RC=0", lines[0])

    def test_stale_result_file_truncated_not_appended(self):
        # a stale result file (e.g. with old rc and NUL padding) must be
        # fully replaced, never appended to or half-read as this run's truth
        with tempfile.TemporaryDirectory() as td:
            log = os.path.join(td, "stale-res.log")
            rpath = log + ".result"
            with open(rpath, "wb") as f:
                f.write(b"SUITE_RC=999\x00STALE-NUL-PAD")
            rc, out = run_wrapper(module="tests.test_board_check", log=log)
            self.assertEqual(0, rc)
            raw = _read_raw(rpath)
            self.assertNotIn(b"STALE-NUL-PAD", raw)
            self.assertNotIn(b"SUITE_RC=999", raw)
            self.assertNotIn(b"\x00", raw)
            self.assertIn(b"SUITE_RC=0", raw)


if __name__ == "__main__":
    unittest.main()
