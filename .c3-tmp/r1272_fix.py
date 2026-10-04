# -*- coding: utf-8 -*-
# R1272 fix: last log line got duplicated date prefix from replace chain; strip dup + recompute task field.
import json, io

P = r'src/os/state.json'
state = json.load(io.open(P, encoding='utf-8'))

last = state['log'][-1]
# expected single prefix "2026-10-04 HH:MM R1272:"
if last.startswith('2026-10-04 2026-10-04 '):
    last = last[len('2026-10-04 '):]
    state['log'][-1] = last

# recompute task = first 60 chars after the timestamp prefix "YYYY-MM-DD HH:MM "
ts_prefix = last[:len('2026-10-04 19:23 ')]
state['task'] = last[len(ts_prefix):][:60]

io.open(P, 'w', encoding='utf-8').write(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
print('line head: %s' % last[:80])
print('task len=%d ok' % len(state['task']))
# verify the waiting-tail distance segment survived correctly
import re
m = re.search(r'当前 \d\d:\d\d·距日界 ~[\d.]+h', last)
print('tail seg: %s' % (m.group(0) if m else 'MISSING'))
print('tick=%s ts=%s' % (state['tick'], state['ts']))
