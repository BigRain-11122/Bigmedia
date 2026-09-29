# -*- coding: utf-8 -*-
# R720: refined b9 block-top detection - broken (R719) vs fixed (R720) same-window diff
import os
from PIL import Image

TMP = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.lc013-tmp"
out = open(os.path.join(TMP, "r720_b9verify2.txt"), "w", encoding="utf-8")

def profile_rows(img, y0, y1, x0=100, x1=980, thr=190):
    px = img.load()
    res = []
    for y in range(y0, y1):
        n = 0
        for x in range(x0, x1):
            r, g, b = px[x, y][:3]
            if r > thr and g > thr and b > thr:
                n += 1
        res.append((y, n))
    return res

for tag, fp in [("BROKEN-r719", os.path.join(TMP, "r719_b9mid_full.png")),
                ("FIXED-r720", os.path.join(TMP, "r720_b9mid.png"))]:
    img = Image.open(fp).convert("RGB")
    rows = profile_rows(img, 700, 1160)
    # text-line clusters: rows with >=80 bright cols
    line_rows = [y for y, n in rows if n >= 80]
    out.write("== %s ==\n" % tag)
    # group consecutive rows into bands (gap > 6 = new cluster)
    clusters = []
    for y in line_rows:
        if clusters and y - clusters[-1][-1] <= 6:
            clusters[-1].append(y)
        else:
            clusters.append([y])
    for c in clusters:
        peak = max(n for y, n in rows if c[0] <= y <= c[-1])
        out.write("  cluster y=%d..%d (h=%d) peak_bright=%d\n"
                  % (c[0], c[-1], c[-1] - c[0] + 1, peak))
    # band 745-767 detail
    band = [(y, n) for y, n in rows if 743 <= y <= 770]
    out.write("  band745-767 bright: %s\n" % ", ".join("%d:%d" % (y, n) for y, n in band if n > 20))
out.close()
print("DONE2")
