# -*- coding: utf-8 -*-
"""Unit tests for the on-call expert invoker (src/call_expert.py).

O-20260924-1033-bm-a: pure functions only - registry loading, prompt
assembly, ledger row rendering. No ollama run, real registry never
modified. Chinese appears as \\uXXXX escapes (ASCII rule).

Run:
    python tests/test_call_expert.py
"""
import contextlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import call_expert as ce  # noqa: E402


def _enter_all(patches):
    """Start every patch in one list (R2428: the hand-written
    `with patches[0], ..., patches[5]` chains silently stopped applying
    once a new patch was inserted mid-list). Returns the ExitStack so
    the caller keeps its usual `with _enter_all(patches):` block."""
    stk = contextlib.ExitStack()
    for p in patches:
        stk.enter_context(p)
    return stk


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
                mock.patch.object(ce, "NOT_EXECUTED_LEDGER",
                                  repo / "not-executed.jsonl"),
                mock.patch.object(ce, "VERDICT_DIR", repo / "verdicts"),
                mock.patch.object(ce, "DEFER_LEDGER",
                                  repo / "defer-ledger.jsonl"),
                mock.patch.object(ce, "read_gpu_headroom", lambda: reading),
                mock.patch.object(ce, "defer_decision",
                                  lambda r, **kw: decision),
                mock.patch.object(ce, "call_model", fake_call_model),
            ]
            with _enter_all(patches):
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


