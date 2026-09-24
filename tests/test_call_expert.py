# -*- coding: utf-8 -*-
"""Unit tests for the on-call expert invoker (src/call_expert.py).

O-20260924-1033-bm-a: pure functions only - registry loading, prompt
assembly, ledger row rendering. No ollama run, real registry never
modified. Chinese appears as \\uXXXX escapes (ASCII rule).

Run:
    python tests/test_call_expert.py
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import call_expert as ce  # noqa: E402


REGISTRY_FIXTURE = {
    "model": "qwen2.5:14b",
    "experts": [
        {"id": "hot-intel", "dept": "\u60c5\u62a5\u90e8",
         "role": "\u70ed\u70b9\u60c5\u62a5\u5b98",
         "prompt_file": "data/experts/prompts/hot-intel.txt"},
        {"id": "S0-topic", "dept": "\u9009\u9898\u7814\u7a76\u90e8",
         "role": "S0 \u9009\u9898\u5b98",
         "prompt_file": "data/experts/prompts/S0-topic.txt",
         "model": "qwen2.5:7b-instruct"},
    ],
}


class TestRegistry(unittest.TestCase):
    def _write(self, d):
        p = Path(d) / "registry.json"
        p.write_text(json.dumps(REGISTRY_FIXTURE, ensure_ascii=False),
                     encoding="utf-8")
        return p

    def test_load_registry_maps_ids(self):
        with tempfile.TemporaryDirectory() as d:
            _, experts = ce.load_registry(self._write(d))
            self.assertEqual({"hot-intel", "S0-topic"}, set(experts))
            self.assertEqual("\u60c5\u62a5\u90e8", experts["hot-intel"]["dept"])

    def test_default_model_falls_back_to_top_level(self):
        with tempfile.TemporaryDirectory() as d:
            _, experts = ce.load_registry(self._write(d))
            self.assertEqual("qwen2.5:14b", experts["hot-intel"]["model"])
            self.assertEqual("qwen2.5:7b-instruct", experts["S0-topic"]["model"])

    def test_bad_registry_raises(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "registry.json"
            p.write_text("not json", encoding="utf-8")
            with self.assertRaises(ValueError):
                ce.load_registry(p)


class TestBuildPrompt(unittest.TestCase):
    def test_prompt_assembles_material_section(self):
        text = ce.build_prompt("\u4f60\u662f\u4e13\u5bb6\u3002\n",
                               "\u6750\u6599\u5185\u5bb9 123")
        self.assertTrue(text.startswith("\u4f60\u662f\u4e13\u5bb6"))
        self.assertIn("===== \u6750\u6599 =====", text)
        self.assertTrue(text.strip().endswith("123"))


class TestLedgerRow(unittest.TestCase):
    def test_row_is_table_shaped_and_sanitized(self):
        row = ce.ledger_row("hot-intel", "\u60c5\u62a5\u5b98",
                            "\u60c5\u62a5\u90e8", "brief.md", 0,
                            "line one\nline two | pipes")
        self.assertTrue(row.startswith("| "))
        self.assertIn("hot-intel", row)
        self.assertIn("| brief.md | 0 |", row)
        self.assertNotIn("\n", row.rstrip("\n"))  # single line
        # newline -> space, pipe -> slash: table stays intact
        self.assertIn("line one line two / pipes", row)
        self.assertNotIn("| pipes", row)  # the raw pipe must be gone

    def test_empty_note_defaults_to_dash(self):
        row = ce.ledger_row("x", "y", "z", "m", 0, "")
        self.assertIn("| - |", row)


if __name__ == "__main__":
    unittest.main(verbosity=2)
