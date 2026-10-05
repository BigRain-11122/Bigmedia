# -*- coding: utf-8 -*-
# verify D-20260930-1 token context + group file mtimes
import os, re, io, datetime

GROUP = r"C:\Users\sjs20\Desktop\FluxGroup"
out = []
def w(s): out.append(str(s))

dp = os.path.join(GROUP, "docs", "decisions.md")
ep = os.path.join(GROUP, "cph4", "evolution-ledger.md")
op = os.path.join(GROUP, "docs", "orders.md")
for p in (dp, ep, op):
    w("%s mtime: %s" % (os.path.basename(p), datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")))

txt = open(dp, encoding="utf-8").read()
lines = txt.splitlines()
w("== lines matching D-20260930-1 (not followed by digit) ==")
pat = re.compile(r"D-20260930-1(?![0-9])")
for i, l in enumerate(lines):
    if pat.search(l):
        w("-- L%d context:" % (i + 1))
        for j in range(max(0, i - 2), min(len(lines), i + 3)):
            w("   %s L%d: %s" % (">>" if j == i else "  ", j + 1, lines[j][:260]))

w("== decisions.md tail 25 lines ==")
for l in lines[-25:]:
    w("  | " + l[:260])

open(os.path.join(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream", "r_cur_check4.txt"), "w", encoding="utf-8").write("\n".join(out))
print("OK")
