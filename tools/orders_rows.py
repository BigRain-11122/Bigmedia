# -*- coding: utf-8 -*-
"""Canonical HQ orders.md row helpers for card-build / probe scripts
(tech#193 pit gate, R2323 live anchor).

Pit (R2323, r2323_build A1 first-run FAIL): HQ orders.md row prefixes
are NOT uniform ``| 2026-10-17``. Live shapes include the nested
double-pipe row (anchor = row 518 ``| | 2026-10-17 03:2x | ...`` --
empty first cell, date in the SECOND cell) and the short-date family
(``| 10-12 23:3x | ...``). Any bare ``startswith("| 2026")`` /
``startswith("| 10-")`` timestamp assertion FALSE-FAILS on the nested
form, and ``line.strip()[1:]``-style first-cell extraction returns an
empty cell for it too (see group_scan._orders_first_cell, which is
fine for tail_key but not for row-consumption builds).

Law (queue tech#193): every build/probe script that consumes orders
rows BY ROW NUMBER (DIGEST/REACT card build family, window/cluster
assertions) must go through this module (or an equivalent lstrip of the
leading pipe/space family) -- never bare startswith on the raw line.

Single truth: the row-counting semantic and the cell-date regex are
imported from src/os/group_scan (canonical ORDERS face), so a row
numbered here is the same row the ORDERS watermark counts. This module
adds only the nested-row-safe wrappers:

    orders_row_cells(line)  -> list[str] | None   (None = not a row)
    orders_row_ts(line)     -> str | None         (first date-shaped cell)
    orders_rows(text)       -> (row_no, ts, line) generator

CLI probe (read-only sanity check on the live file):
    python tools/orders_rows.py [--hq-orders PATH] [--tail N]
"""

import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src", "os"))

from group_scan import ORDERS_CELL_DATE_RE  # noqa: E402  canonical cell-date regex


def orders_row_cells(line):
    """Stripped cell list of an orders |-row; None when not a row.

    Mirrors group_scan's row predicate (``line.lstrip().startswith('|')``)
    so row numbering stays identical to the ORDERS watermark face.
    Leading/trailing pipes are dropped; inner pipes split the cells. A
    nested ``| | 2026-10-17 ...`` row therefore yields '' as its first
    cell and the date as its second -- exactly the shape that broke
    bare-startswith consumers.
    """
    if not line.lstrip().startswith("|"):
        return None
    body = line.strip().strip("|")
    return [cell.strip() for cell in body.split("|")]


def orders_row_ts(line):
    """First date-shaped cell of an orders row, or None.

    Walks cells (empty first cell of nested rows is skipped) and returns
    the first cell matching the canonical ORDERS_CELL_DATE_RE. Separator
    rows (``|---|``) and header rows yield None but are still counted as
    rows by orders_rows()/group_scan -- callers asserting on ts must
    treat None as "row without a leading date", never as "not a row".
    """
    cells = orders_row_cells(line)
    if cells is None:
        return None
    for cell in cells:
        if cell and ORDERS_CELL_DATE_RE.match(cell):
            return cell
    return None


def orders_rows(text):
    """Yield (row_number, ts, line) with group_scan row-numbering parity.

    Row numbers here equal the ORDERS watermark rows: every line whose
    lstrip starts with '|' counts, in file order, starting at 1.
    """
    n = 0
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            n += 1
            yield n, orders_row_ts(line), line


def main(argv=None):
    parser = argparse.ArgumentParser(description="orders rows probe")
    parser.add_argument("--hq-orders", default=os.path.join(
        REPO, "..", "..", "docs", "orders.md"))
    parser.add_argument("--tail", type=int, default=5)
    args = parser.parse_args(argv)

    path = os.path.abspath(args.hq_orders)
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    rows = list(orders_rows(text))
    print("orders-rows probe:", path)
    print("rows=%d" % len(rows))
    for row_no, ts, line in rows[-args.tail:]:
        print("ROW %d ts=%r :: %s" % (row_no, ts, line[:90]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
