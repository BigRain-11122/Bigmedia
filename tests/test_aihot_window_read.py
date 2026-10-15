"""Hermetic tests for src/os/aihot_window_read.py (tech#159).

The real psql/localhost face is NEVER touched here (R1893 stub law): the
runner is injected. Live smoke evidence lives in
data/pipeline/aihot-evidence/r2235_t159_smoke.txt instead.
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.os import aihot_window_read as awr  # noqa: E402


def hexify(text):
    return text.encode("utf-8").hex()


class FakeRunner:
    """Injected runner: returns canned psql output per section marker."""

    def __init__(self, table):
        # table: dict keyed by a distinctive substring of the section SQL
        self.table = table
        self.calls = []

    def __call__(self, sql, timeout=180):
        self.calls.append(sql)
        for key, (rc, out, err) in self.table.items():
            if key in sql:
                return rc, out, err
        return 1, "", "unexpected section"


C_BROKEN = "e5b08f" + "ffffff"  # 小 + invalid tail bytes


class DecodeHexTitleTests(unittest.TestCase):
    def test_clean_title(self):
        text, bad = awr.decode_hex_title(hexify("小巧好用"))
        self.assertEqual(text, "小巧好用")
        self.assertFalse(bad)

    def test_broken_bytes_marked(self):
        text, bad = awr.decode_hex_title(C_BROKEN)
        self.assertTrue(bad)
        self.assertIn("\ufffd", text)

    def test_non_hex_input(self):
        text, bad = awr.decode_hex_title("zznot-hex")
        self.assertTrue(bad)
        self.assertEqual(text, "<HEX-ERR>")

    def test_empty(self):
        text, bad = awr.decode_hex_title("")
        self.assertEqual(text, "")
        self.assertFalse(bad)


class AssertAsciiTests(unittest.TestCase):
    def test_ascii_passes(self):
        awr.assert_ascii("SELECT 1 WHERE id='json-zhihu-hot';")

    def test_cjk_rejected(self):
        with self.assertRaises(ValueError):
            awr.assert_ascii("SELECT '小巧';")

    def test_non_ascii_rejected_via_run_query(self):
        with self.assertRaises(ValueError):
            awr.run_query(lambda s, t: (0, "", ""), "SELECT '小巧';")


class SqlBuilderTests(unittest.TestCase):
    def setUp(self):
        self.since = "2026-10-14 08:00"
        self.until = "2026-10-15 08:00"

    def test_all_sections_ascii(self):
        for sql in [awr.section_a(self.since, self.until),
                    awr.section_b(self.since, self.until, "json-zhihu-hot", 15),
                    awr.section_c(self.since, self.until, 15),
                    awr.section_d(self.since, self.until),
                    awr.section_e(self.since, self.until, "json-zhihu-hot"),
                    awr.section_f_total(self.since, self.until),
                    awr.section_f_census(self.since, self.until)]:
            awr.assert_ascii(sql)

    def test_window_clause_in_every_section(self):
        for sql in [awr.section_a(self.since, self.until),
                    awr.section_b(self.since, self.until, "s", 3),
                    awr.section_c(self.since, self.until, 3),
                    awr.section_d(self.since, self.until),
                    awr.section_e(self.since, self.until, "s")]:
            self.assertIn("a.created_at >= '%s'" % self.since, sql)
            self.assertIn("a.created_at < '%s'" % self.until, sql)

    def test_hex_transport_in_title_sections(self):
        self.assertIn("encode(art.title::bytea,'hex')",
                      awr.section_c(self.since, self.until, 15))
        self.assertIn("encode(art.title::bytea,'hex')",
                      awr.section_d(self.since, self.until))
        self.assertNotIn("left(", awr.section_c(self.since, self.until, 15))

    def test_c_uses_score_order_and_limit(self):
        sql = awr.section_c(self.since, self.until, 12)
        self.assertIn("ORDER BY a.score DESC LIMIT 12", sql)

    def test_d_uses_analyses_created_at_and_prompt_version(self):
        sql = awr.section_d(self.since, self.until)
        self.assertIn("a.prompt_version", sql)
        self.assertIn("a.created_at", sql)  # exists column (R2231 D bug fixed)
        self.assertIn("WHERE a.selected", sql)


class FSectionTests(unittest.TestCase):
    """tech#179: F sections mirror composeDaily judgedReports (timeline_at face)."""

    def setUp(self):
        self.since = "2026-10-14 08:00"
        self.until = "2026-10-15 08:00"

    def test_f_window_on_timeline_at_not_created_at(self):
        for sql in [awr.section_f_total(self.since, self.until),
                    awr.section_f_census(self.since, self.until)]:
            self.assertIn("p.timeline_at >= '%s'" % self.since, sql)
            self.assertIn("p.timeline_at < '%s'" % self.until, sql)
            self.assertNotIn("created_at", sql)  # A-E face must not leak in

    def test_f_mirrors_judgedreports_filters(self):
        for sql in [awr.section_f_total(self.since, self.until),
                    awr.section_f_census(self.since, self.until)]:
            self.assertIn("FROM publications p", sql)
            self.assertIn("p.visibility = 'public'", sql)
            self.assertIn("p.eligible", sql)
            self.assertIn("NOT p.selected OR p.visible_after <= '%s'"
                          % self.until, sql)
            self.assertIn("p.score IS NOT NULL", sql)
            self.assertIn("NOT p.backfill", sql)

    def test_f_census_shape_matches_section_a(self):
        sql = awr.section_f_census(self.since, self.until)
        for frag in ["count(*) FILTER (WHERE p.score >= 60)",
                     "count(*) FILTER (WHERE p.score >= 55)",
                     "count(*) FILTER (WHERE p.selected)"]:
            self.assertIn(frag, sql)

    def _fake_with_f(self, f_total_out, f_census_out):
        return FakeRunner({
            "GROUP BY art.source_id": (0, "", ""),
            "json-zhihu-hot' AND": (0, "", ""),
            "ORDER BY a.score DESC LIMIT 15": (0, "", ""),
            "WHERE a.selected": (0, "", ""),
            "floor(a.score)": (0, "", ""),
            "count(*) FROM publications": (0, f_total_out, ""),
            "GROUP BY p.source_id": (0, f_census_out, ""),
        })

    def test_collect_f_rows_and_semantics_note(self):
        runner = self._fake_with_f("278\n", "json-zhihu-hot|40|58.0|0|1|0\n")
        report, errs, bad = awr.collect(runner, "S", "U", "json-zhihu-hot", 15)
        self.assertEqual(errs, [])
        self.assertEqual(bad, 0)
        self.assertIn('"judged_total": "278"', report)
        self.assertIn('"judged": "40"', report)
        self.assertIn("== F judged_total (timeline_at face) ==", report)
        self.assertIn("== F judged_census (timeline_at face) ==", report)
        self.assertIn("A-E = analyses.created_at", report)
        self.assertIn("F = publications.timeline_at", report)

    def test_f_section_err_counted(self):
        boom = self._fake_with_f("", "")
        boom.table["count(*) FROM publications"] = (1, "", "boom")
        report, errs, bad = awr.collect(boom, "S", "U", "json-zhihu-hot", 15)
        self.assertEqual(errs, ["F judged_total (timeline_at face)"])
        self.assertIn("== F judged_total (timeline_at face) == ERR boom", report)


