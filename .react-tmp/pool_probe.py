# -*- coding: utf-8 -*-
"""R309 REACT form prep: probe BigLife pools.json (rain bucket) + v17 cards.json cfg.
Read-only cross-repo. Output UTF-8 file (console GBK law)."""
import json, io

POOL = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
CARDS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\cards\MC-20260926-CENSUS-v16\cards.json"
OUT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.react-tmp\pool-probe.txt"

d = json.load(io.open(POOL, encoding="utf-8"))
lines = []
lines.append("POOL TOP KEYS: " + repr({k: (type(v).__name__, len(v) if isinstance(v, (list, dict, str)) else "") for k, v in d.items()}))

def walk(o, p, out, depth=0):
    if depth > 8 or len(out) > 400:
        return
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, p + "/" + str(k), out, depth + 1)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, p + "/" + str(i), out, depth + 1)
    elif isinstance(o, str):
        if "雨" in o:
            out.append(p + " = " + o)

hits = []
walk(d, "", hits)
lines.append("--- POOL RAIN HITS (%d) ---" % len(hits))
lines.extend(hits)

c = json.load(io.open(CARDS, encoding="utf-8"))
lines.append("--- CARDS.JSON KEYS: " + repr(sorted(c.keys())))
lines.append("video: " + json.dumps(c.get("video"), ensure_ascii=False))
lines.append("font: " + json.dumps(c.get("font"), ensure_ascii=False))
cc = c.get("cards", [])
lines.append("cards[0] keys: " + repr(sorted(cc[0].keys())) if cc else "no cards")
if cc:
    c0 = {k: v for k, v in cc[0].items() if k != "lines"}
    lines.append("cards[0] non-lines: " + json.dumps(c0, ensure_ascii=False))
    lines.append("cards[0] lines: " + json.dumps(cc[0].get("lines"), ensure_ascii=False))
lines.append("meta keys: " + repr(sorted(c.get("meta", {}).keys())))

io.open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("OK", len(hits))
