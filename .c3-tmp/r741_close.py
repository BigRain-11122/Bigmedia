# -*- coding: utf-8 -*-
# R741 close: renders README (decl row tail + in-chain row) + station-reviews row + lc018 README
#            + queue E19 burn row + state.json (tick/ts/task/focus/log) + status-export.json
import json, io
from datetime import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
hm = now[11:16]

LOG_R741 = (
    "2026-09-30 %s R741: 生产轮·E19 LC-018 陈雅雯拆条渲染腿毕（queue §E 批活池 E19 件·冗余扩容位第十五件·R740 指针①兑现·"
    "R729/R733/R737 同型五步·实活轮·产品优先律 P-20260929-07 对位=本轮新实物=lc-018 成片在链）——"
    "①轮首快速路径五查静（正典 r694_probe.py 复跑 10:12：orders 顶 O-20260928-1910 42 件锚未动/ledger 六模式 CaseSensitive 41=锚零新 CEO 令级事件〔L189/L190=R698/R700 已收讫+L245 值守行位移非事件〕/"
    "decisions UTF8 非空行 75=锚零新行/production=open 自愈核在位 tick740/无 index.lock·树态=bm-a codex 批未闭让位维持〔README/city-humanities mtime 09-29 04:06 实读未动=#86 c+d 判据未达·两文件零接触〕+自产 tmp 族预期态）"
    "+三探针=board exit=0 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现（阻塞≠失败口径）/loop_health 2 FAIL+84 WARN 皆在案史实类（2 outage 同事件足迹已裁定+account-ahead tick740>beats737=R738/R740 收账瞬态族·tick741 收账自平）；"
    "②渲染腿五步毕：素材探针先行=F-025 卡多模态九行全读（AIGC 标签位=卡面左上=同位族·R511 避让法前置执行零修红·来源行「基于硅基城市居民户籍卡档案（展示锚 C-00015）」在位核）"
    "→自产源件 census-card-v6-vertical.mp4（F-025 PNG〔188,550B 核〕派生·scale 660+pad y=160+zoompan ≤1.04·13.000s·ffprobe 与 v15 参照逐参数一致 1080×1920@30）"
    "→对位表 cards-v1-matched.json 12/12 逐拍 visual（源卡即证据·钩子/信条行 verbatim 直引+锚 C-00015 字段展开同源多用注记·b9=第十对人物链卡面双端互证拍·visual-ratio 1.00）"
    "→**b9 卡面注记剥离迁移**（col2 内嵌生产溯源注记〔C-00014 关系字段+职业行双端互记·C-00015/C-00014 年轮 2026-09-30 相遇句双端在册·TTS cards 链截断两 line 项〕=R739 起链笔误·fleet lc001-lc017 卡面零〔〕先例→REQS 溯源层〔verbatim 保真·'/' 拼点还原零损〕·beats/S1 材料零接触=R737 b9 同型第二案）"
    "→**R720 律前置几何修六卡**（b0/b4/b5/b6/b7/b8 @60px 5 行块顶 745 叠压=R711 五行块同型→per-card size 56/54/46/46/52/50 verbatim 零字符·b0 顶 798 净 31/b4 顶 802 净 35/b5+b6 顶 787 净 20=修法地板/b7 顶 807 净 40/b8 顶 812 净 45）"
    "→全卡几何审计 12 卡 problems=NONE（R721 E8 帧验执法面常驻第六件）"
    "→R-E shipinhao 渲染 lc-018-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·58.411s ffprobe=音轨分毫一致 1.589s 余量〔plan 内部预估 59.200s=tail 余量项·实测为准 LC-008 判例〕·hits=[0,11]·角标=BigStream|拆条 018·源城市图鉴 006+§4.5 三开关·plan.json 入 git）；"
    "③S2 三门循环独立执法全绿=ai_feel 0F0W（gaps 11 处 0.239-0.558s·pacing CV 0.251·prosody 9 档 12 拍·copy CV 0.209）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过）+spec 微信视频号双 PASS（9:16+58.41s∈30-60s 窗 1.6s 余量）；"
    "④帧验三律全过=拍头 12/12 语义全中（H1 拍名 12/12 逐拍对位+sys.beat 01→12 连续 t 单调+角标 12 帧全在+AIGC 帧头标识全在）+段中尾 6/6 稳定零录穿（law2=b3/b4/b5 动态三最长 6.45/6.80/6.08s·段尾字幕缺席=SRT 逐 cue 显隐律 R697 判例）+回环 crossings={}（max 6.80s<源 13s 诚实计算）"
    "+AIGC 双标识分层可读（fs-pair-col3-h02-h06-h10 全分辨率实证）+b9 剥离后面容净收束（fs-pair-h04-h09-h11 全分辨率=零〔〕残注+来源行「展示锚 C-00015」净空距完整=R720 前置修持位）"
    "+tile 缩略疑点全分辨率定谳（第 3 列 AIGC 括号「缺失」=缩略伪读·全分辨率三帧括号全在=R189 手段问题律）；"
    "⑤操作红一笔如实入账=build 脚本首跑漏挂 c['visual'] 行（R737 原型有·适配笔误）→渲染器拒稿「bgvideo required for legacy」当场定谳即补挂重跑（幂等零内容损失）；"
    "⑥台账六件=renders README〔声明行收口+在链行〕+station-reviews R741 S2 行+lc018 README 生产记录渲染腿段+门禁块+queue §E E19 burn 行+export 刷（live 三行=R741 实况）；"
    "例行件：日报 09-30 在案不重跑（R713 补产）/W40 周审在案（R576）/月度注记在案（R-20260928-03）/global-benchmarks day6 ≤7 跳过（下期 10-01=#80 并窗勿提前触碰）/"
    "#70 OSS 窗 2=10-02 21:40 前随轮领（窗面义务足 R644 切片 1）/#86 c+d 让位判据未达（codex mtime 04:06 未动）/T1 催办=已裁项停用口径/HQ-FEEDBACK 不写（无集团层新 open 问题·双锚静零膨胀）"
    "/tokens:local=0（渲染+S2 三门=纯脚本机检+帧验=会话多模态零本地模型调用·P-54⑤ 计量律如实记）"
    "——下轮=R742 可领序：①LC-018 收官腿（E8 终审+ASR 终轨+E4 参考仪+M4→F-073 登记→冗余池第十五件落位→E19 出池+补池义务随轮领〔R730/R734/R738 同型〕）"
    "②#70 OSS 窗 2 切片（≤10-02 21:40）③#86 c+d 让位判据④global-benchmarks 10-01 刷新（#80 并窗）。收账显式列文件 commit+push"
) % hm

