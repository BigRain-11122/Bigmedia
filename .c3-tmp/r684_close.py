# -*- coding: utf-8 -*-
# R684 close: ledger updates (renders README / station-reviews / lc003 README / backlog #79 / queue E1)
#             + status-export refresh + state.json accounting + probe re-run
import json, io, os, time, subprocess, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")
NOW = time.strftime("%Y-%m-%d %H:%M:%S")
report = []

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding="utf-8").read()

def wr(p, s):
    io.open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="\n").write(s)

# ---------- 1. renders README ----------
rrp = "output/renders/README.md"
rr = rd(rrp)
OLD_TAIL = (u"；渲染腿=随轮领（拆条形态源卡即证据=LC-001/002 同型：F-032 PNG 派生 census-card-v13-vertical"
            u"+对位表 12/12+R-E shipinhao 渲染[--series-id=拆条 003·源城市图鉴 013]+S2 三门+帧验三律）"
            u"→收官=E8+ASR+E4+M4→F 登记→D25 落位（排期表缺口 1→0 档）。")
NEW_TAIL = (u"；**R684 渲染腿毕**：批中间件增 build_leg_a.py[自产源件+对位表构建件]+render_call.py[UTF-8 argv 渲染 wrapper]"
            u"+s2_gates.py[S2 三门执行件]+fs_extract.py[帧验采样件·fs-h00~11+fs-m/t 00/06/03+双 tile+双 labelzone 裁切]"
            u"+probe-v13-mid.png[源件探针帧]+s2-results.md[三门读数档]——自产源件=`data/sources/footage/census-card-v13-vertical.mp4`"
            u"（R684·F-032 成品卡 PNG 派生·scale 660+pad y=160+zoompan ≤1.04 微动 13s·ffprobe 与 v8 参照逐参数一致 1080×1920@30"
            u"·mp4 gitignored·自产源件仅入声明=R21/R512 先例）+对位表 `cards-v1-matched.json` 落正位（12/12 逐拍 visual·源卡即证据"
            u"·visual-ratio 1.00）+R-E shipinhao 渲染 lc-003-v1-shipinhao-60s.mp4（S5.5 角标=BigStream|拆条 003·源城市图鉴 013"
            u"+§4.5 三开关）+S2 三门全绿+帧验三律全过（station-reviews R684 S2 行）"
            u"→收官腿=E8+ASR+E4+M4→F 登记→D25 落位（排期表缺口 1→0 档）随轮领。")
assert OLD_TAIL in rr, "renders L90 tail not found"
rr = rr.replace(OLD_TAIL, NEW_TAIL)

ROW = (u"| lc-003-v1-shipinhao-60s.mp4 | **在链（queue §E1 批活池 E1 件·#79 尾注 D25 缺口续补·源卡=CENSUS-v13 F-032 何雨欣·"
       u"R683 起链+R684 渲染腿·E8/M4/F 登记=收官腿随轮领）** | **R-E shipinhao 12 段 11 柔转场 0 硬切**·9:16 1080×1920·"
       u"**58.69s ffprobe 实测·1.3s 余量**·hits=[0,11]·**S5.5 角标常驻位**=BigStream\\|拆条 003·源城市图鉴 013"
       u"+§4.5 三开关[glow/scanlines/sys.beat=NN t=MM:SS]·plan.series+s45_dials 入 plan.json·"
       u"**拆条形态对位=源卡即证据 12/12**：census-card-v13-vertical 源卡画面×12[逐拍 req=钩子/档案/信条行 verbatim 直引"
       u"+锚 C-00022 字段展开同源多用注记]·visual-ratio 1.00（源件=F-032 PNG 派生 scale 660+pad y=160+zoompan ≤1.04·13s"
       u"=LC-001/002 R511 法·素材探针先行=九行全读+AIGC 标签位卡面左上定谳=与 F-027 同位族）——"
       u"**S2 三门 R684 循环独立执法全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.583s·pacing CV 0.185·prosody 9 档 12 拍"
       u"·copy CV 0.201）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排"
       u"+timeline 代数过）+spec 微信视频号双 PASS（9:16+58.69s ∈30-60s 窗 1.3s 余量）——**帧验三律全过**：拍头 12/12 语义全中"
       u"（源卡 9 行档案全读+拍标题逐拍对位+sys.beat 01→12 连续）+段中尾 6/6 稳定零录穿（全分辨率复核 fs-m06/fs-t06 定谳："
       u"状态行段中清晰 sys.beat=07 t=00:29=段起始静态戳 §4.5 设计口径·tile 缩略读数 beat=0 系误读·段尾帧状态行出段淡出带"
       u"=11 柔转场设计内非缺陷）+回环 crossings={}（max 拍 6.22s<源 13s·诚实计算）+AIGC 双标识分层可读（帧头标识+卡面左上标签"
       u"垂直错开无叠压·R511 避让法前置执行零修红·底部区裁切零碰撞） | plan.json 入 git·E8 终审+ASR 终轨+E4 随行→M4→F 登记"
       u"→D25 落位=收官腿随轮领 |")
