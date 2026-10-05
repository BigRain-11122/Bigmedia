# -*- coding: utf-8 -*-
"""r1337 E30 dusk-face supply re-derive (derive-blind-spot law R1095: do not trust the
last post-note alone; independent fresh scan of the CURRENT window face).
Current window: 2026-10-05 Mon national-holiday day-5, ~07:0x local = literal dusk.
Faces scanned: axes6 x dusk + sprite x dusk. Evening dusk face never scanned for DAILY before (R1123/R1124/R1305/R1320/R1326 covered morning/weekend/night only) - independent derive
(R1322 post-v67: single gated row 烟火/13 until 10-08 reopen; night face zero R1124/R1305).
Dedup law = card-face level (R1010): lines + source_quote of every fleet cards.json.
"""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "data", "storylines", "cards")

pool = json.load(io.open(os.path.join(ROOT, "..", "..", "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()

faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, "cards.json")
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        faces[d] = face + u"\n" + sq

def shingles(s, n=2):
    s = u"".join(ch for ch in s if not ch.isspace())
    return set(s[i:i+n] for i in range(len(s)-n+1))

FLEET_SH = set()
for f in faces.values():
    FLEET_SH |= shingles(f)
SPIRIT_SH = shingles(spirit)

out = [u"r1337 E30 dusk-face fresh scan (window 2026-10-05 ~07:0x holiday-Mon dusk; independent re-derive)"]
clean_axes = []
for ax in pool["axes"]:
    nb = pool["axes"][ax]["dusk"]
    for i, line in enumerate(nb):
        full_hit = [d for d, f in faces.items() if line in f]
        if full_hit:
            out.append(u"[CONSUMED-CARDFACE %s/dusk/%d] %s | in %s" % (ax, i, line, u",".join(full_hit)))
            continue
        sh = shingles(line)
        col = sorted(sh & FLEET_SH)
        spirit_col = sorted(sh & SPIRIT_SH)
        tags = []
        if not col:
            tags.append(u"CLEAN %s/dusk/%d" % (ax, i))
            clean_axes.append((ax, i, line))
        out.append(u"[%s/dusk/%d] %s | card-face-shingles=%d %s%s%s" % (
            ax, i, line, len(col), (u",".join(col[:6]) if col else u"ZERO"),
            (u"| spirit-layer=%d %s" % (len(spirit_col), u",".join(spirit_col[:4]))) if spirit_col else u"",
            (u" | " + u"; ".join(tags)) if tags else u""))
for i, line in enumerate(pool["sprite"]["dusk"]):
    full_hit = [d for d, f in faces.items() if line in f]
    if full_hit:
        out.append(u"[CONSUMED-CARDFACE sprite/dusk/%d] %s | in %s" % (i, line, u",".join(full_hit)))
        continue
    sh = shingles(line)
    col = sorted(sh & FLEET_SH)
    if not col:
        clean_axes.append((u"sprite", i, line))
    out.append(u"[sprite/dusk/%d] %s | shingle-colisions=%d %s%s" % (
        i, line, len(col), (u",".join(col[:6]) if col else u"ZERO"),
        u" CLEAN" if not col else u""))
out.append(u"")
out.append(u"dusk-face CLEAN rows: %s" % (u" ; ".join(u"%s/dusk/%d %s" % (a, i, l) for a, i, l in clean_axes) or u"NONE"))
io.open(os.path.join(ROOT, ".c3-tmp", "r1337_dusk_scan.txt"), "w", encoding="utf-8").write(u"\n".join(out))
print(u"\n".join(out[-4:]))
print("SCAN OK rows written:", len(out))
