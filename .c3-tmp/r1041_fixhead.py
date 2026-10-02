# -*- coding: utf-8 -*-
"""Fix R1041 log line header: add missing HH:MMx segment so the line follows
the 'YYYY-MM-DD HH:MMx RNNN:' convention (loop_health parses log timestamps).
"""
import json, io, datetime

SP = r'src/os/state.json'
st = json.load(io.open(SP, encoding='utf-8'))
assert st['tick'] == 1041
last = st['log'][-1]
assert last.startswith('2026-10-03 R1041:'), 'unexpected head: %s' % last[:40]
hm = datetime.datetime.now().strftime('%H:%M') + 'x'
st['log'][-1] = last.replace('2026-10-03 R1041:', '2026-10-03 %s R1041:' % hm, 1)
io.open(SP, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=1))
print('fixed head=%s' % st['log'][-1][:40])
