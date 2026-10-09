# R-20261010-bigstream-01 · L-剧漫剧量产线节拍设计（MD-0001 单件全链实耗回测 → MD-0002+ 批量 SOP）

> 队列锚：state/queue/explore.md item 1（P3 队头·判据=单件机时读数）·R1849 交付。
> 数据源：backlog #108 R1782-R1795 注记行（MD-0001 全链实录）+ state log R1847（E4 争抢读数）+ tech#2/#7/#15/#18 在册定谳——零新断言，全部读数逐条锚在案。

## §1 MD-0001 单件全链实耗回测（实测读数表）

| 腿 | 轮 | 实测读数 | 性质 |
|---|---|---|---|
| 剧本+分镜一体化（qwen3.5:9b-16k 原生 API think=false） | R1782 | **24.6s / 1117 tok 一次过**（前置 1 次废飞=/v1 think:false 未生效烧 4096 思维链截断） | GPU 突发 ~1 min |
| CosyVoice3 运行时装包（clone+5 依赖+import 冒烟） | R1783 | 1 轮（盘面/依赖面·零 GPU 冲突） | 一次性 capex |
| GPU 加载+推理试跑 | R1784+R1785 | 加载 13.6s（LOAD-OK）+推理 17.8s 出 9.88s wav（rtf 1.80） | 一次性 capex |
| 多角色配音 | R1786 | narrator 8 镜 30.75s emotive_tts PASS；配角 5 镜两轮判负（长参考乱码/短参考 0.08s 空产出） | 判负分支 |
| T2I PACK 正典件（12 镜 prompt/seed/KB 参数包） | R1788 | 1 轮 CPU 手产 | 每件复现 |
| SDXL 草稿档 roll | R1789 | ComfyUI --lowvram 起服 32s + 12/12 毕 **2.5 分钟（~9s/镜）** | 后判负支线 |
| SDXL 一致门迭代 | R1790 | 4/9→6/9 三轮迭代 **17 张生成证据**=细粒度特征天花板判负 | 判负分支 |
| Qwen-2.1 三件套拉取 | R1791 | 14.24GB avg ~30MB/s ≈ **8 分钟** | 一次性 capex（已落位） |
| Qwen-2.1 正档全量重 roll | R1792 | 12/12 OK **~50-60s/镜 ≈ 10-12 分钟**（VRAM 守卫 ≥9GB 过闸） | **每件主 GPU 段** |
| 定向 best-of-N 补 roll | R1793 | server 11s 起 + 6/6 OK **~45-50s/张 ≈ 5 分钟** → 9/9 GATE PASS | 每件 GPU 段 |
| 装配+S2 三门+帧验三律 | R1794 | 前体 06:22-06:57 **≈35 分钟**（成片 75.84s/13 段·含台账步亡失） | 每件 CPU 段 |
| E8 终审+M4+F-168 登记 | R1795 | 七席 ≥9 同轮毕；E4 同轮回填 8.0（07:17:10 落判·**静 GPU 窗快落**） | 每件 GPU/LLM 段 |
| **Wall-clock 全链** | R1782→R1795 | **≈6.2h / 14 轮**（01:0x→07:17·含 PoC 探路+双判负分支+两模型拉取） | — |

**E8/E4 争抢读数（R1847 实锚）**：E4 v13 两飞 TIMEOUT-1500s ×2 = 50 分钟烧穿零判词（GPU LoRA 训练窗满载型·R1687 争抢退化家族）→ LLM 评审席是全链唯一 contention 敏感段，静窗与撞窗的耗时差 = 分钟级 vs 25 分钟帽连烧。

## §2 判负分支剪除清单（MD-0002+ 每件省下项）

1. **SDXL 草稿档跳过**（R1790 天花板判负在案）→ 直上 Qwen-2.1 正档：省 ~2 轮 + 2.5 min roll + 17 张废 roll。
2. **CosyVoice3 短台词退役**（tech#2 R1828 定谳）→ 配角=edge-tts 档位声直出（cast.json 同源）：省 ~2 轮试错。
3. **模型拉取零复现**（Qwen-2.1 三件套+ComfyUI 0.37.0+runner/asm 脚本全部在位）：省 capex 腿。
4. **prompt lessons 库复用**（R1790-93 实录：style_lock 结构修正〔室内暖场 vs 全局夜雨冲突〕/negative 锁强化〔antenna on head〕/角色 seed 锚 41041/27027/19019）→ gate 预计 1-2 轮过（MD-0001 探路 3 轮的教训变现）。

