# -*- coding: utf-8 -*-
import io, json, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
BASE = os.path.join(ROOT, 'data', 'storylines', 'cards')
out = io.StringIO()
def u(s): out.write(str(s) + '\n')

pool = json.load(io.open(os.path.join(ROOT, '..', '..', 'life', 'BigLife', 'cognition', 'pools.json'), encoding='utf-8'))
fest = pool['axes'][u'求新'][u'festival']
u(u'=== qiuxin/festival bucket (%d lines) ===' % len(fest))
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, 'cards.json')
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding='utf-8'))
        face = u'\n'.join(u'\n'.join(c.get('lines', [])) for c in cfg.get('cards', []))
        sq = cfg.get('meta', {}).get('source_quote', u'')
        faces[d] = (face, sq)
spirit = io.open(os.path.join(ROOT, 'data', 'storylines', 'codex', 'city-spirit.md'), encoding='utf-8').read()
used = {4: u'DAILY-v1', 7: u'DAILY-v7', 12: u'DAILY-v9', 3: u'DAILY-v14', 11: u'DAILY-v15', 13: u'DAILY-v23', 5: u'DAILY-v37', 9: u'DAILY-v43', 14: u'city-spirit-v1.2'}
for i, ln in enumerate(fest):
    tag = used.get(i, u'FREE')
    hits = [d for d, (f, sq) in faces.items() if ln in f or ln in sq]
    u(u'%2d [%s] %s | full-line hits: %s | spirit: %s' % (i, tag, ln, u','.join(hits) if hits else u'NONE', u'HIT' if ln in spirit else u'no'))

u(u'=== FREE rows shingle probe (3-5 char shingles vs fleet faces) ===')
for i, ln in enumerate(fest):
    if i in used:
        continue
    core = ln.strip(u'，。,.！？')
    sh = set()
    for n in (3, 4, 5):
        for j in range(len(core) - n + 1):
            s = core[j:j + n]
            if u'，' in s or u'。' in s:
                continue
            sh.add(s)
    hits = {}
    for s in sorted(sh):
        h = [d for d, (f, sq) in faces.items() if s in f or s in sq]
        if h:
            hits[s] = h
    u(u'--- line%d: %s' % (i, ln))
    if hits:
        for s, h in sorted(hits.items()):
            u(u'    shingle [%s] -> %s' % (s, u','.join(h)))
    else:
        u(u'    all shingles ZERO fleet hits')

io.open(os.path.join(ROOT, '.c3-tmp', 'r1018_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('done')
