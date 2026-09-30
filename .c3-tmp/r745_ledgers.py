# -*- coding: utf-8 -*-
# R745 ledgers: renders README (decl line + in-chain row) + station-reviews row + lc019 README + queue E16 burn row
import io, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'

def rw(p):
    with io.open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()

def wr(p, s):
    with io.open(os.path.join(ROOT, p), 'w', encoding='utf-8') as f:
        f.write(s)

# ---------- 1. renders README ----------
p = 'output/renders/README.md'
t = rw(p)
OLD_DECL = (u"→S2 三门+帧验三律+全卡几何审计 R720 律前置随轮领·收官腿〔E8+ASR+E4+M4→F-074→冗余池第十六件→E16 出池+补池〕随轮领）")
NEW_DECL = (u"→S2 三门+帧验三律+全卡几何审计 R720 律前置=R745 毕〔五卡 per-card size 前置修+b8 fleet 最长 col2 78 字语义预拆+size 36 专项修"
            u"+S2 三门全绿+帧验三律全过·详见下表在链行〕·收官腿〔E8+ASR+E4+M4→F-074→冗余池第十六件→E16 出池+补池〕=R746 随轮领）")
assert t.count(OLD_DECL) == 1, 'decl anchor not unique: %d' % t.count(OLD_DECL)
t = t.replace(OLD_DECL, NEW_DECL)

ROW = (u"| lc-019-v1-shipinhao-60s.mp4 | **在链件·渲染腿毕（R745·queue §E 批活池 E16 件·冗余扩容位第十六件·源卡=CENSUS-v5 F-024 周浩宇·"
       u"R743 起链→R744 定稿音轨→R745 渲染腿毕：S2 三门全绿+帧验三律全过+几何审计 problems=NONE·收官腿〔E8+ASR+E4+M4→F-074〕=R746 待领·"
       u"第十对人物链互证闭环后半件=敬畏验证主题首件位）** | **R-E shipinhao 12 段 11 柔转场 0 硬切**·9:16 1080×1920·"
       u"**57.235s ffprobe 实测=音轨分毫一致·2.765s 余量**〔plan 内部预估 58.033s=tail 余量项·实测为准·LC-008 判例〕·hits=[0,11]·"
       u"S5.5 角标常驻位=BigStream\\|拆条 019·源城市图鉴 005+§4.5 三开关[glow/scanlines/sys.beat=NN t=MM:SS] | "
       u"**视觉动态位=源卡即证据 12/12**（census-card-v5-vertical 源卡画面×12·visual-ratio 1.00·源件=F-024 PNG〔224,256B 核〕派生"
       u"scale 660+pad y=160+zoompan ≤1.04·13.000s=R511 法·ffprobe 与 v15 参照逐参数一致 1080×1920@30·素材探针先行=卡面九行全读"
       u"+AIGC 标签位=卡面左上=同位族·R511 避让法前置执行零修红·来源行〔展示锚 C-00014〕在位核·卡面零〔〕注记核）——"
       u"**R720 律前置几何修（build 级审计驱动）**：b4/b5/b6/b7 @60px 5-7 行块顶 659-745 叠压（R711 型）→per-card size 56/54/50/46 verbatim 零字符"
       u"（b4 4 行顶 798 净 31/b5 4 行顶 802 净 35/b6 4 行顶 812 净 45/b7 5 行顶 787 净 20=修法地板）+"
       u"**b8=78 字 fleet 最长 col2 单行专项修（LC-017 最长 61 对照·fleet 首例）**：size 阶梯 56-46 全档 6-7 行必叠压（r745_wrap_probe.txt em 数学实证）"
       u"→语义断点预拆 5 段（newline-only 零字符=R719/R725 先例族）+per-card size 36（**阶梯下探 fleet 地板 46 之下首例·em 数学在案证据件**）"
       u"=块 6 行顶 788 净 21px≥787 修法地板·全语义断行（防 greedy-36 中词断「…天理」。进|了扭塔…」）——**全卡几何审计 FINAL problems=NONE**——"
       u"**S2 三门 R745 循环独立执法全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·pacing CV 0.282·prosody 9 档 12 拍·copy CV 0.291）"
       u"+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过）"
       u"+spec 微信视频号双 PASS（9:16+57.23s ∈30-60s 窗 2.8s 余量）——**帧验三律全过**：拍头 12/12 语义全中"
       u"（H1 拍名 12/12 逐拍对位+sys.beat 01→12 连续〔t=§4.5 段起始静态戳口径〕+角标 12 帧全在+AIGC 帧头标识全在）"
       u"+段中尾 6/6 稳定零录穿（law2=动态三最长拍 b5/b8/b9〔6.78/5.90/6.95s〕·段尾帧字幕缺席=SRT 逐 cue 显隐律正常行为 R697 判例"
       u"+段尾重影=crossfade 窗正常合成像 R684 族+段尾 HUD 行渐隐=出段淡出带 §4.5 设计口径）+回环 crossings={}（max 拍 6.95s<源 13s·诚实计算）"
       u"+AIGC 双标识分层可读（帧头 y≈55+卡面左上标签 y≈122-165 垂直错开零叠压·fs-pair-h00-h09-h11 全分辨率实证）+"
       u"**b8 专项帧 fs-h08 全分辨率实证**（6 行块逐行 verbatim 净读+来源行「基于硅基城市居民户籍卡档案（展示锚 C-00014）」完整可读零叠压+净隙 ~21px=R720 修法地板持位）"
       u"+tile 缩略误读四点全分辨率定谳（b5 时码 00:35→实 00:16〔fs-h04〕/底注「基于硅基城市」/b8 副文小字〔fs-h08〕/HUD t=00:53→实 00:35=R189 手段问题律）"
       u"+SRT cue 9 与 beats col3 字面核 byte-check 12/12 逐字一致（读端伪差当轮咬住·四源互证零漂移：audio/SRT/voiceover/裁链脚本） | "
       u"plan.json 入 git·mp4 gitignored·**R745 渲染腿毕**（S2 三门+帧验三律+几何审计全绿·收官腿 E8+ASR+E4+M4→F-074=R746 随轮领） |")
