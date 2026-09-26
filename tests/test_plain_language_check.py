# -*- coding: utf-8 -*-
"""Tests for plain_language_check (copy-craft section 2.8 machine gate)."""
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

import plain_language_check as plc  # noqa: E402


class LoadTermsTests(unittest.TestCase):
    def test_terms_file_loads_nonempty(self):
        terms = plc.load_terms()
        self.assertGreaterEqual(len(terms), 12)
        self.assertIn("GATE", terms)

    def test_comments_and_blanks_skipped(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as f:
            f.write("# comment\n\nalpha\nbeta\n")
            path = f.name
        self.assertEqual(plc.load_terms(path), ["alpha", "beta"])


class TitleTests(unittest.TestCase):
    def setUp(self):
        self.terms = ["回测", "GATE", "夏普"]

    def test_title_jargon_is_fail(self):
        f = plc.check_title("回测证书拿到了", self.terms)
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0][0], "FAIL")
        self.assertEqual(f[0][1], "jargon-title")

    def test_title_clean_passes(self):
        self.assertEqual(plc.check_title("一张证书的故事", self.terms), [])


class TextTests(unittest.TestCase):
    def setUp(self):
        self.terms = ["台账"]

    def test_jargon_term_listed_with_first_line(self):
        f = plc.check_text("第一行干净。\n这是台账的第二次提及。", self.terms, "x")
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0][0], "WARN")
        self.assertIn("L2", f[0][2])

    def test_clean_text_no_jargon(self):
        self.assertEqual(plc.check_text("今天讲一个故事。", self.terms, "x"), [])

    def test_long_sentence_by_chars_warns(self):
        long_line = "这是一个超过四十个字符的句子" * 4 + "。"
        f = plc.check_text(long_line, [], "x")
        self.assertTrue(any(x[1] == "longsentence" for x in f))

    def test_long_sentence_by_commas_warns(self):
        f = plc.check_text("买米，买油，买盐，买醋。", [], "x")
        self.assertTrue(any(x[1] == "longsentence" for x in f))

    def test_short_clean_sentence_passes(self):
        self.assertEqual(plc.check_text("灯亮了，人也到了。", [], "x"), [])


class SrtTests(unittest.TestCase):
    def test_srt_noise_filtered(self):
        raw = "1\n00:00:01,000 --> 00:00:02,000\n灯亮了。\n"
        self.assertEqual(plc.srt_text(raw), "灯亮了。")


class BeatsSpokenTests(unittest.TestCase):
    """copy-craft 2.8 check face = spoken column (L7 card/oral split).

    Anchor column = card design face (R446 ruling), not an L18-L20 face.
    """

    def setUp(self):
        self.terms = ["机队", "工牌", "回测"]

    def test_anchor_only_hit_not_flagged(self):
        raw = ("hook | 机队花名册 · 两台电脑 | 系统日志开机：两台电脑。\n"
               "body | 工牌一 / 32 核 | 第一台 32 核，管代码。\n")
        f = plc.check_text(plc.beats_spoken_text(raw), self.terms, "x")
        self.assertEqual(f, [])

    def test_spoken_hit_flagged_with_line_no(self):
        raw = ("hook | 花名册 · 两台电脑 | 系统日志开机：机队点名。\n"
               "body | 身份牌 / 32 核 | 第一台 32 核，管代码。\n")
        f = plc.check_text(plc.beats_spoken_text(raw), self.terms, "x")
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0][0], "WARN")
        self.assertIn("first@L1", f[0][2])

    def test_spoken_hit_line_number_preserved(self):
        raw = ("hook | 花名册 | 系统日志开机：两台电脑。\n"
               "body | 身份牌 | 第二台 16 核，管回测。\n")
        f = plc.check_text(plc.beats_spoken_text(raw), self.terms, "x")
        self.assertEqual(len(f), 1)
        self.assertIn("first@L2", f[0][2])

    def test_longsentence_counts_spoken_only(self):
        raw = "beat | " + "卡" * 30 + " / " + "锚" * 20 + " | 短句一。短句二。\n"
        f = plc.check_text(plc.beats_spoken_text(raw), [], "x")
        self.assertEqual(f, [])

    def test_plain_line_fallback_scanned_whole(self):
        raw = "这一行没有拍型分隔，机队在正文里出现。\n"
        f = plc.check_text(plc.beats_spoken_text(raw), self.terms, "x")
        self.assertEqual(len(f), 1)
        self.assertIn("first@L1", f[0][2])

    def test_two_field_row_falls_back_whole_line(self):
        raw = "hook | 机队点名：两台电脑。\n"
        f = plc.check_text(plc.beats_spoken_text(raw), self.terms, "x")
        self.assertEqual(len(f), 1)


class ExitCodeTests(unittest.TestCase):
    def test_no_args_is_usage_error(self):
        self.assertEqual(plc.main([]), 2)

    def test_title_fail_exits_one(self):
        rc = plc.main(["--title", "夏普值第一名"])
        self.assertEqual(rc, 1)

    def test_clean_title_exits_zero(self):
        rc = plc.main(["--title", "一张证书的故事"])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
