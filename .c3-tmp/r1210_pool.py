# -*- coding: utf-8 -*-
"""R1210: a-leg batch 3 probe. BigLife pool expanded 1440 -> 1626 (mtime 10-04 08:06,
supply gate per R893 verdict 'TOTAL_LINES increment trigger' FIRED). Fresh walk
(read-only), dedupe vs city-spirit rows #1-64 + three codex files, and diff vs the
R893 candidate set (r893_pool.txt) to isolate NEW expansion-face candidates."""
import io, os, json, re

CWD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CWD)  # BigStream repo root
POOLS = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
CODEX = os.path.join(ROOT, "data", "storylines", "codex")

def strip_punct(s):
    return re.sub(r"[。，、；：？！…—·\"'\s（）()「」『』]", "", s)

spirit = io.open(os.path.join(CODEX, "city-spirit.md"), encoding="utf-8").read()
culture = io.open(os.path.join(CODEX, "city-culture.md"), encoding="utf-8").read()
humans = io.open(os.path.join(CODEX, "city-humanities.md"), encoding="utf-8").read()
resid = io.open(os.path.join(CODEX, "city-residents.md"), encoding="utf-8").read()
others = culture + humans + resid

# harvested texts from city-spirit table rows (all sections, #1-64)
used = set()
for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|", spirit, re.M):
    txt = m.group(2).strip().strip("*")
    used.add(strip_punct(txt))
print("used_from_spirit", len(used))

# R893 candidate set (as of 1440 baseline) for new-face diff
old_cand = set()
old_txt = io.open(os.path.join(CWD, "r893_pool.txt"), encoding="utf-8").read()
for m in re.finditer(r"^\s*\[(\d+)\]\s+(.+?)\s*$", old_txt, re.M):
    old_cand.add(strip_punct(m.group(2)))
print("old_candidates_r893", len(old_cand))

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
new_n = 0
for path, idx, s in acc:
    t = s.strip()
    if not t or len(t) < 6 or len(t) > 40:
        continue
    key = strip_punct(t)
    if not key or key in seen:
        continue
    seen.add(key)
    if key in used:
        continue  # already in city-spirit (#1-64)
    if key in strip_punct(others) or t in others:
        continue  # cross-file dedupe
    if not sig.search(t):
        continue
    cand_n += 1
    is_new = key not in old_cand
    if is_new:
        new_n += 1
    ax_sc = path.rsplit("/", 2)
    gkey = "/".join(ax_sc[-2:]) if len(ax_sc) >= 2 else path
    tag = "NEW" if is_new else "old"
    groups.setdefault(gkey, []).append((tag, idx, t))

out = io.open(os.path.join(CWD, "r1210_pool.txt"), "w", encoding="utf-8")
out.write("TOTAL_LINES %d  (r893/r633 baseline 1440, delta %+d)\n" % (total, total - 1440))
out.write("CANDIDATES_AFTER_DEDUPE %d  NEW_FACE %d  OLD_FACE_REMAIN %d\n\n" % (cand_n, new_n, cand_n - new_n))
for gk in sorted(groups):
    rows = groups[gk]
    n_new = sum(1 for r in rows if r[0] == "NEW")
    out.write("== %s == (new %d)\n" % (gk, n_new))
    for tag, idx, t in rows:
        out.write("  [%s][%d] %s\n" % (tag, idx, t))
    out.write("\n")
out.close()
print("total", total, "cand", cand_n, "new_face", new_n)