class TestWedgeProbeCli(unittest.TestCase):
    """tech#120 wiring face: --wedge-probe micro-bails BEFORE the main
    flight when the ollama generation face is wedged; probe itself
    never lands in expert-calls; flag off = existing surface unchanged.
    Everything injected - no ollama, no real registry/ledger writes."""

    def _run_main(self, argv, probe_behavior):
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            (repo / "prompts").mkdir()
            (repo / "prompts" / "p.txt").write_text("prompt", encoding="utf-8")
            mat = repo / "material.md"
            mat.write_text("material body", encoding="utf-8")
            calls = []

            def fake_call_model(model, prompt, timeout=ce.DEFAULT_TIMEOUT):
                calls.append((model, timeout))
                if model == ce.WEDGE_PROBE_MODEL:
                    return probe_behavior()
                return 0, "verdict line"

            patches = [
                mock.patch.object(ce, "REPO", repo),
                mock.patch.object(
                    ce, "load_registry",
                    lambda path=None: ("m", {"hot-intel": {
                        "id": "hot-intel", "dept": "d", "role": "r",
                        "prompt_file": "prompts/p.txt", "model": "m"}})),
                mock.patch.object(ce, "LEDGER", repo / "ledger.md"),
                mock.patch.object(ce, "NOT_EXECUTED_LEDGER",
                                  repo / "not-executed.jsonl"),
                mock.patch.object(ce, "VERDICT_DIR", repo / "verdicts"),
                mock.patch.object(ce, "DEFER_LEDGER",
                                  repo / "defer-ledger.jsonl"),
                mock.patch.object(ce, "call_model", fake_call_model),
            ]
            import io
            import contextlib
            buf = io.StringIO()
            with _enter_all(patches):
                with contextlib.redirect_stdout(buf):
                    rc = ce.main(["call_expert.py", "--expert", "hot-intel",
                                  "--material", str(mat)] + argv)
            ledger_rows = 0
            lg = repo / "ledger.md"
            if lg.exists():
                for ln in lg.read_text(encoding="utf-8").splitlines():
                    if re.match(r"^\| \d{4}-\d{2}-\d{2} ", ln):
                        ledger_rows += 1
            return rc, calls, buf.getvalue(), ledger_rows

    def test_wedge_timeout_bails_fast(self):
        # R2012/R2013 anchor: a wedged ollama burns the whole cap with
        # zero verdicts; the probe converts that into a <=90s bail.
        def timeout_probe():
            raise subprocess.TimeoutExpired(
                cmd="ollama", timeout=ce.WEDGE_PROBE_CAP)
        rc, calls, out, rows = self._run_main(
            ["--wedge-probe"], timeout_probe)
        self.assertEqual(6, rc)
        self.assertEqual([(ce.WEDGE_PROBE_MODEL, ce.WEDGE_PROBE_CAP)],
                         calls)  # zero main flights burned
        self.assertIn("WEDGE-FAIL", out)
        # tech#377 (R2428): the probe itself still never lands as a
        # call, but the bail is no longer silent - one NOT-EXECUTED
        # ledger row records that the seat never ran.
        self.assertEqual(1, rows)
        self.assertIn("NOT-EXECUTED", out)

    def test_wedge_probe_nonzero_rc_bails(self):
        rc, calls, out, rows = self._run_main(
            ["--wedge-probe"], lambda: (1, "boom"))
        self.assertEqual(6, rc)
        self.assertEqual([(ce.WEDGE_PROBE_MODEL, ce.WEDGE_PROBE_CAP)],
                         calls)
        self.assertIn("WEDGE-FAIL", out)
        self.assertEqual(1, rows)
        self.assertIn("NOT-EXECUTED", out)

    def test_wedge_probe_ok_then_main_flight(self):
        rc, calls, out, rows = self._run_main(
            ["--wedge-probe"], lambda: (0, "OK"))
        self.assertEqual(0, rc)
        self.assertEqual([(ce.WEDGE_PROBE_MODEL, ce.WEDGE_PROBE_CAP),
                          ("m", ce.DEFAULT_TIMEOUT)], calls)
        self.assertIn("WEDGE-OK", out)
        self.assertEqual(1, rows)  # main call landed, probe did not

    def test_flag_off_zero_probe_flights(self):
        rc, calls, out, rows = self._run_main([], lambda: (0, "OK"))
        self.assertEqual(0, rc)
        self.assertEqual([("m", ce.DEFAULT_TIMEOUT)], calls)
        self.assertNotIn("WEDGE-", out)

    def test_wedge_probe_respects_custom_main_timeout(self):
        # staged launchers fly --timeout 1500; the probe cap must stay
        # at WEDGE_PROBE_CAP (240s, O-20261015-1335 17G flagship
        # cold-load envelope), not inherit the main cap.
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            (repo / "prompts").mkdir()
            (repo / "prompts" / "p.txt").write_text("p", encoding="utf-8")
            mat = repo / "m.md"
            mat.write_text("body", encoding="utf-8")
            seen = []

            def fake(model, prompt, timeout=ce.DEFAULT_TIMEOUT):
                seen.append((model, timeout))
                return 0, "OK"

            patches = [
                mock.patch.object(ce, "REPO", repo),
                mock.patch.object(
                    ce, "load_registry",
                    lambda path=None: ("m", {"hot-intel": {
                        "id": "hot-intel", "dept": "d", "role": "r",
                        "prompt_file": "prompts/p.txt", "model": "m"}})),
                mock.patch.object(ce, "LEDGER", repo / "l.md"),
                mock.patch.object(ce, "NOT_EXECUTED_LEDGER",
                                  repo / "ne.jsonl"),
                mock.patch.object(ce, "VERDICT_DIR", repo / "v"),
                mock.patch.object(ce, "DEFER_LEDGER", repo / "d.jsonl"),
                mock.patch.object(ce, "call_model", fake),
            ]
            import io
            import contextlib
            buf = io.StringIO()
            with _enter_all(patches):
                with contextlib.redirect_stdout(buf):
                    rc = ce.main(["call_expert.py", "--expert", "hot-intel",
                                  "--material", str(mat), "--timeout", "1500",
                                  "--wedge-probe"])
            self.assertEqual(0, rc)
            self.assertEqual([(ce.WEDGE_PROBE_MODEL, ce.WEDGE_PROBE_CAP),
                              ("m", 1500)], seen)


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
                mock.patch.object(ce, "NOT_EXECUTED_LEDGER",
                                  repo / "not-executed.jsonl"),
                mock.patch.object(ce, "VERDICT_DIR", repo / "verdicts"),
                mock.patch.object(ce, "call_model", fake_call_model),
            ]
            with _enter_all(patches):
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
        self.assertEqual(600, ce.DEFAULT_TIMEOUT)  # O-20261015-1335: 17G flagship funds 300->600

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
                mock.patch.object(ce, "NOT_EXECUTED_LEDGER",
                                  repo / "not-executed.jsonl"),
                mock.patch.object(ce, "VERDICT_DIR", repo / "verdicts"),
                mock.patch.object(ce, "read_gpu_headroom", lambda: None),
                mock.patch.object(ce, "call_model", fake_call_model),
            ]
            with _enter_all(patches):
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
                mock.patch.object(ce, "NOT_EXECUTED_LEDGER",
                                  repo / "not-executed.jsonl"),
                mock.patch.object(ce, "VERDICT_DIR", repo / "verdicts"),
                mock.patch.object(ce, "call_model", fake_call_model),
            ]
            buf = io.StringIO()
            with _enter_all(patches), contextlib.redirect_stdout(buf):
                rc = ce.main(["call_expert.py", "--expert", "hot-intel",
                              "--material", str(mat),
                              "--timeout", "1500"])
            self.assertEqual(3, rc)
            self.assertIn("FAIL model call timeout (1500s)", buf.getvalue())
            # tech#377 (R2428): a dead seat leaves a trace instead of
            # vanishing - still zero verdict archive, but one
            # NOT-EXECUTED row on both faces (ledger + JSONL).
            self.assertFalse((repo / "verdicts").exists())
            lg = (repo / "ledger.md").read_text(encoding="utf-8")
            self.assertIn("NOT-EXECUTED", lg)
            self.assertIn("| 3 |", lg)
            ne = [json.loads(ln) for ln in
                  (repo / "not-executed.jsonl").read_text(
                      encoding="utf-8").splitlines() if ln.strip()]
            self.assertEqual(1, len(ne))
            self.assertEqual("NOT-EXECUTED", ne[0]["mark"])
            self.assertEqual(3, ne[0]["rc"])
            self.assertIn("timeout", ne[0]["reason"])