TASK_R741 = LOG_R741[len("2026-09-30 %s " % hm):][:60]

FOCUS_R742 = (
    "R742: ①LC-018 收官腿（E8 终审+ASR 终轨+E4 参考仪+M4→F-073 登记→冗余池第十五件落位→E19 出池+补池义务随轮领〔R730/R734/R738 同型〕）"
    "②#70 OSS 窗 2 切片（≤10-02 21:40·切片 1 R644 在案）③#86 c+d 让位判据（bm-a codex 批闭 commit 落地）④global-benchmarks 10-01 刷新（#80 并窗）"
    "——五查锚=orders O-20260928-1910 42·ledger 41（L189/L190/L245 注）·decisions 75"
)

# ---- 1. renders README: declaration row tail + in-chain row ----
rp = ROOT + r"\output\renders\README.md"
r = io.open(rp, encoding="utf-8").read()
old_tail = u"全卡几何审计 R720 律前置=R740+ 随轮领）"
new_tail = (u"全卡几何审计 R720 律前置=R741 毕〔六卡前置修+b9 注记剥离+S2 三门全绿+帧验三律全过·详见下表在链行〕·"
            u"收官腿〔E8+ASR+E4+M4→F-073→冗余池第十五件→E19 出池+补池〕=R742 随轮领）")
