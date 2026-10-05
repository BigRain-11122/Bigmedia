# -*- coding: utf-8 -*-
"""Round-opening quick five-check probe (read-only). Output UTF-8 file."""
import json, os, re, subprocess, glob, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
HQ = r"C:\Users\sjs20\Desktop\FluxGroup"
OUT = os.path.join(ROOT, ".c3-tmp", "r_open_probe.txt")

lines = []
def w(s=""):
    lines.append(s)

# 1) state.json top fields + log tail 3
with open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
w("== state.json top-level keys ==")
for k, v in st.items():
    if k == "log":
        w("  log: %d entries" % len(v))
    else:
        w("  %s: %s" % (k, json.dumps(v, ensure_ascii=False)[:600]))
log = st.get("log", [])
w("")
w("== log tail 3 entries ==")
for e in log[-3:]:
    w("---")
    w(e if isinstance(e, str) else json.dumps(e, ensure_ascii=False))
w("")

# decisions watermark diff
dw = st.get("decisions_watermark", {})
dnums = set(dw.get("dnums", []) if isinstance(dw, dict) else [])

# 2) git status
w("== git status --short ==")
p = subprocess.run(["git", "-C", ROOT, "status", "--short"], capture_output=True, text=True, encoding="utf-8", errors="replace")
w(p.stdout.strip() or "(clean)")
w("index.lock exists: %s" % os.path.exists(os.path.join(ROOT, ".git", "index.lock")))
w("")

# HEAD
p = subprocess.run(["git", "-C", ROOT, "log", "-3", "--format=%h %ad %s", "--date=format:%m-%d %H:%M"], capture_output=True, text=True, encoding="utf-8", errors="replace")
w("== git log -3 ==")
w(p.stdout.strip())
w("")

# 3) orders/ latest files
w("== orders/ latest 6 by mtime ==")
od = os.path.join(ROOT, "orders")
files = [(os.path.getmtime(x), x) for x in glob.glob(os.path.join(od, "*")) if os.path.isfile(x)]
for mt, fp in sorted(files, reverse=True)[:6]:
    w("  %s  %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mt)), os.path.basename(fp)))
w("")

# 4) ledger @BigStream scan (strict @ prefix patterns)
w("== evolution-ledger @-mentions (BigStream/全司/七线/六司/八线) ==")
led = os.path.join(HQ, "cph4", "evolution-ledger.md")
pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线全量)")
n = 0
with open(led, encoding="utf-8", errors="replace") as f:
    for i, ln in enumerate(f, 1):
        if pat.search(ln):
            n += 1
            m = re.search(r"(P-\d{4}-\d{2}-\d{2}-\d+|D-\d{8}-\d+|C-\d{8}-\d+)", ln)
            w("  L%d %s :: %s" % (i, m.group(1) if m else "?", ln.strip()[:160]))
w("  total mention lines: %d" % n)
w("  ledger mtime: %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(led))))
w("")

# 5) decisions.md D/C set diff + top dispatch block
w("== FluxGroup/docs/decisions.md ==")
dec = os.path.join(HQ, "docs", "decisions.md")
with open(dec, encoding="utf-8", errors="replace") as f:
    dtxt = f.read()
dset = set(re.findall(r"\b[DC]-\d{8}-\d+\b", dtxt))
new = sorted(dset - dnums) if dnums else sorted(dset)
w("  file D/C set size: %d ; state dnums: %d ; NEW (diff): %s" % (len(dset), len(dnums), new if new else "(none)"))
w("  mtime: %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(dec))))
w("  --- top 25 lines of file (派工通告板 head) ---")
for ln in dtxt.splitlines()[:25]:
    w("  | " + ln[:180])
w("")

# 6) supply-gate / daily / pending E4 checks
w("== supply & routine checks ==")
for cand in [os.path.join(HQ, "life", "BigLife", "census", "anchors", "C-00030.md"),
             os.path.join(HQ, "census", "anchors", "C-00030.md")]:
    if os.path.exists(cand):
        w("  C-00030 anchor EXISTS: %s (mtime %s)" % (cand, time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(cand)))))
    else:
        w("  C-00030 anchor missing: %s" % cand)
anchors_dir = os.path.join(HQ, "life", "BigLife", "census", "anchors")
if os.path.isdir(anchors_dir):
    an = sorted(glob.glob(os.path.join(anchors_dir, "*.md")))
    w("  anchors top 3: %s" % [os.path.basename(x) for x in an[-3:]])
db = os.path.join(ROOT, "data", "intel", "daily", "2026-10-06.md")
w("  daily brief 2026-10-06: %s" % ("EXISTS" if os.path.exists(db) else "MISSING"))
w("")

# recent expert-verdicts (48h) for E4 backfill check
w("== expert-verdicts last 48h ==")
ev = os.path.join(ROOT, "docs", "reviews", "expert-verdicts")
now = time.time()
for fp in sorted(glob.glob(os.path.join(ev, "*.md")), reverse=True)[:8]:
    mt = os.path.getmtime(fp)
    if now - mt < 48 * 3600:
        w("  %s  %s" % (time.strftime("%m-%d %H:%M:%S", time.localtime(mt)), os.path.basename(fp)))
w("")

# 7) queue top + E pool heads
w("== self-improvement-queue head scan ==")
q = os.path.join(ROOT, "docs", "self-improvement-queue.md")
if os.path.exists(q):
    with open(q, encoding="utf-8") as f:
        ql = f.read().splitlines()
    w("  total lines: %d ; mtime: %s" % (len(ql), time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(q)))))
    inE = False
    shown = 0
    for ln in ql:
        if ln.startswith("## ") or ln.startswith("# "):
            w("  HEAD| " + ln[:100])
        if "§E" in ln or "E 池" in ln or "批活池" in ln:
            inE = True
        if inE and shown < 25:
            if ln.strip():
                w("  E| " + ln[:170])
                shown += 1
w("")

# 8) tmp e4-result pending files (recent)
w("== recent e4-result.json / s1-result.json (36h) ==")
for fp in glob.glob(os.path.join(ROOT, "**", "e4-result.json"), recursive=True) + glob.glob(os.path.join(ROOT, ".mc-digest15*", "*")) :
    mt = os.path.getmtime(fp)
    if now - mt < 36 * 3600:
        w("  %s  %s" % (time.strftime("%m-%d %H:%M", time.localtime(mt)), fp.replace(ROOT, ".")))
w("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("probe written:", OUT)
