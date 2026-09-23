# -*- coding: utf-8 -*-
"""Minimal unit tests for the card timeline renderer (src/render/).

Pure functions only (SRT parse / cards load / plan build): no ffmpeg run,
no font file needed, real data/ never touched. Chinese strings appear as
\\uXXXX escapes per the ASCII encoding rule (same as make_draft.py).

Run:
    python tests/test_render_card.py
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "render"))

import render_card_video as rcv  # noqa: E402


def cards_cfg(notice="AI generated content", cards=None):
    return {
        "video": {"width": 1080, "height": 1920, "fps": 30, "bg": "black"},
        "font": {"file": "C:/fake/font.ttc", "cards_size": 60, "subs_size": 44,
                 "aigc_size": 30, "subs_bottom": 300, "line_spacing": 14},
        "aigc_notice": notice,
        "tail": 0.8,
        "cards": cards if cards is not None else [
            {"start": 0, "end": 3, "lines": ["a", "b"]},
            {"start": 3, "end": 15, "lines": ["c"]},
        ],
    }


SRT_OK = "\n".join([
    "1", "00:00:00,000 --> 00:00:03,000",
    "three companies, one human",
    "",
    "2", "00:00:03,000 --> 00:00:06,500",
    "only one line",
    "",
])

SRT_CJK = "\n".join([
    "1", "00:00:00,000 --> 00:00:03,000",
    "\u4e09\u5bb6 AI \u516c\u53f8",
    "",
])


class TestParseSrt(unittest.TestCase):
    def test_ok(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "subs.srt"
            p.write_text(SRT_OK, encoding="utf-8")
            cues = rcv.parse_srt(p)
        self.assertEqual(2, len(cues))
        self.assertEqual((0.0, 3.0, "three companies, one human"), cues[0])
        self.assertEqual((3.0, 6.5, "only one line"), cues[1])

    def test_cjk_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "subs.srt"
            p.write_text(SRT_CJK, encoding="utf-8")
            cues = rcv.parse_srt(p)
        self.assertEqual("\u4e09\u5bb6 AI \u516c\u53f8", cues[0][2])

    def test_rejects_missing_timing(self):
        bad = "1\n00:00:00,000 -x- 00:00:03,000\ntext\n"
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "subs.srt"
            p.write_text(bad, encoding="utf-8")
            with self.assertRaises(ValueError):
                rcv.parse_srt(p)

    def test_rejects_overlap(self):
        bad = ("1\n00:00:00,000 --> 00:00:05,000\na\n\n"
               "2\n00:00:04,000 --> 00:00:06,000\nb\n")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "subs.srt"
            p.write_text(bad, encoding="utf-8")
            with self.assertRaises(ValueError):
                rcv.parse_srt(p)

    def test_rejects_bad_time(self):
        bad = "1\n00:00:00 --> 00:00:03,000\ntext\n"
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "subs.srt"
            p.write_text(bad, encoding="utf-8")
            with self.assertRaises(ValueError):
                rcv.parse_srt(p)


class TestLoadCards(unittest.TestCase):
    def _write(self, d, cfg):
        p = Path(d) / "cards.json"
        p.write_text(json.dumps(cfg, ensure_ascii=False), encoding="utf-8")
        return p

    def test_ok(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = rcv.load_cards(self._write(d, cards_cfg()))
        self.assertEqual(2, len(cfg["cards"]))

    def test_aigc_notice_red_line(self):
        # empty notice must be refused: AIGC labeling is a red line
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                rcv.load_cards(self._write(d, cards_cfg(notice="   ")))

    def test_missing_top_key(self):
        cfg = cards_cfg()
        del cfg["font"]
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                rcv.load_cards(self._write(d, cfg))

    def test_card_overlap(self):
        cfg = cards_cfg(cards=[
            {"start": 0, "end": 5, "lines": ["a"]},
            {"start": 4, "end": 8, "lines": ["b"]},
        ])
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                rcv.load_cards(self._write(d, cfg))

    def test_card_empty_lines(self):
        cfg = cards_cfg(cards=[{"start": 0, "end": 5, "lines": ["", "  "]}])
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                rcv.load_cards(self._write(d, cfg))

    def test_font_key_required(self):
        cfg = cards_cfg()
        del cfg["font"]["subs_bottom"]
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                rcv.load_cards(self._write(d, cfg))


class TestWrap(unittest.TestCase):
    def test_long_cjk_line_wraps(self):
        # 26 CJK chars at 44px on a 1080px frame: budget ~20.9 em -> 2 lines
        text = "\u8f6c" * 26
        wrapped = rcv.wrap_for_width(text, 44, 1080)
        lines = wrapped.split("\n")
        self.assertEqual(2, len(lines))
        for ln in lines:
            self.assertLessEqual(len(ln), 21)

    def test_short_line_untouched(self):
        text = "hello world"
        self.assertEqual(text, rcv.wrap_for_width(text, 44, 1080))

    def test_existing_newline_respected(self):
        text = "aaa\nbbb"
        self.assertEqual("aaa\nbbb", rcv.wrap_for_width(text, 44, 1080))

    def test_narrow_ascii_fits_more(self):
        # 24 ASCII chars ~ 13.2 em < 20.9 em budget -> single line
        text = "abcdefgh" * 3
        self.assertEqual(1, len(rcv.wrap_for_width(text, 44, 1080).split("\n")))


class TestPlanAndMatch(unittest.TestCase):
    def test_voiceover_match(self):
        cues = [(0.0, 3.0, "hello  world"), (3.0, 6.0, "foo\nbar")]
        self.assertTrue(rcv.voiceover_matches("helloworld\n foobar", cues))
        self.assertFalse(rcv.voiceover_matches("helloworld baz", cues))

    def test_build_plan(self):
        cues = rcv.parse_srt(_tmp_srt(SRT_OK))
        with tempfile.TemporaryDirectory() as d:
            plan = rcv.build_render_plan(cards_cfg(), cues, d)
            ft = plan["filter_text"]
            # "[0:v]" must sit directly before the first filter (a comma
            # after a link label = empty filter name = graph parse fail)
            self.assertTrue(ft.startswith("[0:v]drawtext="))
            self.assertTrue(ft.endswith("[v]"))
            # drawtext count = cards + cues + 1 aigc
            self.assertEqual(5, ft.count("drawtext="))
            self.assertEqual(4, ft.count("enable='between(t,"))
            # aigc notice persists for the whole video (no enable window)
            self.assertIn("alpha=0.6", ft)  # O-1937 visual-spec S3: gray60 notice
            # duration = max end (cues 6.5, cards 15) + tail 0.8
            self.assertAlmostEqual(15.8, plan["duration"], places=3)
            for p in plan["textfiles"]:
                self.assertTrue(Path(p).exists())

    def test_build_plan_escapes_colon(self):
        cues = []
        with tempfile.TemporaryDirectory() as d:
            plan = rcv.build_render_plan(cards_cfg(), cues, d)
            self.assertIn("C\\:/fake/font.ttc", plan["filter_text"])

    def test_grain_appends_noise_vignette_after_text(self):
        """O-20260923-2210-bm-a: grain>0 = film grain + vignette, appended
        after all text layers (never before them), and off by default."""
        cues = []
        with tempfile.TemporaryDirectory() as d:
            base = rcv.build_render_plan(cards_cfg(), cues, d)
            self.assertNotIn("noise=alls=", base["filter_text"])
            self.assertNotIn("vignette", base["filter_text"])
            with tempfile.TemporaryDirectory() as d2:
                grainy = rcv.build_render_plan(cards_cfg(), cues, d2, grain=7)
                ft = grainy["filter_text"]
                self.assertIn("noise=alls=7:allf=t+u", ft)
                self.assertIn("vignette=angle=PI/6", ft)
                # texture stages come last: nothing after the vignette
                self.assertTrue(ft.rstrip().endswith("vignette=angle=PI/6[v]"))
                # timeline untouched by the aesthetic pass
                self.assertAlmostEqual(base["duration"], grainy["duration"])


def _tmp_srt(content):
    import tempfile as tf
    d = tf.mkdtemp(prefix="bsrcv-test-")
    p = Path(d) / "subs.srt"
    p.write_text(content, encoding="utf-8")
    return p


if __name__ == "__main__":
    unittest.main(verbosity=2)
