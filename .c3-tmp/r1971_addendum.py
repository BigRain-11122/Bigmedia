# -*- coding: utf-8 -*-
# R1971 addendum: commit probe evidence + export patch artifacts.
import io
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)
sys.path.insert(0, os.path.join(BASE, 'src', 'os'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import close_commit as cc  # noqa: E402

FILES = [
    os.path.join('.c3-tmp', 'r1971_probes.txt'),
    os.path.join('.c3-tmp', 'r1971_export_patch.json'),
    os.path.join('.c3-tmp', 'r1971_addendum.py'),
]
rc, lines = cc.run_close_commit(FILES, "R1971 addendum: probe evidence (board 0 fail / readiness 3 external-CEO blockers "
                                        "0 findings / loop_health 2F both adjudicated outages, drift 16 in-band) + export "
                                        "patch artifact; next: SC-005-04 F-176 on next fire window [via bm-a]")
for ln in lines:
    print(ln)
print('rc=%d' % rc)
