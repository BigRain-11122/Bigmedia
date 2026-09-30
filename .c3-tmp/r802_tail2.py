# -*- coding: utf-8 -*-
# r802: dump last 500 chars of R801 log line (pointer section only)
import io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
st = json.loads(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), 'r', encoding='utf-8-sig').read())
line = [x for x in st['log'] if x.startswith('2026-10-01 02') and 'R801' in x[:60]][-1]
io.open(os.path.join(HERE, 'r802_r801tail2.txt'), 'w', encoding='utf-8').write(u'...tail500>>> ' + line[-500:] + u'\n')
print('OK')
