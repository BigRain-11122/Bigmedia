# R514: inspect plan segments (src_off/source/treatment) + probe reviewsdoc at multiple offsets
import json, io, os, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
PLAN = os.path.join(ROOT, "output", "renders", "bs-006-v1-shipinhao-60s.mp4.plan.json")
TMP = os.path.join(ROOT, ".bs006-tmp")

with io.open(PLAN, encoding="utf-8") as fh:
    p = json.load(fh)
for s in p["segments"]:
    v = s.get("visual") or {}
    print("idx=%s start=%.2f end=%.2f dur=%.2f treat=%s src_off=%s src=%s" % (
        s.get("idx"), s.get("start", 0), s.get("end", 0),
        s.get("end", 0) - s.get("start", 0), s.get("treatment"),
        s.get("src_off"), v.get("source", "-")))

# probe reviewsdoc-vertical at 0.3 / 3.0 / 6.0 / 9.0 to map its content timeline
FOOT = os.path.join(ROOT, "data", "sources", "footage", "reviewsdoc-vertical.mp4")
frames = []
for t in (0.3, 3.0, 6.0, 9.0):
    out = os.path.join(TMP, "probe-rev-t%.1f.png" % t)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", FOOT,
                    "-frames:v", "1", out], check=True)
    frames.append(out)
cmd = ["ffmpeg", "-y", "-v", "error"]
for f in frames:
    cmd += ["-i", f]
cmd += ["-filter_complex",
        "[0:v]scale=270:480[a];[1:v]scale=270:480[b];[2:v]scale=270:480[c];[3:v]scale=270:480[d];"
        "[a][b]hstack=inputs=2[r0];[c][d]hstack=inputs=2[r1];[r0][r1]vstack=inputs=2",
        os.path.join(TMP, "probe-rev-tile.png")]
subprocess.run(cmd, check=True)
print("rev probe tile -> probe-rev-tile.png")
