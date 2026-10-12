# -*- coding: utf-8 -*-
# R2088 close repair: restore the missing closing quote of the R2087 log line
# (insertion bug in r2088_close.py: comma landed before R2087's closing quote).
import sys, re
from datetime import datetime

P = 'src/os/state.json'
txt = open(P, 'rb').read().decode('utf-8')

old = 'R2047 行〕）,\n    "2026-10-13 00:48 R2088:'
new = 'R2047 行〕）",\n    "2026-10-13 00:48 R2088:'
if txt.count(old) != 1:
    print('ANCHOR-FAIL repair count=%d' % txt.count(old))
    sys.exit(1)
txt = txt.replace(old, new, 1)

ts_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
txt2, n = re.subn(r'"ts": "2026-10-13 00:4[0-9]:[0-9]{2}",',
                  '"ts": "' + ts_now + '",', txt, count=1)
if n != 1:
    print('ANCHOR-FAIL ts n=%d' % n)
    sys.exit(1)
txt = txt2

open(P, 'wb').write(txt.encode('utf-8'))

import json
d = json.loads(txt)
print('OK tick=%d ts=%s log_len=%d' % (d['tick'], d['ts'], len(d['log'])))
print('task_head=%s' % d['task'][:20])
print('last2_heads=%s | %s' % (d['log'][-2][:26], d['log'][-1][:26]))
