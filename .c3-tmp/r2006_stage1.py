# -*- coding: utf-8 -*-
"""R2006 stage-1 delivery commit (two-stage close law, os-protocol 6:
delivery files land first so a killed tail loses at most the state
accounting, never the delivery). Explicit-list + pathspec law via the
canonical run_close_commit."""
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "src", "os"))
sys.path.insert(0, os.path.join(REPO, "src"))

import close_commit  # noqa: E402

FILES = [
    os.path.join("src", "os", "loop_health.py"),
    os.path.join("tests", "test_loop_health.py"),
    os.path.join("docs", "capabilities.md"),
    os.path.join("state", "queue", "tech.md"),
    os.path.join(".c3-tmp", "r2006_probes.txt"),
    os.path.join(".c3-tmp", "r2006_probes2.txt"),
]

MESSAGE = (
    "R2006 delivery: tech#114 audio tmp residue guard in loop_health "
    "(audio-tmp-residue face, 8 tests) + untracked listing "
    "exclude-standard correction (tech#64 'respects .gitignore' false "
    "claim closed - ignored files never read as residue; R1900 pyc + "
    "sc001-01-v4-tmp wav double evidence); capabilities v1.101; tech "
    "queue done mark + #115 seed [via bm-a]"
)

rc, lines = close_commit.run_close_commit(FILES, MESSAGE, root=REPO)
for line in lines:
    print(line)
print("STAGE1_RC", rc)
sys.exit(0 if rc == 0 else 1)
