# -*- coding: utf-8 -*-
"""Segment frame-sampling law tests for the layer-1.8 gate (R1820).

R186 fake-green closure: every segment's head/mid/tail frames must be
sampled and decodable (coverage), footage segments must not be
near-solid (degenerate), declared-motion segments must actually move
head->tail (frozen), and a labeled contact sheet must land on disk so
mid/tail frames are always in the inspector's view. Tiny synthetic
ffmpeg lavfi videos - the plan-only suites in test_edit_craft.py stay
ffmpeg-free.

Run:
    python tests/test_edit_frames.py
"""
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import edit_craft_check as ecc  # noqa: E402


def _ffmpeg(args):
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error"] + args,
                    check=True)


def make_moving_video(path, dur=2.4):
    """testsrc: rich texture + a running counter = real motion."""
    _ffmpeg(["-f", "lavfi", "-i", "testsrc=size=160x120:rate=10",
             "-t", str(dur), "-pix_fmt", "yuv420p", "-y", str(path)])


def make_static_video(path, dur=2.4):
    """Textured but motionless: one noise frame looped (frozen tell)."""
    from PIL import Image
    png = path.with_suffix(".png")
    rng = random.Random(7)
    img = Image.new("L", (160, 120))
    img.putdata([rng.randint(0, 255) for _ in range(160 * 120)])
    img.save(png)
    _ffmpeg(["-loop", "1", "-i", str(png), "-t", str(dur),
             "-pix_fmt", "yuv420p", "-y", str(path)])
    png.unlink()


def make_solid_video(path, dur=2.4):
    """Flat gray: degenerate tell for any footage segment."""
    _ffmpeg(["-f", "lavfi", "-i", "color=c=gray:size=160x120:rate=10",
             "-t", str(dur), "-pix_fmt", "yuv420p", "-y", str(path)])


def make_source_video(path, dur=1.0):
    """The stream_loop visual source: short so beats must wrap."""
    _ffmpeg(["-f", "lavfi", "-i", "testsrc=size=160x120:rate=10",
             "-t", str(dur), "-pix_fmt", "yuv420p", "-y", str(path)])


def make_dirty_wrap_video(path, dur=3.0, band_at=0.9, band=0.3):
    """Moving footage with a near-solid band covering the crossing."""
    _ffmpeg(["-f", "lavfi", "-i", "testsrc=size=160x120:rate=10",
             "-f", "lavfi", "-i", "color=c=gray:size=160x120:rate=10",
             "-filter_complex",
             "[0:v]split=2[s1][s2];"
             "[s1]trim=duration=%.2f,setpts=PTS-STARTPTS[a];"
             "[1:v]trim=duration=%.2f,setpts=PTS-STARTPTS[b];"
             "[s2]trim=start=%.2f,setpts=PTS-STARTPTS[c];"
             "[a][b][c]concat=n=3:v=1:a=0" % (band_at, band, band_at),
             "-t", str(dur), "-pix_fmt", "yuv420p", "-y", str(path)])


def loop_plan(n=1, seg_s=3.0, src=None, src_off=0.0, cards_only=()):
    """Matched-mode plan whose segments cite a (short) visual source."""
    segs, bounds = [], []
    for k in range(n):
        segs.append({"idx": k, "dur_s": seg_s, "flash": False,
                     "treatment": "ken_in",
                     "cards_only": k in cards_only,
                     "cards_only_reason":
                         "declared" if k in cards_only else "",
                     "visual_source": str(src), "src_off_s": src_off})
        if k:
            bounds.append({"time_s": k * seg_s, "type": "fade",
                           "fade_s": 0.2})
    return {"segments": segs, "boundaries": bounds,
            "last_beat_end_s": n * seg_s, "tail_s": 0.0,
            "duration_expected_s": n * seg_s, "hits": [],
            "visual_mode": "matched"}


def frame_plan(n=2, seg_s=1.2, treatment="ken_in",
               cards_only=(), flat=(), flash=()):
    segs, bounds = [], []
    for k in range(n):
        segs.append({"idx": k, "dur_s": seg_s, "flash": k in flash,
                     "treatment": "flat" if k in flat else treatment,
                     "cards_only": k in cards_only,
                     "cards_only_reason":
                         "declared" if k in cards_only else ""})
        if k:
            bounds.append({"time_s": k * seg_s, "type": "fade",
                           "fade_s": 0.2})
    return {"segments": segs, "boundaries": bounds,
            "last_beat_end_s": n * seg_s, "tail_s": 0.0,
            "duration_expected_s": n * seg_s, "hits": [],
            "visual_mode": "legacy"}


