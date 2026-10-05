# -*- coding: utf-8 -*-
import json, io
d = json.load(io.open('src/os/state.json', encoding='utf-8'))
ls = [l for l in d['log'] if l.startswith('2026-10-05')]
WEEK = "\u5468\u62a5"  # zhou-bao weekly report
hits = [l[:420] for l in ls if ('W41' in l and (WEEK in l or 'weekly' in l or 'CLOUD_LINE' in l or '#94' in l))]
out = io.open('.c3-tmp/r1382_w41.txt', 'w', encoding='utf-8')
tail = hits[-6:] if len(hits) > 6 else hits
out.write('\n\n'.join(tail))
out.close()
print('today_lines=%d hits=%d' % (len(ls), len(hits)))
