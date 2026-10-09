# R-20261010-bigstream-04 硅基生命元宇宙「城市热点雷达」嵌入模块提案件 v1.0

> 立项三问（P-65）：①**为什么现在**=CEO 第一检查入口=硅基生命元宇宙.html（2026-09-30 反馈令「可视化」专指此件·每次检查应有可见进步）·本司「雷达日报」自托管栈三问判据已收官在役（backlog #107·R1797）且产品化路径定谳=现态内部情报资产（R-20261010-03 §5）——嵌入模块=把本司产线成果放进 CEO 第一眼看到的位置·零账号零 key 零平台依赖；②**落地承接人**=MiniGame 仓 owner（元宇宙文件=MiniGame 仓域·跨仓写禁令·本司只出件=探针读数+消费规格+提案指针）；③**验证声明**=全部读数来自 2026-10-10 02:2x 真跑探针（证据件 .c3-tmp/r1854_cors.json+r1854_latest.json+r1854_probe.py 入 git）·零断言无锚·判负面（live-fetch）如实入件。

## §1 判据预注册（explore#16 原文口径）

- **J1** API CORS 头实测（publicHandler 判据位）：GET 带 Origin / OPTIONS preflight / Origin:null 三面 → Access-Control-Allow-Origin 有无定谳。
- **J2** 消费规格文档：dailies/latest 字段映射 + 模块版式建议。
- **J3** HQ-FEEDBACK 提案指针行（owner/CEO 域待点头·零催办律）。

## §2 J1 CORS 实测读数（2026-10-10 02:2x·栈活性前置核过：/api/health 200 {ok:true,db:ok}）

| 探针 | 状态 | Access-Control-Allow-Origin | 备注 |
|---|---|---|---|
| GET /api/v1/dailies/latest + `Origin: http://localhost:5500` | 200 | **无** | Vary=Accept-Encoding·无 ACAO/ACAH |
| OPTIONS preflight（Origin+ACRM:GET） | 204 | **无** | Hono 路由 204 自动响应·无 CORS 头 |
| GET + `Origin: null`（file:// 打开场景） | 200 | **无** | 同上 |

**定谳：v1 公开 API 无 CORS 支持**——浏览器跨源 fetch 必被同源策略拦截 → **live-fetch 嵌入路径判负**（不改 AIHOT 服务端源码前提·改源码=上游 fork 面非本司域非本件射程）。

**附注（网络面第二门）**：栈三端口全绑 127.0.0.1（端口隔离律·R1710 起站纪律）→ 即使 CORS 开放，非 bm-a 本机打开元宇宙页时 API 亦网络不可达 → live-fetch = **双重不可行**（CORS 门 × 网络门）·结论对元宇宙消费场景（任意机器/任意打开方式）稳健。

## §3 推荐路径定谳：静态快照数据件模式（唯一可行正路）

- **同构先例**：元宇宙既有「硅基生命元宇宙-data.js」独立数据件模式（2026-09-30 反馈令原文「数据件=同目录 硅基生命元宇宙-data.js」）→ 雷达快照数据件=同一模式的第二个数据源，owner 侧零新模式学习成本。
- **双免机制**：`<script>` 标签加载=免 CORS（script 不受同源策略约束）+ 快照随 git 分发=免网络依赖（任何机器打开元宇宙都能渲染当日快照）。
- **生成器**：python zero-key 脚本（**附录 A 全码**·读 /api/v1/dailies/latest → 渲染 `window.RADAR_DAILY = {...}` JS 数据件·~50 行·无第三方依赖）。
- **刷新节律建议**：08:00 compose 出刊后每日一次（MiniGame OS 循环与本栈同宿主机 bm-a·API 本机可达可直接跑生成器；跑批责任归 owner 侧排程域）。
- **红线对位四条**：①无来源不发布=快照保留每 story 的 source.name+links.original（红线消费位字段现成）；②AIGC 显著标识=模块署名行「雷达日报 · AI 生成内容」（attribution.name 字段逐条在）；③脱敏/两态声明=本模块=纯转述无虚构（REACT 两态声明不适用）·底部行标注「基于公开热榜的 AI 生成内容」；④内网锚点清洗=生成器剥离 links.aihot/attribution.url（127.0.0.1 链接不入对外可见数据件·只留 links.original 原文链接）。

## §4 字段映射表（/api/v1/dailies/latest 真返回 → 模块字段·2026-10-09 期实锚）

