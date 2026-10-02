# -*- coding: utf-8 -*-
"""R1017 pre-selection word-face machine probe for xiaoyao/festival FREE rows (2-char distinctive
words, card-face level R1010 law: lines + source_quote; city-spirit.md included)."""
import io, json, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
BASE = os.path.join(ROOT, 'data', 'storylines', 'cards')
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, 'cards.json')
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding='utf-8'))
        face = u'\n'.join(u'\n'.join(c.get('lines', [])) for c in cfg.get('cards', []))
        sq = cfg.get('meta', {}).get('source_quote', u'')
        faces[d] = (face, sq)
spirit = io.open(os.path.join(ROOT, 'data', 'storylines', 'codex', 'city-spirit.md'), encoding='utf-8').read()

CANDS = {
    5: (u'灯影交错映江面，好个逍遥自在天', [u'灯影', u'交错', u'映江面', u'江面', u'好个', u'逍遥自在', u'自在天']),
    9: (u'钓竿一甩乐逍遥', [u'钓竿', u'一甩', u'乐逍遥', u'垂钓', u'钓']),
    11: (u'鱼儿上钩喜出望外', [u'鱼儿', u'上钩', u'喜出望外', u'喜出']),
}
out = []
for idx, (ln, words) in sorted(CANDS.items()):
    out.append(u'=== line%d: %s ===' % (idx, ln))
    for w in words:
        hits = sorted(d for d, (f, sq) in faces.items() if w in f or w in sq)
        sp = u'HIT' if w in spirit else u'no'
        out.append(u'  word [%s] -> cards: %s | spirit: %s' % (w, u','.join(hits) if hits else u'ZERO', sp))
    out.append(u'')
io.open(os.path.join(ROOT, '.c3-tmp', 'r1017_wordface.txt'), 'w', encoding='utf-8').write(u'\n'.join(out))
print('done')
