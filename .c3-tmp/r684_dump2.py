# -*- coding: utf-8 -*-
# R684: dump station-reviews LC-002 S2 row (R680) as format reference
import io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")
sr = os.path.join(ROOT, "docs", "reviews", "station-reviews.md")
lines = io.open(sr, encoding="utf-8").read().splitlines()
out = []
for i, l in enumerate(lines):
    if ("R680" in l and "lc-002" in l.lower()) or ("S2" in l and "lc-002" in l.lower() and "执法" in l):
        out.append("L%d: %s" % (i + 1, l))
io.open(os.path.join(TMP, "r684_sr_r680.txt"), "w", encoding="utf-8").write("\n\n".join(out))
print("hits=%d" % len(out))
