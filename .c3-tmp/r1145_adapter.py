# -*- coding: utf-8 -*-
# R1145 adapter: derive r1145_state.py from r1144_state.py (anchor bump only).
import io

src = io.open('.c3-tmp/r1144_state.py', encoding='utf-8').read()
reps = [
    ('r1144_payload.txt', 'r1145_payload.txt'),
    ('R1144 declared-idle', 'R1145 declared-idle'),
    ('assert st["tick"] == 1143', 'assert st["tick"] == 1144'),
    ('"log"][-1].startswith("2026-10-03 20:55 R1143")', '"log"][-1].startswith("2026-10-03 21:07 R1144")'),
    ('assert st["ts"] == "2026-10-03 20:55:40"', 'assert st["ts"] == "2026-10-03 21:07:43"'),
    ('a = \'"tick": 1143,', 'a = \'"tick": 1144,'),
    ("raw.replace(a, '\"tick\": 1144,", "raw.replace(a, '\"tick\": 1145,"),
    ('anchor = \'"\\n  ],\\n  "ts": "2026-10-03 20:55:40",', 'anchor = \'"\\n  ],\\n  "ts": "2026-10-03 21:07:43",'),
    ('wa = \'\\n  "ts": "2026-10-03 20:55:40",\\n    "law":\'', 'wa = \'\\n  "ts": "2026-10-03 21:07:43",\\n    "law":\''),
    ('assert chk["tick"] == 1144', 'assert chk["tick"] == 1145'),
    ('starts with "R1144:"', 'starts with "R1145:"'),
]
for a, b in reps:
    if a not in src:
        raise SystemExit('MISSING ANCHOR: %r' % a)
    src = src.replace(a, b)
io.open('.c3-tmp/r1145_state.py', 'w', encoding='utf-8').write(src)
print('written ok')