if not rr.endswith("\n"):
    rr += "\n"
rr += ROW + "\n"
wr(rrp, rr)
report.append("renders README: L90 tail replaced + table row appended")

# ---------- 2. station-reviews S2 row ----------
srp = "docs/reviews/station-reviews.md"
sr = rd(srp)
S2ROW = (u"| 2026-09-29 | **S2 三门循环独立执法+帧验三律（lc-003-v1-shipinhao=queue §E1 批活池 E1 件·#79 尾注 D25 缺口续补·"
         u"源卡 CENSUS-v13 F-032 何雨欣·R684 渲染腿）** | lc-003-v1-shipinhao-60s.mp4（R-E shipinhao 12 段·11 柔转场 0 硬切"
         u"·58.69s） | 循环独立执法（ai_feel+层 1.8+spec 微信视频号·纯脚本机检零 LLM）+帧验三律（会话内建多模态） | "
         u"—（机检档·E8 终审待收官腿） | 对位表=cards-v1-matched（**拆条形态源卡即证据 12/12**：自产源件 "
         u"census-card-v13-vertical[=F-032 成品卡 PNG 派生·scale 660+pad y=160+zoompan ≤1.04·13s·ffprobe 与 v8 参照逐参数一致]"
         u"×12 逐拍 req[hook/b1/b10/b11=卡面行 verbatim 直引·b2-b9=锚 C-00022 字段展开同源多用注记]·visual-ratio **1.00**"
         u"·素材探针先行=F-032 九行全读+AIGC 标签位卡面左上定谳[与 F-027 同位族]）；S2 三门=ai_feel 0 FAIL 0 WARN"
         u"（gaps 11 处 0.220-0.583s·pacing CV 0.185·prosody 9 档 12 拍·copy CV 0.201）+层 1.8 六面 PASS（beat-align 11/11"
         u"+camera 12 段全动+visual-ratio 1.00+transition-share 1.00+variety 无连排+timeline 代数过）+spec 微信视频号双 PASS"
         u"（9:16+58.69s ∈30-60s 窗 1.3s 余量） | 三门全绿+帧验三律全过：拍头 12/12 语义全中（源卡 9 行档案全读+拍标题逐拍对位"
         u"+sys.beat 01→12 连续+badge BigStream\\|拆条 003·源城市图鉴 013 完整）+段中尾 6/6 稳定零录穿（全分辨率复核 fs-m06/fs-t06 "
         u"定谳：状态行段中清晰可见 sys.beat=07 t=00:29·tile 缩略读数 beat=0 系缩略图误读·段尾帧状态行出段淡出带=11 柔转场设计口径"
         u"非缺陷）+回环 crossings={}（max 拍 6.22s<源 13s·诚实计算）+AIGC 双标识分层可读（帧头标识+卡面左上标签垂直错开无叠压"
         u"·R511 修红先例前置执行零修红） | `.lc003-tmp/`s2-results.md+fs-tile-heads.png+fs-tile-midtail.png+fs-h00-labelzone.png"
         u"+fs-h11-bottomzone.png+fs-m06.png+fs-t06.png+probe-v13-mid.png+cards-v1-matched.json+plan.json；"
         u"E8 终审+ASR 终轨+E4 随行→M4→F 登记→D25 落位=收官腿随轮领 |\n")
if not sr.endswith("\n"):
    sr += "\n"
sr += S2ROW
wr(srp, sr)
report.append("station-reviews: S2 row appended")

