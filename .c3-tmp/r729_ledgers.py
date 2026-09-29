# -*- coding: utf-8 -*-
# R729 ledger appends: renders README (decl note + in-chain row), station-reviews row,
# queue burn row, lc015 README (production record + gate block update). Anchor-exact, assert-hit.
import io, sys

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'

def patch(path, anchor, addition, mode):
    with io.open(path, encoding='utf-8') as fh:
        t = fh.read()
    if t.count(anchor) != 1:
        print('FAIL anchor-count=%d in %s' % (t.count(anchor), path)); sys.exit(1)
    if mode == 'append-after':
        t = t.replace(anchor, anchor + addition)
    elif mode == 'append-line':
        t = t.replace(anchor, anchor + '\n' + addition)
    with io.open(path, 'w', encoding='utf-8') as fh:
        fh.write(t)
    print('OK', path)

# 1. renders README declaration line - append render-leg-closeout note
patch(ROOT + r'\output\renders\README.md',
      u'→收官腿（E8+ASR+E4+M4→F-070 登记→冗余池第十二件落位）随轮领。',
      u'**渲染腿毕 R729**（F-021 派生 census-card-v2-vertical 13.000s+对位表 12/12+S2 三门全绿 0F0W+帧验三律+全卡几何审计 problems=NONE·b0/b2 R720 律前置修 per-card size 54 块顶 802 净距 35px 像素实证）→收官腿=R730 首位。',
      'append-after')

# 2. renders README - in-chain table row after lc-014 row
ROW = (u"| lc-015-v1-shipinhao-60s.mp4 | **在链·渲染腿毕（R729·queue §E 批活池 E15 件·冗余扩容位第十二件·源卡=CENSUS-v2 F-021 朱鸿奎·收官腿 R730 随轮领=F-070 登记）** "
       u"| **R-E shipinhao 12 段 11 柔转场 0 硬切**·9:16 1080×1920·**57.615s ffprobe 实测=音轨分毫一致·2.385s 余量**·hits=[0,11]·**S5.5 角标常驻位**=BigStream\\|拆条 015·源城市图鉴 002+§4.5 三开关[glow/scanlines/sys.beat=NN t=MM:SS]·plan.series+s45_dials 入 plan.json·"
       u"**拆条形态对位=源卡即证据 12/12**（census-card-v2-vertical 源卡画面×12·visual-ratio 1.00·源件=F-021 PNG 派生 scale 660+pad y=160+zoompan ≤1.04·13.000s=LC-001~014 R511 法·ffprobe 与 v10 参照逐参数一致·素材探针先行=卡面九行全读+AIGC 标签位=卡面左上=同位族）——"
       u"**R720 律前置几何修（build 级审计驱动）**：b0 钩子 48 字/b2 城区职业 53 字副题 @60px 均 5 行块顶 745 叠压（R711 型）→per-card size 54 副题 3 行块顶 802 净距 35px（verbatim 零字符·版式参数律合法面）→**全卡几何审计 12 卡 problems=NONE**（b0/b2 像素实证 fs-h00/fs-h02 全分辨率块顶 805-815 vs 来源行 740-775 净空 35-50px·b11 声明行 130px+ 空带=R725 b4 修法地板同型）——"
       u"**S2 三门 R729 循环独立执法全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·pacing CV 0.255·prosody 9 档 12 拍·copy CV 0.287）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过）+spec 微信视频号双 PASS（9:16+57.62s ∈30-60s 窗 2.4s 余量）——"
       u"**帧验三律全过**：拍头 12/12 语义全中（H1 拍名 12/12 逐拍对位+sys.beat 01→12 连续无跳号 t 单调递增+角标 12 帧全在+AIGC 帧头标识全在）+段中尾 6/6 稳定零录穿（law2=动态三最长拍 b0/b5/b8〔5.96/6.97/6.57s〕·b8 段中 tile「无字幕」疑点全分辨率定谳=字幕两行净读 fs-m08〔R189 手段问题律〕·段尾帧字幕缺席=SRT 逐 cue 显隐律正常行为 R697 判例+段尾重影=crossfade 窗正常合成像 R684 同判）+回环 crossings={}（max 拍 6.97s<源 13s·诚实计算）+AIGC 双标识分层可读（帧头标识+卡面左上标签垂直错开零叠压·fs-pair-h00-h11 全分辨率实证·R511 避让法前置执行零修红） "
       u"| plan.json 入 git·收官腿 R730 随轮领（E8 终审七席+ASR 终轨+E4 同轮回填+M4→F-070 登记→冗余池第十二件落位→release-schedule v2.7→E15 出池+补池义务随轮领） |")
