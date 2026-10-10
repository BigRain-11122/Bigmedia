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
from datetime import datetime
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
                mock.patch.object(ce, "DEFER_LEDGER",
                                  repo / "defer-ledger.jsonl"),
                mock.patch.object(ce, "read_gpu_headroom", lambda: reading),
                mock.patch.object(ce, "defer_decision",
                                  lambda r, **kw: decision),
                mock.patch.object(ce, "call_model", fake_call_model),
            ]
            with patches[0], patches[1], patches[2], patches[3], \
                    patches[4], patches[5], patches[6], patches[7]:
                # argv[0] = script path slot (production: sys.argv[0])
                rc = ce.main(["call_expert.py", "--expert", "hot-intel",
                              "--material", str(mat)] + argv)
            # capture defer rows inside the tmpdir lifetime (tech#89)
            self.defer_rows = []
            dl = repo / "defer-ledger.jsonl"
            if dl.exists():
                for ln in dl.read_text(encoding="utf-8").splitlines():
                    if ln.strip():
                        self.defer_rows.append(json.loads(ln))
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

    def test_defer_lands_one_jsonl_row(self):
        # tech#89 telemetry: the defer event itself lands as one row
        # (R1943 anchor: defers were previously invisible outside the
        # hand-written round log).
        self.defer_rows = []
        rc, calls = self._run_main(
            ["--gpu-guard"],
            {"util_pct": 87, "free_mb": 1400},
            (True, "gpu util 87% > 80% (occupied window)"))
        self.assertEqual(5, rc)
        self.assertEqual(1, len(self.defer_rows))
        row = self.defer_rows[0]
        self.assertEqual(row["event"], "defer")
        self.assertEqual(row["expert"], "hot-intel")
        self.assertEqual(row["rc"], 5)
        self.assertEqual(row["util_pct"], 87)
        self.assertEqual(row["free_mb"], 1400)
        self.assertEqual(row["reason"],
                         "gpu util 87% > 80% (occupied window)")
        self.assertIn("material", row)
        self.assertIn("ts", row)

    def test_no_defer_no_row(self):
        self.defer_rows = []
        rc, _ = self._run_main(["--gpu-guard"],
                               {"util_pct": 5, "free_mb": 9000},
                               (False, ""))
        self.assertEqual(0, rc)
        self.assertEqual([], self.defer_rows)

    def test_force_override_writes_no_defer_row(self):
        self.defer_rows = []
        rc, _ = self._run_main(
            ["--gpu-guard", "--gpu-force"],
            {"util_pct": 87, "free_mb": 1400}, (True, "busy"))
        self.assertEqual(0, rc)
        self.assertEqual([], self.defer_rows)


