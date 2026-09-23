"""Unit tests for the weekly report generator (src/weekly_report.py).

Fixture ledgers live in tests/fixtures/report/ - Chinese data files per
the encoding rule; this script stays pure ASCII. Real ledgers are only
read (one git smoke test, one CLI run into a temp dir) and never
written.

Run:
    python tests/test_weekly_report.py
"""
import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import weekly_report as wr  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MANIFEST = json.loads((FIXTURES / "manifest.json").read_text(encoding="utf-8"))


class WeekBoundsTests(unittest.TestCase):
    def test_wednesday_anchor(self):
        monday, sunday, label = wr.week_bounds(date(2026, 9, 23))
        self.assertEqual(monday, date(2026, 9, 21))
        self.assertEqual(sunday, date(2026, 9, 27))
        self.assertEqual(label, "2026-W39")

    def test_year_boundary_anchor(self):
        monday, _, label = wr.week_bounds(date(2026, 1, 1))
        self.assertEqual(monday, date(2025, 12, 29))
        self.assertEqual(label, "2026-W01")

    def test_sunday_anchor(self):
        monday, sunday, label = wr.week_bounds(date(2026, 9, 27))
        self.assertEqual((monday, sunday), (date(2026, 9, 21), date(2026, 9, 27)))
        self.assertEqual(label, "2026-W39")


class ParserTests(unittest.TestCase):
    def setUp(self):
        self.monday, self.sunday = date(2026, 9, 21), date(2026, 9, 27)
        self.state_path = FIXTURES / MANIFEST["report_state_ok"]
        self.backlog_path = FIXTURES / MANIFEST["report_backlog_ok"]
        self.orders_dir = FIXTURES / "report" / "orders"

    def test_state_window_rounds_idle_other(self):
        st = wr.parse_state(self.state_path, self.monday, self.sunday)
        self.assertEqual(st["tick"], 5)
        self.assertEqual(st["rounds"], 3)
        self.assertEqual(st["idle"], 1)
        self.assertEqual(st["other"], 1)
        self.assertEqual(len(st["lines"]), 4)
        self.assertTrue(any("R4" in ln for ln in st["lines"]))

    def test_backlog_burn_down(self):
        done_lines, open_lines = wr.parse_backlog(self.backlog_path, self.monday, self.sunday)
        self.assertEqual(len(done_lines), 1)
        self.assertIn("#1", done_lines[0])
        self.assertIn("fixture done this week", done_lines[0])
        self.assertEqual(len(open_lines), 2)
        self.assertIn("#2", open_lines[0])
        self.assertIn("#3", open_lines[1])

    def test_orders_window_and_ignores(self):
        names = wr.parse_orders(self.orders_dir, self.monday, self.sunday)
        self.assertEqual(names, ["O-20260923-0900-bm-a.md", "O-20260926-1800-bm-a.md"])
        week38 = wr.parse_orders(self.orders_dir, date(2026, 9, 14), date(2026, 9, 20))
        self.assertEqual(week38, ["O-20260916-0900-bm-a.md"])
        empty = wr.parse_orders(self.orders_dir, date(2026, 9, 7), date(2026, 9, 13))
        self.assertEqual(empty, [])

    def test_template_has_all_placeholders(self):
        text = wr.TEMPLATE.read_text(encoding="utf-8")
        for ph in wr.PLACEHOLDERS:
            self.assertIn("{%s}" % ph, text, "missing placeholder %s" % ph)

    def test_build_report_full(self):
        st = wr.parse_state(self.state_path, self.monday, self.sunday)
        done_lines, open_lines = wr.parse_backlog(self.backlog_path, self.monday, self.sunday)
        names = wr.parse_orders(self.orders_dir, self.monday, self.sunday)
        template = wr.TEMPLATE.read_text(encoding="utf-8")
        text = wr.build_report(template, "2026-W39", self.monday, self.sunday, st,
                               [("abc1234", "2026-09-23 10:00", "fixture commit")],
                               done_lines, open_lines, names, "2026-09-23 18:30")
        self.assertIn("2026-W39", text)
        self.assertIn("- abc1234 2026-09-23 10:00 fixture commit", text)
        self.assertIn("- O-20260923-0900-bm-a.md", text)
        for ph in wr.PLACEHOLDERS:
            self.assertNotIn("{%s}" % ph, text, "unfilled placeholder %s" % ph)

    def test_build_report_empty_sections(self):
        st = {"tick": 0, "lines": [], "rounds": 0, "idle": 0, "other": 0}
        template = wr.TEMPLATE.read_text(encoding="utf-8")
        text = wr.build_report(template, "2026-W39", self.monday, self.sunday, st,
                               [], [], [], [], "2026-09-23 18:30")
        self.assertIn("\n-\n", text.replace("\r\n", "\n"))


class GitSmokeTests(unittest.TestCase):
    def test_real_repo_window_has_commits(self):
        rows = wr.commits_in_window(REPO, date(2026, 9, 21), date(2026, 9, 27))
        self.assertGreaterEqual(len(rows), 1)
        h, when, subject = rows[0]
        self.assertRegex(h, r"^[0-9a-f]{7,}$")
        self.assertRegex(when, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")
        self.assertTrue(subject)


class CliTests(unittest.TestCase):
    def test_cli_writes_report_to_out_dir(self):
        out = Path(tempfile.mkdtemp(prefix="bs-report-"))
        self.addCleanup(shutil.rmtree, out, ignore_errors=True)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = wr.main(["weekly_report", "2026-09-23", str(out)])
        self.assertEqual(rc, 0)
        p = out / "weekly-2026-W39.md"
        self.assertTrue(p.is_file())
        text = p.read_text(encoding="utf-8")
        self.assertIn("BigStream", text)
        self.assertIn("2026-W39", text)
        for ph in wr.PLACEHOLDERS:
            self.assertNotIn("{%s}" % ph, text)

    def test_cli_bad_date_exit_two(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = wr.main(["weekly_report", "not-a-date"])
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
