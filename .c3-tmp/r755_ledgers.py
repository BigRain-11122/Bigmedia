# -*- coding: utf-8 -*-
# R755: ledger updates (renders README decl + in-chain row, station-reviews, lc021 README, queue burn)
#        + status-export refresh + state.json close-out (tick 755, log, focus, watermark +D-20260930-35)
import json, io, os, datetime

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'

def rd(p):
    with io.open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()

def wr(p, t):
    with io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
nowshort = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

# ---------- 1. renders README ----------
p = 'output/renders/README.md'
t = rd(p)
old_tail = (u"·渲染腿=F-022 PNG 派生 census-card-v3-vertical·R511 法→对位表 12/12→R-E shipinhao"
            u"〔拆条 021·源城市图鉴 003〕→S2 三门+帧验三律+全卡几何审计 R720 律前置→收官腿"
            u"〔E8+ASR+E4+M4→F-075→冗余池第十七件→E21 出池=20 卡全覆盖收官〕随轮领）")
new_tail = (u"·渲染腿**毕〔R755：六卡前置修=b3/b5 size 46+b7 size 38+b4/b8/b9 语义断点预拆+size 36/38 下探"
            u"（R745 b8 78 字修法族第二案·verbatim join 断言全过零字符）+全卡几何审计 FINAL problems=NONE"
            u"+S2 三门全绿（ai_feel 0F0W+层 1.8 六面 PASS+spec 双 PASS 58.079s 1.921s 余量）+帧验三律全过**"
            u"→收官腿〔E8+ASR+E4+M4→F-075→冗余池第十七件→E21 出池=20 卡全覆盖收官〕=R756 首位）")
assert old_tail in t, 'renders decl tail not found'
t = t.replace(old_tail, new_tail)

anchor = u"| lc-019-v1-shipinhao-60s.mp4 |"
idx = t.find(anchor)
assert idx > 0, 'lc-019 row not found'
line_end = t.find('\n', idx)
row = (u"\n| lc-021-v1-shipinhao-60s.mp4 | **在链件（queue §E 批活池 E21 件渲染腿毕 R755·CENSUS 锚池 20 卡全覆盖收官件·冗余扩容位第十七件·源卡=CENSUS-v3 F-022 沈佩兰·R753 起链→R754 定稿音轨→R755 渲染腿毕：收官腿待 R756〔E8+ASR+E4+M4→F-075 登记→冗余池第十七件→E21 出池=20 卡全覆盖收官+补池义务随轮领〕）** | "
       u"**R-E shipinhao 12 段 11 柔转场 0 硬切**·9:16 1080×1920·**58.079s ffprobe 实测=音轨分毫一致·1.921s 余量**·hits=[0,11]·S5.5 角标常驻位=BigStream\\|拆条 021·源城市图鉴 003+§4.5 三开关[glow/scanlines/sys.beat=NN t=MM:SS]·plan.series+s45_dials 入 plan.json·"
       u"**拆条形态对位=源卡即证据 12/12**（census-card-v3-vertical 源卡画面×12·visual-ratio 1.00·源件=F-022 PNG〔225,299B 核〕派生 scale 660+pad y=160+zoompan ≤1.04·13.000s=LC-001~019 R511 法〔ffprobe 与 v15 参照逐参数一致〕·素材探针先行=F-022 卡多模态九行全读+AIGC 标签位=卡面左上=同位族·R511 避让法前置执行零修红·来源行〔展示锚 C-00012〕在位核·卡面零〔〕注记核）——"
       u"**R720 律前置几何修（build 级审计驱动·六卡）**：b3/b4/b5/b7/b8/b9 @60px 5-8 行块顶 616-702 叠压（R711 五行块同型）→b3/b5 per-card size 46（5 行顶 787 净 20=修法地板）+b7 size 38（5 行顶 811 净 44）+**b4/b8/b9=语义断点预拆+阶梯下探 36/38（R745 b8 78 字修法族第二案）**（b4 76 字句子级断点 2 段+size 36=6 行顶 788 净 21/b8 69 字断点 2 段+size 38=5 行顶 811 净 44/b9 55 字断点 3 段+size 36=6 行顶 788 净 21·verbatim join 断言全过零字符）→**全卡几何审计 FINAL problems=NONE**——"
       u"**S2 三门 R755 循环独立执法全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·pacing CV 0.272·prosody 9 档 12 拍·copy CV 0.285）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过）+spec 微信视频号双 PASS（9:16+58.08s ∈30-60s 窗 1.9s 余量）——"
       u"**帧验三律全过**：拍头 12/12 语义全中（H1 拍名 12/12 逐拍对位+sys.beat 01→12 连续 t 单调递增+角标 12 帧全在+AIGC 帧头标识全在）+段中尾 6/6 稳定零录穿（law2=动态三最长拍 b0/b4/b5〔6.53/5.74/7.34s〕·段中静态戳 sys.beat=06 t=00:24=段起始 §4.5 设计口径 R684 同判·段尾帧状态行+字幕缺席=出段淡出带+SRT 逐 cue 显隐律 R697 判例·段尾重影=crossfade 窗正常合成像〔同版式双像=12 拍共用同源卡固有形态〕R684/R745 同判）+回环 crossings={}（max 拍 7.34s<源 13s·诚实计算）+AIGC 双标识分层可读（帧头 y≈55-80+卡面左上标签 y≈100-163 垂直错开零叠压·fs-pair-h00-h09-h11 全分辨率实证）+tile 缩略误读族全分辨率定谳（互证拍净读〔tile「夫妻档档/户名字/偶人」伪读族〕+物种行净读 碳基市民·弄堂派·女·58 岁〔tile「青鸾源」伪读〕=R189 手段问题律） | "
       u"plan.json 入 git·mp4 gitignored·**收官腿待 R756**（E8 终审+ASR 终轨 R169 QC recipe+E4 参考仪+M4→F-075 登记→冗余池第十七件落位→E21 出池=20 卡全覆盖收官+补池义务随轮领·发布锁=M5 账号物理件·未上线=未测量） |")
