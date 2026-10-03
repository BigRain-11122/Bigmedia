# -*- coding: utf-8 -*-
# R1161 fast-path five-check probe (read-only, zero API token).
# Collects: state tail, group decisions diff, ledger hits, local orders,
# git status, board top, routines, queue head, src/os listing.
import json, re, os, subprocess, time, io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP  = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT  = os.path.join(ROOT, ".c3-tmp", "r1161_probe.txt")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

buf = io.StringIO()
def sec(t): buf.write("\n===== %s =====\n" % t)

def rd(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()

sec("TIME")
buf.write("now=%s\n" % time.strftime("%Y-%m-%d %H:%M:%S"))

# 1) state.json
st = json.loads(rd(os.path.join(ROOT, "src", "os", "state.json")))
sec("STATE CORE")
buf.write("keys=%s\n" % ",".join(st.keys()))
buf.write("tick=%s ts=%s production=%s\n" % (st.get("tick"), st.get("ts"), st.get("production")))
buf.write("task=%s\n" % str(st.get("task"))[:220])
log = st.get("log", [])
if isinstance(log, list):
    sec("LOG TAIL 3 (of %d)" % len(log))
    for line in log[-3:]:
        buf.write(str(line)[:2400] + "\n")
wm = st.get("decisions_watermark", {})
sec("WATERMARK")
buf.write(json.dumps(wm, ensure_ascii=False)[:700] + "\n")
dnums = set(wm.get("dnums", [])) if isinstance(wm, dict) else set()

# 2) group decisions.md diff (content-addressed)
dtxt = rd(os.path.join(GRP, "docs", "decisions.md"))
cur = set(re.findall(r"[DC]-\d{8}-\d{2}", dtxt))
new = sorted(cur - dnums)
sec("DECISIONS DIFF")
buf.write("cur=%d wm=%d new=%d\n" % (len(cur), len(dnums), len(new)))
buf.write("new_ids=%s\n" % (",".join(new) if new else "NONE"))
buf.write("last_ids=%s\n" % ",".join(sorted(cur)[-8:]))
dl = dtxt.splitlines()
sec("DECISIONS TOP (BigStream/7si hits in first 120 lines)")
for i, l in enumerate(dl[:120]):
    s = l.strip()
    if s and ("BigStream" in s or u"七司" in s):
        buf.write("L%d: %s\n" % (i + 1, s[:200]))

# 3) group orders.md BigStream hits
otxt = rd(os.path.join(GRP, "docs", "orders.md"))
sec("GRP ORDERS BigStream hits (last 5)")
for l in [x.strip()[:180] for x in otxt.splitlines() if "BigStream" in x][-5:]:
    buf.write(l + "\n")

# 4) evolution-ledger scan
led = rd(os.path.join(GRP, "cph4", "evolution-ledger.md")).splitlines()
pat = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线")
hits = [(i + 1, l.strip()) for i, l in enumerate(led) if pat.search(l)]
sec("LEDGER HITS count=%d (last 8)" % len(hits))
for n, l in hits[-8:]:
    buf.write("L%d: %s\n" % (n, l[:190]))
prow = [(i + 1, l.strip()) for i, l in enumerate(led) if re.search(r"P-2026-10-0[34]-", l)]
sec("LEDGER P-2026-10-03/04 rows count=%d" % len(prow))
for n, l in prow[-10:]:
    buf.write("L%d: %s\n" % (n, l[:190]))

# 5) local orders dir
odir = os.path.join(ROOT, "orders")
sec("LOCAL ORDERS TOP6 BY MTIME")
fs = sorted(os.listdir(odir), key=lambda f: os.path.getmtime(os.path.join(odir, f)), reverse=True)
for f in fs[:6]:
    mt = time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(os.path.join(odir, f))))
    buf.write("%s | %s\n" % (mt, f))

# 6) git status
r = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True)
sec("GIT STATUS")
buf.write((r.stdout.strip() or "CLEAN")[:1500] + "\n")
buf.write("index_lock=%s\n" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 7) board top
bl = rd(os.path.join(ROOT, "src", "os", "backlog.md")).splitlines()
sec("BOARD FIRST 14 NUMBERED ITEMS")
c = 0
for l in bl:
    m = re.match(r"^(\d+)\.\s", l)
    if m:
        c += 1
        buf.write("#%s %s | %s\n" % (m.group(1), "DONE" if "[done" in l else "OPEN", l.strip()[:160]))
        if c >= 14:
            break
sec("BOARD FIRST 6 OPEN DETAIL")
c = 0
for l in bl:
    m = re.match(r"^(\d+)\.\s", l)
    if m and "[done" not in l:
        c += 1
        buf.write("#%s %s\n" % (m.group(1), l.strip()[:280]))
        if c >= 6:
            break
sec("BOARD 82/83 CHECK")
for l in bl:
    if re.match(r"^8[23]\.", l):
        buf.write(l.strip()[:280] + "\n")

# 8) routines
sec("ROUTINES")
buf.write("daily_today=%s\n" % os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-10-04.md")))
aud = sorted(os.listdir(os.path.join(ROOT, "docs", "audits")))
buf.write("audits_list=%s\n" % ",".join(aud[-12:]))
gb = rd(os.path.join(ROOT, "docs", "global-benchmarks.md"))
gbd = re.findall(r"2026-\d{2}-\d{2}", gb)
buf.write("gb_dates_head=%s\n" % gbd[:4])
se = json.loads(rd(os.path.join(ROOT, "docs", "status-export.json")))
buf.write("export_ts=%s\n" % str(se.get("export_ts", se.get("ts"))))

# 9) queue head
q = rd(os.path.join(ROOT, "docs", "self-improvement-queue.md")).splitlines()
sec("QUEUE HEAD 40 LINES (of %d)" % len(q))
for l in q[:40]:
    buf.write(l[:170] + "\n")

# 10) src/os listing + python procs
sec("SRC/OS FILES")
buf.write(",".join(sorted(os.listdir(os.path.join(ROOT, "src", "os")))) + "\n")
r2 = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe"], capture_output=True, text=True)
buf.write("python_procs_tail=\n" + r2.stdout[-420:] + "\n")

with open(OUT, "w", encoding="utf-8") as f:
    f.write(buf.getvalue())
print("WROTE", OUT, len(buf.getvalue()))
