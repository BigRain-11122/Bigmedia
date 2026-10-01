import json, os, datetime

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

# 2. ledger mtime vs R928 frozen baseline
led = os.path.join(GRP, "cph4", "evolution-ledger.md")
led_mt = mt(led)
w("ledger_mtime=%s baseline=2026-10-02 03:17:36 drift=%s" % (led_mt, "NONE" if led_mt == "2026-10-02 03:17:36" else "RESCAN-NEEDED"))

# 3. decisions mtime vs frozen baseline
dec = os.path.join(GRP, "docs", "decisions.md")
dec_mt = mt(dec)
w("decisions_mtime=%s baseline=2026-10-02 00:06:16 drift=%s" % (dec_mt, "NONE" if dec_mt == "2026-10-02 00:06:16" else "RESCAN-NEEDED"))

# 4. lock / production / tick / log count
w("index_lock=%s" % os.path.exists(os.path.join(BS, ".git", "index.lock")))
sj = json.load(open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8"))
w("production=%s tick=%s log_entries=%d" % (sj.get("production"), sj.get("tick"), len(sj["log"])))
assert sj.get("production") == "open", "PRODUCTION NOT OPEN - self-heal required"
assert int(sj["tick"]) == 939, "tick drift: %s" % sj["tick"]
assert len(sj["log"]) == 967, "log count drift: %d" % len(sj["log"])

# 5. routine items
w("daily_2026_10_02=%s" % os.path.exists(os.path.join(BS, "data", "intel", "daily", "2026-10-02.md")))
w("codely_mtime=%s (R767 baseline 2026-09-30 18:55:34)" % mt(os.path.join(BS, "CODELY.md")))
w("export_ts=%s" % json.load(open(os.path.join(BS, "docs", "status-export.json"), encoding="utf-8")).get("export_ts"))
w("now=%s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

outp = os.path.join(BS, ".c3-tmp", "r940_scan.txt")
open(outp, "w", encoding="utf-8").write("\n".join(OUT) + "\n")
print("\n".join(OUT))