t = t[:line_end] + row + t[line_end:]
wr(p, t)
print('renders README updated')

# ---------- 2. station-reviews ----------
p = 'docs/reviews/station-reviews.md'
t = rd(p).rstrip('\n')
sr = (u"\n| 2026-09-30 | **S2 三门循环独立执法+帧验三律+全卡几何审计前置修六卡（lc-021-v1-shipinhao=queue §E 批活池 E21 件渲染腿·CENSUS 锚池 20 卡全覆盖收官件·冗余扩容位第十七件·源卡 CENSUS-v3 F-022 沈佩兰·R755 渲染腿）** | "
     u"lc-021-v1-shipinhao-60s.mp4（R-E shipinhao 12 段·11 柔转 0 硬切·58.079s=音轨分毫一致 1.921s 余量）+data/sources/lc021/cards-v1-matched.json（12/12 对位表+六卡前置修）+.lc021-tmp/s2-results.md（三门读数件）+fs-tile-heads.png+fs-tile-midtail.png+fs-pair-h00-h09-h11.png+fs-pair-m05-t00-t05.png（帧验采样与全分辨率定谳件） | "
     u"循环独立执法（ai_feel+层 1.8+spec 微信视频号·引擎脚本零 LLM）+帧验三律（会话多模态 tile+全分辨率定谳） | "
     u"收官腿待 R756（E8 终审+ASR 终轨+E4+M4→F-075 登记→冗余池第十七件→E21 出池=20 卡全覆盖收官+补池义务随轮领） | "
     u"ai_feel 0F0W（gaps 11 处 0.220-0.558s·pacing CV 0.272·prosody 9 档 12 拍·copy CV 0.285）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00 12/12+transition-share 1.00 无连排+timeline 代数过）+spec 微信视频号双 PASS（9:16+58.08s∈30-60s 1.9s 余量）·几何前置修六卡（b3/b5 size 46+b7 size 38+b4/b8/b9 语义断点+size 36/38 下探=R745 b8 修法族第二案·verbatim join 断言全过零字符→FINAL problems=NONE）·帧验=拍头 12/12 语义全中（H1 拍名逐拍对位+sys.beat 01→12 连续 t 单调+角标 12 帧全在+AIGC 帧头标识全在）+段中尾 6/6 零录穿（law2=动态三最长 b0/b4/b5〔6.53/5.74/7.34s〕·段中静态戳 sys.beat=06 t=00:24=§4.5 段起始口径·段尾状态行+字幕缺席=出段淡出带+R697 逐 cue 显隐律·段尾重影=crossfade 同版式双像=12 拍共用同源卡固有形态 R684/R745 同判）+回环 crossings={}（max 7.34s<源 13s）+AIGC 双标识分层可读（帧头 y≈55-80+卡面标签 y≈100-163 垂直错开零叠压）·tile 误读族全分辨率定谳（互证拍净读+物种行净读〔tile「青鸾源」伪读〕+段尾状态行缺失=淡出带=R189 手段问题律） |")
