# TTS 试录样件台账（M2 本地链 PoC · R-B）

> 交付：backlog #9 R-B（`docs/m2-local-stack.md` §4）·音色对位=`docs/persona-jason.md`（Jason 本人出镜·AI 仅补配音位·AIGC 显著标识）。
> 证据纪律：`docs/research-protocol.md` v1.0——实况即证据（命令、时长、文件）；试听质量=人耳项（T4·Qiqi/CEO 终审面），本台账不替耳朵下结论。
> 试录日：2026-09-23（OS 循环 R11 轮）。

## §0 标准试录句（`trial-line.txt`）

> 三家 AI 公司，今天下午同时开工了。它们的员工名单里，只有一个人类。每条命令落台账，永不删除。

取自 `data/sources/bs001/voiceover.txt` 开头钩子句+台账句——真实产能文本，非合成测试句；全引擎同句对比。

## §1 样件清单（全部可复现·命令见 §2/§3）

| 件 | 引擎 | 音色/语音 | 参数 | 实测时长 | 大小 |
|---|---|---|---|---|---|
| `yunyang-default.mp3` | edge-tts | **zh-CN-YunyangNeural**（News·Professional） | 默认 | 9.62s | 57,744 B |
| `yunjian-default.mp3` | edge-tts | zh-CN-YunjianNeural（Sports/Novel·Passion） | 默认 | ~9.7s | 63,216 B |
| `yunxi-default.mp3` | edge-tts | zh-CN-YunxiNeural（Novel·Lively） | 默认 | ~9.6s | 62,784 B |
| `yunyang-rate10-pitch2.mp3` | edge-tts | zh-CN-YunyangNeural | `--rate=-10% --pitch=-2Hz`（沉稳档） | ~10s | 64,080 B |
| `yunyang-subs.mp3` + `yunyang-subs.srt` | edge-tts | zh-CN-YunyangNeural | `--write-subtitles` 直出 SRT（R-C 双路证据之一） | 9.62s | 57,744 B + 250 B |
| `huayan-medium-default.mp3` | **piper1-gpl**（纯本地 CPU） | zh_CN-huayan **medium** | 默认（length_scale=1.0） | 8.17s | 60,882 B |

- 时长口径=ffprobe 实测；标 ~ 号=未逐件 probe（同句同引擎，量级一致）。
- **T2 数据点**：edge-tts 本轮 5 次合成 5/5 首试成功、零失败（单轮样本·不足为可靠性结论，续录）。

## §2 edge-tts 参数表（官方 CLI 实测面·v7.2.8）

- 音色：`--voice zh-CN-XXXNeural`；清单：`edge-tts --list-voices`（本机 zh-CN 实况全表=`edge-voices-zhCN.txt`：男声 4=Yunjian/Yunxi/Yunxia/Yunyang·女声 2·方言 2；**Azure 全量音色不在 edge 通道内**——如 Yunze/Yunye 未出现，以本机实测清单为准）。
- 语速/音量/音调：`--rate=±X%` `--volume=±X%` `--pitch=±XHz`——**负值必须连写式**（`--rate=-10%`，空格式会被吞，research §1.1 A1 在案）。
- 文件进出：`--file 输入.txt --write-media 输出.mp3`；字幕直出：`--write-subtitles 输出.srt`（词级时间戳·实测 3 句 3 轴可用；cue1/cue2 有 50ms 重叠——R-C 对轴时处理）。
- 性质：微软**云端**免费接口（GPL-3.0·A1）——零支出但算力在微软侧，收紧风险在案（SSML 已削）→ 备份线必做（本台账 §3 即备份验证）。

复现命令（本目录内）：
```
edge-tts --voice zh-CN-YunyangNeural --file trial-line.txt --write-media yunyang-default.mp3
edge-tts --voice zh-CN-YunyangNeural --rate=-10% --pitch=-2Hz --file trial-line.txt --write-media yunyang-rate10-pitch2.mp3
edge-tts --voice zh-CN-YunyangNeural --file trial-line.txt --write-media yunyang-subs.mp3 --write-subtitles yunyang-subs.srt
```

## §3 piper1-gpl 备份线实测（T3 解锁·纯本地）

- 安装：`pip install piper-tts`（=OHF-Voice/piper1-gpl 后继仓·GPL-3.0·A3）——本机 Python 3.14 装成，CLI=`piper -m <onnx> -i <txt> -f <wav>`。
- **T3 结论（实测）**：pip 包**无 `--list-voices`**——语音=外置 ONNX 件，官方库仍=HuggingFace `rhasspy/piper-voices`（v1.0.0·A4）；后继仓沿用该库（huayan medium 拉取即用）。
- 模型落位：`data/assets/piper-models/zh_CN-huayan-medium.onnx`（63.2MB·**gitignored 路径不进库**，本台账即位置记录）+ 同名 `.onnx.json` 配置。
- 实测：同句合成 **2.77s（纯 CPU·9950X）**→ 8.17s 音频；wav 转 mp3 入库（`ffmpeg -i in.wav -codec:a libmp3lame -qscale:a 4 out.mp3`）。
- 参数面（CLI 实测）：`--length-scale`（语速倒数）、`--noise-scale`、`--noise-w-scale`、`--sentence-silence`、`--volume`、`--cuda`（本机显存 1.5GB 空闲未动 GPU——分时纪律）。
- 风险在案：官方横幅「LOOKING FOR MAINTAINERS」（A3）——备份线长期可用性风险照记。

## §4 候选对比与人设对位【推论·待人耳终审】

| 候选 | 声线标签（官方） | 对位人设卡（克制白描·CEO） | 位次建议 |
|---|---|---|---|
| zh-CN-YunyangNeural | News·Professional/Reliable | 权威感/新闻播报≈「给数字给台账」口吻·AI 补配音位首选 | **A** |
| zh-CN-YunxiNeural | Novel·Lively/Sunshine | 更年轻·亲和——若 Yunyang 过「播音腔」则备选 | B |
| zh-CN-YunjianNeural | Sports/Novel·Passion | 激情感与「不吹不煽」红线相斥·存疑 | C |
| zh_CN-huayan-medium（piper） | 无官方标签（人耳定） | 纯本地可用=备份价值本身成立；质量是否达标=T4 人耳项 | 备份 |

【推论】人设卡嗓音口径=「本人原声优先·AI 配音仅补位」——样件用途=补配音位选型+备份线验证，非替 Jason 出镜声。

## §5 卡点台账更新（research/local-stack-research-v1.md §6 对应）

| # | 项 | 本轮实况 |
|---|---|---|
| T2 | edge-tts 可靠性 | 单轮 5/5 成功——数据点起录，待多轮累计 |
| T3 | piper1-gpl 语音库 | **解锁**：无 list CLI·外置 ONNX·沿用 HF rhasspy/piper-voices v1.0.0（§3） |
| T4 | huayan 试听质量 | **样件已呈**（`huayan-medium-default.mp3`）——待人耳 |
| T5 | GPL 分发边界 | 不变（内部生产使用无碍） |

## §6 终审与下一步

- **待人耳（CEO/Qiqi·backlog #8）**：A/B/C 位次建议+备份线音质——听 `data/sources/tts-samples/` 即可，无环境要求。
- R-C done 2026-09-23（R12）：双路对轴裁决与证据=`data/sources/bs001/README.md`——B 路（直出+`srt_fix.py` 钳 50ms 重叠）=合成稿正路；A 路（`whisper_to_srt.py`·faster-whisper small int8 CPU）=真人原声通用件（ASR 错字实录在案）。