assert old_tail in r, 'decl row tail not found'
r = r.replace(old_tail, new_tail, 1)
INCHAIN = (
u"| lc-018-v1-shipinhao-60s.mp4 | **在链件·渲染腿毕（queue §E 批活池 E19 件·冗余扩容位第十五件·源卡=CENSUS-v6 F-025 陈雅雯·R739 起链→R740 定稿音轨→R741 渲染腿毕）** | "
u"**R-E shipinhao 12 段 11 柔转场 0 硬切**·9:16 1080×1920·**58.411s ffprobe 实测=音轨分毫一致·1.589s 余量**〔plan 内部预估 59.200s=tail 余量项·实测为准·LC-008 判例〕·hits=[0,11]·**S5.5 角标常驻位**=BigStream\\|拆条 018·源城市图鉴 006+§4.5 三开关[glow/scanlines/sys.beat=NN t=MM:SS]·plan.json 入 git·"
u"**视觉动态位=源卡即证据 12/12**（census-card-v6-vertical 源卡画面×12·visual-ratio 1.00·源件=F-025 PNG〔188,550B 核〕派生 scale 660+pad y=160+zoompan ≤1.04·13.000s=LC-001~017 R511 法·ffprobe 与 v15 参照逐参数一致·素材探针先行=卡面九行全读+AIGC 标签位=卡面左上=同位族·R511 避让法前置执行零修红）——"
u"**b0/b4/b5/b6/b7/b8 前置几何修（R720 律预执行·build 级审计驱动·R711 五行块叠压前科防）**：六卡 @60px 5 行块顶 745 叠压→per-card size 56/54/46/46/52/50 verbatim 零字符（b0 4 行顶 798 净 31/b4 4 行顶 802 净 35/b5+b6 5 行顶 787 净 20=修法地板/b7 4 行顶 807 净 40/b8 4 行顶 812 净 45）·**全卡几何审计 12 卡 problems=NONE**（R721 E8 帧验执法面常驻第六件）——"
u"**b9 卡面注记剥离迁移**（col2 内嵌生产溯源注记〔C-00014 关系字段+职业行双端互记·C-00015/C-00014 年轮 2026-09-30 相遇句双端在册·TTS cards 链截断两 line 项〕=R739 起链笔误·fleet lc001-lc017 卡面零〔〕先例→渲染腿迁回 REQS 溯源层〔verbatim 保真存 cards-v1-matched.json visual.req·'/' 拼点还原零损〕·卡面=锚字段 verbatim 零动·beats/S1 材料零接触=R737 b9 同型第二案）——"
u"**S2 三门 R741 循环独立执法全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.239-0.558s·pacing CV 0.251·prosody 9 档 12 拍·copy CV 0.209）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过）+spec 微信视频号双 PASS（9:16+58.41s ∈30-60s 窗 1.6s 余量）——"
u"**帧验三律全过**：拍头 12/12 语义全中（H1 拍名 12/12 逐拍对位+sys.beat 01→12 连续无跳号 t 单调递增+角标 12 帧全在+AIGC 帧头标识全在）+段中尾 6/6 稳定零录穿（law2=动态三最长拍 b3/b4/b5〔6.45/6.80/6.08s〕·段尾帧字幕缺席=SRT 逐 cue 显隐律正常行为 R697 判例·词中断行「从此/问题」=自然折行非缺陷）+回环 crossings={}（max 拍 6.80s<源 13s·诚实计算）"
u"+AIGC 双标识分层可读（帧头+卡面左上标签垂直错开零叠压·fs-pair-col3-h02-h06-h10 全分辨率实证）+b9 剥离后面容净收束（fs-pair-h04-h09-h11 全分辨率=零〔〕残注+来源行「基于硅基城市居民户籍卡档案（展示锚 C-00015）」净空距完整可读=R720 前置修持位）+tile 缩略疑点全分辨率定谳（第 3 列 AIGC 括号「缺失」=缩略伪读·全分辨率三帧括号全在=R189 手段问题律） | "
u"plan.json 入 git·mp4 gitignored·**R742 收官腿待办**（E8 终审+ASR 终轨+E4 参考仪+M4→F-073 登记→冗余池第十五件落位→E19 出池+补池义务随轮领·发布锁=M5 账号物理件未开·未上线=未测量） | \n"
)
r = r.rstrip('\n') + '\n\n' + INCHAIN
io.open(rp, "w", encoding="utf-8", newline="\n").write(r)

