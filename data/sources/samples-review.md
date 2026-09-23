# 样本试看包（samples-review）

> CEO 令 O-20260923-1830-bm-a「你先跑几个样本我来看看」·测试生产合法态（O-1756）。
> 全部=**测试件·非成品**，不入发布队列。同稿同字卡时间线（`data/sources/bs001/`），唯一变量=音色。
> 试看日：2026-09-23 18:30-18:40（bm-a 交互会话·A 件为 R12 既有 v2）。

## 一、成片组（双击即看·约 1 分钟/件）

| 件 | 音色 | 文件 | 听点 |
|---|---|---|---|
| **A** | **Yunyang 沉稳档**（`--rate=-10% --pitch=-2Hz`） | `output/renders/bs-001-card-v2.mp4` | 新闻播报权威感=「给数字给台账」口吻·官方位次建议 **A** |
| **B** | Yunxi（默认） | `output/renders/bs-001-voice-B-yunxi.mp4` | 更年轻亲和——若嫌 A 播音腔，看这件 |
| **C** | Yunjian（默认） | `output/renders/bs-001-voice-C-yunjian.mp4` | 激情感——对照「不吹不煽」红线自见分晓 |
| **D** | **piper huayan·全链纯本地** | `output/renders/bs-001-voice-D-huayan-local.mp4` | 备份线音质 + 纯本地产线实证（配音=CPU 合成·字幕=ASR 对轴） |

## 二、短句快听组（约 9.6s/件·快速筛）

`data/sources/tts-samples/` 目录：`yunyang-default.mp3` / `yunxi-default.mp3` / `yunjian-default.mp3` / `yunyang-rate10-pitch2.mp3`（=A 沉稳档短句）/ `huayan-medium-default.mp3`（piper）。

## 三、对照要点

1. 时长差异：A 59.93s / B 55.97s / C 57.53s / D 48.83s（huayan 语速快，可调 `--length-scale`）。
2. D 件字幕文本与母稿略有出入=ASR 路固有错字（`data/sources/bs001/README.md` §2 在案），纯看音质。
3. A/B/C 渲染过 `--strict` 校验（voiceover↔SRT 逐字一致）；D 免 strict（A 路）。
4. **决策映射**：选定 → backlog #8 定档 + PLAN §7-7 签批；量产开闸后按定档参数走 #4。

## 四、复现（命令实录）

```
edge-tts --voice zh-CN-YunxiNeural --file data\sources\bs001\voiceover.txt --write-media <tmp>\audio-yunxi.mp3 --write-subtitles <tmp>\subs-yunxi-raw.srt
python src\render\srt_fix.py --in <tmp>\subs-yunxi-raw.srt --out <tmp>\subs-yunxi.srt
python src\render\render_card_video.py --cards data\sources\bs001\cards.json --srt <tmp>\subs-yunxi.srt --voiceover data\sources\bs001\voiceover.txt --strict --audio <tmp>\audio-yunxi.mp3 --out output\renders\bs-001-voice-B-yunxi.mp4
```
（C 同构换 Yunjian；D=piper 合成→whisper 对轴→免 strict 渲染；中间件存 `output/renders/.samples-tmp/`）
