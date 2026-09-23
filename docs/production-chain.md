# BigStream 自动化生产全链路（Production Chain）

> CEO 令 O-20260923-1600-bm-a：「自媒体自动化生产全链路构建」。
> 全链=M0→M6（流程定义=`docs/content-pipeline.md`）；本件=各站自动化设计：自动化级、工具、门禁——引用不复制，工具实况以 `docs/capabilities.md` 为准。

## §0 生产闸门（唯一总开关）

- 闸门态=`src/os/state.json` 字段 `production`（现值 **paused** · O-20260923-1756-bm-a 模式修正「不量产」；开闸史=O-1602 批次2 曾 open·本表当时未同步属滞后·O-1756 回关；量产开闸须 CEO 令）。
- **开闸**=CEO 令 → 总裁办公室落 O 文件 + 翻 `state.json`（`production: open`）+ 改循环任务书生产段（任务书=数据件可热改，无需重装）+ `board_check` 回归。**关闸同律**。
- 机牢执行：`src/make_draft.py` 生产位（`data/drafts/`）在 paused 态拒稿（exit 3）——闸门长牙，不靠自觉。

## §1 自动化级定义

- **全自动**：无人值守可跑（OS 循环/脚本/探针）。
- **半自动**：AI 量产 + 人工点（批注/终审）。
- **人工点**：物理件/裁决（不可自动化·永不代办）。

## §2 全链路站表（七站·自动化级·工具·门禁）

| 站 | 自动化级 | 工具/执行体 | 门禁 | 实况 |
|---|---|---|---|---|
| M0 选题 | 半自动 | OS 循环生产轮提案（源=集团 git 实况）+ `board_check.py` 一致性探针（C-08 live） | CEO 批注门；每题来源可溯；**S0 选题官环节门** | gated（闸门关） |
| M1 母稿 | 半自动 | `src/make_draft.py` 骨架生成（C-15）+ AI 会话填充 | 命名/版本律；骨架自带 GATE PENDING；**S1 编剧官环节门（铁律自检表随稿·进链件 ≥9）** | gated |
| M2 素材 | 半自动 | **本地算力链**（C-11 in-dev·选型已裁=本地优先 O-20260923-1609-bm-a）：edge-tts/faster-whisper/FFmpeg/opencv 已装·四站方案=`docs/m2-local-stack.md`·PoC=backlog #9 | 素材脱敏审；来源可溯；**人味规格环节（O-2210）：拍稿预算含空气预算（60s→≤55s 文本）·配音走 `--human` 种子**；**S2 配音听审官环节门（ASR+ai_feel+spec 三机检前置）** | in-dev |
| M3 变体 | 全自动骨架 | `docs/variant-templates.md` 11 平台骨架（C-07 live）+ make_draft 变体位 | 母稿链接登记；lint 0 FAIL；**S3 变体官环节门（平台语态/规格窗·进链件 ≥9）** | gated |
| M4 审查 | 全动机审＋人工点人审 | `src/draft_lint.py`（C-01 live·12 用例）+ 层 1.5 工艺审（铁律趣律/视觉审）+ **层 1.6 AI 感机检（`src/ai_feel_check.py`·O-2210：gap-zero/gap-uniform/pacing/prosody 四 FAIL 档）**+ **层 1.7 平台规格门（`src/platform_spec_check.py`·时长实测红线工具化：ffprobe 时长/画幅 vs playbook 规格表实解析·首战舰队体检 14 件=视频号 9 PASS+2 时长 FAIL 在案+B站 3 件全低于 3-15min 窗=B站纵深格式待重制）** + 嗓音人审（Qiqi/CEO 抽样） | FAIL=禁发布，无例外；**S4 合规官环节门（红线一票否决）→评审团终审（环节门全过后最后一关）** | **live** |
| M5 发布 | 半自动 | `output/schedule.md` 台账（C-05）；公众号草稿 API+YouTube Data API=接口已定（C-12 blocked·账号） | 发布=M4 PASS+账号就绪双前置；**S5 发布官环节门（readiness 阻塞清零+发布物齐备）** | blocked |
| M6 复盘 | 半自动 | `output/analytics.md`+周报生成器（C-09 in-dev） | 未上线=未测量；周对账一行制；**S6 数据官环节门（假设逐条校准·证伪即改）** | in-dev |