| API 路径 | 类型 | 模块用途 | 版式建议 |
|---|---|---|---|
| `report.date` | str | 日期徽 | 头行「YYYY-MM-DD · 城市热点雷达」 |
| `report.generatedAt` | ISO8601 | 更新时间戳 | 底部署名行 |
| `report.lead.title` | str | 头条标题 | 头条区 H2 级 |
| `report.lead.leadParagraph` | str | 头条摘要 | 头条区正文段（≤3 行截断） |
| `report.sections[].label` | str | 分节标题 | 当前期单节「产品发布/更新」·多节纵列 |
| `report.sections[].items[].title` | str | 故事卡标题 | 卡片题行 |
| `report.sections[].items[].summary` | str | 故事卡摘要 | ≤2 行截断·hover/点击展开 |
| `report.sections[].items[].source.name` | str | 来源角标 | **红线消费位**（无来源不发布） |
| `report.sections[].items[].links.original` | str | 原文外跳链接 | 卡片点击位 |
| `report.attribution.name` | str | 模块署名 | 「雷达日报」+AIGC 标识行 |
| `report.flashes[]` | list | 快讯位 | 当前期空数组=**模块必须处理空态** |
| `schemaVersion` | int | 快照版本字段 | 向后兼容判据位 |
| 空态（date 缺报） | — | 「今日雷达未出刊」占位 | **禁假数据**（诚实空态律） |

## §5 模块版式建议（owner 版式域最终定夺·此处仅建议）

- **嵌入位**：主界面侧栏/面板区一卡位（与既有模块同高）；标题行「城市热点雷达」+日期徽。
- **内容栈**：头条区（title+lead 段）→ 分节故事卡列表（建议 ≤5 卡·每卡=题+来源角标+点击外跳）→ 底部署名行（雷达日报 · AI 生成内容 · 更新时间）。
- **风格**：沿用元宇宙既有「一套日漫化风格+分区调色板+统一自发光信息层」（美感同族律 M9/M15·city-storylines-charter §3 承继）——模块不自立第二画风。
- **交互**：卡片点击=links.original 外跳；无报日渲染空态占位。

## §6 结论应用表

| 行 | 结论 | 承接 |
|---|---|---|
| 1 | CORS 无 ACAO+127.0.0.1 双门 → live-fetch 判负留痕 | 本件 §3 快照路径=唯一可行正路 |
| 2 | 消费规格+生成器附录 A | **MiniGame 仓 owner**（HQ-FEEDBACK F-20261010-02 指针行·点头即接·执行面归其仓域） |
| 3 | 快照生成器落件（tools/radar_snapshot_gen.py+单测） | tech 队新项（gated owner 点头）·判据=生成器真跑出 JS 件+owner 侧模块渲染 PASS |
| 4 | owner 侧 agent 化刷新替代通道 | MCP 端点提案在册（F-20261010-01·radar_get_daily 7 tools 族·已判据 PASS）双提案互补 |

## 变更记录

- 2026-10-10 02:2x R1854 v1.0 首建（explore#16 交付件·判据 J1/J2/J3 全落·探针 r1854_probe.py 四探针+字段 dump 真跑）。

---

## 附录 A 生成器参考码（python·zero-key·无第三方依赖）

```python
# -*- coding: utf-8 -*-
"""radar_snapshot_gen.py -- /api/v1/dailies/latest -> RADAR_DAILY JS data file (metaverse embed).
Usage: python radar_snapshot_gen.py --out <MiniGame repo>/radar-daily-data.js
"""
import argparse, io, json, urllib.request

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default="http://127.0.0.1:3101")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    with urllib.request.urlopen(a.api + "/api/v1/dailies/latest", timeout=10) as r:
        data = json.loads(r.read().decode("utf-8"))
    rep = data.get("report") or {}
    sections = []
    for sec in rep.get("sections", []):
        items = []
        for it in sec.get("items", []):
            items.append({
                "title": it.get("title"),
                "summary": it.get("summary"),
                "source": (it.get("source") or {}).get("name"),
                "original": ((it.get("links") or {}).get("original")),
            })
        sections.append({"label": sec.get("label"), "items": items})
    payload = {
        "schemaVersion": data.get("schemaVersion"),
        "date": rep.get("date"),
        "generatedAt": rep.get("generatedAt"),
        "attributionName": (rep.get("attribution") or {}).get("name"),
        "lead": rep.get("lead", {}),
        "sections": sections,
        "flashes": rep.get("flashes", []),
    }
    js = "// generated by radar_snapshot_gen.py (BigStream R-20261010-04) -- AI-generated content\n"
    js += "window.RADAR_DAILY = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n"
    with io.open(a.out, "w", encoding="utf-8") as f:
        f.write(js)
    print("WROTE", a.out, "date=", rep.get("date"))

if __name__ == "__main__":
    main()
```
