"""Minimal unit tests for the board consistency probe (src/board_check.py).

Ledger fixtures live in tests/fixtures/board/ - Chinese data files per
the encoding rule; this script and the runtime-made draft files stay
pure ASCII (fixture names come from manifest.json). The real ledger
and real drafts under data/ are never touched (production pause, CEO
order O-20260923-1525-bm-a).

Run:
    python tests/test_board_check.py
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

import board_check  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MANIFEST = json.loads((FIXTURES / "manifest.json").read_text(encoding="utf-8"))


def ledger(key):
    return FIXTURES / MANIFEST[key]


def make_drafts(case, names):
    """Create a temp drafts dir with empty .md files; return its Path."""
    d = Path(tempfile.mkdtemp(prefix="bs-board-"))
    case.addCleanup(shutil.rmtree, d, ignore_errors=True)
    for n in names:
        (d / n).write_text("fixture\n", encoding="utf-8")
    return d


def fail_codes(findings):
    return {code for sev, code, _ in findings if sev == "FAIL"}


class BoardConsistencyTests(unittest.TestCase):
    def test_consistent_board_passes(self):
        drafts = make_drafts(self, ["20260923-BS-901-gzh-v1.md", "20260923-BS-901-sph-v1.md"])
        findings, stats = board_check.check_board(ledger("board_ideas_ok"), drafts)
        self.assertEqual(fail_codes(findings), set())
        self.assertEqual(stats["ideas"], 3)
        self.assertEqual(stats["drafts"], 2)
        self.assertEqual(stats["in_prod"], 1)

    def test_overstated_production_fails(self):
        drafts = make_drafts(self, [])
        findings, _ = board_check.check_board(ledger("board_ideas_overstate"), drafts)
        self.assertEqual(fail_codes(findings), {"overstate"})

    def test_stale_ledger_fails(self):
        drafts = make_drafts(self, ["20260923-BS-902-x-v1.md"])
        findings, _ = board_check.check_board(ledger("board_ideas_stale"), drafts)
        self.assertEqual(fail_codes(findings), {"stale"})

    def test_orphan_draft_fails(self):
        drafts = make_drafts(self, ["20260923-BS-901-gzh-v1.md", "20260923-BS-999-x-v1.md"])
        findings, _ = board_check.check_board(ledger("board_ideas_ok"), drafts)
        self.assertEqual(fail_codes(findings), {"orphan"})

    def test_duplicate_id_fails(self):
        drafts = make_drafts(self, ["20260923-BS-901-gzh-v1.md"])
        findings, _ = board_check.check_board(ledger("board_ideas_dup"), drafts)
        self.assertEqual(fail_codes(findings), {"dup-id"})

    def test_unknown_status_fails(self):
        drafts = make_drafts(self, ["20260923-BS-901-gzh-v1.md"])
        findings, _ = board_check.check_board(ledger("board_ideas_badstatus"), drafts)
        self.assertEqual(fail_codes(findings), {"bad-status"})

    def test_missing_flow_line_fails(self):
        drafts = make_drafts(self, [])
        findings, _ = board_check.check_board(ledger("board_ideas_noflow"), drafts)
        self.assertEqual(fail_codes(findings), {"vocab"})

    def test_malformed_draft_name_fails(self):
        drafts = make_drafts(self, ["20260923-BS-901-gzh-v1.md", "20260923-no-id-v1.md"])
        findings, _ = board_check.check_board(ledger("board_ideas_ok"), drafts)
        self.assertEqual(fail_codes(findings), {"bad-name"})

    def test_missing_drafts_dir_fails(self):
        findings, _ = board_check.check_board(ledger("board_ideas_ok"), FIXTURES / "no-such-dir")
        self.assertEqual(fail_codes(findings), {"drafts-dir"})


class CliTests(unittest.TestCase):
    def test_exit_zero_on_consistent_board(self):
        drafts = make_drafts(self, ["20260923-BS-901-gzh-v1.md"])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = board_check.main(["board_check", str(ledger("board_ideas_ok")), str(drafts)])
        self.assertEqual(rc, 0)
        self.assertIn("0 fail", buf.getvalue())

    def test_exit_one_on_inconsistent_board(self):
        drafts = make_drafts(self, [])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = board_check.main(["board_check", str(ledger("board_ideas_overstate")), str(drafts)])
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
