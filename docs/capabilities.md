# BigStream 自动化能力注册表（Capabilities Registry）

> CEO 令 O-20260923-1536-bm-a：「底层技术等一系列的自动化开发能力」。
> 归口=工程技术部；入列规则如下，任何能力宣称必须有实证。

## §1 入列规则

- **live**：已入库且有实测证据（命令/日志/commit）。
- **in-dev**：backlog 已排、OS 循环在建。
- **planned**：已定方向未排期。
- **blocked**：被外部前置卡住（账号未开/CEO 待决/生产暂停令）——须注明卡点。
- 状态变更=改表+commit；宣称 live 而无证据=违规（诚实律）。

## §2 注册表

| ID | 能力 | 归属部门 | 状态 | 入口/证据 |
|---|---|---|---|---|
| C-01 | M4 机审门（draft_lint） | 合规审查部 | live | `python src/draft_lint.py` · 10 稿 0 FAIL 实测（首战拦 1 FAIL 1 脱敏） |
| C-02 | OS 自迭代循环（10 分钟/轮） | 工程技术部 | live | BigStream-OSLoop · 15:32 首轮 spawn 实证（run log） |
| C-03 | CEO 令牌台账（/CEO→O 文件） | 总裁办公室 | live | `orders/` 5 令实录 |
| C-04 | 三级记忆体系 | 工程技术部 | live | 媒体线 CODELY.md + 本仓 CODELY.md |
| C-05 | 发布/数据台账结构 | 平台运营部+数据分析部 | live | `output/schedule.md`+`output/analytics.md` |
| C-06 | draft_lint 测试件 | 工程技术部 | in-dev | backlog #1 |
| C-07 | 11 平台变体骨架模板 | 平台运营部 | in-dev | backlog #2 |
| C-08 | 选题-台账一致性探针 | 选题研究部 | in-dev | backlog #3 |
| C-09 | 自动周报生成器（state+commits→周报） | 数据分析部 | in-dev | backlog #6 |
| C-10 | 视频号口播裁剪（4 稿 67-77s） | 内容生产部 | blocked | 卡点=生产暂停令 |
| C-11 | M2 素材链路（TTS/形象选型） | 内容生产部 | blocked | 卡点=CEO 待决+账号 |
| C-12 | 平台 API 发布对接 | 平台运营部 | blocked | 卡点=账号未开（批次①） |
| C-13 | 数据回流自动化（后台导出→对账） | 数据分析部 | planned | 待上线后实况定通道 |

## §3 能力建设循环

新能力＝工程技术部（或归口部门）在 backlog 立项 → OS 循环按轮开发 → 实测证据落 logs/commit → 本表升 live。禁止跳过证据直接宣称。

## 变更记录

- 2026-09-23: v1.0 建册（CEO 令 O-20260923-1536-bm-a）——live×5 / in-dev×4 / blocked×3 / planned×1。
