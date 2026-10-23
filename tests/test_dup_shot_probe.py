# -*- coding: utf-8 -*-
"""Unit tests for the duplicate-shot probe (backlog#118 C item, R2419).

The probe answers one question the pop/flash faces cannot: does a shot that
comes back later in the film come back reframed, or identical? These tests
pin the two mechanical pieces that decide it:

  * sim() must score a shifted-brightness copy as identical (framing, not
    colour, is what is being compared) and unrelated noise as low
  * centre_crop_zoom() must actually crop-then-resample, so a 1.34x
    push-in of the same frame scores high against itself

No ffmpeg and no real render: pure numpy, so it runs anywhere.

Run:
    python tests/test_dup_shot_probe.py
"""
import sys
import unittest
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import mv_dup_shot_probe as probe  # noqa: E402


def _frame(seed=0):
    rng = np.random.default_rng(seed)
    return rng.integers(0, 256, size=(136, 240, 3), dtype=np.uint8)


class TestSim(unittest.TestCase):
    def test_same_framing_different_exposure_scores_high(self):
        a = _frame(1)
        b = np.clip(a.astype(np.int16) + 25, 0, 255).astype(np.uint8)
        ga, gb = probe.block_grid(a), probe.block_grid(b)
        self.assertGreater(probe.sim(ga, gb), 0.99)

    def test_unrelated_frames_score_low(self):
        ga = probe.block_grid(_frame(2))
        gb = probe.block_grid(_frame(3))
        self.assertLess(probe.sim(ga, gb), 0.5)

    def test_flat_frame_scores_zero_not_nan(self):
        flat = np.full((136, 240, 3), 40, dtype=np.uint8)
        g = probe.block_grid(flat)
        self.assertEqual(probe.sim(g, g), 0.0)


class TestZoom(unittest.TestCase):
    def test_zoom_keeps_shape(self):
        out = probe.centre_crop_zoom(_frame(4), 1.34)
        self.assertEqual(out.shape, (136, 240, 3))

    def test_zoom_changes_framing(self):
        a = _frame(5)
        ga = probe.block_grid(a)
        gz = probe.block_grid(probe.centre_crop_zoom(a, 1.34))
        self.assertLess(probe.sim(ga, gz), 0.9)


class TestShots(unittest.TestCase):
    def test_shots_from_cuts_covers_every_frame(self):
        shots = probe.shots_from_cuts([10, 40], 100)
        self.assertEqual(shots, [(0, 11), (11, 41), (41, 100)])

    def test_shots_from_cuts_without_cuts(self):
        self.assertEqual(probe.shots_from_cuts([], 50), [(0, 50)])


if __name__ == "__main__":
    unittest.main(verbosity=2)