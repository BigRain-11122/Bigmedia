import json, re, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
OUT = []

st = json.load(open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8"))
txt = open(os.path.join(ROOT, "docs", "decisions.md"), encoding="utf-8", errors="replace").read()

# canonical NN=2-digit regex
toks2 = set(re.findall(r"[DC]-20\d{6}-\d{2}", txt))
wm = set(st["decisions_watermark"]["dnums"])
OUT.append("canonical 2-digit: file=%d wm=%d new=%s" % (len(toks2), len(wm), sorted(toks2 - wm) or "NONE"))
OUT.append("in-wm-not-in-file: %s" % (sorted(wm - toks2)[:8] or "NONE"))
# locate the 1-digit false positive context
for m in re.finditer(r"D-20260930-1(?!\d)", txt):
    OUT.append("fp ctx: ..." + txt[max(0, m.start() - 60): m.end() + 40].replace("\n", " ") + "...")

# where does D-20261001-06 BigStream row appear / full text
for m in re.finditer(r"D-20261001-06", txt):
    seg = txt[m.start() - 50: m.start() + 260].replace("\n", " | ")
    if "BigStream" in seg:
        OUT.append("ROW06-BS: " + seg)

# state log: which lines mention the bighouse empower-c for BigStream
log = st["log"]
kws = ["板块十年", "城市生长", "预演", "D-20261001-06 BigStream", "赋能单 c"]
for kw in kws:
    hits = [l for l in log if kw in l]
    OUT.append("kw=%s hits=%d" % (kw, len(hits)))
    for l in hits[-4:]:
        OUT.append("  >> " + l[:500])

# backlog grep
bl = open(os.path.join(BS, "src", "os", "backlog.md"), encoding="utf-8").read()
for kw in ["D-20261001-06", "板块十年", "城市生长", "赋能单"]:
    hits = [l[:300] for l in bl.splitlines() if kw in l]
    OUT.append("backlog kw=%s hits=%d" % (kw, len(hits)))
    for h in hits[-5:]:
        OUT.append("  BK> " + h)

# docs/research listing (names only, newest last)
rd = os.path.join(BS, "docs", "research")
files = sorted(os.listdir(rd))
OUT.append("--- docs/research count: %d ---" % len(files))
for f in files[-25:]:
    OUT.append("RD: " + f)

# research dir for bighouse-like files anywhere in repo (top-level docs + research)
for sub in ["docs", "research"]:
    d = os.path.join(BS, sub)
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if re.search(r"bighouse|big-house|生长|板块|预演", f, re.I):
                OUT.append("CAND FILE: %s/%s" % (sub, f))

with open(os.path.join(BS, ".c3-tmp", "r912_bh.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("lines:", len(OUT))
