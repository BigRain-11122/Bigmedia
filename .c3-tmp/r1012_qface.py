# -*- coding: utf-8 -*-
"""R1012 quote-face word precheck for DAILY v43 candidate (qiuxin/festival/9)."""
import io, os, re, json

BASE = os.path.join('data', 'storylines', 'cards')
quote = u'这灯串串的，就像夜空的星星'
keys = [u'灯串', u'夜空', u'星星', u'就像', u'串串', u'这灯', u'像极了']
hits = {k: [] for k in keys}
spirit = io.open(os.path.join('data', 'storylines', 'codex', 'city-spirit.md'), encoding='utf-8').read()
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, 'cards.json')
    if os.path.isfile(cj):
        try:
            cfg = json.load(io.open(cj, encoding='utf-8'))
            sq = cfg.get('meta', {}).get('source_quote', u'')
        except Exception:
            sq = u''
        for k in keys:
            if k in sq:
                hits[k].append(d + ':' + sq)
for k in keys:
    if k in spirit:
        hits[k].append('CITY-SPIRIT')
out = io.open(os.path.join('.c3-tmp', 'r1012_quote_face.txt'), 'w', encoding='utf-8')
out.write('QUOTE: ' + quote + '\n')
for k in keys:
    if hits[k]:
        out.write(u'%s -> HIT %s\n' % (k, '; '.join(hits[k][:6])))
    else:
        out.write(u'%s -> ZERO fleet source_quote hits\n' % k)
out.close()
print('done')
