# -*- coding: utf-8 -*-
# R1428 batch-close round fresh check + three probes (board/readiness/loop_health).
# Independent OUT hygiene law (R1311): all output to UTF-8 files, zero console reliance.
import io, json, os, re, subprocess, sys, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP  = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT  = io.open(os.path.join(ROOT, ".c3-tmp", "r1428_check.txt"), "w", encoding="utf-8")

def w(s):
    OUT.write(s + "\n")

now = datetime.datetime.now()
w("CHECK_TS " + now.strftime("%Y-%m-%d %H:%M:%S"))

# 1) orders top
od = os.path.join(ROOT, "orders")
files = sorted(os.listdir(od), key=lambda f: os.path.getmtime(os.path.join(od, f)), reverse=True)
w("ORDERS_TOP %s mtime %s" % (files[0], datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(od, files[0]))).strftime("%Y-%m-%d %H:%M:%S")))

# 2) ledger strict @ scan (five modes, strict @ prefix)
ledger = os.path.join(GRP, "cph4", "evolution-ledger.md")
txt = io.open(ledger, encoding="utf-8").read()
pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线)")
hits = 0
for line in txt.splitlines():
    if pat.search(line):
        hits += 1
w("LEDGER_HITS %d mtime %s" % (hits, datetime.datetime.fromtimestamp(os.path.getmtime(ledger)).strftime("%Y-%m-%d %H:%M:%S")))
nonempty = [l for l in txt.splitlines() if l.strip()]
for t in nonempty[-2:]:
    w("LEDGER_TAIL " + t[:150])

# 3) decisions dnum content-addressed diff vs watermark
dec = os.path.join(GRP, "docs", "decisions.md")
dtxt = io.open(dec, encoding="utf-8").read()
cur = set(re.findall(r"[DC]-\d{8}-\d{2}", dtxt))
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
wm = set(st["decisions_watermark"]["dnums"])
new = sorted(cur - wm)
gone = sorted(wm - cur)
w("DECISIONS cur=%d wm=%d NEW=%s GONE=%s mtime=%s" % (len(cur), len(wm), new, gone, datetime.datetime.fromtimestamp(os.path.getmtime(dec)).strftime("%Y-%m-%d %H:%M:%S")))

# 4) dispatch board rows involving BigStream (light count only)
board = re.findall(r"^.*BigStream.*$", dtxt, re.M)
w("BOARD_BS_ROWS %d" % len(board))

# 5) daily 10-06 existence (R1420 produced; no-rescan law applies, existence proof only)
w("DAILY_1006 %s" % os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-10-06.md")))

# 6) OH-20261008 (OSS w5 gate, opens 10-08 21:40)
w("OH_20261008 %s" % os.path.exists(os.path.join(GRP, "cph4", "OH-20261008-bigstream.md")))

# 7) export freshness vs 24h gate
ex = json.load(io.open(os.path.join(ROOT, "docs", "status-export.json"), encoding="utf-8"))
ets = ex.get("export_ts")
try:
    age_h = (now - datetime.datetime.strptime(ets, "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600.0
except Exception:
    age_h = -1
w("EXPORT_TS %s AGE_H %.2f" % (ets, age_h))

# 8) production field + index.lock
w("PRODUCTION %s" % st.get("production"))
w("INDEX_LOCK %s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 9) state tick/ts snapshot (self-accounting expected-dirty state proof)
w("STATE_TICK %s STATE_TS %s" % (st.get("tick"), st.get("ts")))

# 10) backlog top 3 lines
bl = [l for l in io.open(os.path.join(ROOT, "src", "os", "backlog.md"), encoding="utf-8").read().splitlines() if l.strip()]
for t in bl[:3]:
    w("BACKLOG_TOP " + t[:160])

# 11) W41 self-audit existence (weekly gate)
w("AUDIT_W41 %s" % os.path.exists(os.path.join(ROOT, "docs", "audits", "2026-W41-self-audit.md")))

# probes (run all three, no skipping)
probes = [
    ("board", [sys.executable, os.path.join(ROOT, "src", "board_check.py")]),
    ("readiness", [sys.executable, os.path.join(ROOT, "src", "readiness.py")]),
    ("loop_health", [sys.executable, os.path.join(ROOT, "src", "os", "loop_health.py")]),
]
for name, cmd in probes:
    p = subprocess.run(cmd, capture_output=True, cwd=ROOT, timeout=600)
    out = (p.stdout or b"").decode("utf-8", "replace")
    io.open(os.path.join(ROOT, ".c3-tmp", "r1428_probe_%s.txt" % name), "w", encoding="utf-8").write(out)
    lines = out.splitlines()
    tail = lines[-10:] if len(lines) > 10 else lines
    w("== %s rc=%d ==" % (name, p.returncode))
    for t in tail:
        w(t[:220])
OUT.close()
print("OK")
