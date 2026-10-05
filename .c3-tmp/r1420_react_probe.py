# -*- coding: utf-8 -*-
"""R1420 REACT-v9 M0 hot-topic pool probe (10-06 daily brief, 20 items).

Law-level exclusions (recorded in verdict, not probed):
  bili#1/#3/#7 影视综艺面 (R909 precedent) / bili#4 脑洞面 (R455) / bili#5 健康面 (R1030 健康纹身)
  / bili#6 音乐面+具名IP (R1030) / bili#9 政治/军事敏感 / zhihu#1 具名企业商务面+华为族 (R909/R1299)
  / zhihu#2 政治敏感(外国选举) / zhihu#3 国家安全敏感面 / zhihu#5 具名企业+股价族 (R455 price 3-connect)
  / zhihu#6 影视面 / zhihu#7 历史战争科普面 / zhihu#8 健康辟谣面 (R1030) / zhihu#10 影视剧评价面(具名蜗居)

Borderline candidates for mechanical pool evidence:
  A zhihu#4 日本窄轨铁路(194wan) -> 交通制式/坚守旧制 face -> probe rail/boat/travel lines
  B zhihu#9 口渴喝水科普(105wan) -> 喝水/茶汤 face -> probe water/tea/soup lines
  C bili#8 Windows XP 开机音乐 -> 系统开机/数字怀旧 face (数字城市同源) -> probe boot/system lines
  D bili#2 大学生爆改宿舍 -> 校园生活/改造 face -> probe dorm/fix lines
  E bili#10 斥巨资买衣服 -> 消费面 -> price/衣服 family 3-connect check (v2/v7 consumed) + probe
"""
import io, json, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
BASE = os.path.join(ROOT, 'data', 'storylines', 'cards')

pool = json.load(io.open(os.path.join(ROOT, '..', '..', 'life', 'BigLife', 'cognition', 'pools.json'), encoding='utf-8'))
spirit = io.open(os.path.join(ROOT, 'data', 'storylines', 'codex', 'city-spirit.md'), encoding='utf-8').read()

faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, 'cards.json')
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding='utf-8'))
        face = u'\n'.join(u'\n'.join(c.get('lines', [])) for c in cfg.get('cards', []))
        sq = cfg.get('meta', {}).get('source_quote', u'')
        faces[d] = face + u'\n' + sq

def shingles(text, lo=2, hi=5):
    s = set()
    n = len(text)
    for L in range(lo, hi + 1):
        for i in range(0, n - L + 1):
            s.add(text[i:i + L])
    return s

def probe(text):
    hits = {}
    for sh in sorted(shingles(text), key=len, reverse=True):
        if len(sh) < 2:
            continue
        where = sorted(d for d, f in faces.items() if sh in f)
        spirit_hit = sh in spirit
        if not where and not spirit_hit:
            continue
        hits[sh] = (u','.join(where) if where else u'city-spirit')
    kept = []
    for sh in sorted(hits, key=len, reverse=True):
        if any(sh != k and sh in k for k in [x[0] for x in kept]):
            continue
        kept.append((sh, hits[sh]))
    return kept

KW_A = [u'轨', u'铁路', u'火车', u'列车', u'电车', u'地铁', u'渡轮', u'船', u'交通', u'出行', u'慢']
KW_B = [u'喝水', u'口渴', u'渴', u'茶', u'汤', u'水', u'杯', u'灌']
KW_C = [u'开机', u'关机', u'启动', u'电脑', u'系统', u'音乐', u'旋律', u'响']
KW_D = [u'宿舍', u'改造', u'爆改', u'翻新', u'收拾', u'打扫', u'房间', u'住']
KW_E = [u'衣服', u'衬衫', u'买', u'穿', u'价']
GROUPS = [(u'A_rail_gauge', KW_A), (u'B_drink_water', KW_B), (u'C_xp_boot', KW_C), (u'D_dorm_reno', KW_D), (u'E_clothes_price', KW_E)]

AXES = list(pool['axes'].keys())
out = io.StringIO()
def w(s):
    out.write(s)
    out.write(u'\n')

w(u'R1420 REACT-v9 M0 pool probe (10-06 brief; fleet = all card faces + city-spirit)')
w(u'=' * 70)
for gname, kws in GROUPS:
    w(u'== GROUP %s keywords=%s ==' % (gname, u'/'.join(kws)))
    for ax in AXES:
        for bk, rows in pool['axes'][ax].items():
            for i, line in enumerate(rows):
                if any(k in line for k in kws):
                    kept = probe(line)
                    status = u'CLEAN' if not kept else u'HIT: ' + u' ; '.join(u'[%s]->%s' % (sh, where) for sh, where in kept[:4])
                    w(u'%s/%s/%d %s -> %s' % (ax, bk, i, line, status))
    for bk, rows in pool.get('sprite', {}).items():
        for i, line in enumerate(rows):
            if any(k in line for k in kws):
                kept = probe(line)
                status = u'CLEAN' if not kept else u'HIT: ' + u' ; '.join(u'[%s]->%s' % (sh, where) for sh, where in kept[:4])
                w(u'sprite/%s/%d %s -> %s' % (bk, i, line, status))
    w(u'=' * 70)

io.open(os.path.join(ROOT, '.c3-tmp', 'r1420_react_probe.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('done, out=r1420_react_probe.txt')
