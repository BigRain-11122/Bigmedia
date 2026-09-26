# r461 fast-path five-check probe (ASCII script, UTF-8 report file)
import json, os, re, io, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
FG = r"C:\Users\sjs20\Desktop\FluxGroup"
OUTP = os.path.join(ROOT, ".c3-tmp", "r462X_check.txt")
out = io.open(OUTP, "w", encoding="utf-8")
def w(s):
    out.write(s + "\n")

# 1. state.json
st = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
w("tick=%s" % st.get("tick"))
w("ts=%s" % st.get("ts"))
w("production=%s" % st.get("production"))
log = st.get("log", [])
w("log_len=%d" % len(log))
for line in log[-3:]:
    w("LOG>> " + line[:200])

# 2. orders latest 5 by mtime (anchor = O-20260925-1931-HQ-C mtime)
od = os.path.join(ROOT, "orders")
anchor = os.path.join(od, "O-20260925-1931-HQ-C.md")
anchor_m = os.path.getmtime(anchor) if os.path.exists(anchor) else 0
files = [(os.path.getmtime(os.path.join(od, f)), f) for f in os.listdir(od)
         if os.path.isfile(os.path.join(od, f))]
files.sort(reverse=True)
new_after_anchor = [f for m, f in files if m > anchor_m and f != "README.md"]
edited_since_anchor = [f for m, f in files if m > anchor_m]
w("orders_new_after_anchor=%s" % (new_after_anchor if new_after_anchor else "NONE"))
w("orders_edited_since_anchor=%s" % (edited_since_anchor if edited_since_anchor else "NONE"))
for m, f in files[:3]:
    w("ORDER %s mtime=%s" % (f, datetime.datetime.fromtimestamp(m).strftime("%Y-%m-%d %H:%M:%S")))

# 3. ledger scan (canonical method per r459_check/r460_canon: any line containing five-mode tags)
led = io.open(os.path.join(FG, "cph4", "evolution-ledger.md"), encoding="utf-8", errors="replace").read().splitlines()
pat = re.compile(r"@(BigStream|涓冪嚎鍏ㄥ徃|鍏ㄥ徃|鍏徃|鍏嚎鍏ㄩ噺)")
hits = [l for l in led if pat.search(l)]
w("ledger_at_lines=%d" % len(hits))
if hits:
    w("ledger_last_hit_ascii=%s" % hits[-1][:60].encode("ascii", "replace").decode("ascii"))

# 4. decisions non-empty count
dec = io.open(os.path.join(FG, "docs", "decisions.md"), encoding="utf-8", errors="replace").read().splitlines()
nz = [l for l in dec if l.strip()]
w("decisions_nonempty=%d total=%d" % (len(nz), len(dec)))

# 5. routine files
w("intel_0927=%s" % os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-27.md")))
w("audit_w39=%s" % os.path.exists(os.path.join(ROOT, "docs", "audits", "2026-W39-self-audit.md")))
w("index_lock=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 6. CENSUS supply-gate anchor C-00030 (canonical anchors/ position only)
cands = [
    os.path.join(FG, "life", "BigLife", "census", "anchors", "C-00030.md"),
    os.path.join(FG, "media", "BigLife", "census", "anchors", "C-00030.md"),
]
w("anchor_c00030=%s" % any(os.path.exists(p) for p in cands))
for p in cands:
    if os.path.isdir(os.path.dirname(p)):
        names = sorted(os.listdir(os.path.dirname(p)))
        w("anchors_dir=%s last3=%s" % (os.path.dirname(p)[-30:], names[-3:]))

# 7. storylines bm-a write detection (novel/audio/comic, files modified on 09-27)
today = "2026-09-27"
cnt = {"novel": 0, "audio": 0, "comic": 0}
base = os.path.join(ROOT, "data", "storylines")
for sub in cnt:
    d = os.path.join(base, sub)
    if os.path.isdir(d):
        for dirpath, dirnames, filenames in os.walk(d):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    mt = datetime.date.fromtimestamp(os.path.getmtime(fp)).isoformat()
                except OSError:
                    continue
                if mt >= today:
                    cnt[sub] += 1
w("storylines_writes_today=%d/%d/%d" % (cnt["novel"], cnt["audio"], cnt["comic"]))

# 8. status-export export_ts
try:
    se = json.load(io.open(os.path.join(ROOT, "docs", "status-export.json"), encoding="utf-8"))
    w("export_ts=%s" % se.get("export_ts"))
except Exception as e:
    w("export_ts_err=%s" % e)

# 9. backlog top 3 non-header lines
bl = io.open(os.path.join(ROOT, "src", "os", "backlog.md"), encoding="utf-8", errors="replace").read().splitlines()
started = False
shown = 0
for l in bl:
    if not started and l.strip().startswith("#"):
        started = True
        continue
    if not started:
        continue
    if l.strip():
        w("BACKLOG>> " + l[:300])
        shown += 1
    if shown >= 3:
        break

out.close()
print("OK")

