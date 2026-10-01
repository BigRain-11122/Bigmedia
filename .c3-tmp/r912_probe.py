import json, re, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
OUT = []

def sec(t):
    OUT.append("")
    OUT.append("==== " + t + " ====")

st = json.load(open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8"))

sec("decisions token diff (content-addressed)")
txt = open(os.path.join(ROOT, "docs", "decisions.md"), encoding="utf-8", errors="replace").read()
toks = set(re.findall(r"[DC]-20\d{6}-\d+", txt))
wm = set(st["decisions_watermark"]["dnums"])
diff = sorted(toks - wm)
OUT.append("file tokens: %d, watermark: %d, NEW: %s" % (len(toks), len(wm), diff if diff else "NONE"))

sec("state log search: D-20261001-06 / BigHouse / w2 OSS")
log = st["log"]
for kw in ["D-20261001-06", "BigHouse", "赋能单", "OH-2026", "w2", "OSS"]:
    hits = [l for l in log if kw in l]
    OUT.append("kw=%s hits=%d" % (kw, len(hits)))
    for l in hits[-3:]:
        OUT.append("  >> " + l[:400])

sec("state log tail 6 (first 200 chars each)")
for l in log[-6:]:
    OUT.append("T: " + l[:200])

sec("finished.md tail")
fin = open(os.path.join(BS, "output", "finished.md"), encoding="utf-8").read().splitlines()
for l in fin[-25:]:
    OUT.append("FIN: " + l[:200])
OUT.append("--- F-08x grep ---")
for l in fin:
    if re.match(r"^\|?\s*F-08", l) or "F-082" in l or "F-083" in l or "F-084" in l or "F-085" in l:
        OUT.append("F: " + l[:220])

sec("backlog #67 / #70 latest lines")
bl = open(os.path.join(BS, "src", "os", "backlog.md"), encoding="utf-8").read().splitlines()
for i, l in enumerate(bl):
    if l.strip().startswith("67.") or l.strip().startswith("70."):
        OUT.append("BL67/70 head: " + l[:300])
for l in bl:
    if re.search(r"R8[6-9]\d|R90[0-5]", l):
        OUT.append("R8xx: " + l[:260])

sec("queue self-improvement-queue tail 45")
q = os.path.join(BS, "docs", "self-improvement-queue.md")
if os.path.exists(q):
    ql = open(q, encoding="utf-8").read().splitlines()
    OUT.append("queue lines total: %d" % len(ql))
    for l in ql[-45:]:
        OUT.append("Q: " + l[:220])

sec("oss-harvest dir")
oh = os.path.join(ROOT, "cph4", "oss-harvest")
if os.path.isdir(oh):
    OUT.append(str(sorted(os.listdir(oh))))
else:
    OUT.append("(missing)")

sec("HQ-FEEDBACK tail 15")
hf = os.path.join(BS, "HQ-FEEDBACK.md")
if os.path.exists(hf):
    hl = open(hf, encoding="utf-8").read().splitlines()
    for l in hl[-15:]:
        OUT.append("HF: " + l[:200])

sec("global-benchmarks update-record head")
gb = open(os.path.join(BS, "docs", "global-benchmarks.md"), encoding="utf-8").read()
m = re.search(r"#+\s*.{0,6}4|更新记录", gb)
idx = gb.find("更新记录")
if idx > 0:
    OUT.append(gb[idx:idx + 400])

sec("src/os listing")
for f in sorted(os.listdir(os.path.join(BS, "src", "os"))):
    OUT.append("OS: " + f)

with open(os.path.join(BS, ".c3-tmp", "r912_probe.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("lines:", len(OUT))
