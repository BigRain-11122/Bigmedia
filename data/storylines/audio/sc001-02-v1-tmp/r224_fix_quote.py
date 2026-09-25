# -*- coding: utf-8 -*-
import io, json
p = r'src/os/state.json'
s = io.open(p, encoding='utf-8').read()
bad = '\n    2026-09-25 09:3x R224:'
assert bad in s, 'bad line anchor'
s = s.replace(bad, '\n    "2026-09-25 09:3x R224:', 1)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
d = json.load(io.open(p, encoding='utf-8'))
e = json.load(io.open(r'docs/status-export.json', encoding='utf-8'))
print('VALID tick', d['tick'], 'log', len(d['log']), 'last', d['log'][-1][:34], 'export_ts', e['export_ts'])
