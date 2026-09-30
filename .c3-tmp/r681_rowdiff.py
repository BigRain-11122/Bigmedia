# -*- coding: utf-8 -*-
# R681 rowdiff: new ledger rows vs r644_lednew5 baseline + new decisions tail
import os, re, io

T = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(T)
LED = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"

base_led = io.open(os.path.join(T, "r644_lednew5.txt"), "r", encoding="utf-8").read().splitlines()
base_set = set(l.strip() for l in base_led if l.strip())

pat = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线|@全公司|@all-companies")
cur = []
with io.open(LED, "r", encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        if pat.search(line):
            cur.append((i, line.rstrip("\n")))

out = ["=== LEDGER rowdiff (six/seven-mode CaseSensitive) ===",
       "baseline_rows=%d current_rows=%d" % (len(base_set), len(cur))]
new_rows = [(i, l) for i, l in cur if l.strip() not in base_set]
gone = [b for b in sorted(base_set) if b not in set(l.strip() for _, l in cur)]
out.append("NEW=%d GONE=%d" % (len(new_rows), len(gone)))
for i, l in new_rows:
    out.append("NEW L%d: %s" % (i, l[:400]))
for g in gone:
    out.append("GONE: %s" % g[:200])

# decisions tail: last 3 non-empty lines
with io.open(DEC, "r", encoding="utf-8") as f:
    dl = [l.rstrip("\n") for l in f if l.strip()]
out.append("")
out.append("=== DECISIONS tail 3 (nonempty=%d) ===" % len(dl))
for l in dl[-3:]:
    out.append(l[:400])

with io.open(os.path.join(T, "r681_rowdiff.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("\n".join(out))
