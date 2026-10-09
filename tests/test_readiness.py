"""Minimal unit tests for the publish-readiness probe (src/readiness.py).

Fixture ledgers live in tests/fixtures/readiness/ - Chinese data files
per the encoding rule; this script and the runtime-made trees stay
pure ASCII (fixture names come from manifest.json). The real repo
sources under docs/ data/ output/ src/os/ are never touched by unit
tests; one CLI case runs the probe against a temp tree, another
against the real repo (read-only smoke, exit 1 expected pre-launch).

Run:
    python tests/test_readiness.py
"""
import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import readiness  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MANIFEST = json.loads((FIXTURES / "manifest.json").read_text(encoding="utf-8"))


def ledger(key):
    return FIXTURES / MANIFEST[key]


def make_dir(case, prefix):
    d = Path(tempfile.mkdtemp(prefix=prefix))
    case.addCleanup(shutil.rmtree, d, ignore_errors=True)
    return d


def make_drafts(case, spec):
    """spec = [(filename, GATE verdict or None)] -> drafts dir."""
    d = make_dir(case, "bs-rdy-drafts-")
    for name, gate in spec:
        text = ("GATE: %s\n" % gate) if gate else "no gate line here\n"
        (d / name).write_text(text, encoding="utf-8")
    return d


def make_renders(case, names, ledger_key=None):
    """names = media filenames; ledger fixture copied in as README.md."""
    d = make_dir(case, "bs-rdy-renders-")
    for n in names:
        (d / n).write_bytes(b"")
    if ledger_key:
        shutil.copy(ledger(ledger_key), d / "README.md")
    return d


def make_root(case, accounts_key, drafts_spec, render_names, render_ledger_key,
              backlog_key):
    """Assemble a fake repo tree for CLI runs; returns its root Path."""
    root = make_dir(case, "bs-rdy-root-")
    (root / "docs").mkdir()
    (root / "data" / "drafts").mkdir(parents=True)
    (root / "src" / "os").mkdir(parents=True)
    (root / "output" / "renders").mkdir(parents=True)
    shutil.copy(ledger(accounts_key), root / "docs" / "accounts.md")
    for name, gate in drafts_spec:
        text = ("GATE: %s\n" % gate) if gate else "no gate line here\n"
        (root / "data" / "drafts" / name).write_text(text, encoding="utf-8")
    renders = root / "output" / "renders"
    for n in render_names:
        (renders / n).write_bytes(b"")
    if render_ledger_key:
        shutil.copy(ledger(render_ledger_key), renders / "README.md")
    shutil.copy(ledger(backlog_key), root / "src" / "os" / "backlog.md")
    return root


def fail_codes(findings):
    return {code for sev, code, _ in findings if sev == "FAIL"}


class AccountsTests(unittest.TestCase):
    def test_flow_and_rows_parsed(self):
        flow, rows, findings = readiness.parse_accounts(ledger("readiness_accounts_ok"))
        self.assertEqual(fail_codes(findings), set())
        self.assertEqual(len(flow), 4)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0][1], flow[2])   # authenticated
        self.assertEqual(rows[1][1], flow[0])   # not registered
        self.assertEqual(rows[2][1], flow[1])   # registered
        for state in flow:  # cleaner must strip ticks and parentheticals
            self.assertNotIn("`", state)
            self.assertNotIn("(", state)
            self.assertNotIn("\uff08", state)

    def test_noflow_fails(self):
        flow, rows, findings = readiness.parse_accounts(ledger("readiness_accounts_noflow"))
        self.assertEqual(fail_codes(findings), {"accounts-flow"})
        self.assertEqual(flow, [])
        self.assertEqual(rows, [])

    def test_bad_status_fails(self):
        flow, rows, findings = readiness.parse_accounts(ledger("readiness_accounts_badstatus"))
        self.assertEqual(fail_codes(findings), {"accounts-row"})
        self.assertEqual(rows[0][1], None)

    def test_missing_first_batch_warns(self):
        _, _, findings = readiness.parse_accounts(ledger("readiness_accounts_nobatch"))
        self.assertEqual(fail_codes(findings), set())
        self.assertEqual({code for _, code, _ in findings}, {"accounts-batch"})

    def test_flow_capture_bounded_to_one_line(self):
        """Real accounts.md shape: flow line without a semicolon, later
        paragraphs carry semicolons and arrows - the capture must not
        run across paragraphs (regression for the R14 real-run bug)."""
        flow, rows, findings = readiness.parse_accounts(ledger("readiness_accounts_multiflow"))
        self.assertEqual(fail_codes(findings), set())
        self.assertEqual(len(flow), 4)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], flow[2])