assert 'lc-019-v1-shipinhao-60s.mp4 |' not in t, 'in-chain row already present'
lines = t.splitlines(True)
# append after last non-empty line (table ends with lc-018 row)
while lines and not lines[-1].strip():
    lines.pop()
lines.append(ROW + u"\n")
wr(p, u''.join(lines))
print('renders README: decl updated + in-chain row appended')

# ---------- 2. station-reviews ----------
p = 'docs/reviews/station-reviews.md'
t = rw(p)
SR_ROW = (u"| 2026-09-30 | **S2 三门循环独立执法+帧验三律+全卡几何审计前置修（lc-019-v1-shipinhao=queue §E 批活池 E16 件渲染腿·冗余扩容位第十六件·"
          u"源卡 CENSUS-v5 F-024 周浩宇·R745 渲染腿）** | lc-019-v1-shipinhao-60s.mp4（57.235s ffprobe 实测=音轨分毫一致 2.765s 余量）+"
          u".lc019-tmp/s2-results.md（三门读数件）+fs-tile-heads.png+fs-tile-midtail.png+fs-pair-h00-h09-h11.png+fs-h04.png/fs-h08.png"
          u"（全分辨率定谳件）+r745_wrap_probe.txt（b8 em 数学证据件）+data/sources/lc019/cards-v1-matched.json（12/12 对位表） | "
          u"S2 三门=纯脚本机检（ai_feel_check/platform_spec_check/edit_craft_check）；帧验=会话内建多模态零本地模型；渲染=R-E shipinhao 本地链 | "
          u"**S2 三门全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·pacing CV 0.282·prosody 9 档 12 拍·copy CV 0.291）"
          u"+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过）"
          u"+spec 微信视频号双 PASS（9:16+57.23s∈30-60s 窗 2.8s 余量）→**帧验三律全过**：拍头 12/12 语义全中+段中尾 6/6 稳定零录穿"
          u"（law2=动态三最长 b5/b8/b9·段尾字幕缺席=SRT 逐 cue 显隐律 R697 判例·段尾重影=crossfade 正常合成像 R684 族）+回环 crossings={}"
          u"（max 6.95s<源 13s 诚实计算）+AIGC 双标识分层可读（垂直错开零叠压）+**b8 专项修实证**（78 字 fleet 最长 col2 语义预拆 5 段+size 36"
          u"=块 6 行顶 788 净 21px≥787 修法地板·fs-h08 全分辨率=6 行 verbatim 净读+来源行零叠压+**阶梯下探 fleet 地板 46 之下首例**·em 数学证据件在案）"
          u"+tile 缩略误读四点全分辨率定谳（R189 手段问题律）+SRT cue 9 byte-check 12/12 逐字一致（读端伪差当轮咬住） |")