class TestDeferLedger(unittest.TestCase):
    """tech#89 pure face: defer_row exact field set + best-effort
    append (tech#19/52 law: write failure never blocks the defer)."""

    def test_row_exact_field_set(self):
        row = ce.defer_row("E4-audience", "m/e4-material.md",
                           "gpu free 231MB < 2048MB",
                           {"util_pct": 100, "free_mb": 231},
                           now=datetime(2026, 10, 11, 5, 26, 3))
        payload = json.loads(row)
        self.assertEqual(set(payload), {
            "ts", "event", "expert", "material", "reason",
            "util_pct", "free_mb", "rc"})
        self.assertEqual(payload["ts"], "2026-10-11 05:26:03")
        self.assertEqual(payload["event"], "defer")
        self.assertEqual(payload["rc"], 5)

    def test_row_none_reading_nulls(self):
        row = ce.defer_row("hot-intel", "m.md", "r", None)
        payload = json.loads(row)
        self.assertIsNone(payload["util_pct"])
        self.assertIsNone(payload["free_mb"])

    def test_append_best_effort_true_then_false(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sub" / "defer.jsonl"
            self.assertTrue(ce.append_defer_row("{}", path))
            self.assertTrue(path.exists())
            # a directory target fails -> False, never raises
            dir_target = Path(td) / "adir"
            dir_target.mkdir()
            self.assertFalse(ce.append_defer_row("{}", dir_target))


class TestTimeoutCli(unittest.TestCase):
    """tech#45 wiring face: --timeout S passes to call_model; default
    stays 300 (existing surface unchanged); bad values rejected before
    any model flight. Everything injected - no ollama, no real
    registry/ledger writes."""

    def _run_main(self, argv):
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            (repo / "prompts").mkdir()
            (repo / "prompts" / "p.txt").write_text("prompt", encoding="utf-8")
            mat = repo / "material.md"
            mat.write_text("material body", encoding="utf-8")
            captured = []

            def fake_call_model(model, prompt, timeout=ce.DEFAULT_TIMEOUT):
                captured.append(timeout)
                return 0, "verdict line"

            patches = [
                mock.patch.object(ce, "REPO", repo),
                mock.patch.object(
                    ce, "load_registry",
                    lambda path=None: ("m", {"hot-intel": {
                        "id": "hot-intel", "dept": "d", "role": "r",
                        "prompt_file": "prompts/p.txt", "model": "m"}})),
                mock.patch.object(ce, "LEDGER", repo / "ledger.md"),
                mock.patch.object(ce, "VERDICT_DIR", repo / "verdicts"),
                mock.patch.object(ce, "call_model", fake_call_model),
            ]
            with patches[0], patches[1], patches[2], patches[3], \
                    patches[4]:
                rc = ce.main(["call_expert.py", "--expert", "hot-intel",
                              "--material", str(mat)] + argv)
            return rc, captured

    def test_timeout_flag_passes_value(self):
        # the R176/R1847 long-review case: cap raised without a wrapper
        rc, captured = self._run_main(["--timeout", "1500"])
        self.assertEqual(0, rc)
        self.assertEqual([1500], captured)

    def test_default_timeout_unchanged_without_flag(self):
        # existing wrapper/CLI surface: no flag -> DEFAULT_TIMEOUT
        rc, captured = self._run_main([])
        self.assertEqual(0, rc)
        self.assertEqual([ce.DEFAULT_TIMEOUT], captured)
        self.assertEqual(300, ce.DEFAULT_TIMEOUT)

    def test_non_integer_rejected_before_flight(self):
        rc, captured = self._run_main(["--timeout", "1500s"])
        self.assertEqual(2, rc)
        self.assertEqual([], captured)

    def test_non_positive_rejected(self):
        for bad in ("0", "-5"):
            rc, captured = self._run_main(["--timeout", bad])
            self.assertEqual(2, rc)
            self.assertEqual([], captured)

    def test_missing_value_rejected_gracefully(self):
        # trailing --timeout with no value: exit 2, no IndexError crash
        rc, captured = self._run_main(["--timeout"])
        self.assertEqual(2, rc)
        self.assertEqual([], captured)

    def test_guard_and_timeout_combine(self):
        # long-flight正法: --timeout 1500 --gpu-guard both honored,
        # guard probe unavailable -> proceeds with raised cap
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            (repo / "prompts").mkdir()
            (repo / "prompts" / "p.txt").write_text("prompt",
                                                    encoding="utf-8")
            mat = repo / "material.md"
            mat.write_text("material body", encoding="utf-8")
            captured = []

            def fake_call_model(model, prompt, timeout=ce.DEFAULT_TIMEOUT):
                captured.append(timeout)
                return 0, "verdict line"

            patches = [
                mock.patch.object(ce, "REPO", repo),
                mock.patch.object(
                    ce, "load_registry",
                    lambda path=None: ("m", {"hot-intel": {
                        "id": "hot-intel", "dept": "d", "role": "r",
                        "prompt_file": "prompts/p.txt", "model": "m"}})),
                mock.patch.object(ce, "LEDGER", repo / "ledger.md"),
                mock.patch.object(ce, "VERDICT_DIR", repo / "verdicts"),
                mock.patch.object(ce, "read_gpu_headroom", lambda: None),
                mock.patch.object(ce, "call_model", fake_call_model),
            ]
            with patches[0], patches[1], patches[2], patches[3], \
                    patches[4], patches[5]:
                rc = ce.main(["call_expert.py", "--expert", "hot-intel",
                              "--material", str(mat),
                              "--timeout", "1500", "--gpu-guard"])
            self.assertEqual(0, rc)
            self.assertEqual([1500], captured)


    def test_timeout_branch_prints_custom_value(self):
        # the enforce face: TimeoutExpired lands in the branch and the
        # message echoes the CLI-passed cap, not the hardcoded default.
        # Fail path stays zero-pollution: no verdict archive, no ledger.
        import contextlib
        import io
        import subprocess as sp
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            (repo / "prompts").mkdir()
            (repo / "prompts" / "p.txt").write_text("prompt", encoding="utf-8")
            mat = repo / "material.md"
            mat.write_text("material body", encoding="utf-8")

            def fake_call_model(model, prompt, timeout=ce.DEFAULT_TIMEOUT):
                raise sp.TimeoutExpired(cmd="ollama", timeout=timeout)

            patches = [
                mock.patch.object(ce, "REPO", repo),
                mock.patch.object(
                    ce, "load_registry",
                    lambda path=None: ("m", {"hot-intel": {
                        "id": "hot-intel", "dept": "d", "role": "r",
                        "prompt_file": "prompts/p.txt", "model": "m"}})),
                mock.patch.object(ce, "LEDGER", repo / "ledger.md"),
                mock.patch.object(ce, "VERDICT_DIR", repo / "verdicts"),
                mock.patch.object(ce, "call_model", fake_call_model),
            ]
            buf = io.StringIO()
            with patches[0], patches[1], patches[2], patches[3], \
                    patches[4], contextlib.redirect_stdout(buf):
                rc = ce.main(["call_expert.py", "--expert", "hot-intel",
                              "--material", str(mat),
                              "--timeout", "1500"])
            self.assertEqual(3, rc)
            self.assertIn("FAIL ollama timeout (1500s)", buf.getvalue())
            self.assertFalse((repo / "ledger.md").exists())
            self.assertFalse((repo / "verdicts").exists())


class E4AudienceSeatTests(unittest.TestCase):
    """tech#46: E4-audience reference seat registration integrity.

    E seats sit outside the department roster (R174 lineage); this seat
    is the audience reference instrument from dept-review-mechanism S6
    (E4 dual-state: dev-phase Ollama reading, non-intercepting). Checks
    are read-only against the REAL registry + prompt data files.
    """

    def test_seat_in_real_registry(self):
        _, experts = ce.load_registry()
        self.assertIn("E4-audience", experts)
        seat = experts["E4-audience"]
        # dept annotation marks the non-departmental reference seat
        self.assertEqual(
            "\u8bc4\u5ba1\u53c2\u8003\u5e2d\uff08\u975e\u90e8\u95e8\u7f16\u5236\uff09",
            seat["dept"])
        self.assertEqual("E4 \u76f4\u89c9\u89c2\u4f17\u53c2\u8003\u4eea",
                         seat["role"])
        # model falls back to the registry default (qwen2.5:14b)
        self.assertNotEqual("", seat["model"])

    def test_prompt_file_exists_with_core_clauses(self):
        _, experts = ce.load_registry()
        path = REPO / experts["E4-audience"]["prompt_file"]
        self.assertTrue(path.exists(), "prompt file missing: %s" % path)
        text = path.read_text(encoding="utf-8")
        # non-intercepting reference seat (E4 dual-state law)
        self.assertIn("\u975e\u62e6\u622a\u53c2\u8003\u5e2d", text)
        # material contract block (platform+form line first)
        self.assertIn("\u5e73\u53f0\u4e0e\u5f62\u6001", text)
        # the three-question core from the wrapper lineage
        self.assertIn("\u6253\u51e0\u5206\uff080-10\uff09", text)
        self.assertIn("\u6700\u5f31\u7684\u4e00\u9879", text)
        # evidence law (verbatim quote anchor)
        self.assertIn("\u5b9e\u9524\u5f8b", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