patch(ROOT + r'\output\renders\README.md',
      u'→queue §E E14 出池（lane=LC-015 standby 单条<2·补池义务注记） |',
      ROW, 'append-line')

# 3. station-reviews - R729 S2 machine-check row
SR = (u"| 2026-09-30 | **S2 三门循环独立执法+帧验三律+全卡几何审计前置修零缺陷（lc-015-v1-shipinhao=queue §E 批活池 E15 件·冗余扩容位第十二件·源卡 CENSUS-v2 F-021 朱鸿奎·R729 渲染腿）** "
      u"| lc-015-v1-shipinhao-60s.mp4（R-E shipinhao 12 段·11 柔转场 0 硬切·57.615s=音轨分毫一致 2.385s 余量）+cards-v1-matched（b0/b2 几何前置修件）+r729_card_audit.txt "
      u"| 循环独立执法（ai_feel+层 1.8+spec 微信视频号·纯脚本机检零 LLM）+帧验三律（会话内建多模态+全分辨率 pair） | —（机检档·E8 终审待收官腿 R730） "
      u"| **b0/b2 前置修=R720 律预执行**（R711 五行块叠压前科→b0 钩子 48 字/b2 城区职业 53 字副题 @60px 均 5 行块顶 745→build 级审计驱动 per-card size 54 副题 3 行块顶 802 净距 35px·verbatim 零字符·版式参数律）→**全卡几何审计 12 卡 problems=NONE**（r729_card_audit·b0/b2 像素实证 fs-h00/fs-h02 块顶 805-815 vs 来源行 740-775 净空 35-50px=R725 b4 修法地板同型）+S2 三门全绿（ai_feel 0F0W gaps 11 处 0.220-0.558s·pacing CV 0.255·prosody 9 档·copy CV 0.287+层 1.8 六面 PASS visual-ratio 1.00 12/12+spec 双 PASS 9:16+57.62s 2.4s 余量）+帧验三律全过（拍头 12/12〔H1 逐拍+sys.beat 01→12 连续+角标+AIGC 全帧〕+段中尾 6/6 零录穿〔law2=b0/b5/b8 5.96/6.97/6.57s·b8 段中 tile「无字幕」疑点全分辨率定谳=字幕两行净读 fs-m08·R189 手段问题律·段尾字幕缺席=R697 显隐律判例·段尾重影=crossfade 正常〕+回环 crossings={}〔max 6.97s<源 13s〕+AIGC 双标识分层可读） |")
patch(ROOT + r'\docs\reviews\station-reviews.md',
      u'（release-schedule v2.6·视频号冗余弹药 11 件）+queue §E E14 出池（lane=LC-015 standby 单条<2） |',
      SR, 'append-line')

# 4. queue burn row
BURN = (u"- 2026-09-30: **E15 LC-015 渲染腿毕（R729·R728 claim 兑现·R710/R725 同型五步）：F-021 卡面九行全读→census-card-v2-vertical 13.000s 派生（ffprobe 与 v10 参照逐参数一致）→对位表 12/12 visual-ratio 1.00→"
        u"R720 律前置修（b0 钩子 48 字/b2 城区职业 53 字 @60px 均 5 行块顶 745 叠压〔R711 型〕→per-card size 54 副题 3 行块顶 802 净距 35px·verbatim 零字符·版式参数律）→"
        u"lc-015-v1-shipinhao-60s.mp4 57.615s 音轨分毫一致 2.385s 余量（12 段 11 柔 0 硬切·hits=[0,11]·角标=拆条 015·源城市图鉴 002）→全卡几何审计 12 卡 problems=NONE（b0/b2 像素实证净空 35-50px）→"
        u"S2 三门全绿 0F0W（ai_feel CV 0.255/0.287+层 1.8 六面+spec 双 PASS 2.4s 余量）→帧验三律全过（拍头 12/12+段中尾 6/6 零录穿〔b8 tile 疑点全分辨率定谳字幕净读·R697 显隐律判例·crossfade 正常〕+crossings={}〔max 6.97s<源 13s〕+AIGC 双标识分层）——"
        u"收官腿（E8+ASR+E4+M4→F-070 登记→冗余池第十二件→release-schedule v2.7→E15 出池+补池义务）=R730 首位；lane=E15 active+E16 standby 维持 ≥2**")
