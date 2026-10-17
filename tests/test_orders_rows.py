# -*- coding: utf-8 -*-
"""Unit tests for tools/orders_rows.py -- tech#193 pit gate.

Regression locks:
- R2323 live anchor: the nested double-pipe row (row 518 shape
  ``| | 2026-10-17 03:2x | ...``) broke a bare-startswith timestamp
  check in the r2323 DIGEST-v23 build (A1 first-run FAIL). This module
  must extract its ts structurally, forever.
- Canonical parity: row numbering must equal group_scan's ORDERS
  watermark counting (orders_row_stats) on mixed-shape fixtures, so a
  row consumed by a card build is the same row the watermark counts.

Run:
    python tests/test_orders_rows.py
"""

import contextlib
import io as _io
import os
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "src", "os"))

import group_scan  # noqa: E402
import orders_rows  # noqa: E402


# Live shapes from HQ docs/orders.md (verbatim prefixes; bodies trimmed).
ROW_518_ANCHOR = (
    "| | 2026-10-17 03:2x | **【@bm-c 回执】开工令双道排满夜窗收官"
    "（L1157 执行件）** | ①GPU 双卡 0016/0017+CPU 道 V2《法务部》"
    "成片闸 PASS 三线齐发 |"
)
ROW_FULL = (
    "| 2026-10-17 13:5x | **【@bm-c 派单】V5.3 三镜重烧追加单"
    "（O-20261017-1330 逐镜全审定谳产物）** | 三镜=P1-1/P1-2/P2-3 |"
)
ROW_SHORT = "| 10-12 23:3x | CEO 令（原话）：「给我写 大时代…」 | open |"
ROW_SEP = "|---|---|---|"
ROW_HEADER = "| 时间 | 内容 | 状态 |"
NOT_A_ROW = "nothing to see here"

MIXED = "\n".join([
    "# heading",
    ROW_HEADER,
    ROW_SEP,
    ROW_FULL,
    ROW_518_ANCHOR,
    "plain paragraph",
    ROW_SHORT,
])


class OrdersRowCellsTests(unittest.TestCase):
    def test_nested_double_pipe_cells(self):
        cells = orders_rows.orders_row_cells(ROW_518_ANCHOR)
        self.assertIsNotNone(cells)
        self.assertEqual(cells[0], "")
        self.assertEqual(cells[1], "2026-10-17 03:2x")

    def test_normal_row_cells(self):
        cells = orders_rows.orders_row_cells(ROW_FULL)
        self.assertEqual(cells[0], "2026-10-17 13:5x")

    def test_non_row_yields_none(self):
        self.assertIsNone(orders_rows.orders_row_cells(NOT_A_ROW))
        self.assertIsNone(orders_rows.orders_row_cells(""))


class OrdersRowTsTests(unittest.TestCase):
    def test_r2323_nested_double_pipe_anchor(self):
        # The pit itself: this live shape does NOT start with '| 2026'
        # (bare-startswith consumers FALSE-FAIL on it). The structural
        # extraction must still return its timestamp.
        self.assertFalse(ROW_518_ANCHOR.startswith("| 2026"))
        self.assertEqual(
            orders_rows.orders_row_ts(ROW_518_ANCHOR), "2026-10-17 03:2x")

    def test_full_date_row(self):
        self.assertEqual(
            orders_rows.orders_row_ts(ROW_FULL), "2026-10-17 13:5x")

    def test_short_date_row(self):
        self.assertEqual(
            orders_rows.orders_row_ts(ROW_SHORT), "10-12 23:3x")

    def test_deeper_nested_prefix(self):
        line = "| | | 2026-10-17 07:3x | deep nested |"
        self.assertEqual(orders_rows.orders_row_ts(line), "2026-10-17 07:3x")

    def test_separator_and_header_no_ts(self):
        self.assertIsNone(orders_rows.orders_row_ts(ROW_SEP))
        self.assertIsNone(orders_rows.orders_row_ts(ROW_HEADER))

    def test_non_row_no_ts(self):
        self.assertIsNone(orders_rows.orders_row_ts(NOT_A_ROW))


class OrdersRowsParityTests(unittest.TestCase):
    def test_row_count_parity_with_group_scan(self):
        stats_rows, _tail = group_scan.orders_row_stats(MIXED)
        listed = list(orders_rows.orders_rows(MIXED))
        self.assertEqual(len(listed), stats_rows)
        self.assertEqual(
            [row_no for row_no, _ts, _line in listed],
            list(range(1, stats_rows + 1)))

    def test_ts_sequence_on_mixed_fixture(self):
        listed = list(orders_rows.orders_rows(MIXED))
        by_no = {row_no: ts for row_no, ts, _line in listed}
        self.assertIsNone(by_no[1])  # header
        self.assertIsNone(by_no[2])  # separator
        self.assertEqual(by_no[3], "2026-10-17 13:5x")
        self.assertEqual(by_no[4], "2026-10-17 03:2x")
        self.assertEqual(by_no[5], "10-12 23:3x")

    def test_cli_probe_smoke(self):
        with tempfile.NamedTemporaryFile(
                "w", suffix=".md", delete=False, encoding="utf-8") as fh:
            fh.write(MIXED)
            path = fh.name
        try:
            buf = _io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = orders_rows.main(["--hq-orders", path, "--tail", "3"])
            self.assertEqual(rc, 0)
            out = buf.getvalue()
            self.assertIn("rows=5", out)
            self.assertIn("ROW 5", out)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
