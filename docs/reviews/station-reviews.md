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
