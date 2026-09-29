# -*- coding: utf-8 -*-
# R684: LC-003 R-E shipinhao render call (R680 render_call.py adapted: badge=拆条 003·源城市图鉴 013)
import subprocess, sys, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

# probe frame of derived source (mid, t=6.5)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "6.5", "-i",
                os.path.join("data", "sources", "footage", "census-card-v13-vertical.mp4"),
                "-frames:v", "1", os.path.join(".lc003-tmp", "probe-v13-mid.png")], check=True)

cmd = [
    sys.executable,
    os.path.join("src", "render", "edit_craft.py"),
    "--profile", "shipinhao",
    "--cards", os.path.join("data", "sources", "lc003", "cards-v1-matched.json"),
    "--srt", os.path.join(".lc003-tmp", "subs.srt"),
    "--audio", os.path.join(".lc003-tmp", "audio.mp3"),
    "--out", os.path.join("output", "renders", "lc-003-v1-shipinhao-60s.mp4"),
    "--series-badge",
    "--series-id", "\u62c6\u6761 003\u00b7\u6e90\u57ce\u5e02\u56fe\u9274 013",
    "--h1-glow",
    "--scanlines",
    "--sys-status",
]
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
p = subprocess.run(cmd, cwd=ROOT, env=env)
sys.exit(p.returncode)
