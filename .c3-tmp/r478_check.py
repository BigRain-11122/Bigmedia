# -*- coding: utf-8 -*-
"""R478 fast-path five-check + probes + digest (r477_check method, OUTP fresh file; +C-00030/31 anchor canonical-position direct check per R316 supply-gate law)."""
import os, re, glob, time, subprocess, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r478_check.txt")
PROBE_OUT = os.path.join(ROOT, ".c3-tmp", "r478_probe.txt")
lines = []
def w(s):
    lines.append(s)

w("now " + time.strftime("%Y-%m-%d %H:%M:%S"))

# 1. orders latest + edit-detection anchor (D-05(2): any edit to existing order file -> newest mtime surfaces)
od = glob.glob("orders/O-*.md")
od.sort(key=os.path.getmtime)
w("orders_top " + (os.path.basename(od[-1]) if od else "NONE"))
w("orders_top_mtime " + (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(od[-1]))) if od else "-"))
allord = sorted(glob.glob("orders/*.md"), key=os.path.getmtime)
for f in allord[-3:]:
    w("orders_recent " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(f))) + " " + os.path.basename(f))
w("orders_O_count " + str(len(od)))

# 2. index.lock
w("index_lock " + str(os.path.exists(".git/index.lock")))

# 3. ledger five-mode rows (strict @ prefix, r475_canon method)
try:
    ld = open(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md", encoding="utf-8", errors="replace").read()
    pat = re.compile(r"@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf\u5168\u91cf)")
    rows = [l for l in ld.splitlines() if pat.search(l)]
    w("ledger_rows " + str(len(rows)))
    if rows:
        w("ledger_last_row_ascii " + rows[-1][:70].encode("ascii", "replace").decode("ascii"))
    c = {}
    for l in rows:
        for m in pat.findall(l):
            c[m] = c.get(m, 0) + 1
    w("ledger_modes " + str(c))
except Exception as e:
    w("ledger_ERR " + repr(e))

# 4. decisions non-empty count (anchor 45)
try:
    dc = open(r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md", encoding="utf-8").read()
    w("decisions_nonempty " + str(len([l for l in dc.splitlines() if l.strip()])))
except Exception as e:
    w("decisions_ERR " + repr(e))

# 5. daily briefs
w("daily_0927 " + str(os.path.exists("data/intel/daily/2026-09-27.md")))
w("daily_0928 " + str(os.path.exists("data/intel/daily/2026-09-28.md")))

# 6. state fields (json parse)
st_txt = open("src/os/state.json", encoding="utf-8").read()
st = json.loads(st_txt)
w("production " + str(st.get("production")))
w("state_tick " + str(st.get("tick")))
w("state_ts " + str(st.get("ts")))
w("state_task_head " + str(st.get("task"))[:80])
log = st.get("log", [])
w("state_log_len " + str(len(log)))
for i, ent in enumerate(log[-3:]):
    w("log_tail_%d_head %s" % (i, ent[:260]))
    w("log_tail_%d_tail %s" % (i, ent[-150:]))

# 7. C-00030/31 supply gate: canonical anchor position = BigLife census/anchors/ (R316 law) + in-repo reference scan
w("anchor_C00030_canon " + str(os.path.exists(r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md")))
w("anchor_C00031_canon " + str(os.path.exists(r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00031.md")))
try:
    adir = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
    afs = sorted(os.listdir(adir))
    w("anchor_dir_count " + str(len(afs)) + " last3 " + ",".join(afs[-3:]))
except Exception as e:
    w("anchor_dir_ERR " + repr(e))
hits = []
for f in glob.glob("data/**/census*.json", recursive=True) + glob.glob("data/**/anchors*.json", recursive=True):
    try:
        c2 = open(f, encoding="utf-8").read()
        if "C-00030" in c2 or "C-00031" in c2:
            hits.append(f)
    except Exception:
        pass
w("anchor_ref_in_repo " + (str(hits) if hits else "False"))

# 8. storylines bm-a activity signs
base = "data/storylines"
for sub in ("novel", "audio", "comic"):
    d = os.path.join(base, sub)
    newest = 0
    if os.path.isdir(d):
        for root, _dirs, files in os.walk(d):
            for f in files:
                newest = max(newest, os.path.getmtime(os.path.join(root, f)))
    w("storylines_%s_newest %s" % (sub, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(newest)) if newest else "none"))

# 9. git status + HEAD
g = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, encoding="utf-8")
w("git_status_begin")
w(g.stdout.strip() if g.stdout.strip() else "(clean)")
w("git_status_end")
h = subprocess.run(["git", "log", "-1", "--oneline"], capture_output=True, text=True, encoding="utf-8")
w("HEAD " + h.stdout.strip())

# 10. three probes (full output -> r478_probe.txt; digest -> this file)
po = open(PROBE_OUT, "w", encoding="utf-8")
probes = [
    ("board", ["python", "src/board_check.py"]),
    ("readiness", ["python", "src/readiness.py"]),
    ("loop_health", ["python", "src/os/loop_health.py"]),
]
digest = {}
for name, cmd in probes:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True)
    txt = p.stdout.decode("utf-8", errors="replace")
    po.write("=== %s exit=%d ===\n" % (name, p.returncode))
    po.write(txt + "\n")
    if p.stderr:
        po.write("[stderr] " + p.stderr.decode("utf-8", errors="replace")[:500] + "\n")
    digest[name] = (p.returncode, txt)
po.close()

w("")
w("=== probe digest ===")
rc, txt = digest["board"]
summ = [l for l in txt.splitlines() if l.startswith("summary:")]
w("board exit=%d %s" % (rc, summ[0] if summ else "?"))
rc, txt = digest["readiness"]
for l in txt.splitlines():
    if l.startswith("readiness:") or l.startswith("- first-launch") or l.startswith("- M4 gate") or l.startswith("- decision pending"):
        w("readiness " + l)
rc, txt = digest["loop_health"]
for l in txt.splitlines():
    if l.startswith("summary:") or l.startswith("- [FAIL]") or l.startswith("loop health:"):
        w("loop_health " + l)
wl = [l for l in txt.splitlines() if l.startswith("- [WARN]")]
w("loop_health warn_count %d" % len(wl))
w("loop_health warn_new_after_0927_0315 %d" % len([l for l in wl if re.search(r"2026-09-2[78] (0[4-9]|1\d|2\d):", l)]))

with open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("OK r478_check")
