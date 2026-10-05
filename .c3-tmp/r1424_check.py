# -*- coding: utf-8 -*-
# R1424 waiting-idle fresh check + three probes (board/readiness/loop_health).
# Independent OUT hygiene law (R1311): all output to UTF-8 files, zero console reliance.
import io, json, os, re, subprocess, sys, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP  = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT  = io.open(os.path.join(ROOT, ".c3-tmp", "r1424_check.txt"), "w", encoding="utf-8")

def w(s):
    OUT.write(s + "\n")

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
w("CHECK_TS " + now)

# 1) orders top
od = os.path.join(ROOT, "orders")
files = sorted(os.listdir(od), key=lambda f: os.path.getmtime(os.path.join(od, f)), reverse=True)
w("ORDERS_TOP %s mtime %s" % (files[0], datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(od, files[0]))).strftime("%Y-%m-%d %H:%M:%S")))

# 2) ledger strict @ scan (five modes, strict @ prefix)
ledger = os.path.join(GRP, "cph4", "evolution-ledger.md")
txt = io.open(ledger, encoding="utf-8").read()
pat = re.compile(r"@(BigStream|七线全司|全司|六司)")
hits = 0
for line in txt.splitlines():
    if pat.search(line):
        hits += 1
w("LEDGER_HITS %d mtime %s" % (hits, datetime.datetime.fromtimestamp(os.path.getmtime(ledger)).strftime("%Y-%m-%d %H:%M:%S")))

# 3) decisions dnum content-addressed diff vs watermark
dec = os.path.join(GRP, "docs", "decisions.md")
dtxt = io.open(dec, encoding="utf-8").read()
cur = set(re.findall(r"[DC]-\d{8}-\d{2}", dtxt))
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
wm = set(st["decisions_watermark"]["dnums"])
new = sorted(cur - wm)
gone = sorted(wm - cur)
w("DECISIONS cur=%d wm=%d NEW=%s GONE=%s mtime=%s" % (len(cur), len(wm), new, gone, datetime.datetime.fromtimestamp(os.path.getmtime(dec)).strftime("%Y-%m-%d %H:%M:%S")))

# 4) backlog top lines
bl = io.open(os.path.join(ROOT, "src", "os", "backlog.md"), encoding="utf-8").read().splitlines()
for i, line in enumerate(bl[:12]):
    if line.strip():
        w("BL%d %s" % (i, line[:160]))

# 5) daily 10-06 existence (R1420 produced; no-rescan law applies, existence proof only)
w("DAILY_1006 %s" % os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-10-06.md")))

# 6) OH-20261008 (OSS w5 gate, opens 10-08 21:40)
w("OH_20261008 %s" % os.path.exists(os.path.join(GRP, "cph4", "OH-20261008-bigstream.md")))

# 7) export freshness
ex = json.load(io.open(os.path.join(ROOT, "docs", "status-export.json"), encoding="utf-8"))
w("EXPORT_TS %s" % ex.get("export_ts"))

# 8) production field
w("PRODUCTION %s" % st.get("production"))

# probes (run all three, no skipping)
probes = [
    ("board", [sys.executable, os.path.join(ROOT, "src", "board_check.py")]),
    ("readiness", [sys.executable, os.path.join(ROOT, "src", "readiness.py")]),
    ("loop_health", [sys.executable, os.path.join(ROOT, "src", "os", "loop_health.py")]),
]
for name, cmd in probes:
    p = subprocess.run(cmd, capture_output=True, cwd=ROOT, timeout=600)
    out = (p.stdout or b"").decode("utf-8", "replace")
    io.open(os.path.join(ROOT, ".c3-tmp", "r1424_probe_%s.txt" % name), "w", encoding="utf-8").write(out)
    lines = out.splitlines()
    tail = lines[-10:] if len(lines) > 10 else lines
    w("== %s rc=%d ==" % (name, p.returncode))
    for t in tail:
        w(t[:220])
OUT.close()
print("OK")
