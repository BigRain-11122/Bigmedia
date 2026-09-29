# -*- coding: utf-8 -*-
# R687: LC-004 S2 three-gate enforcement (R684 s2_gates.py adapted)
import subprocess, sys, os, io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(ROOT, ".lc004-tmp", "s2-results.md")
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"

BEATS = os.path.join("data", "sources", "lc004", "voiceover-v4.beats.txt")
SRT = os.path.join(".lc004-tmp", "subs.srt")
MP4 = os.path.join("output", "renders", "lc-004-v1-shipinhao-60s.mp4")
PLAN = MP4 + ".plan.json"
PLATFORM = "\u5fae\u4fe1\u89c6\u9891\u53f7"  # weixin shipinhao

cmds = [
    ("gate1_ai_feel", [sys.executable, "src" + os.sep + "ai_feel_check.py",
                       "--beats", BEATS, "--srt", SRT]),
    ("gate2_platform_spec", [sys.executable, "src" + os.sep + "platform_spec_check.py",
                             "--video", MP4, "--platform", PLATFORM]),
    ("gate3_edit_craft_1p8", [sys.executable, "src" + os.sep + "edit_craft_check.py",
                              "--plan", PLAN, "--srt", SRT, "--profile", "shipinhao"]),
]

with io.open(OUT, "w", encoding="utf-8") as out:
    for name, cmd in cmds:
        p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True)
        out.write("=== %s exit=%d ===\n" % (name, p.returncode))
        out.write(p.stdout.decode("utf-8", "replace"))
        err = p.stderr.decode("utf-8", "replace").strip()
        if err:
            out.write("[stderr] " + err[:600] + "\n")
        out.write("\n")
print("gates done ->", OUT)
