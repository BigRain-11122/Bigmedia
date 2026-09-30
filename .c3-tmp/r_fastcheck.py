import json, os, subprocess, glob, io, time, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []
now = time.time()
out.append("NOW = %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)))

# 1. state.json header + tail logs
st_path = os.path.join(ROOT, "src", "os", "state.json")
with open(st_path, encoding="utf-8") as f:
    st = json.load(f)
out.append("== STATE HEADER ==")
for k in ("tick", "ts", "task", "production"):
    out.append("%s = %s" % (k, st.get(k, "<missing>")))
logs = st.get("log", [])
out.append("log_count = %d" % len(logs))
out.append("== LAST 3 LOGS ==")
for e in logs[-3:]:
    out.append(e[:1700])
    out.append("-----8<-----")

# 2. orders latest 4 by mtime
od = os.path.join(ROOT, "orders")
ents = []
for fn in os.listdir(od):
    p = os.path.join(od, fn)
    if os.path.isfile(p):
        ents.append((os.path.getmtime(p), fn))
ents.sort(reverse=True)
out.append("== ORDERS LATEST ==")
for mt, fn in ents[:4]:
    out.append("%s %s" % (time.strftime("%m-%d %H:%M", time.localtime(mt)), fn))

# 3. git status
r = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
out.append("== GIT STATUS ==")
out.append(r.stdout.rstrip() if r.stdout.strip() else "(clean)")
out.append("index_lock = %s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))

# 4. ledger scan (BigStream-tagged rows)
led = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
cnt = 0
last_hits = []
if os.path.exists(led):
    with open(led, encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if "@BigStream" in line:
                cnt += 1
                last_hits.append((i, line.rstrip()[:200]))
out.append("== LEDGER @BigStream substring lines: %d (last anchor=32) ==" % cnt)
for i, l in last_hits[-3:]:
    out.append("L%d: %s" % (i, l))

# 5. decisions non-empty count
dec = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
if os.path.exists(dec):
    with open(dec, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    ne = [l for l in lines if l.strip()]
    out.append("== DECISIONS non-empty lines: %d ==" % len(ne))
    out.append("last: " + ne[-1][:160])

# 6. E4 result probes (last 24h)
out.append("== E4 RESULT PROBES (mtime>=24h) ==")
hits = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    if ".git" in dirpath:
        continue
    for fn in filenames:
        if "e4-result" in fn:
            p = os.path.join(dirpath, fn)
            mt = os.path.getmtime(p)
            if mt >= now - 86400:
                hits.append((mt, p))
for mt, p in sorted(hits):
    out.append("%s %s" % (time.strftime("%m-%d %H:%M:%S", time.localtime(mt)), os.path.relpath(p, ROOT)))

# 7. CENSUS supply gate: anchors
anc = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors"
if os.path.exists(anc):
    names = sorted(os.listdir(anc))
    out.append("== ANCHORS top5: %s (C-00030 exists=%s) ==" % (names[-5:], ("C-00030.md" in names)))

# 8. audits dir (W40 check)
ad = os.path.join(ROOT, "docs", "audits")
out.append("== AUDITS == " + ", ".join(sorted(os.listdir(ad))[-6:]))

# 9. daily brief today
out.append("daily_brief_2026-09-29 = %s" % os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-29.md")))

# 10. global benchmarks update-log head
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
if os.path.exists(gb):
    with open(gb, encoding="utf-8") as f:
        gtxt = f.read()
    idx = gtxt.find("更新记录")
    seg = gtxt[idx:idx + 260] if idx >= 0 else "(no section)"
    out.append("== GB 更新记录 head == " + seg.replace("\n", " | ")[:240])

# 11. suspended processes
try:
    r2 = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"], capture_output=True, text=True)
    py = [l.split('","')[0].strip('"') + " " + l.split('","')[1].strip('"') if '","' in l else l for l in r2.stdout.splitlines()[3:]]
    out.append("== PYTHON PROCS == " + " | ".join(py[:8]))
    r3 = subprocess.run(["tasklist", "/FI", "IMAGENAME eq ollama.exe", "/FO", "CSV"], capture_output=True, text=True)
    ol = [l for l in r3.stdout.splitlines()[3:]]
    out.append("== OLLAMA PROCS == " + " | ".join(ol[:4]))
except Exception as ex:
    out.append("tasklist err: %s" % ex)

# 12. self-improvement queue head
sq = os.path.join(ROOT, "docs", "self-improvement-queue.md")
if os.path.exists(sq):
    with open(sq, encoding="utf-8") as f:
        qlines = f.read().splitlines()
    out.append("== QUEUE total lines: %d ==" % len(qlines))
    # find section D and first open item
    for i, l in enumerate(qlines):
        if l.startswith("## ") or l.startswith("# "):
            out.append("L%d: %s" % (i + 1, l[:80]))
    for i, l in enumerate(qlines[:120]):
        if re.match(r"^\s*[-*]\s*\S", l) and "P-" in l:
            out.append("first-item L%d: %s" % (i + 1, l[:150]))
            break

with open(os.path.join(ROOT, ".c3-tmp", "r_fastcheck.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK", len(out))
