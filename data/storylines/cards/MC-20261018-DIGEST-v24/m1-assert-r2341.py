# -*- coding: utf-8 -*-
"""R2341 DIGEST-v24 M1 assertions (verbatim + numbers + rows-range meta)."""
import io
import json
import re

rows_txt = io.open(r'.c3-tmp/orders-rows-514plus.txt', encoding='utf-8').read()
card = json.load(io.open(
    r'data/storylines/cards/MC-20261018-DIGEST-v24/cards.json',
    encoding='utf-8'))
deck = '\n'.join(card['cards'][0]['lines'])

# A1: rows file covers the claimed window tail
assert 'ROW 522:' in rows_txt and 'ROW 539:' in rows_txt, 'A1 FAIL: window tail'

# A2: CEO verbatim quotes are continuous substrings of the source rows
quotes = [
    ('现在是80分了 好好再打磨一下给成品', 'row 526 V5 精修令'),
    ('按水印的内容是 大喵没鱼吃', 'row 529 暗水印令'),
    ('严格审核后给我终片', 'row 535 终片冲刺令'),
    ('务必做到MV最顶级的', 'row 536 转场顶级令'),
    ('给我全部项目并行开工！', 'row 538 游戏并行开工令'),
    ('互相监督互相制约', 'row 539 对抗式审查令'),
]
for q, src in quotes:
    assert q in rows_txt, 'A2 FAIL: not verbatim in source (%s): %s' % (src, q)
    assert q in deck, 'A2 FAIL: quote missing from deck: %s' % q

# A3: numbers traceable + 18-row window is contiguous
for num in ['80', '256bit', '234.25s', '9 族', '32 款']:
    assert num in rows_txt, 'A3 FAIL: number not in source: %s' % num
ids = [int(x) for x in re.findall(r'^ROW (\d+):', rows_txt, re.M)]
seg = [i for i in ids if 522 <= i <= 539]
assert seg == list(range(522, 540)), (
    'A3 FAIL: rows 522-539 not contiguous 18 (got %d)' % len(seg))

# A4: meta rows-range declaration (tech#202 frontier convention)
m = re.search(r'rows?\s*(\d{1,4})\s*[-\u2013\u2014~]\s*(\d{1,4})',
              json.dumps(card['meta'], ensure_ascii=False))
assert m and int(m.group(1)) == 522 and int(m.group(2)) == 539, (
    'A4 FAIL: rows 522-539 declaration missing from meta')

# A5: title + triple-label carrier lines
for needle in ['城市盘点 024', '终片冲刺夜', '大喵没鱼吃', '234.25s',
               '9 族', '32 款', '互相监督互相制约']:
    assert needle in deck, 'A5 FAIL: %s missing from deck' % needle

print('M1 ASSERT ALL GREEN: quotes=%d numbers=5 window_rows=18 '
      'rows_range=522-539' % len(quotes))
