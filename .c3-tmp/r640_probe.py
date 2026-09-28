# r640 five-check + three probes (UTF-8 file output; ASCII-safe source)
import io, os, re, sys, json, subprocess, datetime

R = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
G = r"C:\Users\sjs20\Desktop\FluxGroup"
out = []

# 1. ledger five-pattern count (case-sensitive, anchor=34)
t = io.open(G + r"\cph4\evolution-ledger.md", encoding="utf-8").read()
pat = re.compile("@BigStream|@\u4e03\u7ebf\u5168\u53f8|@\u5168\u53f8|@\u516d\u53f8|@\u516b\u7ebf")
hits = [l for l in t.splitlines() if pat.search(l)]
out.append("ledger_five=%d (anchor=34)" % len(hits))
if len(hits) > 34:
    out.append("NEW_LEDGER_LINES:")
    for l in hits[34:]:
        out.append(l[:300])

# 2. decisions non-empty count (anchor=68)
d = io.open(G + r"\docs\decisions.md", encoding="utf-8").read()
dec = [l for l in d.splitlines() if l.strip()]
out.append("decisions_nonempty=%d (anchor=68)" % len(dec))
if len(dec) > 68:
    out.append("NEW_DECISION_LINES:")
    for l in dec[68:]:
        out.append(l[:300])

# 3. orders top mtime
od = os.path.join(R, "orders")
fs = sorted(os.listdir(od), key=lambda f: os.path.getmtime(os.path.join(od, f)), reverse=True)[:3]
for f in fs:
    out.append("order: %s mtime=%s" % (f, datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(od, f))).strftime("%m-%d %H:%M:%S")))

# 4. state + last log tail
s = json.load(io.open(os.path.join(R, "src", "os", "state.json"), encoding="utf-8"))
out.append("tick=%s ts=%s production=%s" % (s.get("tick"), s.get("ts"), s.get("production")))
lg = s["log"]
out.append("log_len=%d" % len(lg))
out.append("=== last log tail 1100 ===")
out.append(lg[-1][-1100:])

# 5. REACT-v4 E4 backfill status
rv4 = [(i, l) for i, l in enumerate(lg) if "REACT-v4" in l]
out.append("react_v4_log_mentions=%d" % len(rv4))
for i, l in rv4[-3:]:
    tail8 = l[-800:]
    out.append("  entry#%d first60=%s | tail_has_e4_score=%s" % (i, l[:60], ("E4" in tail8 and ("7.0" in tail8 or "8.0" in tail8 or "9.0" in tail8))))
p = os.path.join(R, "docs", "reviews", "review-20260928-mcreact-v4.md")
if os.path.exists(p):
    rt = io.open(p, encoding="utf-8").read()
    out.append("react_v4_review: len=%d has_E4=%s has_v1.1=%s" % (len(rt), ("E4" in rt), ("v1.1" in rt)))
else:
    out.append("react_v4_review: MISSING")
pe = os.path.join(R, "data", "storylines", "cards", "MC-20260928-REACT-v4-tmp", "e4-result.json")
if os.path.exists(pe):
    out.append("=== react_v4 e4-result.json (head 3500) ===")
    out.append(io.open(pe, encoding="utf-8").read()[:3500])
# expert-verdicts dir candidates
for cand in [os.path.join(R, "expert-verdicts"), os.path.join(R, "docs", "reviews", "expert-verdicts")]:
    if os.path.isdir(cand):
        names = sorted(os.listdir(cand))
        out.append("verdicts_dir=%s n=%d last4=%s" % (cand.replace(R, "."), len(names), names[-4:]))

# 6. daily brief 09-29 (REACT hot-window input)
out.append("=== daily brief 09-29 ===")
out.append(io.open(os.path.join(R, "data", "intel", "daily", "2026-09-29.md"), encoding="utf-8").read())

# 7. HEAD
try:
    gl = subprocess.run(["git", "-C", R, "log", "-1", "--oneline"], capture_output=True, text=True, encoding="utf-8", timeout=15)
    out.append("HEAD=" + (gl.stdout.strip() or gl.stderr.strip()))
except Exception as e:
    out.append("HEAD_err=%s" % e)

# 8. three probes (captured UTF-8)
for name, rel in [("board", os.path.join("src", "board_check.py")), ("readiness", os.path.join("src", "readiness.py")), ("loop_health", os.path.join("src", "os", "loop_health.py"))]:
    try:
        r2 = subprocess.run([sys.executable, rel], cwd=R, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
        out.append("=== probe %s rc=%d ===" % (name, r2.returncode))
        out.append((r2.stdout or "")[-2200:])
        if r2.stderr.strip():
            out.append("STDERR_TAIL: " + r2.stderr.strip()[-300:])
    except Exception as e:
        out.append("probe %s err=%s" % (name, e))

io.open(os.path.join(R, ".c3-tmp", "r640_probe.txt"), "w", encoding="utf-8").write("\n".join(out))
print("PROBE_OK lines=%d" % len(out))
