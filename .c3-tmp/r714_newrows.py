# -*- coding: utf-8 -*-
# R714 new rows: renders README (lc-012 in-chain row) + station-reviews (R714 row)
#                + queue E12 note + lc012 README render-leg record
import io

RENDERS_ROW = (
u"| lc-012-v1-shipinhao-60s.mp4 | **在链·渲染腿毕（queue §E 批活池 E12 件·冗余扩容位第九件·源卡=CENSUS-v14 F-033 潘志明"
u"·R713 起链→R714 渲染腿·收官腿 R715 随轮领·内容产线三工种图鉴拆条链闭环位）** | **R-E shipinhao 12 段 11 柔转场 0 硬切**"
u"·9:16 1080\u00d71920·**58.252s ffprobe 实测=音轨分毫一致·1.75s 余量**（plan 内部预估 59.033s=tail 余量项·实测为准）"
u"·hits=[0,11]·**S5.5 角标常驻位**=BigStream\\|拆条 012·源城市图鉴 014+§4.5 三开关[glow/scanlines/sys.beat=NN t=MM:SS]"
u"·plan.series+s45_dials 入 plan.json·**拆条形态对位=源卡即证据 12/12**（census-card-v14-vertical 源卡画面×12"
u"·visual-ratio 1.00·源件=F-033 PNG 派生 scale 660+pad y=160+zoompan \u22641.04·13.000s=LC-001~011 R511 法"
u"·ffprobe 与 v15 参照逐参数一致·素材探针先行=卡面九行全读+AIGC 标签位=卡面左上=同位族）——"
u"**S2 三门 R714 循环独立执法全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·pacing CV 0.304·prosody 9 档 12 拍"
u"·copy CV 0.354）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排"
u"+timeline 代数过）+spec 微信视频号双 PASS（9:16+58.25s \u220830-60s 窗 1.7s 余量）——**帧验三律全过**："
u"拍头 12/12 语义全中（H1 拍名 12/12 逐拍对位+sys.beat 01\u219212 连续无跳号 t 单调递增+角标 12 帧全在+AIGC 帧头标识全在）"
u"+段中尾 6/6 稳定零录穿（law2=动态三最长拍 b4/b5/b8〔7.77/6.82/5.86s〕·**tile 缩略误读三族定谳**"
u"=\u300c过于人情\u201d\u2192全分辨率正字\u300c迫于人情\u201d〔fs-pair-h04-h11 逐字核〕/b7 字幕\u300c值班\u201d\u2192SRT 正源机核"
u"\u300c每周去留言墙拆信\u201d〔12 cue 与 beats v5 逐字一致·gate1 0F0W 机核〕/b9 卡锚\u300c她那期\u201d\u00d7口播\u300c他抄了\u201d=叙述位设计非错位"
u"〔溯源对表在案〕·段尾帧 sys.beat 行+字幕缺席=淡出窗采样·**LC-011 F-065 已登记件同位对照实证同行为**"
u"=R697 逐 cue 显隐律族+R684 段起始戳设计口径·非缺陷）+回环 crossings={}（max 拍 7.77s<源 13s·诚实计算）"
u"+AIGC 双标识分层可读（帧头标识+卡面左上标签垂直错开零叠压·fs-pair 全分辨率实证·R511 避让法前置执行零修红）"
u" | plan.json 入 git·**收官腿 R715 随轮领**（E8 七席+ASR 终轨 R169 QC recipe+E4 同轮回填\u2192M4\u2192F-066 登记"
u"\u2192冗余池第九件落位\u2192release-schedule v2.4\u2192queue §E E12 出池+补池义务=候选苏梓涵 C-00020/老晶振 C-00019 随选优轮评估） |"
)

