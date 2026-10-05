import json, re, io, os, glob, datetime

base = r"C:\Users\sjs20\Desktop\FluxGroup"
repo = base + r"\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1367_check.txt", "w", encoding="utf-8")
w = out.write

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
w("NOW: " + now + "\n\n")

st = json.load(io.open(repo + r"\src\os\state.json", encoding="utf-8"))
w("tick=%s ts=%s production=%s\n" % (st.get("tick"), st.get("ts"), st.get("production")))
w("task=%s\n" % str(st.get("task"))[:200])
dw = st.get("decisions_watermark", {}) or {}
dnums = dw.get("dnums", []) or []
w("dnums_count=%s last6=%s\n" % (len(dnums), dnums[-6:]))
for k in dw:
    if k != "dnums":
        w("dw.%s=%s\n" % (k, dw[k]))
log = st.get("log", []) or []
w("log_count=%s\n\n== LOG TAIL 1 ==\n" % len(log))
for line in log[-1:]:
    w("LOG| " + line[:500] + "\n\n")

# orders top
for p in sorted(glob.glob(repo + r"\orders\*"), key=os.path.getmtime, reverse=True)[:3]:
    w("ORD| %s mtime=%s\n" % (os.path.basename(p), datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M")))

# decisions.md content-addressed diff
dec = io.open(base + r"\docs\decisions.md", encoding="utf-8").read()
w("decisions_mtime=%s\n" % datetime.datetime.fromtimestamp(os.path.getmtime(base + r"\docs\decisions.md")).strftime("%m-%d %H:%M:%S"))
ds = sorted(set(re.findall(r"[DC]-\d{8}-\d{1,2}", dec)))
new = [d for d in ds if d not in set(dnums)]
gone = [d for d in dnums if d not in set(ds)]
w("decisions_set=%s new_vs_watermark=%s gone=%s\n" % (len(ds), new, gone))

# ledger scan for BS/all-company tags + tail
led = io.open(base + r"\cph4\evolution-ledger.md", encoding="utf-8").read()
llines = led.split("\n")
tags = [l for l in llines if re.search(r"@(BigStream|七线全司|全司|六司|八线)", l)]
w("ledger_tag_lines=%s\n" % len(tags))
for l in tags[-2:]:
    w("LED| L%s %s\n" % (llines.index(l) + 1, l[:200]))
w("== ledger tail 4 ==\n")
for l in llines[-4:]:
    w("T| " + l[:200] + "\n")

# supply-gate anchor check C-00030
for p in [base + r"\life\BigLife\census\anchors\C-00030.md",
          base + r"\life\BigLife\census\anchors\C-00031.md"]:
    w("anchor %s exists=%s\n" % (os.path.basename(p), os.path.exists(p)))

# index.lock / tree quick
w("index_lock=%s\n" % os.path.exists(repo + r"\.git\index.lock"))
w("oh_w4=%s\n" % os.path.exists(base + r"\cph4\oss-harvest\OH-20261005-bigstream.md"))
w("daily1005=%s daily1006=%s\n" % (os.path.exists(repo + r"\data\intel\daily\2026-10-05.md"), os.path.exists(repo + r"\data\intel\daily\2026-10-06.md")))

# dusk standby unlock row (DAILY v68 candidate) containment check in BigLife pools
# true path = cognition/pools.json (codex path = known pseudo-diff, kept for evidence)
pp = base + r"\life\BigLife\cognition\pools.json"
if os.path.exists(pp):
    raw = io.open(pp, encoding="utf-8").read()
    w("cognition_pools_exists=True dusk_standby_row_dusk13=%s\n" % ("修了这么多伞" in raw))
    w("cognition_pools_mtime=%s\n" % datetime.datetime.fromtimestamp(os.path.getmtime(pp)).strftime("%m-%d %H:%M"))
    import json as _j
    try:
        pj = _j.loads(raw)
        w("cognition_pools_TOTAL_LINES=%s\n" % (pj.get("TOTAL_LINES") or pj.get("total_lines") or sum(len(v) for v in pj.values() if isinstance(v, list))))
    except Exception as e:
        w("cognition_pools_TOTAL_LINES=PARSE_ERR:%s\n" % type(e).__name__)
else:
    w("cognition_pools MISSING\n")
w("codex_pools_exists=%s (known pseudo-diff path R1364/R1365)\n" % os.path.exists(base + r"\life\BigLife\codex\pools.json"))

# interchat ledger count
ic = base + r"\life\BigLife\cognition\interchat-ledger.jsonl"
if os.path.exists(ic):
    w("interchat_mtime=%s\n" % datetime.datetime.fromtimestamp(os.path.getmtime(ic)).strftime("%m-%d %H:%M"))
else:
    w("interchat=ABSENT\n")

# E4 backfill evidence (20261005 verdicts on disk)
ev = sorted(glob.glob(repo + r"\expert-verdicts\*20261005*"))
w("e4_verdicts_1005=%s\n" % [os.path.basename(p) for p in ev])

# export freshness
exp = json.load(io.open(repo + r"\docs\status-export.json", encoding="utf-8"))
w("export_ts=%s\n" % exp.get("export_ts"))
live = exp.get("live") or {}
w("live3=%s\n" % json.dumps(live, ensure_ascii=False)[:400] if live else "live3=ABSENT")

out.close()
print("ok")
