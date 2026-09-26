# BigStream — AI 媒体公司

> FLUX Media 线（超体自媒体）的产品公司。2026-09-23 CEO 点名开线：产品名 BigStream（stream=流媒体·连接 FLUX「流即万物」）。
> 形态 = 集团第三家「一人 + AI 劳动力」公司：CEO（Jason）定方向、发号施令；AI 管选题、生产、适配、发布与复盘。
> 集团读序：`/README.md` → `/BRAND.md` → `/docs/philosophy.md` → `/RULES.md` → `../README.md`（线章程）→ 本文件 → `CONSTITUTION.md`（宪法）→ `PLAN.md`。

## Identity

| 项 | 值 |
|---|---|
| 公司 | BigStream / 超体自媒体产品公司 |
| 母体 | FLUX Group（超体宇宙集团）· FLUX Media 线 |
| CEO | Jason（`/CEO` 口令发令 → `orders/` 台账落册，见 PLAN.md §0） |
| 文化分管 | Qiqi（品牌嗓音·人文内核·内容人设终审） |
| 栏目矩阵 | 三案全锁（2026-09-23 终审）：《超体日志》主轴 ·《AI 打工实录》短视频变体 ·《一人集团》深度线（`docs/column-persona-proposals.md`） |
| 组织编制 | 七部一办（AI 全编制）＋CEO 决策面＋Qiqi 终审面：`docs/org-structure.md`；法律层级与宪法红线：`CONSTITUTION.md` |
| 执行 | AI 内容生产线（`docs/content-pipeline.md`）＋ OS 自迭代循环（`docs/os-protocol.md`） |

## 定位与主赛道（CEO 裁决 2026-09-23）

- **主赛道 = 集团 AI 生态**：把「一个人 + AI 如何开出三家无人值守公司」做成知识内容——真实实践、独家数据、天然自传播；反哺集团品牌。
- Lucy 面：knowledge is unbounded——知识传递不设上限。
- WALL-E 面：clean content, not garbage feed——干净内容，不做垃圾流。
- 扩展赛道（后置）：量化投资知识、游戏与小游戏行业——由选题库数据决定开不开。

## 平台矩阵（CEO 令 2026-09-23 · 主流全覆盖）

11 平台四层：视频号 · 公众号 · 抖音 · 小红书 · 快手 · B站 · 知乎 · 今日头条 · 微博 · YouTube · TikTok。
顶层机制=`docs/media-matrix.md`；单平台策略=`docs/platform-playbook.md`；账号台账=`docs/accounts.md`（开号=CEO 物理件，分五批）。

## Structure

```
BigStream/
├── README.md          <- 本文件（公司章程入口）
├── CONSTITUTION.md    <- 公司宪法（顶层规则·法律层级·宪法红线）
├── PLAN.md            <- 公司总纲（阶段/生产线/合规/CEO 待决清单）
├── orders/            <- CEO 令牌台账（/CEO 触发·追加式）
├── docs/              <- production-chain.md / m2-local-stack.md / org-structure.md / capabilities.md / os-protocol.md / media-matrix.md / content-pipeline.md / platform-playbook.md / accounts.md / column-persona-proposals.md / variant-templates.md
├── data/
│   ├── ideas/         <- 选题库（ideas.md 一行一题）
│   ├── drafts/        <- 脚本与文案草稿（10 稿封存·生产暂停中）
│   └── sources/       <- 素材与来源引用（可溯链）
├── output/          <- 成品库（二进制 gitignored；schedule.md/analytics.md 台账入库）
├── research/        <- 调研面（P-65 声明行：双线=市场线→选题研究部·技术线→工程技术部；消费方=M0 选题/人设/平台策略/情报日报 + M2 素材链选型；行程标准与结论应用律正典=../cph4/research-protocol.md，本司细则=docs/research-protocol.md 指针件）
├── src/               <- draft_lint.py（M4 机审）· board_check.py（链路一致性）· make_draft.py（骨架生成）· os/（OS 循环四件套+任务书+state+backlog+skeletons）
└── tests/             <- 脚本测试（按需建）
```

## Skills（司内技能登记 · P-20260926-01）

源码入仓 `tools/skills/`；安装位 workspace scope `.codely-cli/skills/`（新会话自动发现；交互会话中改版后须 `/skills reload` 生效）。清单式回执=技能名+用途+触发场景：

- `bigstream-lcard-pipeline` — L-卡四形态（语录 QUOTE/盘点 DIGEST/图鉴 CENSUS/速报 REACT）全链量产工艺。触发=产/审/续任何 BigStream 静态图文卡（供给门锚核→M0 四维分→M1 verbatim 抽取→M2 --poster+em 预算+验图五检→M3 四禁→M4 四检→M4.5 七席+E4 参考仪→F 登记）。
- `bigstream-s2-probes` — S2 机检三门+验图采样面三律执法组合（层 1.8）。触发=核验/补账/收口任何渲染件与纯音频件（ai_feel/platform_spec/edit_craft 三门+拍头/段中尾/回环边界采样；FAIL 如实入账、不自行修改在途批）。
- 会话内置在役 3 件：`codely-guide`（平台 how-to）/ `skill-creator`（技能创建器）/ `tuanjie-cli`（团结引擎管理）。

## Run commands

- M4 机审全量：`python src/draft_lint.py`
- 链路一致性：`python src/board_check.py`
- 草稿骨架生成：`python src/make_draft.py <选题号> <平台键>`（11 平台键见文件头注；生产位受生产闸门管控，paused 态拒稿）
- 生产闸门态：`src/os/state.json` 的 `production` 字段（现 paused·开闸须 CEO 令）
- M2 本地算力链（选型已裁=本地优先）：`docs/m2-local-stack.md`（实况盘点+四站方案+PoC 阶梯）
- OS 循环注册/自愈：`powershell -NoProfile -ExecutionPolicy Bypass -File src/os/register_loop_task.ps1`
- 循环实况：`logs/probe-heartbeat.txt`（心跳）· `src/os/state.json`（tick 账本）

## Red lines（集团红线本线落地）

- 不做标题党：标题承诺什么，内容就交付什么。
- 不编数据；无来源不发布（cite sources or don't publish）。
- 算法优化分发，不优化成瘾。
- AIGC 内容依法显著标识（中国《人工智能生成合成内容标识办法》+ 各平台对应规则）。
- 账号/凭据 = CEO 物理件：AI 永不代办账号域；密钥只进 `.env`（gitignored）。
