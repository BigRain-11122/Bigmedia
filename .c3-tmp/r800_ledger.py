# -*- coding: utf-8 -*-
# R800: BS-008 render-leg ledger closeout (renders README + station-reviews + bs008 README + queue)
import io

# ---------- 1. renders README: declaration-row update + in-chain table row ----------
p = r"output\renders\README.md"
t = io.open(p, encoding="utf-8").read()
old_tail = "（渲染腿〔素材探针先行→对位表→R-E shipinhao〔系列角标 BS-008 EP.08〕→S2 三门+帧验三律=R760 同型〕→收官腿〔E8+ASR+E4+M4→F 登记→冗余池第十九件→E23 出池+补池义务〕随轮领）"
new_tail = ("（渲染腿**毕**〔R800：素材探针先行〔looplog/reviewsdoc/editgrid 三源三时点多模态=零录穿 probe-r800·biggame-cockpit 弱对位弃用〕→对位表 cards-v2-matched.json 10/12=0.83"
            "〔F-002/F-004 同源 0.83 带=R799 预评估口径兑现〕→全卡几何审计 12 卡 problems=NONE→R-E shipinhao〔系列角标 BS-008 EP.08〕55.254s 音轨分毫一致 4.7s 余量"
            "→S2 三门全绿+帧验三律全过+轮内咬住修红 1 处〔首渲 b4 副题折行断在「2.057」数字中间→分隔符显式拆行 verbatim 零改→重渲复验零数字拆行〕·详见下表在链行〕"
            "→收官腿〔E8+ASR+E4+M4→F 登记→冗余池第十九件→E23 出池+补池义务〕随轮领）")
assert old_tail in t, "declaration tail not found"
t = t.replace(old_tail, new_tail)

row = ("| bs-008-v1-shipinhao-60s.mp4 | **在链件（queue §E 批活池 E23 稿集件·渲染腿毕 R800·收官腿 R801 随轮领）** | "
       "**R-E shipinhao 12 段 11 柔转场 0 硬切**·9:16 1080×1920·**55.254s ffprobe 实测=音轨分毫一致·4.7s 余量**"
       "〔plan 内部预估 56.033s=tail 余量项·实测为准 LC-008 判例〕·hits=[0]·**S5.5 角标常驻位**=BigStream\\|BS-008 EP.08"
       "+§4.5 三开关[glow/scanlines/sys.beat=NN t=MM:SS]·plan.series+s45_dials 入 plan.json·"
       "**稿集形态对位 10/12=0.83**（素材探针先行三源三时点多模态零录穿〔probe-r800/probe-src-tile.png〕："
       "looplog=BS-OSLoop.log 终端×5〔b0 系统日志本体直证=hook 口播「系统日志」字面/b1 门禁链=拦截判定行/b6 无崩年=档案逐年记录形态意象/"
       "b7 死法标注=FAIL 判定行 F-004 v15 b1 同拍位/b10 首月检查=轮次检查节律·同源多用注记〕"
       "+reviewsdoc=站审台账×4〔b2 唯一通关=PASS 判定行/b3 注册件=台账登记 F-004 v15 b8 同拍位/b8 诚实律=verdict+证据链列 F-004 v15 b9 同锚行同拍位/"
       "b9 在册=台账条目〕+editgrid=自产字卡 2×2 网格×1〔b5 逐笔清单=逐条并列网格形态·F-004 v15 b11 同型意象对位声明〕"
       "+cards-only×2〔b4 核心读数=BigMoney 持仓画面判敏感禁用 F-004 v15 b5 同拍位先例/b11 CTA+量化合规拍=F-004 v15 b11 同位〕"
       "·F-002/F-004 同源 0.83 带=R799 预评估口径兑现·biggame-cockpit 弱对位弃用）——"
       "**全卡几何审计 12 卡 problems=NONE 零修红前置预防**（2-3 行块顶 831-874 净 64-107px·r800_card_audit·R720 律预执行=前置预防通道第九件）——"
       "**S2 三门 R800 循环独立执法全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·pacing CV 0.218·prosody 9 档 12 拍·copy CV 0.265=R799 早门读数同音轴确定性）"
       "+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 0.83+transition-share 1.00 无连排+transition-variety+timeline 代数过）"
       "+spec 微信视频号双 PASS（9:16+55.25s ∈30-60s 窗 4.7s 余量）——"
       "**帧验三律全过**：拍头 12/12 语义全中（H1 拍名 12/12 逐拍对位+sys.beat 01→12 连续无跳号 t 单调递增+角标 12 帧全在+AIGC 帧头标识全在）"
       "+**轮内咬住修红 1 处**（首渲 b4 副题折行断在「2.057」数字中间=多模态帧验当场揭→对位表 SPLIT 修正〔b4/b7 在「·」分隔符处显式拆行·卡锚文本 verbatim 零改仅行边界〕"
       "→重渲复验 h04「样本外 Sharpe 2.057/成本 ×2 存活」+h07「成本 ×3 不存活/厚度上限 2 倍」全行零数字拆行=R381 首渲真发现即修同型·b4 核心读数=本件最重要数字位）"
       "+段中尾 6/6 稳定零录穿（law2=动态三最长拍 b0/b1/b11〔6.05/5.72/5.71s〕·tile 缩略误读族〔「1 贝存活」等〕=R189 手段问题律·段尾卡面持久=LC-012 段尾对照同型设计）"
       "+回环 crossings={}（max 拍 6.05s<源 reviewsdoc/editgrid 10s 最短源·诚实计算）+AIGC 双标识分层可读（帧头标识 12/12+卡面左上标签位） "
       "| plan.json 入 git·mp4 gitignored·在链件非成品（收官腿 E8+ASR+E4+M4→F 登记→冗余池第十九件落位→E23 出池+补池义务=R801 首位·发布锁=M5 账号物理件未开·未上线=未测量） |\n")