t += sr + '\n'
wr(p, t)
print('station-reviews updated')

# ---------- 3. lc021 README ----------
p = 'data/sources/lc021/README.md'
t = rd(p)
prod = (u"\n- [2026-09-30 R755 渲染腿毕] F-022 卡多模态九行全读（AIGC 标签位=卡面左上=同位族·来源行〔展示锚 C-00012〕在位核·卡面零〔〕注记核）→"
        u"census-card-v3-vertical.mp4 派生（F-022 PNG〔225,299B 核〕·scale 660+pad y=160+zoompan ≤1.04·13.000s·ffprobe 与 v15 参照逐参数一致 1080×1920@30）→"
        u"对位表 cards-v1-matched.json 12/12 逐拍 visual（visual-ratio 1.00·源卡即证据·锚 C-00012 字段展开同源多用注记）→"
        u"**R720 律前置几何修六卡**（b3/b4/b5/b7/b8/b9 @60px 5-8 行块顶 616-702 叠压=R711 五行块同型→b3/b5 per-card size 46〔5 行顶 787 净 20=修法地板〕+b7 size 38〔5 行顶 811 净 44〕+"
        u"**b4/b8/b9=语义断点预拆+阶梯下探 36/38=R745 b8 78 字修法族第二案**〔b4 76 字句子级断点 2 段+size 36=6 行顶 788 净 21/b8 69 字断点 2 段+size 38=5 行顶 811 净 44/b9 55 字断点 3 段+size 36=6 行顶 788 净 21〕·verbatim join 断言全过零字符）→"
        u"全卡几何审计 FINAL problems=NONE→R-E shipinhao 渲染 lc-021-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·58.079s ffprobe=音轨分毫一致·1.921s 余量·hits=[0,11]·S5.5 角标=BigStream|拆条 021·源城市图鉴 003+§4.5 三开关·plan.json 入 git）→"
        u"S2 三门循环独立执法全绿（ai_feel 0F0W gaps 11 处 0.220-0.558s·pacing CV 0.272·prosody 9 档 12 拍·copy CV 0.285+层 1.8 六面 PASS〔beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过〕+spec 微信视频号双 PASS〔9:16+58.08s∈30-60s 窗 1.9s 余量〕）→"
        u"帧验三律全过（拍头 12/12 语义全中+sys.beat 01→12 连续 t 单调+角标 12 帧全在+AIGC 帧头标识全在·段中尾 6/6 零录穿〔law2=动态三最长 b0/b4/b5 6.53/5.74/7.34s·段中静态戳 sys.beat=06 t=00:24=§4.5 段起始口径·段尾状态行+字幕缺席=出段淡出带+R697 逐 cue 显隐律·段尾重影=crossfade 同版式双像 R684/R745 同判〕·回环 crossings={} max 7.34s<源 13s·"
        u"AIGC 双标识分层可读〔帧头 y≈55-80+卡面左上标签 y≈100-163 垂直错开零叠压·fs-pair-h00-h09-h11 全分辨率实证〕·tile 误读族全分辨率定谳=互证拍净读+物种行净读〔tile「青鸾源」伪读〕=R189 手段问题律）——收官腿（E8+ASR+E4+M4→F-075 登记→冗余池第十七件→E21 出池=20 卡全覆盖收官）=R756 首位。\n")
