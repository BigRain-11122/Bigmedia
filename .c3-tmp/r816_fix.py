# -*- coding: utf-8 -*-
# r816 fix: remove trailing comma introduced after the last "task" property (file-end only)
import io, json

P = r'src/os/state.json'
txt = io.open(P, encoding='utf-8').read()

bad = u'"\n}'          # correct ending (no comma)
tail_bad = u'",\n}'    # current corrupted ending
print('tail_bad count:', txt.count(tail_bad))
assert txt.endswith(tail_bad), 'unexpected file tail: %r' % txt[-20:]
assert txt.count(tail_bad) == 1, 'tail pattern not unique'

txt = txt[:-len(tail_bad)] + bad
io.open(P, 'w', encoding='utf-8', newline='\n').write(txt)

d = json.load(io.open(P, encoding='utf-8'))
print('FIX-OK tick=%d log_len=%d ts=%s' % (d['tick'], len(d['log']), d['ts']))
print('task=%s' % d['task'])
print('focus_head=%s' % d['focus'][:60])
print('last_log_head=%s' % d['log'][-1][:70])
