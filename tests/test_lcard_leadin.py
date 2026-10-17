# -*- coding: utf-8 -*-
"""Tests for tools/lcard_leadin.py (tech#194 off-card lead-in template)."""
import copy
import io
import json
import os
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import lcard_leadin  # noqa: E402

V23 = os.path.join(REPO, "data", "storylines", "cards", "MC-20261017-DIGEST-v23", "cards.json")
REACT22 = os.path.join(REPO, "data", "storylines", "cards", "MC-20261017-REACT-v22", "cards.json")


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


class LeadinTest(unittest.TestCase):
    def test_glossary_loads(self):
        g = lcard_leadin.load_glossary()
        self.assertTrue(g["city_setting"])
        self.assertGreaterEqual(len(g["units"]), 10)

    def test_digest_v23_structure(self):
        r = lcard_leadin.build_leadin(load(V23), lcard_leadin.load_glossary())
        self.assertEqual(r["form"], "DIGEST")
        self.assertLessEqual(len(r["notes"]), 3)  # 2-3 sentence cap (tech#194)
        self.assertTrue(r["motif_exact"])
        self.assertIn(u"\u5f00\u5de5\u4ee4\u4e0b\u7684\u57ce\u5e02", r["paragraph"])  # motif sentence
        self.assertIn(u"\u76f2\u8bc4", r["paragraph"])  # headline term glossed
        self.assertFalse(r["unglossed"])  # context gate green

    def test_digest_deferred_reported(self):
        r = lcard_leadin.build_leadin(load(V23), lcard_leadin.load_glossary())
        self.assertTrue(r["deferred"])  # beyond-cap units stay visible to the editor

    def test_react_v22_two_state(self):
        g = lcard_leadin.load_glossary()
        r = lcard_leadin.build_leadin(load(REACT22), g)
        self.assertEqual(r["form"], "REACT")
        self.assertIn(g["react_two_state"], r["paragraph"])  # fact/fiction declaration
        self.assertIn(u"\u8f74", r["paragraph"])  # axis term glossed

    def test_unglossed_detection(self):
        cfg = load(V23)
        cfg["cards"][0]["lines"].append(u"\u54e8\u5175\u4f4d\u5347\u7ea7")  # fake jargon line
        g = copy.deepcopy(lcard_leadin.load_glossary())
        g["watch_patterns"].append(u"\u54e8\u5175")
        r = lcard_leadin.build_leadin(cfg, g)
        self.assertIn(u"\u54e8\u5175", r["unglossed"])  # gate catches uncovered jargon

    def test_motif_regex(self):
        edv = u"\u524d\u9762\u300c\u88ab\u8ffd\u95ee\u673a\u5236\u7684\u90a3\u4e00\u5929\uff0c\u57ce\u5e02\u628a\u673a\u5236\u8fde\u591c\u7ffb\u4fee\u4e86\u4e00\u904d\u300d\u6bcd\u9898\u540e\u9762"
        m = lcard_leadin.MOTIF_RE.search(edv)
        self.assertEqual(m.group(1), u"\u88ab\u8ffd\u95ee\u673a\u5236\u7684\u90a3\u4e00\u5929\uff0c\u57ce\u5e02\u628a\u673a\u5236\u8fde\u591c\u7ffb\u4fee\u4e86\u4e00\u904d")

    def test_render_md_footer(self):
        r = lcard_leadin.build_leadin(load(V23), lcard_leadin.load_glossary())
        md = lcard_leadin.render_md(load(V23), r, lcard_leadin.load_glossary())
        self.assertIn(u"M5 \u53d1\u5e03\u6848\u5bfc\u8bed\u6bb5\u8349\u7a3f", md)
        self.assertIn("DEFERRED glossary units", md)
        self.assertIn("tools/lcard_leadin.py (tech#194/#200/#204)", md)

    def test_render_md_footer_density_readings(self):
        """tech#204: footer lines carry hits readings + lever markers."""
        cfg = load(V23)
        g = lcard_leadin.load_glossary()
        r = lcard_leadin.build_leadin(cfg, g)
        md = lcard_leadin.render_md(cfg, r, g)
        self.assertRegex(
            md, r"NOTES density basis \(top-3 by per-card hits\): "
                 r".+?\(\d+ hits?[^)]*\)")
        self.assertRegex(
            md, r"DEFERRED glossary units \(beyond top-3 notes\): "
                 r".+?\(\d+ hits?\u00b7(\u5e73\u624b\u96c6\u6309\u672f\u8bed\u7c3f\u5e8f|\u4f4e\u5bc6\u5ea6)\)")