lines = t.split("\n")
idx = next(i for i, l in enumerate(lines) if l.startswith("| bs-007-v1-shipinhao-60s.mp4"))
lines.insert(idx + 1, row.rstrip("\n"))
io.open(p, "w", encoding="utf-8").write("\n".join(lines))
print("renders README: declaration updated + in-chain row after bs-007 row", idx + 1)

# ---------- 2. station-reviews: S2 row append ----------
p2 = r"docs\reviews\station-reviews.md"
sr = ("| 2026-10-01 | **S2 三门循环独立执法+帧验三律+全卡几何审计零修红+轮内咬住排版修红 1 处（bs-008-v1-shipinhao=queue §E 批活池 E23 稿集件渲染腿·视频号冗余池第十九件候选·R799 起链→R800 渲染腿）** | "
      "ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s varied·pacing CV 0.218·prosody 9 档 12 拍·copy CV 0.265=R799 早门读数同音轴确定性）"
      "+层 1.8 六面 PASS（beat-align 11/11·camera 12 段全动·visual-ratio 0.83=10/12〔looplog×5+reviewsdoc×4+editgrid×1+cards-only×2·素材探针先行三源三时点多模态零录穿 probe-r800〕"
      "·transition-share 1.00 无连排·transition-variety·timeline 代数过）+spec 微信视频号双 PASS（9:16+55.25s ∈30-60s 窗 4.7s 余量）| "
      "帧验三律全过：拍头 12/12（H1 拍名逐拍对位+sys.beat 01→12 连续 t 单调+角标 12 帧全在+AIGC 帧头标识全在）"
      "+段中尾 6/6（b0/b1/b11 三最长拍·段中尾字幕净读·tile 缩略误读族全分辨率定谳=R189 手段问题律·段尾卡面持久=LC-012 同型设计）"
      "+回环 crossings={}（max 拍 6.05s<最短源 10s 诚实计算）；"
      "**轮内咬住修红**=首渲 b4 副题折行断在「2.057」数字中间（多模态帧验揭）→对位表 b4/b7 分隔符处显式拆行（卡锚 verbatim 零改仅行边界）→重渲复验零数字拆行"
      "（R381 首渲真发现即修同型·b4 核心读数=本件最重要数字位）；全卡几何审计 r800_card_audit 12 卡 problems=NONE（2-3 行块顶 831-874）"
      "·在链件非成品（E8+ASR+E4+M4→F 登记=R801 收官腿） | S2 probe .c3-tmp/r800_s2.txt·plan.json 入 git |\n")
with io.open(p2, "a", encoding="utf-8") as f:
    f.write(sr)
print("station-reviews row appended")

