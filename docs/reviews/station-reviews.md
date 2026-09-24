# 环节评审台账（Station Reviews Ledger）

> 机制=`docs/dept-review-mechanism.md`（O-20260923-2245-bm-a）。行级追加·禁改写；每行=一次环节评审实况（环节/件/专家席/分/短板/verdict/证据指针）。
> 回填纪律：仅回填**实际发生过**的检查实况（机检结果/终审在案分数），机制生效后新件按 §3 四步正式走门。

| 日期 | 环节 | 件 | 专家席 | 分 | 最弱项/短板 | verdict | 证据指针 |
|---|---|---|---|---|---|---|---|
| 2026-09-23 | M2 素材 | bs-001-v8 三档（light/mid/full） | S2 配音听审官（回填·机检面） | —（测试件·机检档） | full 档 ASR 实测伤事实词（一名→医民/瓶酒→评久） | full=禁量产；light/mid=事实词零损 | `output/renders/.v8-*/asr-check.srt`·review-v8 §一 |
| 2026-09-23 | M2 素材 | bs-001-v9-cyber-light | S2 配音听审官（回填·机检面） | —（测试件） | **ai_feel 首战逮 gap-zero**（零间隙节拍器）；spec 门 PASS 但仅 0.7s 余量 | 机检 FAIL 在案→O-2210 人味机制立项诱因 | `ai_feel_check` v9 跑实录·review-v9 |
| 2026-09-23 | M2 素材 | bs-001-v10-humanfeel | S2 配音听审官（回填·机检面） | —（测试件） | ai_feel 四指纹全 PASS；spec 门 FAIL（64.06s 超窗=空气预算律立法诱因·演示件如实在案） | 机检面全过+一超窗在案 | review 台账 samples-review §七·renders README |
| 2026-09-23 | M4 审查（终审） | bs-001-v8 三档 | 评审团 E1-E7 | 木桶 8.5 | E2 人味金句缺一根/E6 待 CEO 亲耳/E7 视觉未赛博 | FAIL（方向首测件·如实） | `review-20260923-bs001-v8.md` |
| 2026-09-23 | M4 审查（终审） | bs-001-v9-cyber-light | 评审团 E1-E7 | 六席 9+（E4 参考 7） | E4 参考线=情感连接；E7=视觉赛博同步待令 | **PASS=放行候选**（CEO 终审待） | `review-20260923-bs001-v9.md` |
| 2026-09-23 | M5 发布（预检） | 全线（批次①未开） | S5 发布官（回填·机检面） | — | 3 阻塞=批次①账号未开+10 稿 GATE PENDING+BGM/量产等 CEO 键 | 阻塞清零前不动发布 | `readiness.py` 22:32 真跑实录 |
| 2026-09-24 | M4 审查（终审·更账） | bs-001-live-A | **E8 剪辑工艺官（追认席）** | 0/10（盲区实测） | **假绿灯更账**：当时六席 rubric 无剪辑面——9+=「文字声线过审」非「成片工艺过审」；卡点 0 切/转场 0/特效 0（静止模板段）——评审通过了它从未测量的项 | FAIL（剪辑工艺缺位·整改=R-E 剪辑站+层 1.8 门+E8 常设席 2026-09-24 全建） | review-20260924-bs001-live + editing-craft-spec §0 |
| 2026-09-24 | M3 变体（剪辑工艺·抽样） | bs-001-live-A-edit-shipinhao | E8 剪辑工艺官（会话抽样） | 9 | 弱项=Ken Burns 5% 推拉在静态 UI 底版上偏含蓄（取窗差异为主·动底版素材会更显著=假设待 M6）；全柔和转场=profile 正态 | PASS（测试件抽样档·层 1.8 PASS+抽帧验图过） | 层 1.8 跑实录+`.edit-tmp-grid.png` |
| 2026-09-24 | M3 变体（剪辑工艺·抽样） | bs-001-live-A-edit-bilibili | E8 剪辑工艺官（会话抽样） | 9 | 弱项=硬切为 0.05s 二帧淡入近似（真直切待 M2 concat 路）；白闪六命中拍全实证（YAVG 62→196）；B站真件须 16:9+3-15min 重制（#14） | PASS（口味对照件抽样档·层 1.8 PASS+spec 双 FAIL 如实在案） | 层 1.8 跑实录+YAVG 探针实录+`.edit-tmp-grid-bili.png` |
| 2026-09-24 | M3 变体（素材对位·抽样） | bs-001-v11-match-shipinhao | S3 变体官+E8（会话抽样） | 9 | 弱项=拍5「炒股票」细节画面不可证（同源替代：小镇镜因隐私作废）+拍6 自指镜间接呼应——待重采专属素材升格 | PASS（测试件抽样档·层 1.8 全 PASS+12 拍抽帧对位核验零不匹配） | `cards-v10-matched.json`+`.edit-tmp-grid-v11.png`+footage-matching-spec §4 |
| 2026-09-24 | M3 变体（平台规格·抽样） | bs-001-v12-shipinhao-60s / -bilibili-16x9 | S3 变体官（会话抽样） | 9 | 弱项=B站版时长窗仍 FAIL（内容级扩制=#14·引擎 pre-flight WARN 已点火）；**v12-shipinhao=fleet 首件三系门全过**（画幅+时长入窗+层 1.8）；空气预算 L15 首次执法 | PASS（测试件抽样档·规格前置律双实证：时长入窗 57.39s+画幅 16:9 达标） | spec 门跑实录+pre-flight WARN 录+`.edit-tmp-grid-v12.png` |
| 2026-09-24 | **全链走门演练（开闸 checklist ③首战）** | bs-001-v12-shipinhao-60s | S1→S2→S3→S4→评审团终审（全门实走） | S1 9.5/S2 9/S3 9/S4 9.5+终审七席 9+ | 61 的 ASR 同音衰减（噪声级·TTS 读数无损）+CEO 亲验=最后一键 | **PASS=放行候选（fleet 首件三系门全过+全门走毕件）**——审计缺口「零 in-chain 件」终结·开闸 checklist ②③ 已闭 | `review-20260924-bs001-v12.md`+asr-check.srt+三系门跑录 |
| 2026-09-24 | M3 变体（剪辑工艺·平台规格·抽样） | bs-001-v12-douyin-9x16 | E8 剪辑工艺官+S3 变体官（循环独立执法·机检面·R167 补账） | —（测试件·机检档） | 弱项=硬切 4 处仍 0.05s 二帧淡入近似（真直切待队列 A3 concat 路·同 bilibili 件欠账）；**douyin profile 首证件=三 profile 认证收官**：层 1.8 全 PASS（beat-align 11/11+visual-ratio 0.83+flash 6 命中拍+transition-share 0.64 落窗）+spec 抖音双 PASS（9:16+57.39s 入 15-60s·2.6s 余量） | PASS（测试件抽样档·**fleet 第三件全合规件**·三平台口味全集收官：视频号柔/B站硬切/抖音快·一条时间线三剪辑语言）——循环 S2 三门独立执法读数与批内自账零偏差（R145/R147 先例） | e54cbad 批内跑录+R167 循环执法跑录+`bs-001-v12-douyin-9x16.mp4.plan.json` |
| 2026-09-24 | M3 变体（剪辑工艺·引擎升级·抽样） | bs-001-v13-bilibili-16x9 / -douyin-9x16 | E8 剪辑工艺官+E3 工程官（循环独立执法·机检面） | —（测试件·机检档） | **A3 真直切引擎批**：E8 在案弱项「硬切=0.05s 二帧淡入近似」（live-A bilibili+v12 douyin 行欠账）本批闭环——concat 真直拼+边界帧量化+per-run trim 落点；**MAD 逐像素客观验图**：切点 MAD(f-2,f-1)≈0（出镜纯帧到缝零混合）+MAD(f-1,f)=79-136 单帧全距跳·fade 对照组连续渐变=两机制面对照成立；白闪落切后首位帧（flash_st=0 语义）；层 1.8 新代数全 PASS 双件+cut-blended 回归断言（0.05 复辟=FAIL·独立常量门） | PASS（测试件抽样档·引擎级弱项闭环件——B站时长窗 FAIL=#14 在案口径不变·203 回归绿含 4 新 A3 单测） | 双 plan.json（入 git）+R168 循环三门执法跑录+MAD 探针录 |
