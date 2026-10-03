import json, os, re, glob, io, datetime

BS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
FG = r"C:\Users\sjs20\Desktop\FluxGroup"
out = []
def w(s):
    out.append(s)

# 1. orders dir top by mtime
files = glob.glob(os.path.join(BS, "orders", "*.md"))
files.sort(key=os.path.getmtime)
top = files[-1]
w("orders_top=%s mtime=%s" % (os.path.basename(top), datetime.datetime.fromtimestamp(os.path.getmtime(top)).strftime("%Y-%m-%d %H:%M:%S")))

# 2. group file mtimes
for nm, p in [("group_orders", os.path.join(FG, "docs", "orders.md")),
              ("group_decisions", os.path.join(FG, "docs", "decisions.md")),
              ("group_ledger", os.path.join(FG, "cph4", "evolution-ledger.md"))]:
    w("%s_mtime=%s" % (nm, datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")))

# 3. ledger strict @ target lines count
pat = re.compile(u"@BigStream|@\u4e03\u7ebf\u5168\u53f8|@\u5168\u53f8|@\u516d\u53f8|@\u516b\u7ebf\u5168\u91cf")
hits = []
with io.open(os.path.join(FG, "cph4", "evolution-ledger.md"), encoding="utf-8", errors="replace") as f:
    for i, ln in enumerate(f, 1):
        if pat.search(ln):
            hits.append(i)
w("ledger_at_hits=%d (baseline 41)" % len(hits))

# 4. decisions dnum content-address diff vs watermark (NN canonical)
st = json.load(io.open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8"))
wm = set(st.get("decisions_watermark", {}).get("dnums", []))
dn = set()
with io.open(os.path.join(FG, "docs", "decisions.md"), encoding="utf-8", errors="replace") as f:
    for ln in f:
        for m in re.findall(r"[DC]-\d{8}-\d{2}", ln):
            dn.add(m)
new = sorted(dn - wm)
w("dnums_file=%d watermark=%d NEW_DNUMS=%s" % (len(dn), len(wm), new))

# 5. state self fields
w("state_tick=%s state_ts=%s" % (st.get("tick"), st.get("ts")))
w("production=%s" % st.get("production"))

# 6. CENSUS anchors supply gate
anch = sorted(glob.glob(os.path.join(FG, "life", "BigLife", "census", "anchors", "C-*.md")))
w("census_anchors_count=%d last=%s" % (len(anch), os.path.basename(anch[-1]) if anch else "NONE"))

# 7. #86 supply legs fresh (pools content count + interchat lines)
try:
    pj = json.load(io.open(os.path.join(FG, "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
    n = 0
    axes = pj.get("axes", {})
    if isinstance(axes, dict):
        for ax, buckets in axes.items():
            if isinstance(buckets, dict):
                for b, lst in buckets.items():
                    if isinstance(lst, list):
                        n += len(lst)
    sp = pj.get("sprite", {})
    if isinstance(sp, dict):
        for b, lst in sp.items():
            if isinstance(lst, list):
                n += len(lst)
    w("pools_content_entries=%d (baseline 1440)" % n)
except Exception as e:
    w("pools_read_err=%r" % e)
try:
    with io.open(os.path.join(FG, "life", "BigLife", "cognition", "interchat-ledger.jsonl"), encoding="utf-8", errors="replace") as f:
        ic = sum(1 for _ in f)
    w("interchat_lines=%d (baseline 22)" % ic)
except Exception as e:
    w("interchat_read_err=%r" % e)

# 8. routine artifacts + export age + backlog/queue mtime
w("daily_20261004=%s" % os.path.exists(os.path.join(BS, "data", "intel", "daily", "2026-10-04.md")))
w("daily_20261003=%s" % os.path.exists(os.path.join(BS, "data", "intel", "daily", "2026-10-03.md")))
w("index_lock=%s" % os.path.exists(os.path.join(BS, ".git", "index.lock")))
try:
    ex = json.load(io.open(os.path.join(BS, "docs", "status-export.json"), encoding="utf-8"))
    w("export_ts=%s" % ex.get("export_ts", "MISSING"))
except Exception as e:
    w("export_read_err=%r" % e)
for nm, p in [("backlog", os.path.join(BS, "src", "os", "backlog.md")),
              ("queue", os.path.join(BS, "docs", "self-improvement-queue.md"))]:
    w("%s_mtime=%s" % (nm, datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")))
w("now=%s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

txt = "\n".join(out) + "\n"
io.open(os.path.join(BS, ".c3-tmp", "r1109_check.txt"), "w", encoding="utf-8").write(txt)
print("r1109_check written, lines=%d" % len(out))