# ---------- 3. lc003 README render section ----------
lrp = "data/sources/lc003/README.md"
lr = rd(lrp)
LRR684 = (u"- 2026-09-29 R684 渲染腿毕：①素材探针先行=F-032 卡多模态九行全读（AIGC 标签位=卡面左上·与 F-026 底部不同位"
          u"=与 F-027 同位族）→②自产源件 `data/sources/footage/census-card-v13-vertical.mp4`（F-032 PNG 派生·scale 660"
          u"+pad y=160+zoompan ≤1.04 微动 13s·ffprobe 与 v8 参照逐参数一致 1080×1920@30·R511 法+标签避让先例"
          u"**前置执行零修红**）→③对位表 `cards-v1-matched.json` **12/12 逐拍 visual**（源卡×12·逐拍 req=钩子/档案/信条行 "
          u"verbatim 直引+锚 C-00022 字段展开同源多用注记·visual-ratio 1.00）→④R-E shipinhao 渲染 "
          u"`output/renders/lc-003-v1-shipinhao-60s.mp4`（12 段 11 柔 0 硬切·58.69s ffprobe·1.3s 余量·hits=[0,11]·"
          u"S5.5 角标=BigStream\\|拆条 003·源城市图鉴 013+§4.5 三开关）→⑤S2 三门循环独立执法**全绿**（ai_feel 0 FAIL 0 WARN "
          u"gaps 11 处 0.220-0.583s·CV 0.185/0.201+层 1.8 六面 PASS·visual-ratio 1.00+spec 微信视频号双 PASS "
          u"9:16+58.69s∈30-60s）→⑥帧验三律**全过**（拍头 12/12 语义全中+段中尾 6/6 稳定零录穿〔全分辨率复核 fs-m06/fs-t06 定谳"
          u"=状态行段中清晰·段尾出段淡出带=柔转场设计口径〕+回环 crossings={}·max 拍 6.22s<源 13s+AIGC 双标识分层可读垂直错开"
          u"无叠压）——台账=renders 在链行+station-reviews S2 行+本 README；批中间件 `.lc003-tmp/` 增 build_leg_a.py"
          u"/render_call.py/s2_gates.py/fs_extract.py+s2-results.md+帧验采样件。\n")
if not lr.endswith("\n"):
    lr += "\n"
lr += LRR684
wr(lrp, lr)
report.append("lc003 README: R684 render bullet appended")

# ---------- 4. backlog #79 R684 note ----------
bkp = "src/os/backlog.md"
bk = rd(bkp)
MARK = u"（何雨欣/陆海峰 R677 顺位）]**"
assert MARK in bk, "backlog R681 note marker not found"
BK684 = (u"\n\n   **[R684 渲染腿毕 2026-09-29（claim 沿用 R683·queue §E1 E1 件）：①素材探针先行=F-032 卡九行全读"
         u"（AIGC 标签位=卡面左上·与 F-027 同位族）→②自产源件 census-card-v13-vertical.mp4（F-032 PNG 派生·scale 660"
         u"+pad y=160+zoompan ≤1.04·13s·ffprobe 与 v8 参照逐参数一致·R511 法零修红）→③对位表 cards-v1-matched.json 12/12 "
         u"逐拍 visual（源卡×12·钩子/档案/信条行 verbatim+锚 C-00022 字段展开同源多用注记·visual-ratio 1.00）"
         u"→④R-E shipinhao 渲染 lc-003-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·58.69s ffprobe 1.3s 余量·hits=[0,11]·"
         u"S5.5 角标=拆条 003·源城市图鉴 013+§4.5 三开关）→⑤S2 三门全绿（ai_feel 0F0W·层 1.8 六面 PASS·spec 微信视频号"
         u"双 PASS）→⑥帧验三律全过（拍头 12/12+段中尾 6/6 零录穿·全分辨率复核定谳+回环 crossings={}·max 拍 6.22s<源 13s"
         u"+AIGC 双标识分层）；台账=renders 在链行+station-reviews S2 行+lc003 README 生产记录；"
         u"收官腿=E8 终审+ASR 终轨+E4+M4→F 登记→D25 落位（缺口 1→0 档=视频号缺口清零）随轮领。]**")
bk = bk.replace(MARK, MARK + BK684, 1)
wr(bkp, bk)
report.append("backlog: R684 note inserted after R681 note")

# ---------- 5. queue E1 progress note ----------
qp = "docs/self-improvement-queue.md"
qtxt = rd(qp)
QMARK = u"（C-20260929-02 B 款 lane 口径）。"
assert QMARK in qtxt, "queue E2 note marker not found"
Q684 = (u"\n- 2026-09-29: **E1 批活池兑现中段（R684·LC-003 渲染腿毕=源卡探针九行全读→census-card-v13-vertical 自产源件 13s"
        u"（R511 法零修红）→对位表 12/12 visual-ratio 1.00→R-E shipinhao 58.69s（角标拆条 003·源城市图鉴 013+§4.5 三开关）"
        u"→S2 三门全绿（ai_feel 0F0W+spec 双 PASS 1.3s 余量+层 1.8 六面 PASS）→帧验三律全过（拍头 12/12+段中尾 6/6 零录穿"
        u"+回环 crossings={}+AIGC 双标识分层）**——E1 维持 active 至收官（E8+ASR+E4+M4→F 登记→D25 落位随轮领）。")
