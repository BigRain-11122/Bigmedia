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
import tempfile
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


def fixture_cfg_visual(cards_only_idx=(6, 11), n=12):
    """Cards with per-beat visual declarations (footage-matching S1);
    footage beats point at real temp files - the gate existence check
    needs them on disk."""
    cfg = fixture_cfg(n=n)
    holder = tempfile.TemporaryDirectory()
    root = Path(holder.name)
    for i, c in enumerate(cfg["cards"]):
        if i in cards_only_idx:
            c["visual"] = {"cards-only": True,
                           "reason": "cta" if i == n - 1 else "slogan"}
        else:
            f = root / ("shot%02d.mp4" % i)
            f.write_bytes(b"")
            c["visual"] = {"source": str(f), "req": "matched shot"}
    cfg["_holder"] = holder  # keep the temp dir alive with the cfg
    return cfg


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
        # A3: d_k = span_k + incoming fade (last: + tail); cuts add 0 -
        # concat runs trim frame-exact, no f_max blanket needed
        for name in ec.PROFILES:
            plan = ec.plan_edit(self.cfg, name)
            ends = [0.0] + [b["time_s"] for b in plan["boundaries"]] + \
                [plan["last_beat_end_s"]]
            for s in plan["segments"]:
                k = s["idx"]
                span = ends[k + 1] - ends[k]
                inc = (plan["boundaries"][k - 1]["fade_s"]
                       if 1 <= k <= len(plan["boundaries"]) else 0.0)
                want = span + inc + (plan["tail_s"] if k == self.n - 1
                                     else 0.0)
                self.assertAlmostEqual(s["dur_s"], want, places=2)

    def test_true_hard_cuts_blend_nothing(self):
        # A3: cut fade_s must be exactly 0 - the retired 0.05s 2-frame
        # approximation was the E8 review weak point
        for name in ("bilibili", "douyin"):
            plan = ec.plan_edit(self.cfg, name)
            cuts = [b for b in plan["boundaries"] if b["type"] == "cut"]
            self.assertTrue(cuts, name)
            for c in cuts:
                self.assertEqual(c["fade_s"], 0.0)
            self.assertEqual(plan["hard_cut_s"], 0.0)

    def test_boundaries_frame_quantized(self):
        # concat splices land frame-exact only on the frame grid;
        # odd-time cards quantize to it (max shift 1 frame = 33ms).
        # Plan JSON keeps 3dp, so assert frame RECOVERABILITY via
        # round() (the engine's own trim math), not raw exactness.
        cfg = fixture_cfg()
        for i, c in enumerate(cfg["cards"]):
            c["start"] = i * 5 + 0.017
            c["end"] = (i + 1) * 5 + 0.017
        plan = ec.plan_edit(cfg, "douyin")
        for b in plan["boundaries"]:
            frames = b["time_s"] * ec.FPS
            self.assertLess(abs(frames - round(frames)), 0.1)
        self.assertGreaterEqual(plan["last_beat_end_s"], 11 * 5 + 0.017)
        frames = plan["last_beat_end_s"] * ec.FPS
        self.assertLess(abs(frames - round(frames)), 0.1)

    def test_runs_split_only_at_cuts(self):
        # fade chains build runs; cut boundaries are the concat seams
        plan = ec.plan_edit(self.cfg, "douyin")
        self.assertEqual([len(r) for r in
                          ec.build_runs(self.n, plan["boundaries"])],
                         [3, 2, 3, 2, 2])
        plan_b = ec.plan_edit(self.cfg, "bilibili")
        self.assertEqual([len(r) for r in
                          ec.build_runs(self.n, plan_b["boundaries"])],
                         [2] * 6)
        plan_s = ec.plan_edit(self.cfg, "shipinhao")
        self.assertEqual(ec.build_runs(self.n, plan_s["boundaries"]),
                         [list(range(self.n))])

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

    def test_cut_blend_regression_fails(self):
        # A3 independence law: the executor regressing to the retired
        # 0.05s 2-frame approximation must FAIL here, not pass silently
        plan = ec.plan_edit(self.cfg, "bilibili")
        self.assertTrue(any(b["type"] == "cut" for b in plan["boundaries"]))
        for b in plan["boundaries"]:
            if b["type"] == "cut":
                b["fade_s"] = 0.05
                break
        f = {x[1]: x[0] for x in ecc.check(plan, self.cues, "bilibili")}
        self.assertEqual(f.get("cut-blended"), "FAIL")

    def test_independence_constants_match_engine(self):
        # drift between engine profiles and gate SPEC must FAIL loudly:
        # fade windows and pools must stay in sync across both files
        for name, spec in ecc.SPEC.items():
            prof = ec.PROFILES[name]
            self.assertLessEqual(prof["fade_s"], spec["fade_max_s"])
            self.assertGreaterEqual(prof["fade_s"], spec["fade_min_s"])
            for t in prof["pool"]:
                self.assertIn(t, spec["pool"])


