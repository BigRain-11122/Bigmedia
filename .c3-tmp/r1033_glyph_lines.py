# -*- coding: utf-8 -*-
# R1033 precise scan: RENDERED LINES ONLY (cards[].lines + aigc_notice) across ALL card-ish jsons
from fontTools.ttLib import TTCollection
import glob, json

cmap = TTCollection(r"C:\Windows\Fonts\msyh.ttc").fonts[0].getBestCmap()
SKIP = set("\n\r\t\x00") | {chr(c) for c in range(0x20)}

def chars_of(t):
    return {ch for ch in t if ch not in SKIP}

report = []
total_files = 0
allchars = set()
for p in sorted(set(glob.glob(r"data\**\cards*.json", recursive=True))):
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception:
        continue
    if not isinstance(d, dict) or "cards" not in d:
        continue
    total_files += 1
    s = chars_of(str(d.get("aigc_notice", "")))
    for c in d.get("cards", []):
        for ln in c.get("lines", []):
            s |= chars_of(str(ln))
    allchars |= s
    miss = sorted(ch for ch in s if ord(ch) not in cmap)
    if miss:
        # locate exact lines
        for i, c in enumerate(d.get("cards", []), 1):
            for ln in c.get("lines", []):
                lm = [ch for ch in chars_of(str(ln)) if ord(ch) not in cmap]
                if lm:
                    report.append("%s card%d: %s | line=%r" % (
                        p, i, ["U+%04X" % ord(x) for x in lm],
                        str(ln)[:50].encode("unicode_escape").decode()[:80]))
print("cards-style jsons with lines: %d files, %d unique chars in lines" % (total_files, len(allchars)))
m = sorted(ch for ch in allchars if ord(ch) not in cmap)
print("missing-in-lines chars: %s" % ["U+%04X" % ord(x) for x in m])
for r in report:
    print(r)
# also: where do U+2194/U+2713 live (meta prose faces)?
for cp, name in ((0x2194, "U+2194"), (0x2713, "U+2713")):
    ch = chr(cp)
    hits = []
    for p in sorted(set(glob.glob(r"data\**\cards*.json", recursive=True))):
        try:
            raw = open(p, encoding="utf-8").read()
        except Exception:
            continue
        if ch in raw:
            d = json.loads(raw)
            in_lines = any(ch in str(ln) for c in d.get("cards", []) for ln in c.get("lines", []))
            hits.append((p, in_lines))
    print("%s raw hits: %d files; in-LINES hits: %s" % (
        name, len(hits), [p for p, il in hits if il] or "NONE"))
