# -*- coding: utf-8 -*-
# R1275 fix: collapse double date prefix in last log line, recompute task field (offset bug, R1272~R1274_fix.py same pattern).
import json, io, datetime

P = r'src/os/state.json'
state = json.load(io.open(P, encoding='utf-8'))
last = state['log'][-1]
bad = '2026-10-04 2026-10-04 19:53 R1275:'
good = '2026-10-04 19:53 R1275:'
assert bad in last, 'unexpected prefix: ' + last[:60]
state['log'][-1] = last.replace(bad, good, 1)
prefix = '2026-10-04 19:53 '
state['task'] = state['log'][-1][len(prefix):][:60]
io.open(P, 'w', encoding='utf-8').write(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
print('log[-1][:60]=', state['log'][-1][:60])
print('task=', state['task'])
print('ts=', state['ts'], 'tick=', state['tick'])
