# -*- coding: utf-8 -*-
"""Unit tests for the platform spec gate (src/platform_spec_check.py).

O-20260923-2210 continuation: "duration measured" is a mass-production
red line that had no tool (v5 60.58s and v10 64.06s both slipped past
the 60s ceiling - caught only by manual notes). Pure functions only:
playbook parsing, aspect mapping, verdict logic. No ffprobe, real
playbook never touched. Chinese appears as \\uXXXX escapes (ASCII rule).

Run:
    python tests/test_platform_spec.py
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import platform_spec_check as psc  # noqa: E402


PLAYBOOK_FIXTURE = "\n".join([
    "# fixture",
    "",
    "| \u5e73\u53f0 | \u4e3b\u5f62\u6001 | \u753b\u5e45/\u65f6\u957f | \u53d1\u5e03\u901a\u9053\u73b0\u5b9e | \u51b7\u542f\u5b9a\u4f4d |",
    "|---|---|---|---|---|",
    "| \u5fae\u4fe1\u89c6\u9891\u53f7 | \u77ed\u89c6\u9891 | 9:16 \u00b7 30-60s | \u65e0\u516c\u5f00 API | \u79c1\u57df\u5165\u53e3 |",
    "| \u6296\u97f3 | \u77ed\u89c6\u9891 | 9:16 \u00b7 15-60s | \u65e0\u516c\u5f00 API | \u6d41\u91cf\u6c60 |",
    "| B\u7ad9 | \u4e2d\u957f\u89c6\u9891 | 16:9 \u00b7 3-15min | \u65e0\u516c\u5f00 API | \u77e5\u8bc6\u533a |",
    "| YouTube | \u4e2d\u957f+Shorts | 16:9 / 9:16 | API \u53ef\u7528 | \u6d77\u5916 |",
    "| \u5fae\u4fe1\u516c\u4f17\u53f7 | \u56fe\u6587/\u957f\u6587 | \u7ad6\u7248\u56fe\u6587 | \u8349\u7a3f API | \u6df1\u5ea6\u6c89\u6dc0 |",
])


class TestParsePlaybook(unittest.TestCase):
    def setUp(self):
        self.specs = psc.parse_playbook(PLAYBOOK_FIXTURE)

    def test_video_platforms_parsed_with_ranges(self):
        self.assertEqual(("9", "16"), tuple(
            self.specs["\u5fae\u4fe1\u89c6\u9891\u53f7"]["aspects"][0].split(":")))
        self.assertEqual((30, 60), self.specs["\u5fae\u4fe1\u89c6\u9891\u53f7"]["dur_s"])
        self.assertEqual((15, 60), self.specs["\u6296\u97f3"]["dur_s"])
        # 3-15min translates to seconds
        self.assertEqual((180, 900), self.specs["B\u7ad9"]["dur_s"])

    def test_multi_aspect_platform(self):
        self.assertEqual(["16:9", "9:16"],
                         self.specs["YouTube"]["aspects"])
        self.assertIsNone(self.specs["YouTube"]["dur_s"])

    def test_non_video_rows_skipped(self):
        # image/article platforms carry no N:N aspect -> not in specs
        self.assertNotIn("\u5fae\u4fe1\u516c\u4f17\u53f7", self.specs)


class TestAspectName(unittest.TestCase):
    def test_known_aspect_map(self):
        self.assertEqual("9:16", psc.aspect_name(1080, 1920))
        self.assertEqual("16:9", psc.aspect_name(1920, 1080))
        self.assertEqual("3:4", psc.aspect_name(1080, 1440))

    def test_unknown_aspect_returns_none(self):
        self.assertIsNone(psc.aspect_name(100, 200))
        self.assertIsNone(psc.aspect_name(0, 0))


class TestCheck(unittest.TestCase):
    def setUp(self):
        self.spec = {"aspects": ["9:16"], "dur_s": (30, 60)}

    def test_pass_inside_window(self):
        f = psc.check(self.spec, 1080, 1920, 59.93)
        self.assertFalse([x for x in f if x[0] == "FAIL"])

    def test_duration_fail_over_ceiling(self):
        # the v10 incident shape: 64.06s vs the 60s ceiling
        f = psc.check(self.spec, 1080, 1920, 64.06)
        self.assertIn("duration", [x[1] for x in f if x[0] == "FAIL"])

    def test_duration_fail_under_floor(self):
        f = psc.check(self.spec, 1080, 1920, 12.0)
        self.assertIn("duration", [x[1] for x in f if x[0] == "FAIL"])

    def test_aspect_fail(self):
        f = psc.check(self.spec, 1920, 1080, 45.0)
        self.assertIn("aspect", [x[1] for x in f if x[0] == "FAIL"])

    def test_no_range_is_info_not_fail(self):
        spec = {"aspects": ["16:9", "9:16"], "dur_s": None}
        f = psc.check(spec, 1080, 1920, 64.06)
        self.assertFalse([x for x in f if x[0] == "FAIL"])
        self.assertIn("INFO", [x[0] for x in f])


if __name__ == "__main__":
    unittest.main(verbosity=2)
