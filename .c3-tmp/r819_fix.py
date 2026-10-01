# -*- coding: utf-8 -*-
# R819 fix: remove illegal trailing comma after last-field task value (my transcription bug in r819_close.py step 3)
import io, json

P = r'src/os/state.json'
txt = io.open(P, encoding='utf-8').read()

broken = u'留档 r807_sc",\n}'
assert txt.count(broken) == 1, 'broken tail anchor not unique: %d' % txt.count(broken)
txt = txt.replace(broken, u'留档 r807_sc"\n}')

io.open(P, 'w', encoding='utf-8', newline='\n').write(txt)

d = json.load(io.open(P, encoding='utf-8'))
assert d['tick'] == 819, 'tick assert fail'
assert d['ts'] == '2026-10-01 07:55:41', 'ts assert fail: %s' % d['ts']
assert d['log'][-1].startswith('2026-10-01 07:55 R819:'), 'log append fail'
assert d['task'].startswith(u'等待态声明收轮·声明轮并窗第 3 轮'), 'task fail: %s' % d['task']
assert d['focus'].startswith('R819:'), 'focus fail: %s' % d['focus'][:30]
print('FIX-OK tick=%d log_len=%d ts=%s' % (d['tick'], len(d['log']), d['ts']))
print('task=%s' % d['task'])
print('focus_head=%s' % d['focus'][:80])
print('last_log_head=%s' % d['log'][-1][:100])