class TestVisualMatching(unittest.TestCase):
    """footage-matching-spec: per-beat evidence, no default footage."""

    def setUp(self):
        self.cfg = fixture_cfg_visual()
        self.plan = ec.plan_edit(self.cfg, "shipinhao")
        bounds = [0.0] + [b["time_s"] for b in self.plan["boundaries"]] + \
            [self.plan["last_beat_end_s"]]
        self.cues = aligned_cues(bounds, 5.0)

    def tearDown(self):
        self.cfg["_holder"].cleanup()

    def findings(self, plan):
        return {f[1]: f[0] for f in ecc.check(plan, self.cues, "shipinhao")}

    def test_matched_plan_carries_per_beat_sources(self):
        self.assertEqual(self.plan["visual_mode"], "matched")
        for s in self.plan["segments"]:
            if s["cards_only"]:
                self.assertIsNone(s["visual_source"])
                self.assertEqual(s["treatment"], "flat")
                self.assertTrue(s["cards_only_reason"])
            else:
                self.assertTrue(s["visual_source"])
                self.assertIn(s["treatment"], ("ken_in", "ken_out", "punch"))
        self.assertAlmostEqual(self.plan["visual_ratio"], 10.0 / 12, places=3)
        self.assertNotIn(11, self.plan["hits"])  # cards-only never hits

    def test_partial_declaration_raises(self):
        # one undeclared beat among declared ones = the wallpaper sin
        cfg = fixture_cfg_visual()
        cfg["_holder"].cleanup()
        cfg["cards"][3].pop("visual")
        with self.assertRaises(ValueError):
            ec.plan_edit(cfg, "shipinhao")

    def test_cards_only_without_reason_raises(self):
        cfg = fixture_cfg_visual()
        cfg["_holder"].cleanup()
        cfg["cards"][6]["visual"] = {"cards-only": True}
        with self.assertRaises(ValueError):
            ec.plan_edit(cfg, "shipinhao")

    def test_gate_matched_clean_passes(self):
        f = self.findings(self.plan)
        self.assertFalse(any(v == "FAIL" for v in f.values()), f)
        self.assertEqual(f.get("visual-ratio"), "PASS")

    def test_gate_visual_missing_file_fails(self):
        bad = copy.deepcopy(self.plan)
        bad["segments"][0]["visual_source"] = "no/such/shot.mp4"
        f = self.findings(bad)
        self.assertEqual(f.get("visual-missing-file"), "FAIL")

    def test_gate_undeclared_beat_fails(self):
        bad = copy.deepcopy(self.plan)
        bad["segments"][0]["visual_source"] = None
        f = self.findings(bad)
        self.assertEqual(f.get("visual-undeclared"), "FAIL")

    def test_gate_ratio_below_line_fails(self):
        # 7 of 12 cards-only = 0.583 < 0.80 (spec S3 line)
        cfg = fixture_cfg_visual(cards_only_idx=(1, 2, 4, 6, 8, 9, 11))
        plan = ec.plan_edit(cfg, "shipinhao")
        cfg["_holder"].cleanup()
        f = self.findings(plan)
        self.assertEqual(f.get("visual-ratio"), "FAIL")

    def test_gate_legacy_warns_not_fails(self):
        cfg = fixture_cfg()
        plan = ec.plan_edit(cfg, "shipinhao")
        f = self.findings(plan)
        self.assertEqual(f.get("visual-legacy"), "WARN")


