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
