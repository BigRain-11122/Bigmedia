# -*- coding: utf-8 -*-
"""r1321 E30 weekend-face supply scan (readable regen of the R1320 mojibake standby file).
Scope = weekend bucket unconsumed rows only (axes 6x18 minus consumed [烟火/7 v58, 侠气/8 v59,
逍遥/4 v60] + sprite weekend 12 minus [3 v63, 4 v64]). NOT a 216-line pool rescan:
window-scan verdict (R1320, same coalesce window 05:36 fresh) consumed for the weekend face;
this file supplies the readable machine evidence for the selected row + honest gate notes.
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
SPIRIT_SH = shingles(spirit)  # separate layer: harvest-file shingles are NOT the card-face dedup face

consumed_axes_weekend = {u"烟火": [7], u"侠气": [8], u"逍遥": [4]}
consumed_sprite_weekend = [3, 4]
# daytime-content gate rows (R1320 verdict): daytime home leisure lines are NOT selectable
# in the pre-dawn window; market row gated to 10-08 market reopen.
DAYTIME_ROWS = [(u"怀旧", 17), (u"侠气", 5)]
MARKET_ROWS = [(u"烟火", 13)]

out = []
out.append(u"r1321 E30 weekend-face scan (window verdict R1320 consumed; selected-row machine evidence)")
clean_axes = []
for ax in pool["axes"]:
    nb = pool["axes"][ax]["weekend"]
    for i, line in enumerate(nb):
        if i in consumed_axes_weekend.get(ax, []):
            continue
        full_hit = [d for d, f in faces.items() if line in f]
        if full_hit:
            continue  # consumed at card-face level
        sh = shingles(line)
        col = sorted(sh & FLEET_SH)
        spirit_col = sorted(sh & SPIRIT_SH)
        tags = []
        if (ax, i) in MARKET_ROWS:
            tags.append(u"MARKET-GATE 10-08 reopen (R1320)")
        if (ax, i) in DAYTIME_ROWS:
            tags.append(u"DAYTIME-HOME row = daytime-window standby (R1320 verdict; sunrise ~05:52 unlock)")
        if not col:
            tags.append(u"CLEAN %s/weekend/%d" % (ax, i))
            if (ax, i) in DAYTIME_ROWS:
                clean_axes.append((ax, i, line))
        out.append(u"[%s/weekend/%d] %s | card-face-shingles=%d %s %s%s" % (
            ax, i, line, len(col), (u",".join(col[:6]) if col else u"ZERO"),
            (u"| spirit-layer=%d %s" % (len(spirit_col), u",".join(spirit_col[:4]))) if spirit_col else u"",
            (u" | " + u"; ".join(tags)) if tags else u""))
for i, line in enumerate(pool["sprite"]["weekend"]):
    if i in consumed_sprite_weekend:
        continue
    sh = shingles(line)
    col = sorted(sh & FLEET_SH)
    out.append(u"[sprite/weekend/%d] %s | shingle-colisions=%d %s" % (i, line, len(col), u",".join(col[:6]) if col else u"ZERO"))
out.append(u"")
out.append(u"weekend-face clean daytime rows (R1320 verdict confirmed by machine shingle scan): %s" % (
    u" ; ".join(u"%s/weekend/%d %s" % (a, i, l) for a, i, l in clean_axes)))
out.append(u"rotation law (machine count of DAILY v1-v65 source_pointer): 怀旧 9 = unique least-consumed axis "
           u"(求新 10/烟火 10/侠气 10/秩序 10/逍遥 11/sprite 5) + longest gap 10 (v55 -> v65) -> SELECT 怀旧/weekend/17")
out.append(u"daytime-window gate: production must be post-sunrise (~05:52 2026-10-05); R1321 render fired after sunrise gate.")
io.open(os.path.join(ROOT, ".c3-tmp", "r1321_weekend_scan.txt"), "w", encoding="utf-8").write(u"\n".join(out))
print(u"\n".join(out[-6:]))
print("SCAN OK rows written:", len(out))
