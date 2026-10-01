# -*- coding: utf-8 -*-
# R817 fix: strip trailing comma from task line (last JSON member; r816_fix.py precedent)
import io, json

P = r'src/os/state.json'
txt = io.open(P, encoding='utf-8').read()
lines = txt.split('\n')
ti = [i for i, l in enumerate(lines) if l.startswith(u'  "task": "')]
assert len(ti) == 1, 'task anchor not unique'
l = lines[ti[0]]
assert l.endswith(u'",'), 'task line does not end with comma'
lines[ti[0]] = l[:-1]
txt = '\n'.join(lines)
io.open(P, 'w', encoding='utf-8', newline='\n').write(txt)

d = json.load(io.open(P, encoding='utf-8'))
assert d['tick'] == 817, 'tick assert fail'
assert d['ts'], 'ts empty'
print('FIX-OK tick=%d log_len=%d ts=%s' % (d['tick'], len(d['log']), d['ts']))
print('task=%s' % d['task'])
print('last_log_head=%s' % d['log'][-1][:80])
print('focus_head=%s' % d['focus'][:60])
