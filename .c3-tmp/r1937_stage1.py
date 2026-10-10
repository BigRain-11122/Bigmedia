# -*- coding: utf-8 -*-
"""R1937 stage-1: deliverables pre-commit (tech#27 two-stage law)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "os"))
import close_commit as cc  # noqa: E402

FILES = [
    "src/os/mv_sprint_probe.py",
    "tests/test_mv_sprint_probe.py",
    "state/queue/tech.md",
    "docs/capabilities.md",
    "data/pipeline/mv-sprint-probe-ledger.jsonl",
    ".c3-tmp/r1937_probes.txt",
]
MSG = ("R1937 deliver: tech#86 mv_sprint_probe --ledger JSONL ledger face "
       "(one row per run, five-field exact set ts/verdict/rc/newest_age_min/"
       "threshold_min, error runs get their row too = fail-closed is data, "
       "bare flag default data/pipeline/mv-sprint-probe-ledger.jsonl, "
       "best-effort WARN never changes rc, parent auto-created; judgment "
       "position now cites the ledger tail line; 8 new tests, suite 910 "
       "green 90.5s rc=0; live dogfood two real runs field-identical; dual "
       "reading this round: file face quiet x gate NO-GO free 579 ComfyUI "
       "busy = four legs stay gated; tech#85 stays gated on first real "
       "window; meme V1 mp4 not landed) [via bm-a]")

rc, lines = cc.run_close_commit(FILES, MSG)
for ln in lines:
    print(ln)
print("STAGE1_RC", rc)
sys.exit(0 if rc == 0 else 1)
