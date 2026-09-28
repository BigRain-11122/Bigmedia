import json, os, io, time, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, ".c3-tmp", "r658_fivecheck.txt")
L = []
def w(s=""):
    L.append(str(s))

now = time.time()
w("now: " + time.strftime("%Y-%m-%d %H:%M:%S"))

# --- 1) state.json ---
sp = os.path.join(ROOT, "src", "os", "state.json")
st = json.load(io.open(sp, "r", encoding="utf-8"))
w("== state ==")
for k in ("tick", "ts", "task", "production"):
    w(f"{k} = {st.get(k)}")
log = st.get("log", [])
w(f"log_len = {len(log)}")
for e in log[-3:]:
    w("---- logtail ----")
    w(e[:1300])

# --- 2) orders latest ---
od = os.path.join(ROOT, "orders")
fl = sorted(((os.path.getmtime(os.path.join(od, f)), f) for f in os.listdir(od)), reverse=True)
w("== orders latest 6 ==")
for mt, f in fl[:6]:
    w(time.strftime("%m-%d %H:%M ", time.localtime(mt)) + f)

# --- 3) ledger @ rows ---
LED = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
pats = ("@BigStream", "@qi-xian-quan-si", "@quan-si", "@liu-si", "@ba-xian")
pats = ("@BigStream", "@\u4e03\u7ebf\u5168\u53f8", "@\u5168\u53f8", "@\u516d\u53f8", "@\u516b\u7ebf")
cnt = 0
with io.open(LED, "r", encoding="utf-8") as f:
    for line in f:
        if any(p in line for p in pats):
            cnt += 1
w(f"== ledger @rows = {cnt} (anchor 34)")

# --- 4) decisions nonempty ---
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
with io.open(DEC, "r", encoding="utf-8") as f:
    dn = sum(1 for l in f.read().splitlines() if l.strip())
w(f"== decisions nonempty = {dn} (anchor 68)")

# --- 5) index.lock + codex mtimes ---
w("index.lock = " + str(os.path.exists(os.path.join(ROOT, ".git", "index.lock"))))
for rel in ("data/storylines/codex/README.md", "data/storylines/codex/city-humanities.md"):
    p = os.path.join(ROOT, rel)
    w(f"mtime {rel}: " + time.strftime("%m-%d %H:%M:%S", time.localtime(os.path.getmtime(p))))

# --- 6) recent e4/s1 result files (<=48h) in tmp dirs ---
w("== recent e4/s1 result files (<=48h) ==")
tmpdirs = [os.path.join(ROOT, n) for n in os.listdir(ROOT)
           if n.startswith(".") and n.endswith("-tmp") and os.path.isdir(os.path.join(ROOT, n))]
for d in tmpdirs:
    for p in os.listdir(d):
        fp = os.path.join(d, p)
        try:
            mt = os.path.getmtime(fp)
        except OSError:
            continue
        if now - mt <= 48 * 3600 and ("e4" in p.lower() or "s1-result" in p.lower()):
            w(time.strftime("%m-%d %H:%M ", time.localtime(mt)) + fp)
            if p.endswith(".json") and os.path.getsize(fp) < 4000:
                w(io.open(fp, "r", encoding="utf-8", errors="replace").read()[:1500])

# --- 7) react v5 review E4 status ---
rv = os.path.join(ROOT, "docs", "reviews", "review-20260929-mcreact-v5.md")
if os.path.exists(rv):
    txt = io.open(rv, "r", encoding="utf-8").read()
    w("== react v5 review len=" + str(len(txt)) + " ==")
    for line in txt.splitlines():
        if "E4" in line:
            w("E4LINE: " + line[:220])
else:
    w("== react v5 review MISSING")

# --- 8) F-054 row in finished ---
fin = os.path.join(ROOT, "output", "finished.md")
txt = io.open(fin, "r", encoding="utf-8").read()
i = txt.find("F-054")
w("== finished F-054 ==")
w(txt[i:i+900] if i >= 0 else "F-054 NOT FOUND")

# --- 9) audits dir ---
w("== docs/audits ==")
ad = os.path.join(ROOT, "docs", "audits")
for f in sorted(os.listdir(ad)):
    w(f + "  " + time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(os.path.join(ad, f)))))

# --- 10) daily brief today ---
w("daily 2026-09-29 = " + str(os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-09-29.md"))))

# --- 11) queue tail ---
q = os.path.join(ROOT, "docs", "self-improvement-queue.md")
qt = io.open(q, "r", encoding="utf-8").read()
w("== queue len=" + str(len(qt)) + " tail ==")
w(qt[-2400:])

# --- 12) python/ollama processes ---
try:
    r = subprocess.run("tasklist", capture_output=True, text=True, timeout=20)
    for line in r.stdout.splitlines():
        ll = line.lower()
        if "python" in ll or "ollama" in ll or "llama" in ll:
            w("PROC: " + line[:120])
except Exception as ex:
    w("tasklist fail: " + str(ex))

io.open(OUT, "w", encoding="utf-8").write("\n".join(L))
print("written", OUT)
