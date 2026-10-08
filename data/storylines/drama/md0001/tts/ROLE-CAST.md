# MD-0001《台风梅花夜》分角配音表 v1（ROLE-CAST）

> R1786 首产（#108 多角色配音腿）。产线政策=主声线守 light 赛博定档（D-BS/O-2136 CEO 定档不变）·配角多声纹=CosyVoice3 zero-shot 克隆·声音档位非人格新增。

## 分角（cast.json 同源正典）

| 角色 | 气质 | 引擎/声源 | 镜 |
|---|---|---|---|
| narrator 旁白·机器叙述者 | light 赛博 | emotive_tts 产线（zh-CN-YunyangNeural+--cyber light+--human 42·v12 全件套默认） | 1/3/5/6/8/9/12/13 |
| lamp 十四号路灯 | 慢而轻·暖光 | CosyVoice3 zero-shot（参考音=edge-tts zh-CN-YunxiNeural rate-18% pitch-6Hz） | 2/4 |
| tower 邓建国 | 部队腔·慢悠悠 | CosyVoice3 zero-shot（参考音=edge-tts zh-CN-YunjianNeural rate-15% pitch-4Hz） | 7 |
| cat 咪喱 | 嘴甜·喵语混人话 | CosyVoice3 zero-shot（参考音=edge-tts zh-CN-XiaoyiNeural rate+6% pitch+8Hz） | 10/11 |

## 首产读数（2026-10-09 03:2x·两轮 A/B+判别探针）

- **narrator 腿 PASS**：8 段 30.75s（segments/shot01..13.mp3·8 件）；medium ASR（R169 recipe）8 cue 全可读，事实锚存活（台风梅花/疤是资历/超载运行无损耗/守了一宿/灯带如常亮起/尾巴天线/交晨/真实档案改编），同音噪声=whisper 通道在案级（疤是资历→巴士自立、立了大功→裂了大功·BS-002/003/004 同级）。
- **配角 5 镜=两轮迭代 FAIL 定谳（判负留痕合法）**：
  - v1 长参考文本（15-20 字）：shot2 部分可懂/shot10 ASR 英语乱码/shot04+07 ASR 空；
  - v2 参考文本缩至同量级（9-10 字）：更差——shot4 **0.08s 空产出**/shot10 全糊/shot11 复读「我…我…」/shot02+07 乱语（qc-r1786-asr-medium.json 读数）；
  - 判别探针（shot7 台词 11 字+仓库真人参考 zero_shot_prompt.wav+cross_lingual）：9.84s **复读乱码**——短台词弱面与参考音源无关；
  - 失败件归档 fail-r1786/（v2 五件）。
- **根因定谳**：CosyVoice3-0.5B 本机栈对 **≤12 字短台词**（本件角色行 8-11 字）产出不稳定（复读/含糊/空产出）——R1785 70 字长文 SMOKE-OK 通=长短对照实锚；模型自警「synthesis text too short than prompt text→bad performance」两轮均触发。
- **下轮迭代位（判据窗 72h 内·按序）**：①台词加长法=角色行前后加语境句（≥25 字）推理后按时长轴裁剪保 verbatim 锚；②fine-grained 控制（官方 [breath] 标签族·cosyvoice/tokenizer/tokenizer.py#L280）；③inference_instruct2 模式（官方广东话指令示例=instruct_text 语气控制通道）；④参考音改仓库真人样复验（探针已判非主因·低优）。

## 证据链

- 分角机读件=cast.json；narrator beats=narrator.beats.txt；runner=.c3-tmp/r1786_tts_roles.py+log；QC=qc-r1786.json（small 档·繁体噪声面）+qc-r1786-asr-medium.json（正典读数）；探针=.c3-tmp/r1786_probe.py+shot7_crosslingual.wav。
