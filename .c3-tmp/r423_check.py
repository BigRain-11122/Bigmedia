# -*- coding: utf-8 -*-
# r423 fast-path five-check (r422_check.py pattern) + three probes
import subprocess, io, os, datetime

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(repo)
env = dict(os.environ, PYTHONUTF8="1")
L = []
def log(s):
    L.append(s); print(s)

now = datetime.datetime.now()
log("now=" + now.strftime("%Y-%m-%d %H:%M:%S"))

# 0) orders latest filename (state anchor: O-20260925-1931-HQ-C recorded R283)
od = os.path.join(repo, "orders")
ofs = sorted(x for x in os.listdir(od) if x.endswith(".md"))
log("orders_top=" + (ofs[-1] if ofs else "NONE"))
new_orders = [x for x in ofs if x > "O-20260925-1931-HQ-C.md"]
log("orders_new_after_anchor=%s" % (new_orders if new_orders else "none"))

# 0b) bm-a insert commits after 6e9d41f (R419 window anchor)
r = subprocess.run(["git", "log", "--oneline", "6e9d41f..HEAD"], capture_output=True, text=True, encoding="utf-8", errors="replace")
inter = [x for x in (r.stdout or "").splitlines() if x.strip()]
log("inserts_after_6e9d41f=%d" % len(inter))
if inter:
    for x in inter[:5]:
        log("insert=" + x[:100])

# 1) group ledger @-pattern count (anchor 23, tail P-20260926-03)
grp = os.path.normpath(os.path.join(repo, "..", ".."))
ledger = os.path.join(grp, "cph4", "evolution-ledger.md")
pats = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
hits = []
if os.path.exists(ledger):
    with io.open(ledger, encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if any(p in line for p in pats):
                hits.append((i, line.strip()))
log("ledger_at_count=%d (anchor=23)" % len(hits))
if hits:
    log("ledger_tail=" + hits[-1][1][:90])
    log("ledger_new_after_anchor=%s" % (len(hits) > 23))

# 2) group decisions non-empty line count (anchor 40, tail D-20260926-11)
dec = os.path.join(grp, "docs", "decisions.md")
nz = []
if os.path.exists(dec):
    with io.open(dec, encoding="utf-8", errors="replace") as f:
        nz = [l.strip() for l in f if l.strip()]
log("decisions_nz_count=%d (anchor=40)" % len(nz))
if nz:
    log("decisions_tail=" + nz[-1][:90])

# 3) anchors C-00030/C-00031 (supply gate for #63)
for cid in ["C-00030", "C-00031"]:
    p = os.path.join(grp, "life", "BigLife", "census", "anchors", cid + ".md")
    log("anchor_%s=%s" % (cid, os.path.exists(p)))
ap = os.path.join(grp, "life", "BigLife", "census", "anchors")
if os.path.exists(ap):
    tail = sorted(x for x in os.listdir(ap) if x.endswith(".md"))[-3:]
    log("anchors_tail3=" + ",".join(tail))

# 4) daily brief today (2026-09-26) - must exist, do not regen
db = os.path.join(repo, "data", "intel", "daily", "2026-09-26.md")
log("daily_brief_0926=%s" % os.path.exists(db))

# 5) storylines walk (novel/audio/comic) - new writes today = ch.5 v3 drop signal (bm-a)
today = now.strftime("%Y-%m-%d")
for sub in ["novel", "audio", "comic"]:
    d = os.path.join(repo, "data", "storylines", sub)
    n = 0
    if os.path.isdir(d):
        for root, dirs, files in os.walk(d):
            for fn in files:
                fp = os.path.join(root, fn)
                try:
                    mt = datetime.date.fromtimestamp(os.path.getmtime(fp)).isoformat()
                except OSError:
                    continue
                if mt >= today:
                    n += 1
    log("storylines_%s_today_writes=%d" % (sub, n))

# 6) index.lock
lock = os.path.join(repo, ".git", "index.lock")
log("index_lock=%s" % os.path.exists(lock))

# 7) HEAD
r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
log("HEAD=" + (r.stdout.strip() or r.stderr.strip()))

# 8) three probes (board/readiness/loop_health) - never skipped
out_path = os.path.join(repo, ".c3-tmp", "r423_probe.txt")
out = io.open(out_path, "w", encoding="utf-8")
for name, cmd in [
    ("board", ["python", "src/board_check.py"]),
    ("readiness", ["python", "src/readiness.py"]),
    ("loop_health", ["python", "src/os/loop_health.py"]),
]:
    rr = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    out.write("=== %s exit=%d ===\n" % (name, rr.returncode))
    out.write(rr.stdout or "")
    if rr.stderr:
        out.write("[stderr]\n" + rr.stderr)
    out.write("\n")
    log("%s_exit=%d" % (name, rr.returncode))
out.close()
log("probe_file=%s" % out_path)

with io.open(os.path.join(repo, ".c3-tmp", "r423_check.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("check_file=.c3-tmp/r423_check.txt")
