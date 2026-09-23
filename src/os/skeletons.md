# BigStream 草稿骨架数据件（draft skeletons）

> UTF-8 数据件——编码律：`src/make_draft.py` 为纯 ASCII，中文骨架全部住本文件。
> 占位符：`{DATE}` `{TOPIC}` `{PLATFORM}` `{VER}` `{MASTER}` `{SOURCE}` `{SPEC_BLOCK}`——由 make_draft 运行时替换。
> 交付=CEO 令 O-20260923-1600-bm-a（全链构建）；骨架=机制件，生成=受生产闸门管控（production-chain.md §0）。

[master]
# {DATE}-{TOPIC}-公众号-v{VER}

> 母稿（M1 主稿）｜选题 {TOPIC}｜平台 微信公众号｜{DATE}
> 变体登记：（生成变体后回填：平台→文件名）
> 状态：制作中 → 待 M4 合规门

## 标题候选（搜索词+利益点双写）

1.
2.
3.

## 正文

（待填充——标题承诺什么，正文就交付什么）

## 来源清单（可溯·内部私有仓·脱敏引用·M4 逐条对账）

1. {SOURCE}

## AIGC 声明

本文由 BigStream AI 内容生产线生成并自审，依中国《人工智能生成合成内容标识办法》及平台规则显著标识：**本文为 AI 生成内容**。

## GATE

GATE: PENDING（发布前置门未过——M4 机审+人审于发布前执行）

[v1]
# {DATE}-{TOPIC}-{PLATFORM}-v{VER}

> 变体（M3）｜母稿= data/drafts/{MASTER} ｜选题 {TOPIC}｜画幅 9:16 · 55-60s
> 发布联动：见变体头登记块 ｜状态：制作中 → 待 M4

---
母稿= data/drafts/{MASTER}
选题号= {TOPIC}
平台= {PLATFORM}
栏目人设= 待 CEO 点名（A 超体日志 / B AI 打工实录 / C 一人集团）
AIGC 标识= 文案声明 + 平台标识开关（双落）
GATE= PENDING
---

## 口播全文（约 220-240 字 ≈ 55-60s）

（待填充）

## 分镜提示

| 时间 | 口播段 | 画面 | 字幕/特效 |
|---|---|---|---|
| 0-3s | 钩子 |  |  |

## M4 前置自检清单（发布时逐项执行）

- [ ] 口播承诺 vs 内容交付对表（无标题党）
- [ ] 来源=母稿来源清单逐条对账
- [ ] AIGC 显著标识：视频内声明+平台开关
- [ ] 脱敏审：画面无密钥/无内部路径/无未公开数据
- [ ] 时长以 draft_lint 实测为准（≤60s）

## GATE

GATE: PENDING（发布前置门未过——账号未开；M4 机审+人审于发布前执行）

[v-generic]
# {DATE}-{TOPIC}-{PLATFORM}-v{VER}

> 变体（M3）｜母稿= data/drafts/{MASTER} ｜选题 {TOPIC}
> 状态：制作中 → 待 M4

---
母稿= data/drafts/{MASTER}
选题号= {TOPIC}
平台= {PLATFORM}
栏目人设= 待 CEO 点名（A 超体日志 / B AI 打工实录 / C 一人集团）
AIGC 标识= 文案声明 + 平台标识开关（双落）
GATE= PENDING
---

## 平台规格（自 variant-templates.md §3 套用）

{SPEC_BLOCK}

## 内容

（待填充——按上方规格与母稿同源派生）

## M4 前置自检清单（发布时逐项执行）

- [ ] 标题承诺 vs 内容交付对表（无标题党）
- [ ] 来源=母稿来源清单逐条对账
- [ ] AIGC 显著标识按平台规则双落
- [ ] 脱敏审：无密钥/无内部路径/无未公开数据

## GATE

GATE: PENDING（发布前置门未过——账号未开；M4 机审+人审于发布前执行）