# ---- 2. station-reviews row ----
sp2 = ROOT + r"\docs\reviews\station-reviews.md"
sr = io.open(sp2, encoding="utf-8").read().rstrip('\n')
SR_ROW = (
u"| 2026-09-30 | **S2 三门循环独立执法+帧验三律+全卡几何审计前置六卡修+b9 注记剥离（lc-018-v1-shipinhao=queue §E 批活池 E19 渲染腿·冗余扩容位第十五件·源卡 CENSUS-v6 F-025 陈雅雯·R741 渲染腿）** | "
u"lc-018-v1-shipinhao-60s.mp4（R-E shipinhao 12 段·11 柔转 0 硬切·58.411s=音轨分毫一致 1.589s 余量）+cards-v1-matched（六卡前置修+b9 注记剥离注记）+fs 采样件族+s2-results.md | "
u"循环独立执法（ai_feel+层 1.8+spec 微信视频号·引擎脚本零 LLM）+帧验三律（会话多模态 tile+全分辨率定谳） | "
u"收官腿待 R742（E8 终审+ASR 终轨+E4+M4→F-073 登记→冗余池第十五件→E19 出池+补池义务随轮领） | "
u"ai_feel 0F0W（gaps 11 处 0.239-0.558s·pacing CV 0.251·prosody 9 档 12 拍·copy CV 0.209）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00 12/12+transition-share 1.00 无连排+timeline 代数过）+spec 微信视频号双 PASS（9:16+58.41s∈30-60s 1.6s 余量）·几何前置修六卡（b0/b4/b5/b6/b7/b8 @60px 5 行块顶 745→per-card size 56/54/46/46/52/50 verbatim 零字符·修后 12 卡 problems=NONE）·b9 注记剥离=R737 b9 同型第二案（fleet 卡面零〔〕律·'/' 拼点还原零损·beats/S1 材料零接触）·帧验=拍头 12/12 语义全中+段中尾 6/6 零录穿+回环 crossings={}（max 6.80s<源 13s）+AIGC 双标识分层可读·tile 缩略疑点（第 3 列 AIGC 括号）全分辨率定谳=括号全在=R189 手段问题律 | \n"
)
io.open(sp2, "w", encoding="utf-8", newline="\n").write(sr + '\n' + SR_ROW)

# ---- 3. lc018 README: production record append + gate block update ----
lp = ROOT + r"\data\sources\lc018\README.md"
lr = io.open(lp, encoding="utf-8").read()
PROD = (
u"\n- [2026-09-30 10:3x R741 渲染腿毕（R740 指针①兑现·R729/R733/R737 同型五步+全卡几何审计 R720 律前置）] "
u"素材探针先行=F-025 卡多模态九行全读（AIGC 标签位=卡面左上=同位族·R511 避让法前置执行零修红·来源行「基于硅基城市居民户籍卡档案（展示锚 C-00015）」在位核）"
u"→自产源件 data/sources/footage/census-card-v6-vertical.mp4（F-025 PNG〔188,550B 核〕派生·scale 660+pad y=160+zoompan ≤1.04·13.000s·ffprobe 与 v15 参照逐参数一致 1080×1920@30）"
u"→对位表 cards-v1-matched.json 12/12 逐拍 visual（源卡即证据·钩子/信条行 verbatim 直引+锚 C-00015 字段展开同源多用注记·b9=第十对人物链卡面双端互证拍·visual-ratio 1.00）"
u"→**b9 卡面注记剥离迁移**（col2 内嵌生产溯源注记〔C-00014 关系字段+职业行双端互记·C-00015/C-00014 年轮 2026-09-30 相遇句双端在册·TTS cards 链截断两 line 项〕=R739 起链笔误·fleet lc001-lc017 卡面零〔〕先例→REQS 溯源层〔verbatim 保真存 cards-v1-matched.json visual.req·'/' 拼点还原零损〕·卡面=锚字段 verbatim 零动·beats/S1 材料零接触=R737 b9 同型第二案）"
u"→**R720 律前置几何修（build 级审计驱动）**：b0/b4/b5/b6/b7/b8 六卡 @60px 5 行块顶 745 叠压（R711 五行块同型）→per-card size 56/54/46/46/52/50 verbatim 零字符（b0 顶 798 净 31/b4 顶 802 净 35/b5+b6 顶 787 净 20=修法地板/b7 顶 807 净 40/b8 顶 812 净 45）→全卡几何审计 12 卡 problems=NONE（R721 E8 帧验执法面常驻第六件）"
u"→R-E shipinhao 渲染 lc-018-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·58.411s ffprobe 实测=音轨分毫一致·1.589s 余量·hits=[0,11]·S5.5 角标=BigStream|拆条 018·源城市图鉴 006+§4.5 三开关·plan.json 入 git）"
u"→S2 三门循环独立执法全绿（ai_feel 0F0W gaps 11 处 0.239-0.558s·pacing CV 0.251·prosody 9 档 12 拍·copy CV 0.209+层 1.8 六面 PASS+spec 微信视频号双 PASS 9:16+58.41s∈30-60s 1.6s 余量）"
u"→帧验三律全过（拍头 12/12 语义全中+段中尾 6/6 零录穿〔law2=b3/b4/b5 动态三最长 6.45/6.80/6.08s〕+回环 crossings={} max 6.80s<源 13s+AIGC 双标识分层可读+b9 剥离后面容净收束全分辨率实证+tile 缩略疑点〔第 3 列 AIGC 括号〕全分辨率定谳=括号全在 R189 手段问题律）"
u"——操作红一笔如实入账：build 脚本首跑漏挂 c['visual'] 行（R737 原型有·适配笔误）→渲染器拒稿「bgvideo required for legacy」当场定谳即补挂重跑（幂等零内容损失）。\n"
)
lr = lr.replace(u"\n## 门禁块", PROD + u"\n## 门禁块", 1)
OLD_GATE = u"·渲染腿=待领（R729/R733/R737 同型五步：F-025 PNG 派生 census-card-v6-vertical→对位表 12/12→R-E shipinhao〔拆条 018·源城市图鉴 006〕→S2 三门+帧验三律+全卡几何审计 R720 律前置）·收官腿=待领（E8+ASR+E4+M4→F-073 登记→冗余池第十五件落位→E19 出池+补池义务随轮领）"
NEW_GATE = u"·渲染腿=**毕（R741）**（lc-018-v1-shipinhao-60s.mp4 58.411s 在链·S2 三门全绿+全卡几何审计 problems=NONE+帧验三律全过）·收官腿=待领（E8+ASR+E4+M4→F-073 登记→冗余池第十五件落位→E19 出池+补池义务随轮领）"
assert OLD_GATE in lr, 'gate block pattern not found'
lr = lr.replace(OLD_GATE, NEW_GATE, 1)
io.open(lp, "w", encoding="utf-8", newline="\n").write(lr)

