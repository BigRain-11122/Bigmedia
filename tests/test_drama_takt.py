# -*- coding: utf-8 -*-
"""Tests for tools/drama_takt_probe.py (P3 #1 takt probe)."""
import os
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from drama_takt_probe import (  # noqa: E402
    artifact_table,
    chain_span,
    extract_chain,
    parse_round_ts,
)

SAMPLE_LOG = [
    "2026-10-09 00:52 R1780: 生产轮·AIHOT compose 位读数",
    "2026-10-09 01:28 R1782: 生产轮·#108 L-剧漫剧 PoC 起链腿交付",
    "2026-10-09 01:04x R1783: 生产轮·#108 CosyVoice3 运行时装包腿交付毕",
    "2026-10-09 04:33:24 R1788 addendum: SDXL pull COMPLETE within round",
    "2026-10-09 07:22 R1795: 生产轮·#108 MD-0001 E8 终审+M4+F-168 登记毕",
    "2026-10-09 21:0x R1842: 等待窗 P2 生产轮·tech#28 交付",
    "random non-round line",
]


class ParseRoundTsTests(unittest.TestCase):
    def test_plain_minute(self):
        self.assertEqual(parse_round_ts(SAMPLE_LOG[0]), ("2026-10-09", 0, 52, 1780))

    def test_seconds_and_addendum(self):
        self.assertEqual(parse_round_ts(SAMPLE_LOG[3]), ("2026-10-09", 4, 33, 1788))

    def test_minute_placeholder_x(self):
        # "01:04x" -> minute 04 (x dropped)
        self.assertEqual(parse_round_ts(SAMPLE_LOG[2]), ("2026-10-09", 1, 4, 1783))

    def test_hour_minute_placeholder(self):
        # "21:0x" -> hour 21 minute 0
        self.assertEqual(parse_round_ts(SAMPLE_LOG[5]), ("2026-10-09", 21, 0, 1842))

    def test_non_round_line(self):
        self.assertIsNone(parse_round_ts(SAMPLE_LOG[6]))


class ExtractChainTests(unittest.TestCase):
    def test_filters_to_chain_window_and_keeps_order(self):
        chain = extract_chain(SAMPLE_LOG)
        self.assertEqual([r["round"] for r in chain], [1782, 1783, 1788, 1795])
        for r in chain:
            self.assertTrue(r["head"])
        # out-of-window rounds excluded
        self.assertNotIn(1780, [r["round"] for r in chain])
        self.assertNotIn(1842, [r["round"] for r in chain])

    def test_custom_window(self):
        chain = extract_chain(SAMPLE_LOG, first=1840, last=1850)
        self.assertEqual([r["round"] for r in chain], [1842])

    def test_empty(self):
        self.assertEqual(extract_chain([]), [])


class ChainSpanTests(unittest.TestCase):
    def test_total_and_gaps(self):
        chain = extract_chain(SAMPLE_LOG)
        total, gaps = chain_span(chain)
        # 01:28 -> 07:22 = 354 min
        self.assertAlmostEqual(total, 354.0)
        self.assertEqual(len(gaps), 3)
        # R1782(01:28) -> R1783(01:04): placeholder-order artifact, negative gap kept
        self.assertAlmostEqual(gaps[0][2], -24.0)
        # R1788(04:33) -> R1795(07:22) = 169 min
        self.assertAlmostEqual(gaps[2][2], 169.0)

    def test_empty_span(self):
        self.assertEqual(chain_span([]), (0.0, []))


class ArtifactTableTests(unittest.TestCase):
    def test_dir_span_and_absent(self):
        with tempfile.TemporaryDirectory() as root:
            d = os.path.join(root, "sub")
            os.makedirs(d)
            now = time.time()
            with open(os.path.join(d, "a.png"), "w") as f:
                f.write("x")
            os.utime(os.path.join(d, "a.png"), (now - 120, now - 120))
            with open(os.path.join(d, "b.png"), "w") as f:
                f.write("x")
            rows = artifact_table(root, artifacts=["sub", "missing/thing"])
            by_rel = {rel: (when, extra) for rel, when, extra in rows}
            self.assertEqual(by_rel["sub"][0].split(" -> ")[0][-8:],
                             time.strftime("%H:%M:%S", time.localtime(now - 120)))
            self.assertIn("n=2", by_rel["sub"][1])
            self.assertIn("span=2.0min", by_rel["sub"][1])
            self.assertEqual(by_rel["missing/thing"][0], "ABSENT")


if __name__ == "__main__":
    unittest.main()
