# -*- coding: utf-8 -*-
# R691: locate F-036 CENSUS-v17 card dir + read anchor C-00026 (cross-repo read-only)
import glob, io, os

hits = sorted(glob.glob(r"data/storylines/cards/*CENSUS-v17*"))
for h in hits:
    print("DIR:", h)
    for f in sorted(glob.glob(os.path.join(h, "*"))):
        print("   ", f, os.path.getsize(f))

anchor = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00026.md"
print("=== anchor C-00026 exists:", os.path.exists(anchor))
if os.path.exists(anchor):
    with io.open(anchor, encoding="utf-8") as fh:
        print(fh.read())
