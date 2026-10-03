# -*- coding: utf-8 -*-
"""R1132 close fix pass 2: remove trailing comma from R1132 log entry (last
array element must not carry trailing comma). ASCII-only source."""
import io, json

p = r'src/os/state.json'
lines = io.open(p, encoding='utf-8', newline='').readlines()
idx = [i for i, l in enumerate(lines) if l.lstrip().startswith('"2026-10-03 19:03x R1132:')][0]
print('idx', idx, 'ends', repr(lines[idx][-14:]))
body = lines[idx].rstrip('\r\n')
if body.endswith('",'):
    nl = '\r\n' if lines[idx].endswith('\r\n') else '\n'
    lines[idx] = body[:-1] + nl
    io.open(p, 'w', encoding='utf-8', newline='').writelines(lines)
    print('fixed ends', repr(lines[idx][-14:]))
else:
    print('no fix needed')

st = json.load(io.open(p, encoding='utf-8'))
print('VALID JSON: tick=%s ts=%s loglines=%d' % (st['tick'], st['ts'], len(st['log'])))
print('last log starts:', st['log'][-1][:40])
print('task:', st['task'])
