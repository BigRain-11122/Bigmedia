# -*- coding: utf-8 -*-
"""Tests for group_scan (state/queue/tech#50, R1880): fixed single-truth probe
for the task-book group-scan step — dnum watermark diff (8-digit date family,
R1849/R1879 false-quiet regression locks) + ledger marker anchors + mtime
faces.

Fixture tests are hermetic; LiveRepoTests are read-only against the real
group files (skipped when absent).
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src", "os"))

import group_scan as gs  # noqa: E402


class DnumRegexTests(unittest.TestCase):
    """The two incident patterns must never come back (false-quiet locks)."""

    def test_eight_digit_date_family(self):
        # R1879 incident: a 2-digit-month pattern failed this whole family.
        text = "D-20261010-01 and C-20261010-05 pass."
        self.assertEqual(gs.extract_dnums(text),
                         {"D-20261010-01", "C-20261010-05"})

    def test_dates_beyond_month_boundary(self):
        # R1849 incident: a 2026\d{3} month-face pattern missed 1010+ dates.
        text = "D-20261010-01\nC-20261031-12\nD-20261209-3"
        self.assertEqual(gs.extract_dnums(text),
                         {"D-20261010-01", "C-20261031-12", "D-20261209-3"})

    def test_future_year_still_matches(self):
        # No hard-coded year: 2027 tokens are valid dnums.
        self.assertEqual(gs.extract_dnums("D-20270101-01"),
                         {"D-20270101-01"})

    def test_counter_widths(self):
        text = "D-20261010-1 D-20261010-19 D-20261010-123"
        self.assertEqual(gs.extract_dnums(text),
                         {"D-20261010-1", "D-20261010-19", "D-20261010-123"})

    def test_rejects_non_dnum_shapes(self):
        text = ("XD-20261010-01 P-20261010-03 D-2026-1010-01 "
                "SC-20260901 _D-20261010-01 D-20261010-0112")
        self.assertEqual(gs.extract_dnums(text), set())

    def test_row_and_inline_both_counted_once(self):
        text = "- D-20261010-01 row\nrefer D-20261010-01 inline"
        self.assertEqual(gs.extract_dnums(text), {"D-20261010-01"})


class AnchorClassifyTests(unittest.TestCase):
    def test_heading_is_row(self):
        kinds = gs.classify_tokens("### D-20261010-01 some title")
        self.assertEqual(kinds["D-20261010-01"], "row")

    def test_list_marker_is_row(self):
        kinds = gs.classify_tokens("- D-20261010-02 title")
        self.assertEqual(kinds["D-20261010-02"], "row")

    def test_numbered_marker_is_row(self):
        kinds = gs.classify_tokens("12. D-20261010-03 title")
        self.assertEqual(kinds["D-20261010-03"], "row")

    def test_bare_line_start_is_row(self):
        kinds = gs.classify_tokens("D-20261010-04 at line start")
        self.assertEqual(kinds["D-20261010-04"], "row")

    def test_mid_line_is_inline(self):
        kinds = gs.classify_tokens("already cited D-20261010-05 in prose")
        self.assertEqual(kinds["D-20261010-05"], "inline")

    def test_year_in_prefix_is_inline(self):
        kinds = gs.classify_tokens("2026 D-20261010-06 prose")
        self.assertEqual(kinds["D-20261010-06"], "inline")

    def test_row_wins_over_earlier_inline(self):
        text = "inline first D-20261010-07\n### D-20261010-07 later row"
        self.assertEqual(gs.classify_tokens(text)["D-20261010-07"], "row")


class DiffWatermarkTests(unittest.TestCase):
    def test_truly_new_sorted_and_wm_only(self):
        cur = {"D-20261010-02", "C-20260927-01"}
        wm = ["C-20260927-01", "D-20260930-19"]
        new, only = gs.diff_watermark(cur, wm)
        self.assertEqual(new, ["D-20261010-02"])
        self.assertEqual(only, ["D-20260930-19"])

    def test_empty_watermark_everything_new(self):
        # False-quiet direction: a broken regex yielding fewer tokens can
        # only shrink TRULY_NEW, never silently invent quiet.
        new, only = gs.diff_watermark({"D-20261010-01"}, [])
        self.assertEqual(new, ["D-20261010-01"])
        self.assertEqual(only, [])

    def test_slim_family_is_not_new(self):
        new, only = gs.diff_watermark(set(), ["D-20260909-05"])
        self.assertEqual(new, [])
        self.assertEqual(only, ["D-20260909-05"])


class LedgerScanTests(unittest.TestCase):
    def test_lines_vs_occurrences(self):
        text = ("line one @BigStream\n"
                "plain\n"
                "double @BigStream @BigStream\n")
        stats, preview = gs.scan_ledger(text)
        self.assertEqual(stats["@BigStream"], (2, 3))
        self.assertTrue(preview.startswith("double"))

    def test_marker_family_counted_independently(self):
        text = "@BigStream a\n@七线全司 b\n@全司 c\n@六司 d\n@八线全量 e\n"
        stats, _ = gs.scan_ledger(text)
        for marker in gs.LEDGER_MARKERS:
            self.assertEqual(stats[marker], (1, 1))

    def test_empty_text(self):
        stats, preview = gs.scan_ledger("")
        self.assertEqual(stats, {})
        self.assertEqual(preview, "")

    def test_blank_last_line_uses_last_content(self):
        stats, preview = gs.scan_ledger("@BigStream tail\n\n\n")
        self.assertTrue(preview.startswith("@BigStream tail"))


class OwnOrdersTopTests(unittest.TestCase):
    def test_newest_wins(self):
        with tempfile.TemporaryDirectory() as d:
            old = os.path.join(d, "O-old.md")
            new = os.path.join(d, "O-new.md")
            for path in old, new:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("x")
            past = time.time() - 3600
            os.utime(old, (past, past))
            top = gs.own_orders_top(d)
            self.assertEqual(top[0], "O-new.md")

    def test_empty_dir(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(gs.own_orders_top(d))


def _write(path, content):
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)


class MainFixtureTests(unittest.TestCase):
    """Hermetic CLI integration over a fixture group tree."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = self.tmp.name
        self.paths = {
            "decisions": os.path.join(root, "decisions.md"),
            "hq_orders": os.path.join(root, "orders.md"),
            "ledger": os.path.join(root, "ledger.md"),
            "own_orders_dir": os.path.join(root, "own_orders"),
            "state": os.path.join(root, "state.json"),
        }
        os.makedirs(self.paths["own_orders_dir"])
        _write(self.paths["decisions"],
               "- D-20260930-19 known row\nrefer C-20260909-05 inline\n")
        _write(self.paths["ledger"],
               "@BigStream old line\n@BigStream old line again\n")
        _write(self.paths["hq_orders"], "hq order file\n\n")
        _write(os.path.join(self.paths["own_orders_dir"], "O-1.md"), "one\n")
        _write(self.paths["state"], json.dumps(
            {"decisions_watermark": {"dnums": ["D-20260930-19",
                                               "C-20260909-05"]}}))

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, extra=None):
        argv = ["group_scan"]
        for key in ("decisions", "hq_orders", "ledger", "own_orders_dir",
                    "state"):
            argv += ["--" + key.replace("_", "-"), self.paths[key]]
        argv += list(extra or [])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = gs.main(argv)
        return rc, buf.getvalue()

    def test_quiet_when_watermark_covers_all(self):
        rc, out = self._run()
        self.assertEqual(rc, gs.RC_QUIET)
        self.assertIn("truly_new=0", out)
        self.assertIn("wm_only=0", out)
        self.assertIn("TRULY_NEW: (none)", out)
        self.assertIn("@BigStream lines=2 occurrences=2", out)
        self.assertIn("own-orders-top | O-1.md", out)

    def test_new_row_breaks_silence(self):
        with io.open(self.paths["decisions"], "a", encoding="utf-8") as fh:
            fh.write("### D-20261010-01 fresh row\n")
        rc, out = self._run()
        self.assertEqual(rc, gs.RC_NEW)
        self.assertIn("TRULY_NEW: D-20261010-01 [row]", out)

    def test_new_inline_annotated(self):
        with io.open(self.paths["decisions"], "a", encoding="utf-8") as fh:
            fh.write("see D-20261010-02 cited inside prose\n")
        rc, out = self._run()
        self.assertEqual(rc, gs.RC_NEW)
        self.assertIn("D-20261010-02 [inline]", out)

    def test_slim_family_not_reported_new(self):
        # token in watermark but absent from file = slim/inline-consumed
        _write(self.paths["state"], json.dumps(
            {"decisions_watermark": {"dnums": ["D-20260930-19",
                                               "C-20260909-05",
                                               "D-20260101-09"]}}))
        rc, out = self._run()
        self.assertEqual(rc, gs.RC_QUIET)
        self.assertIn("wm_only=1", out)
        self.assertIn("wm_only: D-20260101-09", out)
        self.assertIn("TRULY_NEW: (none)", out)

    def test_missing_decisions_fails_loud(self):
        os.remove(self.paths["decisions"])
        rc, out = self._run()
        self.assertEqual(rc, gs.RC_READ_FAIL)
        self.assertIn("read-fail: decisions", out)

    def test_unreadable_state_fails_loud(self):
        _write(self.paths["state"], "not json {")
        rc, out = self._run()
        self.assertEqual(rc, gs.RC_READ_FAIL)
        self.assertIn("read-fail: state", out)

    def test_out_file_utf8_no_bom_and_trimmed_stdout(self):
        out_path = os.path.join(self.tmp.name, "ev.txt")
        rc, out = self._run(["--out", out_path])
        self.assertIn(rc, (gs.RC_QUIET, gs.RC_NEW))
        self.assertIn("group-scan: overall_rc=", out)
        self.assertIn("DECISIONS: rc=", out)
        self.assertNotIn("=== DECISIONS", out)  # stdout trimmed
        with open(out_path, "rb") as fh:
            data = fh.read()
        self.assertFalse(data.startswith(b"\xef\xbb\xbf"), "BOM leaked")
        text = data.decode("utf-8")
        self.assertIn("=== DECISIONS (rc=", text)
        self.assertIn("=== LEDGER (rc=", text)
        self.assertIn("=== MTIME (rc=", text)

    def test_out_echo_prints_report(self):
        out_path = os.path.join(self.tmp.name, "ev.txt")
        rc, out = self._run(["--out", out_path, "--echo"])
        self.assertIn(rc, (gs.RC_QUIET, gs.RC_NEW))
        self.assertIn("=== DECISIONS (rc=", out)

    def test_usage_error(self):
        self.assertEqual(self._run(["--bogus"])[0], gs.RC_USAGE)


