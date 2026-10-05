# -*- coding: utf-8 -*-
# R1372 check3: enumerate ledger tag lines exactly (reconcile 43 vs 44)
import re, io, datetime

base = r"C:\Users\sjs20\Desktop\FluxGroup"
repo = base + r"\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1372_check3.txt", "w", encoding="utf-8")
w = out.write

# exact bytes from r1370_check.py pattern (with Chinese literals in \u form)
PAT = "@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf)"
led = io.open(base + r"\cph4\evolution-ledger.md", encoding="utf-8").read()
llines = led.split("\n")
tags = [l for l in llines if re.search(PAT, l)]
w("recount_with_r1370_pattern=%s\n" % len(tags))
w("ledger_bytes=%s lines=%s mtime=%s\n\n" % (len(led.encode("utf-8")), len(llines), datetime.datetime.fromtimestamp(__import__("os").path.getmtime(base + r"\cph4\evolution-ledger.md")).strftime("%m-%d %H:%M:%S")))

for i, l in enumerate(llines, 1):
    m = re.search(PAT, l)
    if m:
        w("L%s tag=%s :: %s\n" % (i, m.group(0), l[:90]))
out.close()
print("ok")