marker = u"\n## 门禁块"
assert marker in t
t = t.replace(marker, prod + marker)
old_s2 = u"| S2 三门/帧验三律 | 未到（渲染腿） |"
new_s2 = (u"| S2 三门/帧验三律 | **毕〔R755〕**：三门全绿（ai_feel 0F0W+层 1.8 六面 PASS+spec 双 PASS 9:16+58.079s 1.921s 余量）+帧验三律全过（拍头 12/12+段中尾 6/6 零录穿+回环 {}+AIGC 双标识分层可读）+全卡几何审计 problems=NONE（六卡前置修） |")
assert old_s2 in t, 'gate block S2 row not found'
t = t.replace(old_s2, new_s2)
wr(p, t)
print('lc021 README updated')

# ---------- 4. queue burn row ----------
p = 'docs/self-improvement-queue.md'
t = rd(p).rstrip('\n')
qrow = (u"\n- 2026-09-30: **E21 LC-021 沈佩兰渲染腿毕（R755·R745/R741/R737 同型五步·产品优先律对位=本轮新实物=lc-021 成片在链）**："
        u"F-022 卡多模态探针（AIGC 标签位=卡面左上同位族·零修红）→census-card-v3-vertical 派生（F-022 PNG 225,299B·R511 法 13.000s）→对位表 12/12 visual-ratio 1.00→"
        u"**R720 律前置几何修六卡**（b3/b5 size 46+b7 size 38+b4/b8/b9 语义断点预拆+size 36/38 下探=R745 b8 78 字修法族第二案·b4 76 字/b8 69 字/b9 55 字·句子级断点 2/2/3 段·verbatim join 断言全过零字符→FINAL problems=NONE）→"
        u"R-E shipinhao 渲染 lc-021-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·58.079s=音轨分毫一致 1.921s 余量·hits=[0,11]·S5.5 角标=BigStream|拆条 021·源城市图鉴 003）→"
        u"S2 三门全绿（ai_feel 0F0W gaps 11 处 0.220-0.558s·pacing CV 0.272·copy CV 0.285+层 1.8 六面 PASS+spec 双 PASS 1.9s 余量）→"
        u"帧验三律全过（拍头 12/12 语义全中+sys.beat 01→12 连续·段中尾 6/6 零录穿〔law2=b0/b4/b5 6.53/5.74/7.34s·段尾重影=crossfade 同版式双像 R684/R745 同判·段尾状态行/字幕缺席=出段淡出带+R697 显隐律〕·回环 crossings={} max 7.34s<源 13s·"
        u"AIGC 双标识分层可读〔帧头 y≈55-80+卡面标签 y≈100-163 垂直错开零叠压·fs-pair 全分辨率实证〕·tile 误读族全分辨率定谳=互证拍净读/物种行净读〔tile「青鸾源」伪读〕/段尾状态行缺失=淡出带=R189 手段问题律+§4.5 口径）——"
        u"收官腿（E8+ASR+E4+M4→F-075 登记→冗余池第十七件→E21 出池=**20 卡全覆盖收官**+补池义务）=R756 首位·lane=LC-021〔active·渲染腿毕〕+BS-007 稿集件〔standby 候选〕维持 ≥2。")
t += qrow + '\n'
wr(p, t)
print('queue updated')

print('LEDGERS DONE')
