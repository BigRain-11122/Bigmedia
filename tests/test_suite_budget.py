"""Unit tests for src/os/suite_budget.py (tech#168 suite budget line).

tech#168 selection: (1) budget line via SUITE_SECONDS in the wrapper +
this classifier as the single threshold truth, (3) monitoring note for
the weekly report; (2) layered-suite re-open deferred behind the
FORCED-EVAL verdict. Boundaries are contract: 120.0s IS WARN, 180.0s IS
FORCED-EVAL (>= semantics), and garbage readings must raise, never
fabricate a verdict.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "os"))

import suite_budget as sb  # noqa: E402


class ClassifyTests(unittest.TestCase):
    def test_ok_below_warn_line(self):
        for v in (0, 1.5, 42.8, 119.9):
            self.assertEqual(sb.VERDICT_OK, sb.classify(v))

    def test_warn_at_and_above_line_until_forced(self):
        for v in (120.0, 120.1, 123.2, 150, 179.9):
            self.assertEqual(sb.VERDICT_WARN, sb.classify(v))

    def test_forced_eval_at_and_above_line(self):
        for v in (180.0, 180.01, 300, 99999):
            self.assertEqual(sb.VERDICT_FORCED_EVAL, sb.classify(v))

    def test_garbage_raises_never_fabricates(self):
        for bad in (-1, -0.001):
            with self.assertRaises(ValueError):
                sb.classify(bad)
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                sb.classify(bad)
        for bad in ("123", None, True, [120]):
            with self.assertRaises(TypeError):
                sb.classify(bad)

    def test_threshold_constants_are_contract(self):
        self.assertEqual(120.0, sb.BUDGET_WARN_S)
        self.assertEqual(180.0, sb.BUDGET_FORCED_EVAL_S)


class ParseTests(unittest.TestCase):
    def test_ran_line_plural_and_singular(self):
        self.assertEqual(123.2, sb.seconds_from_ran("Ran 1385 tests in 123.2s"))
        self.assertEqual(0.005, sb.seconds_from_ran("Ran 1 test in 0.005s"))

    def test_ran_line_no_duration_is_none(self):
        self.assertIsNone(sb.seconds_from_ran("Ran 1385 tests"))
        self.assertIsNone(sb.seconds_from_ran(""))
        self.assertIsNone(sb.seconds_from_ran(None))

    def test_result_file_prefers_suite_seconds(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "r.result"
            p.write_text("SUITE_RC=0\nSUITE_RAN=Ran 5 tests in 99.9s\n"
                         "SUITE_SECONDS=123.4\nSUITE_RESULT=OK\n",
                         encoding="utf-8")
            self.assertEqual(123.4, sb.seconds_from_result_file(str(p)))

    def test_result_file_falls_back_to_ran_line(self):
        # pre-tech#168 result files carry the duration only inline
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "old.result"
            p.write_text("SUITE_RC=0\nSUITE_RAN=Ran 477 tests in 42.8s\n",
                         encoding="utf-8")
            self.assertEqual(42.8, sb.seconds_from_result_file(str(p)))

    def test_result_file_garbage_is_none_not_zero(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.result"
            p.write_text("SUITE_RC=0\nSUITE_SECONDS=abc\n", encoding="utf-8")
            self.assertIsNone(sb.seconds_from_result_file(str(p)))
            self.assertIsNone(sb.seconds_from_result_file(str(Path(td) / "absent.result")))


class VerdictLineTests(unittest.TestCase):
    def test_line_names_verdict_seconds_and_thresholds(self):
        line = sb.verdict_line(123.2)
        self.assertTrue(line.startswith("SUITE_BUDGET=WARN 123.2s"))
        self.assertIn("budget-line=WARN at 120s, FORCED-EVAL at 180s", line)
        self.assertIn("tech#168", line)

    def test_line_covers_all_verdicts(self):
        self.assertIn("SUITE_BUDGET=OK", sb.verdict_line(5.0))
        self.assertIn("SUITE_BUDGET=FORCED-EVAL", sb.verdict_line(205.0))


class CLITests(unittest.TestCase):
    def _run(self, *cli):
        return subprocess.run(
            [sys.executable, str(REPO / "src" / "os" / "suite_budget.py")] + list(cli),
            capture_output=True, text=True, timeout=60, cwd=str(REPO))

    def test_cli_seconds_direct(self):
        proc = self._run("--seconds", "130")
        self.assertEqual(0, proc.returncode)
        self.assertIn("SUITE_BUDGET=WARN", proc.stdout)
        self.assertIn("tech#168", proc.stdout)

    def test_cli_result_file_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "r.result"
            p.write_text("SUITE_SECONDS=185.0\n", encoding="utf-8")
            proc = self._run("--result", str(p))
        self.assertEqual(0, proc.returncode)
        self.assertIn("SUITE_BUDGET=FORCED-EVAL", proc.stdout)

    def test_cli_garbage_is_loud_rc2(self):
        proc = self._run("--seconds", "abc")
        self.assertEqual(2, proc.returncode)
        self.assertIn("SUITE_BUDGET-ERROR", proc.stdout)


if __name__ == "__main__":
    unittest.main()
