# -*- coding: utf-8 -*-
"""R1987 round close stage B: state accounting commit (tick 1987) +
self-include (r1987_close.py via autodetect) + SC-005-04 tmp absorption
(S1 burn trail + R1985 stray check scripts = fire-window consumption
handoff per R1985/R1986 notes). MV session domain files untouched.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..", "src", "os")))

from close_commit import run_close_commit  # noqa: E402

DELIVERABLES = [
    "src/os/state.json",
    ".c3-tmp/r1987_close2.py",
    "data/storylines/audio/sc005-04-v1-tmp/asr_diff_r1985.py",
    "data/storylines/audio/sc005-04-v1-tmp/same_text_r1985.py",
    "data/storylines/audio/sc005-04-v1-tmp/s1-retry.err",
    "data/storylines/audio/sc005-04-v1-tmp/s1-retry.out",
    "data/storylines/audio/sc005-04-v1-tmp/s1-run.err",
    "data/storylines/audio/sc005-04-v1-tmp/s1-run.out",
    "data/storylines/audio/sc005-04-v1-tmp/s1-run2.err",
    "data/storylines/audio/sc005-04-v1-tmp/s1-run2.out",
]


def main():
    rc, lines = run_close_commit(
        files=DELIVERABLES,
        message=("R1987 state accounting: tick 1987, tech#106 close "
                 "(comfy_activity C-43 live), S1 timeout carryover "
                 "consumed (chain at gate, zero false-green); absorb "
                 "SC-005-04 tmp S1 burn trail + R1985 stray check "
                 "scripts (fire-window consumption handoff); MV "
                 "session domain files untouched [via bm-a]"),
    )
    for ln in lines:
        print(ln.encode("ascii", "replace").decode("ascii"))
    return rc


if __name__ == "__main__":
    sys.exit(main())
