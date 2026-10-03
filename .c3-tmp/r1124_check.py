# R1124 declared-idle light five-check + three probes (pattern: r1114-r1123)
import json, re, os, io, datetime, subprocess

root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
hq = r"C:\Users\sjs20\Desktop\FluxGroup"
T = os.path.join(root, ".c3-tmp")
TAG = "r1124"
OUT = []

def rd(p):
    with io.open(p, encoding="utf-8", errors="replace") as f:
        return f.read()

def mt(p):
    return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M:%S")

# --- light five-check ---
st = json.loads(rd(os.path.join(root, "src", "os", "state.json")))
OUT.append("tick=%s ts=%s production=%s" % (st.get("tick"), st.get("ts"), st.get("production")))
logs = st.get("log") or []
OUT.append("last log head: %s" % logs[-1][:120])

odir = os.path.join(root, "orders")
files = sorted((os.path.getmtime(os.path.join(odir, f)), f) for f in os.listdir(odir) if not f.startswith("."))
OUT.append("orders top: %s (%s)" % (files[-1][1], mt(os.path.join(odir, files[-1][1]))))

go = os.path.join(hq, "docs", "orders.md")
OUT.append("group orders.md mtime: %s lines=%d" % (mt(go), len(rd(go).splitlines())))

wm = st.get("decisions_watermark") or {}
dn = wm.get("dnums") or []
dp = os.path.join(hq, "docs", "decisions.md")
dc = rd(dp)
fset = set(re.findall(r"[DC]-\d{8}-\d{2}", dc))
OUT.append("decisions mtime=%s file=%d wm=%d NEW=%s" % (mt(dp), len(fset), len(set(dn)), sorted(fset - set(dn))[:10]))

lp = os.path.join(hq, "cph4", "evolution-ledger.md")
ll = rd(lp).splitlines()
bs = [(i, l) for i, l in enumerate(ll, 1) if re.search(r"@BigStream|@八线|@七线全司|@全司|@六司", l)]
OUT.append("ledger mtime=%s lines=%d target-hits=%d last-tag-L%d" % (mt(lp), len(ll), len(bs), bs[-1][0] if bs else 0))
tailtags = [l[:90] for l in ll if re.search(r"@BigStream|@八线|@七线全司|@全司|@六司", l)][-4:]
OUT.append("ledger last-tag tail: %s" % " || ".join(tailtags))

OUT.append("index.lock: %s" % os.path.exists(os.path.join(root, ".git", "index.lock")))

se = json.loads(rd(os.path.join(root, "docs", "status-export.json")))
age = (datetime.datetime.now() - datetime.datetime.strptime(se.get("export_ts", "2000-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600
OUT.append("export_ts=%s age=%.1fh (<24h gate)" % (se.get("export_ts"), age))

OUT.append("daily 10-03: %s | 10-04: %s | W40 audit: %s" % (
    os.path.exists(os.path.join(root, "data", "intel", "daily", "2026-10-03.md")),
    os.path.exists(os.path.join(root, "data", "intel", "daily", "2026-10-04.md")),
    os.path.exists(os.path.join(root, "docs", "audits", "2026-W40-self-audit.md"))))

# #86 three legs supply-gate evidence
po = os.path.join(hq, "life", "BigLife", "cognition", "pools.json")
if os.path.exists(po):
    pj = json.loads(rd(po))
    def cnt(x):
        n = 0
        if isinstance(x, dict):
            for v in x.values():
                n += cnt(v)
            return n
        return 1 if isinstance(x, str) else (len(x) if isinstance(x, list) else 1)
    OUT.append("#86 a pools count=%d (mtime %s)" % (cnt(pj), mt(po)))
ic = os.path.join(hq, "life", "BigLife", "cognition", "interchat-ledger.jsonl")
if os.path.exists(ic):
    OUT.append("#86 c interchat rows=%d" % len([l for l in rd(ic).splitlines() if l.strip()]))
an = os.path.join(hq, "life", "BigLife", "census", "anchors")
if os.path.isdir(an):
    OUT.append("#86 anchors tail=%s C-00030:%s" % (sorted(os.listdir(an))[-2:], os.path.exists(os.path.join(an, "C-00030.md"))))

for p in ("src/os/backlog.md", "docs/self-improvement-queue.md"):
    OUT.append("%s mtime=%s" % (p, mt(os.path.join(root, p))))

with io.open(os.path.join(T, TAG + "_check.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("CHECK OK")

# --- three probes (run fresh, never skip) ---
def run(cmd):
    r = subprocess.run(["python"] + cmd, cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout + r.stderr

board = run(["src/board_check.py"])
open(os.path.join(T, TAG + "_board.txt"), "w", encoding="utf-8").write(board)
rdy = run(["src/readiness.py"])
open(os.path.join(T, TAG + "_rd.txt"), "w", encoding="utf-8").write(rdy)
loop = run(["src/os/loop_health.py"])
open(os.path.join(T, TAG + "_loop.txt"), "w", encoding="utf-8").write(loop)

l_fail = [l for l in loop.splitlines() if "[FAIL]" in l]
l_warn = [l for l in loop.splitlines() if "[WARN]" in l]
summ = []
summ.append("board FAIL lines: %d" % len([l for l in board.splitlines() if "FAIL" in l]))
summ.append("board summary: %s" % [l for l in board.splitlines() if "summary" in l.lower()][:2])
summ.append("readiness: %s" % [l for l in rdy.splitlines() if "readiness" in l.lower() or "blocker" in l.lower()][:6])
summ.append("loop FAIL=%d WARN=%d" % (len(l_fail), len(l_warn)))
for l in l_fail:
    summ.append("LOOPFAIL: " + l[:160])
with io.open(os.path.join(T, TAG + "_probes_summary.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(summ))
print("PROBES OK fails=%d warns=%d" % (len(l_fail), len(l_warn)))
