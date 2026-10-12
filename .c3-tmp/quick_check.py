# -*- coding: utf-8 -*-
# Quick round-start check: state tail, backlog top, orders, git status, watermark diff.
import json, os, re, subprocess, glob, io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, ".c3-tmp", "quick_check_out.txt")
lines = []

def log(s):
    lines.append(str(s))

# 1. state.json tail
with io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8") as f:
    st = json.load(f)
log("tick=%s ts=%s" % (st.get("tick"), st.get("ts")))
log("task=%s" % st.get("task", ""))
log("production=%s" % st.get("production"))
lg = st.get("log", [])
log("log_len=%d" % len(lg))
for x in lg[-3:]:
    log("LOGTAIL>> " + x[:600])
wm = st.get("decisions_watermark", {})
log("watermark_dnums_count=%s" % len(wm.get("dnums", [])))
log("watermark_last=%s" % json.dumps({k: wm.get(k) for k in list(wm.keys())[:6]}, ensure_ascii=False)[:400] if wm else "{}")

# 2. backlog top rows (first 2 non-done candidate rows)
with io.open(os.path.join(ROOT, "src", "os", "backlog.md"), "r", encoding="utf-8") as f:
    bl = f.read()
nondone = [l for l in bl.split("\n") if re.match(r"^\d+\.\s", l) and "[done" not in l][:3]
for i, l in enumerate(nondone):
    log("BACKLOG-TOP%d>> %s" % (i, l[:300]))

# 3. orders latest
orders_files = sorted(glob.glob(os.path.join(ROOT, "orders", "*")), key=os.path.getmtime)
log("orders_latest=%s mtime=%s" % (os.path.basename(orders_files[-1]) if orders_files else "NONE", os.path.getmtime(orders_files[-1]) if orders_files else 0))

# 4. git status
p = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
log("git_status rc=%s" % p.returncode)
gs = p.stdout.strip().split("\n") if p.stdout.strip() else []
log("git_status_lines=%d" % len(gs))
for l in gs[:15]:
    log("GIT>> " + l)
lock = os.path.join(ROOT, ".git", "index.lock")
log("index_lock=%s" % os.path.exists(lock))

# 5. ledger @BigStream count
ledger = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
new_at = []
if os.path.exists(ledger):
    with io.open(ledger, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    at_lines = [l for l in content.split("\n") if "@BigStream" in l or "@七线全司" in l or "@全司" in l or "@六司" in l]
    log("ledger_at_count=%d" % len(at_lines))
    for l in at_lines[-3:]:
        log("LEDGER-TAIL>> " + l[:250])
    # detect un-executed lines
    for l in at_lines:
        if ("未回执行" in l) or ("dispatched" in l and "executed" not in l):
            new_at.append(l[:250])
    log("ledger_unexec=%d" % len(new_at))
    for l in new_at[:3]:
        log("LEDGER-NEW>> " + l)

# 6. decisions.md watermark diff (content-addressed)
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
if os.path.exists(dec):
    with io.open(dec, "r", encoding="utf-8", errors="replace") as f:
        dc = f.read()
    cur = set(re.findall(r"[DC]-\d{8}-\d{2}", dc))
    old = set(wm.get("dnums", []))
    diff = sorted(cur - old)
    log("decisions_total=%d watermark=%d new=%d" % (len(cur), len(old), len(diff)))
    for d in diff[:10]:
        log("DECISION-NEW>> %s" % d)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("OK lines=%d" % len(lines))
