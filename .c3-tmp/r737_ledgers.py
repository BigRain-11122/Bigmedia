# -*- coding: utf-8 -*-
# R737: LC-017 render-leg ledger close (renders README + station-reviews + lc017 README + queue)
import io, json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

def rd(p):
    return io.open(ROOT + "\\" + p, encoding="utf-8").read()

def wr(p, t):
    io.open(ROOT + "\\" + p, "w", encoding="utf-8", newline="").write(t)

# ---------- 1. renders README ----------
p = "output/renders/README.md"
t = rd(p)
anchor_decl = u"——同性质非成品·不入本台账成品位·mp4/音轨 gitignored 盘上留档"
assert t.count(anchor_decl) >= 1, "decl anchor missing"
# only the LC-017 declaration row (L104) carries .lc017-tmp
i = t.find(u".lc017-tmp")
j = t.find(anchor_decl, i)
assert 0 < i < j, "lc017 decl row layout drift"
t = t[:j] + (u"——同性质非成品·不入本台账成品位·mp4/音轨 gitignored 盘上留档"
             u"（**R737 渲染腿收口**：成片 lc-017-v1-shipinhao-60s.mp4 58.502s ffprobe 实测=音轨分毫一致 1.498s 余量+S2 三门全绿"
             u"〔ai_feel 0F0W+层 1.8 六面+spec 双 PASS〕+帧验三律全过+全卡几何审计 12 卡 problems=NONE+s2-results.md+fs-* 帧样件族同目录·"
             u"收官腿=E8+ASR+E4+M4→F-072=R738 待办）") + t[j + len(anchor_decl):]

inchain = (u"\n| lc-017-v1-shipinhao-60s.mp4 | **在链件·冗余扩容位第十四件（queue §E 批活池 E18 件·源卡=CENSUS-v4 F-023 林之恒·"
           u"R735 起链→R736 定稿音轨→R737 渲染腿毕：S2 三门全绿+帧验三律全过+全卡几何审计 problems=NONE·第九对人物链双卡互记+档案记忆主题首件位）** | "
           u"**R-E shipinhao 12 段 11 柔 0 硬切**·9:16 1080×1920·**58.502s ffprobe 实测=音轨分毫一致·1.498s 余量**·hits=[0,11]·"
           u"**S5.5 角标常驻位**=BigStream\\|拆条 017·源城市图鉴 004+§4.5 三开关（[glow/scanlines/sys.beat=NN t=MM:SS]）·plan.json 入 git·"
           u"**视觉动态位=源卡即证据 12/12**（census-card-v4-vertical 源画面共享 12 拍·visual-ratio 1.00·源件=F-023 PNG〔215,466B 核〕派生 "
           u"scale 660+pad y=160+zoompan ≤1.04·13.000s=LC-001~016 R511 法〔ffprobe 与 v15 参照逐参数一致〕·素材探针先行=F-023 卡多模态九行全读·"
           u"AIGC 标签位=卡面左上=同位族·R511 避让法直接适用零修红）·"
           u"**b0/b4/b5/b6/b7/b8/b9 前置几何修（R720 律预执行·build 级审计驱动）**：七卡 @60px 5-9 行块顶 573-745 叠压（R711 五行块同型）→"
           u"per-card size 52/56/46/46/46/46/46 verbatim 零字符（b0 4 行顶 807 净 40/b4 4 行顶 798 净 31/b5+b6+b7 5 行顶 787 净 20=修法地板/"
           u"b8 4 行顶 822 净 55/b9 4 行顶 822 净 55）·**全卡几何审计 12 卡 problems=NONE**（r737_card_audit=R721 E8 帧验执法面常驻第五件）·"
           u"**b9 卡面注记剥离迁移**（col2 内嵌生产溯源注记〔C-00010 年轮「小林馆员照例来买粢饭」双卡互记·令牌号字面=脱敏律选材排除〕="
           u"R735 起链笔误·fleet 扫描 lc001-lc016 卡面零〔〕先例→渲染腿迁回 REQS 溯源层〔verbatim 保真存 cards-v1-matched.json visual.req〕·"
           u"卡面=锚字段 verbatim 零动·beats/S1 材料零接触·R512 脱敏决策维持）·"
           u"**S2 三门 R737 循环独立执法全绿**（ai_feel 0F0W gaps 11 处 0.239-0.558s·pacing CV 0.244·prosody 9 档 12 拍·copy CV 0.287"
           u"+层 1.8 六面 PASS beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过"
           u"+spec 微信视频号双 PASS 9:16+58.50s∈30-60s 窗 1.5s 余量）·"
           u"**帧验三律全过**（拍头 12/12 H1 拍名语义全中+sys.beat 01→12 连续 t 单调+角标 12 帧全在+AIGC 帧头标识全在·"
           u"段中尾 6/6 稳定零录穿 law2=动态三最长 b5/b8/b9〔5.65/6.78/7.10s〕·段尾重影=crossfade 窗正常合成像 R684 同判·"
           u"段尾字幕缺席=SRT 逐 cue 显隐律 R697 判例·**段尾 sys.beat 戳缺席=cue 锁定窗正常行为新判例**〔S4.5(3) one-per-cue 设计·"
           u"render_card_video L424 注·cue10 终 48.543s<尾采样 48.82s·拍头 fs-h09 全分辨率实证 sys.beat=10 t=00:41 在位〕·"
           u"tile 缩略疑点全分辨率定谳=「誊」≠「誉」+来源行完整+顾阿凤行完整=R189 手段问题律·"
           u"回环 crossings={} max 7.10s<源 13s 诚实计算·AIGC 双标识分层可读 fs-t09 全分辨率实证〔帧头 y≈55-75+卡面标签垂直错开零叠压〕） | "
           u"plan.json 入 git·mp4 gitignored·**R738 收官腿待办**（E8 终审+ASR 终轨+E4 参考仪+M4→F-072 登记→冗余池第十四件落位→"
           u"E18 出池+补池义务随轮领·发布锁=M5 账号物理件未开·未上线=未测量） | \n")
