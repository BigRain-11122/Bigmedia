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

## 五、赛博组 v8（O-20260923-2136-bm-a·2026-09-23 21:5X）

> CEO 令「声音更加赛博一点，机器人一点，文案也是」——**A-D 拟人音色组被本组接替为现行候选**（听感保留对照）。
> 同稿（v8 系统日志体·机器叙述者「三号公司 AI 本机」）·同视觉（v7-vis 模板）·同 BGM ducking，唯一变量=**赛博档位**。

| 件 | 档位 | 文件 | 听点 |
|---|---|---|---|
| **light** | 轻度赛博（保情感抑扬+轻机械纹理） | `output/renders/bs-001-v8-cyber-light.mp4`（51.6s） | 最接近人声的冷叙述——若嫌 mid 太机器，听这件 |
| **mid** | **标准机器人（推荐位）** | `output/renders/bs-001-v8-cyber-mid.mp4`（53.2s） | 音高压平+金属颤音——机检实证事实词零损·评审推荐档 |
| **full** | 深度合成（极端参考端） | `output/renders/bs-001-v8-cyber-full.mp4`（54.9s） | 终端合成音质感——够赛博但 ASR 实测打糊事实词（一名/0元/瓶酒），不建议量产 |

- **可懂度分级证据**：三档 ASR 转写比对（faster-whisper·`asr-check.srt`）——light/mid=同 whisper-small 固有同音字噪音；full=真实损耗（详见 `docs/reviews/review-20260923-bs001-v8.md` §一）。
- **文案同步转体**：机器叙述者+系统日志体（系统启动/检测到/自动唤醒/转发指令）——「这条视频就是我剪的」机器自指梗；正典=`docs/copy-craft.md` §2.6。
- **决策映射**：CEO 拣音定档 → 锁 `--cyber` 档位为产线默认（backlog #8 更新）+PLAN §7-7 签批；整改清单（人味补钩/数字锚前移/视觉赛博同步）在 v8 评审台账 §三，待拣音后一并执行。

### 复现（命令实录·赛博组）

```
python src\render\emotive_tts.py --beats data\sources\bs001\voiceover-v8-cyber.beats.txt --voice zh-CN-YunyangNeural --out output\renders\.v8-mid --cyber mid --template output\renders\.v7vis-tmp\cards-vis.json --order "O-20260923-2136-bm-a (cyber voice dial + system-log copy)"
:: BGM sidechain ducking（$T=字卡末拍+0.8s 尾）
ffmpeg -y -i output\renders\.v8-mid\audio.mp3 -stream_loop -1 -i output\renders\.v7vis-tmp\bgm.mp3 -filter_complex "[1:a]volume=0.32[bg];[bg][0:a]sidechaincompress=threshold=0.03:ratio=10:attack=25:release=350[duck];[0:a]apad=whole_dur=$T[vp];[vp][duck]amix=inputs=2:duration=first:normalize=0[a]" -map "[a]" -t $T -c:a libmp3lame -qscale:a 4 output\renders\.v8-mid\audio-bgm.mp3
python src\render\render_card_video.py --cards output\renders\.v8-mid\cards.json --srt output\renders\.v8-mid\subs.srt --voiceover output\renders\.v8-mid\voiceover.txt --strict --audio output\renders\.v8-mid\audio-bgm.mp3 --out output\renders\bs-001-v8-cyber-mid.mp4
```
（light/full 同构换 `--cyber` 档与目录；ASR 听检=`python src\render\whisper_to_srt.py --audio <tmp>\audio.mp3 --out <tmp>\asr-check.srt`）

## 六、定档回执（2026-09-23 22:0X·CEO 点选）

- **声线定档=light 轻度赛博**；**叙述者=机器态确认**（系统日志体正典化）——拟人组 A-D 降为对照留档。
- **v9 定档版**=`output/renders/bs-001-v9-cyber-light.mp4`（59.31s·12 拍·beat2 增「爽的是我们，累的是他」人味反转·beat9 回归甩锅交账梗）——评审六席 9+ **PASS=放行候选**（`docs/reviews/review-20260923-bs001-v9.md`）·待 CEO 终审最后一键。
- 产线默认参数已锁：`emotive_tts --cyber light` + 机器叙述者拍稿（copy-craft §2.6）——mid/full 留档对照（full 禁量产·ASR 实证伤事实词）。

## 七、人味机制组 v10（O-20260923-2210-bm-a·2026-09-23 22:2X）

> CEO 令「从底层要去ai感觉，做好相关机制」——四站人味机制+机检门一次建成（规格=`docs/human-feel-spec.md`）。
> **v10 = v9 同稿同档位，唯一变量=人味机制**（干净 A/B）。

