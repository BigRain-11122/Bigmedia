# -*- coding: utf-8 -*-
"""Tests for src/gpu_attribution.py (tech#16, P2 queue)."""

import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import gpu_attribution as ga


def write_ledger(tmp, rows):
    p = tmp / "samples.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n",
                 encoding="utf-8")
    return p


class ParseRowsTest(unittest.TestCase):
    def test_skips_malformed_and_out_of_window(self):
        rows = [
            {"ts": "2026-10-01T10:00:00", "util_pct": 5.0,
             "mem_used_mib": 6000.0, "power_w": 30.0},
            "not json",
            {"ts": "bad-date", "util_pct": 50.0},
            {"ts": "2026-10-02T10:00:00", "util_pct": "x"},
            {"ts": "2026-09-20T10:00:00", "util_pct": 90.0},
            {"ts": "2026-10-03T10:00:00", "util_pct": 80.0,
             "mem_used_mib": 11000.0, "power_w": 200.0},
        ]
        p = write_ledger(Path(self.enterContext(tempfile.TemporaryDirectory())), rows)
        out = ga.parse_rows(p, since="2026-10-01", until="2026-10-05")
        self.assertEqual(len(out), 2)  # malformed + bad date + str util dropped
        self.assertEqual(out[0][1], 5.0)
        self.assertEqual(out[1][1], 80.0)
        self.assertEqual(out[1][2], 11000.0)

    def test_missing_ledger_raises_honest_error(self):
        with self.assertRaises(SystemExit):
            ga.parse_rows(Path("Z:/nope/missing.jsonl"))


class BandsAndWindowsTest(unittest.TestCase):
    def test_band_stats_counts_and_shares(self):
        rows = [(None, 2.0, None, None), (None, 15.0, None, None),
                (None, 40.0, None, None), (None, 90.0, None, None),
                (None, 8.0, None, None)]
        bands, total = ga.band_stats(rows)
        self.assertEqual(total, 5)
        self.assertEqual(bands["<10 (idle/keep-warm)"][0], 2)
        self.assertEqual(bands["10-30 (light)"][0], 1)
        self.assertEqual(bands["30-70 (workload)"][0], 1)
        self.assertEqual(bands[">=70 (saturated)"][0], 1)
        self.assertAlmostEqual(bands["<10 (idle/keep-warm)"][1], 40.0)

    def test_watch_windows_and_streak(self):
        base = datetime(2026, 10, 1, 0)
        rows = []
        for i in range(24):  # four 6h windows: 5% 5% 5% 60%
            util = 5.0 if i < 18 else 60.0
            rows.append((base.replace(hour=i), util, None, None))
        wins = ga.watch_windows_low(rows)
        self.assertEqual(len(wins), 4)
        self.assertTrue(wins[0][3] and wins[1][3] and wins[2][3])
        self.assertFalse(wins[3][3])
        self.assertEqual(ga.consecutive_low_windows(wins), 3)

    def test_full_report_on_ledger_fixture(self):
        rows = [
            {"ts": "2026-10-01T01:00:00", "util_pct": 5.0,
             "mem_used_mib": 6600.0, "power_w": 30.0},
            {"ts": "2026-10-01T02:00:00", "util_pct": 100.0,
             "mem_used_mib": 11500.0, "power_w": 210.0},
            {"ts": "2026-10-01T03:00:00", "util_pct": 95.0,
             "mem_used_mib": 11500.0, "power_w": 200.0},
        ]
        p = write_ledger(Path(self.enterContext(tempfile.TemporaryDirectory())), rows)
        rep = ga.analyze(p, since="2026-10-01", until="2026-10-02")
        self.assertEqual(rep["n"], 3)
        self.assertAlmostEqual(rep["mean_util"], 66.7, places=1)
        self.assertEqual(rep["max_util"], 100.0)
        self.assertEqual(rep["mem_baseline_mib"], 6600.0)
        # cross-check anchor: weekly reader mean on the same window
        # (weekly_report.in_window compares against date objects)
        from datetime import date
        from weekly_report import gpu_ledger_weekly
        wk = gpu_ledger_weekly(p, date(2026, 10, 1), date(2026, 10, 2))
        self.assertEqual(wk["mean"], 67)  # round(66.67)


if __name__ == "__main__":
    unittest.main()