t = t.rstrip("\n") + "\n" + inchain
wr(p, t)
print("renders README ok")

# ---------- 2. station-reviews ----------
p = "docs/reviews/station-reviews.md"
t = rd(p)
row = (u"| 2026-09-30 | **S2 三门循环独立执法+帧验三律+全卡几何审计前置七卡修+b9 注记剥离（lc-017-v1-shipinhao=queue §E 批活池 E18 渲染腿·"
       u"冗余扩容位第十四件·源卡 CENSUS-v4 F-023 林之恒·R737 渲染腿）** | "
       u"lc-017-v1-shipinhao-60s.mp4（R-E shipinhao 12 段·11 柔转 0 硬切·58.502s=音轨分毫一致 1.498s 余量）"
       u"+cards-v1-matched（七卡前置修+b9 注记剥离注记）+r737_card_audit.txt+fs 采样件族+s2-results.md | "
       u"循环独立执法（ai_feel+层 1.8+spec 微信视频号·引擎脚本零 LLM）+帧验三律（会话多模态 tile+全分辨率定谳） | "
       u"收官腿待 R738（E8 终审+ASR 终轨+E4+M4→F-072 登记→冗余池第十四件→E18 出池+补池义务） | "
       u"**七卡前置修=R720 律预执行**（build 级审计驱动：b0/b4/b5/b6/b7/b8/b9 @60px 5-9 行块顶 573-745 叠压=R711 五行块同型·"
       u"b9 82 字块 size 单参不可修→**注记剥离迁 REQS 溯源层后** size 46 4 行顶 822 净 55px）·"
       u"**b9 卡面注记剥离迁移**（col2 内嵌生产溯源注记=R735 起链笔误〔fleet 扫描 lc001-lc016 卡面+beats col2 零〔〕先例〕·"
       u"verbatim 存 visual.req·卡面锚字段零动·beats/S1 材料零接触·R512 脱敏决策维持）·"
       u"**全卡几何审计 12 卡 problems=NONE**（R721 E8 帧验执法面常驻第五件）"
       u"+S2 三门全绿（ai_feel 0F0W gaps 11 处 0.239-0.558s·pacing CV 0.244·prosody 9 档 12 拍·copy CV 0.287"
       u"+层 1.8 六面 PASS visual-ratio 1.00 12/12+spec 双 PASS 9:16+58.50s 1.5s 余量）"
       u"+帧验三律全过（拍头 12/12 H1 拍名语义全中+sys.beat 01→12 连续 t 单调+角标 12 帧全在+AIGC 帧头标识全在·"
       u"段中尾 6/6 稳定零录穿 law2=动态三最长 b5/b8/b9〔5.65/6.78/7.10s〕·段尾重影=crossfade 窗正常合成像 R684 同判·"
       u"段尾字幕缺席=SRT 逐 cue 显隐律 R697 判例·**段尾 sys.beat 戳缺席=cue 锁定窗正常行为新判例**〔S4.5(3) one-per-cue 设计·"
       u"render_card_video L424 注·cue10 终 48.543s<尾采样 48.82s·拍头 fs-h09 全分辨率实证 sys.beat=10 t=00:41 在位〕·"
       u"tile 缩略疑点全分辨率定谳=「誊」≠「誉」/来源行完整/顾阿凤行完整=R189 手段问题律·回环 crossings={} max 7.10s<源 13s 诚实计算·"
       u"AIGC 双标识分层可读 fs-t09 全分辨率实证〔帧头 y≈55-75+卡面标签垂直错开零叠压〕） | \n")