class GateTests(unittest.TestCase):
    def test_verdicts_parsed(self):
        d = make_drafts(self, [("a.md", "PASS"), ("b.md", "PENDING")])
        gates, findings = readiness.parse_gates(d)
        self.assertEqual(fail_codes(findings), set())
        self.assertEqual(gates["a.md"], "PASS")
        self.assertEqual(gates["b.md"], "PENDING")

    def test_missing_gate_line_fails(self):
        d = make_drafts(self, [("a.md", "PASS"), ("b.md", None)])
        gates, findings = readiness.parse_gates(d)
        self.assertEqual(fail_codes(findings), {"gate-missing"})
        self.assertEqual(gates["b.md"], None)

    def test_missing_dir_fails(self):
        _, findings = readiness.parse_gates(FIXTURES / "no-such-drafts")
        self.assertEqual(fail_codes(findings), {"gate-dir"})


class RenderTests(unittest.TestCase):
    def test_annotated_inventory_passes(self):
        d = make_renders(self, ["alpha.mp4", "beta.wav"], "readiness_renders_ok")
        rows, findings = readiness.parse_renders(d, d / "README.md")
        self.assertEqual(fail_codes(findings), set())
        self.assertEqual([s for _, s in rows],
                         [readiness.TEST_MARK, readiness.TEST_MARK])

    def test_unannotated_fails(self):
        d = make_renders(self, ["alpha.mp4"], "readiness_renders_bare")
        rows, findings = readiness.parse_renders(d, d / "README.md")
        self.assertEqual(fail_codes(findings), {"render-unannot"})
        self.assertIsNone(rows[0][1])

    def test_production_mark_passes(self):
        # D-BS-06 gate-open era: ledger rows carrying the production mark
        # (e.g. "production.batches") count as annotated inventory.
        d = make_renders(self, ["gamma.mp4"], "readiness_renders_product")
        rows, findings = readiness.parse_renders(d, d / "README.md")
        self.assertEqual(fail_codes(findings), set())
        self.assertEqual([s for _, s in rows], [readiness.PRODUCT_MARK])

    def test_superseded_mark_passes_and_prose_guard(self):
        # #23 v14 rectification-batch era: rows superseded by re-renders
        # are a third legal state ("has been ... superseded" cells), while
        # prose lines that merely mention replacement without the prefix
        # stay unannotated (false-hit guard).
        d = make_renders(self, ["gamma.mp4", "delta.mp4"],
                         "readiness_renders_superseded")
        rows, findings = readiness.parse_renders(d, d / "README.md")
        self.assertEqual(fail_codes(findings), {"render-unannot"})
        marks = dict(rows)
        self.assertEqual(marks["gamma.mp4"], readiness.SUPERSEDED_MARK)
        self.assertIsNone(marks["delta.mp4"])

    def test_disposed_mark_passes_and_prose_guard(self):
        # D-BS-08 escalation-disposal era: rows disposed by ruling stay
        # on disk as archive rows ("disposed ... archived" cells) = fourth
        # legal state, while prose lines that merely mention discarding
        # without the archive qualifier stay unannotated (false-hit guard).
        d = make_renders(self, ["gamma.mp4", "delta.mp4"],
                         "readiness_renders_disposed")
        rows, findings = readiness.parse_renders(d, d / "README.md")
        self.assertEqual(fail_codes(findings), {"render-unannot"})
        marks = dict(rows)
        self.assertEqual(marks["gamma.mp4"], readiness.DISPOSED_MARK)
        self.assertIsNone(marks["delta.mp4"])

    def test_product_slot_mark_passes_and_prose_guard(self):
        # R512 release-schedule D-slot era: pre-production goods registered
        # into a schedule slot (LC-001 D15 first case) are a fifth legal
        # state ("slot-filled production" cells), while prose lines that
        # merely say the slot was filled without the production prefix
        # stay unannotated (false-hit guard).
        d = make_renders(self, ["gamma.mp4", "delta.mp4"],
                         "readiness_renders_product_slot")
        rows, findings = readiness.parse_renders(d, d / "README.md")
        self.assertEqual(fail_codes(findings), {"render-unannot"})
        marks = dict(rows)
        self.assertEqual(marks["gamma.mp4"], readiness.PRODUCT_SLOT_MARK)
        self.assertIsNone(marks["delta.mp4"])

    def test_multi_mention_keeps_highest_state(self):
        # R1802 display-layer fix: a file mentioned in several lines
        # keeps its highest-precedence real state (production states
        # beat archive states beat the generic test-piece mark).
        d = make_renders(self, ["gamma.mp4"], None)
        (d / "README.md").write_text(
            "| gamma.mp4 | %s | prose mention |\n"
            "| gamma.mp4 | %s | registered row |\n" % (
                readiness.TEST_MARK, readiness.PRODUCT_SLOT_MARK),
            encoding="utf-8")
        rows, findings = readiness.parse_renders(d, d / "README.md")
        self.assertEqual(fail_codes(findings), set())
        self.assertEqual(rows[0][1], readiness.PRODUCT_SLOT_MARK)

    def test_missing_ledger_fails(self):
        d = make_renders(self, ["alpha.mp4"], None)
        rows, findings = readiness.parse_renders(d, d / "README.md")
        self.assertEqual(fail_codes(findings), {"render-ledger"})
        self.assertIsNone(rows[0][1])

    def test_stale_ledger_row_fails(self):
        d = make_renders(self, ["alpha.mp4"], "readiness_renders_stale")
        _, findings = readiness.parse_renders(d, d / "README.md")
        self.assertEqual(fail_codes(findings), {"render-stale"})

    def test_empty_renders_dir_clean(self):
        d = make_renders(self, [], None)
        rows, findings = readiness.parse_renders(d, d / "README.md")
        self.assertEqual(findings, [])
        self.assertEqual(rows, [])

    def test_missing_renders_dir_fails(self):
        _, findings = readiness.parse_renders(FIXTURES / "no-such-renders",
                                              FIXTURES / "no-such-renders" / "README.md")
        self.assertEqual(fail_codes(findings), {"render-dir"})


