# BigStream M2 本地算力链路（Local Stack）

> CEO 令 O-20260923-1609-bm-a：「大部分我希望利用本地电脑算力！」
> 法：本地算力优先；云/付费 API=兜底，动用须报批（P1 级·预算律 PLAN §7-4）。实况优先——选型以下表「本机实况」为准，装了什么用什么。

## §0 本机算力实况（2026-09-23 16:09 实测）

| 件 | 实况 | 状态 |
|---|---|---|
| GPU | RTX 4070 SUPER **12GB**（Ollama 常驻占 8.6GB·空闲约 3.4GB） | 就绪 |
| GPU 复测 17:4x | 总 12282 MiB·已用 10503·**空闲 1495 MiB**——当日波动 3.4→1.5GB 实证：分时以执行前实测为准 | M1·local-stack-research §0 |
| CPU | Ryzen 9 9950X（16 核 32 线程） | 就绪 |
| LLM | Ollama 常驻：qwen2.5:14b（9.0GB）·qwen2.5:7b（4.7GB）·bge-m3（1.2GB） | 就绪 |
| TTS | edge-tts 7.2.8 | 已装 |
| STT 字幕 | faster-whisper 1.2.1（在役·R169 QC recipe）＋ whisper.cpp 备选轨（parked·R644/OH-20260929-bigstream） | 已装 |
| 剪辑/合成 | FFmpeg（Tuanjie Hub）+ opencv-python + pillow | 已装 |
| 框架 | torch 2.11.0+cu128 | 就绪 |
| 文生图 | **ComfyUI 已装**（09-28·C:\Agent\ComfyUI·py3.12.14+torch 2.14.0+cu126·O-20260928-1748） | 就绪·产线启用仍后置 |

## §1 四站本地选型（v1.2·证据=research/local-stack-research-v1.md）

| 站 | 本地方案 | 算力位 | 备注 |
|---|---|---|---|
| 配音 TTS | edge-tts（音色参数随 `docs/persona-jason.md` 人设卡定——O-1602 令人设=Jason 本人出镜；三案口吻=栏目变体保留） | 云端免费接口·零预算 | v1.2 证据（research §1·R18 补采）：edge-tts=微软**云端**免费接口（许可证现值 **LGPLv3**·R18 更正）·微软已移除自定义 SSML（仅剩单 voice+单 prosody）=收紧先例+**403 波次史四波在案**（2024-10×2/2024-12/2025-08/2026-01·#286 仅大陆复现·修复均以发版收口·仓库 2026-03-22 后无新提交）→**备份必做且升产线刚性依赖**（403 再发=升最新 release+波次期临时切 piper）：纯本地替代=piper1-gpl（旧 rhasspy/piper 仓 2025-10-06 官方归档·后继仓 `pip install piper-tts`·GPL-3.0·官方正寻维护者）；zh_CN huayan（x_low/medium）语音在案 |
| 文案推理 | 本地 Ollama（qwen2.5:14b 起草·7b 快迭代·bge-m3 选题向量化） | 本地 GPU | 交互会话+循环双轨 |
| 字幕对轴 | faster-whisper（口播→时间戳→SRT） | 本地 GPU/CPU 双路 | v1.1 证据（research §2 官方基准）：large-v2 int8 GPU=2926MB 显存·small int8 CPU=1477MB RAM——**显存窗口<3GB 走 CPU int8**；无需系统 FFmpeg（PyAV 捆绑）；AIGC 显著标识字幕同时合成 |
| 剪辑合成 | FFmpeg 时间线脚本（字卡/黑底白字/实录画面拼接）+ opencv 封面合成 | 本地 CPU | `src/render/` 脚本位 |
| 画面（M2 首发路线） | **屏幕实录（集团真实界面·脱敏）+ 极简字卡模板**——非文生图依赖 | 本地 | 黑白极简=集团视觉基调，字卡即品牌 |
| 画面（后置升级） | 本地 ComfyUI（官方 README 无固定最低显存声明——v1.0「可载 SDXL 级」无源断言撤回；官方特性="smart VRAM and RAM management, model offloading, quantized models"·原生含 SDXL/Qwen Image/Wan 视频·Windows N 卡便携包·GPL-3.0·`--disable-api-nodes` 保纯离线） | 本地 GPU | **装机毕（09-28·O-20260928-1748·双验证=cuda True+quick-test 绿）**——产线启用仍后置：等首发数据+显存窗口（执行前实测·禁预支历史数字）·模型首次加载前补采官方 GPU wiki（T1 卡点） |

