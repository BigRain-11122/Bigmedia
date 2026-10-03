# -*- coding: utf-8 -*-
# R1181 state.json trailing-comma fix: remove trailing comma after last log line.
import io, json
p = 'src/os/state.json'
lines = io.open(p, encoding='utf-8').read().split('\n')
target = None
for i, l in enumerate(lines):
    if l.lstrip().startswith('"2026-10-04 03:56 R1181:'):
        target = i
if target is None:
    raise SystemExit('R1181 log line not found')
assert lines[target].rstrip().endswith('",'), 'unexpected tail: %r' % lines[target][-12:]
assert lines[target+1].strip() == '],', 'next line not array close: %r' % lines[target+1]
lines[target] = lines[target].rstrip()[:-1]  # drop trailing comma, keep closing quote
io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
d = json.load(io.open(p, encoding='utf-8'))
print('OK tick=%s ts=%s log_lines=%d' % (d['tick'], d['ts'], len(d['log'])))
print('tail:', d['log'][-1][:60])
