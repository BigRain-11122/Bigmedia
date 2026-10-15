# -*- coding: utf-8 -*-
"""Unit tests for --h2-auto (tech#63/#180 leg-1, R2291): the em-budget
H2 tier ladder built into the renderer.

Pure function tests only (h2_auto_fit / _h2_face_rows): no ffmpeg, no
font file, real data/ never touched. Chinese strings appear as \\uXXXX
escapes per the ASCII encoding rule (same as test_render_card.py).

Ladder law (mirror of tools/lcard_m2.py margin law, tier set per the
tech#180 re-anchor): budget = (frame_w - 2*80) / size; a tier is viable
when budget - worst_auto_line_cost >= 0.30em (zero-margin tier
exclusion law, R380 precedent: 20.00em line at the 46 tier =
20.0 == 20.0 budget, zero margin, excluded -> falls to 44).

Run:
    python tests/test_h2_auto.py
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "render"))

import render_card_video as rcv  # noqa: E402


def _cjk(n):
    # U+4E00 repeats: cost = n * 1.0em
    return "\u4e00" * n


def cfg_with(lines_list, width=1080, per_card_h2=None):
    """lines_list = list of lines-arrays, one per card; per_card_h2 =
    optional list of explicit h2_size values (None = spec default)."""
    cards = []
    for i, lines in enumerate(lines_list):
        c = {"start": 0, "end": 3, "lines": lines}
        if per_card_h2 and per_card_h2[i] is not None:
            c["h2_size"] = per_card_h2[i]
        cards.append(c)
    return {
        "video": {"width": width, "height": 1080, "fps": 30, "bg": "black"},
        "font": {"file": "C:/fake/font.ttc", "subs_size": 38,
                 "subs_bottom": 110, "aigc_size": 30, "line_spacing": 12,
                 "h2_size": 52},
        "aigc_notice": "AI generated content",
        "tail": 0.5,
        "cards": cards,
    }


class TestH2AutoLadder(unittest.TestCase):
    def test_44_tier_reproduces_r380_precedent(self):
        # 20 CJK chars = 20.00em: the 46 tier gives budget 920/46=20.0
        # == 20.0 (zero margin, excluded) -> first viable tier is 44
        # (budget 20.909em, margin +0.909em).
        cfg = cfg_with([["h1", _cjk(20)]])
        self.assertEqual(44, rcv.h2_auto_fit(cfg))

    def test_40_tier_when_44_does_not_fit(self):
        # 21 CJK chars = 21.00em: 44-tier budget 20.909 < 21.30 -> 40
        # (budget 23.0em, margin +2.0em).
        cfg = cfg_with([["h1", _cjk(21)]])
        self.assertEqual(40, rcv.h2_auto_fit(cfg))

    def test_32_tier_skips_36_gap(self):
        # 26 CJK chars = 26.00em: 36-tier budget 25.556 (margin -0.44)
        # -> the ladder's 36->32 gap is real: 32 chosen (28.75em,
        # margin +2.75em). Conservative vs the M2 driver's even-step 34
        # (same deck passes there via a different ladder - both safe).
        cfg = cfg_with([["h1", _cjk(26)]])
        self.assertEqual(32, rcv.h2_auto_fit(cfg))

    def test_no_fit_raises(self):
        # 29 CJK chars = 29.00em: even the 32 tier gives only 28.75em.
        cfg = cfg_with([["h1", _cjk(29)]])
        with self.assertRaises(ValueError) as cm:
            rcv.h2_auto_fit(cfg)
        self.assertIn("no ladder tier fits", str(cm.exception))

    def test_no_h2_lines_raises(self):
        # every card is H1-only: nothing to fit -> loud error, never a
        # silent no-op gate.
        cfg = cfg_with([["only-h1"], ["also-h1"]])
        with self.assertRaises(ValueError) as cm:
            rcv.h2_auto_fit(cfg)
        self.assertIn("no H2 deck lines", str(cm.exception))

    def test_worst_line_drives_the_tier(self):
        # two cards: 10em and 21em H2 lines -> tier must fit the worst.
        cfg = cfg_with([["h1", _cjk(10)], ["h1b", _cjk(21)]])
        self.assertEqual(40, rcv.h2_auto_fit(cfg))

    def test_blank_h2_lines_ignored(self):
        cfg = cfg_with([["h1", _cjk(20), "", "  "]])
        self.assertEqual(44, rcv.h2_auto_fit(cfg))

    def test_wide_frame_uses_its_own_budget(self):
        # 1920-wide deck: budget at 50 = 1760/50 = 35.2em -> a 30em
        # line fits the top tier.
        cfg = cfg_with([["h1", _cjk(30)]], width=1920)
        self.assertEqual(50, rcv.h2_auto_fit(cfg))


class TestH2AutoExplicitOverride(unittest.TestCase):
    def test_violating_override_raises(self):
        # explicit h2_size=50 with a 26em line: budget 920/50=18.4em ->
        # the gate has no override hole.
        cfg = cfg_with([["h1", _cjk(26)]], per_card_h2=[50])
        with self.assertRaises(ValueError) as cm:
            rcv.h2_auto_fit(cfg)
        self.assertIn("explicit h2_size=50 violates em law",
                      str(cm.exception))

    def test_valid_override_all_explicit_returns_none(self):
        # explicit h2_size=34, 26em line: budget 27.06em, margin +1.06
        # -> law holds; nothing left in the auto pool -> None (spec
        # default stays, caller must not mutate cfg).
        cfg = cfg_with([["h1", _cjk(26)]], per_card_h2=[34])
        before = dict(cfg["font"])
        self.assertIsNone(rcv.h2_auto_fit(cfg))
        self.assertEqual(before, cfg["font"])

    def test_mixed_explicit_and_auto_pool(self):
        # card0 keeps a valid explicit 34; card1's 20em line drives the
        # ladder -> 44. Explicit row is still law-validated.
        cfg = cfg_with([["h1", _cjk(26)], ["h1b", _cjk(20)]],
                       per_card_h2=[34, None])
        self.assertEqual(44, rcv.h2_auto_fit(cfg))


class TestH2FaceRows(unittest.TestCase):
    def test_rows_carry_index_and_override(self):
        cfg = cfg_with([["h1", "a", "b"], ["h2", "c"]],
                       per_card_h2=[None, 40])
        rows = rcv._h2_face_rows(cfg)
        self.assertEqual([(0, "a", None), (0, "b", None), (1, "c", 40)],
                         rows)

    def test_no_cards_at_all(self):
        cfg = cfg_with([])
        self.assertEqual([], rcv._h2_face_rows(cfg))
        with self.assertRaises(ValueError):
            rcv.h2_auto_fit(cfg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
