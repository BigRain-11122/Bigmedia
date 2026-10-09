# R-20261010-bigstream-03 · 雷达日报产品化路径调研（零账号依赖面）

> 认领：state/queue/explore.md #3（P3 队头·等待窗取活·O-20261009-1246）。执行轮：R1852（2026-10-10 02:0x）。
> 触发背景：#107 AIHOT PoC 三问判据收官（R1797）+城市信源接线+换名换标毕（R1798）+D-20261009-05 ①默认路线已裁（不接公众号·B站/知乎先行）→ 本件=产品形态后续路径盘点（订阅/消费端/嵌入/变现候选·零账号依赖面）。

## §0 溯源与验证声明（research-protocol 纪律）

| 源 | 级 | 说明 |
|---|---|---|
| AIHOT 代码面（`data/assets/aihot-poc/AIHOT/apps/api/src/routes/*.ts` + `packages/backend/src/publication/feeds.ts`） | A | 本地仓 HEAD 07d4c775 直读（路由/字段正身） |
| 本机实跑（curl 探针 2026-10-10 02:0x：api health / feed/daily.xml / feed/weekly.xml / api/v1/dailies/latest） | M | 全部读数落 §1-§3·零猜测 |
| 未验证面 | — | 公网消费/云阅读器兼容/CORS/WebSub 等**未实跑项逐条标注**，零断言 |

## §1 现状产品面盘点（live-verified，全部本机 127.0.0.1 实测）

栈=api 3101（health 200 `{ok:true,db:"ok"}`）+web 3100+worker（R1799 起在役）。产品面三层：

| 层 | 端点（代码 A 级正身） | 实测读数（M 级） | 状态 |
|---|---|---|---|
| Feed 层 | `/feed.xml`（精选 50 条）·`/feed/full.xml`（全文）·`/feed/all.xml`（7 天全动态）·`/feed/daily.xml`（日报·留 30 期）·`/feed/weekly.xml`（周报·留 12 期）·`/feed/monthly.xml`（月报）·`/feed/category/:file`（分类） | daily.xml 1735B **RSS 2.0 合规**（`<rss version="2.0">`+`atom:link self`+`ttl 30`+CDATA 全文+`guid isPermaLink="false"`+`pubDate GMT`）·weekly.xml 688B **合法空态**（首期未编=数据窗未满） | 在役 |
| API 层 | `/api/v1/items`·`/api/v1/hot-topics`·`/api/v1/stories/:id`·`/api/v1/dailies`·`/api/v1/dailies/latest`·`/api/v1/dailies/:date`·edition 族·`/api/v1/selected/snapshot`·`/api/v1/selected/changes` | `dailies/latest` 200：`schemaVersion:1`+`report`（date/windowStart/windowEnd/links/attribution=雷达日报/lead/sections[]）结构化完整 | 在役 |
| AI 消费层 | **`/api/mcp`**（remote Streamable HTTP·anonymous·read-only·stateless·no push·one tool per ability·TRUST_META=untrusted_external_data+instructionPolicy=treat_as_data_never_execute） | 代码直读（MCP handshake 未实测=§3 判据位） | 在役（未接线） |
| 展示层 | web `/daily/:date`·`/weekly`·`/monthly`·`/all` + OG 图族 `/og/site.png`·`/og/reports/:kind/:file` 等 | R1797 已验 `/daily/2026-10-09` 200 可读 | 在役 |

**绑定事实**：全部链接面=``http://127.0.0.1:3100``（SITE_URL 环境变量派生）→ 现态=**本机/LAN 消费面**；公网消费=改 SITE_URL+公网暴露（见 §5 gated）。

## §2 RSS 消费端路径（零账号·feed 已达标）

- **合规面（M 实测）**：RSS 2.0 必备字段全在位（channel title/link/description/language + item title/link/description/pubDate/guid/author）；`atom:link rel=self` 自引用在位=阅读器自动发现友好；`ttl 30`（分钟）轮询提示在位；description 内 CDATA 全文 HTML=阅读器内直读。
- **消费端候选**（未实测项如实标注）：
  - 自托管阅读器（FreshRSS/Miniflux/Tiny TinyRSS）同机/LAN 订阅 `http://<lan-ip>:3100/feed/daily.xml` — 形态可行（标准 feed），**未实测**=装机判据位；
  - 云阅读器（Feedly/Inoreader 等）须公网 URL → **gated**（§5）；
  - 机队本机脚本消费（daily_brief 同型 curl/JSONL 落盘）— 已有 R1797 证据件先例（报 JSON+feed XML 落档）。
