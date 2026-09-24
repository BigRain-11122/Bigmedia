# -*- coding: utf-8 -*-
"""Unit tests for the edit-craft station + gate (R-E / M4 layer 1.8).

CEO edit-craft order 2026-09-24. Pure functions only: planner algebra
(xfade chain must preserve the absolute beat timeline), deterministic
hit/transition/treatment selection, and the independent gate findings.
No ffmpeg, no real cards file. Chinese appears as \\uXXXX (ASCII rule).

Run:
    python tests/test_edit_craft.py
"""
import copy
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "render"))
sys.path.insert(0, str(REPO / "src"))

import edit_craft as ec  # noqa: E402
import edit_craft_check as ecc  # noqa: E402


def fixture_cfg(n=12, step=5.0, tail=0.8):
    """n beats of `step` seconds; digits live in every third H1."""
    cards = []
    for i in range(n):
        h1 = "beat %d" % i if i % 3 == 0 else ("plain %d" % i)
        cards.append({"start": i * step, "end": (i + 1) * step,
                      "lines": [h1, "second line"]})
    return {"cards": cards, "tail": tail,
            "video": {"width": 1080, "height": 1920, "fps": 30}}


def aligned_cues(bounds, step):
    """Cue edges exactly on every beat boundary (alignment fixture)."""
    cues = []
    for k in range(len(bounds) - 1):
        s = bounds[k] + 0.01
        e = bounds[k + 1] - 0.01
        if e > s:
            cues.append((s, e, "cue %d" % k))
    return cues


class TestPlanner(unittest.TestCase):
    def setUp(self):
        self.cfg = fixture_cfg()
        self.n = len(self.cfg["cards"])

    def test_boundaries_and_duration(self):
        for name in ec.PROFILES:
            plan = ec.plan_edit(self.cfg, name)
            bounds = [b["time_s"] for b in plan["boundaries"]]
            self.assertEqual(len(bounds), self.n - 1)
            self.assertEqual(plan["last_beat_end_s"], 60.0)
            self.assertAlmostEqual(plan["duration_expected_s"], 60.8)
            # strictly increasing, inside the timeline
            self.assertEqual(bounds, sorted(bounds))
            self.assertTrue(all(0 < b < 60.0 for b in bounds))

    def test_duration_algebra_preserves_beats(self):
        # d_k = span_k + f_max (last: + tail), so xfade offsets keep beats
        for name in ec.PROFILES:
            plan = ec.plan_edit(self.cfg, name)
            f_max = plan["f_max_s"]
            ends = [0.0] + [b["time_s"] for b in plan["boundaries"]] + \
                [plan["last_beat_end_s"]]
            for s in plan["segments"]:
                k = s["idx"]
                span = ends[k + 1] - ends[k]
                want = (span + f_max) if k < self.n - 1 else \
                    (span + plan["tail_s"] + f_max)
                self.assertAlmostEqual(s["dur_s"], want, places=2)

    def test_hits_deterministic_and_capped(self):
        for name, prof in ec.PROFILES.items():
            plan = ec.plan_edit(self.cfg, name)
            self.assertEqual(plan, ec.plan_edit(self.cfg, name))  # det.
            self.assertLessEqual(len(plan["hits"]), prof["hit_cap"])
            self.assertIn(0, plan["hits"])        # open beat
            self.assertIn(self.n - 1, plan["hits"])  # CTA beat

    def test_no_static_segments(self):
        for name in ec.PROFILES:
            plan = ec.plan_edit(self.cfg, name)
            for s in plan["segments"]:
                self.assertIn(s["treatment"],
                              ("ken_in", "ken_out", "punch"))

    def test_flash_lands_after_incoming_transition(self):
        # a flash playing mid-blend is swallowed by the xfade (2026-09-24
        # YAVG probe: hit beats on transition boundaries showed no spike)
        for name in ("bilibili", "douyin"):
            plan = ec.plan_edit(self.cfg, name)
            for s in plan["segments"]:
                if s["flash"]:
                    k = s["idx"]
                    inc = plan["boundaries"][k - 1]["fade_s"] if k else 0.0
                    self.assertGreaterEqual(s["flash_st_s"], inc - 1e-6)

    def test_shipinhao_all_transitions(self):
        plan = ec.plan_edit(self.cfg, "shipinhao")
        cuts = [b for b in plan["boundaries"] if b["type"] == "cut"]
        self.assertEqual(len(cuts), 0)

    def test_bilibili_hard_cut_led(self):
        plan = ec.plan_edit(self.cfg, "bilibili")
        trans = [b for b in plan["boundaries"] if b["type"] != "cut"]
        share = len(trans) / float(len(plan["boundaries"]))
        self.assertTrue(0.40 <= share <= 0.60, share)

    def test_no_consecutive_same_transition(self):
        for name in ec.PROFILES:
            plan = ec.plan_edit(self.cfg, name)
            prev = None
            for b in plan["boundaries"]:
                if b["type"] != "cut":
                    self.assertNotEqual(b["type"], prev,
                                        "%s repeats %s" % (name, b["type"]))
                    prev = b["type"]
                else:
                    prev = None