assert 'lc-019-v1-shipinhao' not in t.splitlines()[-1] if t.splitlines() else True
if 'R745 渲染腿）**' not in t:
    t = t.rstrip(u'\n') + u"\n" + SR_ROW + u"\n"
    wr(p, t)
    print('station-reviews: R745 S2 row appended')
else:
    print('station-reviews: row already present, skip')

# ---------- 3. lc019 README ----------
p = 'data/sources/lc019/README.md'
t = rw(p)
PROD = (u"\n- [2026-09-30 12:0x R745 渲染腿毕（R744 claim 兑现·R741/R737 同型五步）] 素材探针先行=F-024 卡多模态九行全读"
        u"（AIGC 标签位=卡面左上=同位族·R511 避让法前置执行零修红·来源行「基于硅基城市居民户籍卡档案（展示锚 C-00014）」在位核·卡面零〔〕注记核）"
        u"→自产源件 data/sources/footage/census-card-v5-vertical.mp4（F-024 PNG〔224,256B 核〕派生·scale 660+pad y=160+zoompan ≤1.04·13.000s·"
        u"ffprobe 与 v15 参照逐参数一致 1080×1920@30）→对位表 cards-v1-matched.json 12/12 逐拍 visual（源卡即证据·锚 C-00014 字段展开同源多用注记·"
        u"b9 互证拍=第十对人物链闭环后半件+第十一对徐根福前件埋点·col2 纯 verbatim 零〔〕=R743 起链前置规避核 12/12·visual-ratio 1.00·正位数据件入 git）"
        u"→**R720 律前置几何修（build 级审计驱动）**：b4/b5/b6/b7 per-card size 56/54/50/46（4/4/4/5 行块顶 798/802/812/787 净 31/35/45/20px·零字符）+"
        u"**b8=78 字 fleet 最长 col2 单行专项修（LC-017 最长 61 对照·fleet 首例）**：size 阶梯 56-46 全档 6-7 行必叠压"
        u"（r745_wrap_probe.txt em 数学实证：punct-preference 断行 46px 处 6 行 top 717.8）→语义断点预拆 5 段（newline-only 零字符=R719/R725 先例族）"
        u"+per-card size 36（**阶梯下探 fleet 地板 46 之下首例·78 字 60px 初 8 行块顶 616 叠压驱动**）=块 6 行顶 788 净 21px≥787 修法地板·"
        u"全语义断行（防 greedy-36 中词断「…天理」。进|了扭塔…」）→**全卡几何审计 FINAL problems=NONE**→"
        u"R-E shipinhao 渲染 lc-019-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·**57.235s ffprobe 实测=音轨分毫一致·2.765s 余量**"
        u"〔plan 内部预估 58.033s=tail 余量项·实测为准 LC-008 判例〕·hits=[0,11]·S5.5 角标=BigStream|拆条 019·源城市图鉴 005+§4.5 三开关·plan.json 入 git）"
        u"→**S2 三门循环独立执法全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·pacing CV 0.282·prosody 9 档 12 拍·copy CV 0.291）"
        u"+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过）"
        u"+spec 微信视频号双 PASS（9:16+57.23s∈30-60s 窗 2.8s 余量）→**帧验三律全过**：拍头 12/12 语义全中"
        u"（H1 拍名 12/12+sys.beat 01→12 连续〔t=§4.5 段起始静态戳口径〕+角标 12 帧全在+AIGC 帧头标识全在）+段中尾 6/6 稳定零录穿"
        u"（law2=动态三最长拍 b5/b8/b9〔6.78/5.90/6.95s〕·段尾帧字幕缺席=SRT 逐 cue 显隐律正常行为 R697 判例·段尾重影=crossfade 窗正常合成像 R684 族"
        u"·段尾 HUD 行渐隐=出段淡出带 §4.5 设计口径）+回环 crossings={}（max 拍 6.95s<源 13s·诚实计算）"
        u"+AIGC 双标识分层可读（帧头 y≈55+卡面左上标签 y≈122-165 垂直错开零叠压·fs-pair-h00-h09-h11 全分辨率实证）"
        u"+**b8 专项帧 fs-h08 全分辨率实证**（6 行块逐行 verbatim 净读+来源行完整可读零叠压+净隙 ~21px=R720 修法地板持位）"
        u"+tile 缩略误读四点全分辨率定谳（b5 时码 00:35→实 00:16〔fs-h04〕/底注「基于硅基城市」/b8 副文小字〔fs-h08〕/HUD t=00:53→实 00:35=R189 手段问题律）"
        u"+**SRT cue 9 与 beats col3 字面核 byte-check 12/12 逐字一致**（读端伪差当轮咬住：read_file 显示长式 vs 盘上 24 字短式——"
        u"audio/SRT/voiceover.txt/裁链脚本四源互证=盘上短式为真相·fs-h08 字幕同读数·ai_feel 门 0F0W 合法性复核过）。\n")
