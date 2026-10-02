# -*- coding: utf-8 -*-
"""R982 round-head five-check (content-addressed scan, D-20260930-19 watermark law; r980 lineage, name-variant only)."""
import io, json, os, re, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
out = []
now = time.strftime("%Y-%m-%d %H:%M:%S")
out.append(u"scan ts: " + now)

# 1) orders: count + top by mtime
orders_dir = os.path.join(BS, "orders")
files = sorted(os.listdir(orders_dir), key=lambda f: os.path.getmtime(os.path.join(orders_dir, f)), reverse=True)
out.append(u"orders files=%d top=%s" % (len(files), files[0]))

# 2) ledger mtime + strict @-prefixed task-mode hits
led = os.path.join(ROOT, "cph4", "evolution-ledger.md")
led_txt = io.open(led, encoding="utf-8").read()
hits = [ln for ln in led_txt.splitlines() if ln.strip().startswith("@")]
task_modes = [ln for ln in hits if re.search(u"@BigStream|@七线全司|@全司|@六司|@八线", ln)]
out.append(u"ledger mtime=%s hits=%d task_modes=%d" % (
    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(led))), len(hits), len(task_modes)))

# 3) decisions mtime + canonical dnum set diff vs state watermark (D-20260930-18)
dec = os.path.join(ROOT, "docs", "decisions.md")
dec_txt = io.open(dec, encoding="utf-8").read()
pat = re.compile(r"(?:D|C)-\d{8}-\d{2}(?!\d)")
dnums = sorted(set(pat.findall(dec_txt)))
sp = json.load(io.open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8"))
wm = set(sp.get("decisions_watermark", {}).get("dnums", []))
new = [d for d in dnums if d not in wm]
out.append(u"decisions mtime=%s dnums=%d NEW=%s" % (
    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(dec))), len(dnums), new))

# 4) index.lock + production + tree
out.append(u"index.lock=%s" % os.path.exists(os.path.join(BS, ".git", "index.lock")))
out.append(u"production=%s tick=%s" % (sp.get("production"), sp.get("tick")))

# 5) supply gates: CENSUS anchors C-00030+, daily brief, OSS w3 file, pools leaves
anchors = os.path.join(ROOT, "life", "BigLife", "census", "anchors")
try:
    a_names = sorted(os.listdir(anchors))
except OSError:
    a_names = []
c30plus = [n for n in a_names if re.match(r"C-(\d{5,})", n) and int(re.match(r"C-(\d{5,})", n).group(1)) >= 30]
out.append(u"CENSUS anchors top=%s c30plus=%d" % (a_names[-1] if a_names else "NONE", len(c30plus)))
out.append(u"daily 2026-10-02 present=%s" % os.path.exists(os.path.join(BS, "data", "intel", "daily", "2026-10-02.md")))
out.append(u"daily 2026-10-03 present=%s" % os.path.exists(os.path.join(BS, "data", "intel", "daily", "2026-10-03.md")))
out.append(u"OH-20261002-bigstream present=%s" % os.path.exists(os.path.join(ROOT, "cph4", "oss-harvest", "OH-20261002-bigstream.md")))
pool = json.load(io.open(os.path.join(ROOT, "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
leaf = 0
for ax, buckets in pool["axes"].items():
    for b, lines in buckets.items():
        leaf += len(lines)
# R982 fix: sprite moved out of axes to top-level key by BigLife restructure; count it too
# (axes-only reading 1296 vs 1440 baseline = structure artifact, not content change)
sprite = pool.get("sprite")
if isinstance(sprite, dict):
    for b, lines in sprite.items():
        if isinstance(lines, list):
            leaf += len(lines)
out.append(u"pools leaf count=%d (1440 baseline, axes+sprite R982 fix)" % leaf)

io.open(os.path.join(BS, ".c3-tmp", "r982_scan.txt"), "w", encoding="utf-8").write(u"\n".join(out))
print("SCAN-OK lines=%d NEW_DNUMS=%d" % (len(out), len(new)))
