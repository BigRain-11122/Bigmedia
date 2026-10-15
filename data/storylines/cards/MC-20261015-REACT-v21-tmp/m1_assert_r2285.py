# -*- coding: utf-8 -*-
"""M1 verbatim assertions for MC-20261015-REACT-v21 (R2285)."""
import json, io, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
CARDS = os.path.join(HERE, '..', 'MC-20261015-REACT-v21', 'cards.json')
OUT = os.path.join(HERE, '..', 'MC-20261015-REACT-v21', 'm1-assert-r2285.txt')

d = json.load(io.open(os.path.abspath(CARDS), encoding='utf-8'))
lines = d['cards'][0]['lines']
res = []

def ck(name, cond, detail=''):
    res.append(('PASS' if cond else 'FAIL') + '  ' + name + (('  ' + detail) if detail else ''))

# 1) hot topic verbatim == daily brief zhihu #8 entry
brief = io.open('data/intel/daily/2026-10-15.md', encoding='utf-8').read()
m = re.search(r'8\. (如何看待二本毕业女生待业一年[^\n]+)\n +- 192 万热度', brief)
hot_full = m.group(1).strip() if m else ''
hot1, hot2 = lines[2], lines[3]
ck('daily-brief zhihu #8 located', bool(hot_full), hot_full[:40])
ck('HOT1+HOT2 == HOT_FULL (split-preserve assertion)', hot1 + hot2 == hot_full,
   'HOT1=%d HOT2=%d FULL=%d' % (len(hot1), len(hot2), len(hot_full)))

# 2) three axis lines verbatim in BigLife pools weekend bucket
pools = json.load(io.open(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json', encoding='utf-8'))
for ax, ln in [('秩序', lines[4]), ('怀旧', lines[5]), ('侠气', lines[6])]:
    inner = ln.split('\uff1a\u300c')[1].rstrip('\u300d')
    ck('axis %s verbatim in weekend bucket' % ax, inner in pools['axes'][ax]['weekend'], inner[:20])

# 3) closing creed verbatim == C-00018 anchor creed
anchor = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00018.md', encoding='utf-8').read()
m = re.search(r'\*\*\u4fe1\u6761\*\* \u300c(.+?)\u300d', anchor)
creed = m.group(1) if m else ''
closing = lines[7]
ck('creed verbatim == C-00018 anchor', ('\u300c%s\u300d' % creed) in closing and closing.startswith('\u50cf\u7d20\u753b\u5320\u4fe1\u6761\uff1a'), creed)

# 4) line-level collision: quoted inner content (axis/creed/hot lines) vs fleet card faces
# boilerplate date-stamp/source lines are legal same-text across same-day cards (v17/v18/v19 precedent)
hits = []
for f in glob.glob(r'data\storylines\cards\MC-*\cards.json'):
    if 'REACT-v21' in f:
        continue
    try:
        o = json.load(io.open(f, encoding='utf-8'))
    except Exception:
        continue
    for c in o.get('cards', []):
        for l in c.get('lines', []):
            if '\u300c' not in l:
                continue
            for ml in lines:
                if '\u300c' in ml and ml == l:
                    hits.append((os.path.basename(os.path.dirname(f)), ml[:24]))
ck('fleet line-collision zero (quoted content lines)', not hits, str(hits[:4]))

# 5) closing creed text not used in any REACT closing (rotation law)
used = []
for f in glob.glob(r'data\storylines\cards\MC-*-REACT-v*\cards.json'):
    if 'REACT-v21' in f:
        continue
    o = json.load(io.open(f, encoding='utf-8'))
    if o['cards'][0]['lines'] and creed in o['cards'][0]['lines'][-1]:
        used.append(os.path.basename(os.path.dirname(f)))
ck('creed unused in REACT v1-v20 closings (rotation)', not used, str(used))

# 6) single bucket discipline: three axis lines all from weekend bucket only
ck('single-bucket discipline (weekend only)', all(
    l.split('\uff1a\u300c')[1].rstrip('\u300d') in pools['axes'][ax]['weekend']
    for ax, l in [('秩序', lines[4]), ('怀旧', lines[5]), ('侠气', lines[6])]))

# 7) no personal name on card face (charter v1.2 signature law)
personal = ['\u7f57\u5927\u58ee', '\u82cf\u6893\u6db5', '\u4f55\u96e8\u6b23', '\u9648\u96c5\u969b']
ck('zero personal name on face (axis/occupation-level only)', not any(p in l for l in lines for p in personal))

io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(res) + '\n')
print('\n'.join(res))
import sys
sys.exit(0 if all(r.startswith('PASS') for r in res) else 1)
