import json, re, os, subprocess, glob

root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
hq = r"C:\Users\sjs20\Desktop\FluxGroup"
out = []

# 1) state.json head fields + last log lines
with open(os.path.join(root, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)

out.append("== state head ==")
for k in st:
    if k not in ("log",):
        v = st[k]
        if isinstance(v, (list, dict)):
            if k == "decisions_watermark" and isinstance(v, dict):
                dnums = v.get("dnums", [])
                out.append("decisions_watermark: dnums=%d last=%s" % (len(dnums), sorted(dnums)[-4:]))
                for kk, vv in v.items():
                    if kk != "dnums":
                        out.append("  wm.%s=%s" % (kk, vv))
            else:
                out.append("%s: <%s len=%d>" % (k, type(v).__name__, len(v)))
        else:
            out.append("%s=%s" % (k, v))

logs = st.get("log", [])
out.append("log_total=%d" % len(logs))
for line in logs[-3:]:
    out.append("LOGTAIL: " + line[:2000])

# 2) git status + log
for cmd in (["git", "status", "--short"], ["git", "log", "--oneline", "-3"]):
    p = subprocess.run(cmd, cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out.append("== %s ==" % " ".join(cmd))
    out.append(p.stdout.strip()[:1500])
    if p.stderr.strip():
        out.append("ERR: " + p.stderr.strip()[:300])

# 3) orders latest
files = glob.glob(os.path.join(root, "orders", "*"))
files.sort(key=os.path.getmtime, reverse=True)
out.append("== orders latest ==")
for fp in files[:4]:
    out.append("%s mtime=%s" % (os.path.basename(fp), os.path.getmtime(fp)))

# 4) evolution-ledger scan
ledger = os.path.join(hq, "cph4", "evolution-ledger.md")
try:
    with open(ledger, encoding="utf-8") as f:
        ltext = f.read()
    pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线全量|八线)")
    hits = [ln for ln in ltext.splitlines() if pat.search(ln)]
    out.append("== ledger scan ==")
    out.append("at_lines=%d" % len(hits))
    for ln in hits[-6:]:
        out.append("LEDGER: " + ln.strip()[:400])
except Exception as e:
    out.append("ledger error: %s" % e)

# 5) decisions.md D/C numbers vs watermark
dec = os.path.join(hq, "docs", "decisions.md")
try:
    with open(dec, encoding="utf-8") as f:
        dtext = f.read()
    dnums = set(re.findall(r"[DC]-20\d{6}-\d{2}", dtext))
    wm_d = set(st.get("decisions_watermark", {}).get("dnums", []))
    new = sorted(dnums - wm_d)
    out.append("== decisions scan ==")
    out.append("file_count=%d watermark_count=%d new_count=%d" % (len(dnums), len(wm_d), len(new)))
    out.append("NEW: %s" % new)
    # top dispatch board lines
    lines = dtext.splitlines()
    out.append("decisions_head:")
    for ln in lines[:12]:
        if ln.strip():
            out.append("DH: " + ln.strip()[:200])
except Exception as e:
    out.append("decisions error: %s" % e)

with open(os.path.join(root, ".c3-tmp", "r910_open_out.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("written %d lines" % len(out))