class TestFrameLaw(unittest.TestCase):
    def setUp(self):
        self.holder = tempfile.TemporaryDirectory()
        self.root = Path(self.holder.name)
        self.out = self.root / "probe"

    def tearDown(self):
        self.holder.cleanup()

    def level(self, findings, code):
        for lv, c, _ in findings:
            if c == code:
                return lv
        return None

    def test_moving_footage_passes_all(self):
        v = self.root / "moving.mp4"
        make_moving_video(v)
        fs = ecc.check_frames(v, frame_plan(), self.out)
        self.assertEqual(self.level(fs, "frame-coverage"), "PASS")
        self.assertIsNone(self.level(fs, "frame-degenerate"))
        self.assertIsNone(self.level(fs, "frame-frozen"))
        self.assertEqual(self.level(fs, "frame-tile"), "PASS")
        self.assertTrue((self.out / "tile.png").exists())
        self.assertEqual(
            len(list((self.out / "frames").glob("*.png"))), 6)  # 2 segs x 3

    def test_static_footage_flags_frozen_not_degenerate(self):
        v = self.root / "static.mp4"
        make_static_video(v)
        fs = ecc.check_frames(v, frame_plan(), self.out)
        self.assertEqual(self.level(fs, "frame-frozen"), "FAIL")
        self.assertIsNone(self.level(fs, "frame-degenerate"))

    def test_solid_footage_flags_degenerate(self):
        v = self.root / "solid.mp4"
        make_solid_video(v)
        fs = ecc.check_frames(v, frame_plan(), self.out)
        self.assertEqual(self.level(fs, "frame-degenerate"), "FAIL")

    def test_declared_still_segments_exempt(self):
        v = self.root / "solid.mp4"
        make_solid_video(v)
        fs = ecc.check_frames(v, frame_plan(cards_only=(0,), flat=(1,)),
                             self.out)
        self.assertIsNone(self.level(fs, "frame-degenerate"))
        self.assertIsNone(self.level(fs, "frame-frozen"))
        self.assertEqual(self.level(fs, "frame-coverage"), "PASS")

    def test_flash_beat_exempt_from_degenerate_only(self):
        v = self.root / "solid.mp4"
        make_solid_video(v)
        fs = ecc.check_frames(v, frame_plan(flash=(0, 1)), self.out)
        self.assertIsNone(self.level(fs, "frame-degenerate"))
        self.assertEqual(self.level(fs, "frame-frozen"), "FAIL")

    def test_subsecond_span_skips_frozen(self):
        v = self.root / "static.mp4"
        make_static_video(v, dur=0.8)
        fs = ecc.check_frames(v, frame_plan(seg_s=0.4), self.out)
        self.assertIsNone(self.level(fs, "frame-frozen"))

    def test_missing_video_fails_cleanly(self):
        fs = ecc.check_frames(self.root / "nope.mp4", frame_plan(), self.out)
        self.assertEqual(self.level(fs, "frame-video"), "FAIL")

    def test_undecodable_video_flags_coverage(self):
        v = self.root / "junk.mp4"
        v.write_bytes(b"this is not a video")
        fs = ecc.check_frames(v, frame_plan(), self.out)
        self.assertEqual(self.level(fs, "frame-coverage"), "FAIL")

    def test_empty_plan_fails_coverage(self):
        v = self.root / "solid.mp4"
        make_solid_video(v)
        fs = ecc.check_frames(v, {"segments": []}, self.out)
        self.assertEqual(self.level(fs, "frame-coverage"), "FAIL")


