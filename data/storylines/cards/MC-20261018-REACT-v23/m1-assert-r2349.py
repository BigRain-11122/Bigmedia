# -*- coding: utf-8 -*-
"""R2349 REACT-v23 M1 assertions (hot verbatim + pool axes + anchor-excerpt closing + heat discipline)."""
import io
import json
import re

intel = io.open(r'data/intel/daily/2026-10-18.md', encoding='utf-8').read()
pools = io.open(
    r'C:/Users/sjs20/Desktop/FluxGroup/life/BigLife/cognition/pools.json',
    encoding='utf-8').read()
anchor = io.open(
    r'C:/Users/sjs20/Desktop/FluxGroup/life/BigLife/census/anchors/C-00021.md',
    encoding='utf-8').read()
card = json.load(io.open(
    r'data/storylines/cards/MC-20261018-REACT-v23/cards.json',
    encoding='utf-8'))
deck = '\n'.join(card['cards'][0]['lines'])

# A1: hot line is verbatim zhihu-hot #1 title (ordinal stripped, zero edit)
i0 = intel.index('## zhihu-hot')
hot = re.search(r'^1\. (.+)$', intel[i0:], re.M).group(1)
assert hot in deck, 'A1 FAIL: hot title not verbatim on deck: %r' % hot

# A2: three axis lines verbatim in ceo_order pool family + on deck (quoted form)
axes = ['新图纸一出，赶紧动手画！', '脑塔一亮，今儿可有新鲜事？', '白光一闪，心跳跟着快了几拍']
for q in axes:
    assert q in pools, 'A2 FAIL: axis line not verbatim in pools.json: %s' % q
    assert ('「%s」' % q) in deck, 'A2 FAIL: axis line missing on deck: %s' % q

# A3: closing excerpt verbatim in C-00021 anchor (jingli-domain family quote)
# + census-registered occupation + exhausted-creed discipline (rotation pool bottom)
assert '跟版本一起长的娃' in anchor, 'A3 FAIL: closing excerpt not in C-00021.md'
assert '信使小跟班' in anchor, 'A3 FAIL: occupation not census-registered in C-00021.md'
assert '信使小跟班家人语：「跟版本一起长的娃」' in deck, 'A3 FAIL: closing line missing on deck'
assert '放学别走' not in deck, 'A3 FAIL: exhausted creed leaked onto deck (rotation pool bottom)'

# A4: heat metadata discipline (meta/README accounting only, never on card face)
assert '3961' in intel, 'A4 FAIL: heat number not in intel source'
assert '3961' not in deck, 'A4 FAIL: heat metadata leaked onto card face'
assert '3961 万' in json.dumps(card['meta'], ensure_ascii=False), (
    'A4 FAIL: heat not carried in meta accounting')

# A5: title + source-date carrier lines
for needle in ['城市速报 023', '今日热点 · 知乎热榜 2026-10-18']:
    assert needle in deck, 'A5 FAIL: %s missing from deck' % needle

print('M1 ASSERT ALL GREEN: hot=verbatim axes=3 closing=anchor-excerpt '
      'creed=pool-bottom-respected heat=meta-only')
