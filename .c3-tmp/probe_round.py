import json, os, re, subprocess, glob, datetime

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
base = os.path.abspath(os.path.join(repo, "..", ".."))
out = []
A = out.append

# 1. state.json summary
with open(os.path.join(repo, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
A("=== STATE ===")
for k in ("production", "tick", "ts", "task"):
    v = st.get(k)
    if isinstance(v, str) and len(v) > 220:
        v = v[:220] + "..."
    A(f"{k}: {v}")
logs = st.get("log", [])
A(f"log_count: {len(logs)}")
for e in logs[-5:]:
    A("LOG| " + str(e)[:560])

# 2. orders latest
A("=== ORDERS (latest 6 by mtime) ===")
files = sorted(glob.glob(os.path.join(repo, "orders", "*")), key=os.path.getmtime, reverse=True)[:6]
for p in files:
    A(os.path.basename(p) + " | " + datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M"))

# 3. decisions + ledger
dc = os.path.join(base, "docs", "decisions.md")
with open(dc, encoding="utf-8") as f:
    dlines = f.readlines()
A(f"decisions_nonempty: {sum(1 for x in dlines if x.strip())}")

el = os.path.join(base, "cph4", "evolution-ledger.md")
with open(el, encoding="utf-8") as f:
    elines = f.readlines()
pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线)")
hits = [(i + 1, l) for i, l in enumerate(elines) if pat.search(l)]
A(f"ledger_atmention_total: {len(hits)}")
sep29 = [(i + 1, l) for i, l in enumerate(elines) if "2026-09-29" in l]
A(f"ledger_lines_dated_0929: {len(sep29)}")
for i, l in sep29[-8:]:
    A(f"  L{i}: " + l.strip()[:210])

# 4. git status
r = subprocess.run(["git", "-C", repo, "status", "--short"], capture_output=True, text=True)
A("=== GIT STATUS ===")
A(r.stdout.strip()[:1400] if r.stdout.strip() else "(clean)")
lock = os.path.join(repo, ".git", "index.lock")
A(f"index_lock: {os.path.exists(lock)}")

# 5. anchors (CENSUS supply gate)
ad = os.path.join(base, "life", "BigLife", "census", "anchors")
if os.path.isdir(ad):
    ids = sorted(os.listdir(ad))
    A(f"anchors_top: {ids[-3:] if ids else '(empty)'}")
else:
    A("anchors_dir_missing: " + ad)

# 6. daily brief today
dbf = os.path.join(repo, "data", "intel", "daily", "2026-09-29.md")
A(f"daily_brief_0929: {os.path.exists(dbf)}")

# 7. results recent (30h)
now = datetime.datetime.now().timestamp()
A("=== result json files recent 30h ===")
cnt = 0
for p in glob.glob(os.path.join(repo, "**", "*result*.json"), recursive=True):
    if ".git" in p:
        continue
    if os.path.getmtime(p) > now - 30 * 3600:
        cnt += 1
        A(p.replace(repo, ".") + " | " + datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M"))
A(f"recent_result_count: {cnt}")
evd = os.path.join(repo, "docs", "reviews", "expert-verdicts")
if os.path.isdir(evd):
    fs = sorted(glob.glob(os.path.join(evd, "*")), key=os.path.getmtime, reverse=True)[:4]
    for p in fs:
        A("verdict| " + os.path.basename(p) + " | " + datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M"))

# 8. backlog items 82+ and open top
with open(os.path.join(repo, "src", "os", "backlog.md"), encoding="utf-8") as f:
    blines = f.readlines()
hi = [l.strip()[:240] for l in blines if re.match(r"^(\d{2,3})\.\s", l) and int(re.match(r"^(\d{2,3})\.\s", l).group(1)) >= 82]
A(f"=== backlog items >=82: {len(hi)} ===")
for h in hi[:6]:
    A(h)
open_items = [l.strip()[:240] for l in blines if re.match(r"^\d+\.\s", l) and "[done" not in l]
A(f"=== open_items_count: {len(open_items)}; first 5: ===")
for h in open_items[:5]:
    A(h)

# 9. queue file: section E / D content head
qf = os.path.join(repo, "docs", "self-improvement-queue.md")
if os.path.exists(qf):
    with open(qf, encoding="utf-8") as f:
        q = f.read()
    A(f"=== queue_len: {len(q)} ===")
    m = re.search(r"#+\s*[§]?E[^\n]*", q)
    if m:
        A("queue_E_head: " + q[m.start():m.start() + 900].replace("\n", " || ")[:900])
# 10. audits / monthly note existence
A(f"w40_audit_exists: {os.path.exists(os.path.join(repo, 'docs', 'audits', '2026-W40-self-audit.md'))}")
mm = glob.glob(os.path.join(repo, "docs", "research", "*月度统计*"))
A(f"monthly_note: {[os.path.basename(x) for x in mm]}")

# 11. src probe names
A("=== src scripts ===")
A(", ".join(os.path.basename(x) for x in glob.glob(os.path.join(repo, "src", "os", "*.py"))))
A(", ".join(os.path.basename(x) for x in glob.glob(os.path.join(repo, "src", "*.py"))))

A("now: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

with open(os.path.join(repo, ".c3-tmp", "probe-round.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("WROTE", len(out), "lines")
