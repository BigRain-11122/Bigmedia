# r1308 quick-path probe: state/git/orders/group-scan/supply-gates -> UTF-8 file
import json, os, re, subprocess, glob, time

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
grp = r"C:\Users\sjs20\Desktop\FluxGroup"
L = []
add = L.append

# --- state.json ---
state = json.load(open(os.path.join(repo, "src", "os", "state.json"), encoding="utf-8"))
add("== STATE keys ==")
for k in state:
    if k == "log":
        continue
    s = json.dumps(state[k], ensure_ascii=False)
    add(f"{k} = {s[:500]}")
log = state.get("log", [])
add(f"log_len = {len(log)}")
for line in log[-3:]:
    add("LOG| " + line[:2200])
add("")

# --- git ---
r = subprocess.run(["git", "-C", repo, "status", "--short"], capture_output=True, text=True, encoding="utf-8", errors="replace")
add("== GIT STATUS == ")
add(r.stdout.strip()[:1800] or "(clean)")
r2 = subprocess.run(["git", "-C", repo, "log", "--oneline", "-4"], capture_output=True, text=True, encoding="utf-8", errors="replace")
add("== GIT LOG ==")
add(r2.stdout.strip()[:1000])
lock = os.path.join(repo, ".git", "index.lock")
add(f"index.lock exists={os.path.exists(lock)}")
add("")

# --- orders latest ---
od = os.path.join(repo, "orders")
files = sorted(glob.glob(os.path.join(od, "*")), key=os.path.getmtime, reverse=True)
add("== ORDERS latest ==")
for f in files[:4]:
    add(os.path.basename(f) + "  mtime=" + time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(f))))
add("")

# --- backlog open items (numbered lines without [done]) ---
bl = open(os.path.join(repo, "src", "os", "backlog.md"), encoding="utf-8").read().splitlines()
add(f"== BACKLOG total_lines={len(bl)} open items ==")
for i, l in enumerate(bl):
    m = re.match(r"^(\d+)\.\s", l)
    if m and "[done" not in l and "unsuspended-by" not in l:
        add(f"OPEN#{m.group(1)} L{i+1}: {l[:260]}")
add("")

# --- group ledger scan ---
lp = os.path.join(grp, "cph4", "evolution-ledger.md")
ll = open(lp, encoding="utf-8").read().splitlines()
add(f"== LEDGER lines={len(ll)} ==")
pat = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线")
hits = [(i + 1, l) for i, l in enumerate(ll) if pat.search(l)]
add(f"at_mentions={len(hits)}")
for i, l in hits[-8:]:
    add(f"L{i}| {l[:200]}")
prow = [(i + 1, l) for i, l in enumerate(ll) if re.search(r"P-2026-10-0[45]-\d+", l)]
add(f"p_rows_1004_1005={len(prow)}")
for i, l in prow[-8:]:
    add(f"P{i}| {l[:200]}")
add("")

# --- group decisions.md: dispatch board + dnum set diff ---
dtxt = open(os.path.join(grp, "docs", "decisions.md"), encoding="utf-8").read()
dnums = set(re.findall(r"[DC]-\d{8}-\d+", dtxt))
wm = state.get("decisions_watermark", {})
prev = set(wm.get("dnums", [])) if isinstance(wm, dict) else set()
add(f"== DECISIONS dnums={len(dnums)} new_vs_wm={sorted(dnums - prev)} ==")
dl = dtxt.splitlines()
add("-- decisions top 35 lines --")
for l in dl[:35]:
    if l.strip():
        add("DT| " + l[:200])
add("")

# --- group orders.md CEO physical items ---
otxt = open(os.path.join(grp, "docs", "orders.md"), encoding="utf-8").read().splitlines()
add(f"== GROUP ORDERS.md lines={len(otxt)} ==")
for i, l in enumerate(otxt):
    if re.search(r"账号|商户号|服务器", l) and i < 120:
        add(f"O{i+1}| {l[:180]}")
add("")

# --- supply gates / routine files ---
db = os.path.join(repo, "data", "intel", "daily", "2026-10-05.md")
add(f"daily_20261005_exists={os.path.exists(db)}")
a30 = os.path.join(grp, "life", "BigLife", "census", "anchors", "C-00030.md")
add(f"anchor_C00030_exists={os.path.exists(a30)}")
ad = os.path.join(grp, "life", "BigLife", "census", "anchors")
if os.path.isdir(ad):
    add(f"anchors_tail={sorted(os.listdir(ad))[-4:]}")
w40 = os.path.join(repo, "docs", "audits", "2026-W40-self-audit.md")
w41 = os.path.join(repo, "docs", "audits", "2026-W41-self-audit.md")
add(f"audit_W40={os.path.exists(w40)} audit_W41={os.path.exists(w41)}")
add("")

# --- recent tmp/e4 results (last 10h) ---
now = time.time()
add("== recent files mtime<10h ==")
cands = []
for d in glob.glob(os.path.join(repo, ".c3-tmp", "*")) + glob.glob(os.path.join(repo, ".*-tmp", "*")) + glob.glob(os.path.join(repo, "r13*.txt")) + glob.glob(os.path.join(repo, "r13*.py")):
    try:
        mt = os.path.getmtime(d)
    except OSError:
        continue
    if now - mt < 10 * 3600:
        cands.append((mt, os.path.relpath(d, repo)))
for mt, rel in sorted(cands, reverse=True)[:20]:
    add(time.strftime("%m-%d %H:%M", time.localtime(mt)) + "  " + rel)
add("")

# --- current time ---
add("now=" + time.strftime("%Y-%m-%d %H:%M:%S"))

out = os.path.join(repo, ".c3-tmp", "r1308_probe.txt")
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w", encoding="utf-8").write("\n".join(L))
print("probe done lines=", len(L))
