# -*- coding: utf-8 -*-
"""R633: dump BigLife dialogue pool structure + proverb-grade candidates (read-only)."""
import io, os, json, re
CWD = os.path.dirname(os.path.abspath(__file__))
POOLS = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
d = json.load(io.open(POOLS, encoding="utf-8"))
OUT = io.open(os.path.join(CWD, "r633_pool.txt"), "w", encoding="utf-8")

def walk(node, path, acc):
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, path + "/" + str(k), acc)
    elif isinstance(node, list):
        for idx, item in enumerate(node):
            if isinstance(item, str):
                acc.append((path, idx, item))
            else:
                walk(item, path + "/" + str(idx), acc)
    elif isinstance(node, str):
        acc.append((path, -1, node))

acc = []
walk(d, "", acc)
OUT.write("TOTAL_LINES %d\n" % len(acc))
# proverb-grade pre-filter: aphoristic signals
sig = re.compile(r"(是.{0,10}的|像|才是|不是.{0,8}是|越.{0,4}越|才|就当|都是|要紧|讲究|规矩|本事|底气|心|路|饭|账|稳|慢|快|真|假)")
cand = []
seen = set()
for path, idx, s in acc:
    t = s.strip()
    if not t or len(t) < 6 or len(t) > 40:
        continue
    if t in seen:
        continue
    seen.add(t)
    if sig.search(t):
        cand.append((path, idx, t))
OUT.write("CANDIDATES %d\n\n== ALL CANDIDATES ==\n" % len(cand))
for path, idx, t in cand:
    OUT.write("%s [%d] %s\n" % (path, idx, t))
OUT.write("\n== STRUCTURE SAMPLE (first 5 per top key) ==\n")
for k in d:
    OUT.write("KEY %s type %s\n" % (k, type(d[k]).__name__))
    sample = json.dumps(d[k], ensure_ascii=False)[:600]
    OUT.write("SAMPLE %s: %s\n\n" % (k, sample))
OUT.close()
print("TOTAL", len(acc), "CAND", len(cand))
