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


if __name__ == "__main__":
    unittest.main(verbosity=2)
