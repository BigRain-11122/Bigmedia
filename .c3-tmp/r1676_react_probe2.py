# -*- coding: utf-8 -*-
"""r1676_react_probe2.py - REACT series bucket ledger + anchor creed scan.

1) Scan MC-*-REACT-*-tmp/cards.json source_facts for bucket names -> usage ledger
2) Scan BigLife census anchors for creed lines in livable-city domain
Output: UTF-8 .c3-tmp/r1676_react_probe2.txt
"""
import io, json, os, glob, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
CARDS = os.path.join(ROOT, "data", "storylines", "cards")
ANCH = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
OUT = os.path.join(ROOT, ".c3-tmp", "r1676_react_probe2.txt")

BUCKETS = ["morning", "dusk", "night", "weekend", "festival", "heatwave",
           "coldsnap", "typhoon", "ceo_order", "rain", "market_open", "market_close"]

lines_out = []
lines_out.append(u"== 1) REACT series bucket usage ledger (cards.json source_facts) ==")
usage = {}
for d in sorted(os.listdir(CARDS)):
    if "REACT" not in d:
        continue
    cj = os.path.join(CARDS, d, "cards.json")
    if not os.path.exists(cj):
        continue
    c = json.load(io.open(cj, encoding="utf-8"))
    sf = c.get("meta", {}).get("source_facts", "")
    found = [b for b in BUCKETS if b in sf]
    usage[d] = found
    lines_out.append(u"%s -> %s" % (d, found))

lines_out.append(u"")
lines_out.append(u"== 2) anchor creed scan (livable-city domain KW) ==")
KW = [u"家", u"城", u"街", u"坊", u"邻", u"暖", u"留", u"安", u"根", u"住", u"守", u"客", u"灯", u"门"]
for p in sorted(glob.glob(os.path.join(ANCH, "C-*.md"))):
    txt = io.open(p, encoding="utf-8").read()
    m = re.search(u"信条[：:]\s*(.+)", txt)
    if not m:
        continue
    creed = m.group(1).strip()
    # name line
    nm = re.search(u"^[#＃\s]*([^\n]+)", txt)
    if any(k in creed for k in KW):
        lines_out.append(u"%s | %s" % (os.path.basename(p), creed))

io.open(OUT, "w", encoding="utf-8").write("\n".join(lines_out) + "\n")
print("PROBE2 OK -> %s (%d lines)" % (OUT, len(lines_out)))
