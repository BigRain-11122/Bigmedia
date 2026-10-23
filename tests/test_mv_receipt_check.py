"""Unit tests for the MV re-run receipt check (src/os/mv_receipt_check.py).

D-20261024-06 (R2431): a rendered v7xx file is not a receipt. The
checker must say ABSENT unless all three pieces exist -- 17 shots, an
edit-grammar reading, and a director PASS (or an explicit failure
list). Nothing here touches the network or the real outbound tree.

Run:
    python tests/test_mv_receipt_check.py
"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src" / "os"))

import mv_receipt_check as mrc  # noqa: E402


def make_dir(case, prefix):
    d = Path(tempfile.mkdtemp(prefix=prefix))
    case.addCleanup(shutil.rmtree, d, ignore_errors=True)
    return d


class TestShots(unittest.TestCase):
    def test_all_seventeen_present(self):
        d = make_dir(self, "mv-rec-")
        for n in range(1, 18):
            (d / ("shot_%02d.mp4" % n)).write_text("x", encoding="utf-8")
        status, detail = mrc.check_shots(d, expected=17)
        self.assertEqual(status, mrc.STATUS_PRESENT)
        self.assertIn("17 shot ids", detail)

    def test_partial_shots_named(self):
        d = make_dir(self, "mv-rec-")
        for n in (1, 2, 3):
            (d / ("shot_%02d.mp4" % n)).write_text("x", encoding="utf-8")
        status, detail = mrc.check_shots(d, expected=17)
        self.assertEqual(status, mrc.STATUS_MISSING)
        self.assertIn("3/17", detail)

    def test_absent_folder(self):
        d = make_dir(self, "mv-rec-")
        status, detail = mrc.check_shots(d / "nope", expected=17)
        self.assertEqual(status, mrc.STATUS_MISSING)
        self.assertIn("no shot folder", detail)


class TestGrammar(unittest.TestCase):
    def _plan(self, case, counts, name="full_mv_v701.json"):
        d = make_dir(case, "mv-rec-plan-")
        (d / name).write_text(json.dumps(counts), encoding="utf-8")
        return d

    def test_matching_grammar(self):
        d = self._plan(self, {"hard_cut": 54, "dissolve": 7,
                              "defocus": 2, "deep_slow": 3})
        status, detail = mrc.check_grammar([d])
        self.assertEqual(status, mrc.STATUS_PRESENT)

    def test_off_grammar_names_gap(self):
        d = self._plan(self, {"hard_cut": 51, "dissolve": 7,
                              "defocus": 2, "deep_slow": 3})
        status, detail = mrc.check_grammar([d])
        self.assertEqual(status, mrc.STATUS_MISSING)
        self.assertIn("hard_cut 51/54", detail)

    def test_no_reading(self):
        d = make_dir(self, "mv-rec-plan-")
        status, _ = mrc.check_grammar([d])
        self.assertEqual(status, mrc.STATUS_MISSING)

    def test_alias_keys_normalized(self):
        self.assertEqual(mrc.grammar_counts({"hardcut": 3})["hard_cut"], 3)


class TestReviewAndVerdict(unittest.TestCase):
    def test_pass_file_found(self):
        d = make_dir(self, "mv-rec-rev-")
        (d / "DIRECTOR-REVIEW-V5-PASS.md").write_text("PASS", encoding="utf-8")
        status, _ = mrc.check_review([d])
        self.assertEqual(status, mrc.STATUS_PRESENT)

    def test_empty_pass_file_is_not_a_pass(self):
        d = make_dir(self, "mv-rec-rev-")
        (d / "DIRECTOR-REVIEW-V5-PASS.md").write_text("", encoding="utf-8")
        status, _ = mrc.check_review([d])
        self.assertEqual(status, mrc.STATUS_MISSING)

    def test_rendered_file_is_never_a_receipt(self):
        d = make_dir(self, "mv-rec-rev-")
        (d / "full_mv_v705.mp4").write_text("x", encoding="utf-8")
        status, _ = mrc.check_review([d])
        self.assertEqual(status, mrc.STATUS_MISSING)

    def test_verdict_needs_all_three(self):
        ok = (mrc.STATUS_PRESENT, "x")
        bad = (mrc.STATUS_MISSING, "x")
        self.assertEqual(mrc.verdict([ok, ok, ok]), "RECEIVED")
        self.assertEqual(mrc.verdict([ok, ok, bad]), "ABSENT")
        self.assertEqual(mrc.verdict([bad, ok, ok]), "ABSENT")

    def test_report_shape(self):
        ok = (mrc.STATUS_PRESENT, "x")
        bad = (mrc.STATUS_MISSING, "y")
        report = mrc.build_report(ok, bad, bad, ts="2026-10-24 06:20:00")
        self.assertEqual(report["verdict"], "ABSENT")
        self.assertEqual(report["shots"]["status"], "present")
        self.assertEqual(report["grammar"]["detail"], "y")


if __name__ == "__main__":
    unittest.main(verbosity=2)