qtxt = qtxt.replace(QMARK, QMARK + Q684, 1)
wr(qp, qtxt)
report.append("queue: E1 R684 progress note appended")

# ---------- 6. status-export refresh ----------
sep = "docs/status-export.json"
se = json.load(io.open(os.path.join(ROOT, sep), encoding="utf-8"))
se["export_ts"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
OS_ROW = (u"tick 684，R684 生产轮·LC-003 渲染腿毕（queue §E1 E1 件·#79 尾注 D25 缺口续补·R680 同型五步）：源卡探针九行全读"
          u"→census-card-v13-vertical 自产源件 13s（R511 法零修红）→对位表 12/12 visual-ratio 1.00→R-E shipinhao 58.69s"
          u"（角标拆条 003·源城市图鉴 013+§4.5 三开关）→S2 三门全绿（ai_feel 0F0W+spec 微信视频号双 PASS 1.3s 余量+层 1.8 "
          u"六面 PASS）→帧验三律全过（拍头 12/12+段中尾 6/6 零录穿·全分辨率复核定谳+回环 crossings={}+AIGC 双标识分层）；"
          u"五查三锚静（orders 顶 O-1910/ledger 37/decisions 74）·bm-a codex 批未闭让位维持·三探针 board 0F/readiness "
          u"3 外部+1 在链预期红（F 登记即清）/loop 3F+48W 在案类（tick684 收账自平）·tokens:local=0·"
          u"下轮=R685 LC-003 收官腿（E8+ASR+E4→M4→F 登记→D25 落位 1→0 档=视频号缺口清零）+E3 REACT-v6 09-30 窗"
          u"+#86 c+d 让位首查")
se["outs"][0][1] = OS_ROW
se["results"].append(["684", OS_ROW])
with io.open(os.path.join(ROOT, sep), "w", encoding="utf-8", newline="\n") as f:
    json.dump(se, f, ensure_ascii=False, indent=1)
report.append("status-export: export_ts + OS row + results 684")

# ---------- 7. state.json accounting ----------
sp = "src/os/state.json"
st = json.load(io.open(os.path.join(ROOT, sp), encoding="utf-8"))
LOG684 = (u"%s R684: 生产轮·LC-003 渲染腿毕（queue §E1 E1 件·#79 尾注 D25 缺口续补·R683 claim 沿用·R680 同型五步·实活轮）——"
          u"①轮首快速路径五查静（r684_probe.py 自跑实证）：无新令（orders 42 件顶=O-20260928-1910 19:12:33 锚未动）"
          u"+无新集团转办（ledger 六模式 CaseSensitive 37=锚零新 CEO 令级事件）+无新决策行（decisions UTF8 非空行 74=锚）"
          u"+production=open 自愈核在位+无 index.lock·树态=bm-a codex 批未闭（README+2/-1/city-humanities+12/-2 worktree "
          u"未暂存·mtime 04:06 实读未动=#86 c+d 让位维持）+untracked 自产 tmp 族预期态；②渲染腿五步毕：素材探针先行="
          u"F-032 卡多模态九行全读（AIGC 标签位=卡面左上·与 F-027 同位族=R511 避让法直接适用）→自产源件 "
          u"data/sources/footage/census-card-v13-vertical.mp4（F-032 PNG 派生·scale 660+pad y=160+zoompan ≤1.04 微动 13s"
          u"·ffprobe 与 v8 参照逐参数一致 1080×1920@30·标签避让前置执行零修红）→对位表 cards-v1-matched.json 12/12 逐拍 "
          u"visual（源卡即证据·钩子/档案/信条行 verbatim 直引+锚 C-00022 字段展开同源多用注记·visual-ratio 1.00）"
          u"→R-E shipinhao 渲染 lc-003-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·hits=[0,11]·58.69s ffprobe 与音轨分毫一致"
          u"·1.3s 余量·S5.5 角标=BigStream|拆条 003·源城市图鉴 013+§4.5 三开关·plan.json 入 git）→S2 三门循环独立执法全绿："
          u"ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.583s·pacing CV 0.185·prosody 9 档 12 拍·copy CV 0.201）+层 1.8 六面 "
          u"PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+share 1.00 无连排+timeline 代数过）+spec 微信视频号"
          u"双 PASS（9:16+58.69s∈30-60s 窗 1.3s 余量）；③帧验三律全过=拍头 12/12 语义全中（源卡 9 行档案全读+拍标题逐拍对位"
          u"+sys.beat 01→12 连续+角标完整）+段中尾 6/6 稳定零录穿（全分辨率复核 fs-m06/fs-t06 定谳：状态行段中清晰 "
          u"sys.beat=07 t=00:29=段起始静态戳 §4.5 设计口径·tile 缩略读数 beat=0 系缩略图误读·段尾帧状态行出段淡出带=11 柔转场"
          u"设计内非缺陷·tile 报告「错位」三项=会话向模型布局标注笔误致·内容逐帧全对位）+回环 crossings={}（max 拍 6.22s<源 13s "
          u"诚实计算）+AIGC 双标识分层可读（帧头标识+卡面左上标签垂直错开无叠压·底部区裁切零碰撞）；④台账六件=renders 在链行"
          u"+L90 声明行渲染腿收口+station-reviews S2 行+lc003 README 生产记录+backlog #79 R684 注+queue §E1 进展注；"
          u"⑤三探针（收账步复跑）=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面+1 发现"
          u"（render-unannot lc-003=在链件诚实预期红·R173/R511/R680 同型·F 登记+成品落位标即清·收官腿范围）/loop_health "
          u"3 FAIL+48 WARN 皆在案类（2 outage=同事件足迹已裁定不重复触发+account-lag done684>tick683=本轮在飞自然态 tick684 "
          u"收账自平 R615-R683 先例连·48 WARN 与 R683 持平零新增）；⑥例行件：日报 09-29 在案不重跑（R637 断轮件补产）"
          u"/W40 周审在案（R576）/月度统计注记 R-20260928-03 在案/global-benchmarks day5 ≤7 跳过（§④ 首行 09-24·下期 10-01"
          u"=#80 并窗勿提前触碰）/T1 催办=已裁项停用口径/当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）/tokens:local=0"
          u"（渲染+S2 三门+帧验=FFmpeg+纯脚本机检+会话内建多模态·零本地模型调用·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变"
          u"（未上线=未测量）——下轮=R685 LC-003 收官腿首位（E8 终审+ASR 终轨 R169 QC recipe+E4 参考仪→M4→F 登记→D25 落位"
          u"=视频号缺口 1→0 档清零）；随轮可领=E3 REACT-v6 09-30 热点窗（P-1 试点件 2/2 终判位）+#86 c+d 让位解除判据随轮首查"
          u"+W41 周报=10-05 后首个周轮（CLOUD_LINE 首测窗）" % NOW)
st["tick"] = 684
st["log"].append(LOG684)
st["ts"] = NOW
st["task"] = LOG684.split(" ", 2)[2][:60]
st["focus"] = (u"R685: ①LC-003 收官腿=E8 终审评审单（七席）+ASR 终轨〔R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1"
              u"·满载机面 Start-Process 脱壳先例〕+E4 参考仪同轮回填→M4→F 登记→**D25 落位（release-schedule v1.4 视频号缺口 "
              u"1→0 档清零·#79 预产全档毕）**+renders 行升「成品·落位」+tmp 批闭收账随收官轮 commit〔.lc003-tmp/〕；"
              u"②E3 REACT-v6=09-30 热点窗开后随轮领（P-1 试点件 2/2 终判位）；③#86 c+d 让位解除判据=bm-a codex 批闭 commit "
              u"落地（树态实读 README+2/-1/city-humanities+12/-2 worktree 未暂存态）随轮首查；④W41 周报=10-05 后首个周轮"
              u"（自驱面+周轮云端行 CLOUD_LINE 首测窗）；⑤#70 OSS 下窗切片 2=09-29 21:40 后开随轮领——五查锚=orders 顶 "
              u"O-20260928-1910·ledger 37（六模式 CaseSensitive）·decisions 74")
with io.open(os.path.join(ROOT, sp), "w", encoding="utf-8", newline="\n") as f:
    json.dump(st, f, ensure_ascii=False, indent=2)
report.append("state.json: tick 684 + log + ts/task/focus")

io.open(os.path.join(TMP, "r684_close_report.txt"), "w", encoding="utf-8").write("\n".join(report))
print("CLOSE OK:", "; ".join(report))
