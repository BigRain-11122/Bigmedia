# r487_ledger_tail.py - dump last 3 five-mode matching ledger lines (full utf-8) for adjudication
import io, os, re
pat = re.compile(r'@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf\u5168\u91cf)')
OUTP = os.path.join(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream", ".c3-tmp", "r487_ledger_tail.txt")
hits = []
with io.open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding='utf-8', errors='replace') as f:
    for i, l in enumerate(f, 1):
        if pat.search(l):
            hits.append((i, l.rstrip('\n')))
out = ["total=%d" % len(hits)]
for i, l in hits[-3:]:
    out.append("L%d: %s" % (i, l))
with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n\n".join(out) + "\n")
print("written=%s total=%d" % (OUTP, len(hits)))
