"""Minimal unit tests for the M4 machine gate (src/draft_lint.py).

Fixture drafts live in tests/fixtures/ - fake content only. The real
drafts under data/drafts/ are never touched (production pause, CEO
order O-20260923-1525-bm-a). Chinese lives in the fixture data files;
this script stays ASCII per the repo encoding rule (filenames come
from manifest.json, never hardcoded here).

Run:
    python tests/test_draft_lint.py
"""
import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import draft_lint  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MANIFEST = json.loads((FIXTURES / "manifest.json").read_text(encoding="utf-8"))


def lint_fixture(key):
    return draft_lint.lint_file(FIXTURES / MANIFEST[key])


def fail_codes(findings):
    return {code for sev, code, _ in findings if sev == "FAIL"}


def warn_codes(findings):
    return {code for sev, code, _ in findings if sev == "WARN"}


class MasterDraftTests(unittest.TestCase):
    def test_baseline_has_no_findings(self):
        findings, stats = lint_fixture("master_baseline")
        self.assertEqual(fail_codes(findings), set())
        self.assertEqual(warn_codes(findings), set())
        self.assertGreater(stats["body_chars"], 0)

    def test_missing_section_and_empty_sources_fail(self):
        findings, _ = lint_fixture("master_bad_structure")
        self.assertEqual(fail_codes(findings), {"structure", "sources"})

    def test_missing_aigc_disclosure_fails(self):
        findings, _ = lint_fixture("master_no_aigc_disclosure")
        self.assertEqual(fail_codes(findings), {"aigc"})

    def test_quant_claims_need_disclaimer(self):
        findings, _ = lint_fixture("master_quant_no_disclaimer")
        self.assertEqual(fail_codes(findings), {"disclaimer"})

    def test_quant_claims_with_disclaimer_pass(self):
        findings, _ = lint_fixture("master_quant_with_disclaimer")
        self.assertEqual(fail_codes(findings), set())

    def test_gate_verdict_needs_date_and_reviewer(self):
        findings, _ = lint_fixture("master_gate_bad_verdict")
        self.assertEqual(fail_codes(findings), {"gate"})


class VariantDraftTests(unittest.TestCase):
    def test_voice_baseline_passes_in_duration_window(self):
        findings, stats = lint_fixture("voice_baseline")
        self.assertEqual(fail_codes(findings), set())
        self.assertEqual(warn_codes(findings), set())
        self.assertGreater(stats["voice_chars"], 0)
        self.assertGreaterEqual(stats["est_seconds"], 25)
        self.assertLessEqual(stats["est_seconds"], 60)

    def test_variant_without_master_link_fails(self):
        findings, _ = lint_fixture("voice_no_master_link")
        self.assertEqual(fail_codes(findings), {"structure"})

    def test_voice_over_60s_warns_but_passes(self):
        findings, stats = lint_fixture("voice_over_60s")
        self.assertEqual(fail_codes(findings), set())
        self.assertEqual(warn_codes(findings), {"duration"})
        self.assertGreater(stats["est_seconds"], 60)

    def test_secret_fails_and_internal_warns(self):
        findings, _ = lint_fixture("variant_secret_and_internal")
        self.assertEqual(fail_codes(findings), {"secrets"})
        self.assertEqual(warn_codes(findings), {"internal"})


class CliTests(unittest.TestCase):
    def test_main_exit_code_zero_on_pass(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = draft_lint.main(["draft_lint", str(FIXTURES / MANIFEST["master_baseline"])])
        self.assertEqual(rc, 0)
        self.assertIn("1 pass", buf.getvalue())

    def test_main_exit_code_one_on_fail(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = draft_lint.main(["draft_lint", str(FIXTURES / MANIFEST["master_quant_no_disclaimer"])])
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
