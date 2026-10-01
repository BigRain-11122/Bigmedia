# -*- coding: utf-8 -*-
"""R893 verify: batch-2 rows (#45-64) of city-spirit.md must (a) match a pool
line verbatim modulo trailing punctuation, (b) not duplicate rows 1-44,
(c) not appear in the other codex files. Output UTF-8 evidence file."""
import io, os, json, re

CWD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CWD)
CODEX = os.path.join(ROOT, "data", "storylines", "codex")
POOLS = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"

def norm(s):
    return re.sub(r"[。，、；：？！…—\s]", "", s.strip())

spirit = io.open(os.path.join(CODEX, "city-spirit.md"), encoding="utf-8").read()
rows = {}
for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", spirit, re.M):
    rows[int(m.group(1))] = (m.group(2).strip().strip("*"), m.group(3).strip())

batch2 = [(n, rows[n][0], rows[n][1]) for n in sorted(rows) if 45 <= n <= 64]
batch1 = {norm(rows[n][0]) for n in rows if n < 45}

d = json.load(io.open(POOLS, encoding="utf-8"))
pool_texts = set()
def walk(node):
    if isinstance(node, dict):
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for it in node:
            walk(it)
    elif isinstance(node, str):
        pool_texts.add(node.strip())
walk(d)

others = ""
for f in ("city-culture.md", "city-humanities.md", "city-residents.md"):
    others += io.open(os.path.join(CODEX, f), encoding="utf-8").read()

out = io.open(os.path.join(CWD, "r893_verify.txt"), "w", encoding="utf-8")
ok = True
out.write("batch2_rows %d\n" % len(batch2))
for n, txt, src in batch2:
    key = norm(txt)
    in_pool = key in {norm(p) for p in pool_texts}
    dup_old = key in batch1
    in_others = txt in others
    status = "OK" if (in_pool and not dup_old and not in_others) else "FAIL"
    if status == "FAIL":
        ok = False
    out.write("#%d [%s] pool=%s dup_old=%s dup_cross=%s | %s | %s\n" % (n, status, in_pool, dup_old, in_others, txt, src))
# axis/scene coverage tally
axes = {}
for n, txt, src in batch2:
    ax = src.split("·")[1].split("（")[0]
    axes[ax] = axes.get(ax, 0) + 1
out.write("\naxis_coverage %s\n" % json.dumps(axes, ensure_ascii=False))
scenes = sorted({re.search(r"（(.+?)场景", s).group(1) for _, _, s in batch2})
out.write("scenes %s\n" % ",".join(scenes))
out.write("VERDICT %s\n" % ("PASS" if ok and len(batch2) == 20 else "FAIL"))
out.close()
print("rows", len(batch2), "ok", ok)
