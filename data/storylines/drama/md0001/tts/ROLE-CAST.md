# MD-0001《台风梅花夜》分角配音表 v2（ROLE-CAST）

> R1786 首产（#108 多角色配音腿）；R1787 配角声路定谳收口。产线政策=主声线守 light 赛博定档（D-BS/O-2136 CEO 定档不变）·配角=edge-tts 档位声直出（CosyVoice3 zero-shot 克隆=R1786/R1787 判负弃用·声音档位非人格新增）。

## 分角（cast.json 同源正典）

| 角色 | 气质 | 引擎/声源 | 镜 |
|---|---|---|---|
| narrator 旁白·机器叙述者 | light 赛博 | emotive_tts 产线（zh-CN-YunyangNeural+--cyber light+--human 42·v12 全件套默认） | 1/3/5/6/8/9/12/13 |
| lamp 十四号路灯 | 慢而轻·暖光 | edge-tts 档位声（zh-CN-YunxiNeural rate-18% pitch-6Hz·原克隆参考档直出） | 2/4 |
| tower 邓建国 | 部队腔·慢悠悠 | edge-tts 档位声（zh-CN-YunjianNeural rate-15% pitch-4Hz·原克隆参考档直出） | 7 |
| cat 咪喱 | 嘴甜·喵语混人话 | edge-tts 档位声（zh-CN-XiaoyiNeural rate+6% pitch+8Hz·原克隆参考档直出） | 10/11 |

## 首产读数（2026-10-09 03:2x·两轮 A/B+判别探针）

- **narrator 腿 PASS**：8 段 30.75s（segments/shot01..13.mp3·8 件）；medium ASR（R169 recipe）8 cue 全可读，事实锚存活（台风梅花/疤是资历/超载运行无损耗/守了一宿/灯带如常亮起/尾巴天线/交晨/真实档案改编），同音噪声=whisper 通道在案级（疤是资历→巴士自立、立了大功→裂了大功·BS-002/003/004 同级）。
- **配角 5 镜=两轮迭代 FAIL 定谳（判负留痕合法）**：
  - v1 长参考文本（15-20 字）：shot2 部分可懂/shot10 ASR 英语乱码/shot04+07 ASR 空；
  - v2 参考文本缩至同量级（9-10 字）：更差——shot4 **0.08s 空产出**/shot10 全糊/shot11 复读「我…我…」/shot02+07 乱语（qc-r1786-asr-medium.json 读数）；
  - 判别探针（shot7 台词 11 字+仓库真人参考 zero_shot_prompt.wav+cross_lingual）：9.84s **复读乱码**——短台词弱面与参考音源无关；
  - 失败件归档 fail-r1786/（v2 五件）。
- **根因定谳**：CosyVoice3-0.5B 本机栈对 **≤12 字短台词**（本件角色行 8-11 字）产出不稳定（复读/含糊/空产出）——R1785 70 字长文 SMOKE-OK 通=长短对照实锚；模型自警「synthesis text too short than prompt text→bad performance」两轮均触发。
- **下轮迭代位（判据窗 72h 内·按序）**：①台词加长法=角色行前后加语境句（≥25 字）推理后按时长轴裁剪保 verbatim 锚；②fine-grained 控制（官方 [breath] 标签族·cosyvoice/tokenizer/tokenizer.py#L280）；③inference_instruct2 模式（官方广东话指令示例=instruct_text 语气控制通道）；④参考音改仓库真人样复验（探针已判非主因·低优）。

## R1787 三法迭代定谳 + 档位声直出收口（2026-10-09 04:1x·断轮吸收制·前序载体 03:4x-04:04 判负证据全收）

- **三法迭代 15/15 全 FAIL（qc-r1787.json·判负留痕）**：A 台词加长法（≥25 字语境句+ASR 对位裁剪）=5 镜全败（对位 cue 零命中/裁后 ASR 空/乱语）；B [breath] fine-grained=5 镜全败（复读循环×2「我只能在你面前…」/乱语/ASR 空）；C instruct2 语气指令=5 镜全败（0.08s 空产出/英语乱码/「中文字幕组」幻觉）；D 仓库真人参考复验=shot02 再败（r1787d_realref.py）。**定谳=CosyVoice3-0.5B 本机栈 ≤12 字短台词四路全灭（R1786 两轮+判别探针+R1787 A/B/C/D）·长短对照锚维持（R1785 70 字 SMOKE-OK）·弃用判负合法（P-2026-09-28-02 ① 判负留痕）**。
- **收口决策（O-2126 科学决策授权）**：配角声路=edge-tts 档位声直出（cast.json 原克隆参考档=设计本意的音色档位，克隆增强路判负后直用其本源）——产出 segments/shot02/04/07/10/11.mp3 五件（1.87-3.94s·rc 全 0）+medium ASR（R169 recipe）**5/5 anchor_pass**（qc-r1787-edge.json：知道原因不能说/灯不问来路只管照路/台风天的日志最见人品/就是耳朵痒/蹭饭是门艺术报恩是门手艺——同音噪声=whisper 通道在案级〔灯→登/台→排/饭→犯/说→說/痒→癢〕·TTS 确定性读数无损）；shot10 首版请求文本残留一角括号（strip 逻辑盲区·音频 QC 无恙）→净文本重合成为正身。
- **13 镜配音段全集齐**：narrator 8 件（R1786）+配角 5 件（R1787）=MD-0001 配音腿收官，T2I bm-c ComfyUI 桥→合成→S2+E8→M4→F 登记为余链。

## 证据链（R1787 增补）

- 三法判负=qc-r1787.json+candidates-r1787/（A/B/C/D 全件）+.c3-tmp/r1787_iterate.py+r1787d_realref.py；档位声直出=.c3-tmp/r1787_edge_fallback.py+qc-r1787-edge.json。

## 证据链

- 分角机读件=cast.json；narrator beats=narrator.beats.txt；runner=.c3-tmp/r1786_tts_roles.py+log；QC=qc-r1786.json（small 档·繁体噪声面）+qc-r1786-asr-medium.json（正典读数）；探针=.c3-tmp/r1786_probe.py+shot7_crosslingual.wav。