class BacklogFlagTests(unittest.TestCase):
    def test_flags_parsed_and_filtered(self):
        needs, suspended = readiness.parse_backlog_flags(ledger("readiness_backlog_flags"))
        self.assertEqual([n for n, _ in needs], ["3"])
        self.assertEqual([n for n, _ in suspended], ["4"])

    def test_clean_board_has_no_flags(self):
        needs, suspended = readiness.parse_backlog_flags(ledger("readiness_backlog_clean"))
        self.assertEqual(needs, [])
        self.assertEqual(suspended, [])


class BlockerTests(unittest.TestCase):
    def test_blockers_built_from_state(self):
        flow, rows, findings = readiness.parse_accounts(ledger("readiness_accounts_ok"))
        self.assertEqual(fail_codes(findings), set())
        gates = {"a.md": "PENDING"}
        needs = [("9", "x lane")]
        blockers = readiness.build_blockers(flow, rows, gates, needs)
        self.assertEqual(len(blockers), 3)
        text = "\n".join(blockers)
        self.assertIn("first-launch accounts not open", text)
        self.assertIn("1/1 draft(s) not GATE PASS", text)
        self.assertIn("decision pending: #9 x lane", text)

    def test_ready_state_has_no_blockers(self):
        flow, rows, _ = readiness.parse_accounts(ledger("readiness_accounts_ready"))
        blockers = readiness.build_blockers(flow, rows, {"a.md": "PASS"}, [])
        self.assertEqual(blockers, [])


