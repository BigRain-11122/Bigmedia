r"""Quick-check probe for round start (fast judgment path). ASCII code only; output to UTF-8 data file."""
import json, os, re, subprocess, glob

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
OUTP = os.path.join(ROOT, ".c3-tmp", "r1180_quick.txt")
out = []
def w(s):
    out.append(str(s))

# 1. state.json essentials
with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
w("tick=%s" % st.get("tick"))
w("ts=%s" % st.get("ts"))
w("task=%s" % str(st.get("task"))[:150])
w("production=%s" % st.get("production"))
dw = st.get("decisions_watermark", {})
dnums = set(dw.get("dnums", [])) if isinstance(dw, dict) else set()
w("dnums_count=%d last5=%s" % (len(dnums), ",".join(sorted(dnums)[-5:]) if dnums else "NONE"))
log = st.get("log", [])
w("log_len=%d" % len(log))
for e in log[-3:]:
    w("LOG>> " + e[:500])

# 2. git status + lock
lock = os.path.join(ROOT, ".git", "index.lock")
w("index_lock=%s" % os.path.exists(lock))
r = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
w("git_status:")
w(r.stdout.strip()[:900] or "(clean)")
r2 = subprocess.run(["git", "log", "--oneline", "-3"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
w("git_log3:")
w(r2.stdout.strip()[:700])

# 3. local orders latest
od = os.path.join(ROOT, "orders")
files = []
for fn in os.listdir(od):
    p = os.path.join(od, fn)
    if os.path.isfile(p):
        files.append((os.path.getmtime(p), fn))
files.sort(reverse=True)
w("orders_top3=%s" % " | ".join("%s" % fn for _, fn in files[:3]))

# 4. evolution-ledger scan (strict @ prefix lines)
el = os.path.join(GRP, "cph4", "evolution-ledger.md")
with open(el, encoding="utf-8", errors="replace") as f:
    lines = f.readlines()
pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线全量)")
hits = [(i + 1, l.rstrip()) for i, l in enumerate(lines) if pat.search(l)]
w("ledger_hits=%d" % len(hits))
for ln, txt in hits[-4:]:
    w("LEDGER L%d: %s" % (ln, txt[:230]))

# 5. decisions.md D/C content-addressed diff
with open(os.path.join(GRP, "docs", "decisions.md"), encoding="utf-8", errors="replace") as f:
    txt = f.read()
nums = set(re.findall(r"[DC]-\d{8}-\d{2}", txt))
new = sorted(nums - dnums)
w("decisions_total=%d new=%d" % (len(nums), len(new)))
w("new_dnums=%s" % (",".join(new) if new else "NONE"))

# 6. daily brief today
w("daily_1004=%s" % os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-10-04.md")))

# 7. audits dir + weekly audit presence
ad = os.path.join(ROOT, "docs", "audits")
names = sorted(os.listdir(ad))
w("audits_files=%s" % ", ".join(names))
w("W40_audit_present=%s" % any("W40" in n for n in names))

# 8. global-benchmarks first date
with open(os.path.join(ROOT, "docs", "global-benchmarks.md"), encoding="utf-8", errors="replace") as f:
    gtxt = f.read()
m = re.search(r"2026-\d{2}-\d{2}", gtxt)
w("gb_first_date=%s" % (m.group(0) if m else "NONE"))

# 9. self-improvement queue head
sq = os.path.join(ROOT, "docs", "self-improvement-queue.md")
with open(sq, encoding="utf-8", errors="replace") as f:
    sqt = f.read()
w("queue_chars=%d" % len(sqt))
w("queue_head_lines:")
cnt = 0
for l in sqt.splitlines():
    if l.strip():
        w("  " + l[:160])
        cnt += 1
    if cnt >= 18:
        break

# 10. src/os scripts inventory
so = os.path.join(ROOT, "src", "os")
w("src_os=%s" % ", ".join(sorted(os.listdir(so))))

with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("WROTE %d lines" % len(out))
