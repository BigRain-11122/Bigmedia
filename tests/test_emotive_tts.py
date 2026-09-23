# -*- coding: utf-8 -*-
"""Pure-function tests for the cyber voice dial (src/render/emotive_tts.py).

O-20260923-2136-bm-a: no TTS/network/ffmpeg run here - the dial table,
the flatten transform and the duration-preservation invariants of the
filter chains are the contract that keeps SRT cues and card cuts valid.

Run:
    python tests/test_emotive_tts.py
"""
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "render"))

import emotive_tts as et  # noqa: E402


class TestCyberize(unittest.TestCase):
    def test_pitch_flattened_uniform(self):
        out = et.cyberize(et.PROFILES, -8, "-4%")
        for name in et.PROFILES:
            flags = out[name]
            self.assertIn("--pitch=-8Hz", flags)
            self.assertEqual(1, sum(1 for f in flags if f.startswith("--pitch=")),
                             "%s must carry exactly one pitch flag" % name)
            for f in flags:
                self.assertFalse(f.startswith("--pitch=+"), name)

    def test_rate_variation_kept_and_shifted(self):
        out = et.cyberize(et.PROFILES, -8, "-4%")
        # hook was -8% -> -12%, punch was +6% -> +2%
        self.assertIn("--rate=-12%", out["hook"])
        self.assertIn("--rate=+2%", out["punch"])
        # body had no flags: gains pitch + (no rate -> no rate flag added)
        self.assertEqual(["--pitch=-8Hz"], out["body"])
        # every profile name survives
        self.assertEqual(set(et.PROFILES), set(out))

    def test_no_mutation_of_base_table(self):
        before = {k: list(v) for k, v in et.PROFILES.items()}
        et.cyberize(et.PROFILES, -12, "-8%")
        self.assertEqual(before, {k: list(v) for k, v in et.PROFILES.items()})


class TestCyberChains(unittest.TestCase):
    def test_three_levels_exist(self):
        self.assertEqual({"light", "mid", "full"}, set(et.CYBER_CHAINS))
        self.assertEqual({"mid", "full"}, set(et.CYBER_PITCH_HZ))
        self.assertEqual(set(et.CYBER_PITCH_HZ), set(et.CYBER_RATE_SHIFT))

    def test_limiter_is_last_stage(self):
        for level, chain in et.CYBER_CHAINS.items():
            stages = [s for s in chain.split(",") if s]
            self.assertTrue(stages[-1].startswith("alimiter="),
                            "%s must end with alimiter" % level)

    def test_asetrate_drop_is_tempo_compensated(self):
        # duration preservation: asetrate factor f must be undone by
        # atempo=1/f (within 0.1%) - else SRT cues drift off the voice.
        for level in ("mid", "full"):
            chain = et.CYBER_CHAINS[level]
            m = re.search(r"asetrate=24000\*(0\.\d+)", chain)
            self.assertIsNotNone(m, "%s: no asetrate drop found" % level)
            factor = float(m.group(1))
            t = re.search(r"atempo=([\d.]+)", chain)
            self.assertIsNotNone(t, "%s: no atempo compensation" % level)
            tempo = float(t.group(1))
            self.assertAlmostEqual(1.0 / factor, tempo, delta=0.001,
                                    msg="%s tempo mismatch" % level)

    def test_light_chain_has_no_resample(self):
        # light only adds texture: no pitch/time stage at all
        chain = et.CYBER_CHAINS["light"]
        for stage in ("asetrate", "atempo", "aresample"):
            self.assertNotIn(stage, chain)
        for stage in ("vibrato", "acrusher", "alimiter"):
            self.assertIn(stage, chain)

    def test_mid_full_carry_machine_texture(self):
        for level in ("mid", "full"):
            chain = et.CYBER_CHAINS[level]
            for stage in ("vibrato", "acrusher", "aecho", "highpass", "lowpass"):
                self.assertIn(stage, chain, "%s missing %s" % (level, stage))
        # the dial must get heavier: full vibrates deeper than mid
        f_mid = float(re.search(r"vibrato=f=(\d+)", et.CYBER_CHAINS["mid"]).group(1))
        f_full = float(re.search(r"vibrato=f=(\d+)", et.CYBER_CHAINS["full"]).group(1))
        self.assertGreater(f_full, f_mid)


if __name__ == "__main__":
    unittest.main(verbosity=2)
