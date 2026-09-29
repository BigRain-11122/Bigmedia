# -*- coding: utf-8 -*-
# R714 newrows fix: steps 3-4 only (renders/station already appended, do not repeat)
import io

QUEUE_NOTE = (
u"  **[R714 \u6e32\u67d3\u817f\u6bd5 2026-09-30\uff08R710 \u540c\u578b\u4e94\u6b65\uff09\uff1a\u7d20\u6750\u63a2\u9488=F-033 \u5361\u4e5d\u884c\u5168\u8bfb\uff08AIGC \u6807\u7b7e\u4f4d=\u5361\u9762\u5de6\u4e0a=\u540c\u4f4d\u65cf\u00b7R511 \u907f\u8ba9\u6cd5\u76f4\u63a5\u9002\u7528\uff09"
u"\u2192census-card-v14-vertical \u6e90\u4ef6\u6d3e\u751f 13.000s\uff08R511 \u6cd5\u00b7ffprobe \u4e0e v15 \u53c2\u7167\u9010\u53c2\u6570\u4e00\u81f4\uff09\u2192\u5bf9\u4f4d\u8868 cards-v1-matched 12/12"
u"\uff08\u6e90\u5361\u5373\u8bc1\u636e\u00b7visual-ratio 1.00\u00b7b9 \u4f55\u96e8\u6b23\u4e92\u8bc1=\u7b2c\u4e94\u5bf9\u4eba\u7269\u94fe+\u4e09\u5de5\u79cd\u95ed\u73af\u62cd\uff09\u2192R-E shipinhao \u6e32\u67d3 lc-012-v1-shipinhao-60s.mp4"
u"\uff0858.252s \u97f3\u8f68\u5206\u6beb\u4e00\u81f4 1.75s \u4f59\u91cf\u00b7hits=[0,11]\u00b7\u89d2\u6807=\u62c6\u6761 012\u00b7\u6e90\u57ce\u5e02\u56fe\u9274 014+§4.5 \u4e09\u5f00\u5173\uff09\u2192S2 \u4e09\u95e8\u5168\u7eff"
u"\uff08ai_feel 0F0W CV 0.304/0.354+\u5c42 1.8 \u516d\u9762 PASS+spec \u5fae\u4fe1\u89c6\u9891\u53f7\u53cc PASS\uff09+\u5e27\u9a8c\u4e09\u5f8b\u5168\u8fc7\uff08\u62cd\u5934 12/12+\u6bb5\u4e2d\u5c3e 6/6 \u96f6\u5f55\u7a7f"
u"\uff08\u6bb5\u5c3e sys.beat+\u5b57\u5e55\u7f3a\u5e2d=\u6de1\u51fa\u7a97\u91c7\u6837\u00b7LC-011 F-065 \u5df2\u767b\u8bb0\u4ef6\u540c\u4f4d\u5bf9\u7167\u5b9a\u8c23\u975e\u7f3a\u9677\uff09+\u56de\u73af crossings={}\u00b7tile \u8bef\u8bfb\u4e09\u65cf\u5b9a\u8c23"
u"=\u8fc7\u4e8e\u2192\u8feb\u4e8e\uff5bfs-pair \u5168\u5206\u8fa8\u7387\uff5d/\u503c\u73ed\u2192\u62c6\u4fe1\uff5bSRT \u6b63\u6e90\u673a\u6838\uff5d/\u5979\u4ed6=\u53d9\u8ff0\u4f4d\u8bbe\u8ba1\uff09\u2014\u2014\u6536\u5b98\u817f\uff08E8+ASR+E4+M4\u2192F-066 \u767b\u8bb0"
u"\u2192\u51a2\u4f59\u6c60\u7b2c\u4e5d\u4ef6\u843d\u4f4d\u2192release-schedule v2.4\u2192E12 \u51fa\u6c60+\u8865\u6c60\u4e49\u52a1\uff09R715 \u968f\u8f6e\u9886]**"
)

# 3) queue E12 note - unique anchor: +E12[active] ... ]**
p = 'docs/self-improvement-queue.md'
t = io.open(p, encoding='utf-8').read()
anchor = u"+E12\u3014active\u3015\u6062\u590d \u22652 \u8fbe\u6807\uff08C-20260929-02 B \u6b3e\u53e3\u5f84\uff09]**"
cnt = t.count(anchor)
assert cnt == 1, 'queue anchor count=%d' % cnt
t = t.replace(anchor, anchor + '\n' + QUEUE_NOTE)
io.open(p, 'w', encoding='utf-8').write(t)
print('queue E12 note inserted')

