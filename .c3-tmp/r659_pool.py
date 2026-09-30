# -*- coding: utf-8 -*-
"""R659: pools.json delta probe vs r640 baseline (1440) + proverb-grade filter + dedup vs city-spirit.md."""
import io, os, json, re

CWD = os.path.dirname(os.path.abspath(__file__))
POOLS = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
SPIRIT = os.path.join(CWD, "..", "data", "storylines", "codex", "city-spirit.md")

d = json.load(io.open(POOLS, encoding="utf-8"))
acc = []

def walk(node, path, acc):
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, path + "/" + str(k), acc)
    elif isinstance(node, list):
        for idx, item in enumerate(node):
            if isinstance(item, str):
                acc.append((path + "/" + str(idx), item))
            else:
                walk(item, path + "/" + str(idx), acc)
    elif isinstance(node, str):
        acc.append((path, node))

walk(d, "", acc)
out = io.open(os.path.join(CWD, "r659_pool.txt"), "w", encoding="utf-8")
out.write("TOTAL_LEAVES %d\n" % len(acc))

# baseline: r640_pool.txt bucket counts (1440 era)
base_counts = {}
for l in io.open(os.path.join(CWD, "r640_pool.txt"), encoding="utf-8"):
    m = re.match(r"(.+) \((\d+)\)$", l.strip())
    if m:
        base_counts[m.group(1)] = int(m.group(2))

# current bucket census (top3 path levels, same as r640)
import collections
cur = collections.Counter()
for p, _ in acc:
    parts = p.strip("/").split("/")
    if len(parts) >= 3:
        cur["/".join(parts[:3])] += 1
new_buckets = {k: v for k, v in cur.items() if k not in base_counts}
grown = {k: v - base_counts[k] for k, v in cur.items() if k in base_counts and v != base_counts[k]}
out.write("BASE_BUCKETS %d CUR_BUCKETS %d NEW_BUCKETS %d GROWN_BUCKETS %d\n" % (
    len(base_counts), len(cur), len(new_buckets), len(grown)))
for k, v in sorted(new_buckets.items()):
    out.write("NEW_BUCKET %s (%d)\n" % (k, v))
for k, v in sorted(grown.items()):
    out.write("GROWN %s +%d\n" % (k, v))

# delta leaves = leaves in new/grown buckets (line-level whole-bucket delta for new buckets;
# for grown buckets, take leaves whose text not seen in r633 candidate dump)
r633_txt = io.open(os.path.join(CWD, "r633_pool.txt"), encoding="utf-8").read()
spirit_txt = io.open(SPIRIT, encoding="utf-8").read()

sig = re.compile(r"(是.{0,10}的|像|才是|不是.{0,8}是|越.{0,4}越|才|就当|都是|要紧|讲究|规矩|本事|底气|心|路|饭|账|稳|慢|快|真|假)")
delta = []
for p, s in acc:
    parts = p.strip("/").split("/")
    b = "/".join(parts[:3]) if len(parts) >= 3 else p
    if b in new_buckets:
        delta.append((p, s, "NEW_BUCKET"))
    elif b in grown:
        if s not in r633_txt:
            delta.append((p, s, "GROWN_NEWTEXT"))
out.write("DELTA_LEAVES %d\n" % len(delta))
cands = []
seen = set()
for p, s, kind in delta:
    t = s.strip()
    if not t or len(t) < 6 or len(t) > 40:
        continue
    if t in seen or t in spirit_txt:
        continue
    seen.add(t)
    if sig.search(t):
        cands.append((p, t, kind))
out.write("PROVERB_CANDS %d\n" % len(cands))
for p, t, kind in cands:
    out.write("CAND [%s] %s || %s\n" % (kind, p, t))
out.close()
print("done -> r659_pool.txt; total=%d delta=%d" % (len(acc), len(delta)))
