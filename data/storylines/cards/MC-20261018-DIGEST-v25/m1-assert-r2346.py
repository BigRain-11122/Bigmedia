# -*- coding: utf-8 -*-
"""R2346 DIGEST-v25 M1 assertions (verbatim + numbers + rows-range meta)."""
import io
import json
import re

rows_txt = io.open(r'.c3-tmp/orders-rows-536plus-r2346.txt', encoding='utf-8').read()
card = json.load(io.open(
    r'data/storylines/cards/MC-20261018-DIGEST-v25/cards.json',
    encoding='utf-8'))
deck = '\n'.join(card['cards'][0]['lines'])

# A1: rows file covers the claimed window tail
assert 'ROW 540:' in rows_txt and 'ROW 544:' in rows_txt, 'A1 FAIL: window tail'

# A2: deck-carried quotes are continuous substrings of BOTH source and deck
deck_quotes = [
    ('清理本机所有的自动化任务', 'row 541 bm-c 全清令'),
    ('需要的自动化恢复', 'row 542 复工对齐令'),
    ('你负责分配好，让他们都各自满负荷运转', 'row 543 BM 仓解锁令'),
    ('膨胀的太厉害太快了', 'row 544 记忆治理席直令'),
]
for q, src in deck_quotes:
    assert q in rows_txt, 'A2 FAIL: not verbatim in source (%s): %s' % (src, q)
    assert q in deck, 'A2 FAIL: quote missing from deck: %s' % q

# A2b: meta-carried quotes are verbatim in source (card face not required)
meta_quotes = [
    ('创立一个专门的agent', 'row 544 记忆治理席直令'),
]
for q, src in meta_quotes:
    assert q in rows_txt, 'A2b FAIL: not verbatim in source (%s): %s' % (src, q)
    assert q in json.dumps(card['meta'], ensure_ascii=False), (
        'A2b FAIL: meta quote missing from meta: %s' % q)

# A3: numbers traceable + 5-row window is contiguous
for num in ['41 个全删', '36/36', '8 仓对齐', '三镜重烧 3/3',
            '93,662→71,850B/112→75 条', '375,794B/322 条']:
    assert num in rows_txt, 'A3 FAIL: number not in source: %s' % num
ids = [int(x) for x in re.findall(r'^ROW (\d+):', rows_txt, re.M)]
seg = [i for i in ids if 540 <= i <= 544]
assert seg == list(range(540, 545)), (
    'A3 FAIL: rows 540-544 not contiguous 5 (got %d)' % len(seg))

# A4: meta rows-range declaration (tech#202 frontier convention)
m = re.search(r'rows?\s*(\d{1,4})\s*[-\u2013\u2014~]\s*(\d{1,4})',
              json.dumps(card['meta'], ensure_ascii=False))
assert m and int(m.group(1)) == 540 and int(m.group(2)) == 544, (
    'A4 FAIL: rows 540-544 declaration missing from meta')

# A5: title + triple-label carrier lines
for needle in ['城市盘点 025', '深夜治理夜', '41 个全删', '36/36',
               '93,662→71,850B', '112→75 条', 'V5.3 重建']:
    assert needle in deck, 'A5 FAIL: %s missing from deck' % needle

print('M1 ASSERT ALL GREEN: deck_quotes=%d meta_quotes=%d numbers=6 '
      'window_rows=5 rows_range=540-544' % (len(deck_quotes), len(meta_quotes)))
