# -*- coding: utf-8 -*-
"""R633 five-check probe script (fast-path five checks + three probes)."""
import io, os, subprocess, sys, re, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CWD = os.path.dirname(os.path.abspath(__file__))
LED = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
OUT = io.open(os.path.join(CWD, "r633_all.txt"), "w", encoding="utf-8")

def w(*a):
    OUT.write(" ".join(str(x) for x in a) + "\n")

# 1) orders check
orders_dir = os.path.join(ROOT, "orders")
ofiles = sorted(os.listdir(orders_dir))
o1928 = [f for f in ofiles if f.startswith("O-20260928")]
w("ORDERS_TOTAL", len(ofiles))
w("ORDERS_0928", len(o1928), sorted(o1928))
anchor = "O-20260927-1050-HQ-C.md"
for f in sorted(o1928):
    w("NEW_ORDER_FILE", f, datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(orders_dir, f))).strftime("%m-%d %H:%M:%S"))

# 2) ledger scan: strict @ prefix, five modes
led_lines = io.open(LED, encoding="utf-8").read().splitlines()
pats = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线"]
rows = []
for i, l in enumerate(led_lines):
    hit = [p for p in pats if p in l]
    if hit:
        rows.append((i + 1, l.strip()))
w("LEDGER_ROWS", len(rows))
for i, l in rows:
    w("LED_ROW", i, l[:160])
# line-level diff vs baseline r632_lednew5.txt
base_file = os.path.join(CWD, "r632_lednew5.txt")
if os.path.exists(base_file):
    base = set(io.open(base_file, encoding="utf-8").read().splitlines())
    cur = set(l for _, l in rows)
    w("LED_NEW", len(cur - base))
    for l in sorted(cur - base):
        w("LED_NEW_LINE", l[:200])
    w("LED_GONE", len(base - cur))
else:
    w("BASELINE_MISSING")

# 3) decisions non-empty count (UTF8)
dec = [l for l in io.open(DEC, encoding="utf-8") if l.strip()]
w("DEC_NONEMPTY", len(dec))
w("DEC_MTIME", datetime.datetime.fromtimestamp(os.path.getmtime(DEC)).strftime("%m-%d %H:%M:%S"))
# last 3 decision ids
for l in dec[-6:]:
    w("DEC_TAIL", l.strip()[:150])

# 4) state check
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
w("STATE_PRODUCTION", st.get("production"), "TICK", st.get("tick"))

# 5) git status quick
r = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
mod = [l for l in r.stdout.splitlines() if l and not l.startswith("??")]
unt = [l for l in r.stdout.splitlines() if l.startswith("??")]
w("GIT_MODIFIED", len(mod))
for l in mod[:10]:
    w("GIT_M", l)
w("GIT_UNTRACKED", len(unt))
fams = {}
for l in unt:
    p = l[3:].strip().split("/")[0]
    fams[p] = fams.get(p, 0) + 1
w("UNTRACKED_FAMILIES", json.dumps(fams, ensure_ascii=False))
w("INDEX_LOCK", os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# three probes
def run(label, args):
    rr = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    w("PROBE", label, "RC", rr.returncode)
    tail = (rr.stdout or "").strip().splitlines()[-8:]
    for t in tail:
        w("  ", t[:200])
    if rr.returncode != 0 and rr.stderr:
        for t in rr.stderr.strip().splitlines()[-4:]:
            w("  ERR", t[:200])

run("board", ["src/board_check.py"])
run("readiness", ["src/readiness.py"])
run("loop_health", ["src/os/loop_health.py"])

# 6) daily brief existence
w("DAILY_0928", os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-28.md")))
# 7) backlog mtime
w("BACKLOG_MTIME", datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(ROOT, "src", "os", "backlog.md"))).strftime("%m-%d %H:%M:%S"))
OUT.close()
print("OK r633_all done")