class TestGate(unittest.TestCase):
    def setUp(self):
        self.cfg = fixture_cfg()
        self.plan = ec.plan_edit(self.cfg, "shipinhao")
        bounds = [0.0] + [b["time_s"] for b in self.plan["boundaries"]] + \
            [self.plan["last_beat_end_s"]]
        self.cues = aligned_cues(bounds, 5.0)

    def findings(self, plan, profile="shipinhao"):
        return {f[1]: f[0] for f in ecc.check(plan, self.cues, profile)}

    def test_clean_plan_passes(self):
        for name in ec.PROFILES:
            plan = ec.plan_edit(self.cfg, name)
            f = {x[1]: x[0] for x in ecc.check(plan, self.cues, name)}
            self.assertFalse(any(v == "FAIL" for v in f.values()),
                               "%s: %s" % (name, f))
            self.assertEqual(f.get("beat-align"), "PASS")

    def test_boundary_off_voice_fails(self):
        bad = copy.deepcopy(self.plan)
        # one miss of 11 still passes by design (>=90%); two must FAIL
        bad["boundaries"][3]["time_s"] += 1.5   # off the voice rhythm
        bad["boundaries"][6]["time_s"] += 1.2
        f = self.findings(bad)
        self.assertEqual(f.get("beat-misaligned"), "FAIL")

    def test_static_segment_fails(self):
        bad = copy.deepcopy(self.plan)
        bad["segments"][5]["treatment"] = "none"
        f = self.findings(bad)
        self.assertEqual(f.get("static-seg"), "FAIL")

    def test_off_pool_transition_fails(self):
        bad = copy.deepcopy(self.plan)
        bad["boundaries"][1]["type"] = "fadegraysfantasy"
        f = self.findings(bad)
        self.assertEqual(f.get("transition-pool"), "FAIL")

    def test_flash_on_calm_profile_fails(self):
        bad = copy.deepcopy(self.plan)
        bad["segments"][1]["flash"] = True
        f = self.findings(bad)
        self.assertEqual(f.get("flash-not-allowed"), "FAIL")

    def test_timeline_drift_fails(self):
        bad = copy.deepcopy(self.plan)
        bad["segments"][2]["dur_s"] += 0.4
        f = self.findings(bad)
        self.assertEqual(f.get("timeline-drift"), "FAIL")

    def test_independence_constants_match_engine(self):
        # drift between engine profiles and gate SPEC must FAIL loudly:
        # fade windows and pools must stay in sync across both files
        for name, spec in ecc.SPEC.items():
            prof = ec.PROFILES[name]
            self.assertLessEqual(prof["fade_s"], spec["fade_max_s"])
            self.assertGreaterEqual(prof["fade_s"], spec["fade_min_s"])
            for t in prof["pool"]:
                self.assertIn(t, spec["pool"])


if __name__ == "__main__":
    unittest.main()
