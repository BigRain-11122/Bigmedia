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
        self.assertIn("tools/lcard_leadin.py (tech#194)", md)


if __name__ == "__main__":
    unittest.main()
