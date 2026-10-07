# -*- coding: utf-8 -*-
# R1692 BS-016 frame verification probe (bs015 frameverify-r1689 pattern; dual wrap b0+b4)
import json, io, os, subprocess

OUT = ".bs016-tmp/frameverify-r1692"
os.makedirs(OUT, exist_ok=True)
mp4 = "output/renders/bs-016-v1-shipinhao-60s.mp4"
c = json.loads(io.open("data/sources/bs016/cards-v1-matched.json", encoding="utf-8").read())
cards = c["cards"]
NET = 4.400  # citywatch trimmed clean window (R188/R197)

def grab(t, name, scale=None):
    vf = ["-vf", "scale=%s" % scale] if scale else []
    cmd = ["ffmpeg", "-y", "-v", "error", "-ss", "%.3f" % t, "-i", mp4, "-frames:v", "1"] + vf + ["-q:v", "3", os.path.join(OUT, name)]
    subprocess.run(cmd, check=True)

# 1) beat-head frames (t=start+0.15) at tile scale
for i, cd in enumerate(cards):
    grab(cd["start"] + 0.15, "beat%d.png" % i, scale="270:480")

# tile 3x4
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(OUT, "beat%d.png" % 0), "-i", os.path.join(OUT, "beat%d.png" % 1),
                "-i", os.path.join(OUT, "beat%d.png" % 2), "-i", os.path.join(OUT, "beat%d.png" % 3),
                "-i", os.path.join(OUT, "beat%d.png" % 4), "-i", os.path.join(OUT, "beat%d.png" % 5),
                "-i", os.path.join(OUT, "beat%d.png" % 6), "-i", os.path.join(OUT, "beat%d.png" % 7),
                "-i", os.path.join(OUT, "beat%d.png" % 8), "-i", os.path.join(OUT, "beat%d.png" % 9),
                "-i", os.path.join(OUT, "beat%d.png" % 10), "-i", os.path.join(OUT, "beat%d.png" % 11),
                "-filter_complex", "[0][1][2][3]hstack=4[a];[4][5][6][7]hstack=4[b];[8][9][10][11]hstack=4[c];[a][b][c]vstack=3",
                "-q:v", "3", os.path.join(OUT, "tile-beats.png")], check=True)

# 2) wrap boundaries full-res: b0 (citywatch, start 0, dur>NET) and b4 (citywatch)
wraps = []
for i, cd in enumerate(cards):
    v = cd.get("visual", {})
    if v.get("source", "").endswith("citywatch-vertical.mp4"):
        dur = cd["end"] - cd["start"]
        if dur > NET:
            wraps.append((i, cd["start"], cd["end"]))
for i, s, e in wraps:
    x = s + NET
    for tag, t in (("pre", x - 0.25), ("x", x), ("post", x + 0.25)):
        if s < t < e:
            grab(t, "b%d_wrap_%s.png" % (i, tag))
    print("wrap beat b%d start=%.2f end=%.2f crossing=%.2f" % (i, s, e, x))

# 3) full-res text frames: b8 census card + b11 CTA + b10 self-ref + b2 directive
grab(cards[8]["start"] + 0.30, "full_b8.png")
grab(cards[11]["start"] + 0.30, "full_b11.png")
grab(cards[10]["start"] + 2.00, "full_b10.png")
grab(cards[2]["start"] + 0.30, "full_b2.png")

print("OK frames out ->", OUT)
