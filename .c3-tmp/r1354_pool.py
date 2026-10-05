# -*- coding: utf-8 -*-
"""R1354: #86 a-leg batch-4 evaluation probe. Fresh walk of BigLife dialogue pool
(read-only), dynamically excludes city-spirit rows 1-83 (batches 0-3) + cross-file
dedupe (culture/humanities/residents) + fleet-level candidates already consumed by
DAILY v1-v67 / REACT v1-v8 / L-cards. Dump remaining candidates for proverb-density
judgment (batch-4 go / no-go honest evaluation per R1353 next-pointer)."""
import io, os, json, re

CWD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CWD)  # BigStream repo root
POOLS = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
CODEX = os.path.join(ROOT, "data", "storylines", "codex")

spirit = io.open(os.path.join(CODEX, "city-spirit.md"), encoding="utf-8").read()
culture = io.open(os.path.join(CODEX, "city-culture.md"), encoding="utf-8").read()
humans = io.open(os.path.join(CODEX, "city-humanities.md"), encoding="utf-8").read()
resid = io.open(os.path.join(CODEX, "city-residents.md"), encoding="utf-8").read()
others = culture + humans + resid

def strip_punct(s):
    return re.sub(r"[。，、；：？！…—·\"'\s（）()「」『』]", "", s)

# harvested texts from city-spirit table rows: | n | text | source |
used = set()
for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|", spirit, re.M):
    txt = m.group(2).strip().strip("*")
    used.add(strip_punct(txt))
print("used_from_spirit", len(used))

d = json.load(io.open(POOLS, encoding="utf-8"))

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
total = len(acc)

sig = re.compile(r"(是.{0,10}的|像|才是|不是.{0,8}是|越.{0,4}越|才|就当|都是|要紧|讲究|规矩|本事|底气|心|路|饭|账|稳|慢|快|真|假)")

groups = {}
seen = set()
cand_n = 0
for path, idx, s in acc:
    t = s.strip()
    if not t or len(t) < 6 or len(t) > 40:
        continue
    key = strip_punct(t)
    if not key or key in seen:
        continue
    seen.add(key)
    if key in used:
        continue  # already in city-spirit (seed + batches 1-3, rows 1-83)
    if key in strip_punct(others) or t in others:
        continue  # cross-file dedupe (culture/humanities/residents)
    if not sig.search(t):
        continue
    cand_n += 1
    ax_sc = path.rsplit("/", 2)
    gkey = "/".join(ax_sc[-2:]) if len(ax_sc) >= 2 else path
    groups.setdefault(gkey, []).append((idx, t))

out = io.open(os.path.join(CWD, "r1354_pool.txt"), "w", encoding="utf-8")
out.write("TOTAL_LINES %d  (r633 baseline 1440)\n" % total)
out.write("CANDIDATES_AFTER_DEDUPE %d  (r1353 run: 433 -> minus batch3 19 = 414 expected)\n\n" % cand_n)
for gk in sorted(groups):
    out.write("== %s ==\n" % gk)
    for idx, t in groups[gk]:
        out.write("  [%d] %s\n" % (idx, t))
    out.write("\n")
out.close()
print("total", total, "cand", cand_n, "groups", len(groups))
