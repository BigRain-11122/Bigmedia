# -*- coding: utf-8 -*-
"""Unit tests for tools/lcard_m2.py (tech#177 canonical L-card M2 driver).

Pure functions only: timestamp formatting, subs derivation from the
cards.json card end (zero hardcode), R2281 copy-residue guard, and the
duration law mirror. No ffmpeg run, real data/ never touched. Chinese
strings appear as \\uXXXX escapes per the ASCII encoding rule.

Run:
    python tests/test_lcard_m2.py
"""
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "src" / "render"))

import lcard_m2  # noqa: E402
import render_card_video as rcv  # noqa: E402

BOTTOM = "\u70ed\u70b9\u8f6c\u8ff0\u81ea\u77e5\u4e4e\u70ed\u699c"  # 8 CJK chars


class TestFmtSrtTs(unittest.TestCase):
    def test_values(self):
        self.assertEqual(lcard_m2.fmt_srt_ts(0), "00:00:00,000")
        self.assertEqual(lcard_m2.fmt_srt_ts(0.8), "00:00:00,800")
        self.assertEqual(lcard_m2.fmt_srt_ts(2.6), "00:00:02,600")
        self.assertEqual(lcard_m2.fmt_srt_ts(3.0), "00:00:03,000")
        self.assertEqual(lcard_m2.fmt_srt_ts(61.25), "00:01:01,250")
        self.assertEqual(lcard_m2.fmt_srt_ts(3600.5), "01:00:00,500")
        self.assertEqual(lcard_m2.fmt_srt_ts(3661.999), "01:01:01,999")

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            lcard_m2.fmt_srt_ts(-1)


class TestBuildSubs(unittest.TestCase):
    def test_end_is_derived_argument(self):
        s = lcard_m2.build_subs(BOTTOM, 2.6)
        self.assertIn("--> 00:00:02,600", s)
        self.assertIn(BOTTOM, s)
        self.assertTrue(s.startswith("1\n00:00:00,000 --> "))

    def test_roundtrip_via_renderer_parse(self):
        # the written cue must parse back to exactly the card end
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "subs.srt"
            p.write_text(lcard_m2.build_subs(BOTTOM, 3.0), encoding="utf-8")
            cues = rcv.parse_srt(str(p))
        self.assertEqual(len(cues), 1)
        self.assertAlmostEqual(cues[0][0], 0.0)
        self.assertAlmostEqual(cues[0][1], 3.0)
        self.assertEqual(cues[0][2], BOTTOM)


class TestR2281Guard(unittest.TestCase):
    """R2281 incident: a 3.0s DIGEST cue pasted into a 2.6s REACT card
    inflated the mp4 to 3.8s and failed the spec probe. The canonical
    driver derives the cue end and hard-checks it before any render."""

    CARD_END = 2.6

    def _cues_for(self, end):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "subs.srt"
            p.write_text(lcard_m2.build_subs(BOTTOM, end), encoding="utf-8")
            return rcv.parse_srt(str(p))

    def test_derived_end_passes_guard(self):
        cues = self._cues_for(self.CARD_END)
        for _, ce, _ in cues:
            self.assertFalse(ce > self.CARD_END + 1e-9)

    def test_residue_end_would_be_caught(self):
        # simulate the R2281 residue: hardcoded 3.0 in a 2.6 card
        cues = self._cues_for(3.0)
        caught = any(ce > self.CARD_END + 1e-9 for _, ce, _ in cues)
        self.assertTrue(caught)


class TestDurationLaw(unittest.TestCase):
    def _cfg(self, end, tail=None):
        cfg = {"cards": [{"start": 0.0, "end": end, "lines": ["x", "y"]}]}
        if tail is not None:
            cfg["tail"] = tail
        return cfg

    def test_expected_duration_card_plus_tail(self):
        cfg = self._cfg(2.6, tail=0.8)
        cues = [(0.0, 2.6, BOTTOM)]
        self.assertAlmostEqual(lcard_m2.expected_duration(cfg, cues), 3.4)

    def test_residue_inflates_duration(self):
        # documents the inflation law the guard exists to prevent:
        # subs end 3.0 > card end 2.6 -> 3.0 + 0.8 = 3.8s mp4
        cfg = self._cfg(2.6, tail=0.8)
        cues = [(0.0, 3.0, BOTTOM)]
        self.assertAlmostEqual(lcard_m2.expected_duration(cfg, cues), 3.8)

    def test_default_tail(self):
        cfg = self._cfg(2.6)
        self.assertAlmostEqual(lcard_m2.expected_duration(cfg, [(0.0, 2.6, "")]),
                               3.1)  # renderer default tail 0.5

    def test_card_end_of(self):
        self.assertAlmostEqual(
            lcard_m2.card_end_of({"cards": [{"end": 2.6}, {"end": 1.9}]}), 2.6)

    def test_card_end_of_empty_raises(self):
        with self.assertRaises(ValueError):
            lcard_m2.card_end_of({"cards": []})


if __name__ == "__main__":
    unittest.main(verbosity=1)
