# r486_check.py - R486 quick-path five-check probe (new file, OUTP new, utf-8; window 6/6 -> batch commit if quiet)
import io, os, re, json, glob, subprocess, datetime
from collections import Counter

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r486_check.txt")
L = []
def w(s):
    L.append(str(s))

now = datetime.datetime.now()
w("now=" + now.strftime("%Y-%m-%d %H:%M:%S"))

# 1) orders: O- count + anchor mtime + edited-since-anchor + top3 newest by mtime
od = os.path.join(ROOT, "orders")
anchor = "O-20260925-1931-HQ-C.md"
am = os.path.getmtime(os.path.join(od, anchor))
o_files = sorted(f for f in os.listdir(od) if f.startswith("O-"))
edited = [f for f in os.listdir(od) if os.path.getmtime(os.path.join(od, f)) > am + 1.0]
w("orders_o_count=%d anchor=%s mtime=%s" % (len(o_files), anchor, datetime.datetime.fromtimestamp(am).strftime("%H:%M:%S")))
w("orders_edited_since_anchor=%s" % (edited or "NONE"))
top3 = sorted(os.listdir(od), key=lambda f: -os.path.getmtime(os.path.join(od, f)))[:3]
for f in top3:
    w("orders_top_mtime=%s %s" % (datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(od, f))).strftime("%m-%d %H:%M:%S"), f))

# 2) ledger five-mode LINE count (canonical metric, anchor=29) + mode breakdown
pat = re.compile(r'@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf\u5168\u91cf)')
hits = [l.rstrip('\n') for l in io.open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding='utf-8', errors='replace') if pat.search(l)]
w("ledger_lines=%d anchor=29" % len(hits))
w("ledger_last_hit_ascii=%s" % hits[-1][:60].encode('ascii', 'replace').decode('ascii'))
c = Counter()
for l in hits:
    for m in pat.findall(l):
        c[m] += 1
w("ledger_modes=%s" % dict(c))

# 3) decisions non-empty count (utf-8, anchor=45)
with io.open(r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md", "r", encoding="utf-8") as f:
    n = sum(1 for ln in f if ln.strip())
w("decisions_nonempty=%d anchor=45" % n)

# 4) index.lock
w("index_lock_exists=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 5) BigLife census anchors canonical position check (C-00030/31)
ad = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
if os.path.isdir(ad):
    names = sorted(x for x in os.listdir(ad) if x.endswith(".md"))
    w("anchors_total=%d tail3=%s" % (len(names), names[-3:]))
else:
    w("anchors_dir_missing")
w("anchor_c00030=%s anchor_c00031=%s" % (
    os.path.exists(os.path.join(ad, "C-00030.md")),
    os.path.exists(os.path.join(ad, "C-00031.md"))))

# 6) storylines subdomain new writes since R485 close (07:53:15)
thr = datetime.datetime(2026, 9, 27, 7, 53, 15).timestamp()
for sub in ("novel", "audio", "comic"):
    d = os.path.join(ROOT, "data", "storylines", sub)
    neww = [os.path.basename(x) for x in glob.glob(os.path.join(d, "*")) if os.path.getmtime(x) > thr]
    w("storylines_%s_new_since_r485=%d" % (sub, len(neww)))

# 7) state.json production self-heal check + tick
with io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8") as f:
    st = json.load(f)
w("production=%s tick=%d" % (st.get("production"), st.get("tick")))
if st.get("production") != "open":
    w("SELF_HEAL_NEEDED")

# 8) routine file states
w("daily_0927=%s daily_0928=%s" % (
    os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-27.md")),
    os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-28.md"))))
aud = os.path.join(ROOT, "docs", "audits")
afiles = sorted(x for x in os.listdir(aud) if x.endswith(".md")) if os.path.isdir(aud) else []
w("audits_tail3=%s" % afiles[-3:])
w("w40_audit=%s" % os.path.exists(os.path.join(aud, "2026-W40-self-audit.md")))

# 9) git HEAD + interleave check (anchor HEAD = 897fd23 R480 batch)
p = subprocess.run(["git", "log", "-1", "--format=%h %s"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
w("git_head=" + (p.stdout or "").strip()[:180])
p2 = subprocess.run(["git", "log", "--oneline", "897fd23..HEAD"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
w("inserts_after_897fd23=%d" % len([x for x in (p2.stdout or "").splitlines() if x.strip()]))

with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("\n".join(L))
