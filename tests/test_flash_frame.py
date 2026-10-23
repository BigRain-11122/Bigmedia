# -*- coding: utf-8 -*-
"""Unit tests for the layer 1.8 flash-frame face (tech#368, R2418).

Anchor: full_mv_v700 carried one frame of a foreign shot at 44.042s. Every
existing gate missed it (cut checks pass, head/mid/tail sampling never lands
on it). These tests pin the two directions that matter:

  * a one-frame colour flip inside an otherwise static shot -> FAIL
  * a genuine cut (all following frames change) -> no FAIL
  * a clean static shot -> PASS

Synthetic clips are built with ffmpeg lavfi concat; the tests skip when
ffmpeg is unavailable. No real render is touched.

Run:
    python tests/test_flash_frame.py
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

FPS = 24
HAVE_FFMPEG = shutil.which("ffmpeg") is not None


def _clip(path, parts):
    """Build an mp4 from lavfi colour parts: [(colour, seconds), ...]."""
    cmd = ["ffmpeg", "-y", "-nostdin", "-loglevel", "error"]
    for colour, secs in parts:
        cmd += ["-f", "lavfi", "-i",
                "color=c=%s:s=320x180:r=%d:d=%s" % (colour, FPS, secs)]
    n = len(parts)
    graph = "".join("[%d:v]" % k for k in range(n))
    graph += "concat=n=%d:v=1:a=0[out]" % n
    cmd += ["-filter_complex", graph, "-map", "[out]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)]
    proc = subprocess.run(cmd, capture_output=True, timeout=120)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace")[:300])
    return path


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg not on PATH")
class TestFlashFrame(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_single_frame_flip_fails(self):
        clip = _clip(self.root / "flash.mp4",
                     [("red", "0.5"), ("blue", "0.041667"), ("red", "0.5")])
        findings = ecc.check_flash(clip, FPS)
        fails = [f for f in findings if f[0] == "FAIL"]
        self.assertEqual(len(fails), 1, findings)
        self.assertEqual(fails[0][1], "flash-frame")
        hits, frames, err = ecc.scan_flash_frames(clip, FPS)
        self.assertIsNone(err)
        self.assertEqual(len(hits), 1, hits)
        self.assertAlmostEqual(hits[0]["t"], 0.5, delta=1.0 / FPS)
        self.assertGreaterEqual(frames, 20)

    def test_two_frame_flip_fails(self):
        clip = _clip(self.root / "flash2.mp4",
                     [("red", "0.5"), ("blue", "0.0833333"), ("red", "0.5")])
        findings = ecc.check_flash(clip, FPS)
        self.assertEqual(findings[0][0], "FAIL", findings)
        hits, frames, err = ecc.scan_flash_frames(clip, FPS)
        self.assertIsNone(err)
        self.assertEqual(len(hits), 1, hits)
        self.assertEqual(hits[0]["len"], 2, hits)
        self.assertAlmostEqual(hits[0]["t"], 0.5417, delta=2.0 / FPS)

    def test_genuine_cut_is_not_a_flash(self):
        clip = _clip(self.root / "cut.mp4",
                     [("red", "0.5"), ("blue", "0.5")])
        findings = ecc.check_flash(clip, FPS)
        self.assertEqual([f for f in findings if f[0] == "FAIL"], [], findings)
        self.assertEqual(findings[0][1], "flash-frame")
        self.assertEqual(findings[0][0], "PASS")

    def test_static_shot_passes(self):
        clip = _clip(self.root / "static.mp4", [("green", "1.0")])
        findings = ecc.check_flash(clip, FPS)
        self.assertEqual(findings[0][0], "PASS", findings)

    def test_missing_video_fails_closed(self):
        findings = ecc.check_flash(self.root / "nope.mp4", FPS)
        self.assertEqual(findings[0][0], "FAIL")
        self.assertEqual(findings[0][1], "flash-video")

    def test_usage_requires_a_mode(self):
        self.assertEqual(ecc.main(["edit_craft_check.py"]), 2)

    def test_standalone_flash_mode_runs(self):
        clip = _clip(self.root / "standalone.mp4",
                     [("red", "0.5"), ("blue", "0.041667"), ("red", "0.5")])
        rc = ecc.main(["edit_craft_check.py", "--video", str(clip), "--flash"])
        self.assertEqual(rc, 1)  # flash present -> FAIL -> exit 1


if __name__ == "__main__":
    unittest.main()