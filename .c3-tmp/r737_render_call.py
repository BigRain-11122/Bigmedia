# -*- coding: utf-8 -*-
# R737: LC-017 R-E shipinhao render call (R733 render_call.py adapted: badge=chaitiao 017 - source census 004)
import subprocess, sys, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

# probe frame of derived source (mid, t=6.5)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "6.5", "-i",
                os.path.join("data", "sources", "footage", "census-card-v4-vertical.mp4"),
                "-frames:v", "1", os.path.join(".lc017-tmp", "probe-v4-mid.png")], check=True)

cmd = [
    sys.executable,
    os.path.join("src", "render", "edit_craft.py"),
    "--profile", "shipinhao",
    "--cards", os.path.join("data", "sources", "lc017", "cards-v1-matched.json"),
    "--srt", os.path.join(".lc017-tmp", "subs.srt"),
    "--audio", os.path.join(".lc017-tmp", "audio.mp3"),
    "--out", os.path.join("output", "renders", "lc-017-v1-shipinhao-60s.mp4"),
    "--series-badge",
    "--series-id", "\u62c6\u6761 017\u00b7\u6e90\u57ce\u5e02\u56fe\u9274 004",
    "--h1-glow",
    "--scanlines",
    "--sys-status",
]
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
p = subprocess.run(cmd, cwd=ROOT, env=env)
sys.exit(p.returncode)
