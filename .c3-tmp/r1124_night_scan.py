# -*- coding: utf-8 -*-
# R1124: sprite night-bucket residue fresh scan (R1123 pointer: night-window continuation position)
# Criteria per series law: pool verbatim rows; skip night/8 (v54 consumed); city-spirit NOT_IN;
# card-face-level fleet dedup (R1010 law: lines + source_quote); 2+ char shingle probe;
# onomatopoeia 4th-use block (post-v64); night rows = literal-night window legal (R1020).
import json, io, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
BASE = os.path.join(ROOT, "data", "storylines", "cards")
T = os.path.join(ROOT, ".c3-tmp")
OUT = []

pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
nb = pool["sprite"]["night"]
assert len(nb) == 12, "sprite night bucket != 12 rows"
OUT.append("sprite night bucket 12 rows (R982 structure):")
for i, l in enumerate(nb):
    OUT.append("  night/%d: %s" % (i, l))

spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()

# fleet card faces (all existing pieces incl v64)
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        faces[d] = (face, sq)
OUT.append("fleet pieces scanned: %d" % len(faces))

ONO_BLOCKED = [u"叮叮当", u"嗡嗡嗡", u"叮咚"]  # onomatopoeia band 3-link formed v50/v63/v64 -> 4th use blocked

def shingles(s):
    return [s[i:i+2] for i in range(len(s) - 1)] + [s[i:i+3] for i in range(len(s) - 2)]

clean = []
for i, l in enumerate(nb):
    if i == 8:
        OUT.append("night/%d SKIP: v54 consumed row" % i)
        continue
    tags = []
    if l in spirit:
        tags.append("city-spirit HIT")
    full_hits = sorted(d for d, (f, sq) in faces.items() if l in f or l in sq)
    if full_hits:
        tags.append("full-line consumed by %s" % u",".join(full_hits[:3]))
    # 2+ char shingle probe (word-level overlap with fleet card faces)
    sh_hits = {}
    for sh in shingles(l):
        h = sorted(d for d, (f, sq) in faces.items() if sh in f or sh in sq)
        if h:
            sh_hits[sh] = h[:4]
    if sh_hits:
        tags.append("shingle hits: " + u"; ".join(u"%s->%s" % (k, u",".join(v)) for k, v in sorted(sh_hits.items())))
    # onomatopoeia 4th-use check: row itself contains a blocked onomatopoeia token
    for t in ONO_BLOCKED:
        if t in l:
            tags.append("onomatopoeia 4th-use BLOCKED token %s" % t)
    OUT.append("night/%d [%s] %s" % (i, l, ("GATED: " + " | ".join(tags)) if tags else "CLEAN"))
    if not tags:
        clean.append((i, l))

OUT.append("")
OUT.append("VERDICT: clean rows = %d" % len(clean))
for i, l in clean:
    OUT.append("  CANDIDATE night/%d: %s" % (i, l))

io.open(os.path.join(T, "r1124_night_scan.txt"), "w", encoding="utf-8").write(u"\n".join(OUT))
print("SCAN DONE clean=%d" % len(clean))
for i, l in clean:
    print("CANDIDATE night/%d: %s" % (i, l))
