# -*- coding: utf-8 -*-
"""R475 canonical five-mode ledger scan (r462_canon method, OUTP fresh file)."""
import io, re, os
from collections import Counter

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
P1 = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
OUTP = os.path.join(ROOT, ".c3-tmp", "r475_canon.txt")
out = io.open(OUTP, "w", encoding="utf-8")
def w(s):
    out.write(s + "\n")

pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
hits = [l.rstrip('\n') for l in io.open(P1, encoding='utf-8', errors='replace') if pat.search(l)]
w("ledger_matches=%d" % len(hits))
w("ledger_last_hit_ascii=%s" % hits[-1][:60].encode('ascii', 'replace').decode('ascii'))
c = Counter()
for l in hits:
    for m in pat.findall(l):
        c[m] += 1
w("ledger_modes=%s" % dict(c))
out.close()
print("OK r475_canon ->", OUTP)
