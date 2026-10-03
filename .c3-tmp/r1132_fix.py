# -*- coding: utf-8 -*-
"""R1132 close fix: append trailing comma to R1131 log entry (was last array
element before R1132 line insert). ASCII-only source."""
import io

p = r'src/os/state.json'
lines = io.open(p, encoding='utf-8', newline='').readlines()
idx = [i for i, l in enumerate(lines) if l.lstrip().startswith('"2026-10-03 18:5x R1131:')][0]
print('idx', idx, 'ends', repr(lines[idx][-12:]))
body = lines[idx].rstrip('\r\n')
if body.endswith('"') and not body.endswith('",'):
    nl = '\r\n' if lines[idx].endswith('\r\n') else '\n'
    lines[idx] = body + ',' + nl
    io.open(p, 'w', encoding='utf-8', newline='').writelines(lines)
    print('fixed ends', repr(lines[idx][-14:]))
else:
    print('no fix needed')

import json
st = json.load(io.open(p, encoding='utf-8'))
print('tick=%s ts=%s loglines=%d' % (st['tick'], st['ts'], len(st['log'])))
print('last log starts:', st['log'][-1][:40])
