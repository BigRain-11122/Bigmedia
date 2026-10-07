# -*- coding: utf-8 -*-
"""r1676_react_probe.py - REACT-v11 (F-159) topic mapping probe.

Candidate: zhihu-hot 2026-10-08 #8 "世界上最宜居的城市是哪一座？"
Method: mechanical scan of BigLife pools.json buckets for livable-city
domain keywords; three-axis direct mapping check per bucket; bucket
freshness ledger vs REACT v1-v10 series usage.
Output: UTF-8 file .c3-tmp/r1676_react_probe.txt
"""
import io, json, os, re

POOL = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r1676_react_probe.txt")

pools = json.load(io.open(POOL, encoding="utf-8"))
axes = pools["axes"]

# REACT series bucket usage ledger (v1-v10, from finished.md / review trail)
# v9=heatwave (喝水解渴), v10=morning (破烂变黄金), v6=morning; fresh candidates
# noted at R1548: dusk / typhoon / coldsnap / ceo_order
used = {"v6": "morning", "v9": "heatwave", "v10": "morning"}

KW = [u"宜居", u"住", u"家", u"城", u"街", u"坊", u"邻", u"舒服", u"安",
      u"生活", u"烟火", u"摊", u"茶", u"客", u"留", u"慢", u"闲", u"惬意"]

lines_out = []
lines_out.append(u"== A) axes x buckets inventory ==")
inv = {}
for ax, buckets in axes.items():
    for b, rows in buckets.items():
        inv.setdefault(b, {})[ax] = len(rows)
for b in sorted(inv):
    lines_out.append(u"%s: %s" % (b, " ".join(u"%s=%d" % (a, n) for a, n in sorted(inv[b].items()))))

lines_out.append(u"")
lines_out.append(u"== B) keyword hits per bucket (livable-city domain) ==")
for b in sorted(inv):
    for ax in sorted(inv[b]):
        hits = [r for r in axes[ax][b] if any(k in r for k in KW)]
        if hits:
            for h in hits:
                lines_out.append(u"%s/%s: %s" % (ax, b, h))

lines_out.append(u"")
lines_out.append(u"== C) fresh-bucket three-axis check ==")
for b in ("dusk", "typhoon", "coldsnap", "ceo_order", "weekend", "night", "festival"):
    have = [ax for ax in sorted(axes) if b in axes.get(ax, {})]
    lines_out.append(u"%s axes=%s" % (b, have))

io.open(OUT, "w", encoding="utf-8").write("\n".join(lines_out) + "\n")
print("PROBE OK -> %s (%d lines)" % (OUT, len(lines_out)))
