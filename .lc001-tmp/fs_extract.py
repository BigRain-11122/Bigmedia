# R511: LC-001 frame-sampling extraction (three laws: beat-heads / mid-tail / crossing-math)
import json, io, os, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
MP4 = os.path.join(ROOT, "output", "renders", "lc-001-v1-shipinhao-60s.mp4")
CARDS = os.path.join(ROOT, "data", "sources", "lc001", "cards-v1-matched.json")
TMP = os.path.join(ROOT, ".lc001-tmp")

with io.open(CARDS, encoding="utf-8") as fh:
    cards = json.load(fh)["cards"]

def grab(t, out):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "%.3f" % t, "-i", MP4,
                   "-frames:v", "1", out], check=True)

# law 1: 12 beat-head frames (start + 0.15)
heads = []
for i, c in enumerate(cards):
    out = os.path.join(TMP, "fs-h%02d.png" % i)
    grab(c["start"] + 0.15, out)
    heads.append(out)

# law 2: mid + tail for longest census beats (5,7) and the ledger beat (9)
midtail = []
for i in (5, 7, 9):
    c = cards[i]
    m = os.path.join(TMP, "fs-m%02d.png" % i)
    t = os.path.join(TMP, "fs-t%02d.png" % i)
    grab((c["start"] + c["end"]) / 2.0, m)
    grab(c["end"] - 0.30, t)
    midtail += [m, t]

def tile(files, out, cols):
    n = len(files)
    rows = (n + cols - 1) // cols
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for f in files:
        cmd += ["-i", f]
    parts = []
    for r in range(rows):
        idxs = list(range(r * cols, min((r + 1) * cols, n)))
        parts.append(";".join("[%d:v]scale=270:480[u%d]" % (i, i) for i in idxs) + ";" +
                     "".join("[u%d]" % i for i in idxs) + "hstack=inputs=%d[r%d]" % (len(idxs), r))
    parts.append("".join("[r%d]" % r for r in range(rows)) + "vstack=inputs=%d" % rows)
    cmd += ["-filter_complex", ";".join(parts), out]
    subprocess.run(cmd, check=True)

tile(heads, os.path.join(TMP, "fs-tile-heads.png"), 4)
tile(midtail, os.path.join(TMP, "fs-tile-midtail.png"), 2)

# law 3: crossing math (all beats src_off=0; crossing iff beat dur > source dur)
srcs = {"census-card-v7-vertical.mp4": 13.0, "reviewsdoc-vertical.mp4": 10.0}
crossings = {}
for i, c in enumerate(cards):
    v = c.get("visual")
    if not v:
        continue
    sname = os.path.basename(v["source"])
    if c["end"] - c["start"] > srcs[sname]:
        crossings[i] = round(srcs[sname] - 0.0, 2)
print("crossings =", crossings if crossings else "{} (all beats shorter than source, src_off=0)")
print("heads:", len(heads), "midtail:", len(midtail))
print("done -> fs-tile-heads.png / fs-tile-midtail.png")
