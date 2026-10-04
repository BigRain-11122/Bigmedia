# -*- coding: utf-8 -*-
# r1258 dig2: night-window (ye chuang) candidate supply state post-v64 - did any round adjudicate 10-04 night window?
import json, io

d = json.load(io.open('src/os/state.json', encoding='utf-8'))
log = d['log']
out = []
# find entries mentioning night-window after R1123 (v64 produced 10-03 17:37)
hits = []
for x in log:
    head = x[:26]
    if (u'\u591c\u7a97' in x) or (u'\u591c\u665a' in x and u'\u5019\u9009' in x):
        hits.append(x)
out.append('night-window mentions: %d' % len(hits))
# print the ones around R1122/R1123 and any AFTER R1123 that adjudicate the next night window
for x in hits:
    rn = x[:26]
    out.append('--- %s' % rn)
    # print segment around the night-window term
    i = x.find(u'\u591c\u7a97')
    out.append(x[max(0, i-200):i+900])
    out.append('')
io.open('.c3-tmp/r1258_yechuang.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('mentions=%d' % len(hits))
