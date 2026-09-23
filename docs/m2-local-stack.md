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
| STT 字幕 | faster-whisper 1.2.1 | 已装 |
| 剪辑/合成 | FFmpeg（Tuanjie Hub）+ opencv-python + pillow | 已装 |
| 框架 | torch 2.11.0+cu128 | 就绪 |
| 文生图 | ComfyUI 未装 | **缺口·后置** |

## §1 四站本地选型（v1.1·证据=research/local-stack-research-v1.md）

| 站 | 本地方案 | 算力位 | 备注 |
|---|---|---|---|
| 配音 TTS | edge-tts（音色参数随 `docs/persona-jason.md` 人设卡定——O-1602 令人设=Jason 本人出镜；三案口吻=栏目变体保留） | 云端免费接口·零预算 | v1.1 证据（research §1）：edge-tts=微软**云端**免费接口（GPL-3.0）·微软已移除自定义 SSML（仅剩单 voice+单 prosody）=收紧先例→**备份必做**：纯本地替代=piper1-gpl（旧 rhasspy/piper 仓 2025-10-06 官方归档·后继仓 `pip install piper-tts`·GPL-3.0·官方正寻维护者）；zh_CN huayan（x_low/medium）语音在案 |
| 文案推理 | 本地 Ollama（qwen2.5:14b 起草·7b 快迭代·bge-m3 选题向量化） | 本地 GPU | 交互会话+循环双轨 |
| 字幕对轴 | faster-whisper（口播→时间戳→SRT） | 本地 GPU/CPU 双路 | v1.1 证据（research §2 官方基准）：large-v2 int8 GPU=2926MB 显存·small int8 CPU=1477MB RAM——**显存窗口<3GB 走 CPU int8**；无需系统 FFmpeg（PyAV 捆绑）；AIGC 显著标识字幕同时合成 |
| 剪辑合成 | FFmpeg 时间线脚本（字卡/黑底白字/实录画面拼接）+ opencv 封面合成 | 本地 CPU | `src/render/` 脚本位 |
| 画面（M2 首发路线） | **屏幕实录（集团真实界面·脱敏）+ 极简字卡模板**——非文生图依赖 | 本地 | 黑白极简=集团视觉基调，字卡即品牌 |
| 画面（后置升级） | 本地 ComfyUI（官方 README 无固定最低显存声明——v1.0「可载 SDXL 级」无源断言撤回；官方特性="smart VRAM and RAM management, model offloading, quantized models"·原生含 SDXL/Qwen Image/Wan 视频·Windows N 卡便携包·GPL-3.0·`--disable-api-nodes` 保纯离线） | 本地 GPU | 缺口后置不变：等首发数据+显存窗口（当前空闲 1.5GB）·装机前补采官方 GPU wiki（T1 卡点） |

## §2 显存分时策略（多公司共机纪律）

- 本机 Ollama 常驻（BigMoney/集团共享）——渲染任务执行前查 `nvidia-smi` 空闲位（当日实测波动 3.4→1.5GB·历史数字不可预支）：
  - 空闲 ≥6GB → 可评估 SDXL 级（后置；官方未声明最低显存，装机前补采 GPU wiki=T1）；
  - 空闲 ≥3GB → faster-whisper large int8 GPU 档（官方基准 2926MB）；
  - 空闲不足 → **CPU int8 路线照常**（small 档 1477MB RAM·TTS 云端不占显存）；重 GPU 任务暂停排队（keepwarm.pause 同源礼仪），**禁强杀他人常驻进程**（集团共享机纪律 governance §6）。
- 媒体线任务=非紧急批处理，让位优先级最高的是量化公司盘中任务。

## §3 兜底报批规则（P1 级）

本地不满足才走云/付费（如高质量配音克隆、商业图库），**逐单报批**：需求+三家比价+预期收益 → CEO 署名。零预算原则不动。

## §4 PoC 阶梯（backlog 驱动·循环可执行）

1. **R-A** 口播→成品最小闭环 PoC：`src/render/` 落一个 FFmpeg 时间线脚本——输入=口播 txt + SRT + 字卡模板 → 输出=9:16 mp4（黑底白字卡版 BS-001 60s 口播）——**纯本地·零安装**。
2. **R-B** edge-tts 音色参数表（音色随 `docs/persona-jason.md` 定——Jason 出镜·负值参数连写式 `--rate=-50%`）+ 试录样件落 `data/sources/tts-samples/`；**本地替代备份=piper1-gpl**（`pip install piper-tts`·zh_CN huayan medium 候选·旧 Piper 仓已官方归档）真装真听对比；试听终审=Qiqi/CEO 人耳项（T4）。
3. **R-C** faster-whisper 字幕对轴脚本（口播 wav → SRT → 硬字幕合成入 R-A 流水）——双路对比：edge-tts `--write-subtitles` 直出 SRT（TTS 侧词级时间戳）vs STT 反推，PoC 择优。
4. **R-D** （后置）ComfyUI 安装评估报告——仅在首发数据证明需要 AIGC 画面时提请。

## §5 红线（不变）

素材来源可溯（`data/sources/`）；画面/字幕脱敏审（M4）；AIGC 依法显著标识（字幕声明+平台开关双落）；量化内容附非投资建议。

## 变更记录

- 2026-09-23: v1.0 立册（CEO 令 O-20260923-1609-bm-a）——四站本地选型+显存分时+PoC 阶梯；四站三件已装实测。
- 2026-09-23: R-A 落地——`src/render/render_card_video.py`（口播 txt+SRT+字卡 JSON→9:16 mp4·AIGC 标识常驻烧录·CJK 折行防裁·纯本地零安装）；BS-001 黑底白字卡版实渲染过（1080×1920·58.8s·三段抽帧目检）。本机 ffmpeg 9.0.1（gyan full）实况两条：①已删 `-filter_complex_script` 选项→用 `-filter_complex` 内联；②drawtext 无 fontconfig 会崩→fontfile 必须显式（脚本已内置校验）。
- 2026-09-23: v1.1 按证据升级（CEO 令 O-20260923-1719-bm-a·证据=research/local-stack-research-v1.md）——TTS 备份线更名 piper1-gpl（旧 Piper 仓归档）；撤回「可载 SDXL 级」无源断言（官方无最低显存声明·T1 卡点）；faster-whisper 基准入表（GPU int8 2926MB / CPU int8 1477MB）；分时纪律按当日实测修订；R-B/R-C 对齐人设卡（Jason 出镜）。
