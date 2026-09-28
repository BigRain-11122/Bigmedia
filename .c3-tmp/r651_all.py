# -*- coding: utf-8 -*-
"""R651 five-check probe (content-addressed anchors, no full rereads)."""
import io, os, re, subprocess, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
DECISIONS = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
OUT = []

def p(s):
    OUT.append(s)

def mt(f):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %H:%M:%S")
    except OSError:
        return "MISSING"

# 1) state
with io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = f.read()
prod = re.search(r'"production":\s*"([^"]+)"', st).group(1)
tick = re.search(r'"tick":\s*(\d+)', st).group(1)
p("STATE_PRODUCTION=%s TICK=%s" % (prod, tick))

# 2) orders: count + anchor mtime + edited/new since anchor
orders_dir = os.path.join(ROOT, "orders")
ofiles = [x for x in os.listdir(orders_dir) if x.startswith("O-")]
anchor = os.path.join(orders_dir, "O-20260928-1910-bm-a.md")
recent = []
for x in ofiles:
    fp = os.path.join(orders_dir, x)
    m = os.path.getmtime(fp)
    if m > os.path.getmtime(anchor):
        recent.append(x)
p("ORDERS_COUNT=%d ANCHOR_MTIME=%s" % (len(ofiles), mt(anchor)))
p("ORDERS_RECENT_SINCE_ANCHOR=%s" % (sorted(recent) if recent else "NONE"))

# 3) ledger six-unique (CaseSensitive)
modes = re.compile(r"@(BigStream|七线全司|全司|六司|八线)")
uniq = set()
cur_rows = []
total_lines = 0
with io.open(LEDGER, encoding="utf-8", errors="replace") as f:
    for i, line in enumerate(f, 1):
        total_lines += 1
        if modes.search(line):
            uniq.add(i)
            cur_rows.append("L%d\t%s" % (i, line.rstrip("\n")))
p("LEDGER_MTIME=%s TOTAL_LINES=%d SIX_UNIQUE_LINES=%d" % (mt(LEDGER), total_lines, len(uniq)))
p("LEDGER_ANCHOR_EXPECT=34 VERDICT=%s" % ("ANCHOR_OK" if len(uniq) == 34 else "BROKEN-ANCHOR"))

# 3b) rowdiff vs r644 baseline (L<num>\tab format law, R644)
base = os.path.join(ROOT, ".c3-tmp", "r644_lednew5.txt")
with io.open(base, encoding="utf-8", errors="replace") as f:
    base_rows = [l.rstrip("\n") for l in f if l.strip()]
cur_set = set(cur_rows)
base_set = set(base_rows)
new_rows = sorted(cur_set - base_set, key=lambda x: int(x.split("\t")[0][1:]))
gone_rows = sorted(base_set - cur_set, key=lambda x: int(x.split("\t")[0][1:]))
p("ROWDIFF_BASE=%s BASE_ROWS=%d CUR_ROWS=%d NEW=%d GONE=%d" % (os.path.basename(base), len(base_rows), len(cur_rows), len(new_rows), len(gone_rows)))
for r in new_rows[:5]:
    p("NEW_ROW=%s" % r[:400])
for r in gone_rows[:5]:
    p("GONE_ROW=%s" % r[:400])

# 4) decisions UTF8 non-empty lines
cnt = 0
with io.open(DECISIONS, encoding="utf-8", errors="replace") as f:
    for line in f:
        if line.strip():
            cnt += 1
p("DECISIONS_NONEMPTY=%d MTIME=%s" % (cnt, mt(DECISIONS)))
p("DECISIONS_ANCHOR_EXPECT=68 VERDICT=%s" % ("ANCHOR_OK" if cnt == 68 else "BROKEN-ANCHOR"))

# 5) tree state
try:
    os.remove(os.path.join(ROOT, ".git", "index.lock"))
    p("INDEX_LOCK=present-removed")
except OSError:
    p("INDEX_LOCK=False")
gs = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
mod = [l for l in gs if l.startswith("M ") or l.startswith(" M")]
unt = [l for l in gs if l.startswith("??")]
p("GIT_MODIFIED=%d UNTRACKED=%d" % (len(mod), len(unt)))
for l in mod:
    p("MODIFIED_FILE=%s mtime=%s" % (l, mt(os.path.join(ROOT, l[3:].strip()))))
fams = {}
for l in unt:
    name = l[3:].strip()
    key = name.split("/")[0] if "/" in name else "(root)"
    fams[key] = fams.get(key, 0) + 1
p("UNTRACKED_FAMILIES=%s" % dict(sorted(fams.items())))

# 5b) codex zone detail (bm-a active-write evidence)
for name in ("data/storylines/codex/README.md", "data/storylines/codex/city-humanities.md", "data/storylines/codex/city-spirit.md"):
    fp = os.path.join(ROOT, *name.split("/"))
    p("CODEX_MTIME %s = %s" % (name, mt(fp)))

# 6) routine anchors
daily = os.path.join(ROOT, "data", "intel", "daily", "2026-09-29.md")
p("DAILY_0929=%s" % os.path.exists(daily))
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
p("GLOBAL_BENCH_MTIME=%s (<=7d skip, next 10-01 #80)" % mt(gb))
w40 = os.path.join(ROOT, "docs", "audits", "2026-W40-self-audit.md")
p("W40_AUDIT=%s" % os.path.exists(w40))

with io.open(os.path.join(ROOT, ".c3-tmp", "r651_all.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("WROTE r651_all.txt lines=%d" % len(OUT))
