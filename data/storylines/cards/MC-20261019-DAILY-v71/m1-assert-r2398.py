# -*- coding: utf-8 -*-
"""R2398 DAILY-v71 M1 assertions (pool structure + verbatim row + 11 used-row
anchors + CEO order-day unlock anchors + fleet dedup + face discipline +
desensitization).  Cross-repo reads are read-only (pool json + group orders)."""
import datetime
import glob
import io
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
POOLS = r'C:/Users/sjs20/Desktop/FluxGroup/life/BigLife/cognition/pools.json'
HQ_ORDERS = r'C:/Users/sjs20/Desktop/FluxGroup/docs/ordersorders.md'
HQ_ORDERS = r'C:/Users/sjs20/Desktop/FluxGroup/docs/orders.md'

pools = json.load(io.open(POOLS, encoding='utf-8'))
card = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      'cards.json'), encoding='utf-8'))
deck = '\n'.join(card['cards'][0]['lines'])
face_lines = card['cards'][0]['lines']

# A1: pool window structure (axes 6 x 12 buckets x 18 rows + sprite 12 x 12)
AXES = ['烟火', '秩序', '求新', '怀旧', '侠气', '逍遥']
assert sorted(pools['axes'].keys()) == sorted(AXES), (
    'A1 FAIL: axes keys drift: %r' % (sorted(pools['axes'].keys()),))
for ax in AXES:
    b = pools['axes'][ax]['ceo_order']
    assert isinstance(b, list) and len(b) == 18, (
        'A1 FAIL: %s ceo_order bucket rows != 18: %d' % (ax, len(b)))
spr = pools['sprite']['ceo_order']
assert len(spr) == 12, 'A1 FAIL: sprite ceo_order rows != 12: %d' % len(spr)

# A2: candidate row verbatim at axes[怀旧][ceo_order][7]
ROW = '听说城主有令，咱先别急着打听'
b = pools['axes']['怀旧']['ceo_order']
assert ROW in b, 'A2 FAIL: row not verbatim in 怀旧 ceo_order bucket'
assert b.index(ROW) == 7, 'A2 FAIL: row index drift: %d' % b.index(ROW)
assert ('「%s」' % ROW) in deck, 'A2 FAIL: row missing on deck'

# A3: 11 consumed-position structure anchors (v70 + REACT-v12/23/24 + city-spirit#46)
USED = {
    ('烟火', 17): '城主发话了，早点铺子快忙活起来',          # DAILY-v70 F-166
    ('秩序', 4): '守门人说，规矩不能松',                     # REACT-v12 F-158
    ('侠气', 2): '有难处，找我准没错',                       # REACT-v12 F-158
    ('逍遥', 1): '城主发令，咱悠着点',                       # REACT-v12 F-158
    ('求新', 1): '新图纸一出，赶紧动手画！',                 # REACT-v23 F-196
    ('怀旧', 6): '脑塔一亮，今儿可有新鲜事？',               # REACT-v23 F-196
    ('侠气', 0): '白光一闪，心跳跟着快了几拍',               # REACT-v23 F-196
    ('求新', 12): '啥新鲜玩意儿又上架了？',                  # REACT-v24 F-197
    ('烟火', 15): '白茫茫的光，包子铺都得开张了',            # REACT-v24 F-197
    ('侠气', 13): '城主一声令，咱这买卖就能赚翻天',          # REACT-v24 F-197
    ('秩序', 9): '校准了时间，日子才踏实',                   # city-spirit #46
}
for (ax, idx), row in USED.items():
    got = pools['axes'][ax]['ceo_order'][idx]
    assert got == row, ('A3 FAIL: used-row anchor drift at %s/%d: %r'
                        % (ax, idx, got))

# A4: CEO order-day unlock anchors in group orders (host read-only direct read)
hq = io.open(HQ_ORDERS, encoding='utf-8').read()
assert '| 2026-10-19 15:43（校时 15:43·模拟态全司推广令） |' in hq, (
    'A4 FAIL: 15:43 order-day anchor row missing in HQ orders')
assert '| 2026-10-19 15:45（校时 15:45·BigLife census 解禁令） |' in hq, (
    'A4 FAIL: 15:45 anchor row missing in HQ orders')
assert '| 2026-10-19 19:35（校时 19:35） |' in hq, (
    'A4 FAIL: 19:35 anchor row missing in HQ orders')

# A5: fleet dedup (city-spirit + every card face/source_quote + fragment probes)
spirit = io.open(os.path.join(REPO, 'data/storylines/codex/city-spirit.md'),
                 encoding='utf-8').read()
assert ROW not in spirit, 'A5 FAIL: row already in city-spirit.md'
hits = []
self_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
for p in glob.glob(os.path.join(REPO, 'data/storylines/cards/*/cards.json')):
    if self_dir in p:
        continue
    try:
        c = json.load(io.open(p, encoding='utf-8'))
    except Exception:
        continue
    blob = '\n'.join(l for cd in c.get('cards', []) for l in cd.get('lines', []))
    blob += '\n' + c.get('meta', {}).get('source_quote', '')
    for frag in [ROW, '听说城主有令', '先别急着打听']:
        if frag in blob:
            hits.append((os.path.basename(os.path.dirname(p)), frag))
assert not hits, 'A5 FAIL: fleet dedup hits: %r' % (hits,)

# A6: face discipline (4 lines / numbering / date line / attribution)
assert len(face_lines) == 4, 'A6 FAIL: deck line count != 4'
assert face_lines[0] == '城市日签 071', 'A6 FAIL: title line drift'
assert face_lines[1] == '2026-10-19 · 城主连令日 · 晚', (
    'A6 FAIL: date line drift: %r' % face_lines[1])
assert face_lines[2] == '「%s」' % ROW, 'A6 FAIL: quote line drift'
assert face_lines[3] == '——硅基城市台词池 · 怀旧轴', 'A6 FAIL: attribution drift'
assert datetime.date(2026, 10, 19).weekday() == 0, (
    'A6 FAIL: calendar fact drift (2026-10-19 != Monday)')

# A7: desensitization (real CEO facts never on the card face)
for bad in ['CEO', 'Jason', 'O-2026', 'bm-a', 'bm-b', 'bm-c', 'BigLife',
            'BigStream', '机队', '模拟态', '解禁', '满负荷']:
    assert bad not in deck, 'A7 FAIL: real-world token on face: %s' % bad

print('M1 ASSERT ALL GREEN: pool=6x18+12 row=verbatim@怀旧/7 used=11-anchored '
      'orderday=15:43+19:35-anchored dedup=city-spirit+fleet-CLEAN '
      'face=4-line-discipline desens=zero-leak')