## §3 MD-0002+ 批量 SOP（七腿·剪枝后 5-7 轮/件）

| # | 腿 | 载具/工艺 | 预估机时 | 轮数 |
|---|---|---|---|---|
| 1 | 题材选型+溯源预登（M0） | 编年史/codex A 级事件+人物锚+四先在形态避让表（R1843 范式） | CPU·随轮 | 1 |
| 2 | 剧本腿 | 9b-16k **原生 /api/generate think=false**（R1782 工艺）+schema 机检 ≤5%+verbatim 锚抽验 | GPU ~1-2 min | 1 |
| 3 | PACK+TTS | PACK-v1 同构 12 镜包 + narrator emotive_tts + 配角 edge-tts 档位声 | CPU+秒级 | 1 |
| 4 | T2I 正档 | runner_r1792 同构（VRAM 守卫 ≥9GB·Start-Process 脱壳双 redirect·用后杀 server） | **GPU 10-12 min** | 1 |
| 5 | 一致门+定向补 roll | 参照卡并排 gate ≥8/9·fail 镜 best-of-N ≤9 候选 | GPU 3-6 min | 1 |
| 6 | 装配+S2+帧验 | asm_r1794 同构 + drama-ep 窗律（tech#15 首件锁参复检位）+S2 三门+帧验三律 | CPU 15-20 min | 1（交付件先行 commit） |
| 7 | E8+M4+F 登记 | 七席盲评 ≥9 + E4 参考仪**同窗飞**（静 GPU 窗） | GPU 10-30 min | 1 |

## §4 节拍读数与批量窗数学（判据=单件机时读数）

- **单件 GPU-active 中位 ≈35 min**（剧本 1 + T2I 10-12 + 补 roll 3-6 + E8/E4 10-30·P25-P75 带 25-50 min）。
- **单件满链轮数（剪枝后）5-7 轮** vs MD-0001 实际 14 轮（探路+判负分支+拉取全计入首件）。
- **12:00 后独占窗（2-3h）≈ 2 件满链**（T2I 串行 + E8 窗尾批飞）；若 T2I 前置腿批产 + E8 集中批飞 → **3 件/窗**。
- **日 ceiling（单 12GB 卡·单 ComfyUI·含 CEO 用机让路窗）≈ 3-4 件/日**——M5 发布批/合集装配（explore#2）容量参考数。
- T2I 段天然可跨窗切分（每件 frames 独立落盘）→ 窗中断恢复友好；E8/E4 不可切分 → 永排窗尾或静夜窗。

## §5 调度铁律（实锚承继）

1. **LLM 评审席排静窗**（R1847 双 TIMEOUT 实锚）：E8/E4 在 GPU 满载窗（MV sprint/LoRA 训练）内禁飞——25 min 帽连烧零判词。
2. **GPU 让路守卫**：nvidia-smi 前置（free ≥9GB 才起 ComfyUI·R1792 闸）；CEO 用机/MV sprint 窗零自排 GPU 活（O-20261006-2110 承继）。
3. **runner 正法**：Start-Process 脱壳+双 redirect（R1792 前台 5min 零输出帽杀实录）。
4. **12:00 独占窗叠加序建议**（tech#18 三件同窗输入）：窗头 MD-0002 剧本腿（~2 min 搭车）→ tech#18 GPU 三件（27b A/B / Krea 2 A/B / 27b S1）→ 窗外 CPU 腿（PACK+TTS）→ 次窗 T2I 正档+E8。

## §6 结论应用表

| 输出 | 消费位 |
|---|---|
| §3 七腿 SOP + §5 窗叠加序 | main#4 MD-0002 剧本腿（12:00 窗）执行序输入 |
| §4 单件机时读数 + 日 ceiling | tech#18 GPU 排程表参数；M5 合集/发布批容量预估（explore#2） |
| §2 剪枝清单 | MD-0002+ 每件起链时自查（禁复活判负分支） |
| 首件校准回填位 | 新 tech 队项：MD-0002 装配毕后实耗对账（SOP 预估 vs 实测·逐腿 delta 入档） |

## 验证声明

本件全部机时读数逐条锚 backlog #108 R1782-R1795 注记行与 state log R1847；批量窗数学=读数派生算术（零外推断言）；判据「单件机时读数」已满足（§1 实测表+§4 汇总读数）。剪枝项均有在案定谳（R1790 SDXL 判负/tech#2 CosyVoice 退役/R1791 模型落位），零新立法。
