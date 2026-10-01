# -*- coding: utf-8 -*-
import json, io, re
d = json.load(io.open('src/os/state.json', encoding='utf-8'))
hits = []
for l in d['log']:
    m = re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2} R(\d+): ', l)
    if m and 'DIGEST' in l and int(m.group(1)) >= 683:
        hits.append((int(m.group(1)), l))
out = '\n\n'.join('R%d :: %s' % (r, l[:400]) for r, l in hits[-12:]) or 'NO DIGEST MENTIONS R683+'
io.open('.c3-tmp/r870_dig.txt', 'w', encoding='utf-8').write(out)
print('hits=%d' % len(hits))
