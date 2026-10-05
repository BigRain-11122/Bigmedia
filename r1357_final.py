# -*- coding: utf-8 -*-
# R1357 final four-exhaustive check: queue undone items, a-leg trigger (BigLife pools.json), proposal face
import os, re, glob, json, io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []
def w(s): out.append(str(s))

# 1. self-improvement queue undone rows
q = open(os.path.join(ROOT, "docs", "self-improvement-queue.md"), encoding="utf-8").read()
w("== queue rows NOT done (pool|# |item) ==")
for l in q.splitlines():
    if l.strip().startswith("|") and "[done" not in l and "状态" not in l and "---" not in l:
        if re.match(r"^\|\s*[A-D]\d", l.strip()):
            w("  " + l[:230])
w("== queue §D proposal face (last 12 lines of D section) ==")
idx = q.find("## D")
if idx >= 0:
    for l in q[idx:].splitlines()[-14:]:
        w("  | " + l[:230])
else:
    w("  (no ## D section found)")

# 2. a-leg trigger: pools.json path from r1353/r1354 pool scripts
for script in ("r1353_pool.py", "r1354_pool.py"):
    p = os.path.join(ROOT, script)
    if os.path.exists(p):
        t = open(p, encoding="utf-8").read()
        m = re.findall(r"[A-Za-z]:[^\"']*pools\.json", t)
        w("%s pools.json path refs: %s" % (script, m[:2]))
        m2 = re.findall(r"TOTAL_LINES[^\n]{0,80}", t)
        w("%s TOTAL_LINES refs: %s" % (script, m2[:3]))

# find pools.json under FluxGroup (BigLife repo)
hits = []
for base in (r"C:\Users\sjs20\Desktop\FluxGroup", ):
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "Library", "Temp", "__pycache__", "output", "renders", ".c3-tmp")]
        for f in filenames:
            if f == "pools.json":
                hits.append(os.path.join(dirpath, f))
w("== pools.json found: %d ==" % len(hits))
for h in hits[:5]:
    try:
        j = json.load(open(h, encoding="utf-8"))
        tl = j.get("TOTAL_LINES") or j.get("total_lines")
        w("  %s -> TOTAL_LINES=%s, keys=%s" % (h, tl, list(j.keys())[:8]))
    except Exception as e:
        w("  %s -> parse fail %r" % (h, e))

# 3. city-spirit.md tail (change log with pool baseline)
cs = open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
w("== city-spirit.md last 12 lines ==")
for l in cs.splitlines()[-12:]:
    w("  | " + l[:230])
m = re.findall(r"(?:总行|TOTAL|净候选|433|397)[^\n]{0,100}", cs)
w("pool-count mentions: %s" % m[:6])

open(os.path.join(ROOT, "r1357_final.txt"), "w", encoding="utf-8").write("\n".join(out))
print("OK")
