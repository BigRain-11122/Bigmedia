# -*- coding: utf-8 -*-
# R808: S2 three-gate independent enforcement for bs-011-v1-shipinhao-60s.mp4
# (R806 s2 chain-inheritance; beats = v3 final trimmed track)
import subprocess, io

VID = r"output\renders\bs-011-v1-shipinhao-60s.mp4"
PLAN = VID + ".plan.json"
SRT = r".bs011-tmp\subs.srt"
BEATS = r"data\sources\bs011\voiceover-v3.beats.txt"
PLAT = "\u5fae\u4fe1\u89c6\u9891\u53f7"  # 微信视频号 (u-escape per R173 precedent)

out = io.open(r".c3-tmp\r808_s2.txt", "w", encoding="utf-8")

def run(name, cmd):
    r = subprocess.run(cmd, capture_output=True)
    txt = (r.stdout + b"\n" + r.stderr).decode("utf-8", "replace")
    out.write("==== %s exit=%d ====\n%s\n" % (name, r.returncode, txt))
    print("%s exit=%d" % (name, r.returncode))

run("ffprobe", ["ffprobe", "-v", "error", "-show_entries",
                "format=duration:stream=width,height,codec_type",
                "-of", "default=nw=1", VID])
run("ai_feel", ["python", "-X", "utf8", "src/ai_feel_check.py",
                "--beats", BEATS, "--srt", SRT])
run("spec", ["python", "-X", "utf8", "src/platform_spec_check.py",
             "--video", VID, "--platform", PLAT])
run("edit_craft", ["python", "-X", "utf8", "src/edit_craft_check.py",
                  "--plan", PLAN, "--srt", SRT, "--profile", "shipinhao"])
out.close()
print("S2DONE")
