# -*- coding: utf-8 -*-
"""R2372 DIGEST-v26 remediation-round-1 M1 assertions.

Rebuilt after the red-team round-4 rejection (review-20261019-mcdigest-v26):
- P1 fix: mid-sentence excerpt quotes now carry ellipsis marks, sentence
  starts restored as leading ellipsis per the remediation spec.
- P2 fix: no sentence-final period added inside quote marks (original
  punctuation preserved verbatim).
- P2 fix: line-7 quote now carries an inline landing phrase.
- P2 fix: source line no longer contains the 'tai4zhang4' jargon token.
- A2 law: deck line == exact expected string; core substring == verbatim
  continuous substring of the orders source window.
- A6 extended: jargon gate covers deck body AND the burned source line.
"""
import io
import json
import re

rows_txt = io.open(r'.c3-tmp/orders-rows-545plus-r2372.txt',
                   encoding='utf-8').read()
card = json.load(io.open(
    r'data/storylines/cards/MC-20261019-DIGEST-v26/cards.json',
    encoding='utf-8'))
deck = '\n'.join(card['cards'][0]['lines'])
subs_txt = io.open(
    r'data/storylines/cards/MC-20261019-DIGEST-v26/subs.srt',
    encoding='utf-8').read()

# A1: rows file covers the claimed window tail (cluster closure row 583)
assert 'ROW 545:' in rows_txt and 'ROW 583:' in rows_txt, 'A1 FAIL: window'

# A2: deck quote lines are EXACT; cores are continuous verbatim substrings.
# (trunc, lead, tail): trunc=True -> mid-sentence excerpt, ellipsis mandatory.
deck_quotes = [
    ('「……不要再改这么多版本了」往后 ≤3 版',
     '不要再改这么多版本了', True),
    ('「给我引入监督和校对的机制……」新立监制',
     '给我引入监督和校对的机制', True),
    ('「……所有环节 都要有专家……」12 环节配齐',
     '所有环节 都要有专家', True),
    ('「要高效快速啊 5天搞不定一个」MV 出片提速',
     '要高效快速啊 5天搞不定一个', False),
    ('「全面开工」02:18 V5.9 双签出片',
     '全面开工', False),
]
for deck_line, core, trunc in deck_quotes:
    assert core in rows_txt, 'A2 FAIL: core not verbatim in source: %s' % core
    assert deck_line in deck, 'A2 FAIL: deck line mismatch: %s' % deck_line
    seg = deck_line.split('「', 1)[1].split('」', 1)[0]
    if trunc:
        assert '……' in seg, ('A2 FAIL: excerpt without ellipsis '
                             'mark (red-team P1 law): %s' % seg)
    assert '。' not in seg, ('A2 FAIL: added sentence-final period inside '
                             'quote (red-team P2 law): %s' % seg)

# A2b: full original sentences verbatim in source (what the excerpts cut)
for full in ['我希望后面的出品 不要再改这么多版本了',
             '而且我说过mv的所有环节 都要有专家']:
    assert full in rows_txt, 'A2b FAIL: full sentence not in source: %s' % full
assert ('我希望后面的出品 不要再改这么多版本了'
        in json.dumps(card['meta'], ensure_ascii=False)), (
    'A2b FAIL: meta full-sentence carry missing')

# A3: numbers traceable + 39-row window contiguous
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

# A5: title + triple-label carriers + tech#224 landing-phrase carriers
for needle in ['城市盘点 026', '一日打磨日', 'V5.4→V5.9', '14→6', '≤3',
               '12 环节', '02:18', '新立监制', '全面开工', '双签出片',
               'MV 出片提速']:
    assert needle in deck, 'A5 FAIL: %s missing from deck' % needle

# A6 (tech#224 audience gate): zero internal jargon on deck body AND
# the burned source line (red-team P2[3] fix: subs line carries the
# 'tai4zhang4' token -> fixed to 'ling2 pi1 dang4 an4').
face = deck + '\n' + subs_txt
for jargon in ['正典', '台账', '闸', '席', 'XFS', 'assert', 'bit-acc']:
    assert jargon not in face, (
        'A6 FAIL: internal jargon on card face (tech#224): %s' % jargon)
assert '一日打磨日令批档案' in subs_txt, (
    'A6 FAIL: source line missing fixed wording')
assert '令批台账档案' not in subs_txt, (
    'A6 FAIL: old jargon source line still burned')

print('M1 ASSERT ALL GREEN (remediation r1): deck_quotes=%d exact '
      'numbers=8 window_rows=39 rows_range=545-583 tech#224_face=clean '
      '(deck+subs)' % len(deck_quotes))
