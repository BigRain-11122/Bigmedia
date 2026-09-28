# -*- coding: utf-8 -*-
# R644 five-check probe: group ledger scan (case-sensitive, five patterns) + rowdiff vs r636 baseline + decisions count
import io, os, collections

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
LEDGER = os.path.join(ROOT, "cph4", "evolution-ledger.md")
DECISIONS = os.path.join(ROOT, "docs", "decisions.md")
C3 = os.path.join(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(C3, "r636_lednew5.txt")
OUT = os.path.join(C3, "r644_lednew5.txt")

PATS = ["@BigStream", "@七线全司", "@全司", "@六司", "@media全司", "@八线全量"]

t = io.open(LEDGER, encoding="utf-8").read()
lines = t.splitlines()
c = collections.Counter()
matched = []
for i, line in enumerate(lines):
    hit = None
    for pat in PATS:
        if pat in line:
            hit = pat
            c[pat] += 1
    if hit:
        matched.append("L%d\t%s" % (i + 1, line.strip()))

# five-pattern unique-line count (the anchor metric; @八线全量 rows tracked in
# matched file per R377 pattern extension but excluded from the five-pattern
# unique count unless they also hit one of the five)
five = set()
six = []
for i, line in enumerate(lines):
    hit5 = [p for p in PATS[:5] if p in line]
    if hit5:
        five.add("L%d\t%s" % (i + 1, line.strip()))
    if hit5 or "@八线全量" in line:
        six.append("L%d\t%s" % (i + 1, line.strip()))

io.open(OUT, "w", encoding="utf-8").write("\n".join(six) + ("\n" if six else ""))
total = sum(c.values())

base = io.open(BASELINE, encoding="utf-8").read().splitlines() if os.path.exists(BASELINE) else []
cur = set(six)
bset = set(base)
new = sorted(cur - bset)
gone = sorted(bset - cur)

dt = io.open(DECISIONS, encoding="utf-8").read()
dcount = sum(1 for l in dt.splitlines() if l.strip())

import json
res = {
    "LEDGER_TOTAL_PATTERN_HITS": total,
    "LEDGER_BY_PAT": dict(c),
    "LEDGER_MTIME": os.path.getmtime(LEDGER),
    "FIVE_UNIQUE_LINES": len(five),
    "SIX_UNIQUE_LINES": len(six),
    "LEDGER_NEW": len(new),
    "LEDGER_GONE": len(gone),
    "DECISIONS_NONEMPTY": dcount,
    "MATCHED_LINES": len(six),
    "BASELINE_LINES": len(base),
}
for k, v in res.items():
    print(k, v)
for l in new:
    print("NEW_LINE:", l[:160])
for l in gone:
    print("GONE_LINE:", l[:160])
