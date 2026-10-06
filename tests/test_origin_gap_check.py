# -*- coding: utf-8 -*-
"""Unit tests for the idle-face origin gap pre-check
(src/os/origin_gap_check.py).

R1500 root fix for the R1496(b) push-reject incident: origin-only new
orders must break the quiet state, and a failed fetch must never be
silent (PT-20260928-01 silent-fallback defect family). Pure functions
only - no git, no network.

Run:
    python tests/test_origin_gap_check.py
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "os"))

import origin_gap_check as ogc  # noqa: E402


class TestParseCount(unittest.TestCase):
    def test_plain_int(self):
        self.assertEqual(3, ogc.parse_count("3\n"))

    def test_blank_and_garbage_are_zero(self):
        self.assertEqual(0, ogc.parse_count(""))
        self.assertEqual(0, ogc.parse_count(None))
        self.assertEqual(0, ogc.parse_count("abc"))


class TestClassifyDiff(unittest.TestCase):
    def test_new_order_is_flagged(self):
        cls = ogc.classify_diff([
            "A\torders/O-20261006-1410-HQ-C.md",
        ])
        self.assertEqual(["orders/O-20261006-1410-HQ-C.md"], cls["new_orders"])
        self.assertEqual([], cls["changed_orders"])
        self.assertEqual([], cls["other_files"])

    def test_modified_order_and_other_files_bucketed(self):
        cls = ogc.classify_diff([
            "M\torders/O-20260928-1910-bm-a.md",
            "M\tsrc/os/state.json",
            "A\tdata/x.md",
        ])
        self.assertEqual([], cls["new_orders"])
        self.assertEqual(["orders/O-20260928-1910-bm-a.md"],
                         cls["changed_orders"])
        self.assertEqual(["src/os/state.json", "data/x.md"],
                         cls["other_files"])

    def test_rename_attributed_to_new_path(self):
        cls = ogc.classify_diff(["R100\torders/old.md\torders/new.md"])
        self.assertEqual(["orders/new.md"], cls["changed_orders"])

    def test_malformed_lines_ignored(self):
        cls = ogc.classify_diff(["", "garbage line without tab", "\n"])
        self.assertEqual([], cls["new_orders"])
        self.assertEqual([], cls["other_files"])


class TestBuildFindings(unittest.TestCase):
    def test_fetch_failure_is_loud_fail(self):
        finds = ogc.build_findings(
            {"new_orders": [], "changed_orders": [], "other_files": []},
            behind=0, ahead=0, fetch_rc=128, fetch_err="connection refused")
        self.assertEqual(1, len(finds))
        self.assertEqual("FAIL", finds[0]["level"])
        self.assertEqual("fetch-fail", finds[0]["code"])
        self.assertIn("connection refused", finds[0]["text"])

    def test_origin_new_order_breaks_quiet(self):
        cls = {"new_orders": ["orders/O-X.md"], "changed_orders": [],
               "other_files": []}
        finds = ogc.build_findings(cls, behind=1, ahead=0)
        codes = [f["code"] for f in finds]
        self.assertIn("origin-new-orders", codes)
        self.assertIn("origin-behind", codes)
        self.assertEqual(["FAIL", "FAIL"], [f["level"] for f in finds])

    def test_diverged_replaces_behind(self):
        cls = {"new_orders": [], "changed_orders": [], "other_files": []}
        finds = ogc.build_findings(cls, behind=2, ahead=1)
        codes = [f["code"] for f in finds]
        self.assertIn("diverged", codes)
        self.assertNotIn("origin-behind", codes)

    def test_sync_with_local_push_pending_is_info_only(self):
        cls = {"new_orders": [], "changed_orders": [], "other_files": []}
        finds = ogc.build_findings(cls, behind=0, ahead=2)
        self.assertEqual(1, len(finds))
        self.assertEqual("INFO", finds[0]["level"])
        self.assertEqual("local-ahead", finds[0]["code"])

    def test_upstream_missing_is_fail(self):
        finds = ogc.build_findings(
            {"new_orders": [], "changed_orders": [], "other_files": []},
            behind=0, ahead=0, upstream_missing=True)
        self.assertEqual("upstream-missing", finds[0]["code"])
        self.assertEqual("FAIL", finds[0]["level"])


class TestSummarize(unittest.TestCase):
    def test_quiet_when_no_findings(self):
        self.assertEqual(("origin-gap: QUIET", 0), ogc.summarize([]))

    def test_info_only_still_quiet(self):
        finds = [{"level": "INFO", "code": "local-ahead", "text": "x"}]
        summary, code = ogc.summarize(finds)
        self.assertEqual(0, code)
        self.assertIn("QUIET", summary)

    def test_any_fail_is_findings_exit1(self):
        finds = [{"level": "INFO", "code": "a", "text": ""},
                 {"level": "FAIL", "code": "origin-new-orders", "text": ""}]
        self.assertEqual(("origin-gap: FINDINGS", 1), ogc.summarize(finds))


class TestRender(unittest.TestCase):
    def test_render_head_and_lines(self):
        finds = [{"level": "FAIL", "code": "origin-behind",
                  "text": "origin is ahead by 1 commit(s)"}]
        lines = ogc.render(finds, ahead=0, behind=1, upstream="origin/main")
        self.assertTrue(lines[0].startswith("origin-gap vs origin/main"))
        self.assertTrue(lines[1].startswith("- [FAIL] origin-behind:"))

    def test_render_quiet_has_no_finding_lines(self):
        lines = ogc.render([], ahead=0, behind=0, upstream="origin/main")
        self.assertEqual(2, len(lines))
        self.assertIn("quiet", lines[1])


class TestIncidentReplay(unittest.TestCase):
    """R1496(b) replay: bm-c pushes an order while we idle locally."""

    def test_replay_new_order_from_origin_breaks_all_quiet_gates(self):
        diff = ["A\torders/O-20261006-1410-HQ-C.md",
                "M\tfleet/backlog.md"]
        cls = ogc.classify_diff(diff)
        finds = ogc.build_findings(cls, behind=1, ahead=0)
        summary, code = ogc.summarize(findings=finds)
        self.assertEqual(1, code)
        self.assertEqual("origin-gap: FINDINGS", summary)
        self.assertTrue(any(f["code"] == "origin-new-orders" for f in finds))

    def test_replay_pre_incident_state_is_quiet(self):
        cls = ogc.classify_diff([])
        finds = ogc.build_findings(cls, behind=0, ahead=0)
        self.assertEqual(("origin-gap: QUIET", 0), ogc.summarize(finds))


if __name__ == "__main__":
    unittest.main()
