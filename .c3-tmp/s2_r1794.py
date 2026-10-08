# -*- coding: utf-8 -*-
"""R1794 successor body: S2 three-gate enforcement for MD-0001 draft.
Gates: ai_feel_check, platform_spec_check (bilibili CJK via \\u), edit_craft_check.
ASCII rule; CJK lives in data files / u-escapes only.
"""
import subprocess
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

MD = "data/storylines/drama/md0001"
MP4 = "output/renders/md-0001-v1-bilibili-16x9.mp4"
PLAN = MP4 + ".plan.json"
BEATS = MD + "/tts/md0001-full.beats.txt"
SRT = MD + "/tts/md0001-full.srt"


def run(name, args):
    r = subprocess.run([sys.executable] + args, capture_output=True)
    out = r.stdout.decode("utf-8", errors="replace")
    err = r.stderr.decode("utf-8", errors="replace")
    print("=== %s (rc=%d) ===" % (name, r.returncode))
    print(out[-3500:])
    if err.strip():
        print("[stderr]", err[-800:])
    return r.returncode


rc1 = run("ai_feel_check",
          ["src/ai_feel_check.py", "--beats", BEATS, "--srt", SRT])
platform = "B\u7ad9"  # CJK platform name via u-escape (R173 law)
rc2 = run("platform_spec_check",
          ["src/platform_spec_check.py", "--video", MP4, "--platform", platform])
rc3 = run("edit_craft_check",
          ["src/edit_craft_check.py", "--plan", PLAN, "--srt", SRT,
           "--profile", "bilibili"])
print("GATE-RCS", rc1, rc2, rc3)
