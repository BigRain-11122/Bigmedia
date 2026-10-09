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


class TestVerdictArchive(unittest.TestCase):
    def test_file_name_deterministic(self):
        self.assertEqual("20260924-103300-hot-intel.md",
                         ce.verdict_file_name("hot-intel", "20260924-103300"))
        name = ce.verdict_file_name("S0-topic")
        self.assertTrue(name.endswith("-S0-topic.md"))

    def test_save_verdict_writes_full_text_with_header(self):
        with tempfile.TemporaryDirectory() as d:
            p = ce.save_verdict(Path(d), "x.md", "hot-intel",
                                "\u60c5\u62a5\u5b98", "\u60c5\u62a5\u90e8",
                                "qwen2.5:14b", "brief.md",
                                "\u7ed3\u8bba\u7b2c\u4e00\u884c\n\u7b2c\u4e8c\u884c")
            text = p.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("# hot-intel"))
            self.assertIn("\u60c5\u62a5\u90e8", text)              # dept
            self.assertIn("qwen2.5:14b", text)                     # model
            self.assertIn("brief.md", text)                        # material
            self.assertIn("\u7ed3\u8bba\u7b2c\u4e00\u884c", text)     # full body
            self.assertIn("\u7b2c\u4e8c\u884c", text)              # not truncated


class TestGpuGuardParse(unittest.TestCase):
    """tech#44 pure face: nvidia-smi CSV -> reading dict."""

    def test_parses_first_row(self):
        r = ce.parse_headroom("87, 1400\n12, 9000\n")
        self.assertEqual(87, r["util_pct"])
        self.assertEqual(1400, r["free_mb"])

    def test_single_row(self):
        r = ce.parse_headroom("  5 , 9700 ")
        self.assertEqual(5, r["util_pct"])
        self.assertEqual(9700, r["free_mb"])

    def test_garbage_returns_none(self):
        self.assertIsNone(ce.parse_headroom(""))
        self.assertIsNone(ce.parse_headroom("   \n"))
        self.assertIsNone(ce.parse_headroom("not a csv"))
        self.assertIsNone(ce.parse_headroom("ERR!\n"))


class TestGpuGuardDecision(unittest.TestCase):
    """tech#44 pure face: threshold semantics (strict > / strict <)."""

    def test_none_reading_never_defers(self):
        self.assertEqual((False, ""), ce.defer_decision(None))

    def test_busy_util_defers(self):
        defer, reason = ce.defer_decision({"util_pct": 87, "free_mb": 9000})
        self.assertTrue(defer)
        self.assertIn("87%", reason)

    def test_tight_vram_defers(self):
        defer, reason = ce.defer_decision({"util_pct": 5, "free_mb": 1024})
        self.assertTrue(defer)
        self.assertIn("1024MB", reason)

    def test_headroom_ok_no_defer(self):
        self.assertEqual((False, ""),
                         ce.defer_decision({"util_pct": 60, "free_mb": 9000}))

    def test_boundaries_strict(self):
        # util == 80 and free == 2048 are exactly at threshold: no defer
        self.assertEqual(
            (False, ""),
            ce.defer_decision({"util_pct": 80, "free_mb": 2048}))
        self.assertTrue(ce.defer_decision({"util_pct": 81, "free_mb": 2048})[0])
        self.assertTrue(ce.defer_decision({"util_pct": 80, "free_mb": 2047})[0])


class TestGpuGuardCli(unittest.TestCase):
    """tech#44 wiring face: --gpu-guard defers BEFORE the call;
    --gpu-force overrides; guard off = existing call surface unchanged.
    Everything injected - no ollama, no real registry/ledger writes."""

    def _run_main(self, argv, reading, decision):
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            (repo / "prompts").mkdir()
            (repo / "prompts" / "p.txt").write_text("prompt", encoding="utf-8")
            reg = repo / "registry.json"
            reg.write_text(json.dumps({
                "model": "m",
                "experts": [{"id": "hot-intel", "dept": "d", "role": "r",
                             "prompt_file": "prompts/p.txt"}]}),
                encoding="utf-8")
            mat = repo / "material.md"
            mat.write_text("material body", encoding="utf-8")
            calls = []

            def fake_call_model(model, prompt, timeout=ce.DEFAULT_TIMEOUT):
                calls.append(model)
                return 0, "verdict line"

            patches = [
                mock.patch.object(ce, "REPO", repo),
                # load_registry's default path arg binds at def time, so
                # patch the loader itself with the fixture registry
                mock.patch.object(
                    ce, "load_registry",
                    lambda path=None: ("m", {"hot-intel": {
                        "id": "hot-intel", "dept": "d", "role": "r",
                        "prompt_file": "prompts/p.txt", "model": "m"}})),
                mock.patch.object(ce, "LEDGER", repo / "ledger.md"),
                mock.patch.object(ce, "VERDICT_DIR", repo / "verdicts"),
                mock.patch.object(ce, "read_gpu_headroom", lambda: reading),
                mock.patch.object(ce, "defer_decision",
                                  lambda r, **kw: decision),
                mock.patch.object(ce, "call_model", fake_call_model),
            ]
            with patches[0], patches[1], patches[2], patches[3], \
                    patches[4], patches[5], patches[6]:
                # argv[0] = script path slot (production: sys.argv[0])
                rc = ce.main(["call_expert.py", "--expert", "hot-intel",
                              "--material", str(mat)] + argv)
            return rc, calls

    def test_guard_defers_before_call(self):
        rc, calls = self._run_main(
            ["--gpu-guard"],
            {"util_pct": 87, "free_mb": 1400},
            (True, "gpu util 87% > 80% (occupied window)"))
        self.assertEqual(5, rc)
        self.assertEqual([], calls)  # zero model flights burned

    def test_force_override_flies(self):
        rc, calls = self._run_main(
            ["--gpu-guard", "--gpu-force"],
            {"util_pct": 87, "free_mb": 1400}, (True, "busy"))
        self.assertEqual(0, rc)
        self.assertEqual(["m"], calls)

    def test_guard_probe_unavailable_proceeds(self):
        rc, calls = self._run_main(["--gpu-guard"], None, (False, ""))
        self.assertEqual(0, rc)
        self.assertEqual(["m"], calls)

    def test_guard_off_busy_gpu_still_flies(self):
        # existing wrapper/CLI surface: no flag -> behavior unchanged
        rc, calls = self._run_main(
            [], {"util_pct": 87, "free_mb": 1400}, (True, "busy"))
        self.assertEqual(0, rc)
        self.assertEqual(["m"], calls)


if __name__ == "__main__":
    unittest.main(verbosity=2)
