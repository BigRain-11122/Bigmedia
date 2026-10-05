import json, re, io, os, glob, datetime

base = r"C:\Users\sjs20\Desktop\FluxGroup"
repo = base + r"\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1363_check.txt", "w", encoding="utf-8")
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
w("log_count=%s\n\n== LOG TAIL 3 ==\n" % len(log))
for line in log[-3:]:
    w("LOG| " + line[:700] + "\n\n")

# orders top
for p in sorted(glob.glob(repo + r"\orders\*"), key=os.path.getmtime, reverse=True)[:3]:
    w("ORD| %s mtime=%s\n" % (os.path.basename(p), datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M")))

# decisions.md content-addressed diff + dispatch board head
dec = io.open(base + r"\docs\decisions.md", encoding="utf-8").read()
ds = sorted(set(re.findall(r"[DC]-\d{8}-\d{1,2}", dec)))
new = [d for d in ds if d not in set(dnums)]
w("\ndecisions_set=%s new_vs_watermark=%s\n" % (len(ds), new))

# ledger scan for BS/all-company tags + tail
led = io.open(base + r"\cph4\evolution-ledger.md", encoding="utf-8").read()
llines = led.split("\n")
tags = [l for l in llines if re.search(r"@(BigStream|七线全司|全司|六司|八线)", l)]
w("ledger_tag_lines=%s\n" % len(tags))
for l in tags[-3:]:
    w("LED| " + l[:240] + "\n")
w("== ledger tail 6 ==\n")
for l in llines[-6:]:
    w("T| " + l[:240] + "\n")

# supply-gate anchor check C-00030
for p in [base + r"\life\BigLife\census\anchors\C-00030.md",
          base + r"\life\BigLife\census\anchors\C-00031.md"]:
    w("anchor %s exists=%s\n" % (os.path.basename(p), os.path.exists(p)))

# index.lock / tree quick
w("index_lock=%s\n" % os.path.exists(repo + r"\.git\index.lock"))
w("oh_w4=%s\n" % os.path.exists(base + r"\cph4\oss-harvest\OH-20261005-bigstream.md"))
w("daily1005=%s daily1006=%s\n" % (os.path.exists(repo + r"\data\intel\daily\2026-10-05.md"), os.path.exists(repo + r"\data\intel\daily\2026-10-06.md")))
w("pools_mtime=%s\n" % datetime.datetime.fromtimestamp(os.path.getmtime(base + r"\life\BigLife\codex\pools.json")).strftime("%m-%d %H:%M") if os.path.exists(base + r"\life\BigLife\codex\pools.json") else "NA")

out.close()
print("ok")
