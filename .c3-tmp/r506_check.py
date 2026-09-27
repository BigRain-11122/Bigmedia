# r506_check.py - R506 full-round five-check probe (agenda-4 research round; anchors: orders 35, ledger 30, decisions 45)
import io, os, re, json, glob, subprocess, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r506_check.txt")
L = []
def w(s):
    L.append(str(s))

now = datetime.datetime.now()
w("now=" + now.strftime("%Y-%m-%d %H:%M:%S"))

# 1) orders: O- count + anchor mtime + edited-since-anchor
od = os.path.join(ROOT, "orders")
anchor = "O-20260927-1050-HQ-C.md"
am = os.path.getmtime(os.path.join(od, anchor))
o_files = sorted(f for f in os.listdir(od) if f.startswith("O-"))
edited = [f for f in os.listdir(od) if os.path.getmtime(os.path.join(od, f)) > am + 1.0]
w("orders_o_count=%d anchor=%s mtime=%s" % (len(o_files), anchor, datetime.datetime.fromtimestamp(am).strftime("%m-%d %H:%M:%S")))
w("orders_edited_since_anchor=%s" % (edited or "NONE"))

# 2) ledger five-mode LINE count (canonical metric, anchor=30)
pat = re.compile(r'@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf\u5168\u91cf)')
hits = [l.rstrip('\n') for l in io.open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding='utf-8', errors='replace') if pat.search(l)]
w("ledger_lines=%d anchor=30" % len(hits))
if len(hits) > 30:
    for h in hits[30:]:
        w("ledger_new_hit=" + h[:120].encode('ascii', 'replace').decode('ascii'))

# 3) decisions non-empty count (utf-8, anchor=45)
with io.open(r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md", "r", encoding="utf-8") as f:
    n = sum(1 for ln in f if ln.strip())
w("decisions_nonempty=%d anchor=45" % n)

# 4) index.lock
w("index_lock_exists=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 5) BigLife census anchors + interchat probe (#72, window <=09-28 12:00)
ad = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
if os.path.isdir(ad):
    names = sorted(x for x in os.listdir(ad) if x.endswith(".md"))
    w("anchors_total=%d tail3=%s" % (len(names), names[-3:]))
w("anchor_c00030=%s anchor_c00031=%s" % (
    os.path.exists(os.path.join(ad, "C-00030.md")),
    os.path.exists(os.path.join(ad, "C-00031.md"))))
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

# 6) state.json: production + ts_prev + tick
sp = os.path.join(ROOT, "src", "os", "state.json")
with io.open(sp, "r", encoding="utf-8") as f:
    st = json.load(f)
w("production=%s tick=%d" % (st.get("production"), st.get("tick")))
if st.get("production") != "open":
    w("SELF_HEAL_NEEDED")
ts_prev = st.get("ts")
w("ts_prev=%s" % ts_prev)
w("log_last_head=" + repr(str(st["log"][-1])[:60]))
w("log_len=%d" % len(st["log"]))

# 7) storylines subdomain new writes since R505 ts
thr = datetime.datetime.strptime(ts_prev, "%Y-%m-%d %H:%M:%S").timestamp() if ts_prev else 0
for sub in ("novel", "audio", "comic"):
    d = os.path.join(ROOT, "data", "storylines", sub)
    neww = [os.path.basename(x) for x in glob.glob(os.path.join(d, "*")) if os.path.getmtime(x) > thr]
    w("storylines_%s_new_since_r505=%d" % (sub, len(neww)))

# 8) routine file states
w("daily_0927=%s daily_0928=%s" % (
    os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-27.md")),
    os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-28.md"))))
aud = os.path.join(ROOT, "docs", "audits")
afiles = sorted(x for x in os.listdir(aud) if x.endswith(".md")) if os.path.isdir(aud) else []
w("audits_tail3=%s" % afiles[-3:])
w("w40_audit=%s" % os.path.exists(os.path.join(aud, "2026-W40-self-audit.md")))
hq = os.path.join(ROOT, "HQ-FEEDBACK.md")
w("hq_feedback_mtime=%s" % datetime.datetime.fromtimestamp(os.path.getmtime(hq)).strftime("%m-%d %H:%M:%S"))

# 9) git log top3 + status
p = subprocess.run(["git", "log", "-3", "--format=%h %ad %s", "--date=format:%m-%d %H:%M"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
for ln in (p.stdout or "").splitlines():
    if ln.strip():
        w("git_log=" + ln.strip()[:150])
p = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
mod = 0
for ln in (p.stdout or "").splitlines():
    if ln.strip():
        w("git_status=" + ln.strip()[:120])
        mod += 1
w("git_status_dirty_count=%d" % mod)

# 10) status-export anchor dump
sep = os.path.join(ROOT, "docs", "status-export.json")
se = json.load(io.open(sep, "r", encoding="utf-8"))
w("export_ts=" + repr(se.get("export_ts")))
w("outs_len=%d results_len=%d" % (len(se.get("outs", [])), len(se.get("results", []))))
o0 = se["outs"][0]
w("outs0_1_head=" + repr(str(o0[1])[:100]))
w("outs0_1_tail=" + repr(str(o0[1])[-60:]))

with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("written=%s lines=%d" % (os.path.basename(OUTP), len(L)))
for ln in L:
    if ln.startswith(("orders_", "ledger_", "decisions_", "index_lock", "anchor_c", "anchors_total", "biglife_", "production=", "storylines_", "daily_092", "w40_", "git_status_dirty", "now=", "ts_prev")):
        print(ln)