STATION_ROW = (
u"| 2026-09-30 | **S2 三门循环独立执法+帧验三律（lc-012-v1-shipinhao=queue §E 批活池 E12 件·冗余扩容位第九件"
u"·源卡 CENSUS-v14 F-033 潘志明·R714 渲染腿）** | lc-012-v1-shipinhao-60s.mp4（R-E shipinhao 12 段·11 柔转场 0 硬切"
u"·58.252s） | 循环独立执法（ai_feel+层 1.8+spec 微信视频号·纯脚本机检零 LLM）+帧验三律（会话内建多模态） "
u"| —（机检档·E8 终审待收官腿） | 对位表=cards-v1-matched（**拆条形态源卡即证据 12/12**·visual-ratio 1.00"
u"·b9 何雨欣互证拍=C-00022 跨卡互指=**拆条系列第五对人物链+内容产线三工种图鉴拆条链闭环**〔主播 LC-003\u2192字幕君 LC-011"
u"\u2192选题官 LC-012·MEDIA 城同城三工种同构 R303/R305 在册〕）+S2 三门全绿（ai_feel 0F0W gaps 11 处 0.220-0.558s"
u"·pacing CV 0.304·prosody 9 档 12 拍·copy CV 0.354+层 1.8 六面 PASS〔beat-align 11/11+camera 12 段全动"
u"+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过〕+spec 双 PASS 1.7s 余量）+帧验三律全过"
u"（拍头 12/12 语义全中〔H1 拍名 12/12 逐拍对位+sys.beat 01\u219212 连续 t 单调+角标 12 帧全在〕+段中尾 6/6 零录穿"
u"〔law2=b4/b5/b8 动态三最长 7.77/6.82/5.86s·**tile 缩略误读三族定谳**=过于\u2192迫于〔fs-pair 全分辨率逐字核〕"
u"/值班\u2192拆信〔SRT 正源 12 cue 机核=beats v5 逐字一致〕/b9 她那期×他抄了=叙述位设计非错位〔溯源对表在案〕"
u"·段尾帧 sys.beat 行+字幕缺席=淡出窗采样**LC-011 F-065 已登记件同位对照实证同行为**=R697 逐 cue 显隐律族"
u"+R684 段起始戳设计口径·非缺陷〕+回环 crossings={}〔max 7.77s<源 13s〕+AIGC 双标识分层可读"
u"〔帧头标识+卡面左上标签垂直错开零叠压·fs-pair-h04-h11 全分辨率实证·R511 避让法前置执行零修红〕）"
u"+台账=renders 在链行+lc012 README 生产记录+queue E12 注 |"
)

QUEUE_NOTE = (
u"  **[R714 渲染腿毕 2026-09-30（R710 同型五步）：素材探针=F-033 卡九行全读（AIGC 标签位=卡面左上=同位族·R511 避让法直接适用）"
u"\u2192census-card-v14-vertical 源件派生 13.000s（R511 法·ffprobe 与 v15 参照逐参数一致）\u2192对位表 cards-v1-matched 12/12"
u"（源卡即证据·visual-ratio 1.00·b9 何雨欣互证=第五对人物链+三工种闭环拍）\u2192R-E shipinhao 渲染 lc-012-v1-shipinhao-60s.mp4"
u"（58.252s 音轨分毫一致 1.75s 余量·hits=[0,11]·角标=拆条 012·源城市图鉴 014+§4.5 三开关）\u2192S2 三门全绿"
u"（ai_feel 0F0W CV 0.304/0.354+层 1.8 六面 PASS+spec 微信视频号双 PASS）+帧验三律全过（拍头 12/12+段中尾 6/6 零录穿"
u"〔段尾 sys.beat+字幕缺席=淡出窗采样·LC-011 F-065 已登记件同位对照定谳非缺陷〕+回环 crossings={}·tile 误读三族定谳"
u"=过于\u2192迫于〔fs-pair 全分辨率〕/值班\u2192拆信〔SRT 正源机核〕/她他=叙述位设计）——收官腿（E8+ASR+E4+M4\u2192F-066 登记"
u"\u2192冗余池第九件落位\u2192release-schedule v2.4\u2192E12 出池+补池义务）R715 随轮领]**"
)

# 1) renders README append
p = 'output/renders/README.md'
t = io.open(p, encoding='utf-8').read()
assert t.endswith('\n')
t = t.rstrip('\n') + '\n' + RENDERS_ROW + '\n'
io.open(p, 'w', encoding='utf-8').write(t)
print('renders row appended')

# 2) station-reviews append
p = 'docs/reviews/station-reviews.md'
t = io.open(p, encoding='utf-8').read()
t = t.rstrip('\n') + '\n' + STATION_ROW + '\n'
io.open(p, 'w', encoding='utf-8').write(t)
print('station row appended')

# 3) queue E12 note (insert after the R712/R713 note line, before '## burn' section)
p = 'docs/self-improvement-queue.md'
t = io.open(p, encoding='utf-8').read()
anchor = u'\u6062\u590d \u22652 \u8fbe\u6807\uff08C-20260929-02 B \u6b3e\u53e3\u5f84\uff09]**'  # 恢复 ≥2 达标（C-20260929-02 B 款口径）]**
assert t.count(anchor) == 1, 'queue anchor count=%d' % t.count(anchor)
t = t.replace(anchor, anchor + '\n' + QUEUE_NOTE)
io.open(p, 'w', encoding='utf-8').write(t)
print('queue E12 note inserted')

# 4) lc012 README: production record + gate block update
p = 'data/sources/lc012/README.md'
t = io.open(p, encoding='utf-8').read()
rec_anchor = u'\u300a\u524d\u7f6e\u300b'  # end of TTS line uses ...BGM-A 纯净）。
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
print('ALL LEDGER ROWS DONE')
