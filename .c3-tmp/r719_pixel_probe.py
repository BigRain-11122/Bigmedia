# -*- coding: utf-8 -*-
# R719: pixel-level measurement of H1 glyph band + card source-line band
# in LC-013 head frames (b0 t=0.2 vs b9 t=41.8 vs b9-mid t=45.5)
from PIL import Image
import numpy as np

def band_rows(path, x0, x1, thresh=200):
    im = np.asarray(Image.open(path).convert("L"))
    seg = im[:, x0:x1]
    rowmax = seg.max(axis=1)
    rows = np.where(rowmax >= thresh)[0]
    return rows

def clusters(rows, gap=12):
    out = []
    if len(rows) == 0:
        return out
    s = prev = rows[0]
    for r in rows[1:]:
        if r - prev > gap:
            out.append((s, prev))
            s = r
        prev = r
    out.append((s, prev))
    return out

for tag in ["h00", "h09", "b9mid"]:
    p = r".lc013-tmp\r719_%s_full.png" % tag
    rows = band_rows(p, 100, 1000)
    cs = clusters(rows)
    print("== %s: bright-row clusters (y ranges with white glyphs), x=100-1000 ==" % tag)
    for (a, b) in cs:
        h = b - a
        print("   y %4d-%4d  h=%3d" % (a, b, h))
    # source line = small text near card bottom-left region; card spans x 210-870
    rows2 = band_rows(p, 240, 860, 185)
    cs2 = clusters(rows2)
    print("   -- x=240-860 (card interior) --")
    for (a, b) in cs2:
        print("   y %4d-%4d  h=%3d" % (a, b, b - a))
