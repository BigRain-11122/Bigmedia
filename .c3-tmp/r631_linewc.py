# -*- coding: utf-8 -*-
# r631_linewc.py -- machine cost check for DIGEST-v9 candidate card lines (ASCII source)
import io, sys
sys.path.insert(0, 'src/render')
from render_card_video import _line_cost

LINES = [
    u"城市盘点 009",
    u"自驱力生态令 2026-09-28 落账 09:20:25",
    u"「不能有任何闲置资源，还有空转浪费现象」",
    u"3 缺口：创新无定轨 · 空转无定义 · 拉满张力",
    u"3 缺口：创新无定轨 · 空转无统一定义 · 拉满张力",
    u"闭环 4 件：提案轨·空转禁令·诚实边界·计量回访",
    u"闭环 4 件：提案轨、空转禁令、诚实边界、计量回访",
    u"提案轨 · 空转禁令 · 诚实边界 · 计量回访",
    u"3 缺口定谳 → 生态闭环 4 件立法",
    u"提案轨：三句式 · 无需 CEO 令 · 判据 ≤3 问",
    u"提案轨：三句式 · 无需 CEO 令 · 试点 ≤2 周",
    u"空转 4 形态定规 · idle-fast 跳轮路径全司废止",
    u"空转 4 形态定规 · idle-fast 全司废止",
    u"8 线点名 · 本司 ack ≤10 分钟 · 回访 10-05",
    u"8 线点名 · 集团 ack ≤15 分钟 · 本司 ≤10 分钟",
    u"每窗提案 ≥1 · 判负留痕合法 · 回访 10-05",
    u"拉满指标：GPU >70% · 队列常备 25 条",
]
BUDGET = 23.0
res = []
for ln in LINES:
    c = _line_cost(ln)
    res.append(u"%-6.2fem  margin %+-5.2fem  %s" % (c, BUDGET - c, ln))
io.open('.c3-tmp/r631_linewc.txt', 'w', encoding='utf-8').write('\n'.join(res))
print('written %d lines' % len(LINES))
