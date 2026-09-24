# BigStream 自迭代协议（OS Protocol）

> CEO 令 O-20260923-1525-bm-a：「先开工底层和功能，建立规则，自我迭代，不要进行生产」。
> 本协议=OS 循环的结构与法规。任务书=`src/os/iteration_prompt.txt`（每轮必读·外置 UTF-8）；状态账本=`src/os/state.json`；任务板=`src/os/backlog.md`。
> 级别：T2 机制（AI 直接落地·7 天否决窗，同集团 cph4/evolution.md 分级立法）。

## §1 结构（四件套）

| 件 | 路径 | 职责 |
|---|---|---|
| 注册器 | `src/os/register_loop_task.ps1` | Windows 任务 `BigStream-OSLoop` ·10 分钟/轮 ·幂等可重跑（自愈用） |
| 启动器 | `src/os/iteration_loop.ps1` | 每轮：锁检查→无头 spawn 一轮 codely→心跳→25 分钟预算超时击杀 |
| 隐身器 | `src/os/InvisibleRunner.vbs` | 计划任务永不弹窗（U060 同源纪律） |
| 任务书 | `src/os/iteration_prompt.txt` | UTF-8 中文 mandate——编码律：.ps1 纯 ASCII，中文只进数据件 |

触发链：OS 计划任务 → wscript 隐身 → powershell 启动器 → `codely -y -p <任务书>`（工作目录=本仓根）。
装法（自愈/新机同一条命令）：`powershell -NoProfile -ExecutionPolicy Bypass -File src/os/register_loop_task.ps1`
心跳/日志：`logs/probe-heartbeat.txt` + `logs/iteration-loop/`（gitignored·运行时排气；账本证据走 state.json 与 git log）。
选型依据：会话内 durable cron 只在 CLI 开窗时空转（BigMoney 实证 8.8 小时零跳动）——OS 级任务是唯一无窗存活的 10 分钟通道。

## §2 每轮动作（以任务书全文为准）

读记忆 → 读 state → 取 backlog 顶行 → 干活 → 收账（tick+1 + commit + push）。空转=记 idle 即收轮。

## §3 优先级与禁区（体系优先阶段·O-20260923-1756-bm-a）

- 优先级：O-20260923-1756 模式修正（体系优先·测试生产）> 修红 > 底层功能 > 规则建设 > 台账维护。
- 边界：不量产生成（N=6 封存·启动须 CEO 令·机牢=`state.json` `production: paused`）；测试生产合法（单件过链 PoC·标「测试件·非成品」·不入发布队列）；发布（M5）须账号+M4 全绿；账号域永不代办；跨仓写禁令；P1 级只提案。

## §4 互斥与自愈

- 互斥：`logs/iteration-loop/round.lock`（40 分钟过期）+ 计划任务 `MultipleInstances=IgnoreNew`；同仓有活体在写（git 锁/状态异常）→本轮只读。
- 自愈：计划任务丢失→重跑注册器（幂等）；注册即点火（不等整点，首火=下一个 8 分钟边界）。

## §5 度量（诚实纪律）

- 循环健康判据：心跳时间戳间隔≤20 分钟（同机队通信 SLA）；state.json 的 tick 序列连续无空洞。
- 判据机器化（R17·C-20）：`python src/os/loop_health.py` 只读探针——心跳新鲜度/间隔（SLA 20 分钟=WARN 级·长轮次 25 分钟预算内静默合法；锁龄 40 分钟=FAIL 级停跳线）、tick↔完成轮次对账（账目滞后=FAIL·防 R4/R5 型断洞）、台账卫生（叙事时间戳乱序/缺行=WARN·近似分钟如 17:2x 合法）、backlog 燃尽率（info）。WARN=顾问级如实记录，不阻断循环。
- 未发生=未测量：循环自评只看 state.json/log 与 git 实况，禁自夸。

## §6 Token 面纪律（O-20260923-2241-bm-a「尽量调用本地工作流去减少token使用」）

