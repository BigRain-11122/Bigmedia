# -*- coding: utf-8 -*-
import io, json, os, glob

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
BASE = os.path.join(ROOT, 'data', 'storylines', 'cards')
out = io.StringIO()
def w(s): out.write(unicode(s) if False else str(s))
def u(s): out.write(s + u'\n')

pool = json.load(io.open(os.path.join(ROOT, '..', '..', 'life', 'BigLife', 'cognition', 'pools.json'), encoding='utf-8'))
fest = pool['axes'][u'逍遥'][u'festival']
u(u'=== xiaoyao/festival bucket (%d lines) ===' % len(fest))
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, 'cards.json')
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding='utf-8'))
        face = u'\n'.join(u'\n'.join(c.get('lines', [])) for c in cfg.get('cards', []))
        sq = cfg.get('meta', {}).get('source_quote', u'')
        faces[d] = (face, sq)
spirit = io.open(os.path.join(ROOT, 'data', 'storylines', 'codex', 'city-spirit.md'), encoding='utf-8').read()
used = {3: u'DAILY-v6', 15: u'DAILY-v12', 1: u'DAILY-v18', 2: u'DAILY-v29', 4: u'DAILY-v31', 16: u'DAILY-v36', 13: u'DAILY-v42', 17: u'REACT-v8'}
for i, ln in enumerate(fest):
    tag = used.get(i, u'FREE')
    hits = [d for d, (f, sq) in faces.items() if ln in f or ln in sq]
    u(u'%2d [%s] %s | full-line hits: %s | spirit: %s' % (i, tag, ln, u','.join(hits) if hits else u'NONE', u'HIT' if ln in spirit else u'no'))

# per FREE line: probe every 2+ char segment (3-6 char shingles) for word-face hits
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

u(u'=== cards README tail ===')
t = io.open(os.path.join(BASE, 'README.md'), encoding='utf-8').read().splitlines()
for l in t[-6:]:
    u(l[:600])

u(u'=== finished.md tail ===')
t = io.open(os.path.join(ROOT, 'output', 'finished.md'), encoding='utf-8').read().splitlines()
for l in t[-30:]:
    u(l[:600])

u(u'=== v47 review file ===')
for f in sorted(glob.glob(os.path.join(ROOT, 'docs', 'reviews', 'review-20261002-mcdaily-v47*'))):
    u(u'--- %s ---' % os.path.basename(f))
    for l in io.open(f, encoding='utf-8').read().splitlines():
        u(l[:300])

io.open(os.path.join(ROOT, '.c3-tmp', 'r1017_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('done')