# ---- 4. queue E19 burn row (after the R740 row) ----
qp = ROOT + r"\docs\self-improvement-queue.md"
q = io.open(qp, encoding="utf-8").read()
R740_ROW_TAIL = u"→收官腿（E8+ASR+E4+M4→F-073→冗余池第十五件落位→E19 出池+补池义务）随轮领。"
assert R740_ROW_TAIL in q, 'queue R740 row tail not found'
QUEUE_ROW = (
u"\n- 2026-09-30: **E19 LC-018 陈雅雯拆条渲染腿毕（R741·R740 指针①兑现·R729/R733/R737 同型五步·实活轮·产品优先律对位=本轮新实物=lc-018 成片在链）**："
u"F-025 卡多模态读（AIGC 标签位=卡面左上同位族·R511 零修红）→census-card-v6-vertical.mp4 派生（13.000s·ffprobe 与 v15 逐参数一致）→对位表 cards-v1-matched 12/12（visual-ratio 1.00·b9=第十对人物链卡面双端互证拍）"
u"→R720 律前置几何修六卡（b0/b4/b5/b6/b7/b8 @60px 5 行块顶 745 叠压→per-card size 56/54/46/46/52/50 verbatim 零字符·修后 12 卡 problems=NONE）+**b9 注记剥离迁 REQS 溯源层**（col2 内嵌生产溯源注记=R739 起链笔误·fleet lc001-lc017 卡面零〔〕先例·'/' 拼点还原零损·beats/S1 材料零接触=R737 b9 同型第二案）"
u"→R-E shipinhao 渲染 lc-018-v1-shipinhao-60s.mp4（58.411s=音轨分毫一致 1.589s 余量·hits=[0,11]·角标=BigStream|拆条 018·源城市图鉴 006）"
u"→S2 三门全绿（ai_feel 0F0W CV 0.251/0.209+层 1.8 六面 PASS+spec 双 PASS 1.6s 余量）+帧验三律全过（拍头 12/12+段中尾 6/6 零录穿+回环 crossings={}+AIGC 双标识全分辨率实证·tile 缩略疑点〔第 3 列 AIGC 括号〕全分辨率定谳=括号全在 R189 手段问题律）；"
u"操作红一笔=build 首跑漏挂 c['visual'] 行（R737 原型适配笔误）→渲染器拒稿即补挂重跑（幂等零损）；"
u"台账六件（renders 声明行收口+在链行/station-reviews R741/lc018 README 渲染腿段+门禁块/queue burn/export 刷）——收官腿（E8+ASR+E4+M4→F-073 登记→冗余池第十五件落位→E19 出池+补池义务随轮领）=R742 首位；lane=E19〔active·渲染腿毕〕+E16 周浩宇〔standby〕维持 ≥2。"
)
q = q.replace(R740_ROW_TAIL, R740_ROW_TAIL + QUEUE_ROW, 1)
io.open(qp, "w", encoding="utf-8", newline="\n").write(q)

