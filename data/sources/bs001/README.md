# BS-001 素材包台账（视频号 60s 字卡版）

> PoC 全链（R-A/R-B/R-C）实证件。渲染器=`src/render/render_card_video.py`；对轴工具=`src/render/srt_fix.py` + `src/render/whisper_to_srt.py`；试配音色对位=`docs/persona-jason.md`。

## §1 文件清单

| 件 | 说明 |
|---|---|
| `voiceover.txt` | 口播母稿（渲染器 `--strict` 校验基准） |
| `cards.json` | 5 卡时间线 + AIGC 标识（红线内建·拒渲染空声明） |
| `subs.srt` | **正路字幕**＝edge-tts 直出 + srt_fix 钳重叠（R-C·替换 R-A 占位件） |
| `subs-edgetts-raw.srt` | edge-tts 直出原始件（cue1/2 有 50ms 重叠＝钳制前证据） |
| `subs-whisper.srt` | A 路对轴件（对比证据·未入流水） |
| `audio-yunyang.mp3` | Yunyang 试配音（`--rate=-10% --pitch=-2Hz`·**音色未定档**＝backlog #8 人耳项） |

## §2 双路对轴对比（R-C 裁决·2026-09-23 R12）

| 维度 | B 路＝edge-tts 直出+srt_fix 钳制 | A 路＝faster-whisper small int8 CPU |
|---|---|---|
| 文本 | 逐字精确（renderer `--strict` 实过） | ASR 固有错在案：它们→他们·软著→软着·诚实门禁→城市门禁·标点半角化 |
| 时间轴 | 词级（合成侧） | 词级（共享边界 31.94s 两路几乎重合＝交叉验证） |
| cue 粒度 | 不均：cue8 单条 14.39s | 均匀：18 cues·均 3.3s |
| 裁决 | **合成配音稿正路**（零 ASR 风险） | **真人原声（Jason）通用件**（ASR 稿须人工校对回母稿） |

复现：`edge-tts --voice zh-CN-YunyangNeural --rate=-10% --pitch=-2Hz --file voiceover.txt --write-media audio-yunyang.mp3 --write-subtitles subs-edgetts-raw.srt` → `python src/render/srt_fix.py --in subs-edgetts-raw.srt --out subs.srt` → `python src/render/whisper_to_srt.py --audio audio-yunyang.mp3 --out subs-whisper.srt`

## §3 渲染实况

- v2（R-C）：`python src/render/render_card_video.py --cards cards.json --strict --audio audio-yunyang.mp3 --out output/renders/bs-001-card-v2.mp4` → 1080×1920·59.93s·1506KB·aac 24kHz mono（ffprobe 实证）
- t=33 抽帧像素实测（亮度带投影）：4 行字幕块 1620-1877 全在帧内·AIGC 标识带 48-76·字卡带 791-1128——**连带修红**：drawtext CRLF 行距翻倍缺陷（textfile 含 `\r\n` 时 `\r` 被当独立换行·行距 70→142px 实测·≥3 行字幕裁帧底）→ 渲染器 textfile 改 LF 写出 + `tests/test_align_tools.py` 回归锁死
- 逐行居中/ASS 评估：多行字幕仅现于长 cue（cue8）；**先治粒度再谈 ASS**——长 cue 再切后单行 cue 天然居中，ASS 迁移触发条件=治粒度后仍存多行 cue

## §4 遗留（→ backlog #4 产线批）

1. cue8 单条 14.39s＝长 cue 再切（可借 A 路词级时间轴做混合切分：B 路精确文本 × A 路细粒度）
2. 字卡时间轴漂移：卡止 58.0s vs 音频 59.93s（尾段 2s 无字卡）
3. 音色定档待人耳（backlog #8·CEO/Qiqi）——当前音轨为候选 A 试配音，定档后须重合成重对轴
