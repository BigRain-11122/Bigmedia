# -*- coding: ascii -*-
# R1422 quick-path five-check probe (ASCII only per encoding law)
import json, os, re, subprocess, io, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
out = io.StringIO()

def w(s=""):
    out.write(s + "\n")

# 1) git status short + index.lock
try:
    g = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    w("GIT_STATUS_SHORT_BEGIN")
    w(g.stdout.strip() if g.stdout.strip() else "(clean)")
    w("GIT_STATUS_SHORT_END")
except Exception as e:
    w("GIT_STATUS_ERR: %s" % e)
lock = os.path.join(ROOT, ".git", "index.lock")
w("INDEX_LOCK: %s" % ("EXISTS" if os.path.exists(lock) else "none"))

# last commit
try:
    lg = subprocess.run(["git", "log", "-1", "--oneline"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    w("LAST_COMMIT: %s" % lg.stdout.strip())
except Exception as e:
    w("GIT_LOG_ERR: %s" % e)

# 2) state.json fields
try:
    with io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8") as f:
        st = json.load(f)
    w("STATE_TICK: %s" % st.get("tick"))
    w("STATE_TS: %s" % st.get("ts"))
    w("STATE_TASK: %s" % (st.get("task") or "")[:80])
    w("PRODUCTION: %s" % st.get("production"))
    wm = st.get("decisions_watermark", {})
    dn = wm.get("dnums", []) if isinstance(wm, dict) else []
    w("WATERMARK_DNUMS_COUNT: %s" % len(dn))
except Exception as e:
    w("STATE_ERR: %s" % e)

# 3) orders/ latest file (by name prefix date sorting)
odir = os.path.join(ROOT, "orders")
try:
    names = [n for n in os.listdir(odir) if n.lower().endswith(".md")]
    names.sort(reverse=True)
    w("ORDERS_TOP3: %s" % names[:3])
    if names:
        p = os.path.join(odir, names[0])
        w("ORDERS_TOP_MTIME: %s" % os.path.getmtime(p))
except Exception as e:
    w("ORDERS_ERR: %s" % e)

# 4) group ledger strict @BigStream scan (five modes)
led = os.path.join(GRP, "cph4", "evolution-ledger.md")
try:
    with io.open(led, "r", encoding="utf-8", errors="replace") as f:
        txt = f.read()
    pat = re.compile(r"@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf\u5168\u91cf)")
    hits = pat.findall(txt)
    w("LEDGER_TAGS_TOTAL: %s" % len(hits))
    from collections import Counter
    w("LEDGER_TAGS_BREAKDOWN: %s" % dict(Counter(hits)))
    w("LEDGER_MTIME: %s" % os.path.getmtime(led))
    # tail 5 lines
    tl = [l for l in txt.splitlines() if l.strip()][-5:]
    w("LEDGER_TAIL5:")
    for l in tl:
        w("  | " + l[:150])
except Exception as e:
    w("LEDGER_ERR: %s" % e)

# 5) decisions.md dnum set diff vs watermark (content-addressed, D-20260930-19)
dec = os.path.join(GRP, "docs", "decisions.md")
try:
    with io.open(dec, "r", encoding="utf-8", errors="replace") as f:
        dtxt = f.read()
    cur = set(re.findall(r"[DC]-\d{8}-\d{2}", dtxt))
    w("DECISIONS_CUR_SET_COUNT: %s" % len(cur))
    w("DECISIONS_MTIME: %s" % os.path.getmtime(dec))
    prev = set(dn) if dn else set()
    new = sorted(cur - prev)
    gone = sorted(prev - cur)
    w("DECISIONS_NEW: %s" % new)
    w("DECISIONS_GONE: %s" % gone)
except Exception as e:
    w("DECISIONS_ERR: %s" % e)

# 6) daily brief for 10-06 (already produced by R1420?)
d6 = os.path.join(ROOT, "data", "intel", "daily", "2026-10-06.md")
w("DAILY_1006: %s" % ("EXISTS" if os.path.exists(d6) else "MISSING"))
# backlog/queue mtime
for nm, p in [("backlog", os.path.join(ROOT, "src", "os", "backlog.md")),
              ("queue", os.path.join(ROOT, "docs", "self-improvement-queue.md")),
              ("export", os.path.join(ROOT, "docs", "status-export.json"))]:
    w("%s_MTIME: %s" % (nm.upper(), os.path.getmtime(p) if os.path.exists(p) else "MISSING"))

with io.open(os.path.join(ROOT, "r_cur_check5_out.txt"), "w", encoding="utf-8") as f:
    f.write(out.getvalue())
print(out.getvalue())