t = t.rstrip("\n") + "\n" + row
wr(p, t)
print("station-reviews ok")

# ---------- 3. lc017 README ----------
p = "data/sources/lc017/README.md"
t = rd(p)
prod = (u"- [2026-09-30 09:xx R737 渲染腿毕] F-023 卡多模态九行全读（AIGC 标签位=卡面左上=同位族·R511 避让法直接适用零修红）→"
        u"自产源件 data/sources/footage/census-card-v4-vertical.mp4（F-023 PNG〔215,466B 核〕派生·scale 660+pad y=160+zoompan ≤1.04·"
        u"13.000s·ffprobe 与 v15 参照逐参数一致 1080×1920@30）→对位表 cards-v1-matched.json 12/12 逐拍 visual（源卡即证据·"
        u"锚 C-00013 字段展开同源多用注记·b9=第九对人物链卡面双端互证拍〔C-00013×C-00010 双端在册·LC-016 F-071 当日收官前件直连〕·"
        u"visual-ratio 1.00·正位数据件入 git）→**R720 律前置几何修（build 级审计驱动）**：七卡 @60px 5-9 行块顶 573-745 叠压→"
        u"per-card size 52/56/46/46/46/46/46 verbatim 零字符（全 ≥787 修法地板·b9 82 字块 size 单参不可修）→"
        u"**b9 卡面注记剥离迁移**（col2 内嵌生产溯源注记〔C-00010 年轮…双卡互记·令牌号字面=脱敏律选材排除〕=R735 起链笔误·"
        u"fleet 扫描 lc001-lc016 卡面零〔〕先例→渲染腿迁回 REQS 溯源层 verbatim 保真·卡面=锚字段 verbatim 零动·beats/S1 材料零接触·"
        u"R512 脱敏决策维持）→R-E shipinhao 渲染 lc-017-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·58.502s ffprobe=音轨分毫一致·"
        u"1.498s 余量·hits=[0,11]·S5.5 角标=BigStream|拆条 017·源城市图鉴 004+§4.5 三开关·plan.json 入 git）→"
        u"S2 三门循环独立执法全绿（ai_feel 0F0W gaps 11 处 0.239-0.558s·pacing CV 0.244·prosody 9 档 12 拍·copy CV 0.287+"
        u"层 1.8 六面 PASS+spec 微信视频号双 PASS 9:16+58.50s∈30-60s 窗 1.5s 余量）+全卡几何审计 12 卡 problems=NONE+"
        u"帧验三律全过（拍头 12/12+段中尾 6/6 零录穿+回环 crossings={}+AIGC 双标识全分辨率分层可读·"
        u"段尾 sys.beat 戳缺席=cue 锁定窗正常行为新判例〔S4.5(3) one-per-cue·cue10 终 48.543s<采样 48.82s〕·"
        u"tile 缩略疑点全分辨率定谳=「誊」≠「誉」/来源行完整=R189 手段问题律）。\n")