class TestNotExecutedTrace(unittest.TestCase):
    """tech#377 (R2428): a seat that never ran must leave a trace on
    both faces - the human ledger and the JSONL readiness reads."""

    def test_row_field_set(self):
        row = ce.not_executed_row(
            "S4-compliance", "data/drafts/20261024-BS-006-\u516c\u4f17\u53f7.md",
            "brain /health unreachable", 3,
            now=datetime(2026, 10, 24, 5, 1, 2))
        payload = json.loads(row)
        self.assertEqual("NOT-EXECUTED", payload["mark"])
        self.assertEqual("2026-10-24 05:01:02", payload["ts"])
        self.assertEqual(3, payload["rc"])
        self.assertEqual("S4-compliance", payload["expert"])
        self.assertIn("unreachable", payload["reason"])

    def test_append_best_effort(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "sub" / "ne.jsonl"
            self.assertTrue(ce.append_not_executed("{}", path))
            self.assertEqual(1, len(path.read_text(
                encoding="utf-8").splitlines()))
            # directory target = write failure, never an exception
            self.assertFalse(ce.append_not_executed("{}", Path(td)))

    def test_record_writes_both_faces(self):
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "expert-calls.md"
            jsonl = Path(td) / "ne.jsonl"
            ok = ce.record_not_executed(
                "S4-compliance", "S4 \u5408\u89c4\u5e2d", "\u5408\u89c4\u5ba1\u67e5\u90e8",
                "data/drafts/m.md", "brain /health unreachable", 3,
                ledger=ledger, jsonl=jsonl)
            self.assertEqual((True, True), ok)
            text = ledger.read_text(encoding="utf-8")
            self.assertIn("| 3 |", text)
            self.assertIn("NOT-EXECUTED", text)
            # header created on first write, not duplicated
            ce.record_not_executed("S4-compliance", "r", "d", "m", "again",
                                   3, ledger=ledger, jsonl=jsonl)
            self.assertEqual(1, ledger.read_text(
                encoding="utf-8").count("| \u65f6\u95f4 |"))
            self.assertEqual(2, len(jsonl.read_text(
                encoding="utf-8").splitlines()))


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


class TestBrainWireTransport(unittest.TestCase):
    """tech#186: call_model flies the :8090 OpenAI wire. Hermetic --
    brain_health_ok and urllib.request.urlopen are both injected; no
    live server is ever contacted (mock.patch saves/restores the real
    module members, so the tech#175 double-key teardown is not needed
    here)."""

    def setUp(self):
        patcher = mock.patch.object(ce, "brain_health_ok",
                                    return_value=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    @staticmethod
    def _fake_response(payload_bytes):
        resp = mock.MagicMock()
        resp.__enter__.return_value.read.return_value = payload_bytes
        resp.__exit__.return_value = False
        return resp

    def test_wire_flight_posts_openai_shape(self):
        import urllib.request as urlreq
        captured = {}

        def fake_urlopen(request, timeout=None):
            captured["url"] = request.full_url
            captured["data"] = json.loads(request.data.decode("utf-8"))
            captured["timeout"] = timeout
            body = {"choices": [{"message": {"content": "\u7ed3\u8bba"}}]}
            return self._fake_response(
                json.dumps(body).encode("utf-8"))

        with mock.patch.object(urlreq, "urlopen",
                               side_effect=fake_urlopen):
            code, out = ce.call_model("qwen3.6-35b", "ping",
                                      timeout=123)
        self.assertEqual(0, code)
        self.assertEqual("\u7ed3\u8bba", out)
        self.assertEqual(ce.BRAIN_URL, captured["url"])
        self.assertEqual(123, captured["timeout"])
        payload = captured["data"]
        self.assertEqual("qwen3.6-35b", payload["model"])
        self.assertFalse(payload["stream"])
        self.assertEqual([{"role": "user", "content": "ping"}],
                         payload["messages"])
        self.assertEqual({"enable_thinking": False},
                         payload["chat_template_kwargs"])

    def test_liveness_fail_short_circuits_before_flight(self):
        import urllib.request as urlreq
        with mock.patch.object(ce, "brain_health_ok",
                               return_value=False):

            def boom(request, timeout=None):
                raise AssertionError("no flight expected on dead lane")

            with mock.patch.object(urlreq, "urlopen",
                                   side_effect=boom):
                code, out = ce.call_model("qwen3.6-35b", "ping")
        self.assertEqual(3, code)
        self.assertIn("unreachable", out)

    def test_transport_timeout_reads_rc3(self):
        import urllib.request as urlreq
        with mock.patch.object(urlreq, "urlopen",
                               side_effect=OSError("timed out")):
            code, out = ce.call_model("qwen3.6-35b", "ping",
                                      timeout=77)
        self.assertEqual(3, code)
        self.assertIn("timeout", out)
        self.assertIn("77", out)

    def test_transport_error_reads_rc3(self):
        import urllib.request as urlreq
        with mock.patch.object(
                urlreq, "urlopen",
                side_effect=OSError("connection refused")):
            code, out = ce.call_model("qwen3.6-35b", "ping")
        self.assertEqual(3, code)
        self.assertIn("transport error", out)
        self.assertIn("connection refused", out)

    def test_empty_choices_read_as_empty_verdict(self):
        import urllib.request as urlreq
        with mock.patch.object(
                urlreq, "urlopen",
                return_value=self._fake_response(b'{"choices": []}')):
            code, out = ce.call_model("qwen3.6-35b", "ping")
        self.assertEqual(0, code)
        self.assertEqual("", out)

    def test_wedge_probe_model_follows_brain_default(self):
        self.assertEqual(ce.BRAIN_DEFAULT_MODEL, ce.WEDGE_PROBE_MODEL)

    def test_health_url_derives_from_brain_base(self):
        self.assertTrue(ce.BRAIN_HEALTH_URL.endswith("/health"))
        base = ce.BRAIN_HEALTH_URL[:-len("/health")]
        self.assertTrue(ce.BRAIN_URL.startswith(base))

    def test_health_url_override_wins(self):
        # tech#379: a provider without /health still has to be probeable.
        self.assertEqual(
            "http://127.0.0.1:11434/",
            ce.resolve_health_url(
                "http://127.0.0.1:11434/v1/chat/completions",
                "http://127.0.0.1:11434/"))

    def test_health_url_default_from_base(self):
        self.assertEqual(
            "http://127.0.0.1:8090/health",
            ce.resolve_health_url(
                "http://127.0.0.1:8090/v1/chat/completions"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
