# -*- coding: utf-8 -*-
"""R654 five-check probe (idle-fast path). ASCII output only for console safety."""
import io, os, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []

def p(label, obj):
    OUT.append(label + ": " + str(obj))

# 0. now
p("NOW", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# 1. git log recent (is bm-a codex batch closed by a commit?)
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

# 5. orders top file
orders_dir = os.path.join(ROOT, "orders")
files = [(f, os.path.getmtime(os.path.join(orders_dir, f))) for f in os.listdir(orders_dir) if f.endswith(".md")]
files.sort(key=lambda x: -x[1])
p("ORDERS_COUNT", len(files))
p("ORDERS_TOP", files[0][0] + " " + datetime.datetime.fromtimestamp(files[0][1]).strftime("%Y-%m-%d %H:%M:%S"))

# 6. ledger five-mode scan: @BigStream/@七线全司/@全司/@六司/@八线 (CaseSensitive), rowdiff vs baseline
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
# rowdiff vs baseline (baseline format: "L<idx>\t<line>" per R644 format law)
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

# 7. decisions.md non-empty line count (UTF8)
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

# 9. backlog top lines (first ~40 lines)
BL = os.path.join(ROOT, "src", "os", "backlog.md")
with io.open(BL, "r", encoding="utf-8", errors="replace") as fh:
    lines = [l.rstrip("\n") for l in fh][:30]
p("BACKLOG_MTIME", datetime.datetime.fromtimestamp(os.path.getmtime(BL)).strftime("%Y-%m-%d %H:%M:%S"))
for l in lines[:14]:
    if l.strip():
        p("BL", l[:150])

# 10. anchors count (CENSUS anchor pool for #63 supply-gate check)
# search census anchors max C-000NN in data/storylines/codex? Prior rounds used an anchors count in card dirs.
# R619: ANCHORS_COUNT=20 tail=C-00029 via r619_all; find the source: likely data/cards/ or city census. Search minimal: count C-000xx in census anchor registry used earlier. We just glob for the census file used by prior probes.
import re
cands = []
for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "data")):
    for fn in filenames:
        if fn.endswith(".json") and "census" in fn.lower():
            cands.append(os.path.join(dirpath, fn))
p("CENSUS_JSON_CANDS", len(cands))
if cands:
    fp = sorted(cands)[-1]
    p("CENSUS_TOP", fp.replace(ROOT, "") + " " + datetime.datetime.fromtimestamp(os.path.getmtime(fp)).strftime("%m-%d %H:%M"))

with io.open(os.path.join(ROOT, ".c3-tmp", "r654_fivecheck.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(OUT))
print("PROBE_OK lines=" + str(len(OUT)))
