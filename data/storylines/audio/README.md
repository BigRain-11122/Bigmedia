# 有声线台账（L-音 · data/storylines/audio/）

> 正典=`docs/city-storylines-charter.md` §1/§4/§5（有声线编制/路径/门禁映射）。产线=循环既有 TTS 链直接复用（research/city-storylines-research-v1.md §5）：`emotive_tts --cyber light --human 42`·机器叙述者=城市自述视角。mp3 产物 gitignored（charter §4 口径·本 README 即记账）。

## 台账

| 件 | 时长 | cues | TTS 参数 | S2 机检 | 状态 |
|---|---|---|---|---|---|
| SC-001-01-v1.mp3《硅基城市·第一章·立国日》 | 3:50.4（ffprobe 230.422s） | 13 | zh-CN-YunyangNeural+cyber light+human 42（产线默认） | ai_feel 0 FAIL 0 WARN（gaps 12 处 0.239-0.558s varied/pacing CV 0.396/prosody 8 档/copy CV 0.425） | 在链·E8 前 |

## 门禁记录（charter §5 有声线四检·M4 口径）

- **红线五条**：✓ 章节名纪实零标题党/七条来源全可溯/无虚构添加（beats=网文稿正文逐字拍化·预告口播化去括号=结构处理）
- **三重标注**：✓ 虚实级=纪实线声明音频开头内置（cue01「基于硅基城市真实事件改编」）+AIGC 级=音频开头显著内置（cue01「本节目由 AI 参与生成」·AIGC 标识办法）+来源级=继承文本（cue01「完整来源清单见图文页」→`data/storylines/novel/SC-001-01-v1.md` 文末七条）
- **来源继承**：✓ 同文本逐字（charter §3 一题三态·网文稿→有声稿同文本 TTS）
- **S2 机检**：✓ ai_feel 全绿（读数上行）；spec 面=音频时长 ffprobe 实测 3:50.4——单集 10-20min=〔通识假设〕未核验（research §2 卡点 U2），首章文本 1100 字固有长度如实·不硬凑（纪实线禁虚构）；层 1.8=纯音频无剪辑面 N/A

## 待办（拆细）

- E8 终审听审（首件有声听审定标：S2 席 ASR 事实词核验 R169 QC recipe 随批·Ollama 席对纯音频件评分维度首定）→ finished.md F 系登记
- 中间件目录 `sc001-01-v1-tmp/`（seg/gap/breath·批次闭收账惯例）——批闭即收

## 变更记录

- 2026-09-25: 台账立账（R222·#27 ①有声首集腿——beats 12 拍/13 cues/TTS light/S2 ai_feel 全绿/成品落位；CEO 令 O-20260925-0850-bm-a 循环份额首件）
