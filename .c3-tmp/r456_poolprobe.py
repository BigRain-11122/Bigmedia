# -*- coding: utf-8 -*-
# r456 probe: dump every market_close bucket in BigLife pools.json (all pool trees,
# any depth) with 0-based indices, to a UTF-8 file. ASCII console output only.
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
POOLS = os.path.join(HERE, "..", "..", "..", "life", "BigLife", "cognition", "pools.json")
OUT = os.path.join(HERE, "r456_market_close_dump.txt")

pools = json.load(io.open(POOLS, encoding="utf-8"))
out = []
top_keys = sorted(pools.keys())
out.append("TOP-LEVEL KEYS: " + ", ".join(top_keys))
counts = {}


def walk(node, path):
    if isinstance(node, dict):
        for k in sorted(node.keys()):
            walk(node[k], path + [k])
    elif isinstance(node, list):
        key = "/".join(path)
        counts[key] = len(node)
        if path and path[-1] == "market_close":
            out.append("")
            out.append("== %s ==" % key)
            for i, ln in enumerate(node):
                out.append("%d %s" % (i, ln))


walk(pools, [])
out.append("")
out.append("BUCKET SIZES (all):")
for k in sorted(counts):
    out.append("  %s -> %d lines" % (k, counts[k]))
io.open(OUT, "w", encoding="utf-8").write("\n".join(out))
print("DUMP OK lines=%d buckets=%d" % (len(out), len(counts)))
