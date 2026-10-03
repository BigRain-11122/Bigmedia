# -*- coding: utf-8 -*-
# R1075 #86 a-leg definitive content count (content-addressing law; mtime is false signal).
# Clone of the r1008-series counting approach: axes/*/bucket lists + sprite bucket lists.
import io, json, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
pool = json.load(io.open(
    os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"),
    encoding="utf-8"))

total = 0
parts = []
axes = pool.get("axes", {})
for ax, buckets in axes.items():
    if isinstance(buckets, dict):
        for bk, lines in buckets.items():
            if isinstance(lines, list):
                total += len(lines)
                parts.append("%s/%s=%d" % (ax, bk, len(lines)))
sp = pool.get("sprite")
if isinstance(sp, dict):
    for bk, lines in sp.items():
        if isinstance(lines, list):
            total += len(lines)
            parts.append("sprite/%s=%d" % (bk, len(lines)))
extra = {k: (len(v) if isinstance(v, list) else type(v).__name__) for k, v in pool.items()
         if k not in ("axes", "sprite")}
print("TOTAL_CONTENT_ENTRIES=%d (baseline 1440)" % total)
print("top-level extra keys: %s" % extra)
print("first parts: %s" % "; ".join(parts[:6]))
