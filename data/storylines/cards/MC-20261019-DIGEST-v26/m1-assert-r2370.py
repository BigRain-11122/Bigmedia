# -*- coding: utf-8 -*-
"""R2370 DIGEST-v26 M1 assertions (verbatim + numbers + rows-range meta)."""
import io
import json
import re

rows_txt = io.open(r'.c3-tmp/orders-rows-545plus-r2370.txt', encoding='utf-8').read()
card = json.load(io.open(
    r'data/storylines/cards/MC-20261019-DIGEST-v26/cards.json',
    encoding='utf-8'))
deck = '\n'.join(card['cards'][0]['lines'])

# A1: rows file covers the claimed window tail (cluster closure = row 583 ship receipt)
assert 'ROW 545:' in rows_txt and 'ROW 583:' in rows_txt, 'A1 FAIL: window tail'

# A2: deck-carried quotes are continuous substrings of BOTH source and deck
deck_quotes = [
    ('不要再改这么多版本了', 'row 564 版本数收口令'),
    ('给我引入监督和校对的机制', 'row 561 制监席新立令'),
    ('所有环节 都要有专家', 'row 562 全环节专家覆盖律'),
    ('要高效快速啊 5天搞不定一个', 'row 563 效率令'),
    ('全面开工', 'row 582 全面开工令'),
]
for q, src in deck_quotes:
    assert q in rows_txt, 'A2 FAIL: not verbatim in source (%s): %s' % (src, q)
    assert q in deck, 'A2 FAIL: quote missing from deck: %s' % q

# A2b: meta-carried quotes are verbatim in source (card face not required)
meta_quotes = [
    ('我希望后面的出品 不要再改这么多版本了', 'row 564 版本数收口令'),
]
for q, src in meta_quotes:
    assert q in rows_txt, 'A2b FAIL: not verbatim in source (%s): %s' % (src, q)
    assert q in json.dumps(card['meta'], ensure_ascii=False), (
        'A2b FAIL: meta quote missing from meta: %s' % q)

# A3: numbers traceable + 39-row window is contiguous
for num in ['V5.4→V5.9', '一日六版', '14→6', '≤3', '12 环节',
            '5622 帧', '全片 bit-acc', '02:18']:
    assert num in rows_txt, 'A3 FAIL: number not in source: %s' % num
ids = [int(x) for x in re.findall(r'^ROW (\d+):', rows_txt, re.M)]
seg = [i for i in ids if 545 <= i <= 583]
assert seg == list(range(545, 584)), (
    'A3 FAIL: rows 545-583 not contiguous 39 (got %d)' % len(seg))

# A4: meta rows-range declaration (tech#202 frontier convention)
m = re.search(r'rows?\s*(\d{1,4})\s*[-\u2013\u2014~]\s*(\d{1,4})',
              json.dumps(card['meta'], ensure_ascii=False))
assert m and int(m.group(1)) == 545 and int(m.group(2)) == 583, (
    'A4 FAIL: rows 545-583 declaration missing from meta')

# A5: title + triple-label carrier lines + tech#224 audience-translation carriers
for needle in ['城市盘点 026', '一日打磨日', 'V5.4→V5.9', '14→6', '≤3',
               '12 环节', '02:18', '新立监制', '全面开工', '双签出片']:
    assert needle in deck, 'A5 FAIL: %s missing from deck' % needle

# A6 (tech#224 audience gate): no internal jargon tokens on the card face
for jargon in ['正典', '台账', '闸', '席', 'XFS', 'assert', 'bit-acc']:
    assert jargon not in deck, (
        'A6 FAIL: internal jargon on card face (tech#224): %s' % jargon)

print('M1 ASSERT ALL GREEN: deck_quotes=%d meta_quotes=%d numbers=8 '
      'window_rows=39 rows_range=545-583 tech#224_face=clean'
      % (len(deck_quotes), len(meta_quotes)))