@unittest.skipUnless(
    os.path.exists(str(gs.DEFAULTS["decisions"]))
    and os.path.exists(str(gs.DEFAULTS["state"]))
    and os.path.exists(str(gs.DEFAULTS["ledger"])),
    "live group files not present")
class LiveRepoTests(unittest.TestCase):
    """Read-only real-run face (tech#50 criterion: readings == ad-hoc face)."""

    def _run_live(self, extra=None):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = gs.main(["group_scan"] + list(extra or []))
        return rc, buf.getvalue()

    def test_live_quiet_or_new_never_read_fail(self):
        rc, out = self._run_live()
        self.assertIn(rc, (gs.RC_QUIET, gs.RC_NEW))
        self.assertIn("=== DECISIONS (rc=", out)
        self.assertIn("@BigStream lines=", out)

    def test_live_token_family_lock(self):
        # CUR=0 false-quiet lock (R1879 family): the live file must yield a
        # non-empty token set whose shapes are exactly D/C + 8-digit date +
        # counter. Under-matching regexes fail here.
        text, _, _ = gs.read_text(gs.DEFAULTS["decisions"])
        tokens = gs.extract_dnums(text)
        self.assertTrue(tokens, "CUR=0 false-quiet regression")
        for token in tokens:
            self.assertRegex(token, r"^[DC]-20\d{6}-\d{1,3}$")

    def test_live_watermark_present(self):
        wm = gs.load_watermark(gs.DEFAULTS["state"])
        self.assertTrue(wm, "watermark missing/empty")


if __name__ == "__main__":
    unittest.main()
