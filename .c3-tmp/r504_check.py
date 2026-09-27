# r504_check.py - R504 quick-path five-check probe (new file via write_file, OUTP new, utf-8; O-1050 active-agenda round, window R503-R508)
import io, os, re, json, glob, subprocess, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r504_check.txt")
L = []
def w(s):
    L.append(str(s))

now = datetime.datetime.now()
w("now=" + now.strftime("%Y-%m-%d %H:%M:%S"))

# 1) orders: O- count + anchor mtime (anchor=O-20260927-1050-HQ-C CEO direct order) + edited-since-anchor
od = os.path.join(ROOT, "orders")
anchor = "O-20260927-1050-HQ-C.md"
am = os.path.getmtime(os.path.join(od, anchor))
o_files = sorted(f for f in os.listdir(od) if f.startswith("O-"))
edited = [f for f in os.listdir(od) if os.path.getmtime(os.path.join(od, f)) > am + 1.0]
w("orders_o_count=%d anchor=%s mtime=%s" % (len(o_files), anchor, datetime.datetime.fromtimestamp(am).strftime("%m-%d %H:%M:%S")))
w("orders_edited_since_anchor=%s" % (edited or "NONE"))

# 2) ledger five-mode LINE count (canonical metric, anchor=30 since R487)
pat = re.compile(r'@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf\u5168\u91cf)')
hits = [l.rstrip('\n') for l in io.open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding='utf-8', errors='replace') if pat.search(l)]
w("ledger_lines=%d anchor=30" % len(hits))
w("ledger_last_hit_ascii=%s" % hits[-1][:60].encode('ascii', 'replace').decode('ascii'))

# 3) decisions non-empty count (utf-8, anchor=48 after R503 processed 45->48)
with io.open(r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md", "r", encoding="utf-8") as f:
    n = sum(1 for ln in f if ln.strip())
w("decisions_nonempty=%d anchor=48" % n)

# 4) index.lock
w("index_lock_exists=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 5) BigLife census anchors canonical position check (C-00030/31 supply-gate)
ad = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
if os.path.isdir(ad):
    names = sorted(x for x in os.listdir(ad) if x.endswith(".md"))
    w("anchors_total=%d tail3=%s" % (len(names), names[-3:]))
else:
    w("anchors_dir_missing")
w("anchor_c00030=%s anchor_c00031=%s" % (
    os.path.exists(os.path.join(ad, "C-00030.md")),
    os.path.exists(os.path.join(ad, "C-00031.md"))))

# 5b) BigLife interchat content ledger presence probe (#72 knowledge item, window <=09-28 12:00)
ic = []
BL = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife"
KEY = "\u4e92\u804a"
for dirpath, dirnames, filenames in os.walk(BL):
    for fn in filenames:
        if KEY in fn:
            ic.append(os.path.join(dirpath, fn))
    for dn in dirnames:
        if KEY in dn:
            ic.append(os.path.join(dirpath, dn) + os.sep)
    if len(ic) >= 5:
        break
w("biglife_interchat_hits=%d" % len(ic))

# 6) state.json: production self-heal check + tail reprs
sp = os.path.join(ROOT, "src", "os", "state.json")
with io.open(sp, "r", encoding="utf-8") as f:
    st = json.load(f)
w("production=%s tick=%d" % (st.get("production"), st.get("tick")))
if st.get("production") != "open":
    w("SELF_HEAL_NEEDED")
w("state_mtime=%s" % datetime.datetime.fromtimestamp(os.path.getmtime(sp)).strftime("%m-%d %H:%M:%S"))
ts_prev = st.get("ts")
w("ts_prev=%s" % ts_prev)
w("task_prev_repr=" + repr(st.get("task")))
w("log_len=%d" % len(st["log"]))
for e in st["log"][-3:]:
    w("log_tail3=" + str(e)[:70])

# 7) storylines subdomain new writes since prev ts
thr = datetime.datetime.strptime(ts_prev, "%Y-%m-%d %H:%M:%S").timestamp() if ts_prev else 0
for sub in ("novel", "audio", "comic"):
    d = os.path.join(ROOT, "data", "storylines", sub)
    neww = [os.path.basename(x) for x in glob.glob(os.path.join(d, "*")) if os.path.getmtime(x) > thr]
    w("storylines_%s_new=%d" % (sub, len(neww)))

# 8) routine file states
w("daily_0927=%s daily_0928=%s" % (
    os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-27.md")),
    os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-28.md"))))
aud = os.path.join(ROOT, "docs", "audits")
afiles = sorted(x for x in os.listdir(aud) if x.endswith(".md")) if os.path.isdir(aud) else []
w("w40_audit=%s" % os.path.exists(os.path.join(aud, "2026-W40-self-audit.md")))
hq = os.path.join(ROOT, "HQ-FEEDBACK.md")
w("hq_feedback_mtime=%s" % datetime.datetime.fromtimestamp(os.path.getmtime(hq)).strftime("%m-%d %H:%M:%S"))

# 9) backlog top 3 non-empty lines
with io.open(os.path.join(ROOT, "src", "os", "backlog.md"), "r", encoding="utf-8") as f:
    lines = [ln.rstrip('\n') for ln in f if ln.strip()]
for ln in lines[:3]:
    w("backlog_top=" + ln[:150])

# 10) git HEAD top3
p = subprocess.run(["git", "log", "-3", "--format=%h %ad %s", "--date=format:%m-%d %H:%M"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
for ln in (p.stdout or "").splitlines():
    if ln.strip():
        w("git_log=" + ln.strip()[:160])

# 11) git status --short
p = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
mod = 0
for ln in (p.stdout or "").splitlines():
    if ln.strip():
        w("git_status=" + ln.strip()[:120])
        mod += 1
w("git_status_dirty_count=%d" % mod)

# 12) R-03 file presence + version markers (agenda-1 target file)
r03 = os.path.join(ROOT, "docs", "research", "R-20260927-bigstream-03-ai-forms-platform-algorithms.md")
if os.path.exists(r03):
    txt = io.open(r03, "r", encoding="utf-8").read()
    w("r03_exists len=%d has_v01=%s has_v10=%s" % (len(txt), "v0.1" in txt, "v1.0" in txt))
else:
    w("r03_missing")

# 13) release-schedule-v1 presence (agenda-2 delivered R503)
w("release_schedule_v1=%s" % os.path.exists(os.path.join(ROOT, "docs", "release-schedule-v1.md")))

with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("written=%s lines=%d" % (os.path.basename(OUTP), len(L)))
for ln in L:
    if ln.startswith(("orders_", "ledger_lines", "decisions_", "index_lock", "anchor_", "anchors_total", "biglife_", "production=", "storylines_", "daily_092", "w40_", "git_status_dirty", "now=", "r03_", "release_")):
        print(ln)
