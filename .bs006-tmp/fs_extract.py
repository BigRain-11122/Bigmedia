# R514: BS-006 frame-sampling verification (three laws: beat-heads / mid-tail / crossing-math)
import json, io, os, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
MP4 = os.path.join(ROOT, "output", "renders", "bs-006-v1-shipinhao-60s.mp4")
CARDS = os.path.join(ROOT, "data", "sources", "bs006", "cards-v1-matched.json")
PLAN = MP4 + ".plan.json"
TMP = os.path.join(ROOT, ".bs006-tmp")

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

# law 2: mid + tail for the three heaviest footage beats (b0 looplog / b6 reviewsdoc / b10 reviewsdoc)
midtail = []
for i in (0, 6, 10):
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

# law 3: crossing math from plan (src_off + source durations)
with io.open(PLAN, encoding="utf-8") as fh:
    p = json.load(fh)
segs = p.get("segments", p.get("segs", []))
SRC_DUR = {"looplog-vertical.mp4": 12.0, "reviewsdoc-vertical.mp4": 10.0,
           "editgrid-vertical.mp4": 10.0}
crossings = {}
for s in segs:
    v = s.get("visual") or {}
    src = os.path.basename(v.get("source", "")) if v.get("source") else None
    if not src:
        continue
    off = s.get("src_off", 0) or 0
    dur = s.get("end", 0) - s.get("start", 0)
    if dur > SRC_DUR[src] - off:
        crossings[s.get("idx")] = round(SRC_DUR[src] - off, 2)
print("crossings =", crossings if crossings else "{} (all beats shorter than source window, no loop wrap)")
print("heads:", len(heads), "midtail:", len(midtail))
print("plan keys:", ",".join(p.keys()))
print("series:", json.dumps(p.get("series", {}), ensure_ascii=False))
