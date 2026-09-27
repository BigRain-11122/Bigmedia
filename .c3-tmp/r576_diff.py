# r576: ledger diff vs r533 baseline + full new decision rows
import io, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, ".c3-tmp", "r576_diff.txt")
o = []

def pids(path):
    ids = []
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            m = re.search(r"P-\d{4}-\d{2}-\d{2}-\d{2}", line)
            if m:
                ids.append(m.group(0))
    return ids

base = os.path.join(ROOT, ".c3-tmp", "r533_lednew.txt")
new = os.path.join(ROOT, ".c3-tmp", "r576_newdump.txt")
if os.path.exists(base):
    b, n = pids(base), pids(new)
    o.append("BASELINE pids=%d" % len(b))
    o.append("NEW      pids=%d" % len(n))
    o.append("LOST   =%s" % sorted(set(b) - set(n)))
    o.append("ADDED  =%s" % sorted(set(n) - set(b)))
else:
    o.append("BASELINE r533_lednew.txt MISSING")

# full text of new decision rows D48, D56, D61, D62 + committee header rules D57/D58/D63
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
with io.open(DEC, "r", encoding="utf-8", errors="replace") as f:
    dl = [l.rstrip("\n") for l in f if l.strip()]
o.append("=== FULL ROWS ===")
for i in (48, 56, 57, 58, 61, 62, 63):
    if i <= len(dl):
        o.append("D%02d FULL: %s" % (i, dl[i-1]))
        o.append("")

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o))
print("OK")
