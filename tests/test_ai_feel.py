# -*- coding: utf-8 -*-
"""Unit tests for the AI-feel gate (src/ai_feel_check.py).

O-20260923-2210-bm-a: pure functions only - gap extraction, CV math and
the findings logic on fixture beats/SRT. No ffmpeg, no TTS, real data
never touched. Chinese appears as \\uXXXX escapes (ASCII rule).

Run:
    python tests/test_ai_feel.py
"""
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "render"))

import ai_feel_check as afc  # noqa: E402


def srt_from_spans(spans):
    """spans = [(start, end), ...] -> minimal SRT text."""
    def ts(t):
        h = int(t // 3600)
        m = int(t % 3600 // 60)
        s = int(t % 60)
        ms = int(round((t - int(t)) * 1000))
        return "%02d:%02d:%02d,%03d" % (h, m, s, ms)
    out = []
    for i, (a, z) in enumerate(spans, 1):
        out += [str(i), "%s --> %s" % (ts(a), ts(z)), "line %d" % i, ""]
    return "\n".join(out)


BEATS_ZERO_GAP = "\n".join([
    "body | a / b | " + "\u957f\u53e5" * 4,
    "body | a / b | " + "\u957f\u53e5" * 4,
    "body | a / b | " + "\u957f\u53e5" * 4,
    "body | a / b | " + "\u957f\u53e5" * 4,
    "body | a / b | " + "\u957f\u53e5" * 4,
])

BEATS_VARIED = "\n".join([
    "hook | a / b | " + "\u957f\u53e5" * 5,
    "punch | a / b | " + "\u77ed" ,
    "body | a / b | " + "\u957f\u53e5" * 3,
    "wink | a / b | " + "\u957f\u53e5" * 2,
    "turn | a / b | " + "\u77ed\u77ed",
    "proof | a / b | " + "\u957f\u53e5" * 4,
])


class TestMath(unittest.TestCase):
    def test_cv(self):
        self.assertAlmostEqual(0.0, afc.cv([5.0, 5.0, 5.0]))
        self.assertGreater(afc.cv([5.0, 1.0, 6.0]), 0.4)
        self.assertEqual(0.0, afc.cv([3.0]))  # n<2 = 0 by contract

    def test_inter_cue_gaps(self):
        cues = [(0.0, 3.0, "a"), (3.2, 6.0, "b"), (6.9, 9.0, "c")]
        self.assertEqual([0.2, 0.9], afc.inter_cue_gaps(cues))


class TestGateLogic(unittest.TestCase):
    def _findings(self, beats_text, spans):
        with tempfile.TemporaryDirectory() as d:
            bp = Path(d) / "beats.txt"
            bp.write_text(beats_text, encoding="utf-8")
            beats = __import__("emotive_tts").parse_beats(bp)
            sp = Path(d) / "subs.srt"
            sp.write_text(srt_from_spans(spans), encoding="utf-8")
            cues = __import__("render_card_video").parse_srt(sp)
            return {(lv, code) for lv, code, _ in afc.check(beats, cues)}

    def test_zero_gap_metronome_fails(self):
        # 5 beats back-to-back (the v9 pre-human render shape)
        spans = [(0.0, 3.0), (3.0, 6.0), (6.0, 9.0), (9.0, 12.0), (12.0, 15.0)]
        f = self._findings(BEATS_ZERO_GAP, spans)
        self.assertIn(("FAIL", "gap-zero"), f)
        self.assertIn(("FAIL", "prosody-flat"), f)   # all on 'body'
        self.assertIn(("FAIL", "pacing-metronome"), f)  # identical durations

    def test_varied_render_passes(self):
        # v10 post-human shape: varied gaps + varied lengths + profiles
        spans = [(0.0, 3.1), (3.42, 5.9), (6.35, 10.2),
                 (10.66, 13.4), (13.99, 16.0), (16.31, 21.3)]
        f = self._findings(BEATS_VARIED, spans)
        self.assertNotIn(("FAIL", "gap-zero"), f)
        self.assertNotIn(("FAIL", "gap-uniform"), f)
        self.assertNotIn(("FAIL", "prosody-flat"), f)
        self.assertNotIn(("FAIL", "pacing-metronome"), f)
        self.assertIn(("PASS", "gaps"), f)

    def test_uniform_nonzero_gaps_fail(self):
        # gaps exist but are all exactly 0.30s = machine cadence
        spans = [(0.0, 3.0), (3.30, 6.0), (6.30, 9.0), (9.30, 12.0),
                 (12.30, 15.0)]
        f = self._findings(BEATS_VARIED, spans)
        self.assertIn(("FAIL", "gap-uniform"), f)

    def test_copy_uniformity_is_advisory_not_blocking(self):
        spans = [(0.0, 3.0), (3.42, 6.0), (6.35, 9.0), (9.9, 12.0),
                 (12.5, 15.0), (15.7, 18.0)]
        f = self._findings(BEATS_ZERO_GAP, spans)
        # even where everything else fails, copy CV only ever WARNs
        self.assertNotIn(("FAIL", "copy-uniform"),
                         {k for k in f if k[1] == "copy-uniform"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
