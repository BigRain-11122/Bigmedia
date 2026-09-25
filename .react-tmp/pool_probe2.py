# -*- coding: utf-8 -*-
"""R313 pool probe for REACT-v2 topic mapping (write UTF-8 file, no console CJK)."""
import io, json, re, collections

POOL = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
OUT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.react-tmp\pool-probe2.txt"

p = json.load(io.open(POOL, encoding="utf-8"))
axes = p["axes"]; sprite = p["sprite"]

buckets = set()
for ax, bmap in axes.items():
    buckets.update(bmap.keys())
lines = []
lines.append("AXES: %s" % sorted(axes.keys()))
lines.append("BUCKETS(%d): %s" % (len(buckets), sorted(buckets)))
lines.append("SPRITE buckets: %s" % sorted(sprite.keys()))
lines.append("")

def walk(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, path + "/" + str(k), out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path + "/%d" % i, out)
    else:
        out.append((path, str(node)))

allq = []
for ax in axes:
    walk(axes[ax], "/" + ax, allq)
walk(sprite, "/sprite", allq)
lines.append("TOTAL QUOTES: %d" % len(allq))
lines.append("")

KW = {
    "FOOD-topic3": ["吃", "饭", "面", "菜", "味", "馋", "嘴", "灶", "汤", "点心", "小吃"],
    "PRICE-topic5": ["价", "涨", "贵", "行情", "块钱", "肉", "牛肉"],
    "HAIR-topic9": ["发型", "头发", "剪", "潮", "打扮", "时髦"],
}
for tag, kws in KW.items():
    hits = [(pa, q) for pa, q in allq if any(k in q for k in kws)]
    lines.append("=== %s hits: %d ===" % (tag, len(hits)))
    for pa, q in hits[:40]:
        lines.append("%s = %s" % (pa, q))
    lines.append("")

# bucket-level counts for market_open/market_close (price topic) and any meal-ish bucket
for b in sorted(buckets):
    cnt = sum(len(v) for v in axes[ax].get(b, []) if isinstance(v, list) for ax in axes) if False else None
lines.append("=== bucket quote counts per axis ===")
cnt = collections.Counter()
for ax in axes:
    for b, val in axes[ax].items():
        n = 0
        if isinstance(val, list):
            n = len(val)
        elif isinstance(val, dict):
            n = sum(len(v) if isinstance(v, list) else 1 for v in val.values())
        cnt[b] += n
for b, n in sorted(cnt.items()):
    lines.append("%s: %d" % (b, n))
lines.append("sprite: %d" % len(sprite))

io.open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("OK", len(allq))
