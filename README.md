# BigStream — AI 媒体公司

> FLUX Media 线（超体自媒体）的产品公司。2026-09-23 CEO 点名开线：产品名 BigStream（stream=流媒体·连接 FLUX「流即万物」）。
> 形态 = 集团第三家「一人 + AI 劳动力」公司：CEO（Jason）定方向、发号施令；AI 管选题、生产、适配、发布与复盘。
> 集团读序：`/README.md` → `/BRAND.md` → `/docs/philosophy.md` → `/RULES.md` → `../README.md`（线章程）→ 本文件 → `PLAN.md`。

## Identity

| 项 | 值 |
|---|---|
| 公司 | BigStream / 超体自媒体产品公司 |
| 母体 | FLUX Group（超体宇宙集团）· FLUX Media 线 |
| CEO | Jason（`/CEO` 口令发令 → `orders/` 台账落册，见 PLAN.md §0） |
| 文化分管 | Qiqi（品牌嗓音·人文内核·内容人设终审） |
| 执行 | AI 内容生产线（`docs/content-pipeline.md`） |

## 定位与主赛道（CEO 裁决 2026-09-23）

- **主赛道 = 集团 AI 生态**：把「一个人 + AI 如何开出三家无人值守公司」做成知识内容——真实实践、独家数据、天然自传播；反哺集团品牌。
- Lucy 面：knowledge is unbounded——知识传递不设上限。
- WALL-E 面：clean content, not garbage feed——干净内容，不做垃圾流。
- 扩展赛道（后置）：量化投资知识、游戏与小游戏行业——由选题库数据决定开不开。

## 平台矩阵（CEO 令 2026-09-23）

视频号 · 公众号 · B站 · YouTube · 新浪微博（详见 `docs/platform-playbook.md`；账号 = CEO 物理件，见 `docs/accounts.md`）。

## Structure

```
BigStream/
├── README.md          <- 本文件（公司章程入口）
├── PLAN.md            <- 公司总纲（阶段/生产线/合规/CEO 待决清单）
├── orders/            <- CEO 令牌台账（/CEO 触发·追加式）
├── docs/              <- content-pipeline.md / platform-playbook.md / accounts.md
├── data/
│   ├── ideas/         <- 选题库（ideas.md 一行一题）
│   ├── drafts/        <- 脚本与文案草稿
│   └── sources/       <- 素材与来源引用（可溯链）
├── output/           <- 成品库（gitignored·二进制不入库）
├── src/               <- 工具脚本（适配/审查门/统计，按需建）
└── tests/             <- 脚本测试（按需建）
```

## Run commands

（暂无——生产线脚本到位后回填于此，一行命令制）

## Red lines（集团红线本线落地）

- 不做标题党：标题承诺什么，内容就交付什么。
- 不编数据；无来源不发布（cite sources or don't publish）。
- 算法优化分发，不优化成瘾。
- AIGC 内容依法显著标识（中国《人工智能生成合成内容标识办法》+ 各平台对应规则）。
- 账号/凭据 = CEO 物理件：AI 永不代办账号域；密钥只进 `.env`（gitignored）。