class DensityRankingTest(unittest.TestCase):
    """tech#200: per-card hit density outranks static glossary order."""

    GLOSS = {
        "city_setting": ["s1", "s2"],
        "react_two_state": "twostate",
        "motif_fallback": "fallback",
        "units": [
            {"terms": ["aa"], "note": "early-once"},
            {"terms": ["zz", "yy", "xx"], "note": "late-dense"},
            {"terms": ["bb"], "note": "early-second"},
            {"terms": ["cc"], "note": "fourth"},
        ],
        "watch_patterns": ["aa", "zz", "yy", "xx", "bb", "cc"],
    }

    def cfg(self, text):
        return {"meta": {"form": "DIGEST", "topic": "t", "editorial_value": ""},
                "cards": [{"lines": [text]}]}

    def test_density_beats_glossary_order(self):
        r = lcard_leadin.build_leadin(self.cfg(u"aa zz yy zz xx zz"), self.GLOSS)
        self.assertEqual(r["notes"][0], "late-dense")  # 4 hits > 1 despite later index

    def test_tie_break_keeps_glossary_order(self):
        r = lcard_leadin.build_leadin(self.cfg(u"aa bb zz cc"), self.GLOSS)
        self.assertEqual(r["notes"], ["early-once", "late-dense", "early-second"])
        # tech#204: 4-way 1-hit tie -> cap cut by index, reading names the lever
        self.assertEqual(
            r["deferred"],
            [u"cc (1 hit\u00b7\u5e73\u624b\u96c6\u6309\u672f\u8bed\u7c3f\u5e8f)"])

    def test_unit_hits_longest_match_no_double_count(self):
        self.assertEqual(lcard_leadin.unit_hits(u"bm-c \u8f66\u9053",
                                                [u"bm-c \u8f66\u9053", u"\u8f66\u9053", "bm-c"]), 1)

    def test_v22_anchor_core_units_recovered(self):
        """R2334 anchor regression: v22 lead-in must gloss its core jargon, not static top units."""
        g = lcard_leadin.load_glossary()
        cfg = load(os.path.join(REPO, "data", "storylines", "cards",
                                "MC-20261017-DIGEST-v22", "cards.json"))
        r = lcard_leadin.build_leadin(cfg, g)
        self.assertIn(u"\u4fee\u6cd5\u5305", r["paragraph"])  # core unit back in notes
        self.assertIn(u"V4\uff0fV5", r["paragraph"])  # V4/V5 note recovered over statics


class FooterReadingTest(unittest.TestCase):
    """tech#204: DEFERRED/NOTE lines carry density readings so the editor
    can tell a boundary tie (lever: reorder glossary) from low density
    (lever: change the card-face word)."""

    GLOSS5 = {
        "city_setting": ["s1"],
        "react_two_state": "twostate",
        "motif_fallback": "fallback",
        "units": [
            {"terms": ["aa"], "note": "u-aa"},
            {"terms": ["zz", "yy"], "note": "u-zz"},
            {"terms": ["bb"], "note": "u-bb"},
            {"terms": ["cc"], "note": "u-cc"},
            {"terms": ["dd"], "note": "u-dd"},
        ],
        "watch_patterns": ["aa", "zz", "yy", "bb", "cc", "dd"],
    }

    def cfg(self, text):
        return {"meta": {"form": "DIGEST", "topic": "t", "editorial_value": ""},
                "cards": [{"lines": [text]}]}

    def test_deferred_tie_reading(self):
        r = lcard_leadin.build_leadin(self.cfg(u"aa bb zz cc"), self.GLOSS5)
        self.assertEqual(
            r["deferred"],
            [u"cc (1 hit\u00b7\u5e73\u624b\u96c6\u6309\u672f\u8bed\u7c3f\u5e8f)"])

    def test_deferred_low_density_reading(self):
        # zz 3 hits, aa 2, bb 2 -> boundary 2; cc 1 sits below it
        r = lcard_leadin.build_leadin(self.cfg(u"zz zz zz aa aa bb bb cc"),
                                      self.GLOSS5)
        self.assertEqual(r["deferred"], [u"cc (1 hit\u00b7\u4f4e\u5bc6\u5ea6)"])

    def test_note_readings_tied_set_marked(self):
        r = lcard_leadin.build_leadin(self.cfg(u"aa bb zz cc"), self.GLOSS5)
        self.assertEqual(r["note_readings"], [
            u"aa (1 hit\u00b7\u5e73\u624b\u96c6\u6309\u672f\u8bed\u7c3f\u5e8f)",
            u"zz (1 hit\u00b7\u5e73\u624b\u96c6\u6309\u672f\u8bed\u7c3f\u5e8f)",
            u"bb (1 hit\u00b7\u5e73\u624b\u96c6\u6309\u672f\u8bed\u7c3f\u5e8f)",
        ])

    def test_note_reading_untied_no_marker(self):
        r = lcard_leadin.build_leadin(self.cfg(u"zz zz zz zz"), self.GLOSS5)
        self.assertEqual(r["note_readings"], [u"zz (4 hits)"])
        self.assertEqual(r["deferred"], [])


if __name__ == "__main__":
    unittest.main()
