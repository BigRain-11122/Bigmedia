# -*- coding: utf-8 -*-
"""R633: read full ledger rows 160/162 + decisions new rows."""
import io, os
CWD = os.path.dirname(os.path.abspath(__file__))
OUT = io.open(os.path.join(CWD, "r633_rows.txt"), "w", encoding="utf-8")
def w(*a): OUT.write(" ".join(str(x) for x in a) + "\n")

led = io.open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding="utf-8").read().splitlines()
for i, l in enumerate(led):
    if l.startswith("| P-2026-09-28-08") or l.startswith("| P-2026-09-28-09"):
        w("=== LED", i + 1, "===")
        w(l.strip())
        if i + 1 < len(led) and led[i + 1].strip():
            w("CONT:", led[i + 1].strip())
        if i + 2 < len(led) and led[i + 2].strip() and not led[i + 2].startswith("| P-"):
            w("CONT2:", led[i + 2].strip())

dec = [l for l in io.open(r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md", encoding="utf-8") if l.strip()]
for l in dec:
    s = l.strip()
    if s.startswith("| D-20260928-01") or s.startswith("| C-20260928-02"):
        w("=== DEC ===")
        w(s)
OUT.close()
print("OK")
