# -*- coding: utf-8 -*-
# R872 edge-clipping check: per-band horizontal ink extent must stay inside side margins.
from PIL import Image
import io, sys

png = r"data\storylines\cards\MC-20261001-DIGEST-v13\MC-20261001-DIGEST-v13.png"
im = Image.open(png).convert("L")
W, H = im.size
px = im.load()

BANDS = [(48, 77), (218, 299), (494, 528), (554, 588), (614, 648), (674, 708),
         (734, 768), (794, 828), (854, 888), (970, 1007)]
INK = 200
out = []
ok = True
for i, (a, b) in enumerate(BANDS):
    xs = [x for y in range(a, b + 1) for x in range(0, W, 2) if px[x, y] >= INK]
    if not xs:
        ok = False
        out.append("band %02d: NO INK FOUND (unexpected)" % i)
        continue
    x0, x1 = min(xs), max(xs)
    lm, rm = x0, W - 1 - x1
    clipped = x0 < 8 or x1 > W - 9
    if clipped:
        ok = False
    out.append("band %02d: x %4d-%4d  Lmargin %4d  Rmargin %4d  clip=%s" % (i, x0, x1, lm, rm, clipped))
io.open(r"data\storylines\cards\MC-20261001-DIGEST-v13-tmp\edge-check-r872.txt", "w", encoding="utf-8").write("\n".join(out))
print("EDGE OK=%s" % ok)
sys.exit(0 if ok else 1)
