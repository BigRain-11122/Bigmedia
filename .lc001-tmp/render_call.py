# R511: LC-001 R-E shipinhao render call (UTF-8 argv, no PS console CJK roundtrip)
import subprocess, sys, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
cmd = [
    sys.executable,
    os.path.join("src", "render", "edit_craft.py"),
    "--profile", "shipinhao",
    "--cards", os.path.join("data", "sources", "lc001", "cards-v1-matched.json"),
    "--srt", os.path.join(".lc001-tmp", "subs.srt"),
    "--audio", os.path.join(".lc001-tmp", "audio.mp3"),
    "--out", os.path.join("output", "renders", "lc-001-v1-shipinhao-60s.mp4"),
    "--series-badge",
    "--series-id", "\u62c6\u6761 001\u00b7\u6e90\u57ce\u5e02\u56fe\u9274 007",
    "--h1-glow",
    "--scanlines",
    "--sys-status",
]
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
p = subprocess.run(cmd, cwd=ROOT, env=env)
sys.exit(p.returncode)