- **路由三问**（同集团 local-first）：①能否脚本确定性完成（探针/周报/台账核验/规格门=纯脚本零 token）？②能否本地模型完成（Ollama/faster-whisper/FFmpeg=零 API）？③必须会话模型的最小必要面是什么？
- **空转快速路径**：空转轮禁全文档重读——四查（新令/任务板/树/锁）+三探针全静即一行收账（任务书【空转快速路径】节为准）；探针照跑=响应性不降，只省重读 token。
- **计量原则**：测量先行——本条生效前后，空转轮的轮次时长/操作步数对比入 state.json log（idle vs idle-fast 可分辨）。
- **外部 API 面**：web 采集/云端模型仅调研令或 CEO 明令授权时用；产线默认=本地栈四站；edge-tts=免费云端接口（piper=纯本地备份线在案）。

## §7 周期性自我审查（O-20260924-1057-bm-a「子公司建立起周期性的自我审查」）

- **节律**：每周一期（ISO 周）——**当周自审缺=任意轮补产**（与情报日报同款触发律）；数据包=`python src/os/self_audit.py`（自动采集零 token·探针/台账/测试/git 全量→`docs/audits/packs/<ISO周>-pack.md`），判读层=一轮填写周报告 `docs/audits/<ISO周>-self-audit.md`。
- **判读五清单**：①三维健康（团队/流程/资源·深审框架=`audits/2026-09-24-company-audit.md`）②机制漂移（可调 loop-engineer 专家）③效率平衡度量（dept-review §5 B5：评审轮次/件+催办行数）④上周整改项复查（闭环验证）⑤假设校准登记（未上线=未测量·只登记不结论）。
- **深浅分层**：周自审=结构化轻审（一轮预算内）；**全盘深审（如 O-1043 三维审计）=CEO 令触发**·不每周重复——审计不官僚化（O-2248 平衡律适用）。
- **续链**：跨期问题=整改项带 owner 入 backlog；**连续两期同一缺口=升级 PLAN §7 呈 CEO**。
- **集团耦合**：周自审早于周日集团进化轮完成（任意轮补产自然满足）——进化轮感知面可直接读本期报告。

## 变更记录

- 2026-09-23: v1.0 建立（CEO 令 O-20260923-1525-bm-a）。同批推翻 PLAN §8 原文「P3 后再装循环」——CEO 令优先。
- 2026-09-23: v1.1 模式切换——CEO 令 O-20260923-1602-bm-a 解除生产暂停，循环转复工主线（调研→人设→自主素材生产）；底线区（账号域/跨仓写/P1 提案制）不变。
- 2026-09-23: v1.2 模式同步——CEO 令 O-20260923-1756-bm-a 模式修正（体系建设优先·不量产·允许测试生产）；§3 优先级与边界随令更新；「不量产」落为机牢（`state.json` `production: paused`·make_draft 生产位拒稿·测试位照走）。
- 2026-09-23: v1.3 §5 判据长牙（OS 循环 R17）——新增 C-20 循环健康探针引用行；SLA 20 分钟（WARN）与锁龄 40 分钟（FAIL）分级明确；真跑 4 WARN 皆为在案史实（叙事时间戳漂移×2·R4+R5 修复行·R5 26 分钟长轮间隙）。
- 2026-09-23: v1.4 §6 Token 面纪律（CEO 令 O-20260923-2241-bm-a）——路由三问+空转快速路径（任务书同步增节）+计量原则+外部 API 面约束；10 分钟节律不降（CEO 亲令保持），空转轮省重读 token。
- 2026-09-24: v1.5 §7 周期性自我审查（CEO 令 O-20260924-1057-bm-a）——周一期+当周缺任意轮补产+数据包脚本零 token 先行+判读五清单+深浅分层（深审=CEO 令触发）+连续两期同缺口升级；首期 2026-W39 报告在案（深审=当日 O-1043）。
