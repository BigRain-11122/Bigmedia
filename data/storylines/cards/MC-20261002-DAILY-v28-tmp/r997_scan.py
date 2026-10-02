# R997 quick-path five-check scan (fresh re-verify, zero-token probes)
# encoding: utf-8
import json, io, os, re, sys, glob, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
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
    # 派工通告板 block head (top 8 lines of the block)
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

# --- 5. daily brief for today (10-02) present? ---
p("daily_brief_1002: %s" % os.path.exists("data/intel/daily/2026-10-02.md"))

p("")
print("\n".join(OUT))