# 4) lc012 README: production record + gate block update
p = 'data/sources/lc012/README.md'
t = io.open(p, encoding='utf-8').read()
old_tail = u"cyber light+human 42 \u4ea7\u7ebf\u9ed8\u8ba4\u00b7BGM-A \u7eaf\u51c0\uff09\u3002"
assert t.count(old_tail) == 1, 'lc012 readme tail anchor count=%d' % t.count(old_tail)
new_tail = old_tail + u"""
- [2026-09-30 R714 \u6e32\u67d3\u817f] census-card-v14-vertical \u6d3e\u751f\uff08F-033 PNG\u00b7R511 \u6cd5\u00b713.000s ffprobe \u4e0e v15 \u53c2\u7167\u9010\u53c2\u6570\u4e00\u81f4\uff09\u2192\u5bf9\u4f4d\u8868 cards-v1-matched 12/12\uff08\u6e90\u5361\u5373\u8bc1\u636e visual-ratio 1.00\uff09\u2192R-E shipinhao \u6e32\u67d3 lc-012-v1-shipinhao-60s.mp4\uff0858.252s \u97f3\u8f68\u5206\u6beb\u4e00\u81f4\u00b71.75s \u4f59\u91cf\u00b7hits=[0,11]\u00b7\u89d2\u6807=\u62c6\u6761 012\u00b7\u6e90\u57ce\u5e02\u56fe\u9274 014+§4.5 \u4e09\u5f00\u5173\uff09\u2192S2 \u4e09\u95e8\u5168\u7eff\uff08ai_feel 0F0W CV 0.304/0.354+\u5c42 1.8 \u516d\u9762 PASS+spec \u5fae\u4fe1\u89c6\u9891\u53f7\u53cc PASS 1.7s \u4f59\u91cf\uff09+\u5e27\u9a8c\u4e09\u5f8b\u5168\u8fc7\uff08\u62cd\u5934 12/12+\u6bb5\u4e2d\u5c3e 6/6 \u96f6\u5f55\u7a7f+\u56de\u73af crossings={} \u00b7 tile \u8bef\u8bfb\u4e09\u65cf\u5b9a\u8c23\u3010\u8fc7\u4e8e\u2192\u8feb\u4e8e\u5168\u5206\u8fa8\u7387/\u503c\u73ed\u2192\u62c6\u4fe1 SRT \u6b63\u6e90/\u5979\u4ed6=\u53d9\u8ff0\u4f4d\u3011\u00b7\u6bb5\u5c3e sys.beat+\u5b57\u5e55\u7f3a\u5e2d=\u6de1\u51fa\u7a97\u91c7\u6837\u00b7LC-011 F-065 \u540c\u4f4d\u5bf9\u7167\u975e\u7f3a\u9677\uff09\u3002"""
t = t.replace(old_tail, new_tail)

old_gate = u"- S1=9/10 PASS\uff082026-09-29 23:52:42\uff09\u00b7M1=0F0W\uff08v5 \u7ec8\u7a3f\uff09\u00b7\u7a7a\u6c14\u9884\u7b97=58.252s\u220830-60s \u7a97 1.75s \u4f59\u91cf\u3002\n- \u4f59\u817f=\u6e32\u67d3\u817f\uff08F-033 PNG \u6d3e\u751f census-card-v14-vertical\u00b7R511 \u6cd5\u2192\u5bf9\u4f4d\u8868 12/12\u2192R-E shipinhao\uff3b--series-id=\u62c6\u6761 012\u00b7\u6e90\u57ce\u5e02\u56fe\u9274 014\uff3d\u2192S2 \u4e09\u95e8\u2192\u5e27\u9a8c\u4e09\u5f8b=R710 \u540c\u578b\uff09\u2192\u6536\u5b98\u817f\uff08E8+ASR+E4+M4\u2192F \u767b\u8bb0\u2192\u51a2\u4f59\u6c60\u7b2c\u4e5d\u4ef6\u843d\u4f4d\uff09\u968f\u8f6e\u9886\u3002"
assert t.count(old_gate) == 1, 'lc012 gate anchor count=%d' % t.count(old_gate)
new_gate = (u"- S1=9/10 PASS\uff082026-09-29 23:52:42\uff09\u00b7M1=0F0W\uff08v5 \u7ec8\u7a3f\uff09\u00b7\u7a7a\u6c14\u9884\u7b97=58.252s\u220830-60s \u7a97 1.75s \u4f59\u91cf\u3002\n"
            u"- S2=\u4e09\u95e8\u5168\u7eff\uff08R714\uff1aai_feel 0F0W+\u5c42 1.8 \u516d\u9762+spec \u53cc PASS\uff09\u00b7\u5e27\u9a8c\u4e09\u5f8b\u5168\u8fc7\uff08R714\uff09\u3002\n"
            u"- \u4f59\u817f=\u6536\u5b98\u817f\uff08E8+ASR+E4+M4\u2192F-066 \u767b\u8bb0\u2192\u51a2\u4f59\u6c60\u7b2c\u4e5d\u4ef6\u843d\u4f4d\u2192release-schedule v2.4\u2192E12 \u51fa\u6c60\uff09R715 \u968f\u8f6e\u9886\u3002")
t = t.replace(old_gate, new_gate)
io.open(p, 'w', encoding='utf-8').write(t)
print('lc012 readme updated')
print('FIX STEPS 3-4 DONE')