# ---------- 3. bs008 README: render-leg row ----------
p3 = r"data\sources\bs008\README.md"
br = ("- **R800 渲染腿毕（五步全链）**：①素材探针先行=looplog/reviewsdoc/editgrid 三源三时点多模态定谳零录穿（probe-r800/probe-src-tile.png·looplog=BS-OSLoop.log 静态终端 12s/reviewsdoc=台账清单静态 10s/editgrid=自产字卡 2×2 网格静态 10s·**biggame-cockpit 弱对位弃用**=R799 预评估口径执行）；"
      "②对位表 cards-v2-matched.json 10/12=0.83（looplog×5〔b0/b1/b6/b7/b10〕+reviewsdoc×4〔b2/b3/b8/b9〕+editgrid×1〔b5 逐笔清单=网格并列形态·F-004 v15 b11 同型意象〕+cards-only×2〔b4 核心读数=BigMoney 持仓画面判敏感禁用 F-004 v15 b5 同拍位先例/b11 CTA+量化合规拍〕=F-002/F-004 同源 0.83 带·R799 预评估口径兑现）；"
      "③全卡几何审计 problems=NONE 零修红前置预防（12 卡 2-3 行块顶 831-874 净 64-107px·r800_card_audit）；"
      "④R-E shipinhao 渲染 bs-008-v1-shipinhao-60s.mp4（9:16 1080×1920·55.254s=音轨分毫一致 4.7s 余量·12 段 11 柔 0 硬切·hits=[0]·角标=BigStream|BS-008 EP.08+§4.5 三开关·plan.json 入 git）"
      "+**轮内咬住修红 1 处**（首渲 b4 副题折行断在「2.057」数字中间=多模态帧验当场揭→对位表 b4/b7 分隔符处显式拆行〔卡锚 verbatim 零改仅行边界〕→重渲复验零数字拆行=R381 首渲真发现即修同型·b4 核心读数=本件最重要数字位）；"
      "⑤S2 三门循环独立执法全绿（ai_feel 0F0W CV 0.218/0.265+层 1.8 六面 PASS visual-ratio 0.83+spec 微信视频号双 PASS 4.7s 余量）+帧验三律全过（拍头 12/12+段中尾 6/6+回环 crossings={}〔max 拍 6.05s<最短源 10s〕）；"
      "台账=renders 在链行+station-reviews S2 行+本节。**收官腿（E8+ASR+E4+M4→F 登记→冗余池第十九件落位→E23 出池+补池义务）=R801 首位**。\n")
with io.open(p3, "a", encoding="utf-8") as f:
    f.write(br)
print("bs008 README row appended")

# ---------- 4. queue §E burn row ----------
p4 = r"docs\self-improvement-queue.md"
q = ("- 2026-10-01: **E23 BS-008《幸存者档案》渲染腿毕（R800·R799 指针兑现·lane=E23〔active〕+supply-gated 豁免面维持·产品优先律对位=本轮新实物=bs-008-v1-shipinhao-60s.mp4 成片在链）**："
     "①素材探针先行=looplog/reviewsdoc/editgrid 三源三时点多模态定谳零录穿（probe-r800/probe-src-tile.png·biggame-cockpit 弱对位弃用）；"
     "②对位表 cards-v2-matched.json 10/12=0.83（looplog×5〔b0 系统日志直证/b1 门禁链=拦截判定行/b6 无崩年=档案逐年记录形态/b7 死法标注=FAIL 判定行/b10 首月检查=轮次检查节律〕"
     "+reviewsdoc×4〔b2 唯一通关=PASS 判定/b3 注册件=台账登记/b8 诚实律=verdict 证据链列 F-004 v15 b9 同拍位/b9 在册=台账条目〕"
     "+editgrid×1〔b5 逐笔清单=网格并列形态 F-004 v15 b11 同型〕+cards-only×2〔b4 核心读数=BigMoney 判敏感禁用/b11 CTA+合规拍〕=F-002/F-004 同源 0.83 带=R799 预评估口径兑现）；"
     "③全卡几何审计 12 卡 problems=NONE（r800_card_audit·R720 律预执行=前置预防通道第九件）；"
     "④R-E shipinhao 渲染毕（9:16 1080×1920·55.254s ffprobe=音轨分毫一致 4.7s 余量·12 段 11 柔 0 硬切·hits=[0]·角标=BigStream|BS-008 EP.08+§4.5 三开关·plan.json 入 git）"
     "+**轮内咬住修红 1 处**（首渲 b4 副题折行断在「2.057」数字中间→对位表 b4/b7 分隔符显式拆行〔verbatim 零改仅行边界〕→重渲复验零数字拆行=R381 同型）；"
     "⑤S2 三门循环独立执法全绿（ai_feel 0F0W CV 0.218/0.265+层 1.8 六面 PASS visual-ratio 0.83+spec 微信视频号双 PASS 4.7s 余量）；"
     "⑥帧验三律全过（拍头 12/12+段中尾 6/6+回环 crossings={}〔max 拍 6.05s<最短源 10s〕）；"
     "台账=renders 在链行+station-reviews S2 行+bs008 README 渲染腿段+export 刷。**收官腿（E8 终审+ASR 终轨+E4 参考仪+M4→F 登记→冗余池第十九件落位→E23 出池+补池义务随轮领）=R801 首位**。\n")
with io.open(p4, "a", encoding="utf-8") as f:
    f.write(q)
print("queue burn row appended")
