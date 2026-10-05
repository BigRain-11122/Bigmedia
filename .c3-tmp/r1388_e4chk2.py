# -*- coding: utf-8 -*-
import io
t = io.open('data/storylines/cards/MC-20261005-DAILY-v68-tmp/e4_call.py', encoding='utf-8').read()
out = []
for c in (u'城市日签 067', u'侠气轴声口', u'前六十六张', u'侠气轴', u'茶余饭后讲讲闲话，才不闷/'):
    idx = t.find(c)
    seg = t[max(0, idx-60):idx+80] if idx >= 0 else u'---'
    out.append(u'[%s] %d :: %s' % (c, idx, seg))
io.open('.c3-tmp/r1388_e4chk2.txt', 'w', encoding='utf-8').write(u'\n=====\n'.join(out))
print('ok')
