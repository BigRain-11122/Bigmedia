# -*- coding: utf-8 -*-
# R820 fix (applied in R821 round-open): remove illegal trailing comma after last-field task
# value left by r820_close.py (r817/r819 fix precedent; R820 close wrote the comma and its own
# json.load verification never ran to completion -> state left invalid for ~15 min)
import io, json

P = r'src/os/state.json'
txt = io.open(P, encoding='utf-8').read()

broken = u'留档 r807_sc",\n}'
assert txt.count(broken) == 1, 'broken tail anchor not unique: %d' % txt.count(broken)
txt = txt.replace(broken, u'留档 r807_sc"\n}')

io.open(P, 'w', encoding='utf-8', newline='\n').write(txt)

d = json.load(io.open(P, encoding='utf-8'))
assert d['tick'] == 820, 'tick assert fail: %s' % d['tick']
assert d['ts'] == '2026-10-01 08:08:06', 'ts assert fail: %s' % d['ts']
assert d['log'][-1].startswith('2026-10-01 08:08 R820:'), 'log append fail'
assert d['task'].startswith(u'等待态声明收轮·声明轮并窗第 4 轮'), 'task fail: %s' % d['task']
assert d['focus'].startswith('R820:'), 'focus fail: %s' % d['focus'][:30]
print('FIX-OK tick=%d log_len=%d ts=%s' % (d['tick'], len(d['log']), d['ts']))
print('task=%s' % d['task'])
print('last_log_head=%s' % d['log'][-1][:80])
