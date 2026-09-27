# r481_canon.py - canonical ledger scan (r462_canon method: matching LINES) + mode breakdown, OUTP new file
import io, re, os
from collections import Counter

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
P1 = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
OUTP = os.path.join(ROOT, ".c3-tmp", "r481_canon.txt")
out = io.open(OUTP, "w", encoding="utf-8")
def w(s):
    out.write(s + "\n")

pat = re.compile(r'@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf\u5168\u91cf)')
hits = [l.rstrip('\n') for l in io.open(P1, encoding='utf-8', errors='replace') if pat.search(l)]
w("ledger_matches=%d anchor=29" % len(hits))
w("ledger_last_hit_ascii=%s" % hits[-1][:60].encode('ascii', 'replace').decode('ascii'))
c = Counter()
for l in hits:
    for m in pat.findall(l):
        c[m] += 1
w("ledger_modes=%s" % dict(c))
# metric-mismatch note: r481_check occurrences=41 vs lines=29 (multi-occurrence lines inflate)
occ = sum(len(pat.findall(l)) for l in hits)
w("occurrences_total=%d (r481_check metric mismatch root cause: occurrences vs lines)" % occ)
out.close()
print("OK lines=%d occ=%d" % (len(hits), occ))
