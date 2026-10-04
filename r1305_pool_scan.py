# -*- coding: utf-8 -*-
"""R1305 DAILY v65 pool scan: night-window position (sprite night residue + six-axes night fresh re-scan).
Post-v64 supply state: sprite weekend exhausted; six-axes daytime R1032-depletion; registered unlock
windows include night-window rows (sprite night residue). Production moment ~02:4x = literal night.
"""
import io, json, os, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
BASE = os.path.join(ROOT, "data", "storylines", "cards")
out = io.StringIO()

pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
out.write("pool structure: axes=%d sprite_buckets=%d\n" % (len(pool["axes"]), len(pool["sprite"])))

# fleet card faces (all cards.json lines + source_quote)
faces = []
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        faces.append((d, face + u"\n" + sq))
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()

# seasonal / context gate words (R972 seasonal-mismatch law + unlock-window gates)
GATES = re.compile(u"年味|春联|春雨|元宵|端午|中秋|冬至|腊|寒潮|雪|夏|空调|西瓜|蚊|大雨|暴雨|台风|雨伞|收市|开盘|交易日")

def shingle_hits(row, n=2):
    hits = []
    for i in range(len(row) - n + 1):
        g = row[i:i+n]
        for d, f in faces:
            if g in f:
                hits.append((g, d))
                break
    return hits

out.write(u"\n== sprite[night] 12 rows ==\n")
for i, row in enumerate(pool["sprite"][u"night"]):
    inflag = any(row in f for d, f in faces)
    spiritflag = row in spirit
    gate = GATES.search(row)
    sh = shingle_hits(row)
    out.write(u"night/%d %r consumed=%s spirit=%s gate=%s shingles=%s\n" % (i, row, inflag, spiritflag, gate.group(0) if gate else None, sh if sh else "ZERO"))

out.write(u"\n== axes[*][night] fresh re-scan (six axes x 18 rows, R1023-R1029 zero-clean carried) ==\nclean rows:\n")
found = 0
for ax, buckets in pool["axes"].items():
    if u"night" not in buckets:
        continue
    for i, row in enumerate(buckets[u"night"]):
        if not row:
            continue
        inflag = any(row in f for d, f in faces)
        spiritflag = row in spirit
        gate = GATES.search(row)
        sh = shingle_hits(row)
        if not inflag and not spiritflag and not gate and not sh:
            out.write(u"CLEAN %s/night/%d %r\n" % (ax, i, row))
            found += 1
out.write("six-axes night clean rows: %d\n" % found)

# also fresh scan axes weekend+morning+market_close+dusk daytime faces for completeness (holiday context)
out.write(u"\n== axes[*][weekend] fresh scan (holiday-day adjacency) ==\nclean rows:\n")
found2 = 0
for ax, buckets in pool["axes"].items():
    if u"weekend" not in buckets:
        continue
    for i, row in enumerate(buckets[u"weekend"]):
        if not row:
            continue
        inflag = any(row in f for d, f in faces)
        spiritflag = row in spirit
        gate = GATES.search(row)
        sh = shingle_hits(row)
        if not inflag and not spiritflag and not gate and not sh:
            out.write(u"CLEAN %s/weekend/%d %r\n" % (ax, i, row))
            found2 += 1
out.write("six-axes weekend clean rows: %d\n" % found2)

io.open(os.path.join(ROOT, "r1305_pool_scan.txt"), "w", encoding="utf-8").write(out.getvalue())
print("scan written; sprite-night consumed rows listed; axes-night clean=%d axes-weekend clean=%d" % (found, found2))