anchor = u"\n## 门禁块"
assert anchor in t, 'gate-block anchor missing'
assert 'R745 渲染腿毕（R744 claim 兑现' not in t, 'prod row already present'
t = t.replace(anchor, PROD + anchor, 1)
OLD_GATE = u"渲染腿=待领·收官腿=待领。发布锁=M5 账号物理件不变（未上线=未测量）。"
NEW_GATE = (u"**渲染腿=R745 毕**（S2 三门全绿+帧验三律全过+几何审计 problems=NONE+b8 fleet 最长 col2 语义预拆+size 36 专项修）"
            u"·收官腿=待领（E8+ASR+E4+M4→F-074 登记→冗余池第十六件→E16 出池+补池）。发布锁=M5 账号物理件不变（未上线=未测量）。")
assert t.count(OLD_GATE) == 1, 'gate anchor not unique: %d' % t.count(OLD_GATE)
t = t.replace(OLD_GATE, NEW_GATE)
wr(p, t)
print('lc019 README: prod row + gate block updated')

# ---------- 4. queue E16 burn row ----------
p = 'docs/self-improvement-queue.md'
t = rw(p)
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
    if u'E16 空气预算裁链定稿+TTS 定稿音轨毕（R744' in l:
        idx = i
        break
assert idx is not None, 'queue E16 R744 line not found'
assert u'E16 LC-019 渲染腿毕（R745' not in t, 'queue row already present'
lines.insert(idx + 1, QROW)
wr(p, u''.join(lines))
print('queue: E16 R745 burn row inserted after R744 line (idx %d)' % idx)
print('LEDGERS_DONE')
