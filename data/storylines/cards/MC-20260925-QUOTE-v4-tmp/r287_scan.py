# -*- coding: utf-8 -*-
"""R287 fast-path scan: group ledger @-lines + HQ decisions count + local facts. ASCII output only."""
import io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
LEDGER = os.path.join(ROOT, "cph4", "evolution-ledger.md")
DECISIONS = os.path.join(ROOT, "docs", "decisions.md")
BMD = os.path.join(ROOT, "media", "BigStream")

def read_utf8(p):
    if not os.path.exists(p):
        return None
    with io.open(p, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

# 1. ledger lines containing @BigStream / @全司 / @七线全司 / @六司
pat_list = [u"@BigStream", u"@全司", u"@七线全司", u"@六司"]
ledger = read_utf8(LEDGER)
if ledger is None:
    print("LEDGER: MISSING")
else:
    lines = ledger.splitlines()
    hits = []
    for i, ln in enumerate(lines, 1):
        if any(p in ln for p in pat_list):
            hits.append((i, ln.strip()))
    print("LEDGER_MATCH_LINES: %d" % len(hits))
    for i, ln in hits:
        # print line number + first 120 ascii-sanitized
        safe = ln.encode("ascii", "backslashreplace").decode("ascii")
        print("  L%d: %s" % (i, safe[:160]))

# 2. HQ decisions non-empty line count (UTF8)
dec = read_utf8(DECISIONS)
if dec is None:
    print("DECISIONS: MISSING")
else:
    nonempty = [ln for ln in dec.splitlines() if ln.strip()]
    print("DECISIONS_NONEMPTY: %d  TOTAL: %d" % (len(nonempty), len(dec.splitlines())))

# 3. local facts
print("INDEX_LOCK: %s" % os.path.exists(os.path.join(BMD, ".git", "index.lock")))
novel = os.path.join(BMD, "data", "storylines", "novel")
print("NOVEL_CH5_V3: %s" % os.path.exists(os.path.join(novel, "SC-001-05-v3.md")))
orders = sorted(os.listdir(os.path.join(BMD, "orders")))
print("ORDERS_TOP: %s" % orders[-1])
