# -*- coding: utf-8 -*-
"""r1676_react_probe3.py - card-face actual bucket usage + anchor format check + creed scan.

1) For each REACT piece: which pool rows are ON THE CARD FACE (lines) -> real bucket used
2) C-00019 anchor raw head -> fix creed line format
3) Rescan anchors with corrected pattern, livable-city domain filter
Output: UTF-8 .c3-tmp/r1676_react_probe3.txt
"""
import io, json, os, glob, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
CARDS = os.path.join(ROOT, "data", "storylines", "cards")
ANCH = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
POOLF = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
OUT = os.path.join(ROOT, ".c3-tmp", "r1676_react_probe3.txt")

pools = json.load(io.open(POOLF, encoding="utf-8"))
axes = pools["axes"]
# index: line -> (axis, bucket)
idx = {}
for ax, buckets in axes.items():
    for b, rows in buckets.items():
        for r in rows:
            idx[r] = (ax, b)

lines_out = []
lines_out.append(u"== 1) REACT card-face real bucket usage ==")
for d in sorted(os.listdir(CARDS)):
    if "REACT" not in d:
        continue
    cj = os.path.join(CARDS, d, "cards.json")
    if not os.path.exists(cj):
        continue
    c = json.load(io.open(cj, encoding="utf-8"))
    used = set()
    for card in c.get("cards", []):
        for ln in card.get("lines", []):
            for r, (ax, b) in idx.items():
                if r in ln:
                    used.add((ax, b))
    lines_out.append(u"%s -> %s" % (d, sorted(used)))

lines_out.append(u"")
lines_out.append(u"== 2) C-00019 anchor raw head (format check) ==")
p19 = os.path.join(ANCH, "C-00019.md")
lines_out.append(io.open(p19, encoding="utf-8").read()[:400])

lines_out.append(u"")
lines_out.append(u"== 3) creed rescan (corrected pattern) ==")
for p in sorted(glob.glob(os.path.join(ANCH, "C-*.md"))):
    txt = io.open(p, encoding="utf-8").read()
    m = re.search(u"信条[^\n「」]*「?(.{2,40})」?", txt)
    if not m:
        continue
    creed = m.group(1).strip()
    KW = [u"家", u"城", u"街", u"坊", u"邻", u"暖", u"留", u"安", u"根", u"住", u"守", u"客", u"灯", u"门", u"慢", u"日子", u"生活"]
    hits = [k for k in KW if k in creed]
    if hits:
        lines_out.append(u"%s | %s | KW=%s" % (os.path.basename(p), creed, ",".join(hits)))

io.open(OUT, "w", encoding="utf-8").write("\n".join(lines_out) + "\n")
print("PROBE3 OK -> %s (%d lines)" % (OUT, len(lines_out)))
