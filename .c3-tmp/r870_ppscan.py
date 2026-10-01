# -*- coding: utf-8 -*-
import json, io, re
d = json.load(io.open('src/os/state.json', encoding='utf-8'))
first = None
cnt = 0
rows = []
for l in d['log']:
    m = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) R(\d+): ', l)
    if m and 'P-2026-09-29-07' in l:
        cnt += 1
        if first is None:
            first = (m.group(1), m.group(2), l[:800])
        rows.append('%s R%s' % (m.group(1), m.group(2)))
io.open('.c3-tmp/r870_pp.txt', 'w', encoding='utf-8').write(
    'count=%d\nALL ROUNDS: %s\n\nFIRST FULL:\n%s' % (cnt, ', '.join(rows), first[2] if first else ''))
print('count=%d' % cnt)
