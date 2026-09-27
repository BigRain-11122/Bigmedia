# r489_check.py - R489 quick-path five-check probe (new file, OUTP new, utf-8; idle-fast window round 2/6, window R488-R493)
import io, os, re, json, glob, subprocess, datetime
from collections import Counter

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r489_check.txt")
L = []
def w(s):
    L.append(str(s))

now = datetime.datetime.now()
w("now=" + now.strftime("%Y-%m-%d %H:%M:%S"))

# 1) orders: O- count + anchor mtime + edited-since-anchor
od = os.path.join(ROOT, "orders")
anchor = "O-20260925-1931-HQ-C.md"
am = os.path.getmtime(os.path.join(od, anchor))
o_files = sorted(f for f in os.listdir(od) if f.startswith("O-"))
edited = [f for f in os.listdir(od) if os.path.getmtime(os.path.join(od, f)) > am + 1.0]
w("orders_o_count=%d anchor=%s mtime=%s" % (len(o_files), anchor, datetime.datetime.fromtimestamp(am).strftime("%H:%M:%S")))
w("orders_edited_since_anchor=%s" % (edited or "NONE"))

# 2) ledger five-mode LINE count (canonical metric, anchor=30 after R487 P-2026-09-27-02)
pat = re.compile(r'@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf\u5168\u91cf)')
hits = [l.rstrip('\n') for l in io.open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding='utf-8', errors='replace') if pat.search(l)]
w("ledger_lines=%d anchor=30" % len(hits))
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

# 6) storylines subdomain new writes since R488 close (08:26:04)
thr = datetime.datetime(2026, 9, 27, 8, 26, 4).timestamp()
for sub in ("novel", "audio", "comic"):
    d = os.path.join(ROOT, "data", "storylines", sub)
    neww = [os.path.basename(x) for x in glob.glob(os.path.join(d, "*")) if os.path.getmtime(x) > thr]
    w("storylines_%s_new_since_r488=%d" % (sub, len(neww)))

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
hq = os.path.join(ROOT, "HQ-FEEDBACK.md")
w("hq_feedback_mtime=%s" % datetime.datetime.fromtimestamp(os.path.getmtime(hq)).strftime("%m-%d %H:%M:%S"))

# 9) backlog top claimability read (top 3 non-empty lines)
with io.open(os.path.join(ROOT, "src", "os", "backlog.md"), "r", encoding="utf-8") as f:
    lines = [ln.rstrip('\n') for ln in f if ln.strip()]
for ln in lines[:3]:
    w("backlog_top=" + ln[:150])

# 10) git HEAD top3 (expect R487 live-round commit at HEAD, no cut-ins)
p = subprocess.run(["git", "log", "-3", "--format=%h %ad %s", "--date=format:%m-%d %H:%M"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
for ln in (p.stdout or "").splitlines():
    if ln.strip():
        w("git_log=" + ln.strip()[:160])

# 11) status-export mojibake residue scan (R487 GBK-damaged chars fix; R488 claimed landed)
se_path = os.path.join(ROOT, "docs", "status-export.json")
se_txt = io.open(se_path, "r", encoding="utf-8", errors="replace").read()
moji = ["\u6536\u8b26", "\u6536\u8bb3", "\u6536\u8bb0", "\u56de\u626d", "\u5b9a\u8c34"]
left = [m for m in moji if m in se_txt]
w("mojibake_in_status_export=%s" % (left if left else "NONE"))

with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("\n".join(L))
