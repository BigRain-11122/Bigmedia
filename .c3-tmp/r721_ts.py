# -*- coding: utf-8 -*-
import io, json, time
p = 'src/os/state.json'
s = io.open(p, encoding='utf-8').read()
old = '"ts": "2026-09-30 03:44:49"'
new = '"ts": "%s"' % time.strftime('%Y-%m-%d %H:%M:%S')
assert old in s, 'ts anchor missing'
s = s.replace(old, new, 1)
json.loads(s)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ts ->', new)