class TestRampMicroBlocks(unittest.TestCase):
    """C1 engine-integration algebra (research/ffmpeg-editing-craft-v1
    S1.4): fixed-span variable-rate - total output frames unchanged,
    micro-block edges on the 1/FPS grid, exact per-block speeds."""

    LADDER = [1.2, 1.6667, 2.5]

    def test_span_algebra_sum_equals_plain_render(self):
        for dur in (1.5, 2.37, 4.83, 7.5, 12.0):
            blocks = ec.build_micro_blocks(dur, 0.5, self.LADDER)
            self.assertIsNotNone(blocks, dur)
            self.assertEqual(sum(b["out_frames"] for b in blocks),
                             int(round(dur * ec.FPS)) + 1)

    def test_head_speed_one_and_ladder_ascending_consumption(self):
        blocks = ec.build_micro_blocks(4.83, 0.5, self.LADDER)
        self.assertEqual(blocks[0]["speed"], 1.0)
        speeds = [b["speed"] for b in blocks[1:]]
        self.assertTrue(all(v > 1.0 for v in speeds))
        self.assertEqual(speeds, sorted(speeds))      # ease-in ladder
        # window law: ramp tail <= 40% of the beat span
        self.assertLessEqual(sum(b["out_frames"] for b in blocks[1:]),
                             0.4 * 4.83 * ec.FPS + 0.5)

    def test_source_windows_contiguous_and_frame_quantized(self):
        blocks = ec.build_micro_blocks(4.83, 0.5, self.LADDER)
        self.assertEqual(blocks[0]["src_start_s"], 0.0)
        for prev, cur in zip(blocks, blocks[1:]):
            self.assertAlmostEqual(prev["src_end_s"], cur["src_start_s"],
                                   places=6)
        for b in blocks:
            # every source edge is an integer source-frame multiple
            # (6dp rounding leaves <1e-4 frame = sub-frame residue only)
            for edge in (b["src_start_s"], b["src_end_s"]):
                self.assertAlmostEqual(edge * ec.FPS, round(edge * ec.FPS),
                                       places=4)
            # actual speed is exact: n_src/n_out (no drift accumulation)
            n_out = b["out_frames"]
            n_src = round((b["src_end_s"] - b["src_start_s"]) * ec.FPS)
            self.assertAlmostEqual(b["speed"], n_src / float(n_out),
                                   places=5)

    def test_ramp_consumes_more_source_than_window(self):
        blocks = ec.build_micro_blocks(4.83, 0.5, self.LADDER)
        src_total = (blocks[-1]["src_end_s"] - blocks[0]["src_start_s"])
        out_total = sum(b["out_frames"] for b in blocks) / ec.FPS
        self.assertGreater(src_total, out_total)     # S1.1 fixed-span law

    def test_short_beat_degrades_to_none(self):
        self.assertIsNone(ec.build_micro_blocks(0.05, 0.5, self.LADDER))
        self.assertIsNone(ec.build_micro_blocks(0.2, 0.5, self.LADDER))
        # window clamped to 40% of span: 1.2s beat still ramps (smaller)
        blocks = ec.build_micro_blocks(1.2, 0.5, self.LADDER)
        self.assertIsNotNone(blocks)
        self.assertLessEqual(sum(b["out_frames"] for b in blocks[1:]),
                             round(0.4 * 1.2 * ec.FPS))

    def test_douyin_ramps_punch_beats_only(self):
        cfg = fixture_cfg()
        plan = ec.plan_edit(cfg, "douyin")
        ramped = [s["idx"] for s in plan["segments"] if s["ramp"]]
        self.assertEqual(ramped, plan["ramp_beats"])
        self.assertEqual(ramped, plan["hits"])       # punch treatment beats
        for s in plan["segments"]:
            if s["ramp"]:
                self.assertEqual(s["treatment"], "punch")
        # A3 span algebra untouched by the ramp: d_k == span_k + incoming
        # fade (recomputed from THIS plan's own boundaries - profiles
        # differ in fade_s, so cross-profile dur lists legitimately
        # differ; the law is per-plan, not per-profile-pair).
        bts = ([0.0] + [b["time_s"] for b in plan["boundaries"]]
               + [plan["last_beat_end_s"]])
        last = len(plan["segments"]) - 1
        for k, s in enumerate(plan["segments"]):
            span = bts[k + 1] - bts[k]
            incoming = plan["boundaries"][k - 1]["fade_s"] if k else 0.0
            expected = span + incoming + (plan["tail_s"] if k == last else 0.0)
            self.assertAlmostEqual(s["dur_s"], expected, places=3)
        # beat times themselves are profile-independent
        plain = ec.plan_edit(cfg, "shipinhao")
        self.assertEqual([b["time_s"] for b in plan["boundaries"]],
                         [b["time_s"] for b in plain["boundaries"]])

    def test_other_profiles_ramp_off(self):
        cfg = fixture_cfg()
        for name in ("shipinhao", "bilibili"):
            plan = ec.plan_edit(cfg, name)
            self.assertTrue(all(s["ramp"] is None
                                for s in plan["segments"]))

    def test_cards_only_beats_never_ramp(self):
        cfg = fixture_cfg_visual(cards_only_idx=(0, 6, 11))
        plan = ec.plan_edit(cfg, "douyin")
        cfg["_holder"].cleanup()
        for s in plan["segments"]:
            if s["cards_only"]:
                self.assertIsNone(s["ramp"])
        # beat 0 is cards-only here, so it must not be a ramp beat even
        # though the plain fixture makes it a hit
        self.assertNotIn(0, plan["ramp_beats"])

    def test_filter_string_carries_pitfall_trio(self):
        cfg = fixture_cfg()
        plan = ec.plan_edit(cfg, "douyin")
        seg = next(s for s in plan["segments"] if s["ramp"])
        fc = ec.ramp_filter_complex(seg, seg["ramp"], 1080, 1920, 0.0)
        n_blocks = len(seg["ramp"])
        self.assertIn("[0:v]split=%d" % n_blocks, fc)
        # pitfall 1: per-block setsar + one more on the treatment chain
        self.assertEqual(fc.count("setsar=1"), n_blocks + 1)
        # pitfall 2: rebase+speed in ONE setpts, divide AFTER subtract
        self.assertEqual(fc.count("setpts=(PTS-STARTPTS)/"), n_blocks)
        self.assertIn("concat=n=%d:v=1:a=0[cat]" % n_blocks, fc)
        self.assertIn("zoompan=", fc)                          # treatment
        if seg["flash"]:
            self.assertIn("fade=t=in", fc)


if __name__ == "__main__":
    unittest.main()
