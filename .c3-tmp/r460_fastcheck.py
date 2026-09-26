# r460 fast-path five-check probe (ASCII script, UTF-8 report file)
import json, os, re, io, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
FG = r"C:\Users\sjs20\Desktop\FluxGroup"
OUTP = os.path.join(ROOT, ".c3-tmp", "r460_fastcheck.txt")
out = io.open(OUTP, "w", encoding="utf-8")
def w(s):
    out.write(s + "\n")

# 1. state.json
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
w("tick=%s" % st.get("tick"))
w("ts=%s" % st.get("ts"))
w("production=%s" % st.get("production"))
w("task=%s" % st.get("task"))
log = st.get("log", [])
w("log_len=%d" % len(log))
for line in log[-3:]:
    w("LOG>> " + line)

# 2. orders latest 5 by mtime
od = os.path.join(ROOT, "orders")
files = [(os.path.getmtime(os.path.join(od, f)), f) for f in os.listdir(od)
         if os.path.isfile(os.path.join(od, f))]
files.sort(reverse=True)
for m, f in files[:5]:
    w("ORDER %s mtime=%s" % (f, datetime.datetime.fromtimestamp(m).strftime("%Y-%m-%d %H:%M:%S")))

# 3. ledger strict @ scan
led = io.open(os.path.join(FG, "cph4", "evolution-ledger.md"), encoding="utf-8", errors="replace").read().splitlines()
pat = re.compile(r"@BigStream|@七线全司|@全司|@六司|@八线全量")
hits = [l for l in led if l.lstrip().startswith("@") and pat.search(l)]
w("ledger_at_lines=%d" % len(hits))
if hits:
    w("ledger_last_hit=%s" % hits[-1][:160])

# 4. decisions non-empty count
dec = io.open(os.path.join(FG, "docs", "decisions.md"), encoding="utf-8", errors="replace").read().splitlines()
nz = [l for l in dec if l.strip()]
w("decisions_nonempty=%d total=%d" % (len(nz), len(dec)))

# 5. global benchmarks first dated line (section 4 update record head)
gb = io.open(os.path.join(ROOT, "docs", "global-benchmarks.md"), encoding="utf-8", errors="replace").read().splitlines()
dates = [l for l in gb if re.search(r"2026-\d{2}-\d{2}", l)]
w("gb_first_dated=%s" % (dates[0][:120] if dates else "NONE"))

# 6. routine files
w("intel_today=%s" % os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-27.md")))
w("audit_w39=%s" % os.path.exists(os.path.join(ROOT, "docs", "audits", "2026-W39-self-audit.md")))
w("index_lock=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 7. CENSUS supply-gate anchor C-00030 (canonical anchors/ position only)
cands = [
    os.path.join(FG, "life", "BigLife", "census", "anchors", "C-00030.md"),
    os.path.join(FG, "media", "BigLife", "census", "anchors", "C-00030.md"),
]
w("anchor_c00030=%s" % any(os.path.exists(p) for p in cands))
# list actual anchors dir top entries
for p in cands:
    if os.path.isdir(os.path.dirname(p)):
        names = sorted(os.listdir(os.path.dirname(p)))
        w("anchors_dir=%s last3=%s" % (os.path.dirname(p)[-30:], names[-3:]))

# 8. status-export export_ts
try:
    se = json.load(io.open(os.path.join(ROOT, "docs", "status-export.json"), encoding="utf-8"))
    w("export_ts=%s" % se.get("export_ts"))
except Exception as e:
    w("export_ts_err=%s" % e)

out.close()
print("OK")
