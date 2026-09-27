# R511: LC-001 frame-sampling plan probe - extract per-beat visual offsets + crossing points
import json, io, os, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
PLAN = os.path.join(ROOT, "output", "renders", "lc-001-v1-shipinhao-60s.mp4.plan.json")
OUT = os.path.join(ROOT, ".lc001-tmp", "fs-plan.txt")
lines = []
with io.open(PLAN, encoding="utf-8") as fh:
    p = json.load(fh)

segs = p.get("segments", p.get("segs", []))
lines.append("keys: %s" % ",".join(p.keys()))
for s in segs:
    lines.append("seg idx=%s start=%s end=%s dur=%s treatment=%s src_off=%s src=%s" % (
        s.get("idx"), round(s.get("start", 0), 2), round(s.get("end", 0), 2),
        round(s.get("end", 0) - s.get("start", 0), 2), s.get("treatment"),
        s.get("src_off"), (s.get("visual") or {}).get("source", "?")))

# source durations for crossing math
for src in ("data/sources/footage/census-card-v7-vertical.mp4",
            "data/sources/footage/reviewsdoc-vertical.mp4"):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1", os.path.join(ROOT, src.replace("/", os.sep))],
                       capture_output=True)
    lines.append("src %s duration=%s" % (os.path.basename(src), r.stdout.decode().strip()))

with io.open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print("done ->", OUT)
