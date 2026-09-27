# R514: BS-006 footage probe (four candidate sources, mid frame each, tiled)
import subprocess, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".bs006-tmp")
FOOT = os.path.join(ROOT, "data", "sources", "footage")

SRC = ["looplog-vertical.mp4", "reviewsdoc-vertical.mp4",
       "editgrid-vertical.mp4", "citywatch-vertical.mp4"]

frames = []
for i, s in enumerate(SRC):
    out = os.path.join(TMP, "probe-src%d.png" % i)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "2.0", "-i",
                    os.path.join(FOOT, s), "-frames:v", "1", out], check=True)
    frames.append(out)

# durations for crossing math later
for s in SRC:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1", os.path.join(FOOT, s)],
                       capture_output=True)
    print(s, r.stdout.decode().strip())

# tile 2x2
cmd = ["ffmpeg", "-y", "-v", "error"]
for f in frames:
    cmd += ["-i", f]
cmd += ["-filter_complex",
        "[0:v]scale=405:720[a];[1:v]scale=405:720[b];[2:v]scale=405:720[c];[3:v]scale=405:720[d];"
        "[a][b]hstack=inputs=2[r0];[c][d]hstack=inputs=2[r1];[r0][r1]vstack=inputs=2",
        os.path.join(TMP, "probe-src-tile.png")]
subprocess.run(cmd, check=True)
print("probe tile -> probe-src-tile.png")
