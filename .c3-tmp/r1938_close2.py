# -*- coding: utf-8 -*-
"""R1938 close stage-2: state already finalized (tick=1938, first run);
first run failed at commit on a missing-file list error (launch logs had
landed in repo root, now moved into tmp dirs). This stage carries the
commit+push only. Self-inclusion law adds r1938_close.py (stage-1 script)
and this stage-2 script via tick-anchor autodetect.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "os"))
import close_commit as cc  # noqa: E402

FILES = [
    "src/os/state.json",
    "src/os/backlog.md",
    "state/queue/main.md",
    "state/queue/tech.md",
    "docs/status-export.json",
    "output/finished.md",
    "data/storylines/cards/README.md",
    "docs/reviews/station-reviews.md",
    "docs/reviews/expert-calls.md",
    "docs/reviews/review-20261010-mcdigest-v17.md",
    "docs/reviews/review-20261010-mcreact-v13.md",
    "docs/reviews/expert-verdicts/20261011-040541-E4-audience.md",
    "docs/reviews/expert-verdicts/20261011-041119-E4-audience.md",
    "docs/reviews/expert-verdicts/20261011-041115-S1-script.md",
    "data/storylines/cards/MC-20261010-DIGEST-v17-tmp/e4_call.py",
    "data/storylines/cards/MC-20261010-DIGEST-v17-tmp/e4-result.json",
    "data/storylines/cards/MC-20261010-DIGEST-v17-tmp/e4-launch.err",
    "data/storylines/cards/MC-20261010-REACT-v13-tmp/e4-result.json",
    "data/storylines/cards/MC-20261010-REACT-v13-tmp/e4-refly3-r1938.out",
    "data/storylines/cards/MC-20261010-REACT-v13-tmp/e4-refly3-r1938.err",
    ".c3-tmp/r1938_probes.txt",
    ".c3-tmp/sc004-s1/s1-out.txt",
    ".c3-tmp/sc004-s1/s1-err.txt",
]
MSG = ("R1938 close: review-leg wave all-landed - DIGEST v17 F-170 "
       "registered (assertions ALL GREEN + transcription 10/10 + M4.5 6x9 "
       "+ E4 8.0 backfill); SC-004-01 S1 10/10 zero-violation first "
       "audio-line pass (F-171 candidate); REACT-v13 E4 third flight 8.0 "
       "(R1847 TIMEOUT debt cleared); first real window = mv_probe quiet "
       "x gate GO x GEN-OK (tech#85 anchor); five checks quiet; probes "
       "in-band; export refreshed F-170 live line; #112 due 08:00 "
       "[via bm-a]")

rc, lines = cc.run_close_commit(FILES, MSG)
for ln in lines:
    print(ln)
print("CLOSE_RC", rc)
sys.exit(0 if rc == 0 else 1)
