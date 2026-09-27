# r576: read new decisions lines + dump ledger matched lines for diff vs prior dumps
import io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"

out = []

# --- decisions: dump all non-empty lines with index ---
with io.open(DEC, "r", encoding="utf-8", errors="replace") as f:
    dlines = [l for l in f if l.strip()]
out.append("=== DECISIONS nonempty=%d ===" % len(dlines))
for i, l in enumerate(dlines, 1):
    out.append("D%02d| %s" % (i, l.rstrip()[:400]))

# --- ledger: dump all five-mode matched lines ---
tags = ["\u0040BigStream", "\u0040\u4e03\u7ebf\u5168\u53f8", "\u0040\u5168\u53f8", "\u0040\u516d\u53f8"]
out.append("=== LEDGER matched ===")
n = 0
with io.open(LEDGER, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        if any(t in line for t in tags):
            n += 1
            out.append("L%02d| %s" % (n, line.rstrip()[:400]))
out.append("LEDGER total=%d" % n)

with io.open(os.path.join(ROOT, ".c3-tmp", "r576_newdump.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK")
