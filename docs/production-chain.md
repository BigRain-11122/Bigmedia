# BigStream 自动化生产全链路（Production Chain）

> CEO 令 O-20260923-1600-bm-a：「自媒体自动化生产全链路构建」。
> 全链=M0→M6（流程定义=`docs/content-pipeline.md`）；本件=各站自动化设计：自动化级、工具、门禁——引用不复制，工具实况以 `docs/capabilities.md` 为准。

## §0 生产闸门（唯一总开关）

- 闸门态=`src/os/state.json` 字段 `production`（现值 **paused** · O-20260923-1525-bm-a）。
- **开闸**=CEO 令 → 总裁办公室落 O 文件 + 翻 `state.json`（`production: open`）+ 改循环任务书生产段（任务书=数据件可热改，无需重装）+ `board_check` 回归。**关闸同律**。
- 机牢执行：`src/make_draft.py` 生产位（`data/drafts/`）在 paused 态拒稿（exit 3）——闸门长牙，不靠自觉。

## §1 自动化级定义

- **全自动**：无人值守可跑（OS 循环/脚本/探针）。
- **半自动**：AI 量产 + 人工点（批注/终审）。
- **人工点**：物理件/裁决（不可自动化·永不代办）。

## §2 全链路站表（七站·自动化级·工具·门禁）

| 站 | 自动化级 | 工具/执行体 | 门禁 | 实况 |
|---|---|---|---|---|
| M0 选题 | 半自动 | OS 循环生产轮提案（源=集团 git 实况）+ `board_check.py` 一致性探针（C-08 live） | CEO 批注门；每题来源可溯 | gated（闸门关） |
| M1 母稿 | 半自动 | `src/make_draft.py` 骨架生成（C-15）+ AI 会话填充 | 命名/版本律；骨架自带 GATE PENDING | gated |
| M2 素材 | 半自动 | 零预算链路选型（C-11 blocked·needs-CEO）；三案人设参数已锁 | 素材脱敏审；来源可溯 | blocked |
| M3 变体 | 全自动骨架 | `docs/variant-templates.md` 11 平台骨架（C-07 live）+ make_draft 变体位 | 母稿链接登记；lint 0 FAIL | gated |
| M4 审查 | 全动机审＋人工点人审 | `src/draft_lint.py`（C-01 live·12 用例）+ 嗓音人审（Qiqi/CEO 抽样） | FAIL=禁发布，无例外 | **live** |
| M5 发布 | 半自动 | `output/schedule.md` 台账（C-05）；公众号草稿 API+YouTube Data API=接口已定（C-12 blocked·账号） | 发布=M4 PASS+账号就绪双前置 | blocked |
| M6 复盘 | 半自动 | `output/analytics.md`+周报生成器（C-09 in-dev） | 未上线=未测量；周对账一行制 | in-dev |

链路单命令视图：`python src/board_check.py`（选题板↔稿位一致性·FAIL 类见该文件头注）。

## §3 生产模式协议（开闸后循环切换）

1. 总裁办公室：落 O 文件 + 翻 `state.json` `production: open` + 改 `src/os/iteration_prompt.txt` 生产段。
2. 循环生产轮节奏：每周 M0 提案批（≤5 条防灌水）→ **CEO 批注（人工点）** → M1/M3 量产（make_draft 骨架）→ M4 机审全绿 → 嗓音抽样人审 → M5 排期台账 → M6 周复盘。
3. 量产红线：标题党检测/来源完备/AIGC 标识/量化声明/时长实测——M4 是唯一发布前置。
4. 节奏与北极星：P3 常态·周复盘驱动；商业化仍 P1 署名。

## §4 红线（全链路任何站不得绕过）

不标题党 / 无来源不发布 / AIGC 依法标识 / 量化附非投资建议 / 账号物理件永不代办——宪法 `CONSTITUTION.md` §2 全文。

## 变更记录

- 2026-09-23: v1.0 建链（CEO 令 O-20260923-1600-bm-a）——七站全表+生产闸门+生产模式协议；M4 已 live，M0/M1/M3 骨架就绪待闸，M2/M5 blocked（选型/账号），M6 in-dev。
