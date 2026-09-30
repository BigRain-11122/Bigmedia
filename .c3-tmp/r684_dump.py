# -*- coding: utf-8 -*-
# R684: dump exact LC-003 rows from renders README + station-reviews tail (UTF-8 files, avoid GBK console)
import io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")

# renders README: LC-003 related lines with line numbers
rr = os.path.join(ROOT, "output", "renders", "README.md")
lines = io.open(rr, encoding="utf-8").read().splitlines()
out = []
for i, l in enumerate(lines):
    if "LC-003" in l or "lc-003" in l:
        out.append("L%d: %s" % (i + 1, l))
io.open(os.path.join(TMP, "r684_rr_lc003.txt"), "w", encoding="utf-8").write("\n\n".join(out))

# station-reviews tail 3 rows
sr = os.path.join(ROOT, "docs", "reviews", "station-reviews.md")
slines = io.open(sr, encoding="utf-8").read().splitlines()
io.open(os.path.join(TMP, "r684_sr_tail.txt"), "w", encoding="utf-8").write(
    "\n\n".join("L%d: %s" % (i + 1, l) for i, l in enumerate(slines[-3:], start=len(slines) - 2)))
print("done rr=%d hits sr_tail=%d total=%d" % (len(out), 3, len(slines)))
