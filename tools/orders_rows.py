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
import subprocess
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


HQ_ORDERS_DEFAULT = os.path.abspath(os.path.join(
    REPO, "..", "..", "docs", "orders.md"))


def read_hq_orders_text(path=None):
    """Host orders.md text, read-only (D-20261001-03 zero-write canon)."""
    with open(path or HQ_ORDERS_DEFAULT, encoding="utf-8",
              errors="replace") as fh:
        return fh.read()


def rows_window_text(text, start, end):
    """'ROW N: <row line>' lines for rows start..end inclusive (tech#231).

    m1-assert evidence-snapshot fallback leg: card-build assertions keep
    their .c3-tmp/orders-rows-*.txt snapshots only until the round-end
    cleanup hook deletes them, after which re-running an assertion died
    on FileNotFoundError (R2369/R2371/R2372 three-reel pit). This rebuilds
    the same 'ROW N:' window text in-process from any orders.md text with
    row numbering identical to the ORDERS watermark (tech#193 canonical
    parity), so assertions stay permanently re-runnable with zero repo
    bloat and zero cross-repo writes. Windows extending past the current
    tail yield the rows that exist (callers assert contiguity themselves
    -- fail-closed on shrinkage).
    """
    if start < 1 or end < start:
        raise ValueError("window must satisfy 1 <= start <= end")
    out = []
    for row_no, _ts, line in orders_rows(text):
        if start <= row_no <= end:
            out.append("ROW %d: %s" % (row_no, line))
    return out


def rows_window_from_host(start, end, path=None):
    """rows_window_text over the host orders.md (snapshot-missing leg)."""
    return rows_window_text(read_hq_orders_text(path), start, end)


def read_origin_orders_text(ref="origin/main", path=None, git_binary="git"):
    """orders.md blob text at ``ref`` via ``git show`` (tech#250 origin face).

    Why (R2392 seed): origin-only rows (ORIGIN-DELTA ahead state, the
    D-13 SLA consumption face) had to be hand-rolled as one-shot git-show
    extraction scripts for four straight rounds (R2385/R2387/R2389/R2392
    .c3-tmp throwaways) because this module only read the worktree face.
    This is the canonical origin face: byte-capture
    ``git -C <repo> show <ref>:<relpath>``, decode utf-8/replace
    (read_hq_orders_text parity).

    Fail-closed by design: any git failure (bad ref, not a repo, origin
    never fetched) raises RuntimeError -- a silent fallback to the
    host worktree file would re-create the exact worktree-blind-spot
    family (R2059/R2064) that the ORIGIN-DELTA face exists to catch.
    Zero repo writes (D-20261001-03 read-only canon).
    """
    target = os.path.abspath(path or HQ_ORDERS_DEFAULT)
    probe = subprocess.run(
        [git_binary, "-C", os.path.dirname(target),
         "rev-parse", "--show-toplevel"],
        capture_output=True, timeout=60)
    if probe.returncode != 0:
        raise RuntimeError(
            "orders_rows origin face: %r is not inside a git repo "
            "(git rev-parse rc=%d)"
            % (os.path.dirname(target), probe.returncode))
    toplevel = probe.stdout.decode("utf-8", errors="replace").strip()
    rel = os.path.relpath(target, toplevel).replace(os.sep, "/")
    show = subprocess.run(
        [git_binary, "-C", toplevel, "show", "%s:%s" % (ref, rel)],
        capture_output=True, timeout=120)
    if show.returncode != 0:
        err = show.stderr.decode("utf-8", errors="replace").strip()[-300:]
        raise RuntimeError(
            "orders_rows origin face: git show %s:%s failed rc=%d: %s"
            % (ref, rel, show.returncode, err))
    return show.stdout.decode("utf-8", errors="replace")


def rows_window_from_origin(start, end, ref="origin/main", path=None,
                            git_binary="git"):
    """rows_window_text over the origin-face blob (tech#250).

    Window/row semantics are the shared pure core, so an origin row
    numbered here is the same row the ORDERS / ORIGIN-DELTA faces count.
    """
    return rows_window_text(
        read_origin_orders_text(ref, path, git_binary), start, end)


def _harden_console_stdio():
    """tech#245 (R2388): orders_rows console face prints UTF-8.

    tech#243's twin for this probe: rows 596-600 consumption hit full
    CJK mojibake on the GBK codepage console (R2387 anchor), forcing a
    stable second read_file hop per judgment. Reconfigure stdout/stderr
    to encoding='utf-8' + errors='replace' (group_scan.py parity; the
    R2276 hardening contract). pythonw None-streams and the unittest
    harness (StringIO has no reconfigure) both no-op via AttributeError.
    """
    for stream in (sys.stdout, sys.stderr):
        if stream is None:
            continue
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


def main(argv=None):
    _harden_console_stdio()
    parser = argparse.ArgumentParser(description="orders rows probe")
    parser.add_argument("--hq-orders", default=os.path.join(
        REPO, "..", "..", "docs", "orders.md"))
    parser.add_argument("--tail", type=int, default=5)
    parser.add_argument("--window", nargs=2, type=int,
                        metavar=("START", "END"),
                        help="print the 'ROW N: <line>' window text "
                             "(tech#231 m1-assert fallback source)")
    parser.add_argument("--source", choices=["host", "origin"],
                        default="host",
                        help="row source face: 'host' worktree file "
                             "(default -- zero regression for existing "
                             "--window consumers) or 'origin' git-show "
                             "blob face (tech#250)")
    parser.add_argument("--ref", default="origin/main",
                        help="git ref for --source origin "
                             "(default origin/main)")
    args = parser.parse_args(argv)

    path = os.path.abspath(args.hq_orders)
    if args.source == "origin":
        # tech#250: origin-only rows (ORIGIN-DELTA ahead state) read via
        # the canonical git-show face -- no more hand-rolled extraction.
        text = read_origin_orders_text(args.ref, path)
    else:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    if args.window:
        start, end = args.window
        for line in rows_window_text(text, start, end):
            print(line)
        return 0
    rows = list(orders_rows(text))
    print("orders-rows probe:", path)
    print("rows=%d" % len(rows))
    for row_no, ts, line in rows[-args.tail:]:
        print("ROW %d ts=%r :: %s" % (row_no, ts, line[:90]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
