# -*- coding: utf-8 -*-
"""R1305 focus candidates: CENSUS C-00030 anchor, self-improvement queue top, export freshness."""
import os, io, json, re, glob

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
out = io.StringIO()

# 1) CENSUS supply gate: C-00030 handwritten anchor (cross-repo read-only, canonical position only)
for pat in [r"life\BigLife\census\anchors\C-00030.md", r"life\BigLife\census\anchors\C-00031.md"]:
    p = os.path.join(GRP, pat)
    out.write(f"anchor {pat}: exists={os.path.exists(p)}\n")
ad = os.path.join(GRP, r"life\BigLife\census\anchors")
if os.path.isdir(ad):
    ids = sorted(f[:-3] for f in os.listdir(ad) if re.match(r"C-\d{5}\.md$", f))
    out.write(f"anchors top 3: {ids[-3:]} total={len(ids)}\n")

# 2) self-improvement queue top section
q = os.path.join(ROOT, "docs", "self-improvement-queue.md")
if os.path.exists(q):
    with open(q, encoding="utf-8") as f:
        txt = f.read()
    out.write(f"\nqueue len={len(txt)}\n")
    # top of pool section (§D/§E) - print first 120 lines
    lines = txt.splitlines()
    out.write("queue head 60 lines:\n")
    for ln in lines[:60]:
        out.write("  " + ln[:180] + "\n")

# 3) status-export freshness
se = os.path.join(ROOT, "docs", "status-export.json")
if os.path.exists(se):
    with open(se, encoding="utf-8") as f:
        ex = json.load(f)
    out.write(f"\nexport_ts: {ex.get('export_ts')}\n")
    cur = ex.get("current", "")
    rec = ex.get("recent", "")
    nxt = ex.get("next", "")
    out.write(f"current: {str(cur)[:150]}\n")
    out.write(f"recent: {str(rec)[:150]}\n")
    out.write(f"next: {str(nxt)[:150]}\n")

with open(os.path.join(ROOT, "r_cur_check2.txt"), "w", encoding="utf-8") as f:
    f.write(out.getvalue())
print("ok")
