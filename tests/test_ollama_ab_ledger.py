# -*- coding: utf-8 -*-
"""Tests for src/os/ollama_ab_ledger.py (state/queue/tech#119)."""

import datetime
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "os"))

import ollama_ab_ledger as abl  # noqa: E402


class TestAppendAbRow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.path = os.path.join(self.tmp, "nested", "ollama-ab-ledger.jsonl")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _read_rows(self):
        with io.open(self.path, "r", encoding="utf-8") as fh:
            return [json.loads(x) for x in fh.read().splitlines() if x]

    def test_row_shape_and_defaults(self):
        ok = abl.append_ab_row("prefilter-ab", "qwen2.5:14b-8k", 0,
                               path=self.path,
                               when=datetime.datetime(2026, 10, 12, 3, 20, 0))
        self.assertTrue(ok)
        rows = self._read_rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], {
            "ts": "2026-10-12 03:20:00",
            "purpose": "prefilter-ab",
            "model": "qwen2.5:14b-8k",
            "rc": 0,
        })
        # n/note omitted when not provided (tech#52 optional-column law).
        self.assertNotIn("n", rows[0])
        self.assertNotIn("note", rows[0])

    def test_optional_n_and_note_included(self):
        ok = abl.append_ab_row("score-ab", "qwen2.5:14b-8k", 3, n=7,
                               note="cand arm item 7 timeout",
                               path=self.path,
                               when=datetime.datetime(2026, 10, 12, 3, 21, 0))
        self.assertTrue(ok)
        row = self._read_rows()[0]
        self.assertEqual(row["n"], 7)
        self.assertEqual(row["note"], "cand arm item 7 timeout")
        self.assertEqual(row["rc"], 3)

    def test_parent_dir_autocreated_and_order_kept(self):
        self.assertFalse(os.path.isdir(os.path.dirname(self.path)))
        abl.append_ab_row("ab", "m", 0, n=1, path=self.path)
        abl.append_ab_row("ab", "m", 1, n=2, path=self.path)
        rows = self._read_rows()
        self.assertEqual([r["n"] for r in rows], [1, 2])

    def test_best_effort_never_raises(self):
        # A path whose parent is a *file* makes makedirs/open fail; the
        # metering helper must WARN and return False, never raise.
        blocker = os.path.join(self.tmp, "blocker")
        with io.open(blocker, "w", encoding="utf-8") as fh:
            fh.write("x")
        bad = os.path.join(blocker, "sub", "ledger.jsonl")
        self.assertFalse(abl.append_ab_row("ab", "m", 0, path=bad))
        self.assertFalse(os.path.exists(bad))


if __name__ == "__main__":
    unittest.main()
