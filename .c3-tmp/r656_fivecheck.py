# -*- coding: utf-8 -*-
"""R656 five-check probe (idle-fast path). Replicates R655 format law, baseline r644_lednew5.txt. ASCII-safe console output."""
import io, os, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []

def p(label, obj):
    OUT.append(label + ": " + str(obj))

p("NOW", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# 1. git log recent (bm-a codex batch closed by a commit?)
r = subprocess.run(["git", "log", "--oneline", "-6"], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
p("GIT_LOG_6", r.stdout.strip().replace("\n", " | "))

# 2. staged stat (codex files)
r = subprocess.run(["git", "diff", "--cached", "--stat"], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
p("CACHED_STAT", r.stdout.strip().replace("\n", " | "))

# 3. worktree diff stat for codex files
r = subprocess.run(["git", "diff", "--stat", "--", "data/storylines/codex/"], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
p("WORKTREE_CODEX_DIFF", r.stdout.strip().replace("\n", " | "))

# 4. codex mtimes
for f in ["README.md", "city-humanities.md"]:
    fp = os.path.join(ROOT, "data", "storylines", "codex", f)
    if os.path.exists(fp):
        mt = datetime.datetime.fromtimestamp(os.path.getmtime(fp)).strftime("%Y-%m-%d %H:%M:%S")
        p("MTIME_" + f, mt)

# 5. orders top file + edited-since-anchor check
orders_dir = os.path.join(ROOT, "orders")
files = [(f, os.path.getmtime(os.path.join(orders_dir, f))) for f in os.listdir(orders_dir) if f.endswith(".md")]
files.sort(key=lambda x: -x[1])
p("ORDERS_COUNT", len(files))
p("ORDERS_TOP", files[0][0] + " " + datetime.datetime.fromtimestamp(files[0][1]).strftime("%Y-%m-%d %H:%M:%S"))
p("ORDERS_EDITED_SINCE_ANCHOR", len([x for x in files if datetime.datetime.fromtimestamp(x[1]) > datetime.datetime(2026, 9, 28, 19, 12, 40)]))

# 6. ledger five-mode scan rowdiff vs baseline
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
BASE = os.path.join(ROOT, ".c3-tmp", "r644_lednew5.txt")
p("LEDGER_MTIME", datetime.datetime.fromtimestamp(os.path.getmtime(LEDGER)).strftime("%Y-%m-%d %H:%M:%S") if os.path.exists(LEDGER) else "MISSING")

def ledger_matches():
    pats = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线"]
    rows = set()
    with io.open(LEDGER, "r", encoding="utf-8", errors="replace") as fh:
        for i, line in enumerate(fh, 1):
            for pat in pats:
                if pat in line:
                    rows.add((i, line.rstrip("\n")))
                    break
    return rows

rows = ledger_matches()
p("LEDGER_MATCH_ROWS", len(rows))
if os.path.exists(BASE):
    base_rows = set()
    with io.open(BASE, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            num, txt = line.split("\t", 1)
            base_rows.add((int(num[1:]), txt))
    new = sorted(rows - base_rows)
    gone = sorted(base_rows - rows)
    p("ROWDIFF_NEW", len(new))
    for n, t in new[:5]:
        p("  NEW_L" + str(n), t[:160])
    p("ROWDIFF_GONE", len(gone))
    for n, t in gone[:5]:
        p("  GONE_L" + str(n), t[:160])
else:
    p("BASELINE", "MISSING")

# 7. decisions.md non-empty line count
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
if os.path.exists(DEC):
    p("DECISIONS_MTIME", datetime.datetime.fromtimestamp(os.path.getmtime(DEC)).strftime("%Y-%m-%d %H:%M:%S"))
    cnt = 0
    with io.open(DEC, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.strip():
                cnt += 1
    p("DECISIONS_NONEMPTY", cnt)

# 8. index.lock
p("INDEX_LOCK", os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 9. backlog mtime
BL = os.path.join(ROOT, "src", "os", "backlog.md")
p("BACKLOG_MTIME", datetime.datetime.fromtimestamp(os.path.getmtime(BL)).strftime("%Y-%m-%d %H:%M:%S"))

# 10. state.json machine fields (production / tick / ts)
import json
with io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8") as fh:
    st = json.load(fh)
p("STATE_PRODUCTION", st.get("production"))
p("STATE_TICK", st.get("tick"))
p("STATE_TS", st.get("ts"))

# 11. BigLife census anchors pool (#63/#86 supply gate): count + C-00030 existence
ANCH = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
if os.path.isdir(ANCH):
    anchor_files = [f for f in os.listdir(ANCH) if f.startswith("C-") and f.endswith(".md")]
    anchor_files.sort()
    p("ANCHORS_COUNT", len(anchor_files))
    p("ANCHORS_TAIL", anchor_files[-1] if anchor_files else "NONE")
    p("ANCHORS_C00030", os.path.exists(os.path.join(ANCH, "C-00030.md")))
    p("ANCHORS_MTIME_TOP", datetime.datetime.fromtimestamp(max(os.path.getmtime(os.path.join(ANCH, f)) for f in anchor_files)).strftime("%Y-%m-%d %H:%M:%S") if anchor_files else "NONE")
else:
    p("ANCHORS_DIR", "MISSING " + ANCH)

# 12. untracked families quick census (bm-a signs check)
r = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
lines = [l for l in r.stdout.splitlines() if l.strip()]
mod = [l for l in lines if l[:2] in ("M ", " M", "MM")]
unt = [l for l in lines if l.startswith("??")]
p("GIT_MODIFIED_N", len(mod))
for l in mod:
    p("  MOD", l[:160])
fams = {}
for l in unt:
    seg = l[3:].strip().split("/")[0] if "/" in l[3:] else l[3:].strip()
    fams[seg] = fams.get(seg, 0) + 1
p("UNTRACKED_N", len(unt))
p("UNTRACKED_FAMS", " | ".join(k + "=" + str(v) for k, v in sorted(fams.items())))

with io.open(os.path.join(ROOT, ".c3-tmp", "r656_fivecheck.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(OUT))
print("PROBE_OK lines=" + str(len(OUT)))
