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

## §3 优先级与禁区（底层优先阶段）

- 优先级：修红 > 底层功能 > 规则建设 > 台账维护。
- 禁区：**内容生产全停**（M0/M1/M2/M3）——解除须 CEO 令；账号域永不代办；跨仓写禁令；P1 级只提案。

## §4 互斥与自愈

- 互斥：`logs/iteration-loop/round.lock`（40 分钟过期）+ 计划任务 `MultipleInstances=IgnoreNew`；同仓有活体在写（git 锁/状态异常）→本轮只读。
- 自愈：计划任务丢失→重跑注册器（幂等）；注册即点火（不等整点，首火=下一个 8 分钟边界）。

## §5 度量（诚实纪律）

- 循环健康判据：心跳时间戳间隔≤20 分钟（同机队通信 SLA）；state.json 的 tick 序列连续无空洞。
- 未发生=未测量：循环自评只看 state.json/log 与 git 实况，禁自夸。

## 变更记录

- 2026-09-23: v1.0 建立（CEO 令 O-20260923-1525-bm-a）。同批推翻 PLAN §8 原文「P3 后再装循环」——CEO 令优先。
