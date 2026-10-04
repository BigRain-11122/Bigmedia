# -*- coding: utf-8 -*-
# R1274 fix: strip duplicated date prefix in last log line (R1272/R1273 same-type bug), recompute task field.
import json, io, re

P = r'src/os/state.json'
state = json.load(io.open(P, encoding='utf-8'))
last = state['log'][-1]

# strip duplicated leading date "2026-10-04 " before the real "2026-10-04 19:44 R1274" stamp
m = re.match(r'^(2026-10-04) (2026-10-04 \d\d:\d\d R1274: )', last)
if m:
    last = last[len('2026-10-04 '):]
    state['log'][-1] = last

# recompute task = first 60 chars after the timestamp prefix "YYYY-MM-DD HH:MM "
ts_prefix = last[:len('2026-10-04 19:44 ')]
state['task'] = last[len(ts_prefix):][:60]

io.open(P, 'w', encoding='utf-8').write(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
print('line head: %s' % last[:50])
print('task len=%d ok' % len(state['task']))
# verify the waiting-tail distance segment survived correctly
m2 = re.search(r'当前 \d\d:\d\d·距日界 ~[\d.]+h', last)
print('tail seg: %s' % (m2.group(0) if m2 else 'MISSING'))
print('tick=%s ts=%s' % (state['tick'], state['ts']))
