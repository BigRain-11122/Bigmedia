# -*- coding: utf-8 -*-
"""Unit tests for the local substitution rate report packer (src/os/local_rate_report.py).

backlog #57 prep (R1307): pure functions only — log-line parsing, weekly
aggregation, p4-ledger row parsing, and report rendering. Real state.json and
p4-ledger.md are never touched; fixtures only.

Run:
    python tests/test_local_rate_report.py
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "os"))

import local_rate_report as lrr  # noqa: E402


class TestParseRounds(unittest.TestCase):
    def test_first_match_per_line_wins(self):
        # a recap quoting an earlier round's metering must not double count
        line = (u"2026-10-05 02:5x R1305: production round ... tokens:local=1 "
                u"(S1 first-read) ... recap: earlier round said tokens:local=2")
        rounds = lrr.parse_rounds([line])
        self.assertEqual(1, len(rounds))
        self.assertEqual(1, rounds[0]["local"])
        self.assertEqual("R1305", rounds[0]["round"])
        self.assertEqual("2026-W41", rounds[0]["week"])

    def test_line_without_metering_is_skipped(self):
        self.assertEqual([], lrr.parse_rounds([u"2026-09-24 10:00 R100: no metering here"]))

    def test_cloud_entry_parsed_and_defaults_zero(self):
        with_cloud = lrr.parse_rounds([u"2026-09-25 01:00 R101: tokens:local=2 tokens:cloud=1"])
        without = lrr.parse_rounds([u"2026-09-25 01:00 R101: tokens:local=2"])
        self.assertEqual(1, with_cloud[0]["cloud"])
        self.assertEqual(0, without[0]["cloud"])


class TestAggregateWeeks(unittest.TestCase):
    def setUp(self):
        self.rounds = [
            {"date": "2026-09-24", "week": "2026-W38", "round": "R1", "local": 0, "cloud": 0},
            {"date": "2026-09-24", "week": "2026-W38", "round": "R2", "local": 2, "cloud": 0},
            {"date": "2026-10-05", "week": "2026-W41", "round": "R3", "local": 1, "cloud": 0},
            {"date": "2026-10-05", "week": "2026-W41", "round": "R4", "local": 0, "cloud": 0},
        ]

    def test_weekly_sums_and_rate(self):
        weeks = lrr.aggregate_weeks(self.rounds)
        self.assertEqual(2, weeks["2026-W38"]["l2"])
        self.assertEqual(2, weeks["2026-W38"]["rounds"])
        self.assertEqual(1, weeks["2026-W38"]["active_rounds"])
        self.assertAlmostEqual(1.0, weeks["2026-W38"]["rate"])
        self.assertEqual(1, weeks["2026-W41"]["l2"])
        self.assertEqual(2, weeks["2026-W41"]["rounds"])

    def test_rate_none_when_denominator_zero(self):
        weeks = lrr.aggregate_weeks([self.rounds[0]])
        self.assertIsNone(weeks["2026-W38"]["rate"])

    def test_last_date_tracks_latest_line(self):
        weeks = lrr.aggregate_weeks(self.rounds)
        self.assertEqual("2026-10-05", weeks["2026-W41"]["last_date"])


class TestP4Ledger(unittest.TestCase):
    def test_parses_data_rows_only(self):
        text = (
            u"# P4 ledger\n\n"
            u"| 时间 | 输入件 | 模型 | 摘要件 | 行数 | 引用 | 截断 | 时长 | 判定 |\n"
            u"|---|---|---|---|---|---|---|---|---|\n"
            u"| 2026-09-26 00:27 | R-a.md | qwen2.5:7b-instruct | a.digest-v1.md | 40 | 30 | no | 8s | PASS |\n"
            u"| 2026-09-26 00:29 | R-a.md | qwen2.5:14b | a.digest-v1.md | 36 | 17 | no | 21s | PASS |\n"
            u"| note row without table cells\n"
        )
        rows = lrr.parse_p4_ledger(text)
        self.assertEqual(2, len(rows))
        self.assertEqual("qwen2.5:14b", rows[1]["model"])
        self.assertEqual("PASS", rows[1]["verdict"])

    def test_header_row_excluded(self):
        text = (u"| 时间 | 输入件 | 模型 | 摘要件 | 行数 | 引用 | 截断 | 时长 | 判定 |\n"
                u"|---|---|---|---|---|---|---|---|---|\n")
        self.assertEqual([], lrr.parse_p4_ledger(text))


class TestRenderReport(unittest.TestCase):
    def test_renders_sections_and_boundary_notes(self):
        rounds = [
            {"date": "2026-10-05", "week": "2026-W41", "round": "R1307", "local": 1, "cloud": 0},
        ]
        weeks = lrr.aggregate_weeks(rounds)
        p4_rows = [{
            "time": u"2026-09-26 00:27", "input": u"R-a.md", "model": u"qwen2.5:7b-instruct",
            "digest": u"a.digest-v1.md", "lines": u"40", "refs": u"30",
            "truncated": u"no", "secs": u"8s", "verdict": u"PASS",
        }]
        text = lrr.render_report(rounds, weeks, p4_rows)
        self.assertIn(u"周轮汇表", text)
        self.assertIn(u"2026-W41", text)
        self.assertIn(u"本地处理 1 件", text)
        self.assertIn(u"云端省减 1 读取轮次", text)
        self.assertIn(u"P4 调研摘要台账独立面：1 行", text)
        for note in lrr.BOUNDARY_NOTES:
            self.assertIn(note, text)
        self.assertIn(u"刷新指令", text)

    def test_zero_cloud_face_rended_as_honest_L3(self):
        rounds = [{"date": "2026-10-05", "week": "2026-W41", "round": "R1", "local": 3, "cloud": 0}]
        weeks = lrr.aggregate_weeks(rounds)
        text = lrr.render_report(rounds, weeks, [])
        self.assertIn(u"生产推理面 L3=0", text)


if __name__ == "__main__":
    unittest.main()
