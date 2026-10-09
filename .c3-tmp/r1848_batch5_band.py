import json, re, os

BIGLIFE = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife'
cur = json.load(open(os.path.join(BIGLIFE, 'cognition', 'pools.json'), encoding='utf-8'))

pool_lines = []
for axis, scenes in cur['axes'].items():
    for scene, ls in scenes.items():
        for ln in ls:
            pool_lines.append((axis, scene, ln.strip()))
for scene, ls in cur['sprite'].items():
    for ln in ls:
        pool_lines.append(('像素灵', scene, ln.strip()))
uniq = {}
for axis, scene, ln in pool_lines:
    uniq.setdefault(ln, (axis, scene))
OUT = []
A = OUT.append
A('total_flat=%d unique=%d' % (len(pool_lines), len(uniq)))

# adopted: strip trailing period for normalization (批一 尾句规范化)
spirit = open('data/storylines/codex/city-spirit.md', encoding='utf-8').read()
rows = re.findall(r'^\|\s*(\d+)\s*\|\s*(.+?)\s*\|', spirit, re.M)
adopted_norm = set()
for n, t in rows:
    t = re.sub(r'\*\*', '', t).strip()
    adopted_norm.add(t.rstrip('。'))
A('adopted_norm=%d' % len(adopted_norm))

tri = {}
for f in ('city-culture.md', 'city-humanities.md', 'city-residents.md'):
    tri[f] = open('data/storylines/codex/' + f, encoding='utf-8').read()

def in_tri(ln):
    return any((ln in c) or (ln + '。' in c) for c in tri.values())

net = [(ln, ax, sc) for ln, (ax, sc) in uniq.items() if ln not in adopted_norm and not in_tri(ln)]
A('net_after_norm=%d' % len(net))
tri_hits = sum(1 for ln, _, _ in net if False)
A('tri_excluded=%d' % (len(uniq) - len(net) - len([1 for ln in uniq if ln in adopted_norm])))

# mechanical aphorism-shape band: length 8-24, drop marketing/chat openers
STOP = re.compile(r'^(欢迎|大家|快来|尝尝|支起来|赶紧|哟|喽|哈哈|嘿|哎呀|来一|来来|走过路过|瞧一|看一看|上新|开张|客官|小二|老字号.{0,2}店|今日特|新鲜)')
band = []
for ln, ax, sc in net:
    L = len(ln)
    if 8 <= L <= 24 and not STOP.search(ln):
        band.append((ax, sc, ln))
A('band_8_24=%d' % len(band))

by_axis = {}
for ax, sc, ln in band:
    by_axis.setdefault(ax, []).append((sc, ln))
A('')
for ax in by_axis:
    A('===== %s (%d) =====' % (ax, len(by_axis[ax])))
    for sc, ln in by_axis[ax]:
        A('%s|%s' % (sc, ln))

open('.c3-tmp/r1848_batch5_band.txt', 'w', encoding='utf-8').write('\n'.join(OUT))
print('BAND_OK net=%d band=%d' % (len(net), len(band)))
