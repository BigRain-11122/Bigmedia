import os, re, json, glob, subprocess, time, datetime

BASE = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(BASE, ".c3-tmp", "r683_check.txt")
L = []

def add(s):
    L.append(str(s))

# --- git ---
try:
    r = subprocess.run(["git", "status", "--short"], cwd=BASE, capture_output=True, timeout=30)
    txt = r.stdout.decode("utf-8", errors="replace").strip()
    add("=== GIT STATUS ===")
    add(txt if txt else "(clean)")
    r = subprocess.run(["git", "status", "-sb"], cwd=BASE, capture_output=True, timeout=30)
    add(r.stdout.decode("utf-8", errors="replace").splitlines()[0][:100])
    r = subprocess.run(["git", "log", "-1", "--format=%h %ad %s", "--date=iso"], cwd=BASE, capture_output=True, timeout=30)
    add("HEAD: " + r.stdout.decode("utf-8", errors="replace").strip()[:160])
except Exception as e:
    add("git error: %r" % e)
add("index.lock: %s" % os.path.exists(os.path.join(BASE, ".git", "index.lock")))

# --- orders latest ---
od = os.path.join(BASE, "orders")
fs = []
for f in os.listdir(od):
    p = os.path.join(od, f)
    if os.path.isfile(p):
        fs.append((os.path.getmtime(p), f))
fs.sort(reverse=True)
add("=== ORDERS latest 5 (mtime | name) ===")
for mt, f in fs[:5]:
    add("%s | %s" % (time.strftime("%Y-%m-%d %H:%M", time.localtime(mt)), f))

# --- ledger scan (strict @ prefixes) ---
ledger = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
pat = re.compile(r"@(BigStream|八线全量|七线全司|全司|六司)")
cnt = 0
lastn = None
with open(ledger, encoding="utf-8") as f:
    for i, ln in enumerate(f, 1):
        if pat.search(ln):
            cnt += 1
            lastn = (i, ln.strip())
add("=== LEDGER strict @-lines: %d ===" % cnt)
if lastn:
    add("last L%d: %s" % (lastn[0], lastn[1][:150]))

# --- decisions count ---
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
with open(dec, encoding="utf-8") as f:
    dl = f.read().splitlines()
ne = sum(1 for x in dl if x.strip())
add("=== DECISIONS non-empty lines: %d ===" % ne)
lastd = ""
for x in dl:
    if x.strip():
        lastd = x.strip()
add("last: %s" % lastd[:150])

# --- state.json ---
with open(os.path.join(BASE, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
add("=== STATE ===")
add("tick=%s ts=%s production=%s" % (st.get("tick"), st.get("ts"), st.get("production")))
add("task=%s" % str(st.get("task"))[:150])
logs = st.get("log", [])
add("log entries: %d" % len(logs))
add("=== LAST 5 LOG LINES (800 chars each) ===")
for ln in logs[-5:]:
    add(ln[:800])
    add("----")

# --- routine files ---
db = os.path.join(BASE, "data", "intel", "daily", "2026-09-29.md")
add("daily brief 09-29 exists: %s" % os.path.exists(db))
today = datetime.date(2026, 9, 29)
add("ISO week today: %s" % today.isocalendar()[1])
for wk in (39, 40):
    p = os.path.join(BASE, "docs", "audits", "2026-W%d-self-audit.md" % wk)
    add("audit W%d exists: %s" % (wk, os.path.exists(p)))
res = glob.glob(os.path.join(BASE, "docs", "research", "*月度统计*"))
add("monthly stat notes: %s" % [os.path.basename(x) for x in res])
se = os.path.join(BASE, "docs", "status-export.json")
try:
    with open(se, encoding="utf-8") as f:
        sx = json.load(f)
    add("status-export export_ts: %s" % sx.get("export_ts"))
except Exception as e:
    add("status-export error: %r" % e)

# global benchmarks last update line
gb = os.path.join(BASE, "docs", "global-benchmarks.md")
with open(gb, encoding="utf-8") as f:
    g = f.read().splitlines()
idx = next((i for i, x in enumerate(g) if "更新记录" in x), None)
if idx is not None:
    add("GB-update head: %s" % g[idx][:90])
    if idx + 1 < len(g):
        add("GB-update next: %s" % g[idx + 1][:90])

# CENSUS anchor C-00030
anchor = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md"
add("CENSUS C-00030 anchor exists: %s" % os.path.exists(anchor))
if os.path.exists(anchor):
    add("  anchor mtime: %s" % time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(anchor))))

# recent e4/s1 result files (48h)
add("=== recent result json (48h) ===")
cutoff = time.time() - 48 * 3600
hits = []
for root, dirs, files in os.walk(BASE):
    if ".git" in root:
        continue
    for fn in files:
        if ("e4-result" in fn or "s1-result" in fn) and fn.endswith(".json"):
            p = os.path.join(root, fn)
            mt = os.path.getmtime(p)
            if mt > cutoff:
                hits.append((time.strftime("%m-%d %H:%M", time.localtime(mt)), os.path.relpath(p, BASE)))
for h in sorted(hits):
    add(h)

# python / ollama processes
try:
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"], capture_output=True, timeout=30)
    add("=== python.exe procs ===")
    add(r.stdout.decode("utf-8", errors="replace").strip()[:1200])
except Exception as e:
    add("tasklist error: %r" % e)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print("OK")
