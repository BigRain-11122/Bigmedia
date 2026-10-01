# -*- coding: utf-8 -*-
import json, re, os, subprocess, io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
FG = r"C:\Users\sjs20\Desktop\FluxGroup"
out = io.open(os.path.join(ROOT, ".c3-tmp", "r_check.txt"), "w", encoding="utf-8")
W = out.write

p = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
W("=== GIT STATUS ===\n"); W(p.stdout or "(clean)\n")
p = subprocess.run(["git", "log", "-5", "--oneline"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
W("=== GIT LOG 5 ===\n"); W(p.stdout)

s = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
W("=== STATE HEAD ===\n")
for k in ("ts", "task", "tick"):
    W("%s=%s\n" % (k, s.get(k)))
W("production=%s\n" % json.dumps(s.get("production"), ensure_ascii=False)[:300])
wm = s.get("decisions_watermark")
W("decisions_watermark=%s\n" % json.dumps(wm, ensure_ascii=False)[:600])
log = s.get("log", [])
W("log_len=%d\n" % len(log))
W("=== STATE LOG TAIL 3 ===\n")
for line in log[-3:]:
    W(str(line)[:1800] + "\n----\n")

od = os.path.join(ROOT, "orders")
files = []
for f in os.listdir(od):
    fp = os.path.join(od, f)
    if os.path.isfile(fp):
        files.append((os.path.getmtime(fp), f))
files.sort(reverse=True)
W("=== ORDERS TOP 5 (newest) ===\n")
for t, f in files[:5]:
    W(f + "\n")

led = os.path.join(FG, "cph4", "evolution-ledger.md")
txt = io.open(led, encoding="utf-8", errors="replace").read()
at = [l for l in txt.splitlines() if "@BigStream" in l]
W("=== LEDGER @BigStream count=%d (tail 3) ===\n" % len(at))
for l in at[-3:]:
    W(l[:260] + "\n")

dec = os.path.join(FG, "docs", "decisions.md")
dtxt = io.open(dec, encoding="utf-8", errors="replace").read()
nums = set(re.findall(r"[DC]-\d{8}-\d{2}", dtxt))
wmd = set()
if isinstance(wm, dict):
    wmd = set(wm.get("dnums", []))
W("=== DECISIONS nums=%d watermark=%d new=%s ===\n" % (len(nums), len(wmd), sorted(nums - wmd)))
W("=== DECISIONS HEAD 30 lines ===\n")
for l in dtxt.splitlines()[:30]:
    W(l[:200] + "\n")

W("=== ROUTINE CHECKS ===\n")
W("daily 2026-10-01: %s\n" % os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-10-01.md")))
aud = os.path.join(ROOT, "docs", "audits")
if os.path.isdir(aud):
    af = sorted(os.listdir(aud))
    W("audits files tail 5: %s\n" % af[-5:])
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
if os.path.exists(gb):
    g = io.open(gb, encoding="utf-8", errors="replace").read().splitlines()
    upd = [l for l in g if "更新记录" in l or re.match(r"\s*20\d\d-\d\d-\d\d", l)]
    W("global-benchmarks upd lines head 3: %s\n" % [u[:80] for u in upd[:3]])
out.close()
print("done")
