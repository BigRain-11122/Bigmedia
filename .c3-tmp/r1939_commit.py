# -*- coding: utf-8 -*-
"""R1939 close retry 2: explicit file-level list (tmp dir expanded; no -A)."""
import os
import sys
sys.path.insert(0, "src/os")

from close_commit import run_close_commit  # noqa: E402

TMP = "data/storylines/audio/sc004-01-v1-tmp"
FILES = [
    "data/storylines/audio/README.md",
    "data/storylines/audio/SC-004-01-v1.srt",
    "state/queue/main.md",
    "state/queue/tech.md",
    ".c3-tmp/same_text_r1939.py",
    ".c3-tmp/r1939_same_text.txt",
    "src/os/state.json",
]
for name in sorted(os.listdir(TMP)):
    p = os.path.join(TMP, name)
    if os.path.isfile(p):
        FILES.append(p.replace("\\", "/"))

MSG = ("R1939 SC-004-01 Taifeng audio first pass: TTS light 236.41s 17 cues, same-text 17/17 miss0, "
       "ai_feel 0F0W, M4 pass, ledger row raised (F-171 next); tech#87 restock [via bm-a]")

rc, lines = run_close_commit(files=FILES, message=MSG)
for ln in lines:
    print(ln.encode("ascii", "backslashreplace").decode("ascii"))
print("RC=%d NFILES=%d" % (rc, len(FILES)))
sys.exit(rc)