链路单命令视图：`python src/board_check.py`（选题板↔稿位一致性·FAIL 类见该文件头注）。
**环节门正典=`docs/dept-review-mechanism.md`**（O-2245·七席 S0-S6 与评审团关系见该件）。

## §3 生产模式协议（开闸后循环切换）

1. 总裁办公室：落 O 文件 + 翻 `state.json` `production: open` + 改 `src/os/iteration_prompt.txt` 生产段。
2. 循环生产轮节奏：每周 M0 提案批（≤5 条防灌水）→ **CEO 批注（人工点）** → M1/M3 量产（make_draft 骨架）→ M4 机审全绿 → 嗓音抽样人审 → M5 排期台账 → M6 周复盘。
3. 量产红线：标题党检测/来源完备/AIGC 标识/量化声明/时长实测——M4 是唯一发布前置。
4. 节奏与北极星：P3 常态·周复盘驱动；商业化仍 P1 署名。
5. **评审效率**（O-2245/O-2248）：环节门并行评审+合并整改清单；终审返工 ≤2 轮超限升裁；批量内变体共享母件结论轻量复检；SLA ≤24h 不压件——**审到点上，不审到瘫**（正典=dept-review-mechanism §5·红线面豁免不参与平衡）。

## §4 红线（全链路任何站不得绕过）

不标题党 / 无来源不发布 / AIGC 依法标识 / 量化附非投资建议 / 账号物理件永不代办——宪法 `CONSTITUTION.md` §2 全文。

## 变更记录

- 2026-09-23: v1.0 建链（CEO 令 O-20260923-1600-bm-a）——七站全表+生产闸门+生产模式协议；M4 已 live，M0/M1/M3 骨架就绪待闸，M2/M5 blocked（选型/账号），M6 in-dev。
- 2026-09-23: v1.1 本地算力批（CEO 令 O-20260923-1609-bm-a）——M2 站选型已裁=**本地算力优先**（四站本地方案+显存分时+PoC 阶梯=`docs/m2-local-stack.md`）；M2 由 blocked 转 in-dev。
- 2026-09-23: v1.2 闸门机牢同步（CEO 令 O-20260923-1756-bm-a 模式修正·R15 补落）——O-1602 开闸态与本令「不量产」意图不符属机牢缺口：`production` 回 `paused`+`mode` 改 systems-first；make_draft 闸门报错文案引用本令；测试生产位（`--out` 临时目录）不受闸门影响照旧放行（令中「允许测试生产」）。§1 站表实况 gated 行随闸门态恢复正确。
- 2026-09-23: v1.3 人味机制批（CEO 令 O-20260923-2210-bm-a「从底层要去ai感觉，做好相关机制」）——M2 增人味规格环节（空气预算律·`--human` 种子）；M4 增层 1.6 AI 感机检（`src/ai_feel_check.py` 四指纹）；规格正典=`docs/human-feel-spec.md`；首战实证 v9 FAIL（零间隙节拍器）→v10 PASS。
- 2026-09-23: v1.4 平台规格门（O-2210 自治续·时长实测红线工具化）——M4 增层 1.7 `src/platform_spec_check.py`（ffprobe 时长/画幅 vs playbook 规格表**实解析**单一真相零漂移·10 单测）；首战舰队体检：视频号线 9/11 PASS（v5 60.58s/v10 64.06s 两超窗在案·v9 仅 0.7s 余量=空气预算律必要性再证）；**B站三件全低于 3-15min 窗→「B站版」定位修正=纵深格式重制非 60s 改写**（backlog #14·量产开闸后执行）。
- 2026-09-23: v1.5 部门专家评审机制（CEO 令 O-20260923-2245-bm-a「制定部门专家评审机制，提升每个环节品质」）——七站各挂环节席（S0 选题官/S1 编剧官/S2 配音听审官/S3 变体官/S4 合规官/S5 发布官/S6 数据官·归口部门见 org-structure）；正典=`docs/dept-review-mechanism.md`·台账=`docs/reviews/station-reviews.md`（今晚实况回填首批）；进链件环节席 ≥9·测试件=机检+抽样。
- 2026-09-23: v1.6 评审效率平衡（CEO 校准令 O-20260923-2248-bm-a「你也不能审到效率产出低下，要平衡」）——§3 增评审效率行：并行评审/终审返工 ≤2 轮超限升裁/批量共享轻量复检/SLA ≤24h；正典=dept-review-mechanism v1.1 §5（B1-B6·红线面豁免不参与平衡）。