class TestLoopCrossLaw(unittest.TestCase):
    """Law 3: stream_loop wrap-crossing zone sampling (R196 closure)."""

    def setUp(self):
        self.holder = tempfile.TemporaryDirectory()
        self.root = Path(self.holder.name)
        self.out = self.root / "probe"

    def tearDown(self):
        self.holder.cleanup()

    def level(self, findings, code):
        for lv, c, _ in findings:
            if c == code:
                return lv
        return None

    def test_wrap_beat_samples_crossing_zone(self):
        src = self.root / "src.mp4"
        make_source_video(src, dur=1.0)
        v = self.root / "moving.mp4"
        make_moving_video(v, dur=3.0)
        fs = ecc.check_frames(v, loop_plan(src=src), self.out)
        self.assertEqual(self.level(fs, "loop-cross"), "PASS")
        for tag in ("pre", "x", "post"):
            self.assertTrue(
                (self.out / "frames" / ("s00-x0-%s.png" % tag)).exists())
        self.assertTrue((self.out / "tile.png").exists())

    def test_short_beat_no_wrap_no_findings(self):
        src = self.root / "src.mp4"
        make_source_video(src, dur=5.0)
        v = self.root / "moving.mp4"
        make_moving_video(v, dur=3.0)
        fs = ecc.check_frames(v, loop_plan(src=src), self.out)
        self.assertIsNone(self.level(fs, "loop-cross"))
        self.assertIsNone(self.level(fs, "loop-cross-probe"))

    def test_dirty_crossing_zone_flags_r196_tell(self):
        src = self.root / "src.mp4"
        make_source_video(src, dur=1.0)
        v = self.root / "dirtywrap.mp4"
        make_dirty_wrap_video(v, band_at=0.9, band=0.3, dur=3.0)
        fs = ecc.check_frames(v, loop_plan(src=src), self.out)
        self.assertEqual(self.level(fs, "loop-cross-dirty"), "FAIL")
        self.assertEqual(self.level(fs, "loop-cross"), "PASS")

    def test_crossing_samples_on_junk_video_flag_coverage(self):
        src = self.root / "src.mp4"
        make_source_video(src, dur=1.0)
        v = self.root / "junk.mp4"
        v.write_bytes(b"not a video")
        fs = ecc.check_frames(v, loop_plan(src=src), self.out)
        self.assertEqual(self.level(fs, "frame-coverage"), "FAIL")
        self.assertEqual(self.level(fs, "loop-cross-coverage"), "FAIL")

    def test_unprovable_source_flags_probe_face(self):
        src = self.root / "src.txt"
        src.write_text("not footage", encoding="utf-8")
        v = self.root / "moving.mp4"
        make_moving_video(v, dur=3.0)
        fs = ecc.check_frames(v, loop_plan(src=src), self.out)
        self.assertEqual(self.level(fs, "loop-cross-probe"), "FAIL")

    def test_cap_beyond_four_crossings_warns(self):
        src = self.root / "src.mp4"
        make_source_video(src, dur=0.3)
        v = self.root / "moving.mp4"
        make_moving_video(v, dur=3.0)
        fs = ecc.check_frames(v, loop_plan(src=src), self.out)
        self.assertEqual(self.level(fs, "loop-cross-capped"), "WARN")
        self.assertEqual(self.level(fs, "loop-cross"), "PASS")

    def test_cards_only_source_skipped(self):
        src = self.root / "src.mp4"
        make_source_video(src, dur=1.0)
        v = self.root / "moving.mp4"
        make_moving_video(v, dur=3.0)
        fs = ecc.check_frames(v, loop_plan(src=src, cards_only=(0,)),
                              self.out)
        self.assertIsNone(self.level(fs, "loop-cross"))
        self.assertIsNone(self.level(fs, "loop-cross-probe"))

    # ---- tech#23 (R1834): branch-aware wrap crossing faces ----------

    def test_plain_matched_src_off_is_dead_data(self):
        """Plain matched renders from the source head (no -ss), so a
        plan src_off_s never shifts the wrap - crossings at k*src_len."""
        src = self.root / "src3.mp4"
        make_source_video(src, dur=3.0)
        seg = {"visual_source": str(src), "src_off_s": 1.5}
        times, over, err = ecc._wrap_crossings(seg, 0.0, 5.0)
        self.assertIsNone(err)
        self.assertEqual([round(t, 3) for t in times], [3.0])
        self.assertEqual(over, 0)

    def test_ramp_walk_matches_ladder_speeds(self):
        """A speed>1 micro-block reaches the boundary EARLIER than the
        linear src_len guess - the walk must reflect block speeds."""
        src = self.root / "src3.mp4"
        make_source_video(src, dur=3.0)
        seg = {"visual_source": str(src), "src_off_s": 0.0,
               "ramp": [{"src_start_s": 0.0, "src_end_s": 4.833,
                         "speed": 1.0},
                        {"src_start_s": 4.833, "src_end_s": 9.1,
                         "speed": 2.0}]}
        times, over, err = ecc._wrap_crossings(seg, 0.0, 8.0)
        self.assertIsNone(err)
        self.assertEqual(len(times), 3)
        for want, got in zip([3.0, 5.417, 6.917], times):
            self.assertAlmostEqual(want, got, places=2)
        self.assertEqual(over, 0)

    def test_ramp_src_off_honored_in_head_block(self):
        """Ramp trims at absolute src_off + block position on the looped
        timeline - a head-block crossing lands at src_len - src_off."""
        src = self.root / "src3.mp4"
        make_source_video(src, dur=3.0)
        seg = {"visual_source": str(src), "src_off_s": 1.5,
               "ramp": [{"src_start_s": 0.0, "src_end_s": 3.033,
                         "speed": 1.0}]}
        times, over, err = ecc._wrap_crossings(seg, 0.0, 5.0)
        self.assertIsNone(err)
        self.assertEqual([round(t, 3) for t in times], [1.5])
        self.assertEqual(over, 0)

    def test_ramp_src_off_beyond_src_len_still_valid(self):
        """src_off >= src_len is legal on a looped input (the old linear
        face mislabeled it degenerate); the walk still finds k >= 1."""
        src = self.root / "src3.mp4"
        make_source_video(src, dur=3.0)
        seg = {"visual_source": str(src), "src_off_s": 3.5,
               "ramp": [{"src_start_s": 0.0, "src_end_s": 2.967,
                         "speed": 1.0}]}
        times, over, err = ecc._wrap_crossings(seg, 0.0, 5.0)
        self.assertIsNone(err)
        self.assertEqual([round(t, 3) for t in times], [2.5])
        self.assertEqual(over, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
