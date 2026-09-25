# R238 fast-path scan: group ledger + decisions anchors, storylines progress, lock check
import io, os, json, glob, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = io.open(os.path.join(ROOT, ".bs005-tmp", "r238-scan.txt"), "w", encoding="utf-8")

# 1. Group ledger scan: strict line-contains @ four modes
ledger = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
pat = ("@BigStream", "@七线全司", "@全司", "@六司")
n = 0
last = ""
mtime_l = ""
if os.path.exists(ledger):
    mtime_l = datetime.datetime.fromtimestamp(os.path.getmtime(ledger)).strftime("%m-%d %H:%M:%S")
    with io.open(ledger, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if any(p in line for p in pat):
                n += 1
                last = line.strip()[:120]
out.write("ledger_at_lines=%d (anchor=14) mtime=%s\n" % (n, mtime_l))
out.write("ledger_last_match=%s\n" % last)

# 2. Group decisions: UTF8 non-empty line count (anchor 24, total 27 dual)
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
mtime_d = ""
if os.path.exists(dec):
    mtime_d = datetime.datetime.fromtimestamp(os.path.getmtime(dec)).strftime("%m-%d %H:%M:%S")
    with io.open(dec, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    nonempty = sum(1 for l in lines if l.strip())
    out.write("decisions_nonempty=%d (anchor=24) total=%d (anchor=27) mtime=%s\n" % (nonempty, len(lines), mtime_d))
else:
    out.write("decisions MISSING\n")

# 3. index.lock check
lock = os.path.join(ROOT, ".git", "index.lock")
out.write("index_lock=%s\n" % os.path.exists(lock))

# 4. storylines progress: novel / comic / audio latest
for sub in ("novel", "comic", "audio"):
    d = os.path.join(ROOT, "data", "storylines", sub)
    files = []
    if os.path.isdir(d):
        for fn in os.listdir(d):
            p = os.path.join(d, fn)
            if os.path.isfile(p):
                files.append((fn, os.path.getmtime(p)))
    files.sort(key=lambda x: -x[1])
    top3 = [(f, datetime.datetime.fromtimestamp(m).strftime("%m-%d %H:%M")) for f, m in files[:3]]
    out.write("storylines_%s=%s\n" % (sub, top3))

# 5. orders top file mtime
od = os.path.join(ROOT, "orders")
of = sorted(((os.path.getmtime(os.path.join(od, f)), f) for f in os.listdir(od)), reverse=True)[0]
out.write("orders_top=%s mtime=%s\n" % (of[1], datetime.datetime.fromtimestamp(of[0]).strftime("%m-%d %H:%M")))

# 6. state.json focus fields
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8"))
out.write("state_tick=%d production=%s\n" % (st.get("tick", -1), st.get("production")))

# 7. daily report today
today = "2026-09-25"
dr = os.path.join(ROOT, "data", "intel", "daily", today + ".md")
out.write("daily_report=%s\n" % os.path.exists(dr))

# 8. global benchmarks freshness
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
if os.path.exists(gb):
    out.write("global_benchmarks_mtime=%s\n" % datetime.datetime.fromtimestamp(os.path.getmtime(gb)).strftime("%m-%d %H:%M"))

# 9. weekly audit current week exists
w = glob.glob(os.path.join(ROOT, "docs", "audits", "2026-W39*"))
out.write("week_audit=%s\n" % [os.path.basename(x) for x in w])

out.close()
print("done")