gate_old = (u"·渲染腿/收官腿=后续轮领（F-023 PNG 派生 census-card-v4-vertical·R511 法+全卡几何审计 R720 律→E8+ASR+E4+M4→F-072 登记→"
            u"冗余池第十四件）。发布锁=M5 账号物理件不变（未上线=未测量）。")
gate_new = (u"·**渲染腿=毕（R737：S2 三门全绿+帧验三律全过+全卡几何审计 problems=NONE+七卡前置修+b9 注记剥离迁 REQS）**·"
            u"收官腿=R738 待办（E8+ASR+E4+M4→F-072 登记→冗余池第十四件落位→E18 出池+补池义务随轮领）。"
            u"发布锁=M5 账号物理件不变（未上线=未测量）。")
assert gate_old in t, "gate anchor missing in lc017 README"
t = t.replace(gate_old, gate_new)
t = t.rstrip("\n") + "\n" + prod
wr(p, t)
print("lc017 README ok")

# ---------- 4. queue burn row ----------
p = "docs/self-improvement-queue.md"
t = rd(p)
burn = (u"- 2026-09-30: **E18 LC-017 林之恒拆条渲染腿毕（R737·R736 claim 承接·R729/R733 同型五步·实活轮）**："
        u"F-023 卡多模态读（AIGC 标签位=卡面左上同位族·R511 零修红）→census-card-v4-vertical.mp4 派生（13.000s·ffprobe 与 v15 逐参数一致）"
        u"→对位表 cards-v1-matched 12/12（visual-ratio 1.00·b9=第九对人物链卡面双端互证拍）→R720 律前置几何修七卡"
        u"（b0/b4/b5/b6/b7/b8/b9 @60px 5-9 行块顶 573-745 叠压→per-card size 52/56/46×5 verbatim 零字符·"
        u"b9 82 字块 size 单参不可修→**卡面注记剥离迁 REQS 溯源层**〔col2 内嵌生产溯源注记=R735 起链笔误·fleet lc001-lc016 卡面零〔〕先例·"
        u"beats/S1 材料零接触·R512 脱敏决策维持〕）→R-E shipinhao 渲染 lc-017-v1-shipinhao-60s.mp4（58.502s=音轨分毫一致 1.498s 余量·"
        u"hits=[0,11]·角标=BigStream|拆条 017·源城市图鉴 004）→S2 三门全绿（ai_feel 0F0W CV 0.244/0.287+层 1.8 六面 PASS+"
        u"spec 双 PASS 1.5s 余量）+全卡几何审计 12 卡 problems=NONE+帧验三律全过（拍头 12/12+段中尾 6/6 零录穿+回环 crossings={}+"
        u"AIGC 双标识 fs-t09 全分辨率实证·**段尾 sys.beat 戳缺席=cue 锁定窗正常行为新判例**〔S4.5(3) one-per-cue·cue10 终 48.543s<"
        u"采样 48.82s·拍头 fs-h09 实证在位〕·tile 缩略疑点全分辨率定谳「誊」≠「誉」=R189 手段问题律）；"
        u"台账六件（renders 声明行收口+在链行/station-reviews R737/lc017 README 渲染腿段+门禁块/queue burn/export 刷）——"
        u"收官腿（E8+ASR+E4+M4→F-072 登记→冗余池第十四件落位→E18 出池+补池义务随轮领）=R738 首位；"
        u"lane=E18〔active·渲染腿毕〕+E16〔standby〕维持 ≥2。\n")
t = t.rstrip("\n") + "\n" + burn
wr(p, t)
print("queue ok")
print("LEDGERS_DONE")
