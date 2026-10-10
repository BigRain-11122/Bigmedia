# -*- coding: utf-8 -*-
"""R1909 fast-path five-checks probe (compact). Evidence file, committed per tech#64 convention."""
import os, re, subprocess, time, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP = r"C:\Users\sjs20\Desktop\FluxGroup"
out = []
def w(s): out.append(s)

def mtime(p):
    try: return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(p)))
    except Exception: return "MISSING"

# 1) own orders dir top file
od = os.path.join(ROOT, "orders")
try:
    fs = sorted(os.listdir(od), key=lambda f: os.path.getmtime(os.path.join(od, f)), reverse=True)
    w("own_orders_top=%s mtime=%s" % (fs[0], mtime(os.path.join(od, fs[0]))))
except Exception as e:
    w("own_orders_err=%s" % e)

# 2) group orders mtime + tail 5
go = os.path.join(GRP, "docs", "orders.md")
w("hq_orders_mtime=%s (anchor R1907 20:15:33)" % mtime(go))
try:
    with open(go, encoding="utf-8") as f: lines = f.readlines()
    w("hq_orders_lines=%d" % len(lines))
    for ln in lines[-6:]:
        t = ln.strip()
        if t: w("  | " + t[:160])
except Exception as e:
    w("hq_orders_read_err=%s" % e)

# 3) decisions dnum content-address diff vs state watermark
st = json.load(open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
wm = set(st.get("decisions_watermark", {}).get("dnums", []))
dec = os.path.join(GRP, "docs", "decisions.md")
try:
    txt = open(dec, encoding="utf-8").read()
    cur = set(re.findall(r"\b([DC]-20\d{6}-\d{2})\b", txt))
    new = sorted(cur - wm)
    w("decisions_mtime=%s wm_size=%d cur_size=%d truly_new=%s" % (mtime(dec), len(wm), len(cur), new if new else "[]"))
except Exception as e:
    w("decisions_err=%s" % e)

# 4) ledger @BigStream lines
lg = os.path.join(GRP, "cph4", "evolution-ledger.md")
try:
    with open(lg, encoding="utf-8") as f: ll = f.readlines()
    hits = [(i+1, l.strip()[:150]) for i, l in enumerate(ll) if "@BigStream" in l]
    w("ledger_mtime=%s bigstream_lines=%d" % (mtime(lg), len(hits)))
    for i, t in hits[-4:]: w("  L%d %s" % (i, t))
except Exception as e:
    w("ledger_err=%s" % e)

# 5) git status via real git.exe + index.lock + backlog/queue mtimes
GIT = r"C:\Program Files\Git\cmd\git.exe"
try:
    r = subprocess.run([GIT, "status", "--short"], cwd=ROOT, capture_output=True)
    st_txt = r.stdout.decode("utf-8", "replace").strip()
    lines = [l for l in st_txt.splitlines() if l.strip()]
    w("git_status_entries=%d (filter ours: state.json M expected)" % len(lines))
    for l in lines[:12]: w("  g| " + l[:150])
except Exception as e:
    w("git_err=%s" % e)
lock = os.path.join(ROOT, ".git", "index.lock")
w("index_lock=%s" % ("YES" if os.path.exists(lock) else "False"))
w("backlog_mtime=%s" % mtime(os.path.join(ROOT, "src", "os", "backlog.md")))
for q in ("main.md", "tech.md", "explore.md"):
    w("queue_%s_mtime=%s" % (q.split('.')[0], mtime(os.path.join(ROOT, "state", "queue", q))))

# 6) viewing seats (R1762 dual-path law): meme outbound + krea2 30s-reel-v1
def scan_dir(p, anchor, label):
    if not os.path.isdir(p):
        w("%s=ABSENT" % label); return
    fs = []
    for dp, dn, fn in os.walk(p):
        for f in fn:
            fp = os.path.join(dp, f)
            fs.append((os.path.getmtime(fp), os.path.relpath(fp, p)))
    fs.sort()
    w("%s files=%d newest:" % (label, len(fs)))
    for t, f in fs[-6:]:
        w("  %s %s" % (time.strftime("%m-%d %H:%M:%S", time.localtime(t)), f))

MEME_ANCHOR = "2026-10-10 15:41 narration.mp3"
scan_dir(os.path.join(GRP, "cph4", "fleet", "meme-daily-v1", "outbound"), MEME_ANCHOR, "meme_outbound")
scan_dir(os.path.join(GRP, "cph4", "fleet", "mv0001-handover", "outbound", "krea2", "30s-reel-v1"), "R1907 20:03:42 DELIVERY-NOTE-v44", "krea2_30sreel")

print("\n".join(out))
