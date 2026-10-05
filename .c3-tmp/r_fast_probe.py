# -*- coding: utf-8 -*-
"""R-round fast-path probe: state tail, watermark diff, ledger scan, gates."""
import io, json, os, re, subprocess, glob

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
HQ = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT = os.path.join(ROOT, ".c3-tmp", "r_probe_fast.txt")
lines = []
def w(s):
    lines.append(s)

# 1) state.json top fields + log tail
with io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8") as f:
    st = json.load(f)
w("=== state.json top ===")
for k in ("tick", "ts", "task", "production"):
    if k in st:
        w("%s: %s" % (k, st[k]))
wm = st.get("decisions_watermark", {})
w("watermark keys: %s" % list(wm.keys()))
dnums = wm.get("dnums", []) if isinstance(wm, dict) else []
w("dnums count: %d" % len(dnums))
w("dnums tail(8): %s" % (dnums[-8:] if dnums else []))
w("watermark raw (trimmed): %s" % json.dumps(wm, ensure_ascii=False)[:400])
log = st.get("log", [])
w("log count: %d" % len(log))
w("=== log tail 3 ===")
for entry in log[-3:]:
    w(entry[:600])
    w("---")

# 2) group decisions.md D/C numbers (content-addressed)
dec_path = os.path.join(HQ, "docs", "decisions.md")
with io.open(dec_path, "r", encoding="utf-8") as f:
    dec_txt = f.read()
dnums_file = set(re.findall(r"D-\d{8}-\d{2}", dec_txt))
cnums_file = set(re.findall(r"C-\d{8}-\d{2}", dec_txt))
w("=== group decisions.md ===")
w("D set size: %d | C set size: %d" % (len(dnums_file), len(cnums_file)))
wset = set(dnums) if dnums else set()
new_d = dnums_file - wset
new_c = cnums_file - wset
w("new D vs watermark: %s" % (sorted(new_d) if new_d else "NONE"))
w("new C vs watermark: %s" % (sorted(new_c) if new_c else "NONE"))

# 3) evolution-ledger @BigStream scan (strict @ prefix lines)
led_path = os.path.join(HQ, "cph4", "evolution-ledger.md")
with io.open(led_path, "r", encoding="utf-8") as f:
    led_txt = f.read()
pat = re.compile(r"@[Bb]ig[Ss]tream|@七线全司|@全司|@六司|@八线全量")
hits = []
for i, ln in enumerate(led_txt.splitlines(), 1):
    if pat.search(ln):
        hits.append((i, ln.strip()))
w("=== evolution-ledger scan ===")
w("total @lines: %d" % len(hits))
for i, ln in hits[-6:]:
    w("L%d: %s" % (i, ln[:300]))

# 4) gates: daily brief today, W41 audit, orders latest, backlog quick
today = "2026-10-06"
brief = os.path.join(ROOT, "data", "intel", "daily", today + ".md")
w("=== gates ===")
w("daily brief %s exists: %s" % (today, os.path.exists(brief)))
w41 = os.path.join(ROOT, "docs", "audits", "2026-W41-self-audit.md")
w("W41 audit exists: %s" % os.path.exists(w41))
orders = sorted(glob.glob(os.path.join(ROOT, "orders", "*.md")), key=os.path.getmtime)
w("orders latest 3: %s" % [os.path.basename(p) for p in orders[-3:]])
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
with io.open(gb, "r", encoding="utf-8") as f:
    gb_txt = f.read()
m = re.search(r"(\d{4}-\d{2}-\d{2})", gb_txt[:2000])
w("global-benchmarks first date: %s" % (m.group(1) if m else "?"))

# 5) git status
p = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True)
w("=== git status ===")
w(p.stdout.strip()[:800] if p.stdout.strip() else "(clean)")
lock = os.path.join(ROOT, ".git", "index.lock")
w("index.lock exists: %s" % os.path.exists(lock))
p2 = subprocess.run(["git", "log", "--oneline", "-3"], cwd=ROOT, capture_output=True, text=True)
w("HEAD 3: %s" % p2.stdout.strip().replace("\n", " | "))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("OK %d lines -> %s" % (len(lines), OUT))
