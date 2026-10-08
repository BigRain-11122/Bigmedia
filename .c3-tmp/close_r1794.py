# -*- coding: utf-8 -*-
"""R1794 close: explicit-file git add + commit + push (real git.exe law)."""
import subprocess
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
GIT = r"C:\Program Files\Git\cmd\git.exe"

FILES = [
    "output/renders/README.md",
    "output/renders/md-0001-v1-bilibili-16x9.mp4.plan.json",
    "docs/reviews/station-reviews.md",
    "src/os/backlog.md",
    "src/os/state.json",
    "docs/status-export.json",
    "data/storylines/drama/md0001/tts/md0001-full.beats.txt",
    "data/storylines/drama/md0001/tts/md0001-full.srt",
    ".c3-tmp",  # whole loop-tmp domain: asm-r1794/ + r1793/r1794 helpers
]

MSG = ("R1794: #108 MD-0001 drama PoC assembly leg closed (broken-round "
       "absorb: prior body 06:22-06:57 full assembly then 25min kill at "
       "06:57; this body ran S2 gates + 3-law frame verify + ledgers) - "
       "draft md-0001-v1-bilibili-16x9.mp4 75.84s; ai_feel 0F0W, "
       "edit-craft 0F1W PASS, spec duration FAIL recorded (60-90s episode "
       "charter vs 180-900s platform window); E8/M4/F next [via bm-a]")


def run(args, label):
    r = subprocess.run([GIT] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    print("==", label, "rc=", r.returncode)
    out = (r.stdout or "") + (r.stderr or "")
    print(out.strip()[-1500:])
    if r.returncode != 0:
        sys.exit(3)


run(["add"] + FILES, "add")
run(["commit", "-m", MSG], "commit")
run(["push"], "push")
run(["status", "--short"], "status")
run(["log", "--oneline", "-3"], "log")
