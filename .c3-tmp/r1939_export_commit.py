# -*- coding: utf-8 -*-
"""R1939 close stage-2b: export refresh commit (canonical writer output + evidence)."""
import sys
sys.path.insert(0, "src/os")

from close_commit import run_close_commit  # noqa: E402

FILES = [
    "docs/status-export.json",
    ".c3-tmp/r1939_export_patch.json",
    ".c3-tmp/r1939_commit.py",
]

MSG = "R1939 export refresh via canonical writer (live lines plain-speak SC-004-01 audio first pass) [via bm-a]"

rc, lines = run_close_commit(files=FILES, message=MSG)
for ln in lines:
    print(ln.encode("ascii", "backslashreplace").decode("ascii"))
print("RC=%d" % rc)
sys.exit(rc)
