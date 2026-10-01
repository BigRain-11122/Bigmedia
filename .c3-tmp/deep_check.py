# -*- coding: utf-8 -*-
# Deep check: D-20261001-06 dispatch novelty + OSS w3 slice status + gb freshness + full R852 log
import json, re, os, io, datetime

BASE = r"C:\Users\sjs20\Desktop\FluxGroup"
BM = os.path.join(BASE, "media", "BigStream")
OUT = []
def w(s): OUT.append(str(s))

# full R852 log line
with open(os.path.join(BM, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
log = st.get("log") or []
for line in log[-1:]:
    w("== R852 FULL LOG ==")
    w(line)

# decisions.md mtime
dec_path = os.path.join(BASE, "docs", "decisions.md")
w("== decisions.md mtime=%s" % datetime.datetime.fromtimestamp(os.path.getmtime(dec_path)).strftime("%Y-%m-%d %H:%M:%S"))

# dispatch rows containing D-20261001-06 (all) and any BigStream rows
dec = open(dec_path, encoding="utf-8").read()
w("== D-20261001-06 rows in decisions.md ==")
for l in dec.splitlines():
    if "D-20261001-06" in l:
        w("D0606>> " + l.strip()[:400])
w("== BigStream rows anywhere mentioning 收讫/回执 status ==")
m = re.search(r"派工通告板(.*?)(?=\n#+ |\Z)", dec, re.S)
blk = m.group(1) if m else ""
for l in blk.splitlines():
    if "BigStream" in l:
        w("BS_ROW>> " + l.strip()[:400])

# does any own-repo file already reference D-20261001-06 (ack trace)?
w("== own-repo ack trace for D-20261001-06 ==")
hits = 0
for root, dirs, files in os.walk(BM):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
    for fn in files:
        if fn.endswith((".md", ".json", ".txt")):
            p = os.path.join(root, fn)
            try:
                if os.path.getsize(p) > 3_000_000: continue
                t = open(p, encoding="utf-8", errors="ignore").read()
                if "D-20261001-06" in t:
                    w("HIT>> %s (mtime %s)" % (os.path.relpath(p, BM), datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M")))
                    hits += 1
            except Exception:
                pass
w("hits=%d" % hits)

# OSS harvest window 3 slice check
oh_path = os.path.join(BASE, "cph4", "oss-harvest", "OH-20260926-bigstream.md")
if os.path.exists(oh_path):
    oh = open(oh_path, encoding="utf-8").read()
    w("== OH file tail (window-3 slice check) ==")
    w("OH_len=%d" % len(oh))
    tl = [l for l in oh.splitlines() if l.strip()]
    for l in tl[-25:]:
        w("OH>> " + l[:220])
else:
    w("OH file NOT FOUND")

# gb freshness precise
gb = open(os.path.join(BM, "docs", "global-benchmarks.md"), encoding="utf-8").read()
idx = gb.find("更新记录")
w("== GB update-record head ==")
head = gb[idx:idx+400] if idx >= 0 else "NONE"
w(head)

# r852 scan evidence
p2 = os.path.join(BM, ".c3-tmp", "r852_scan.txt")
if os.path.exists(p2):
    w("== r852_scan.txt ==")
    w(open(p2, encoding="utf-8").read()[:1500])

with open(os.path.join(BM, ".c3-tmp", "deep_check_out.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("OK lines=%d" % len(OUT))
