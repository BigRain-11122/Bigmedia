# -*- coding: utf-8 -*-
# R267 group scan (pure ASCII script; Chinese patterns via unicode escapes)
# Scans: cph4/evolution-ledger.md transfer rows (@BigStream/@7line-all/@all/@6cos)
#        + FluxGroup/docs/decisions.md row anchors. UTF-8 channel (R266 lesson).
import io
import re

LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
DECISIONS = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"

# @BigStream | @qi-xian-quan-si | @quan-si | @liu-si
PAT = re.compile("@BigStream|@\u4e03\u7ebf\u5168\u53f8|@\u5168\u53f8|@\u516d\u53f8")

with io.open(LEDGER, encoding="utf-8") as f:
    lines = f.read().splitlines()
hits = [l.strip() for l in lines if PAT.search(l)]
print("LEDGER_HITS", len(hits))
for l in hits[-3:]:
    print("LEDGER_LAST:", l[:120])

with io.open(DECISIONS, encoding="utf-8") as f:
    dlines = f.read().splitlines()
nonempty = [l for l in dlines if l.strip()]
print("DECISIONS_NONEMPTY", len(nonempty))
print("DECISIONS_TOTAL", len(dlines))
if nonempty:
    print("DEC_LAST:", nonempty[-1][:100])
