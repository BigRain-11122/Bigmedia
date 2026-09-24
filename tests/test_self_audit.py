# -*- coding: utf-8 -*-
"""Unit tests for the weekly self-audit packer (src/os/self_audit.py).

O-20260924-1057: pure functions only - ISO week math and pack rendering.
No probes, no git, real ledgers never touched.

Run:
    python tests/test_self_audit.py
"""
import sys
import unittest
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "os"))

import self_audit as sa  # noqa: E402


class TestIsoWeek(unittest.TestCase):
    def test_known_week(self):
        self.assertEqual("2026-W39", sa.iso_week_of(date(2026, 9, 24)))

    def test_year_boundary_uses_iso_year(self):
        # 2027-01-01 falls in ISO week 53 of 2026
        self.assertEqual("2026-W53", sa.iso_week_of(date(2027, 1, 1)))


class TestRenderPack(unittest.TestCase):
    def test_pack_renders_all_sections(self):
        pack = {
            "week": "2026-W39",
            "collected": "2026-09-24 10:58",
            "probes": [("board_check", 0, "summary: 0 fail"),
                       ("readiness", 1, "4 blocker(s) -> NOT READY")],
            "loop": {"tick": 113, "last_log_head": "R113 ..."},
            "backlog": {"done": 11, "open": 6},
            "orders": {"files": 24, "claimed": 15, "receipted": 6},
            "gates": {"station_reviews": 6, "expert_calls": 2},
            "renders": {"mp4_on_disk": 17, "ledger_rows": 17},
            "tests": {"tail": "OK"},
            "git": {"commits_7d": 170},
        }
        text = sa.render_pack(pack)
        self.assertIn("2026-W39", text)
        self.assertIn("board_check: exit=0", text)
        self.assertIn("readiness: exit=1", text)
        self.assertIn("tick=113", text)
        self.assertIn("done=11 open=6", text)
        self.assertIn("17", text)
        self.assertIn("170", text)
        # judgment checklist present for the loop round to fill
        self.assertIn("1. ", text)
        self.assertIn("5. ", text)

    def test_probe_failure_still_renders(self):
        pack = {
            "week": "2026-W40", "collected": "x",
            "probes": [("readiness", 2, "probe missing")],
            "loop": {"tick": None, "last_log_head": "-"},
            "backlog": {"done": 0, "open": 0},
            "orders": {"files": 0, "claimed": 0, "receipted": 0},
            "gates": {"station_reviews": 0, "expert_calls": 0},
            "renders": {"mp4_on_disk": 0, "ledger_rows": 0},
            "tests": {"tail": "-"},
            "git": {"commits_7d": 0},
        }
        text = sa.render_pack(pack)
        self.assertIn("exit=2", text)
        self.assertIn("tick=None", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
