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
from datetime import date, datetime, timedelta

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


class OrdersRowStatsTests(unittest.TestCase):
    """tech#103 pure core: |-row count + last-row first-cell fingerprint."""

    def test_counts_pipe_rows_only(self):
        text = ("intro line\n"
                "| 10-09 09:0x | a |\n"
                "| --- | --- |\n"
                "  | 10-09 11:0x | indented |\n"
                "plain\n")
        rows, tail = gs.orders_row_stats(text)
        self.assertEqual(3, rows)
        self.assertEqual("10-09 11:0x", tail)

    def test_single_pipe_row_last_wins(self):
        rows, tail = gs.orders_row_stats("| only-cell\n")
        self.assertEqual((1, "only-cell"), (rows, tail))

    def test_empty_text(self):
        self.assertEqual((0, ""), gs.orders_row_stats(""))


class OrdersFaceTests(unittest.TestCase):
    """tech#103 face: the four spec cases (R1978 blind-window root-fix).

    R1975-R1977 judged the orders face quiet by mtime-anchor MEMORY
    comparison while three new CEO rows had not yet landed locally; the
    face now carries its own content-addressing watermark judgment.
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = self.tmp.name
        self.paths = {"hq_orders": os.path.join(root, "orders.md"),
                      "state": os.path.join(root, "state.json")}

    def _write_orders(self, text):
        _write(self.paths["hq_orders"], text)

    def _write_state_wm(self, rows, tail_key):
        _write(self.paths["state"], json.dumps(
            {"orders_row_watermark": {"rows": rows, "tail_key": tail_key}}))

    def test_new_row_breaks_silence(self):
        self._write_orders("| 10-11 13:2x | first |\n| 10-11 13:4x | second |\n")
        self._write_state_wm(1, "10-11 13:2x")
        rc, text = gs.face_orders(self.paths)
        self.assertEqual(gs.RC_NEW, rc)
        self.assertIn("ORDERS-NEW: rows 1->2", text)
        self.assertIn("tail_key '10-11 13:2x'->'10-11 13:4x'", text)

    def test_watermark_match_is_quiet(self):
        self._write_orders("| 10-11 13:4x | tail |\n")
        self._write_state_wm(1, "10-11 13:4x")
        rc, text = gs.face_orders(self.paths)
        self.assertEqual(gs.RC_QUIET, rc)
        self.assertIn("ORDERS: quiet (watermark matches)", text)

    def test_missing_watermark_first_run_is_new_not_quiet(self):
        # first-run semantics: no stored baseline must never read quiet
        self._write_orders("| 10-11 13:4x | tail |\n")
        _write(self.paths["state"], json.dumps({}))
        rc, text = gs.face_orders(self.paths)
        self.assertEqual(gs.RC_NEW, rc)
        self.assertIn("watermark-missing", text)
        self.assertIn("ORDERS-NEW: watermark-missing", text)

    def test_read_fail_hq_orders(self):
        _write(self.paths["state"], json.dumps({}))
        rc, text = gs.face_orders(self.paths)  # orders.md absent
        self.assertEqual(gs.RC_READ_FAIL, rc)
        self.assertIn("read-fail: hq-orders", text)

    def test_shrink_also_breaks_silence(self):
        # removal/re-layout direction is a deviation too (fail-closed)
        self._write_orders("| 10-09 09:0x | only row |\n")
        self._write_state_wm(2, "10-09 10:0x")
        rc, text = gs.face_orders(self.paths)
        self.assertEqual(gs.RC_NEW, rc)
        self.assertIn("ORDERS-NEW: rows 2->1", text)


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
        _write(self.paths["hq_orders"],
               "| 10-09 09:0x | seed row |\n| 10-09 10:0x | seed tail |\n")
        _write(os.path.join(self.paths["own_orders_dir"], "O-1.md"), "one\n")
        _write(self.paths["state"], json.dumps(
            {"decisions_watermark": {"dnums": ["D-20260930-19",
                                               "C-20260909-05"]},
             "orders_row_watermark": {"rows": 2,
                                      "tail_key": "10-09 10:0x"}}))

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

    def test_orders_new_row_breaks_silence_overall(self):
        # tech#103 CLI wiring: a new orders table row must break the whole
        # probe's silence even when the decisions face stays quiet.
        with io.open(self.paths["hq_orders"], "a", encoding="utf-8") as fh:
            fh.write("| 10-11 13:4x | fresh |\n")
        rc, out = self._run()
        self.assertEqual(gs.RC_NEW, rc)
        self.assertIn("truly_new=0", out)          # decisions face quiet
        self.assertIn("ORDERS-NEW: rows 2->3", out)
        self.assertIn("tail_key '10-09 10:0x'->'10-11 13:4x'", out)

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
                                               "D-20260101-09"]},
             "orders_row_watermark": {"rows": 2,
                                      "tail_key": "10-09 10:0x"}}))
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


class DigestSupplyFaceTests(unittest.TestCase):
    """tech#129: DIGEST 史源 supply-gap advisory face (R2050 seed).

    Five manual supply-blindspot corrections on record
    (R870/R1095/R1303/R1536/R2050) -- this face is the machine hint: an
    unconsumed orders cluster newer than the latest DIGEST card surfaces
    as a per-round advisory line, and breaks silence (WARN) once it has
    sat >2 days. Creative judgment (A-grade + number-density grading)
    stays with the loop body; the face is a backstop, not an auto-trigger.
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = self.tmp.name
        self.orders = os.path.join(root, "orders.md")
        self.cards = os.path.join(root, "cards")
        os.makedirs(os.path.join(self.cards, "MC-20261011-DIGEST-v18"))
        _write(self.orders, "| 10-11 11:3x | covered |\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_row_dates_both_live_shapes(self):
        text = ("| 10-12 13:5x | a |\n"
                "| 2026-09-28 18:1x | b |\n"
                "| 10-09 ~12:2x | c |\n"
                "| 时间 | header |\n"
                "|---|---|\n")
        self.assertEqual(gs.orders_row_dates(text, year=2026),
                         {date(2026, 10, 12), date(2026, 9, 28),
                          date(2026, 10, 9)})

    def test_latest_digest_prefers_non_tmp_at_same_date(self):
        os.makedirs(os.path.join(self.cards, "MC-20261011-DIGEST-v18-tmp"))
        os.makedirs(os.path.join(self.cards, "MC-20261010-DIGEST-v17"))
        latest = gs.latest_digest_card(self.cards)
        self.assertEqual((latest[0], latest[1]),
                         (date(2026, 10, 11), "MC-20261011-DIGEST-v18"))

    def test_latest_digest_missing_dir_is_none(self):
        self.assertIsNone(gs.latest_digest_card(
            os.path.join(self.tmp.name, "no-such-dir")))

    def test_quiet_when_latest_card_covers_rows(self):
        verdict = gs.classify_digest_supply_gap(
            {date(2026, 10, 11), date(2026, 10, 12)}, date(2026, 10, 12),
            date(2026, 10, 14))
        self.assertEqual(verdict["status"], "quiet")

    def test_advisory_when_cluster_fresh(self):
        verdict = gs.classify_digest_supply_gap(
            {date(2026, 10, 13)}, date(2026, 10, 12), date(2026, 10, 13))
        self.assertEqual(verdict["status"], "advisory")
        self.assertEqual(verdict["age_days"], 0)

    def test_v19_window_shape_gap_warn(self):
        # R2050 criterion "10-12 簇落账→若 v19 未产应点名", clock advanced
        # past the 2d threshold: v18 covers 10-11, the 10-12 cluster sat
        # unconsumed, on 10-15 the backstop fires.
        verdict = gs.classify_digest_supply_gap(
            {date(2026, 10, 11), date(2026, 10, 12)}, date(2026, 10, 11),
            date(2026, 10, 15))
        self.assertEqual(verdict["status"], "gap")
        self.assertEqual(verdict["unconsumed"], 1)
        self.assertEqual(verdict["oldest"], date(2026, 10, 12))

    def test_r870_family_blindspot_shape(self):
        # R870-shape chronic window: v10 covers 09-29; 09-30/10-01 rows
        # unconsumed; on 10-03 the backstop fires (the real R870 window
        # resolved by hand inside ~2d -- below the WARN line, which is
        # exactly the honest resolution boundary of this face).
        verdict = gs.classify_digest_supply_gap(
            {date(2026, 9, 30), date(2026, 10, 1)}, date(2026, 9, 29),
            date(2026, 10, 3))
        self.assertEqual(verdict["status"], "gap")
        self.assertEqual(verdict["age_days"], 3)

    def test_face_quiet_when_covered(self):
        rc, out = gs.face_digest_supply(
            {"cards_dir": self.cards, "hq_orders": self.orders},
            today=date(2026, 10, 14))
        self.assertEqual(rc, gs.RC_QUIET)
        self.assertIn("DIGEST-SUPPLY: quiet", out)

    def test_face_gap_breaks_silence(self):
        _write(self.orders, "| 10-12 12:4x | fresh cluster |\n")
        rc, out = gs.face_digest_supply(
            {"cards_dir": self.cards, "hq_orders": self.orders},
            today=date(2026, 10, 15))
        self.assertEqual(rc, gs.RC_NEW)
        self.assertIn("DIGEST-SUPPLY-GAP:", out)
        self.assertIn("age 3d", out)

    def test_face_inactive_when_cards_dir_missing(self):
        rc, out = gs.face_digest_supply(
            {"cards_dir": os.path.join(self.tmp.name, "nope"),
             "hq_orders": self.orders},
            today=date(2026, 10, 15))
        self.assertEqual(rc, gs.RC_QUIET)
        self.assertIn("DIGEST-SUPPLY: inactive", out)

    def test_face_read_fail_hq_orders(self):
        rc, out = gs.face_digest_supply(
            {"cards_dir": self.cards,
             "hq_orders": os.path.join(self.tmp.name, "nope.md")},
            today=date(2026, 10, 15))
        self.assertEqual(rc, gs.RC_READ_FAIL)
        self.assertIn("read-fail: hq-orders", out)


class DigestSupplyCliTests(unittest.TestCase):
    """CLI wiring: gap WARN breaks the whole probe's silence; advisory
    does not. Dates are computed against the real clock for determinism."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = self.tmp.name
        self.paths = {
            "decisions": os.path.join(root, "decisions.md"),
            "hq_orders": os.path.join(root, "orders.md"),
            "ledger": os.path.join(root, "ledger.md"),
            "own_orders_dir": os.path.join(root, "own_orders"),
            "state": os.path.join(root, "state.json"),
            "cards_dir": os.path.join(root, "cards"),
        }
        os.makedirs(self.paths["own_orders_dir"])
        os.makedirs(self.paths["cards_dir"])
        _write(self.paths["decisions"],
               "- D-20260930-19 known row\nrefer C-20260909-05 inline\n")
        _write(self.paths["ledger"], "@BigStream old line\n")
        _write(os.path.join(self.paths["own_orders_dir"], "O-1.md"), "one\n")
        _write(self.paths["state"], json.dumps(
            {"decisions_watermark": {"dnums": ["D-20260930-19",
                                               "C-20260909-05"]},
             "orders_row_watermark": {"rows": 1,
                                      "tail_key": "seed"}}))

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self):
        argv = ["group_scan"]
        for key in ("decisions", "hq_orders", "ledger", "own_orders_dir",
                    "state", "cards_dir"):
            argv += ["--" + key.replace("_", "-"), self.paths[key]]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = gs.main(argv)
        return rc, buf.getvalue()

    @staticmethod
    def _card_name(day):
        return "MC-%s-DIGEST-v99" % day.strftime("%Y%m%d")

    def test_gap_breaks_overall_rc(self):
        today = datetime.now().date()
        os.makedirs(os.path.join(
            self.paths["cards_dir"], self._card_name(today - timedelta(days=5))))
        row_day = today - timedelta(days=3)
        tail_key = row_day.strftime("%m-%d") + " 09:0x"
        _write(self.paths["hq_orders"],
               "| %s | cluster |\n" % tail_key)
        _write(self.paths["state"], json.dumps(
            {"decisions_watermark": {"dnums": ["D-20260930-19",
                                               "C-20260909-05"]},
             "orders_row_watermark": {"rows": 1,
                                      "tail_key": tail_key}}))
        rc, out = self._run()
        self.assertEqual(rc, gs.RC_NEW)
        self.assertIn("DIGEST-SUPPLY-GAP:", out)
        self.assertIn("=== DIGEST-SUPPLY (rc=1)", out)

    def test_advisory_keeps_overall_quiet(self):
        today = datetime.now().date()
        os.makedirs(os.path.join(
            self.paths["cards_dir"], self._card_name(today - timedelta(days=5))))
        row_day = today - timedelta(days=1)
        tail_key = row_day.strftime("%m-%d") + " 09:0x"
        _write(self.paths["hq_orders"],
               "| %s | cluster |\n" % tail_key)
        _write(self.paths["state"], json.dumps(
            {"decisions_watermark": {"dnums": ["D-20260930-19",
                                               "C-20260909-05"]},
             "orders_row_watermark": {"rows": 1,
                                      "tail_key": tail_key}}))
        rc, out = self._run()
        self.assertEqual(rc, gs.RC_QUIET)
        self.assertIn("DIGEST-SUPPLY: 1 unconsumed orders row-date(s)",
                      out)
        self.assertIn("advisory", out)

    def test_covered_cluster_face_silent(self):
        today = datetime.now().date()
        os.makedirs(os.path.join(
            self.paths["cards_dir"], self._card_name(today)))
        tail_key = today.strftime("%m-%d") + " 09:0x"
        _write(self.paths["hq_orders"],
               "| %s | cluster |\n" % tail_key)
        _write(self.paths["state"], json.dumps(
            {"decisions_watermark": {"dnums": ["D-20260930-19",
                                               "C-20260909-05"]},
             "orders_row_watermark": {"rows": 1,
                                      "tail_key": tail_key}}))
        rc, out = self._run()
        self.assertEqual(rc, gs.RC_QUIET)
        self.assertIn("DIGEST-SUPPLY: quiet", out)


class _FakeProc:
    def __init__(self, returncode=0, stdout=b""):
        self.returncode = returncode
        self.stdout = stdout


class OrdersOriginDeltaTests(unittest.TestCase):
    """tech#133 (R2059/R2064): origin-only rows must break silence."""

    def test_classify_quiet_when_equal(self):
        verdict = gs.classify_orders_origin_delta(310, 310)
        self.assertEqual(verdict["status"], "quiet")
        self.assertEqual(verdict["delta"], 0)

    def test_classify_ahead_breaks_silence(self):
        # R2064 live anchor: origin 312 vs worktree 311.
        verdict = gs.classify_orders_origin_delta(312, 311)
        self.assertEqual(verdict["status"], "ahead")
        self.assertEqual(verdict["delta"], 1)

    def test_classify_local_ahead_is_quiet(self):
        # A push window (worktree ahead of origin) is NOT a blind spot.
        verdict = gs.classify_orders_origin_delta(310, 312)
        self.assertEqual(verdict["status"], "quiet")
        self.assertEqual(verdict["delta"], -2)

    def test_classify_degraded(self):
        verdict = gs.classify_orders_origin_delta(None, 310)
        self.assertEqual(verdict["status"], "degraded")
        self.assertIsNone(verdict["origin"])

    def test_resolve_git_skips_gitsilent(self):
        # The PATH git on this machine is the stdout-swallowing gitsilent
        # wrapper (R-1952): it must never be resolved for this face (0-row
        # silent-kill family).
        with tempfile.TemporaryDirectory() as td:
            silent = os.path.join(td, "gitsilent", "git.exe")
            os.makedirs(os.path.dirname(silent))
            with io.open(silent, "wb"):
                pass
            self.assertIsNone(gs._resolve_git(silent))

    def test_resolve_git_unresolved_when_absent(self):
        self.assertIsNone(gs._resolve_git(r"C:\no\such\git.exe"))

    def _rows_with_runner(self, runner, git_path):
        return gs.orders_origin_rows(group_root=".", runner=runner,
                                     git_path=git_path)

    def test_orders_origin_rows_success(self):
        calls = []

        def fake_runner(argv):
            calls.append(argv)
            if "fetch" in argv:
                return _FakeProc(0)
            return _FakeProc(0, b"| 10-12 17:2x | a |\n| 10-12 17:4x | b |\n")

        rows, source = self._rows_with_runner(
            fake_runner, r"C:\Program Files\Git\cmd\git.exe")
        self.assertEqual(rows, 2)
        self.assertEqual(source, "origin/main")
        self.assertEqual(len(calls), 2)  # fetch then show
        self.assertIn("fetch", calls[0])
        self.assertIn("show", calls[1])

    def test_orders_origin_rows_fetch_fail_degrades(self):
        rows, source = self._rows_with_runner(
            lambda argv: _FakeProc(1), r"C:\Program Files\Git\cmd\git.exe")
        self.assertIsNone(rows)
        self.assertIn("fetch-failed", source)

    def test_orders_origin_rows_show_fail_degrades(self):
        def fake_runner(argv):
            if "fetch" in argv:
                return _FakeProc(0)
            return _FakeProc(128, b"")

        rows, source = self._rows_with_runner(
            fake_runner, r"C:\Program Files\Git\cmd\git.exe")
        self.assertIsNone(rows)
        self.assertIn("show-failed", source)

    def test_orders_origin_rows_fetch_exception_degrades(self):
        def fake_runner(argv):
            raise OSError("network down")

        rows, source = self._rows_with_runner(
            fake_runner, r"C:\Program Files\Git\cmd\git.exe")
        self.assertIsNone(rows)
        self.assertIn("fetch-error", source)

    def test_orders_origin_rows_git_unresolved(self):
        rows, source = self._rows_with_runner(
            lambda argv: _FakeProc(0), r"C:\no\such\git.exe")
        self.assertIsNone(rows)
        self.assertIn("git-unresolved", source)

    def _face_with(self, orders_text, origin_body, git_exists=True):
        with tempfile.TemporaryDirectory() as td:
            op = os.path.join(td, "orders.md")
            with io.open(op, "w", encoding="utf-8") as fh:
                fh.write(orders_text)
            paths = dict(gs.DEFAULTS)
            paths["hq_orders"] = op

            def fake_runner(argv):
                if "fetch" in argv:
                    return _FakeProc(0)
                return _FakeProc(0, origin_body)

            git_path = (r"C:\Program Files\Git\cmd\git.exe" if git_exists
                        else r"C:\no\such\git.exe")
            return gs.face_orders_origin_delta(paths, runner=fake_runner,
                                               git_path=git_path)

    def test_face_quiet_when_origin_matches(self):
        rc, out = self._face_with("| a |\n| b |\n", b"| a |\n| b |\n")
        self.assertEqual(rc, gs.RC_QUIET)
        self.assertIn("ORDERS-ORIGIN-DELTA: quiet", out)
        self.assertIn("worktree rows=2", out)

    def test_face_ahead_breaks_silence(self):
        rc, out = self._face_with("| a |\n", b"| a |\n| b |\n")
        self.assertEqual(rc, gs.RC_NEW)
        self.assertIn("ORDERS-ORIGIN-DELTA-WARN", out)
        self.assertIn("1 origin-only row(s)", out)
        self.assertIn("R2059/R2064 family", out)

    def test_face_degraded_when_git_absent(self):
        rc, out = self._face_with("| a |\n", b"| a |\n", git_exists=False)
        self.assertEqual(rc, gs.RC_QUIET)
        self.assertIn("ORDERS-ORIGIN-DELTA: degraded", out)
        self.assertIn("worktree-only behavior", out)

    def test_face_local_read_fail(self):
        paths = dict(gs.DEFAULTS)
        paths["hq_orders"] = os.path.join("Z:", "no", "such", "orders.md")
        rc, out = gs.face_orders_origin_delta(paths)
        self.assertEqual(rc, gs.RC_READ_FAIL)
        self.assertIn("read-fail", out)


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

    def test_live_orders_rows_positive(self):
        # tech#103 live shape lock: the real HQ orders.md is a pipe-row
        # table; a shape change (rows collapsing to 0) must fail here.
        text, _, _ = gs.read_text(gs.DEFAULTS["hq_orders"])
        rows, tail_key = gs.orders_row_stats(text)
        self.assertGreater(rows, 0)
        self.assertTrue(tail_key)

    def test_live_digest_supply_face_present(self):
        # tech#129 live wiring: the face runs against the real cards dir;
        # today's rows are covered by the staged v19 card -> quiet (zero
        # false-touch on an in-batch/consumed round, the seed criterion).
        rc, out = self._run_live()
        self.assertIn("=== DIGEST-SUPPLY (rc=", out)
        self.assertIn(rc, (gs.RC_QUIET, gs.RC_NEW))

    def test_live_orders_origin_delta_face_present(self):
        # tech#133 live wiring: the face runs a real fetch+show (or degrades
        # on network failure -- quiet/degraded/WARN are all legal probe
        # states, never rc 3). Live dogfood R2064: the WARN variant fired
        # with origin 312 vs worktree 311 (the durable 15:2x stuck row).
        rc, out = self._run_live()
        self.assertIn("=== ORDERS-ORIGIN-DELTA (rc=", out)
        self.assertTrue(
            "ORDERS-ORIGIN-DELTA:" in out
            or "ORDERS-ORIGIN-DELTA-WARN:" in out)


if __name__ == "__main__":
    unittest.main()
