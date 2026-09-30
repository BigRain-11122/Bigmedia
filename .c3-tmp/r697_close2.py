# -*- coding: utf-8 -*-
# R697 close (queue leg only): append E7 render-leg note
import io
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
p = "docs/self-improvement-queue.md"
with io.open(ROOT + "\\" + p, encoding="utf-8") as f:
    s = f.read()
old = u"lane=E3 REACT-v6\u301409-30 \u7a97\u4f4d\u3015+E7\u3014active\u3015\u6062\u590d \u22652 \u8fbe\u6807\uff08C-20260929-02 B \u6b3e\u53e3\u5f84\uff09]**"
assert old in s, "queue E7 anchor missing"
new = old + (u"\n  **[R697 \u7a7a\u6c14\u9884\u7b97+\u6e32\u67d3\u817f\u6bd5 2026-09-29\uff1a\u2460\u7a7a\u6c14\u9884\u7b97\u4e09\u9053 v1 69.44s \u8d85\u7a97\u2192v2 60.03s \u8584\u8d85\u5e3d\u2192**v3 58.66s \u5b9a\u7a3f 1.34s \u4f59\u91cf**\uff08"
             u"\u5361\u7247\u951a\u70b9\u5217\u96f6\u52a8+\u4fe1\u6761\u96f6\u52a8+\u951a\u8bed\u4fdd\u771f[\u6885\u82b1/\u70df\u55d3/\u8fc7\u4e91\u96e8\u4e00\u53f7/\u5168\u57ce\u706f\u5e26/\u5341\u56db\u53f7\u8def\u706f/\u4e09\u53e5\u8bdd/\u9493\u4e86\u4e00\u8f88\u5b50\u98ce=\u5361\u53e3\u5206\u5de5]\u00b7M1 \u590d\u68c0 0F0W\uff09"
             u"\u2461TTS light \u5b9a\u7a3f\u97f3\u8f68\uff08--order LC-007-v3\u00b7--template=.lc006-tmp/cards.json\uff09"
             u"\u2462census-card-v18-vertical \u6e90\u4ef6\u6d3e\u751f\uff08F-037 PNG\u00b7R511 \u6cd5 13s\uff09+\u5bf9\u4f4d\u8868 12/12 visual-ratio 1.00"
             u"\u2463R-E shipinhao \u6e32\u67d3 58.66s hits=[0,11]\uff08S5.5 \u89d2\u6807=\u62c6\u6761 007\u00b7\u6e90\u57ce\u5e02\u56fe\u9274 018\uff09"
             u"\u2464S2 \u4e09\u95e8\u5168\u7eff+\u5e27\u9a8c\u4e09\u5f8b\u5168\u8fc7\uff08station-reviews R697 \u884c\u00b7\u6bb5\u5c3e\u5b57\u5e55\u7f3a\u5e2d=SRT \u9010 cue \u663e\u9690\u5f8b\u673a\u6838\u5b9a\u8c2d\u975e\u7f3a\u9677\uff09"
             u"\u2014\u2014\u4f59\u817f=\u6536\u5b98\u817f\uff08E8+ASR+E4+M4\u2192F \u767b\u8bb0\u2192\u5197\u4f59\u6c60\u7b2c\u56db\u4ef6\u843d\u4f4d\uff09R698 \u968f\u8f6e\u9886]**")
s = s.replace(old, new, 1)
with io.open(ROOT + "\\" + p, "w", encoding="utf-8") as f:
    f.write(s)
print("queue updated")
