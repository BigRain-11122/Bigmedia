import json, os, re, glob, datetime

BS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
GRP = os.path.abspath(os.path.join(BS, "..", ".."))
OUT = []

def w(s):
    OUT.append(s)

def mt(p):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return "ERR:" + str(e)

# 1. orders anchor
od = os.path.join(BS, "orders")
ofs = sorted(f for f in os.listdir(od) if f.endswith(".md"))
w("orders_files=%d top=%s" % (len(ofs), ofs[-1]))

# 2. ledger mtime (lightweight proof; baseline 2026-10-02 03:17:36 per R928 scan)
led = os.path.join(GRP, "cph4", "evolution-ledger.md")
w("ledger_mtime=%s baseline=2026-10-02 03:17:36" % mt(led))
if os.path.getmtime(led) > datetime.datetime(2026, 10, 2, 3, 17, 36).timestamp():
    txt = open(led, encoding="utf-8").read()
    hits = re.findall(r"@(?:BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8)", txt)
    w("ledger_drift=RESCAN strict_hits=%d" % len(hits))
else:
    w("ledger_drift=NONE_mtime_frozen")

# 3. decisions mtime + dnum content-addressed diff vs watermark
dec = os.path.join(GRP, "docs", "decisions.md")
w("decisions_mtime=%s baseline=2026-10-02 00:06:16" % mt(dec))
dtxt = open(dec, encoding="utf-8").read()
dnums = set(re.findall(r"D-\d{8}-\d+|C-\d{8}-\d+", dtxt))
sj = json.load(open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8"))
wm = set(sj.get("decisions_watermark", {}).get("dnums", []))
new = sorted(dnums - wm)
w("dnums_file=%d watermark=%d new=%s" % (len(dnums), len(wm), new if new else "NONE"))

# 4. production / lock
w("production=%s" % sj.get("production"))
w("index_lock=%s" % os.path.exists(os.path.join(BS, ".git", "index.lock")))

# 5. supply probes
# CENSUS anchors
anch = glob.glob(os.path.join(GRP, "life", "BigLife", "census", "anchors", "C-*.md"))
nums = sorted(int(re.search(r"C-(\d+)", os.path.basename(a)).group(1)) for a in anch)
w("census_anchor_top=%s c30plus=%d" % ("C-%05d" % nums[-1] if nums else "NONE", sum(1 for n in nums if n >= 30)))

# pools.json leaf count
pj = os.path.join(GRP, "life", "BigLife", "cognition", "pools.json")
w("pools_mtime=%s" % mt(pj))
raw = open(pj, encoding="utf-8").read()
w("pools_raw_lines=%d" % len(raw.splitlines()))
try:
    data = json.loads(raw)
    def leaves(x):
        if isinstance(x, str):
            return 1
        if isinstance(x, list):
            return sum(leaves(i) for i in x)
        if isinstance(x, dict):
            return sum(leaves(v) for v in x.values())
        return 0
    w("pools_json_leaves=%d baseline=1440" % leaves(data))
except Exception as e:
    w("pools_json=ERR:" + str(e))

# interchat ledger
il = os.path.join(GRP, "life", "BigLife", "cognition", "interchat-ledger.jsonl")
w("interchat_mtime=%s lines=%d baseline=22" % (mt(il), len(open(il, encoding="utf-8").read().splitlines())))

# novel ch3+ v4 / ch6
nv = sorted(glob.glob(os.path.join(BS, "data", "storylines", "novel", "SC-001-*.md")))
w("novel_files=%s" % [os.path.basename(x) for x in nv])

# daily brief today
w("daily_2026_10_02=%s" % os.path.exists(os.path.join(BS, "data", "intel", "daily", "2026-10-02.md")))

# state tail
w("state_tick=%s ts=%s" % (sj.get("tick"), sj.get("ts")))

outp = os.path.join(BS, ".c3-tmp", "r938_scan.txt")
open(outp, "w", encoding="utf-8").write("\n".join(OUT) + "\n")
print("\n".join(OUT))
