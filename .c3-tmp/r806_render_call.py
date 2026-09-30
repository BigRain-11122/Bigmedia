# -*- coding: utf-8 -*-
# R806: BS-010 R-E shipinhao render call (R755/R803 render_call adapted: badge=BS-010 EP.10)
import subprocess, sys, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

cmd = [
    sys.executable,
    os.path.join("src", "render", "edit_craft.py"),
    "--profile", "shipinhao",
    "--cards", os.path.join("data", "sources", "bs010", "cards-v1-matched.json"),
    "--srt", os.path.join(".bs010-tmp", "subs.srt"),
    "--audio", os.path.join(".bs010-tmp", "audio.mp3"),
    "--out", os.path.join("output", "renders", "bs-010-v1-shipinhao-60s.mp4"),
    "--series-badge",
    "--series-id", "BS-010 EP.10",
    "--h1-glow",
    "--scanlines",
    "--sys-status",
]
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
p = subprocess.run(cmd, cwd=ROOT, env=env)
sys.exit(p.returncode)