## §2 显存分时策略（多公司共机纪律）

- 本机 Ollama 常驻（BigMoney/集团共享）——渲染任务执行前查 `nvidia-smi` 空闲位（当日实测波动 3.4→1.5GB·历史数字不可预支）：
  - 空闲 ≥6GB → 可评估 SDXL 级（后置；官方未声明最低显存，首次加载模型前补采 GPU wiki=T1）；
  - 空闲 ≥3GB → faster-whisper large int8 GPU 档（官方基准 2926MB）；
  - 空闲不足 → **CPU int8 路线照常**（small 档 1477MB RAM·TTS 云端不占显存）；重 GPU 任务暂停排队（keepwarm.pause 同源礼仪），**禁强杀他人常驻进程**（集团共享机纪律 governance §6）。
- 媒体线任务=非紧急批处理，让位优先级最高的是量化公司盘中任务。

## §3 兜底报批规则（P1 级）

本地不满足才走云/付费（如高质量配音克隆、商业图库），**逐单报批**：需求+三家比价+预期收益 → CEO 署名。零预算原则不动。

## §4 PoC 阶梯（backlog 驱动·循环可执行）

1. **R-A** 口播→成品最小闭环 PoC：`src/render/` 落一个 FFmpeg 时间线脚本——输入=口播 txt + SRT + 字卡模板 → 输出=9:16 mp4（黑底白字卡版 BS-001 60s 口播）——**纯本地·零安装**。
2. **R-B done 2026-09-23**（台账=`data/sources/tts-samples/README.md`）——edge-tts 参数表+6 样件（男声 3 候选位次建议 Yunyang A/Yunxi B/Yunjian C·Yunyang 沉稳档 `--rate=-10% --pitch=-2Hz`·`--write-subtitles` 直出 SRT 实测）；**piper1-gpl 真装真录**（`pip install piper-tts`·zh_CN huayan medium 63MB 模型落 `data/assets/piper-models/`（gitignored）·纯 CPU 2.77s 合成 8.17s 音频·T3 解锁）；试听终审=Qiqi/CEO 人耳项（T4·backlog #8）。
3. **R-C done 2026-09-23**（OS 循环 R12·台账=`data/sources/bs001/README.md`）——双路对轴+裁决：B 路=edge-tts `--write-subtitles` 直出+`src/render/srt_fix.py` 钳 50ms 重叠＝**合成稿正路**（文本逐字精确·strict 实过）；A 路=`src/render/whisper_to_srt.py`（faster-whisper small int8 CPU·词级时间戳·断点优先句读）＝**真人原声通用件**（ASR 固有错在案：它们→他们/软著→软着/诚实门禁→城市门禁）。BS-001 换真轴+试配音轨 v2 重渲（59.93s·aac）。**连带修红**：drawtext CRLF 行距翻倍（write_text 默认 `\r\n`→`\r` 被当独立换行·行距 70→142px 像素实测·≥3 行字幕裁帧底）→LF 修复+回归测试锁。遗留=cue8 长 cue 再切+卡轴漂移（→#4 产线批）。
4. **R-D** （后置·09-28 改制）装机评估已被 O-20260928-1748 提前闭口（ComfyUI 装毕双验证）——余项=**生产启用评估**（模型选型/显存排程/工作流定型）：仅在首发数据证明需要 AIGC 画面或漫画/图文卡线批量需求触发时提请。

## §5 红线（不变）

素材来源可溯（`data/sources/`）；画面/字幕脱敏审（M4）；AIGC 依法显著标识（字幕声明+平台开关双落）；量化内容附非投资建议。

## 变更记录