# ---- 5. state.json ----
sp = ROOT + r"\src\os\state.json"
st = json.load(io.open(sp, encoding="utf-8"))
log_n_before = len(st["log"])
st["tick"] = 741
st["ts"] = now
st["task"] = TASK_R741
st["focus"] = FOCUS_R742
st["log"].append(LOG_R741)
io.open(sp, "w", encoding="utf-8", newline="\n").write(
    json.dumps(st, ensure_ascii=False, indent=1))

# ---- 6. status-export.json ----
ep = ROOT + r"\docs\status-export.json"
ex = json.load(io.open(ep, encoding="utf-8"))
ex["export_ts"] = now
ex["outs"][0] = [
    u"OS 循环",
    u"tick 741，R741 生产轮·E19 LC-018 陈雅雯拆条渲染腿毕（产品优先律对位=lc-018-v1-shipinhao-60s.mp4 成片在链）——"
    u"六卡前置几何修（b0/b4/b5/b6/b7/b8 per-card size verbatim 零字符·problems=NONE）+b9 注记剥离迁溯源层（R737 同型第二案）+S2 三门全绿"
    u"（ai_feel 0F0W+层 1.8 六面 PASS+spec 微信视频号双 PASS 58.41s 1.6s 余量）+帧验三律全过（拍头 12/12+段中尾 6/6+回环 {}）"
    u"·收官腿 F-073=R742 首位·lane=E19〔active〕+E16 周浩宇〔standby〕≥2 达标·发布锁=M5 账号物理件不变"
]
ex["live"] = [
    [u"当前活：LC-018 渲染腿毕（R741）——lc-018-v1-shipinhao-60s.mp4 58.411s 在链·S2 三门全绿+帧验三律全过·收官腿 F-073=R742 首位·lane=E19〔active〕+E16 周浩宇〔standby〕≥2 达标"],
    [u"最近实物：output/renders/lc-018-v1-shipinhao-60s.mp4 渲染腿毕 58.411s（2026-09-30 " + now[11:16] + u"）·最近成品=F-072 lc-017-v1-shipinhao-60s.mp4（09:21 登记）"],
    [u"下个里程碑：LC-018 收官腿 F-073 登记（≤48h 窗 2026-10-02 前）·#70 OSS 窗 2 切片（≤10-02 21:40）·global-benchmarks 7 日刷（10-01 #80 并窗）"],
]
ex["results"].append(["741", LOG_R741])
io.open(ep, "w", encoding="utf-8", newline="\n").write(
    json.dumps(ex, ensure_ascii=False, indent=1))

# ---- verify ----
st2 = json.load(io.open(sp, encoding="utf-8"))
ex2 = json.load(io.open(ep, encoding="utf-8"))
r2 = io.open(rp, encoding="utf-8").read()
sr2 = io.open(sp2, encoding="utf-8").read()
lr2 = io.open(lp, encoding="utf-8").read()
q2 = io.open(qp, encoding="utf-8").read()
rep = []
rep.append("state tick=%s ts=%s logN=%d (before %d, expect %d) task[:20]=%r" % (
    st2["tick"], st2["ts"], len(st2["log"]), log_n_before, log_n_before + 1, st2["task"][:20]))
rep.append("export_ts=%s results_tail=%s outs0_head=%r live_rows=%d" % (
    ex2["export_ts"], ex2["results"][-1][0], ex2["outs"][0][1][:18], len(ex2["live"])))
rep.append("renders: decl_new_tail=%s inchain=%s" % (new_tail[:20] in r2, "| lc-018-v1-shipinhao-60s.mp4" in r2))
rep.append("station: R741_row=%s" % ("R741 渲染腿" in sr2))
rep.append("lc018 readme: prod_row=%s gate_new=%s" % ("R741 渲染腿毕" in lr2, NEW_GATE[:10] in lr2))
rep.append("queue: E19_R741_row=%s" % ("E19 LC-018 陈雅雯拆条渲染腿毕（R741" in q2))
io.open(ROOT + r"\.c3-tmp\r741_close_verify.txt", "w", encoding="utf-8").write("\n".join(rep))
print("CLOSE_DONE")
print("\n".join(rep))
