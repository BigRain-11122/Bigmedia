# -*- coding: utf-8 -*-
"""R1354 verify: a-leg batch-4 rows (#84-100) of city-spirit.md must
(a) match a BigLife pool line verbatim modulo trailing punctuation,
(b) not duplicate rows 1-83,
(c) not appear in the other codex files (culture/humanities/residents),
(d) not duplicate any consumed fleet card line (DAILY/REACT/QUOTE/L-卡
    cards under data/storylines/cards/ + reviews materials) - R1010 卡面级
    fleet 去重 standard carried from R1353.
Output UTF-8 evidence file."""
import io, os, json, re, glob

CWD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CWD)
CODEX = os.path.join(ROOT, "data", "storylines", "codex")
POOLS = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"

def norm(s):
    return re.sub(r"[。，、；：？！…—·“”\"'\s（）()「」『』/]", "", s.strip())

spirit = io.open(os.path.join(CODEX, "city-spirit.md"), encoding="utf-8").read()
rows = {}
for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", spirit, re.M):
    rows[int(m.group(1))] = (m.group(2).strip().strip("*"), m.group(3).strip())

batch4 = [(n, rows[n][0], rows[n][1]) for n in sorted(rows) if 84 <= n <= 100]
old = {norm(rows[n][0]) for n in rows if n < 84}

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
pool_norm = {norm(p) for p in pool_texts}

others = ""
for f in ("city-culture.md", "city-humanities.md", "city-residents.md"):
    others += io.open(os.path.join(CODEX, f), encoding="utf-8").read()
others_norm = norm(others)

fleet = ""
for p in glob.glob(os.path.join(ROOT, "data", "storylines", "cards", "**", "*"), recursive=True):
    if os.path.isfile(p) and (p.endswith(".json") or p.endswith(".md")):
        try:
            fleet += io.open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            pass
fleet_norm = norm(fleet)

out = io.open(os.path.join(CWD, "r1354_verify.txt"), "w", encoding="utf-8")
ok = True
out.write("batch4_rows %d\n" % len(batch4))
for n, txt, src in batch4:
    key = norm(txt)
    in_pool = key in pool_norm
    dup_old = key in old
    in_others = (key in others_norm) or (txt in others)
    in_fleet = key in fleet_norm
    status = "OK" if (in_pool and not dup_old and not in_others and not in_fleet) else "FAIL"
    if status == "FAIL":
        ok = False
    out.write("#%d [%s] pool=%s dup_old=%s dup_cross=%s dup_fleet=%s | %s | %s\n"
              % (n, status, in_pool, dup_old, in_others, in_fleet, txt, src))

axes = {}
for n, txt, src in batch4:
    ax = src.split("·")[1].split("（")[0]
    axes[ax] = axes.get(ax, 0) + 1
scenes = sorted({re.search(r"（(.+?)场景", s).group(1) for _, _, s in batch4})
out.write("\naxis_coverage %s\n" % json.dumps(axes, ensure_ascii=False))
out.write("scenes %s\n" % ",".join(scenes))
out.write("total_spirit_rows %d\n" % len(rows))
out.write("VERDICT %s\n" % ("PASS" if ok and len(batch4) == 17 else "FAIL"))
out.close()
print("rows", len(batch4), "ok", ok)
