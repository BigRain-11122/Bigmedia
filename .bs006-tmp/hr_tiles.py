# R514: high-res targeted re-verification tiles (R189 tile-misread rule: full-res over tile-downscale)
import subprocess, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".bs006-tmp")

def htile(files, out, w=540, h=960):
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for f in files:
        cmd += ["-i", f]
    n = len(files)
    fc = ";".join("[%d:v]scale=%d:%d[u%d]" % (i, w, h, i) for i in range(n))
    fc += ";" + "".join("[u%d]" % i for i in range(n)) + "hstack=inputs=%d" % n
    cmd += ["-filter_complex", fc, out]
    subprocess.run(cmd, check=True)

# heads of the three reviewsdoc beats (b3 / b6 / b10)
htile([os.path.join(TMP, "fs-h03.png"), os.path.join(TMP, "fs-h06.png"),
       os.path.join(TMP, "fs-h10.png")], os.path.join(TMP, "fs-tile-rev-heads.png"))

# mid+tail of b0 / b6 / b10 (6 panels, 3 cols x 2 rows)
mids = ["fs-m00.png", "fs-t00.png", "fs-m06.png", "fs-t06.png", "fs-m10.png", "fs-t10.png"]
cmd = ["ffmpeg", "-y", "-v", "error"]
for f in mids:
    cmd += ["-i", os.path.join(TMP, f)]
fc = ";".join("[%d:v]scale=540:960[u%d]" % (i, i) for i in range(6))
fc += ";[u0][u1][u2]hstack=inputs=3[r0];[u3][u4][u5]hstack=inputs=3[r1];[r0][r1]vstack=inputs=2"
cmd += ["-filter_complex", fc, os.path.join(TMP, "fs-tile-midtail-hr.png")]
subprocess.run(cmd, check=True)
print("done -> fs-tile-rev-heads.png / fs-tile-midtail-hr.png")
