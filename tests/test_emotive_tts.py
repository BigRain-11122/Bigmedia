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


class TestHumanFeel(unittest.TestCase):
    """O-20260923-2210-bm-a: seeded micro-variance = the anti-metronome
    contract (reproducible renders, bounded jitter, breaths only after
    long sentences)."""

    def test_human_series_deterministic_and_bounded(self):
        a = et.human_series(42, 5)
        b = et.human_series(42, 5)
        self.assertEqual(a, b)
        self.assertEqual(5, len(a))
        for rate_jit, pitch_jit in a:
            self.assertTrue(et.HUMAN_RATE_JIT[0] <= rate_jit <= et.HUMAN_RATE_JIT[1])
            self.assertTrue(et.HUMAN_PITCH_JIT[0] <= pitch_jit <= et.HUMAN_PITCH_JIT[1])

    def test_boundary_plan_varies_within_range(self):
        durs = [5.9, 2.9, 3.8, 5.4, 6.4, 5.5, 4.3, 4.2, 5.7, 4.4, 4.2]
        plan = et.boundary_plan(7, durs)
        self.assertEqual(len(durs) - 1, len(plan))
        for item in plan:
            lo = et.HUMAN_GAP_BASE - et.HUMAN_GAP_SPREAD
            hi = et.HUMAN_GAP_BASE + et.HUMAN_GAP_SPREAD
            self.assertTrue(lo - 1e-9 <= item["gap"] <= hi + 1e-9)
        gaps = [i["gap"] for i in plan]
        self.assertGreater(max(gaps) - min(gaps), 0.05,
                            "gaps must vary (uniform gaps = AI metronome)")

    def test_breath_only_after_long_beats(self):
        durs = [5.0, 1.0, 5.0, 1.0, 6.0, 1.0]
        for seed in range(20):
            for i, item in enumerate(et.boundary_plan(seed, durs)):
                if item["breath"]:
                    self.assertGreaterEqual(
                        durs[i], et.HUMAN_BREATH_AFTER_S,
                        "seed %d breath after short beat %d" % (seed, i))

    def test_boundary_plan_deterministic(self):
        durs = [5.0, 1.0, 5.0, 1.0]
        self.assertEqual(et.boundary_plan(3, durs), et.boundary_plan(3, durs))
        self.assertNotEqual(et.boundary_plan(3, durs), et.boundary_plan(4, durs))

    def test_jitter_flags_merges_existing_values(self):
        out = et.jitter_flags(["--rate=-8%", "--pitch=-3Hz"], 2, 1)
        self.assertEqual(["--rate=-6%", "--pitch=-2Hz"], out)

    def test_jitter_flags_adds_when_profile_bare(self):
        out = et.jitter_flags([], -2, 3)  # body profile carries no flags
        self.assertEqual(["--rate=-2%", "--pitch=+3Hz"], out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
