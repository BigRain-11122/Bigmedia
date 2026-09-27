import os, json, datetime

R = r"C:\Users\sjs20\Desktop\FluxGroup"
B = os.path.join(R, "media", "BigStream")
out = []

def w(s):
    out.append(s)

# 1. ledger five-mode count + mtime
led = os.path.join(R, "cph4", "evolution-ledger.md")
modes = ["@BigStream", "@\u4e03\u7ebf\u5168\u53f8", "@\u5168\u53f8", "@\u516d\u53f8", "@\u516b\u7ebf\u5168\u91cf"]
with open(led, encoding="utf-8", errors="replace") as f:
    lines = f.read().splitlines()
cnt = 0
for ln in lines:
    if any(m in ln for m in modes):
        cnt += 1
w("LEDGER_MTIME " + datetime.datetime.fromtimestamp(os.path.getmtime(led)).strftime("%Y-%m-%d %H:%M:%S"))
w("LEDGER_FIVEMODE " + str(cnt))
w("LEDGER_TAILTS " + (lines[-1][:60] if lines else "EMPTY"))

# 2. decisions non-empty UTF8 lines + mtime
dec = os.path.join(R, "docs", "decisions.md")
with open(dec, encoding="utf-8", errors="replace") as f:
    dl = [l for l in f.read().splitlines() if l.strip()]
w("DECISIONS_MTIME " + datetime.datetime.fromtimestamp(os.path.getmtime(dec)).strftime("%Y-%m-%d %H:%M:%S"))
w("DECISIONS_NONEMPTY " + str(len(dl)))

# 3. state production + tick
st = os.path.join(B, "src", "os", "state.json")
with open(st, encoding="utf-8") as f:
    s = json.load(f)
w("STATE_PRODUCTION " + str(s.get("production")))
w("TICK " + str(s.get("tick")))

# 4. daily brief 09-28
db = os.path.join(B, "data", "intel", "daily", "2026-09-28.md")
w("DAILY_0928 " + str(os.path.exists(db)))

# 5. W40 self-audit
au = os.path.join(B, "docs", "audits", "2026-W40-self-audit.md")
w("AUDIT_W40 " + str(os.path.exists(au)))

# 6. CENSUS anchors (canonical position only)
for cid in ("C-00030", "C-00031"):
    p = os.path.join(R, "life", "BigLife", "census", "anchors", cid + ".md")
    w("ANCHOR_" + cid + " " + str(os.path.exists(p)))

# 7. orders count + latest mtime
od = os.path.join(B, "orders")
files = [os.path.join(od, x) for x in os.listdir(od)]
latest = max(files, key=os.path.getmtime)
w("ORDERS_COUNT " + str(len(files)))
w("ORDERS_LATEST " + os.path.basename(latest) + " " + datetime.datetime.fromtimestamp(os.path.getmtime(latest)).strftime("%Y-%m-%d %H:%M:%S"))

# 8. index.lock
w("LOCK " + str(os.path.exists(os.path.join(B, ".git", "index.lock"))))

# 9. #78 footage gate: latest file in footage dir
ft = os.path.join(B, "data", "sources", "footage")
if os.path.isdir(ft):
    ff = [os.path.join(ft, x) for x in os.listdir(ft) if os.path.isfile(os.path.join(ft, x))]
    if ff:
        lf = max(ff, key=os.path.getmtime)
        w("FOOTAGE_TOP " + os.path.basename(lf) + " " + datetime.datetime.fromtimestamp(os.path.getmtime(lf)).strftime("%Y-%m-%d %H:%M:%S"))

# 10. now
w("NOW " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

with open(os.path.join(B, ".c3-tmp", "r575_check.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("OK " + str(len(out)) + " lines")