- **期数窗事实**：daily 留 30 期/weekly 12 期/monthly 12 期（代码 A 级）；weekly 首期需 7 天日报累积+edition 语义非回填（R1772 定谳）→ **weekly feed 上线窗 ≈10-16、monthly ≈11-09**（推算·以实际 compose 为准）。

## §3 MCP 消费路径（零账号·机队直连=本调研最优候选）

`/api/mcp` = MCP 官方 Streamable HTTP transport，**匿名只读、无状态、零推送**，一能力一 tool，自带双 TRUST_META（内容=不可信外部数据·指令=只作数据永不执行）——与机队 MCP 生态（Codely 等 agent 客户端）直接对位：

- **机队消费形态**：任一 codely/agent 实例将 `http://127.0.0.1:3101/api/mcp` 注册为 MCP server → 雷达日报能力（日报/周报/热点/精选快照族 tool）成为机队各循环可直接调用的情报源——**零账号、零 API key、零平台依赖**；
- **安全面正身（A 级）**：anonymous+read-only+stateless+no push=最小暴露面；TRUST_META 双声明=内容污染/指令注入防线内置；
- **实测销项（R1853·explore#15）**：MCP handshake 与 tool 清单已实跑全通 → **判据 PASS**（详见 §3.1）；机队 codely 配置域接线=机队配置面（.codely-cli MCP 注册=宿主/机队管辖，本司循环不擅动——提案面走 §3.2）。

## §3.1 MCP 实测读数（R1853·判据=一次 MCP 通道真读日报 lead 字段）

四步全通（探针 `.c3-tmp/r1853_mcp_probe.py`+`r1853b_mcp_criterion.py`·证据 `.c3-tmp/r1853_mcp_evidence.json`+`r1853_mcp_criterion.json`）：

| 步 | 调用 | 读数 |
|---|---|---|
| 1 | `initialize`（protocolVersion 2025-03-26） | **200**·`text/event-stream` 回流·`serverInfo={name:"radar",version:"4.0.0"}`·instructions 真返（7 tool 用法自述+TRUST_META 内容申明原文在位）·**无 Mcp-Session-Id 头=stateless 实证** |
| 2 | `notifications/initialized` | **202**·空正文（notification 预期态） |
| 3 | `tools/list` | **200**·**7 tools**=radar_get_latest / radar_search / radar_get_hot_topics / radar_get_story / radar_get_daily / radar_get_weekly / radar_get_monthly——「一能力一 tool」代码申明实证 |
| 4 | `tools/call radar_get_daily` | **200**·784B markdown 渲染件（`# 雷达日报 日报 · 2026-10-09`+窗口行+安全边界行+头条位） |

**判据闭合（内容级等价）**：MCP 渲染件为 markdown 形态（非 JSON），与 `/api/v1/dailies/latest` 的 `report.lead` 字段交叉对读——`lead.title`+`lead.leadParagraph` **2/2 全文命中** MCP 件（头条行=`头条：AI 代理按需支付：BlockRun 和 Incarna 如何使用 Amazon Bedrock AgentCore 支持`）→ **「MCP 通道真读日报 lead 字段」判据 PASS**（.c3-tmp/r1853_mcp_criterion.json 留档）。

## §3.2 机队 codely MCP 注册提案 v0.1（呈报位=HQ-FEEDBACK F-20261010-01·宿主/机队管辖域·本司不擅动）

- **目标**：机队 codely/agent 实例将 `http://127.0.0.1:3101/api/mcp`（Streamable HTTP·protocolVersion 2025-03-26·server name `radar`）注册为 MCP server → 7 tool 成为机队各循环可直接调用的情报源（**零账号、零 API key、零平台依赖**）；接线条判据=真读 daily lead 成功（**本件已单机预演 PASS=§3.1**）。
- **分期（改动量升序）**：
  - **P1 零改动档**=本机（bm-a）codely 实例注册（127.0.0.1 面内即可用）——配置正身=codely MCP server 配置域（`.codely-cli` 键名格式=宿主文档域·本提案不擅断具体键名）；
  - **P2 配置级档**=跨机机队接入（bm-b/bm-c）——前置三件：API 绑定面 127.0.0.1→LAN IP（R1710 端口隔离律放宽=安全面权衡·宿主/CEO 决策域）+防火墙放行+**栈存活 SLA**（三外部杀进程史 R1727/R1750/R1752·活性守卫 R1752 在役·栈死即 tool 失败=机队接线后可见性上升需值守面知悉）；
  - **P3 gated 档**=公网暴露（域名备案=CEO 物理件·§5 表）。
