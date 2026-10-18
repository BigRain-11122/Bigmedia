# BigStream 司流程清单·批一机制面（C-20261018-02 执掌席供证）

> 供证律=C-20261018-02 §二.1 schema 现读（源=docs/os-protocol.md v1.14 全文实读+docs/capabilities.md C 册 C-01~C-52 行实读+schtasks 三任务 2026-10-18 12:2x 实测+state/queue 三队现读+iteration_loop.ps1 现读 L1-158）；裁决权归委员会，本件零新法零裁决（§二 B 型活口一项=按案 §二.2 证据+裁决提案呈报）。
> 落点律：本件=本仓 docs/ 供证件（跨仓写禁令执法=不写 cph4 案表）；HQ-FEEDBACK 回执一行随批二交付轮落（24h 窗内·案 §四）。
> 批面拆分：批一=机制面（本件）；批二=产线面（M0-M5 七站+评审链+四内容线·下窗交付）。

## §一 机制面流程总清单（每流程一行·案 §二.1 律）

| ID | 流程 | 执掌席 | 触发节律 | 写入资源面 | 依赖面 | 预算与产出账 |
|---|---|---|---|---|---|---|
| BS-M1 | OS 自迭代轮（BigStream-OSLoop） | 工程技术部（循环席执行） | schtasks BigStream-OSLoop **PT10M 实测**（任务级帽 35min 实测；体内预算=25min 墙钟——B 型活口见 §二.1） | src/os/state.json（ts/task/tick/log）+git commit/push+logs/iteration-loop/*（gitignored 运行时排气） | round.lock（D-20260925-03：PID 判活+CreateNew 原子+1.2x 缓释+40min 硬帽）+MultipleInstances=IgnoreNew+API 503 风暴预闸（C-20261015-03 tech#205）+cloud-cap 让路 defer 窗（C-20261015-03） | ~25min/轮·产出=轮 log+按序取活交付件 |
| BS-M2 | state 收账面（finalize_state 单一写手） | 循环席 | 每轮收账步 | src/os/state.json——禁手写 json.dump（tech#149 强制律：前缀校验+task 60 字例+tick 守卫） | src/os/close_commit.py 正身 | 零 token·产出=机读心跳面（fleet-audit 判活直读·ts/task 顶导字段） |
| BS-M3 | status-export 刷新（P-61 导出步） | 循环席 | 每轮收账·export_ts ≤24h 新鲜度闸 | docs/status-export.json——禁手写（tech#148：一律 export_refresh 正身或 close_commit export 参数·rc=2 拒写守门） | export_refresh.py+close_commit | 零 token·产出=CEO 过程可见三行（当前活/最近实物/下个里程碑） |
| BS-M4 | 集团转办/决策消费（group_scan 六面一体 C-35） | 循环席 | 每轮轮首（D-20260930-19 SLA：新行 ≤2 轮周期 ≤20min ack） | state.json decisions_watermark（dnums 内容寻址差集·D-20260930-18 禁纯行数比对）+log/commit ack 行（P-51 双载体：行号+轮号+下一动作） | 集团仓只读消费正典（D-20261001-03：fetch+git show origin/main:path·禁 working-tree pull）+origin-delta anchor 内容引用律（tech#165） | 探针零 token·产出=新令/决策消费闭环 |
| BS-M5 | origin 差集前置查（origin_gap_check） | 循环席 | 每轮快速判定前置位（R1500 根修位） | 无（只读探针·FAIL=新令类破静转全任务书） | git fetch+origin refs | 零 token·产出=origin-only 新令零漏检（R1496 push 拒收事故根治面） |
| BS-M6 | 三探针（board_check C-08/readiness C-19/loop_health C-20） | 工程技术部 | 每轮（消费面=loop_health --loop+readiness --summary 紧凑面·全量面=审计用不废弃） | 无（只读·FAIL 如实入账不阻断） | 台账族（ideas/drafts/renders/GATE/state/queue） | 零 token·产出=台账一致性/首发阻塞/循环健康三面读数 |
| BS-M7 | 三队队列系统（state/queue main/tech/explore） | 循环席 | 按序取活（P1 backlog 顶行→P2 tech 队头→P3 explore 队头·真 gated 项跳过）+轮末补货步 ≥1 条 | state/queue/*.md（done 标日期回写·行首 done 标记前移律 tech#184·队头判定一律 queue_status --item 禁截断 dump） | src/os/backlog.md 一法一册指针 | 零 token·产出=无活可干时的自驱取活面（O-20261009-1246 轮引擎） |
| BS-M8 | 情报日报（daily_brief C-23） | 选题研究部 | 每日一份（当日缺=任意轮先补产铁律·重跑=当日最新真相） | data/intel/daily/YYYY-MM-DD.md | B站热门 API+知乎热榜 API（零 key 零 token·带 UA 实测通） | 零 token·产出=20 条双源热榜（REACT M0 供给源） |
| BS-M9 | 周自审（self_audit C-25） | 总裁办公室（循环归口执行） | 每周一期 ISO 周（当周缺=任意轮补产） | docs/audits/packs/<ISO周>-pack.md+docs/audits/<ISO周>-self-audit.md | 三探针+台账族+git log | 零 token 数据包+一轮判读·产出=判读五清单周报告（深审=CEO 令触发不每周） |
| BS-M10 | 全球基准面 7 日刷新（P-56） | 循环席 | docs/global-benchmarks.md §④ 首行 >7 天=刷新轮（采集 ≤15min 限时律·零 key 优先） | docs/global-benchmarks.md §①/§④ 各追加一行 | 外部锚源分级 A-D/M（research-protocol） | ≤15min·产出=基准面保鲜 |
| BS-M11 | AIHOT 栈自愈+日报链（watchdog C-48+aihot_procs C-47） | 工程技术部 | schtasks BigStream-AIHotWatchdog **PT5M 实测**（watchdog-state pause 旗让路面：R2309 复役·CEO 用机窗 pause 设计内） | data/pipeline/aihot-watchdog-state.json+data/assets/aihot-poc/+AIHOT 日报 compose（daily:YYYY-MM-DD catch-up） | apps/worker+apps/api 进程拓扑探测+LLM 面=bm-a:8090 brain（CEO 让路 pause 态 2026-10-17T22:51 起·CoderServe Disabled 设计内） | 零外部 API·产出=栈存活自愈（PT5M heal）+日报出刊（judged>0 即刊） |
| BS-M12 | 集团巡逻承载（HQ-Patrol-BigStream） | 集团巡逻面（Tools/patrol-fleet-carrier.ps1 -Code bigstream·U060 静默链） | schtasks HQ-Patrol-BigStream **PT30M 实测** | 集团 patrol 通道（本司=被巡对象·本司零写面） | 集团 Tools 任务族 | 零本司成本·产出=集团对司巡逻闭环（PATROL-FLEET 十域扫） |
| BS-M13 | 会话级 durable cron 面 | —（现读=零在册） | —（会话级 cron 随窗死=死线单盯守必须活窗承载·CEO 盯守自严律） | 无 | 无 | D 型查面：旧夜审 cron 族本司零残存（schtasks 现读三任务全在册无孤儿·案卷行 4 同查面 ✓） |

## §二 成对冲突扫描（机制面·案 §一 A/B/C/D 逐对过）

### 二.1 B 型活口一项（本轮新发现·案 §二.2 证据+裁决+修法+防复发闸全四件）

| 冲突对 | 型 | 证据（现读实锚） | 裁决提案 | 当窗修法 | 防复发闸 |
|---|---|---|---|---|---|
| iteration_loop 25min 墙钟 vs 正当长轮（案卷行 2 同源·**本司腿**） | B | 本仓 src/os/iteration_loop.ps1 现读：L21 `[int]$RoundTimeoutMinutes = 25`+L129-147 `WaitForExit(25*60*1000)`→`ROUND TIMEOUT after 25min - killing headless process tree`（墙钟击杀·不问输出活性）；集团 10-18 根治三件套（活性门控预算=连续 25min 零输出静默门+240min 硬顶·击杀仅凭证据）只落 BM 仓 945c3f60·本仓发射器未承 | 采纳集团正典 iteration_loop v2 活性门控预算（BM 仓 945c3f60 范式只读移植）·schtasks 任务级 35min 帽同步抬至 >240min（长轮存活面） | **tech#217 已落队**（state/queue/tech.md·下轮即领）·发射器每发火从盘重读=改盘即生效零重装 | 移植后=墙钟击杀路径退役断言+长轮跨 25min 零墙钟杀实证窗（对照 BM 案卷 TIMEOUT 清账族计数）+loop_health 锁龄线随升注记 |

### 二.2 已治族注记（存量已知·如实入行）

- **A 型·state.json 多写者**（OSLoop finalize_state 单一写手 vs pulse 槽级刷 vs bm-a 交互窗共享工作树）：治理在册=tech#149 单一记账写手+并窗期 `M src/os/state.json`=自记账预期态豁免+多窗显式列文件纪律（R19/R39 插队 commit 实锚）+pulse-only 零 tick/log 接触（os-protocol v1.14 心跳 pulse 律）✓
- **A 型·capabilities.md 多写者**（循环升表 vs 交互会话升表）：同 R19/R39 族·收账显式列文件纪律在册 ✓
- **B 型·loop_health 历史读数 4F**：B 型历史已治族注（tech#215 log-order 压噪+adjudicated-pair fold·R2353 落·tech#214 写时防线）✓
- **C 型·临时件轮末清理钩 vs 在飞批中间件**：批未闭不预补账（R35/R144 先例）+批闭收账（R150 先例）+renders tmp 声明行制——本轮活例=tech#216 交付件 11:22 落盘未 commit（C-52 册行同批滞留）→本轮 214 测试验证后随批一 manifest 收口=清理钩执法闭环 ✓
- **D 型·idle-fast 快速路径 vs 现行空轮判定路径**：idle-fast 空转路径全司废止已注记（P-2026-09-28-02 ②·os-protocol v1.11+任务书同步）=closed 先例 ✓
- **D 型·旧夜审 cron 族**：本司 schtasks 三任务全在册（OSLoop/AIHotWatchdog/HQ-Patrol）·零孤儿零残存 ✓

### 二.3 D-20261018-01 复役看护随查（案批注面）

本司三 schtasks 现读全 **Enabled**（12:2x 实测·下次运行时间均在档）——全司任务 Disabled 复犯面本司读数=0 ✓

## §三 O-025 四标高效复核带（机制面·批一）

- **顺畅**：五查快速判定省重读 token（判定面保留·响应性不降）+三探针紧凑消费面（--loop/--summary/queue_status --item）
- **高效**：例行全脚本零 token（探针/周报/台账核验）·判断=模型最小必要·tokens:local 计量探针（C-33）在役·外部 API 仅调研令/CEO 授权
- **简洁**：一法一册一账（dept-review 合一 R151·指针制·单一真相律）·记账预算 ≤5 处/轮·空轮一行声明收轮·纯规则章程类 md 停产
- **先进**：内容寻址水位（D-18）+机读心跳面 ts/task（v1.10）+原子抢锁（D-20260925-03）+活性门控预算（**本司腿=tech#217 落位后承**）+fire_consume 原子通道（C-45）
- **成本账**：机制面全程 CPU 轻面零外部 API（edge-tts=免费接口+piper 纯本地备份线在案）；本轮机制面供证成本=一轮 CPU 面内（现读+写件+收账）

## §四 批二预告（产线面·窗至 10-19 ~11:3x）

产线面流程清单（production-chain M0-M5 七站+dept-review 评审链+四条内容线〔L-卡/audio/drama/短切片〕+meme 线停用态〔O-20261017-1741〕+MV 查看位面〔执行认领制·mv 会话域零接触律〕）+产线面成对冲突扫描+四标带——源=production-chain v2.5+dept-review-mechanism v1.7+expert-roster v1.2+各线 charter 现读；HQ-FEEDBACK 回执一行随批二交付轮落。

## §五 验证声明

本件全部源面 2026-10-18 12:1x-12:4x 现读（os-protocol 85 行全文/capabilities C 册行/iteration_loop.ps1 L1-158/schtasks 三任务 verbose 实测/三队现读）；B 型活口证据=文件行号级实锚非记忆复述；零推测成分；裁决权归委员会（本件=供证非自裁）。
