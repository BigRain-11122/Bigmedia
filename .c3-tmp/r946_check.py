import json, os, datetime, re

BS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
GRP = os.path.abspath(os.path.join(BS, "..", ".."))
OUT = []

def w(s):
    OUT.append(s)

def mt(p):
    return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")

# 1. orders anchor (lightweight: count + top filename + dir mtime)
od = os.path.join(BS, "orders")
ofs = sorted(f for f in os.listdir(od) if f.endswith(".md"))
w("orders_files=%d top=%s dir_mtime=%s" % (len(ofs), ofs[-1], mt(od)))

# 2. ledger mtime vs R928 frozen baseline (mtime-anchored carry-forward from R938 full scan)
led = os.path.join(GRP, "cph4", "evolution-ledger.md")
led_mt = mt(led)
w("ledger_mtime=%s baseline=2026-10-02 03:17:36 drift=%s" % (led_mt, "NONE" if led_mt == "2026-10-02 03:17:36" else "RESCAN-NEEDED"))

# 3. decisions mtime vs frozen baseline + fresh dnum set-diff (content-addressed)
dec = os.path.join(GRP, "docs", "decisions.md")
dec_mt = mt(dec)
w("decisions_mtime=%s baseline=2026-10-02 00:06:16 drift=%s" % (dec_mt, "NONE" if dec_mt == "2026-10-02 00:06:16" else "RESCAN-NEEDED"))
sj = json.load(open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8"))
dnums = set(sj["decisions_watermark"]["dnums"])
raw = open(dec, encoding="utf-8").read()
found = set(re.findall(r"[DC]-\d{8}-\d{2}", raw))
new = sorted(found - dnums)
w("dnum_fresh_diff=%s count_found=%d count_wm=%d" % ("NONE" if not new else "NEW:" + ",".join(new), len(found), len(dnums)))

# 4. lock / production / tick / log count
w("index_lock=%s" % os.path.exists(os.path.join(BS, ".git", "index.lock")))
w("production=%s tick=%s log_entries=%d" % (sj.get("production"), sj.get("tick"), len(sj["log"])))
assert sj.get("production") == "open", "PRODUCTION NOT OPEN - self-heal required"
assert int(sj["tick"]) == 945, "tick drift: %s" % sj["tick"]
assert len(sj["log"]) == 973, "log count drift: %d" % len(sj["log"])
assert not new, "new dnums require full-taskbook path: %s" % new

# 5. CENSUS C-00030 supply gate fresh check
ap = os.path.join(GRP, "life", "BigLife", "census", "anchors")
if os.path.isdir(ap):
    anchors = sorted(f for f in os.listdir(ap) if f.endswith(".md"))
    c30plus = [a for a in anchors if a >= "C-00030"]
    w("census_anchor_top=%s c30plus=%d dir_mtime=%s" % (anchors[-1] if anchors else "NONE", len(c30plus), mt(ap)))
    w("CENSUS_C00030_present=%s" % os.path.exists(os.path.join(ap, "C-00030.md")))
else:
    w("census_anchors_dir=MISSING path=%s" % ap)

# 6. backlog top lines
bp = os.path.join(BS, "src", "os", "backlog.md")
w("backlog_mtime=%s" % mt(bp))

# 7. routine items
w("daily_2026_10_02=%s" % os.path.exists(os.path.join(BS, "data", "intel", "daily", "2026-10-02.md")))
w("codely_mtime=%s (R767 baseline 2026-09-30 18:55:34)" % mt(os.path.join(BS, "CODELY.md")))
w("export_ts=%s" % json.load(open(os.path.join(BS, "docs", "status-export.json"), encoding="utf-8")).get("export_ts"))
w("now=%s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

outp = os.path.join(BS, ".c3-tmp", "r946_scan.txt")
open(outp, "w", encoding="utf-8").write("\n".join(OUT) + "\n")
print("\n".join(OUT))