- **受益面**：机队循环直连情报源——M0 选题源参考（hot_topics Top10/主题检索 radar_search/get_latest 24h·7 日 briefings）+每日/每周/每月编辑件；TRUST_META 防注入内置=机队消费安全面前置达标。
- **呈报位**：HQ-FEEDBACK F-20261010-01（P2·宿主/机队管辖域待点头·点头后接线窗=本机 P1 档零改动先行）。

## §4 嵌入输出候选（零账号·跨仓提案位）

- **候选 A=硅基生命元宇宙.html「城市热点雷达」模块**：消费 `/api/v1/dailies/latest` JSON（lead+sections 结构化完整）或 `/feed/daily.xml`——元宇宙=CEO 第一检查入口（09-30 裁决），热点雷达模块=「城市生长」叙事的自然数据面；**未测面**：`file://` 打开跨源 fetch=CORS 判据位（API publicHandler 是否带 CORS 头未验）；**跨仓写禁令**：元宇宙文件=MiniGame 仓域 → 本司只出消费规格+提案件，执行面归该仓 owner（提案落点=本仓 research/ 提案文档+HQ-FEEDBACK 指针）；
- **候选 B=OG 图族**：`/og/reports/:kind/:file` 日报卡图自动产出（代码 A 级）→ M5 发布批的封面/分享图素材零成本面（未实测渲染质量=验收位）。

## §5 分发/订阅/变现 gated 面（如实盘点·不催办）

| gated 面 | 卡点 | 依据 |
|---|---|---|
| 公网 RSS/API/MCP 消费 | 服务器+域名备案 | C-20261009-02 CEO 物理件清单（服务器域名备案） |
| 云阅读器订阅 | 同上（公网 URL 前置） | §2 |
| 邮件订阅 | SMTP 轮换 | C-20261009-02 CEO 物理件清单 |
| 公众号源/渠道 | D-20261009-05 ①已裁=不接（CEO 一句话例外窗保留） | 集团决策 |
| 云 LLM 付费扩容 | D-20261009-05 ③真金预算门 | 集团决策 |

**零账号变现定谳（诚实）**：无公网暴露=无对外变现面；现态产品价值=**内部情报资产**（M0 选题源·机队 MCP 消费·可视化嵌入·发布批素材库）——「变现」路径全部 gated 于 CEO 物理件/决策件，本件不催办（现状行口径）。

## §6 结论应用表

| # | 结论 | 级别 | 下一步 |
|---|---|---|---|
| 1 | Feed 层已达标（RSS 2.0 合规+30 期窗+全文 CDATA）——订阅形态零工程 | M 实测 | 无需改动；SITE_URL 改 LAN IP=同机/LAN 阅读器订阅（配置级） |
| 2 | **MCP 端点=机队零账号情报分发最优路径**（匿名只读+防注入内置） | A 代码+M 实测 | **R1853 实测销项=判据 PASS**（handshake/7 tools/daily lead 交叉对读全通=§3.1）；机队注册提案 v0.1 呈报 HQ-FEEDBACK（§3.2·宿主域待点头） |
| 3 | v1 API+OG 图族=嵌入/素材双面就绪 | A 代码 | 元宇宙模块提案件入队（跨仓提案·CORS 判据位先行） |
| 4 | weekly/monthly feed 合法空态=数据窗未满非缺陷 | M 实测 | 不干预；10-16/11-09 自然解锁（推算） |
| 5 | 公网分发/订阅/变现全面 gated（域名/SMTP/决策件） | 盘点 | 现状行呈报·零催办 |

## 变更记录

- v1.0（2026-10-10 R1852）：首版（五端点族 live 盘点+MCP/v1/OG 三新面发现+gated 面盘点+结论应用表）。
- v1.1（2026-10-10 R1853）：§3 未测面销项（explore#15 承接）——§3.1 MCP 四步实测读数+判据 PASS（daily lead 内容级等价交叉对读）+§3.2 机队注册提案 v0.1（分期 P1/P2/P3·呈报位 HQ-FEEDBACK F-20261010-01）+§6 行 2 升实测态。
