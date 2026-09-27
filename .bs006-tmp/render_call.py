# R514: BS-006 R-E shipinhao render call (UTF-8 argv, no PS console CJK roundtrip)
import subprocess, sys, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
cmd = [
    sys.executable,
    os.path.join("src", "render", "edit_craft.py"),
    "--profile", "shipinhao",
    "--cards", os.path.join("data", "sources", "bs006", "cards-v1-matched.json"),
    "--srt", os.path.join(".bs006-tmp", "subs.srt"),
    "--audio", os.path.join(".bs006-tmp", "audio.mp3"),
    "--out", os.path.join("output", "renders", "bs-006-v1-shipinhao-60s.mp4"),
    "--series-badge",
    "--series-id", "BS-006 EP.06",
    "--h1-glow",
    "--scanlines",
    "--sys-status",
]
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
p = subprocess.run(cmd, cwd=ROOT, env=env)
sys.exit(p.returncode)
