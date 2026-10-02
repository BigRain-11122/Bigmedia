# R998 quick-path five-check scan (fresh re-verify, zero-token probes incl board/readiness/loop_health)
# encoding: utf-8
import json, io, os, re, sys, glob, datetime, subprocess

OUT = []
def p(s=""):
    OUT.append(s)

now = datetime.datetime.now()
p("scan_ts: %s" % now.strftime("%Y-%m-%d %H:%M:%S"))

# --- 1. orders latest file (top-of-board O-令 check) ---
orders = sorted(glob.glob("orders/*.md"), key=os.path.getmtime)
p("orders_count: %d | top: %s (mtime %s)" % (
    len(orders), os.path.basename(orders[-1]) if orders else "NONE",
    datetime.datetime.fromtimestamp(os.path.getmtime(orders[-1])).strftime("%m-%d %H:%M:%S") if orders else "-"))

# --- 2. evolution-ledger mtime + @BigStream unexecuted rows ---
LED = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
if os.path.exists(LED):
    m = os.path.getmtime(LED)
    p("ledger_mtime: %s" % datetime.datetime.fromtimestamp(m).strftime("%Y-%m-%d %H:%M:%S"))
    txt = open(LED, encoding="utf-8", errors="replace").read()
    pats = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
    total = 0
    for pat in pats:
        rows = [ln for ln in txt.splitlines() if pat in ln]
        total += len(rows)
        p("  ledger %s rows: %d" % (pat, len(rows)))
    p("ledger_total_at_rows: %d" % total)
else:
    p("ledger MISSING")

# --- 3. decisions.md dnum content-addressed diff vs watermark ---
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
st = json.load(open("src/os/state.json", encoding="utf-8"))
wm = st.get("decisions_watermark", {})
prev = set(wm.get("dnums", [])) if isinstance(wm, dict) else set()
if os.path.exists(DEC):
    m = os.path.getmtime(DEC)
    p("decisions_mtime: %s" % datetime.datetime.fromtimestamp(m).strftime("%Y-%m-%d %H:%M:%S"))
    dtxt = open(DEC, encoding="utf-8", errors="replace").read()
    cur = set(re.findall(r"[DC]-\d{8}-\d{2}", dtxt))
    p("decisions_dnum_set: %d | watermark: %d" % (len(cur), len(prev)))
    new = sorted(cur - prev)
    p("NEW_DNUMS: %s" % (new if new else "NONE"))
    lines = dtxt.splitlines()
    for i, ln in enumerate(lines):
        if "派工通告板" in ln:
            p("--- 派工通告板 head ---")
            for j in range(i, min(i + 8, len(lines))):
                p("  " + lines[j][:120])
            break
else:
    p("decisions MISSING")

# --- 4. tree state + index.lock ---
p("index_lock: %s" % os.path.exists(".git/index.lock"))

# --- 5. daily brief for today (10-02) present? + CENSUS supply anchor + OH w3 window file ---
p("daily_brief_1002: %s" % os.path.exists("data/intel/daily/2026-10-02.md"))
p("census_C00030: %s" % os.path.exists(r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md"))
p("oh_20261002: %s" % os.path.exists(r"C:\Users\sjs20\Desktop\FluxGroup\cph4\oss-harvest\OH-20261002-bigstream.md"))
p("production: %s | tick: %s" % (st.get("production"), st.get("tick")))

# --- 6. three probes (board / readiness / loop_health summary) ---
def probe(path, name):
    try:
        r = subprocess.run([sys.executable, path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
        txt = r.stdout.decode("utf-8", errors="replace")
        p("--- probe %s (rc=%s) ---" % (name, r.returncode))
        keep = [ln for ln in txt.splitlines() if re.search(r"FAIL|BLOCK|阻塞|PASS|OK|WARN|ideas|drafts|production|发现", ln)]
        p("\n".join(keep[-14:]) if keep else txt[-800:])
    except Exception as e:
        p("probe %s ERROR: %r" % (name, e))

probe("src/board_check.py", "board")
probe("src/readiness.py", "readiness")
probe("src/os/loop_health.py", "loop_health")

out = "\n".join(OUT)
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "r998_scan.txt"), "w", encoding="utf-8").write(out)
print(out[-1500:])