class ReportTests(unittest.TestCase):
    def test_template_placeholders_all_filled(self):
        template = (REPO / "src" / "os" / "readiness_template.md").read_text(encoding="utf-8")
        flow, rows, _ = readiness.parse_accounts(ledger("readiness_accounts_ok"))
        render_rows = [("alpha.mp4", readiness.TEST_MARK)]
        report = readiness.build_report(template, "ts", flow, rows,
                                        {"a.md": "PENDING"}, render_rows,
                                        [("3", "clause")], [], ["b1"], [])
        for key in readiness.PLACEHOLDERS:
            self.assertNotIn("{%s}" % key, report)
        self.assertIn(readiness.TEST_MARK, report)

    def test_report_shows_real_ledger_states(self):
        # R1802 display-layer fix: the 3rd section shows each ledger
        # row's real state, not a hard-coded test-piece string.
        template = (REPO / "src" / "os" / "readiness_template.md").read_text(encoding="utf-8")
        flow, rows, _ = readiness.parse_accounts(ledger("readiness_accounts_ok"))
        render_rows = [("a.mp4", readiness.PRODUCT_SLOT_MARK),
                       ("b.mp4", readiness.PRODUCT_MARK),
                       ("c.mp4", readiness.SUPERSEDED_MARK),
                       ("d.mp4", readiness.DISPOSED_MARK),
                       ("e.mp4", readiness.TEST_MARK),
                       ("f.mp4", None)]
        report = readiness.build_report(template, "ts", flow, rows,
                                        {"a.md": "PENDING"}, render_rows,
                                        [], [], [], [])
        for mark in (readiness.PRODUCT_SLOT_MARK, readiness.PRODUCT_MARK,
                     readiness.SUPERSEDED_MARK, readiness.DISPOSED_MARK,
                     readiness.TEST_MARK, readiness.MISSING_MARK):
            self.assertIn(mark, report)
        self.assertIn("- none", report)  # empty suspended/findings lists


class AsrPinTests(unittest.TestCase):
    """P-2 pinned-model observation (R1302): WARN only when the pin
    record declares weights that are no longer on disk (sweep damage)."""

    def _make_record(self, root, files):
        (root / "data" / "pipeline").mkdir(parents=True, exist_ok=True)
        (root / "data" / "pipeline" / "asr-pin.json").write_text(
            json.dumps({"model": "medium",
                        "dir": "data/assets/models/faster-whisper-medium",
                        "files": files}), encoding="utf-8")

    def test_missing_record_is_silent(self):
        root = make_dir(self, "bs-rdy-pin-")
        self.assertEqual(
            readiness.parse_asr_pin(root / "data" / "pipeline" / "asr-pin.json"), [])

    def test_intact_pin_has_no_findings(self):
        root = make_dir(self, "bs-rdy-pin-")
        base = root / "data" / "assets" / "models" / "faster-whisper-medium"
        base.mkdir(parents=True)
        for f in ("model.bin", "config.json"):
            (base / f).write_bytes(b"x")
        self._make_record(root, ["model.bin", "config.json"])
        self.assertEqual(
            readiness.parse_asr_pin(root / "data" / "pipeline" / "asr-pin.json"), [])

    def test_swept_weights_warn(self):
        root = make_dir(self, "bs-rdy-pin-")
        self._make_record(root, ["model.bin", "config.json"])
        findings = readiness.parse_asr_pin(root / "data" / "pipeline" / "asr-pin.json")
        codes = {code for _, code, _ in findings}
        sevs = {sev for sev, _, _ in findings}
        self.assertEqual(codes, {"asr-pin"})
        self.assertEqual(sevs, {"WARN"})


