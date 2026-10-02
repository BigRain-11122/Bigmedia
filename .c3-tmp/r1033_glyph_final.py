# -*- coding: utf-8 -*-
# R1033 final glyph-coverage audit - extended corpus (video-line matched cards included)
from fontTools.ttLib import TTCollection
import glob, json

def cmap_of(p):
    return TTCollection(p).fonts[0].getBestCmap()

cmap = cmap_of(r"C:\Windows\Fonts\msyh.ttc")
cmap_b = cmap_of(r"C:\Windows\Fonts\msyhbd.ttc")
SKIP = set("\n\r\t\x00") | {chr(c) for c in range(0x20)}

def chars_of(t):
    return {ch for ch in t if ch not in SKIP}

faces = {}
# Face A: L-card poster cards (data/storylines/cards/**/cards.json)
for p in glob.glob(r"data\storylines\cards\**\cards.json", recursive=True):
    d = json.load(open(p, encoding="utf-8"))
    s = chars_of(str(d.get("aigc_notice", "")))
    for c in d.get("cards", []):
        for ln in c.get("lines", []):
            s |= chars_of(ln)
    faces["A:" + p] = s
# Face A2: video-line matched cards (data/**/cards*.json, excl. Face A dupes)
for p in glob.glob(r"data\**\cards*.json", recursive=True):
    if p in faces:
        continue
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception:
        continue
    body = json.dumps(d, ensure_ascii=False)
    s = chars_of(body)
    # keep only the card-line-relevant scan (whole-file scan is conservative)
    faces["A2:" + p] = s
# Face B: burned subtitle tracks
for p in glob.glob(r"data\**\*.srt", recursive=True):
    t = open(p, encoding="utf-8-sig", errors="replace").read()
    faces["B:" + p] = chars_of(t)

allchars = set()
for s in faces.values():
    allchars |= s
miss = sorted(ch for ch in allchars if ord(ch) not in cmap)
miss_b = sorted(ch for ch in allchars if ord(ch) not in cmap_b)

out = []
out.append("R1033 FINAL glyph audit (extended corpus)")
out.append("corpus: %d files, %d unique chars" % (len(faces), len(allchars)))
out.append("missing from msyh.ttc face0: %s" % [ "U+%04X" % ord(ch) for ch in miss ])
for ch in miss:
    hits = [p for p, s in faces.items() if ch in s]
    out.append("  U+%04X in %d file(s): %s" % (ord(ch), len(hits), hits))
out.append("missing from msyhbd.ttc face0: %s" % [ "U+%04X" % ord(ch) for ch in miss_b ])
open(r".c3-tmp\r1033_glyph_audit_final.txt", "w", encoding="utf-8").write("\n".join(out))
print("files=%d chars=%d miss_reg=%d miss_bold=%d" % (len(faces), len(allchars), len(miss), len(miss_b)))
for ch in miss:
    hits = [p for p, s in faces.items() if ch in s]
    print("U+%04X -> %d files: %s" % (ord(ch), len(hits), [h.split(chr(92))[-1] for h in hits][:4]))
