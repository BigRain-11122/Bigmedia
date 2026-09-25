# 有声线台账（L-音 · data/storylines/audio/）

> 正典=`docs/city-storylines-charter.md` §1/§4/§5（有声线编制/路径/门禁映射）。产线=循环既有 TTS 链直接复用（research/city-storylines-research-v1.md §5）：`emotive_tts --cyber light --human 42`·机器叙述者=城市自述视角。mp3 产物 gitignored（charter §4 口径·本 README 即记账）。

## 台账

| 件 | 时长 | cues | TTS 参数 | S2 机检 | 状态 |
|---|---|---|---|---|---|
| SC-001-01-v1.mp3《硅基城市·第一章·立国日》 | 3:50.4（ffprobe 230.422s） | 13 | zh-CN-YunyangNeural+cyber light+human 42（产线默认） | ai_feel 0 FAIL 0 WARN（gaps 12 处 0.239-0.558s varied/pacing CV 0.396/prosody 8 档/copy CV 0.425） | **成品·F-008（R223 E8 终审听审七席 9.0+ASR 终轨回听事实词全存活）** |

## 门禁记录（charter §5 有声线四检·M4 口径）

- **红线五条**：✓ 章节名纪实零标题党/七条来源全可溯/无虚构添加（beats=网文稿正文逐字拍化·预告口播化去括号=结构处理）
- **三重标注**：✓ 虚实级=纪实线声明音频开头内置（cue01「基于硅基城市真实事件改编」）+AIGC 级=音频开头显著内置（cue01「本节目由 AI 参与生成」·AIGC 标识办法）+来源级=继承文本（cue01「完整来源清单见图文页」→`data/storylines/novel/SC-001-01-v1.md` 文末七条）
- **来源继承**：✓ 同文本逐字（charter §3 一题三态·网文稿→有声稿同文本 TTS）
- **S2 机检**：✓ ai_feel 全绿（读数上行）；spec 面=音频时长 ffprobe 实测 3:50.4——单集 10-20min=〔通识假设〕未核验（research §2 卡点 U2），首章文本 1100 字固有长度如实·不硬凑（纪实线禁虚构）；层 1.8=纯音频无剪辑面 N/A

## 状态（R223 收官）

- **E8 终审听审毕+F-008 登记**（`output/finished.md`·成品库第七件·有声线 L-音 首件·编号避让 F-007=BS-005e 预留位）——**纯音频件评分维度首定**（E7→声音质感位/E8→节奏工艺位/S1→同文本律继承位·`docs/reviews/review-20260925-sc00101-v1.md`）；S2 席 ASR 终轨回听=R169 QC recipe 本轮新跑（事实词全存活·同音噪声 ≈30 处=专名密度最高件·字幕轨=edge-tts 精确直出零损）
- E4 参考仪在飞（PID 61972·1500s 窗·下轮回填·追加制·非拦截）
- 中间件 `sc001-01-v1-tmp/`（asr-check.srt+e4_call.py/e4-result 落位+seg/gap/breath）=批闭收账随 R223 commit（R150/R201 惯例）

## 变更记录

- 2026-09-25: 台账立账（R222·#27 ①有声首集腿——beats 12 拍/13 cues/TTS light/S2 ai_feel 全绿/成品落位；CEO 令 O-20260925-0850-bm-a 循环份额首件）
- 2026-09-25: R223 收官——E8 终审听审首件定标（七席全 9.0+S2 ASR 终轨回听事实词全存活·同音噪声 ≈30 处〔字位 2.7%·DD 同带〕·字幕轨零损）→**F-008 登记**（编号避让 F-007=BS-005e 预留位）；E4 参考仪在飞下轮回填