class CliTests(unittest.TestCase):
    def test_ready_tree_exits_zero(self):
        root = make_root(self, "readiness_accounts_ready", [("d1.md", "PASS")],
                         [], None, "readiness_backlog_clean")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = readiness.main(["readiness.py", "--root", str(root)])
        self.assertEqual(rc, 0)
        self.assertIn("READY", buf.getvalue())

    def test_not_ready_tree_exits_one(self):
        root = make_root(self, "readiness_accounts_ok", [("d1.md", "PENDING")],
                         ["alpha.mp4"], None, "readiness_backlog_flags")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = readiness.main(["readiness.py", "--root", str(root)])
        self.assertEqual(rc, 1)
        out = buf.getvalue()
        self.assertIn("NOT READY", out)
        self.assertIn("render-ledger", out)
        self.assertIn("decision pending: #3", out)

    def test_out_file_written(self):
        root = make_root(self, "readiness_accounts_ready", [("d1.md", "PASS")],
                         [], None, "readiness_backlog_clean")
        out = make_dir(self, "bs-rdy-out-") / "report.md"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = readiness.main(["readiness.py", "--root", str(root), "--out", str(out)])
        self.assertEqual(rc, 0)
        self.assertTrue(out.is_file())
        self.assertIn("report written", buf.getvalue())

    def test_bad_flag_exits_two(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = readiness.main(["readiness.py", "--bogus"])
        self.assertEqual(rc, 2)

    def test_real_repo_smoke_not_ready(self):
        """Read-only smoke on the real repo: pre-launch state must exit 1.

        Draft-GATE counts drift as production batches flip verdicts
        (D-BS-06 gate-open era), so assert the pattern, not the count.
        """
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = readiness.main(["readiness.py"])
        self.assertEqual(rc, 1)
        out = buf.getvalue()
        self.assertIn("NOT READY", out)
        self.assertIn("draft(s) not GATE PASS", out)
        self.assertIn(readiness.TEST_MARK, out)  # real render ledger annotated


class SummaryModeTests(unittest.TestCase):
    """--summary routine face (tech#11): count lines + full
    blockers/findings, no per-file tables; same analysis and exit code."""

    def test_summary_counts_and_blockers_no_tables(self):
        root = make_root(self, "readiness_accounts_ok",
                         [("d1.md", "PASS"), ("d2.md", "PENDING")],
                         ["gamma.mp4", "delta.mp4"], "readiness_renders_superseded",
                         "readiness_backlog_flags")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = readiness.main(["readiness.py", "--root", str(root), "--summary"])
        self.assertEqual(rc, 1)
        out = buf.getvalue()
        self.assertIn("readiness summary (gen", out)
        self.assertIn("- gates: 2 drafts -> PASS=1, PENDING=1", out)
        self.assertIn("renders: 2 media ->", out)
        self.assertIn("- blocker:", out)
        self.assertIn("decision pending: #3", out)  # needs-CEO item kept in full
        self.assertNotIn("|", out)  # no markdown tables in the compact face
        self.assertIn("NOT READY", out)

    def test_summary_out_file_still_writes_full_report(self):
        root = make_root(self, "readiness_accounts_ready", [("d1.md", "PASS")],
                         [], None, "readiness_backlog_clean")
        out = make_dir(self, "bs-rdy-sum-out-") / "report.md"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = readiness.main(["readiness.py", "--root", str(root),
                                 "--summary", "--out", str(out)])
        self.assertEqual(rc, 0)
        self.assertTrue(out.is_file())
        text = out.read_text(encoding="utf-8")
        self.assertIn("|", text)  # file artifact stays the full report
        self.assertIn("report written", buf.getvalue())

    def test_real_repo_summary_smoke(self):
        """Read-only smoke: compact face runs on the real repo, keeps
        the verdict line, drops every table row."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = readiness.main(["readiness.py", "--summary"])
        self.assertEqual(rc, 1)
        out = buf.getvalue()
        self.assertIn("readiness summary (gen", out)
        self.assertIn("renders:", out)
        self.assertIn("NOT READY", out)
        self.assertNotIn("|", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
