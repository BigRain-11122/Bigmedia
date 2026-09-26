import os, re, subprocess, sys, time, io
from datetime import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
os.chdir(ROOT)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

def ex(p):
    return os.path.exists(p)

# 1 supply gate: census anchors canonical position only (R316 discipline)
ADIR = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
c30 = ex(os.path.join(ADIR, "C-00030.md"))
c31 = ex(os.path.join(ADIR, "C-00031.md"))
names = sorted(f for f in os.listdir(ADIR) if f.endswith(".md"))
print("anchors: C-00030=%s C-00031=%s count=%d tail=%s" % (c30, c31, len(names), names[-2:]))

# 2 lock
print("index.lock:", ex(os.path.join(ROOT, ".git", "index.lock")))

# 3 ledger four-mode count (line-contains token, R327 discipline)
modes = ["@BigStream", "@\u4e03\u7ebf\u5168\u53f8", "@\u5168\u53f8", "@\u516d\u53f8"]
LED = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
cnt = 0
with open(LED, encoding="utf-8", errors="replace") as f:
    for line in f:
        if any(m in line for m in modes):
            cnt += 1
print("ledger four-mode lines:", cnt)

# 4 decisions non-empty lines + tail decision id (python utf-8, ASCII digest)
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
n = 0
last = ""
with open(DEC, encoding="utf-8", errors="replace") as f:
    for line in f:
        if line.strip():
            n += 1
            last = line.strip()
ids = re.findall(r"D-\d{8}-\d+", last)
print("decisions non-empty:", n, "tail-id:", ids[-1] if ids else "none")

# 5 storylines new writes since 2026-09-26 00:00 (ch.5 v3 / ch.6 landing check)
th = time.mktime(time.strptime("2026-09-26 00:00:00", "%Y-%m-%d %H:%M:%S"))
hits = []
base = os.path.join(ROOT, "data", "storylines")
for sub in ("novel", "audio", "comic"):
    for dp, dn, fn in os.walk(os.path.join(base, sub)):
        for f in fn:
            p = os.path.join(dp, f)
            try:
                if os.path.getmtime(p) >= th:
                    hits.append(os.path.relpath(p, base))
            except OSError:
                pass
print("storylines new since 00:00:", len(hits), sorted(hits)[:4])

# 6 routine files
print("daily 09-26:", ex(os.path.join(ROOT, "data", "intel", "daily", "2026-09-26.md")))
print("W39 audit:", ex(os.path.join(ROOT, "docs", "audits", "2026-W39-self-audit.md")))

# 7 probes
def run(label, args):
    r = subprocess.run([sys.executable] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    m = re.findall(r"(\d+)\s*FAIL\s*[^\n]*?(\d+)\s*WARN", out)
    fails = sum(int(a) for a, b in m)
    warns = sum(int(b) for a, b in m)
    print("%s: exit=%d FAIL=%d WARN=%d" % (label, r.returncode, fails, warns))
    tail = [l for l in out.splitlines() if l.strip()][-2:]
    for l in tail:
        try:
            print("   |", l.encode("ascii", "replace").decode("ascii")[:160])
        except Exception:
            print("   | <line>")

run("board", ["src/board_check.py"])
run("readiness", ["src/readiness.py"])
run("loop_health", ["src/os/loop_health.py"])
