# -*- coding: utf-8 -*-
# R720: b8 band-collision adjudication - my re-render vs R718 original evidence frame
import os
from PIL import Image

TMP = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.lc013-tmp"
out = open(os.path.join(TMP, "r720_b8verify.txt"), "w", encoding="utf-8")

def profile_clusters(img, y0, y1, x0=100, x1=980, thr=190, minbright=80):
    px = img.load()
    rows = []
    for y in range(y0, y1):
        n = 0
        for x in range(x0, x1):
            r, g, b = px[x, y][:3]
            if r > thr and g > thr and b > thr:
                n += 1
        rows.append((y, n))
    line_rows = [y for y, n in rows if n >= minbright]
    clusters = []
    for y in line_rows:
        if clusters and y - clusters[-1][-1] <= 6:
            clusters[-1].append(y)
        else:
            clusters.append([y])
    res = []
    for c in clusters:
        peak = max(n for y, n in rows if c[0] <= y <= c[-1])
        res.append((c[0], c[-1], peak))
    return res, rows

for tag, fp in [("MINE-r720-b8head", os.path.join(TMP, "r720_b8head.png")),
                ("ORIG-R718-fs-h08", os.path.join(TMP, "fs-h08.png")),
                ("MINE-r720-b10head", os.path.join(TMP, "r720_b10head.png"))]:
    img = Image.open(fp).convert("RGB")
    W, H = img.size
    cl, rows = profile_clusters(img, 700, 1200)
    out.write("== %s (%dx%d) ==\n" % (tag, W, H))
    for a, b, peak in cl:
        out.write("  cluster y=%d..%d (h=%d) peak=%d\n" % (a, b, b - a + 1, peak))
    band = [(y, n) for y, n in rows if 743 <= y <= 770 and n > 20]
    out.write("  band745-767: %s\n" % ", ".join("%d:%d" % (y, n) for y, n in band))
out.close()
print("B8DONE")
