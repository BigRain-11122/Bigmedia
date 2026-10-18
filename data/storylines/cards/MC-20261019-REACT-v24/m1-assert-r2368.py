# -*- coding: utf-8 -*-
"""R2368 REACT-v24 M1 assertions (hot wrap preservation + pool axes + anchor-excerpt closing + heat discipline)."""
import io
import json
import re

intel = io.open(r'data/intel/daily/2026-10-19.md', encoding='utf-8').read()
pools = json.load(io.open(
    r'C:/Users/sjs20/Desktop/FluxGroup/life/BigLife/cognition/pools.json',
    encoding='utf-8'))
anchor = io.open(
    r'C:/Users/sjs20/Desktop/FluxGroup/life/BigLife/census/anchors/C-00010.md',
    encoding='utf-8').read()
card = json.load(io.open(
    r'data/storylines/cards/MC-20261019-REACT-v24/cards.json',
    encoding='utf-8'))
deck = '\n'.join(card['cards'][0]['lines'])

# A1: hot title verbatim zhihu-hot #4 (ordinal stripped, zero edit) and the
# two-segment comma split preserves every character (HOT1+HOT2 == HOT_FULL)
i0 = intel.index('## zhihu-hot')
hot = re.search(r'^4\. (.+)$', intel[i0:], re.M).group(1)
hot1 = '杭州21岁大三女生摆摊卖柠檬奶，一年开出20家门店，'
hot2 = '月营业额超100万，她成功的因素有哪些？'
assert hot1 + hot2 == hot, ('A1 FAIL: split loses/edits chars: %r vs %r'
                            % (hot1 + hot2, hot))
assert hot1 in deck and hot2 in deck, 'A1 FAIL: hot segments missing on deck'

# A2: three axis lines verbatim in ceo_order buckets of the named axes + on deck
axes = {
    '求新': '啥新鲜玩意儿又上架了？',
    '烟火': '白茫茫的光，包子铺都得开张了',
    '侠气': '城主一声令，咱这买卖就能赚翻天',
}
for axis, q in axes.items():
    bucket = pools['axes'][axis]['ceo_order']
    assert q in bucket, ('A2 FAIL: axis line not verbatim in %s ceo_order: %s'
                         % (axis, q))
    assert ('「%s」' % q) in deck, 'A2 FAIL: axis line missing on deck: %s' % q
    assert ('%s轴' % axis) in deck, 'A2 FAIL: axis label missing: %s' % axis

# A3: closing excerpt verbatim in C-00010 anchor (nianlun daily-log family)
# + census-registered occupation + deck line present
assert '头几家客倌真灵额，一早就来捧场' in anchor, (
    'A3 FAIL: closing excerpt not in C-00010.md')
assert '数据粥铺摊主' in anchor, 'A3 FAIL: occupation not census-registered in C-00010.md'
assert '数据粥铺摊主开档语：「头几家客倌真灵额，一早就来捧场」' in deck, (
    'A3 FAIL: closing line missing on deck')
assert '开档' in anchor, 'A3 FAIL: kaidang trade jargon not in anchor'

# A4: heat metadata discipline (meta/README accounting only, never on card face)
assert '291' in intel, 'A4 FAIL: heat number not in intel source'
assert '291' not in deck, 'A4 FAIL: heat metadata leaked onto card face'
assert '291 万' in json.dumps(card['meta'], ensure_ascii=False), (
    'A4 FAIL: heat not carried in meta accounting')

# A5: title + source-date carrier lines
for needle in ['城市速报 024', '今日热点 · 知乎热榜 2026-10-19']:
    assert needle in deck, 'A5 FAIL: %s missing from deck' % needle

# A6: deck line count discipline (8 lines: title+date+2 hot+3 axes+1 closing)
assert len(card['cards'][0]['lines']) == 8, 'A6 FAIL: deck line count != 8'

print('M1 ASSERT ALL GREEN: hot=verbatim-wrap-preserved axes=3-bucketed '
      'closing=nianlun-excerpt heat=meta-only lines=8')
