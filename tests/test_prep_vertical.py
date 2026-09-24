# -*- coding: utf-8 -*-
"""Tests for prep_vertical single + batch modes (A5).

Fake subprocess injection only - no real ffmpeg, no network, no repo
files touched; all inputs are zero-byte stubs created in a temp dir.
"""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "render"))

import prep_vertical as pv  # noqa: E402


class FakeCompleted:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def make_fake_run(calls, fail_names=()):
    """Record every cmd; fake ffmpeg writes its output, ffprobe answers."""
    def fake(cmd, capture_output=False, text=False):
        calls.append(list(cmd))
        joined = " ".join(cmd)
        if cmd[0] == "ffprobe":
            return FakeCompleted(0, stdout="width=2048\nheight=1104")
        if any(fn in joined for fn in fail_names):
            return FakeCompleted(1, stderr="boom")
        Path(cmd[-1]).write_bytes(b"x" * 2048)
        return FakeCompleted(0)
    return fake


class BatchModeTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def run_main(self, extra, fail_names=()):
        calls = []
        with mock.patch.object(pv.subprocess, "run",
                               make_fake_run(calls, fail_names)):
            code = pv.main(["--batch", str(self.dir)] + extra)
        return code, calls

    def test_batch_processes_all_videos_once(self):
        (self.dir / "a.mp4").write_bytes(b"")
        (self.dir / "b.mov").write_bytes(b"")
        (self.dir / "notes.txt").write_bytes(b"")
        sub = self.dir / "sub"
        sub.mkdir()
        (sub / "d.mp4").write_bytes(b"")
        code, calls = self.run_main([])
        self.assertEqual(code, 0)
        ffms = [c for c in calls if c[0] == "ffmpeg"]
        self.assertEqual(len(ffms), 2)  # txt + subdir not recursed
        self.assertTrue((self.dir / "a-vertical.mp4").exists())
        self.assertTrue((self.dir / "b-vertical.mp4").exists())

    def test_batch_skip_existing_outputs_idempotent(self):
        (self.dir / "a.mp4").write_bytes(b"")
        (self.dir / "a-vertical.mp4").write_bytes(b"done")
        code, calls = self.run_main([])
        self.assertEqual(code, 0)
        self.assertEqual([c for c in calls if c[0] == "ffmpeg"], [])

    def test_batch_never_takes_suffixed_outputs_as_input(self):
        (self.dir / "a.mp4").write_bytes(b"")
        (self.dir / "orphan-vertical.mp4").write_bytes(b"old output")
        code, calls = self.run_main([])
        self.assertEqual(code, 0)
        ffms = [c for c in calls if c[0] == "ffmpeg"]
        self.assertEqual(len(ffms), 1)
        self.assertIn("a.mp4", " ".join(ffms[0]))

    def test_batch_force_redoes_existing(self):
        (self.dir / "a.mp4").write_bytes(b"")
        (self.dir / "a-vertical.mp4").write_bytes(b"stale")
        code, calls = self.run_main(["--force"])
        self.assertEqual(code, 0)
        self.assertEqual(len([c for c in calls if c[0] == "ffmpeg"]), 1)

    def test_batch_fail_aggregates_to_exit_3(self):
        (self.dir / "good.mp4").write_bytes(b"")
        (self.dir / "bad.mp4").write_bytes(b"")
        code, calls = self.run_main([], fail_names=("bad.mp4",))
        self.assertEqual(code, 3)
        self.assertFalse((self.dir / "bad-vertical.mp4").exists())
        self.assertTrue((self.dir / "good-vertical.mp4").exists())

    def test_batch_custom_suffix_and_canvas(self):
        (self.dir / "a.mp4").write_bytes(b"")
        code, calls = self.run_main(["--suffix", "-16x9",
                                     "--w", "1920", "--h", "1080"])
        self.assertEqual(code, 0)
        self.assertTrue((self.dir / "a-16x9.mp4").exists())
        vf = calls[0][calls[0].index("-vf") + 1]
        self.assertIn("scale=1920:1080", vf)

    def test_batch_missing_dir_exit_2(self):
        code = pv.main(["--batch", str(self.dir / "nope")])
        self.assertEqual(code, 2)

    def test_batch_no_videos_exit_2(self):
        (self.dir / "only.txt").write_bytes(b"")
        self.assertEqual(pv.main(["--batch", str(self.dir)]), 2)


class SingleModeTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_need_exactly_one_of_in_or_batch(self):
        self.assertEqual(pv.main([]), 2)
        self.assertEqual(
            pv.main(["--in", "a.mp4", "--batch", str(self.dir)]), 2)

    def test_single_mode_write_unchanged(self):
        src = self.dir / "raw.mp4"
        src.write_bytes(b"")
        out = self.dir / "v.mp4"
        calls = []
        with mock.patch.object(pv.subprocess, "run",
                               make_fake_run(calls)):
            self.assertEqual(
                pv.main(["--in", str(src), "--out", str(out)]), 0)
        ffms = [c for c in calls if c[0] == "ffmpeg"]
        self.assertEqual(len(ffms), 1)
        self.assertTrue(out.exists())
        self.assertEqual(ffms[0][6], str(src))  # -i position

    def test_single_mode_missing_input_exit_2(self):
        self.assertEqual(
            pv.main(["--in", str(self.dir / "ghost.mp4")]), 2)

    def test_dry_run_probe_no_ffmpeg(self):
        src = self.dir / "raw.mp4"
        src.write_bytes(b"")
        calls = []
        with mock.patch.object(pv.subprocess, "run",
                               make_fake_run(calls)):
            self.assertEqual(pv.main(["--in", str(src)]), 0)
        self.assertEqual([c for c in calls if c[0] == "ffmpeg"], [])
        self.assertEqual(len([c for c in calls if c[0] == "ffprobe"]), 1)


if __name__ == "__main__":
    unittest.main()
