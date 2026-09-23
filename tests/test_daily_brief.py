# -*- coding: utf-8 -*-
"""Unit tests for the intel daily-brief collector (src/intel/).

O-20260923-2304-bm-a: parsers are pure functions (no network), Chinese
payloads appear as plain dict fixtures (data lives in fixtures, source
stays ASCII per encoding rule).

Run:
    python tests/test_daily_brief.py
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "intel"))

import daily_brief as db  # noqa: E402


BILI_FIXTURE = {
    "code": 0,
    "data": {"list": [
        {"title": "\u7eff\u7ea2\u8272\u6807\u9898\u4e00",
         "owner": {"name": "UP\u4e3bA"}},
        {"title": "", "owner": {"name": "no-title"}},
        {"title": "\u6807\u9898\u4e8c", "owner": {}},
    ]},
}

ZHIHU_FIXTURE = {
    "data": [
        {"target": {"title": "\u95ee\u9898\u4e00"}, "detail_text": "1234 \u4e07\u70ed\u5ea6"},
        {"target": {}, "detail_text": "no-target"},
        {"target": {"title": "   "}, "detail_text": "blank-title"},
    ]
}


class TestParsers(unittest.TestCase):
    def test_bilibili_parse_skips_empty_titles(self):
        rows = db.parse_bilibili(BILI_FIXTURE)
        self.assertEqual(2, len(rows))
        self.assertEqual("\u7eff\u7ea2\u8272\u6807\u9898\u4e00", rows[0][0])
        self.assertEqual("UP\u4e3bA", rows[0][1])
        self.assertEqual("\u6807\u9898\u4e8c", rows[1][0])

    def test_bilibili_parse_tolerates_none(self):
        self.assertEqual([], db.parse_bilibili(None))
        self.assertEqual([], db.parse_bilibili({}))

    def test_zhihu_parse_skips_blank_titles(self):
        rows = db.parse_zhihu(ZHIHU_FIXTURE)
        self.assertEqual(1, len(rows))
        self.assertEqual("\u95ee\u9898\u4e00", rows[0][0])
        self.assertEqual("1234 \u4e07\u70ed\u5ea6", rows[0][1])

    def test_zhihu_parse_tolerates_none(self):
        self.assertEqual([], db.parse_zhihu(None))


class TestRender(unittest.TestCase):
    def test_brief_has_ok_and_honest_fail_sections(self):
        result = {
            "ok": {"zhihu-hot": [("\u9898", "\u70ed")],
                   "bilibili-popular": []},
            "fail": {"bilibili-popular": "empty list"},
        }
        text = db.render_brief("2026-09-23", result)
        self.assertIn("2026-09-23", text)
        self.assertIn("zhihu-hot", text)
        self.assertIn("\u9898", text)
        self.assertIn("\u901a\u9053\u5361\u70b9", text)  # channel blockers
        self.assertIn("empty list", text)

    def test_brief_all_ok_marks_channels_clean(self):
        result = {"ok": {"zhihu-hot": [("\u9898", "")],
                         "bilibili-popular": [("\u98982", "")]},
                  "fail": {}}
        text = db.render_brief("2026-09-23", result)
        self.assertNotIn("\u901a\u9053\u5361\u70b9", text)
        self.assertIn("\u53cc\u6e90\u5168\u901a", text)  # both channels clean


if __name__ == "__main__":
    unittest.main(verbosity=2)
