# -*- coding: utf-8 -*-
"""Unit tests for src/research_digest.py (P4 minimal build, R307).

Suite style = unittest discovery (house rule; no pytest dependency).
Fake model injection: rd.call_model is swapped per-test, so no real
ollama call runs here. The REAL smoke evidence lives in the p4-ledger
row of the R307 run (docs/local-llm-p4-criteria.md sec.4).
ASCII rule: test source is pure ASCII; Chinese strings use \\u escapes.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import research_digest as rd  # noqa: E402

GOOD_DIGEST = (
    "## " + "\u4e00\u53e5\u8bdd\u7ed3\u8bba\n"
    "\u7c89\u4e1d\u91c7\u96c6\u53ea\u80fd\u8d70\u5b98\u65b9\u901a\u9053\u3002[L1]\n"
    "## " + "\u8981\u70b9\n"
    "### " + "\u901a\u9053\n"
    "- " + "\u516c\u4f17\u53f7 8 \u4e2a\u7559\u8a00\u63a5\u53e3\u5f00\u653e\u3002[L2][L3]\n"
    "## " + "\u5173\u952e\u6570\u5b57\u4e0e\u4e13\u540d\n"
    "- 8 [L2]\n"
    "## " + "\u5361\u70b9\u4e0e\u672a\u51b3\n"
    "- " + "\u89c6\u9891\u53f7\u65e0\u516c\u5f00\u901a\u9053\u3002[L4]\n")


class TestPureHelpers(unittest.TestCase):

    def test_number_source(self):
        numbered, n = rd.number_source("a\nb\nc")
        self.assertEqual(n, 3)
        self.assertEqual(numbered.splitlines()[0], "L1\ta")
        self.assertEqual(numbered.splitlines()[2], "L3\tc")

    def test_clip_text_short_passes_through(self):
        text, clipped = rd.clip_text("abc", 10)
        self.assertEqual((text, clipped), ("abc", False))

    def test_clip_text_long_clips_on_line_boundary(self):
        text = "0123456789\n" * 5
        cut, clipped = rd.clip_text(text, 22)
        self.assertTrue(clipped)
        self.assertLessEqual(len(cut), 22)
        self.assertNotIn(cut[-1:], "\r")  # clip ends clean

    def test_build_prompt_substitutes_and_appends(self):
        template = "\u5e45\u5ea6 {max_lines} \u884c"
        prompt = rd.build_prompt(template, "L1\tx", 42, False)
        self.assertIn("42", prompt)
        self.assertIn("L1\tx", prompt)
        self.assertNotIn("{max_lines}", prompt)

    def test_strip_verification_section(self):
        digest = "body\n\n## " + "\u9a8c\u8bc1\u58f0\u660e\n- x\n"
        self.assertEqual(rd.strip_verification_section(digest), "body")


class TestCheckDigest(unittest.TestCase):

    def _as_dict(self, digest, n_lines, cap):
        return dict((name, ok) for name, ok, _
                    in rd.check_digest(digest, n_lines, cap))

    def test_good_digest_all_pass(self):
        checks = self._as_dict(GOOD_DIGEST, 10, 60)
        self.assertTrue(checks["J2_line_cap"])
        self.assertTrue(checks["J2_structure"])
        self.assertTrue(checks["J1_citations"])

    def test_out_of_range_citation_fails_j1(self):
        bad = GOOD_DIGEST.replace("[L4]", "[L99]")
        checks = self._as_dict(bad, 10, 60)
        self.assertFalse(checks["J1_citations"])

    def test_citation_floor_fails_j1(self):
        # R307 run 2 regression lock: a single marker is not traceability.
        starved = GOOD_DIGEST.replace("[L2][L3]", "").replace("[L4]", "")
        checks = self._as_dict(starved, 10, 60)
        self.assertFalse(checks["J1_citations"])

    def test_over_line_cap_fails_j2(self):
        huge = GOOD_DIGEST + "line\n" * 100
        checks = self._as_dict(huge, 10, 60)
        self.assertFalse(checks["J2_line_cap"])


class TestRunDigest(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self._orig_call_model = rd.call_model

    def tearDown(self):
        rd.call_model = self._orig_call_model
        self._tmp.cleanup()

    def test_missing_input(self):
        s = rd.run_digest(self.tmp / "nope.md",
                          ledger_path=self.tmp / "p4-ledger.md")
        self.assertEqual(s["error"], "input file missing")

    def test_end_to_end_fake_model(self):
        src = self.tmp / "fan-ops.md"
        src.write_text(
            "\u516c\u4f17\u53f7 8 \u4e2a\u7559\u8a00\u63a5\u53e3\n"
            "\u89c6\u9891\u53f7\u65e0\u516c\u5f00\u901a\u9053\n"
            "\u7070\u4ea7\u5224\u8d1f\n"
            "\u4f01\u5fae\u5b98\u65b9 API \u4e3a\u4e3b\u8def\n", encoding="utf-8")
        prompt_file = self.tmp / "prompt.txt"
        prompt_file.write_text("tpl {max_lines}", encoding="utf-8")
        ledger = self.tmp / "p4-ledger.md"

        def fake_call_model(model, prompt, timeout=300):
            self.assertNotIn("{max_lines}", prompt)
            return 0, GOOD_DIGEST

        rd.call_model = fake_call_model
        s = rd.run_digest(src, prompt_file=prompt_file, ledger_path=ledger)
        self.assertIsNone(s["error"])
        self.assertEqual(s["verdict"], "PASS")
        out_text = Path(s["out"]).read_text(encoding="utf-8")
        self.assertIn("\u9a8c\u8bc1\u58f0\u660e", out_text)  # tool statement
        self.assertIn("[L1]", out_text)                      # digest body
        self.assertTrue(ledger.exists())
        self.assertIn("PASS", ledger.read_text(encoding="utf-8"))

    def test_ollama_failure_reported(self):
        src = self.tmp / "x.md"
        src.write_text("one\n", encoding="utf-8")
        prompt_file = self.tmp / "prompt.txt"
        prompt_file.write_text("tpl {max_lines}", encoding="utf-8")

        def bad_call_model(model, prompt, timeout=300):
            return 3, "boom"

        rd.call_model = bad_call_model
        s = rd.run_digest(src, prompt_file=prompt_file,
                          ledger_path=self.tmp / "p4-ledger.md")
        self.assertEqual(s["error"], "ollama exit 3")


if __name__ == "__main__":
    unittest.main()
