# -*- coding: utf-8 -*-
import json, io, re
d = json.load(io.open('src/os/state.json', encoding='utf-8'))
out = []
for l in d['log']:
    m = re.match(r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) R(\d+): ', l)
    if not m:
        continue
    date, hhmm, r = m.group(1), m.group(2), int(m.group(3))
    if date >= '2026-09-29' and r >= 683:
        # keep only round headers with round-start facts (first 900 chars) for rounds that are NOT waiting-declarations
        if '等待态声明收轮' not in l[:80]:
            out.append('R%d %s %s :: %s' % (r, date, hhmm, l[:700]))
io.open('.c3-tmp/r870_active.txt', 'w', encoding='utf-8').write('\n\n'.join(out))
print('active_rounds=%d' % len(out))
