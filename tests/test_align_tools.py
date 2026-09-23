# -*- coding: utf-8 -*-
"""Unit tests for R-C alignment tools: srt_fix (loose parse / overlap
clamp / rewrite) and whisper_to_srt.build_cues (pure grouping logic).

No model, no network, no real data/ files. Chinese appears as
\\uXXXX escapes per the ASCII encoding rule.

Run:
    python tests/test_align_tools.py
"""
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "render"))

import srt_fix  # noqa: E402
import whisper_to_srt as w2s  # noqa: E402


def write_tmp(text):
    p = Path(tempfile.mkdtemp(prefix="bsalign-")) / "in.srt"
    p.write_text(text, encoding="utf-8")
    return p


OVERLAP_SRT = "\n".join([
    "1", "00:00:00,100 --> 00:00:03,662",
    "line one",
    "",
    "2", "00:00:03,612 --> 00:00:06,637",   # 50ms overlap, edge-tts style
    "line two",
    "",
    "3", "00:00:06,637 --> 00:00:09,562",
    "line three",
]) + "\n"

MALFORMED_SRT = "\n".join([
    "garbage block without timing",
    "",
    "1", "00:00:00,000 --> 00:00:02,000",
    "good cue",
]) + "\n"

CJK = "\u4e09\u5bb6 AI \u516c\u53f8"  # "three AI companies" style token


class TestSrtFix(unittest.TestCase):
    def test_parse_loose_accepts_overlap(self):
        cues = srt_fix.parse_srt_loose(write_tmp(OVERLAP_SRT))
        self.assertEqual(len(cues), 3)
        self.assertAlmostEqual(cues[1][0], 3.612)

    def test_parse_loose_skips_malformed_blocks(self):
        cues = srt_fix.parse_srt_loose(write_tmp(MALFORMED_SRT))
        self.assertEqual(len(cues), 1)
        self.assertEqual(cues[0][2], "good cue")

    def test_clamp_pushes_start_to_prev_end(self):
        cues = srt_fix.parse_srt_loose(write_tmp(OVERLAP_SRT))
        fixed, dropped = srt_fix.clamp_overlaps(cues)
        self.assertEqual(dropped, 0)
        self.assertAlmostEqual(fixed[1][0], 3.662)  # = prev end, no overlap

    def test_clamp_drops_degenerate_cue(self):
        cues = [(0.0, 2.0, "a"), (1.0, 1.5, "b")]  # fully inside prev
        fixed, dropped = srt_fix.clamp_overlaps(cues)
        self.assertEqual(len(fixed), 1)
        self.assertEqual(dropped, 1)

    def test_write_srt_format_and_roundtrip(self):
        out = Path(tempfile.mkdtemp(prefix="bsalign-")) / "out.srt"
        srt_fix.write_srt([(0.0, 2.5, CJK), (2.5, 4.0, "b")], out)
        text = out.read_text(encoding="utf-8")
        self.assertIn("1\n00:00:00,000 --> 00:00:02,500\n" + CJK, text)
        self.assertIn("2\n00:00:02,500 --> 00:00:04,000\nb", text)
        # renderer's strict parser must accept the rewritten file
        import render_card_video as rcv
        parsed = rcv.parse_srt(out)
        self.assertEqual(len(parsed), 2)

    def test_fmt_t_padding(self):
        self.assertEqual(srt_fix.fmt_t(3662.5), "01:01:02,500")
        self.assertEqual(srt_fix.fmt_t(0.0), "00:00:00,000")


class TestBuildCues(unittest.TestCase):
    def words(self, *items):
        return [{"start": s, "end": e, "word": t} for s, e, t in items]

    def test_splits_on_char_budget_at_word_boundary(self):
        # budget is max-inclusive: merge up to 6 chars, split before 7th
        cues = w2s.build_cues(self.words(
            (0.0, 0.4, "aaa"), (0.4, 0.8, "bbb"), (0.8, 1.2, "cccc")), max_chars=6)
        self.assertEqual([c[2] for c in cues], ["aaabbb", "cccc"])

    def test_splits_on_silence_gap(self):
        cues = w2s.build_cues(self.words(
            (0.0, 0.5, "aaa"), (2.0, 2.5, "bbb")), max_chars=20)
        self.assertEqual(len(cues), 2)
        self.assertAlmostEqual(cues[1][0], 2.0)

    def test_skips_empty_words(self):
        cues = w2s.build_cues(self.words(
            (0.0, 0.3, " "), (0.3, 0.6, "aaa")), max_chars=20)
        self.assertEqual(cues, [(0.3, 0.6, "aaa")])

    def test_single_oversize_word_is_kept(self):
        cues = w2s.build_cues(self.words((0.0, 1.0, "a" * 30)), max_chars=5)
        self.assertEqual(len(cues), 1)

    def test_breaks_at_punctuation_once_half_budget(self):
        cues = w2s.build_cues(self.words(
            (0.0, 0.5, "abc."), (0.5, 1.0, "de"), (1.0, 1.5, "fgh")), max_chars=6)
        self.assertEqual([c[2] for c in cues], ["abc.", "defgh"])

    def test_overflow_prefers_last_in_cue_punctuation(self):
        # max=12: "b," sits below half budget so it stays in-cue, then
        # the oversized token forces a cut that snaps to the "b," ender
        # and the over-budget tail is drained by further closes.
        cues = w2s.build_cues(self.words(
            (0.0, 0.3, "aa"), (0.3, 0.6, "b,"), (0.6, 1.0, "cccc"),
            (1.0, 1.5, "d" * 12)), max_chars=12)
        self.assertEqual([c[2] for c in cues], ["aab,", "cccc", "d" * 12])

    def test_cjk_join_without_separator(self):
        cues = w2s.build_cues(self.words(
            (0.0, 0.3, CJK[:2]), (0.3, 0.6, CJK[2:])), max_chars=20)
        self.assertEqual(cues[0][2], CJK)


class TestRenderRegressions(unittest.TestCase):
    def test_render_textfiles_use_lf_not_crlf(self):
        # CRLF textfiles make drawtext treat \r as an extra break:
        # measured line pitch doubled (70 -> 142px) and 3-line cues
        # clipped at the frame bottom (R-C, t=33 frame of v2 render)
        import render_card_video as rcv
        cfg = {
            "video": {"width": 1080, "height": 1920, "fps": 30},
            "font": {"file": "C:/fake/font.ttc", "cards_size": 60,
                     "subs_size": 44, "aigc_size": 30, "subs_bottom": 300,
                     "line_spacing": 14},
            "aigc_notice": "AI generated",
            "tail": 0.8,
            "cards": [{"start": 0, "end": 2, "lines": ["x", "y"]}],
        }
        tmp = Path(tempfile.mkdtemp(prefix="bslf-"))
        plan = rcv.build_render_plan(cfg, [(0.0, 1.0, "a\nb")], tmp)
        bad = [p.name for p in plan["textfiles"]
               if b"\r\n" in p.read_bytes()]
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