class CollectTests(unittest.TestCase):
    def _fake(self, c_out="", d_out="", b_out="", a_out="", e_out="",
              f_total_out="", f_census_out=""):
        # key order matters: B's SQL also contains the LIMIT marker, so the
        # B-specific key must be matched first.
        return FakeRunner({
            "GROUP BY art.source_id": (0, a_out, ""),
            "json-zhihu-hot' AND": (0, b_out, ""),
            "ORDER BY a.score DESC LIMIT 15": (0, c_out, ""),
            "WHERE a.selected": (0, d_out, ""),
            "floor(a.score)": (0, e_out, ""),
            "count(*) FROM publications": (0, f_total_out, ""),
            "GROUP BY p.source_id": (0, f_census_out, ""),
        })

    def test_happy_path_all_sections(self):
        c_row = "73.00|rss-x|%s\n" % hexify("hello title")
        runner = self._fake(c_out=c_row,
                            a_out="src-a|100|56.0|0|1|0\n",
                            b_out="51.0|f|%s\n" % hexify("zhihu title"),
                            d_out="58.0|json-zhihu-hot|selection-score@1|"
                                  "2026-10-14 08:30|%s\n" % hexify("selected one"),
                            e_out="51|1\n",
                            f_total_out="278\n",
                            f_census_out="json-zhihu-hot|40|58.0|0|1|0\n")
        report, errs, bad = awr.collect(runner, "S", "U", "json-zhihu-hot", 15)
        self.assertEqual(errs, [])
        self.assertEqual(bad, 0)
        for header in ["A per-source", "B json-zhihu-hot top",
                       "C top15 any", "D selected_ledger",
                       "E json-zhihu-hot band",
                       "F judged_total (timeline_at face)",
                       "F judged_census (timeline_at face)"]:
            self.assertIn("== %s ==" % header, report)
        self.assertIn('"title": "hello title"', report)
        self.assertIn('"prompt_version": "selection-score@1"', report)
        self.assertIn('"title": "selected one"', report)
        self.assertIn('"judged_total": "278"', report)

    def test_bad_utf8_row_counted_and_marked(self):
        c_row = "58.00|json-zhihu-hot|%s\n" % C_BROKEN
        runner = self._fake(c_out=c_row)
        report, errs, bad = awr.collect(runner, "S", "U", "json-zhihu-hot", 15)
        self.assertEqual(bad, 1)
        self.assertIn("[bad_utf8 rows in section: 1]", report)
        self.assertIn('"bad_utf8": true', report)
        self.assertEqual(errs, [])

    def test_section_err_captured_not_fatal(self):
        boom = {"GROUP BY art.source_id": (1, "", "boom"),
                "ORDER BY a.score DESC LIMIT": (1, "", "boom"),
                "WHERE a.selected": (1, "", "boom"),
                "floor(a.score)": (1, "", "boom"),
                "json-zhihu-hot' AND": (1, "", "boom"),
                "count(*) FROM publications": (1, "", "boom"),
                "GROUP BY p.source_id": (1, "", "boom")}
        report, errs, bad = awr.collect(FakeRunner(boom), "S", "U", "json-zhihu-hot", 15)
        self.assertEqual(len(errs), 7)
        self.assertEqual(report.count("ERR boom"), 7)

    def test_a_row_without_hex_ignored_for_bad_count(self):
        runner = self._fake(a_out="src|10|55.0|0|0|0\n")
        report, errs, bad = awr.collect(runner, "S", "U", "json-zhihu-hot", 15)
        self.assertEqual(bad, 0)

    def test_empty_sections_render_no_rows(self):
        runner = self._fake()
        report, errs, bad = awr.collect(runner, "S", "U", "json-zhihu-hot", 15)
        self.assertEqual(errs, [])
        self.assertEqual(report.count("(no rows)"), 7)

    def test_sql_passed_to_runner_is_ascii(self):
        runner = self._fake()
        awr.collect(runner, "S", "U", "json-zhihu-hot", 15)
        for sql in runner.calls:
            awr.assert_ascii(sql)