patch(ROOT + r'\docs\self-improvement-queue.md',
      u'收官腿（E8+ASR+E4+M4→F-070→冗余池第十二件→E15 出池）=后续轮领；lane=E15 active+E16 standby 维持 ≥2**',
      BURN, 'append-line')

# 5. lc015 README production record
REC = (u"- [2026-09-30 06:4x R729 渲染腿毕（R728 claim 兑现·R710/R725 同型五步）] 素材探针=F-021 卡多模态九行全读（AIGC 标签位=卡面左上=同位族·R511 避让法前置执行）→census-card-v2-vertical.mp4 派生（F-021 PNG·scale 660+pad y=160+zoompan ≤1.04·13.000s·ffprobe 与 v10 参照逐参数一致 1080×1920@30）→对位表 cards-v1-matched.json 12/12 逐拍 visual（源卡即证据·钩子/信条行 verbatim 直引·b9 第七对人物链互证拍〔C-00011×C-00017 双端在册〕·visual-ratio 1.00·正位数据件入 git）→"
       u"**R720 律前置几何修（build 级审计驱动）**：b0 钩子 48 字/b2 城区职业 53 字副题 @60px 均 5 行块顶 745 叠压（R711 型）→per-card size 54 副题 3 行块顶 802 净距 35px（verbatim 零字符·版式参数律合法面）→R-E shipinhao 渲染 lc-015-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·57.615s ffprobe=音轨分毫一致·2.385s 余量·hits=[0,11]·S5.5 角标=BigStream|拆条 015·源城市图鉴 002+§4.5 三开关·plan.json 入 git）；"
       u"**全卡几何审计 12 卡 problems=NONE**（r729_card_audit·b0/b2 像素实证 fs-h00/fs-h02 全分辨率块顶 805-815 vs 来源行 740-775 净空 35-50px·b11 声明行 130px+ 空带）；"
       u"**S2 三门循环独立执法全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·pacing CV 0.255·prosody 9 档 12 拍·copy CV 0.287）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过）+spec 微信视频号双 PASS（9:16+57.62s ∈30-60s 窗 2.4s 余量）；"
       u"**帧验三律全过**：拍头 12/12 语义全中（H1 拍名 12/12+sys.beat 01→12 连续 t 单调+角标 12 帧全在+AIGC 帧头标识全在）+段中尾 6/6 零录穿（law2=b0/b5/b8 动态三最长 5.96/6.97/6.57s·b8 段中 tile「无字幕」疑点全分辨率定谳=字幕两行净读 fs-m08〔R189 手段问题律〕·段尾帧字幕缺席=SRT 逐 cue 显隐律 R697 判例·b0 段尾重影=crossfade 窗正常合成像 R684 同判）+回环 crossings={}（max 6.97s<源 13s 诚实计算）+AIGC 双标识分层可读（帧头+卡面标签垂直错开零叠压·fs-pair-h00-h11 全分辨率实证）。")
patch(ROOT + r'\data\sources\lc015\README.md',
      u'——v1-v3 beats 全留档·渲染腿（R710/R725 同型五步+全卡几何审计）=R729 首位。',
      REC, 'append-line')

# 6. lc015 README gate block update
patch(ROOT + r'\data\sources\lc015\README.md',
      u'·渲染腿/收官腿=后续轮领（R710/R725 渲染五步+E8+ASR+E4+M4→F-070→冗余池第十二件→E15 出池）。',
      u'·**渲染腿毕 R729**（F-021 派生 census-card-v2-vertical 13.000s+对位表 12/12+R720 律前置修 b0/b2 size 54 块顶 802 净距 35px+全卡几何审计 problems=NONE+S2 三门全绿 0F0W·57.62s 双 PASS 2.4s 余量+帧验三律全过）·收官腿=R730 首位（E8+ASR+E4+M4→F-070→冗余池第十二件→E15 出池）。',
      'append-after')

print('LEDGERS_DONE')
