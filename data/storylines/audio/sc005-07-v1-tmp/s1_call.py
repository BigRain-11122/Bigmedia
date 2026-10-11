#!/usr/bin/env python3
"""SC-005-07 S1 staged launcher (fire-window turnkey, R2008 prestage).

Pre-staged per the R1995/R1999 double window-loss gate: fire_consume.py
dispatches THIS file the moment the card says fire, so no material
discovery or command assembly ever happens inside the 120s TTL.

Flight: S1-script v1.5 gate on the SC-005-07 s1-material (C-00012
沈佩兰 season-2 opener, R2007 preload, F-180 pre-registered).
--gpu-guard defers cheaply if the window flips after dispatch (R1986
verdict-void law: an in-flight call that hit a flipped window is
discarded and re-dispatched, never trusted). Verdict auto-archives to
docs/reviews/expert-verdicts/<ts>-S1-script.md + expert-calls.md line
(call_expert single-writer).
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
OUT = Path(__file__).with_name("s1-run.out")
ERR = Path(__file__).with_name("s1-run.err")

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

MATERIAL = "data/storylines/audio/SC-005-07-v1-s1-material.md"
TIMEOUT_S = "1500"

with OUT.open("wb") as fo, ERR.open("wb") as fe:
    proc = subprocess.Popen(
        [sys.executable, "src/call_expert.py",
         "--expert", "S1-script",
         "--material", MATERIAL,
         "--timeout", TIMEOUT_S, "--gpu-guard"],
        cwd=str(REPO), stdout=fo, stderr=fe,
        creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
print("SC-005-07 S1 flight dispatched pid=%d" % proc.pid)
