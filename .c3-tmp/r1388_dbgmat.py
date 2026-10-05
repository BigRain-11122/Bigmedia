# -*- coding: utf-8 -*-
import io
t = io.open('data/storylines/cards/MC-20260905-DAILY-v67-tmp/e4_call.py', encoding='utf-8').read()
i = t.find(u'material')
seg = t[i:i+130]
io.open('.c3-tmp/r1388_dbg2.txt', 'w', encoding='utf-8').write(repr(seg))
probe = u"'material': 'MC-20260905-DAILY-v67 static card (cards.json + render output)'}"
io.open('.c3-tmp/r1388_dbg2.txt', 'a', encoding='utf-8').write(u"\nprobe_in=" + str(probe in t) + u"\nseg=" + repr(seg))
print('ok', probe in t)
