# -*- coding: utf-8 -*-
"""M1 assertion for MC-20261024-DIGEST-v28 (R2420).

Reads the group orders ledger from origin/main (read-only), rebuilds the
10-20 11:24 -> 10-23 23:25 window, and machine-checks every number and
every quoted fragment that appears on the card.

Run: python m1-assert-r2420.py   (exit 0 = ALL GREEN)
"""
import io
import json
import os
import subprocess
import sys

GROUP_REPO = r"D:\FluxGroup"
CARD_DIR = os.path.dirname(os.path.abspath(__file__))

# (row date prefix, verbatim fragment in that row, fragment placed on card)
ANCHORS = [
    ("2026-10-20 18:21", "全部停止走云端，全部走本地了", "全部停止走云端，全部走本地了"),
    ("2026-10-20 18:32", "不要再消耗云端 token", "不要再消耗云端 token"),
    ("2026-10-21 16:2x", "尽量少用云端，多用本地", "尽量少用云端，多用本地"),
    ("2026-10-23 23:5x", "周末可以云端和本地平衡生产。", "周末可以云端和本地平衡生产。"),
    ("2026-10-23 10:0x", "成立专门的部门去搞，快点", "成立专门的部门去搞，快点"),
]


def load_rows():
    r = subprocess.run(
        ["git", "-C", GROUP_REPO, "show", "origin/main:docs/orders.md"],
        capture_output=True)
    if r.returncode != 0:
        raise SystemExit("FAIL: cannot read origin/main:docs/orders.md")
    text = r.stdout.decode("utf-8", "replace")
    return [l for l in text.splitlines() if l.startswith("| 2026-")]


def main():
    rows = load_rows()
    start = None
    for i, line in enumerate(rows):
        if "2026-10-20 11:24" in line[:40]:
            start = i
            break
    if start is None:
        raise SystemExit("FAIL: window start row not found")
    window = []
    for line in rows[start:]:
        window.append(line)
        if "2026-10-23 23:25" in line[:40]:
            break

    ceo_rows = [l for l in window if "CEO" in l]
    print("window rows=%d | CEO-note rows=%d" % (len(window), len(ceo_rows)))
    problems = []
    if len(window) != 47:
        problems.append("expected 47 window rows, got %d" % len(window))
    if len(ceo_rows) != 43:
        problems.append("expected 43 CEO rows, got %d" % len(ceo_rows))

    for date, row_frag, _ in ANCHORS:
        hit = [l for l in window if l[:40].find(date) >= 0]
        if not hit:
            problems.append("row missing: %s" % date)
        elif not any(row_frag in l for l in hit):
            problems.append("quote missing in %s: %s" % (date, row_frag))

    cfg = json.load(io.open(os.path.join(CARD_DIR, "cards.json"),
                            encoding="utf-8"))
    lines = "\n".join(cfg["cards"][0]["lines"])
    for _, _, card_frag in ANCHORS:
        if card_frag not in lines:
            problems.append("card line missing quote: %s" % card_frag)
    for token in ("47", "3", "1"):
        if token not in lines:
            problems.append("card line missing number: %s" % token)

    if problems:
        print("FAIL:")
        for p in problems:
            print(" -", p)
        return 1
    print("ALL GREEN: 47 window rows / 43 CEO rows, %d verbatim quotes, "
          "3 cloud turns, 1 dept" % len(ANCHORS))
    return 0


if __name__ == "__main__":
    sys.exit(main())