| 机制 | 实现 | v9（前） | v10（后） |
|---|---|---|---|
| 逐段微抖动 | `--human 42`（率±3%/音高±2Hz·种子可复现） | 每句同一副嗓 | 逐句微变 |
| 呼吸间隙 | 句间 0.12-0.48s 变长（时间线随实测重算零漂移） | **全零=节拍器感（机检 FAIL）** | 0.22-0.58s 变长（机检 PASS） |
| 呼吸声 | 长句后 50% 概率 brown-noise 呼吸 | 无 | 实装 |
| 房间底噪 | pink noise −44dB 床+微早期反射 | 真空 TTS | 有空气感 |
| 画面质感 | `--grain 7 --bg 0x0a0a0d`（颗粒+暗角+深灰底） | 纯黑模板指纹 | 制作感（抽帧验图在案） |

- **机检门首战**：`src/ai_feel_check.py` 对 v9 逮出 gap-zero（其余 pacing/prosody/copy 全 PASS——v9 文本结构本身健康）→ v10 全 PASS。
- v10 成片=`output/renders/bs-001-v10-humanfeel.mp4`（64.06s·19.1MB·strict 过·ASR 事实词全存活）。
- **诚实入账**：64.06s 超 60s 规格（呼吸空气 +4.75s）→ 立法**空气预算律**（60s 视频文本预算 ≤55s·L15）：量产版须先删文案后保空气，不靠压间隙换时长。

### 复现（命令实录·v10）

```
python src\render\emotive_tts.py --beats data\sources\bs001\voiceover-v9-cyber.beats.txt --voice zh-CN-YunyangNeural --out output\renders\.v10-light --cyber light --human 42 --template output\renders\.v7vis-tmp\cards-vis.json --order "O-20260923-2210-bm-a (human-feel dial, seed 42)"
:: BGM duck 同 §五实录（$T=64.06）
python src\render\render_card_video.py --cards output\renders\.v10-light\cards.json --srt output\renders\.v10-light\subs.srt --voiceover output\renders\.v10-light\voiceover.txt --strict --audio output\renders\.v10-light\audio-bgm.mp3 --grain 7 --bg 0x0a0a0d --out output\renders\bs-001-v10-humanfeel.mp4
python src\ai_feel_check.py --beats data\sources\bs001\voiceover-v9-cyber.beats.txt --srt output\renders\.v10-light\subs.srt
```

## 八、实录素材组（O-20260924-1115·2026-09-24 11:2X）

> CEO 令「Biggame总控 自行去录制画面，然后剪接出各个视频版本，试跑一次」——**素材层升级**：真实画面替代纯色底=去 AI 感最强一环（今晨审计缺口落地）。
> 录源=Biggame 像素小镇看板（窗口标题「Biggame · 小游戏公司总控」·自包含活数据页·只读打开）·45s 实录（gdigrab 区域采集·15fps）→blur-pad 竖版 1080×1920。复用 v10 全套（音频/字幕/字卡时间线=产线默认·反重复）。

| 件 | 剪辑路线 | 文件 | 听看点 |
|---|---|---|---|
| **live-A** | **实拍底版+字卡混合** | `output/renders/bs-001-live-A-pixelboard.mp4`（64.06s·31.7MB） | 真实录屏做底+H1/H2 字卡浮层+字幕+AIGC+grain7——「游戏公司实拍讲集团故事」 |
| **live-B** | **纯实录纪录片式** | `output/renders/bs-001-live-B-puredoc.mp4`（64.06s·15.8MB） | 同底版无字卡（`--no-cards`）·纯字幕+grain4——让画面自己说话 |

- **抽帧验图（A）**：层级成立（模糊底+清晰横幅+白字描边卡+底部字幕+左上 AIGC）；四条迭代输入如实入账：①字卡与游戏 UI 文字局部叠压 ②AIGC 对比度偏弱 ③字幕断词（「一名」拆行）④中段 UI 信息密度高只作氛围层。
- **机检**：ai_feel 全 PASS（复用 v10 时间线）；spec 门=时长 64.06s 超窗（同 v10 在案·机制演示件·量产按空气预算律 L15 裁）。
- **决策映射**：CEO 拣式（A 混合/B 纯实录/按选题选）→锁「实拍底版」为产线新默认层（`--bgvideo`）+四条迭代输入入整改队列。

### 复现（命令实录·实录组）

```
python src\render\record_screen.py --open-app "file:///C:/Users/sjs20/Desktop/FluxGroup/gaming/MiniGame/%E5%83%8F%E7%B4%A0%E5%B0%8F%E9%95%87%E7%9C%8B%E6%9D%BF.html#test" --title "小游戏公司总控" --seconds 45 --out data\sources\footage\biggame-cockpit-raw.mp4 --close
ffmpeg -y -i data\sources\footage\biggame-cockpit-raw.mp4 -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24:2[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p data\sources\footage\biggame-cockpit-vertical.mp4
python src\render\render_card_video.py --cards output\renders\.v10-light\cards.json --srt output\renders\.v10-light\subs.srt --voiceover output\renders\.v10-light\voiceover.txt --strict --audio output\renders\.v10-light\audio-bgm.mp3 --bgvideo data\sources\footage\biggame-cockpit-vertical.mp4 --grain 7 --out output\renders\bs-001-live-A-pixelboard.mp4
（B 版同构加 --no-cards 换 --grain 4 与 --out）
```
