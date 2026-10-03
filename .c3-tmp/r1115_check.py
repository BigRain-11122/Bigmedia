import json, re, os, glob, subprocess, io

BM = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
out = io.StringIO()
def w(s=""):
    out.write(s + "\n")

# --- five checks (fast-path) ---
# 1) orders top + mtime
od = sorted(glob.glob(BM + r"\orders\*.md"), key=os.path.getmtime)
top = od[-1] if od else None
w("orders_top: %s mtime=%s" % (os.path.basename(top) if top else "none",
   os.path.getmtime(top) if top else "-"))
import datetime
def fts(p):
    return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")
if top: w("  mtime_h: %s" % fts(top))

# 2) group orders.md mtime + BS-relevant rows
gp = GRP + r"\docs\orders.md"
w("group_orders_mtime: %s" % fts(gp))
g = open(gp, encoding="utf-8", errors="replace").read()
bs_rows = [i+1 for i, ln in enumerate(g.splitlines()) if "@BigStream" in ln]
w("group_orders_BigStream_rows: %s" % bs_rows)

# 3) ledger strict @ target rows + mtime + last target line identity
lp = GRP + r"\cph4\evolution-ledger.md"
led = open(lp, encoding="utf-8", errors="replace").read().splitlines()
terms = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
rows = [i for i, ln in enumerate(led, 1) if any(t in ln for t in terms)]
w("ledger_target_rows: %d (frozen baseline 41) mtime=%s" % (len(rows), fts(lp)))
if rows:
    w("  last_target_row_line: %d :: %s" % (rows[-1], led[rows[-1]-1][:90].encode("ascii","replace").decode()))

# 4) decisions.md content-addressed diff (D-20260930-19 watermark law)
dp = GRP + r"\docs\decisions.md"
dec = open(dp, encoding="utf-8", errors="replace").read()
nums = set(re.findall(r"[DC]-\d{8}-\d{2}", dec))
st = json.load(open(BM + r"\src\os\state.json", encoding="utf-8"))
wm = set(st.get("decisions_watermark", {}).get("dnums", []))
w("decisions_mtime: %s" % fts(dp))
w("decisions_nums_total: %d wm: %d NEW_DNUMS: %s" % (len(nums), len(wm), sorted(nums - wm)))
# dispatch board BS rows (unacked check)
board = re.findall(r"派工通告[^\n]*", dec)
w("dispatch_board_headers: %d" % len(board))

# 5) lock / production / tick / ts
lock = BM + r"\logs\iteration-loop\round.lock"
w("index_lock_exists: %s round_lock: %s" % (os.path.exists(BM + r"\.git\index.lock"),
   open(lock).read().strip() if os.path.exists(lock) else "none"))
w("production: %s tick: %s ts: %s" % (st.get("production"), st.get("tick"), st.get("ts")))

# 6) routine items
w("daily_1003: %s  daily_1004: %s" % (
   os.path.exists(BM + r"\data\intel\daily\2026-10-03.md"),
   os.path.exists(BM + r"\data\intel\daily\2026-10-04.md")))
w("W40_audit: %s" % os.path.exists(BM + r"\docs\audits\2026-W40-self-audit.md"))
gb = open(BM + r"\docs\global-benchmarks.md", encoding="utf-8", errors="replace").read()
gd = re.findall(r"2026-\d\d-\d\d", gb)
w("GB_last_refresh: %s (gate 10-08)" % (gd[0] if gd else "?"))

# 7) #86 three supply legs (marker-free content-count law R1076)
import json as _j
pool = GRP + r"\life\BigLife\cognition\pools.json"
_pc = 0
if os.path.exists(pool):
    _d = _j.load(open(pool, encoding="utf-8"))
    def _cnt(o):
        n = 0
        if isinstance(o, dict):
            for v in o.values(): n += _cnt(v)
        elif isinstance(o, list):
            n += len(o)
        return n
    _pc = _cnt(_d)
w("pools_entry_count: %d (baseline 1440 content-count)" % _pc)
ic = glob.glob(GRP + r"\life\BigLife\cognition\interchat-ledger.jsonl")
if ic:
    w("interchat_rows: %d (baseline 22)" % sum(1 for _ in open(ic[0], encoding="utf-8", errors="replace")))
anch = sorted(glob.glob(GRP + r"\life\BigLife\census\anchors\C-*.md"))
w("CENSUS_anchors_last: %s count=%d (C-00030 gate: %s)" % (
   os.path.basename(anch[-1]) if anch else "none", len(anch),
   os.path.exists(GRP + r"\life\BigLife\census\anchors\C-00030.md")))

# 8) export_ts age
ex = json.load(open(BM + r"\docs\status-export.json", encoding="utf-8"))
w("export_ts: %s (age check vs now)" % ex.get("export_ts"))

# 9) backlog/queue mtime + git status
w("backlog_mtime: %s" % fts(BM + r"\src\os\backlog.md"))
w("queue_mtime: %s" % fts(BM + r"\docs\self-improvement-queue.md"))
gs = subprocess.run(["git", "status", "--short"], cwd=BM, capture_output=True, text=True).stdout
w("git_status: %r" % gs.strip())

open(BM + r"\.c3-tmp\r1115_check.txt", "w", encoding="utf-8").write(out.getvalue())
print(out.getvalue())
