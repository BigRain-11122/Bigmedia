# -*- coding: utf-8 -*-
"""Wrap-crossing renderer contract tests (tech#28, R1842).

tech#23/R1834 proved the render-vs-check divergence face (3/3): the
plain matched branch plays the looped source from its head (render_
segments passes no -ss there, so plan src_off_s is DEAD DATA on that
branch and wraps land at k*src_len), while ramp segments cross the
loop boundary early when a speed>1 micro-block runs (block walk, not
the linear src_len-src_off guess - the R196 fake-green face). The
r1834 pilot fixed _wrap_crossings to be branch-aware, but the pilot
script itself was cleaned up, leaving the check machine-side
self-attested. This module is the standing doorbell (tech#28):

  * REAL renders through render_segments - the production code path,
    not a hand-copied pipeline - for BOTH branch faces;
  * a two-color synthetic source (head half red, tail half cyan)
    lets wrap positions be read back from rendered frames: right
    before a predicted crossing the frame must be the source TAIL
    color, right after it the HEAD color;
  * if anyone adds -ss to the plain matched branch or changes the
    ramp coordinate system, predicted-vs-actual colors diverge and
    this suite rings. Must-run window: any renderer face change.

Run:
    python tests/test_wrap_contract.py
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "render"))

import edit_craft_check as ecc  # noqa: E402
import edit_craft  # noqa: E402

SRC_LEN = 1.5           # synthetic source length: wraps every 1.5s
HALF = 0.75             # red 0..0.75, cyan 0.75..1.5
PROBE_S = 0.05          # pre/post sample offset around a crossing
W, H = 320, 180


def _ffmpeg(args):
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error"] + args,
                   check=True)


def make_two_color_source(path):
    """Head half solid red, tail half solid cyan (loop-wrapped by the
    renderer with -stream_loop): after every wrap the frame returns to
    red, just before a wrap it is cyan."""
    _ffmpeg(["-f", "lavfi",
             "-i", "color=c=red:size=%dx%d:rate=30" % (W, H),
             "-f", "lavfi",
             "-i", "color=c=cyan:size=%dx%d:rate=30" % (W, H),
             "-filter_complex",
             "[0:v]trim=duration=%.2f,setpts=PTS-STARTPTS[r];"
             "[1:v]trim=duration=%.2f,setpts=PTS-STARTPTS[c];"
             "[r][c]concat=n=2:v=1:a=0" % (HALF, HALF),
             "-pix_fmt", "yuv420p", "-t", "%.2f" % SRC_LEN,
             "-y", str(path)])


def _seg(idx, dur, src, src_off, ramp):
    return {"idx": idx, "src_off_s": src_off, "dur_s": dur,
            "treatment": "push", "hit": False, "flash": False,
            "flash_st_s": 0.0, "cards_only": False,
            "cards_only_reason": "", "visual_source": str(src),
            "ramp": ramp}


class WrapRenderContract(unittest.TestCase):
    """Renderer face <-> _wrap_crossings walk contract (tech#28)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="wrap-contract-"))
        cls.src = cls.tmp / "twocolor.mp4"
        make_two_color_source(cls.src)
        cls.cfg = {"video": {"width": W, "height": H}}
        # segment 0: plain matched, plan src_off is DEAD DATA on this
        # branch -> wraps must land at 1.5 / 3.0 (k*src_len), never at
        # 0.75 / 2.25 / 3.75. segment 1: hand-walked ramp (src_off 0.7;
        # block0 abs 0.7-1.7 at speed 1.6 crosses 1.5 at 0.5s; block1
        # abs 1.7-3.1 at speed 1.0 crosses 3.0 at 1.925s).
        cls.seg_plain = _seg(0, 4.0, cls.src, 0.75, None)
        cls.seg_ramp = _seg(1, 2.025, cls.src, 0.7, [
            {"src_start_s": 0.0, "src_end_s": 1.0, "speed": 1.6},
            {"src_start_s": 1.0, "src_end_s": 2.4, "speed": 1.0},
        ])
        plan = {"visual_mode": "matched",
                "segments": [cls.seg_plain, cls.seg_ramp]}
        segs = edit_craft.render_segments(plan, cls.cfg, None, cls.tmp)
        if segs is None or len(segs) != 2:
            raise AssertionError("render_segments failed for the "
                                 "contract plan")
        cls.seg_plain_path, cls.seg_ramp_path = segs[0], segs[1]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _rgb(self, video, t):
        png = self.tmp / ("probe-%s-%.3f.png" % (video.stem, t))
        if not ecc._extract_frame(video, t, png):
            self.fail("frame extraction failed at t=%.3f" % t)
        from PIL import Image, ImageStat
        img = Image.open(png)
        img.load()
        return ImageStat.Stat(img).mean

    def _assert_color(self, rgb, want, ctx):
        r, g, b = rgb[0], rgb[1], rgb[2]
        if want == "red":
            self.assertTrue(
                r > 150 and g < 110 and b < 110,
                "%s: wanted source HEAD color (red), got "
                "r=%.0f g=%.0f b=%.0f" % (ctx, r, g, b))
        else:
            self.assertTrue(
                g > 150 and b > 150 and r < 110,
                "%s: wanted source TAIL color (cyan), got "
                "r=%.0f g=%.0f b=%.0f" % (ctx, r, g, b))

    def _verify_crossings(self, seg, video, expected):
        # contract side A: the check-side walk must predict the
        # hand-computed truth (locks _wrap_crossings itself).
        times, over, err = ecc._wrap_crossings(seg, 0.0, seg["dur_s"])
        self.assertIsNone(err)
        self.assertEqual([round(t, 3) for t in times], expected,
                         "_wrap_crossings walk drifted from the "
                         "hand-computed contract")
        self.assertEqual(over, 0)
        # contract side B: the real render must actually wrap exactly
        # there - tail color before, head color after every crossing.
        for t in times:
            self._assert_color(
                self._rgb(video, max(t - PROBE_S, 1e-3)),
                "cyan", "pre-crossing t=%.3f" % t)
            self._assert_color(
                self._rgb(video, t + PROBE_S),
                "red", "post-crossing t=%.3f" % t)

    def test_plain_matched_wrap_contract(self):
        # wraps at k*src_len: src_off_s (0.75) must be dead data here.
        # If a -ss ever lands on this branch, wraps shift to
        # 0.75/2.25/3.75 and the pre/post colors invert -> FAIL.
        self._verify_crossings(self.seg_plain, self.seg_plain_path,
                               [round(SRC_LEN, 3), round(2 * SRC_LEN, 3)])

    def test_ramp_wrap_contract(self):
        # speed>1 block crosses the boundary EARLIER than the linear
        # guess (linear would say 0.6/2.0; the block walk says
        # 0.5/1.925). The render must match the walk, not the guess.
        self._verify_crossings(self.seg_ramp, self.seg_ramp_path,
                               [0.5, 1.925])

    def test_ramp_face_absolute_src_off_coords(self):
        # pure functional face lock: ramp trims at absolute
        # src_off_s + block span and divides AFTER the subtract
        # (pitfall 2) - a coordinate-system change rings here even
        # before the render-level contract fires.
        s = {"dur_s": 2.0, "treatment": "push", "flash": False,
             "flash_st_s": 0.0}
        fc = edit_craft.ramp_filter_complex(
            s, [{"src_start_s": 0.0, "src_end_s": 1.0, "speed": 1.6}],
            W, H, 0.7)
        self.assertIn("trim=start=0.700000:end=1.700000", fc)
        self.assertIn("setpts=(PTS-STARTPTS)/1.600000", fc)


if __name__ == "__main__":
    unittest.main()
