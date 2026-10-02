# -*- coding: utf-8 -*-
# R1033 OSS slice-2 knife-3: local evidence probe - glyph coverage audit
# Corpus faces:
#   RENDERED (text actually burned on card faces / video frames):
#     A) all data/storylines/cards/**/cards.json -> aigc_notice + cards[].lines + meta.topic
#     B) all *.srt under data/** (burned subtitle tracks)
#   SOURCE (candidate text that may become rendered via verbatim laws):
#     C) data/intel/daily/*.md (hot titles - REACT verbatim source)
#     D) all *.beats.txt under data/** (vo/card columns)
# Fonts actually used by the pipeline (comic_compose.py / render_card_video.py / emotive_tts):
#   C:/Windows/Fonts/msyh.ttc (face 0) + msyhbd.ttc (h1 bold)
# Verdict per face: unique chars missing from msyh face-0 cmap (and bold cmap).
import glob, json, os, re, sys
from fontTools.ttLib import TTCollection

OUT = r".c3-tmp\r1033_glyph_audit.txt"

def face_cmap(path):
    coll = TTCollection(path)
    return coll.fonts[0].getBestCmap()

cmap = face_cmap(r"C:\Windows\Fonts\msyh.ttc")
cmap_b = face_cmap(r"C:\Windows\Fonts\msyhbd.ttc")

SKIP = set("\n\r\t\x00") | {chr(c) for c in range(0x20)}

def chars_of(text):
    return {ch for ch in text if ch not in SKIP}

def collect(rendered, sources):
    # Face A: cards.json
    for p in glob.glob(r"data\storylines\cards\**\cards.json", recursive=True):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            print("WARN parse", p, e); continue
        rendered.setdefault("A:" + p, set()).update(chars_of(d.get("aigc_notice", "")))
        rendered.setdefault("A:" + p, set()).update(chars_of(str(d.get("meta", {}).get("topic", ""))))
        for c in d.get("cards", []):
            for ln in c.get("lines", []):
                rendered.setdefault("A:" + p, set()).update(chars_of(ln))
    # Face B: srt files under data/
    for p in glob.glob(r"data\**\*.srt", recursive=True):
        try:
            t = open(p, encoding="utf-8-sig", errors="replace").read()
        except Exception as e:
            print("WARN read", p, e); continue
        rendered.setdefault("B:" + p, set()).update(chars_of(t))
    # Face C: daily briefs
    for p in glob.glob(r"data\intel\daily\*.md"):
        t = open(p, encoding="utf-8", errors="replace").read()
        sources.setdefault("C:" + p, set()).update(chars_of(t))
    # Face D: beats
    for p in glob.glob(r"data\**\*.beats.txt", recursive=True):
        t = open(p, encoding="utf-8", errors="replace").read()
        sources.setdefault("D:" + p, set()).update(chars_of(t))

rendered, sources = {}, {}
collect(rendered, sources)

def audit(store, label):
    allchars = set()
    for s in store.values():
        allchars |= s
    missing = {ch: [] for ch in sorted(allchars) if ord(ch) not in cmap}
    missing_b = {ch: [] for ch in sorted(allchars) if ord(ch) not in cmap_b}
    per_file = {}
    for p, s in store.items():
        m = sorted(ch for ch in s if ord(ch) not in cmap)
        if m:
            per_file[p] = m
    lines = []
    lines.append("== %s face: %d files, %d unique chars ==" % (label, len(store), len(allchars)))
    lines.append("missing from msyh.ttc face0: %d chars" % len(missing))
    for ch in missing:
        cps = "U+%04X" % ord(ch)
        hits = [p for p in per_file if ch in per_file[p]]
        lines.append("  %r %s files=%d e.g. %s" % (ch, cps, len(hits), hits[0] if hits else "?"))
    lines.append("missing from msyhbd.ttc face0: %d chars" % len(missing_b))
    for ch in list(missing_b)[:10]:
        lines.append("  bold-missing %r U+%04X" % (ch, ord(ch)))
    return lines

out = []
out.append("R1033 glyph-coverage audit (OSS slice-2 knife-3 local evidence)")
out.append("fonts: msyh.ttc face0 cmap=%d codepoints; msyhbd.ttc face0 cmap=%d" % (len(cmap), len(cmap_b)))
out += audit(rendered, "RENDERED")
out += audit(sources, "SOURCE")
# emoji / symbol census in source face (REACT hot-title latent risk quantifier)
emoji = [ch for s in sources.values() for ch in s if ord(ch) >= 0x1F000 or 0x2600 <= ord(ch) <= 0x27BF]
out.append("emoji/symbol-range chars in SOURCE face: %d occurrences, %d unique: %r" % (
    len(emoji), len(set(emoji)), sorted(set(emoji))))
open(OUT, "w", encoding="utf-8").write("\n".join(out))
print("written", OUT, "rendered_files=%d source_files=%d" % (len(rendered), len(sources)))