class CliTests(unittest.TestCase):
    def test_main_rc2_on_psql_unreachable(self):
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "ev.txt")
            saved = awr.PSQL
            awr.PSQL = os.path.join(td, "no-such-psql.exe")
            try:
                rc = awr.main(["--since", "2026-10-14 08:00",
                               "--until", "2026-10-14 09:00",
                               "--out", out])
            finally:
                awr.PSQL = saved
            self.assertEqual(rc, 2)

    def test_main_collect_path_with_patched_runner(self):
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "ev.txt")
            fake = self._fake_all()
            saved = awr.default_runner
            awr.default_runner = fake
            try:
                rc = awr.main(["--since", "2026-10-14 08:00",
                               "--until", "2026-10-14 09:00",
                               "--out", out])
            finally:
                awr.default_runner = saved
            self.assertEqual(rc, 0)
            with open(out, encoding="utf-8") as f:
                body = f.read()
            self.assertIn("== C top15 any ==", body)
            self.assertIn('"title": "cli row"', body)

    def _fake_all(self):
        c_row = "58.00|src|%s\n" % hexify("cli row")
        return FakeRunner({
            "GROUP BY art.source_id": (0, "", ""),
            "json-zhihu-hot' AND": (0, "", ""),
            "ORDER BY a.score DESC LIMIT 15": (0, c_row, ""),
            "WHERE a.selected": (0, "", ""),
            "floor(a.score)": (0, "", ""),
            "count(*) FROM publications": (0, "", ""),
            "GROUP BY p.source_id": (0, "", ""),
        })


class EvidenceSmokeFileTests(unittest.TestCase):
    """The committed live-smoke evidence must carry the fixed C section."""

    EVIDENCE = os.path.join(os.path.dirname(__file__), "..", "data",
                            "pipeline", "aihot-evidence",
                            "r2235_t159_smoke.txt")

    def test_file_exists_and_c_section_has_titles(self):
        if not os.path.exists(self.EVIDENCE):
            self.skipTest("smoke evidence not generated in this checkout")
        with open(self.EVIDENCE, encoding="utf-8") as f:
            body = f.read()
        self.assertIn("== C top15 any ==", body)
        self.assertNotIn("== C top15 any == ERR", body)
        rows = [l for l in body.splitlines()
                if l.startswith("{") and '"bad_utf8"' in l]
        self.assertTrue(rows)
        for l in rows:
            row = json.loads(l)
            self.assertIn("title", row)
            self.assertIsInstance(row["bad_utf8"], bool)


if __name__ == "__main__":
    unittest.main()
