import os, subprocess, time

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .c3-tmp -> repo root
fg = os.path.dirname(os.path.dirname(repo))  # FluxGroup root
os.chdir(repo)

def g(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout.strip()

print("git_status:", repr(g("git status --short")))
print("head:", g("git rev-parse --short HEAD"))
print("index_lock:", os.path.exists(".git/index.lock"))

pats = ["@BigStream", "@\u4e03\u7ebf\u5168\u53f8", "@\u5168\u53f8", "@\u516d\u53f8"]
ledger = os.path.join(fg, "cph4", "evolution-ledger.md")
n = 0
with open(ledger, encoding="utf-8", errors="replace") as f:
    for line in f:
        if any(p in line for p in pats):
            n += 1
print("ledger_at_lines:", n)

dec = os.path.join(fg, "docs", "decisions.md")
lines = [l for l in open(dec, encoding="utf-8", errors="replace").read().splitlines() if l.strip()]
print("decisions_nonempty:", len(lines))
print("decisions_tail:", lines[-1][:80] if lines else "EMPTY")

anchors = os.path.join(fg, "life", "BigLife", "census", "anchors")
print("anchor_C00030:", os.path.exists(os.path.join(anchors, "C-00030.md")))
print("anchor_C00031:", os.path.exists(os.path.join(anchors, "C-00031.md")))
try:
    names = sorted(os.listdir(anchors))
    print("anchors_tail:", names[-3:])
except Exception as e:
    print("anchors_err:", e)

print("daily_brief_0926:", os.path.exists(os.path.join(repo, "data", "intel", "daily", "2026-09-26.md")))
print("w39_audit:", os.path.exists(os.path.join(repo, "docs", "audits", "2026-W39-self-audit.md")))

thr = time.mktime(time.strptime("2026-09-26 00:00:00", "%Y-%m-%d %H:%M:%S"))
for sub in ["novel", "audio", "comic"]:
    d = os.path.join(repo, "data", "storylines", sub)
    cnt = 0
    if os.path.isdir(d):
        for r, ds, fs in os.walk(d):
            for fn in fs:
                try:
                    if os.path.getmtime(os.path.join(r, fn)) >= thr:
                        cnt += 1
                except OSError:
                    pass
    print("storylines_%s_new_writes_0926:" % sub, cnt)

om = os.path.join(repo, "orders")
latest = max(os.listdir(om), key=lambda f: os.path.getmtime(os.path.join(om, f)))
print("orders_latest:", latest)
