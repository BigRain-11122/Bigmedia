import json, re, io, os, glob, datetime

base = r"C:\Users\sjs20\Desktop\FluxGroup"
repo = base + r"\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1362_probe.txt", "w", encoding="utf-8")
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
w("log_count=%s\n\n== LOG TAIL 4 ==\n" % len(log))
for line in log[-4:]:
    w("LOG| " + line[:700] + "\n\n")

# decisions.md content-addressed diff + dispatch board head
dec = io.open(base + r"\docs\decisions.md", encoding="utf-8").read()
ds = sorted(set(re.findall(r"[DC]-\d{8}-\d{1,2}", dec)))
new = [d for d in ds if d not in set(dnums)]
w("decisions_set=%s new_vs_watermark=%s\n\n" % (len(ds), new))
w("== decisions.md head 40 ==\n")
for l in dec.split("\n")[:40]:
    w(l[:200] + "\n")

# ledger scan for BS/all-company tags + tail
led = io.open(base + r"\cph4\evolution-ledger.md", encoding="utf-8").read()
llines = led.split("\n")
tags = [l for l in llines if re.search(r"@(BigStream|七线全司|全司|六司|八线)", l)]
w("\nledger_tag_lines=%s\n" % len(tags))
for l in tags[-5:]:
    w("LED| " + l[:240] + "\n")
w("\n== ledger tail 12 ==\n")
for l in llines[-12:]:
    w("T| " + l[:240] + "\n")

# supply-gate anchor check C-00030
for p in [base + r"\life\BigLife\census\anchors\C-00030.md",
          base + r"\life\BigLife\census\anchors\C-00031.md"]:
    w("\nanchor %s exists=%s" % (os.path.basename(p), os.path.exists(p)))

# today's expert verdicts / e4 results (backfill candidates)
w("\n\n== expert-verdicts 2026-10-05 ==\n")
for p in sorted(glob.glob(repo + r"\docs\reviews\expert-verdicts\20261005*"))[-8:]:
    w("EV| " + os.path.basename(p) + "\n")
for pat in [r"\.c3-tmp\*e4*", r"\.*tmp*\**e4*"]:
    for p in sorted(glob.glob(repo + pat))[-6:]:
        w("E4F| " + p.replace(repo, "") + " mtime=" + datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M") + "\n")

out.close()
print("ok")
