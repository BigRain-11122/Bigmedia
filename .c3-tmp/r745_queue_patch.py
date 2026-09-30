# -*- coding: utf-8 -*-
# R745 queue patch (search-string fix: 'E16 LC-019 空气预算裁链定稿+TTS 定稿音轨毕（R744')
import io, os
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
p = os.path.join(ROOT, 'docs', 'self-improvement-queue.md')
t = io.open(p, encoding='utf-8').read()
assert u'E16 LC-019 渲染腿毕（R745' not in t, 'queue row already present'
QROW = (u"2026-09-30: **E16 LC-019 渲染腿毕（R745·R744 claim 兑现·R741/R737 同型五步·实活轮·产品优先律对位=本轮新实物=lc-019 成片在链）**："
        u"F-024 卡多模态读（AIGC 标签位=卡面左上·R511 零修红）→census-card-v5-vertical.mp4 派生（13.000s·ffprobe 与 v15 逐参数一致）"
        u"→对位表 12/12（visual-ratio 1.00·b9=第十对人物链闭环后半件+第十一对徐根福埋点）→R720 律前置修（b4/b5/b6/b7 per-card 56/54/50/46+"
        u"**b8=78 字 fleet 最长 col2 语义预拆 5 段+size 36 专项修**〔newline-only 零字符·块 6 行顶 788 净 21px≥787 地板·r745_wrap_probe.txt em 实证〕"
        u"·FINAL problems=NONE）→渲染 57.235s=音轨分毫一致 2.765s 余量·hits=[0,11]→S2 三门全绿（ai_feel 0F0W CV 0.282/0.291+层 1.8 六面"
        u"+spec 微信视频号双 PASS 2.8s 余量）→帧验三律全过（拍头 12/12+段中尾 6/6〔law2=b5/b8/b9〕+回环 crossings={}+AIGC 双标识 fs-pair 全分辨率"
        u"+b8 专项帧 fs-h08 实证+tile 误读四点全分辨率定谳 R189 律）→收官腿（E8+ASR+E4+M4→F-074→冗余池第十六件→E16 出池+补池）=R746 随轮领\n")
lines = t.splitlines(True)
idx = None
for i, l in enumerate(lines):
    if u'LC-019 空气预算裁链定稿+TTS 定稿音轨毕（R744' in l:
        idx = i
        break
assert idx is not None, 'queue E16 R744 line still not found'
lines.insert(idx + 1, QROW)
io.open(p, 'w', encoding='utf-8').write(u''.join(lines))
print('queue: E16 R745 row inserted after line idx %d' % idx)
print('QUEUE_DONE')
