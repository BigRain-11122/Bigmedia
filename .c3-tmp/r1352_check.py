import json, re, io, sys, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GROUP = r"C:\Users\sjs20\Desktop\FluxGroup"
out = io.StringIO()

def w(s=""):
    out.write(str(s) + "\n")

# 1) state.json essentials
with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
w("== state.json ==")
w("tick=%s" % st.get("tick"))
w("ts=%s" % st.get("ts"))
w("task=%s" % st.get("task"))
w("production=%s" % st.get("production"))
wm = st.get("decisions_watermark") or {}
w("watermark.dnums_count=%s" % len(wm.get("dnums", [])))
log = st.get("log", [])
w("log_len=%d" % len(log))
for e in log[-2:]:
    w("LOG| " + json.dumps(e, ensure_ascii=True))

# 2) group decisions.md content-addressed scan
try:
    with open(os.path.join(GROUP, "docs", "decisions.md"), encoding="utf-8") as f:
        dtext = f.read()
    dnums = sorted(set(re.findall(r"[DC]-\d{8}-\d{2}", dtext)))
    state_dnums = set(wm.get("dnums", []))
    new_dnums = sorted(set(dnums) - state_dnums)
    w("== decisions.md ==")
    w("dnum_count=%d" % len(dnums))
    w("NEW=%s" % json.dumps(new_dnums, ensure_ascii=True))
    import datetime
    w("mtime=%s" % datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(GROUP, "docs", "decisions.md"))).strftime("%Y-%m-%d %H:%M:%S"))
    w("-- head 12 lines (dispatch board zone) --")
    for i, ln in enumerate(dtext.splitlines()[:12]):
        w("D%02d| %s" % (i, ln))
except Exception as ex:
    w("decisions.md ERROR %r" % ex)

# 3) evolution-ledger @BigStream scan (canonical strict-prefix)
try:
    lp = os.path.join(GROUP, "cph4", "evolution-ledger.md")
    with open(lp, encoding="utf-8") as f:
        llines = f.readlines()
    w("== evolution-ledger ==")
    w("total_lines=%d" % len(llines))
    raw = [(i + 1, ln.rstrip()) for i, ln in enumerate(llines)
           if re.search(r"@BigStream|@Bigstream|@七线全司|@全司|@六司", ln)]
    canon = [(i, ln) for i, ln in raw if re.search(r"@BigStream|@Bigstream|@七线全司|@全司|@六司", ln)]
    w("raw_hits=%d" % len(raw))
    for i, ln in raw[-5:]:
        w("L%d| %s" % (i, ln[:200]))
except Exception as ex:
    w("ledger ERROR %r" % ex)

# 4) orders dir top files + index.lock + git status + last commit
try:
    od = os.path.join(ROOT, "orders")
    files = sorted(
        [(f, os.path.getmtime(os.path.join(od, f))) for f in os.listdir(od)],
        key=lambda x: -x[1])[:4]
    import datetime
    w("== orders/ top ==")
    for f, m in files:
        w("%s mtime=%s" % (f, datetime.datetime.fromtimestamp(m).strftime("%m-%d %H:%M")))
except Exception as ex:
    w("orders dir ERROR %r" % ex)

w("index.lock exists=%s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

import subprocess
g = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
w("== git status ==")
w((g.stdout or "").strip()[:2000])
c = subprocess.run(["git", "log", "--oneline", "-1"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
w("LAST_COMMIT| " + (c.stdout or "").strip())

with open(os.path.join(ROOT, ".c3-tmp", "r1352_check.txt"), "w", encoding="utf-8") as f:
    f.write(out.getvalue())
print("written r1352_check.txt")
