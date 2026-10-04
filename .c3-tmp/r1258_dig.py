# -*- coding: utf-8 -*-
# r1258 dig: R1123 / R1032 exhaustion adjudication segments (why-are-100-free-weekend-lines-not-supply)
import json, io

d = json.load(io.open('src/os/state.json', encoding='utf-8'))
log = d['log']
out = []
for tag in ['R1123', 'R1032']:
    e = [x for x in log if (' ' + tag + ':') in x[:26]]
    out.append('=== %s entries=%d ===' % (tag, len(e)))
    t = e[0] if e else ''
    i = t.find(u'\u67af\u7aed')  # kujie
    out.append('len=%d kujie_idx=%d' % (len(t), i))
    out.append(t[max(0, i-1500):i+2200] if i >= 0 else t[:2500])
    out.append('')
io.open('.c3-tmp/r1258_kujie2.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok')