- 2026-09-23: v1.0 立册（CEO 令 O-20260923-1609-bm-a）——四站本地选型+显存分时+PoC 阶梯；四站三件已装实测。
- 2026-09-23: R-A 落地——`src/render/render_card_video.py`（口播 txt+SRT+字卡 JSON→9:16 mp4·AIGC 标识常驻烧录·CJK 折行防裁·纯本地零安装）；BS-001 黑底白字卡版实渲染过（1080×1920·58.8s·三段抽帧目检）。本机 ffmpeg 9.0.1（gyan full）实况两条：①已删 `-filter_complex_script` 选项→用 `-filter_complex` 内联；②drawtext 无 fontconfig 会崩→fontfile 必须显式（脚本已内置校验）。
- 2026-09-23: v1.1 按证据升级（CEO 令 O-20260923-1719-bm-a·证据=research/local-stack-research-v1.md）——TTS 备份线更名 piper1-gpl（旧 Piper 仓归档）；撤回「可载 SDXL 级」无源断言（官方无最低显存声明·T1 卡点）；faster-whisper 基准入表（GPU int8 2926MB / CPU int8 1477MB）；分时纪律按当日实测修订；R-B/R-C 对齐人设卡（Jason 出镜）。
- 2026-09-23: R-B 落地（OS 循环 R11）——TTS 双轨试录：edge-tts 参数表+6 样件、piper1-gpl 真装真录（huayan medium·纯 CPU 2.77s·模型 gitignored 于 data/assets/piper-models/）；T3 解锁（后继仓沿用 HF rhasspy/piper-voices）；位次建议 Yunyang A——选型定档待人耳终审（backlog #8）。
- 2026-09-23: R-C 落地（OS 循环 R12）——双路字幕对轴裁决+BS-001 v2 音轨重渲；连带修红 drawtext CRLF 行距翻倍（LF 写出+回归锁）；PoC 阶梯 R-A/R-B/R-C 全 done，R-D 维持后置。
- 2026-09-23: v1.2（OS 循环 R18·随 research v1.2 同步）——TTS 行证据更新：edge-tts 许可证更正 LGPLv3（LICENSE 直采）；403 四波风控史入案（#286 仅大陆复现）→备份线升**产线刚性依赖**；403 再发处置口径=升最新 release+波次期临时切 piper。
- 2026-09-28: v1.3 ComfyUI 装毕收口（CEO 令 O-20260928-1748 GitHub 全面安装令）——§0 文生图行翻正（未装→已装）+§1 画面后置升级行改注（产线启用仍后置）+§2 T1 触点改「首次加载模型前」+§4 R-D 改制（安装评估已闭·余项=生产启用评估）；随行撞号更正=他件「C-16 图像生成线」系误指（capabilities 册内 C-16=全链量产生产轮·文生图正位=C-11/本册 §1 画面后置升级）。
- 2026-09-24: A 路仪器校准（OS 循环 R169·自进清单 C2）——`whisper_to_srt.py` 参数面四配置对照+medium 探针（基准=v12 母版音轨 cyber light 57s·ref=v11-trim beats·字符级 Levenshtein CER）：small int8 基线 13.07%·beam5 零增益·`--no-context` +1 字+提速 30%·域 initial_prompt **反劣化**（一名→印明新错）·**medium int8+beam5+noctx=5.53%——模型档位=主因子**（同音位点 12→8·累/方案/废×2/活/账全修复·事实词零损维持·瓶→品新增 1）；工具落 `--beam-size/--no-context/--initial-prompt` 旋钮（默认值不动=无实测增益不改行为）·**S2 asr-check QC recipe=`--model medium --beam-size 5 --no-context`**（首载 ~1min·57s 片 ~21s）·small 默认=快道；测试 +4（207 全回归绿）。
- 2026-09-29: v1.4 STT 备选轨登记+HF_HUB_OFFLINE 坑律正典化（OS 循环 R644·#87=P-2026-09-28-08 whisper.cpp 接线单·集团 CPH4 dogfood 五门过转办承接）——**whisper.cpp（ggml-org·MIT·53,990★·push 2026-09-24·GitHub API 实采）登记=S2 ASR 备选轨 parked**（在役 faster-whisper R169 QC recipe 无短板触发不轻换·五门+判据预注册+结论应用表全档=`cph4/oss-harvest/OH-20260929-bigstream.md` 切片 1）；增量面=ggml 本地模型零 HF hub 依赖（R638 挂起坑天然根除）+单二进制零 Python 栈；**重开条件**=HF hub 型环境阻塞再发且 HF_HUB_OFFLINE=1 缓解失效→A/B 实测腿（标准片=BS-002 v2 终轨 58.02s·判据=CER ≤5.53% 且耗时 ≤21s）过线即 adopt；**HF_HUB_OFFLINE=1=产线默认环境位**（R638 根因=faster-whisper 载模前置 HF hub 在线 etag 检查网络挂起型·360MB WS 停 20min 实证·`whisper_to_srt.py` docstring 同步落地）·模型类登记不拉取（P-17 矩阵·试验走 Bonsai 波范式禁自行占显存）。
