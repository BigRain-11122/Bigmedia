

---

# OH-20260926-bigstream — 开源收获轮·BigStream 首窗切片 2

- **窗**：首窗 2026-09-26 21:40 → 2026-09-29 21:40｜本切片=2026-09-27 03:1x（BigStream OSLoop R458·P-20260926-08·R432 下窗指针三向换刀执行）
- **实搜面（≥2 处实录·本切片 3 刀=切片帽内）**：①GitHub API search `pysubs2+subtitle`（7 命中·top6 全读：tkarabela/pysubs2〔440★·MIT·pushed 2026-08-16·Python 字幕编辑库 SRT/ASS/SSA/VTT/MicroDVD/TTML/MPL2·docs=readthedocs〕/EutropicAI/yuisub〔28★·GPL-3.0·动画字幕 LLM 翻译〕/tin2tin/import_subtitles〔11★·无 license·Blender 插件·pushed 2023〕/SomeBottle/Konnyaku〔5★·MIT·LLM 字幕翻译〕/azratul/llm-subs〔3★·GPL-3.0·LLM 字幕翻译+ASS 回插〕/maicon1998/offline-subtitle-translator〔0★·MIT〕）②GitHub API search `edge-tts`（**2950 命中**·top8 全读：abus-aikorea/voice-pro〔12938★·GPL-3.0·Gradio WebUI TTS+克隆+Whisper 大杂烩〕/rany2/edge-tts〔12078★·**核心库=本司产线在役**·pushed 2026-03〕/cosin2077/easyVoice〔2327★·无 license·超长文本多角色 TS 工具〕/travisvn/openai-edge-tts〔2112★·GPL-3.0·OpenAI 兼容端点壳〕/Vincentwei1021/anything2explainer〔2088★·NOASSERTION·Claude Code 技能·Remotion 黑底讲解视频管线〕/Agents365-ai/video-podcast-maker〔1635★·MIT·pushed 2026-09-14·Topic→4K 解说视频·本地 edge TTS+Remotion+五平台预设=B站/YouTube/小红书/抖音/视频号〕/LuckyHookin/edge-TTS-record〔1370★·无 license·浏览器录音工具·pushed 2024-11〕/ABexit/ASR-LLM-TTS〔1279★·Apache-2.0·ASR+LLM+TTS 全家桶〕）③Ollama library 索引页 ollama.com/library（**JS 壳死面如实记**：fetch 返回单模型残片=dolphin-mistral 2 年旧档·非全库索引·零新断言零爬升=不恋战律执行）。
- **候选（五门评估 2 项）**：**①pysubs2**（源=https://github.com/tkarabela/pysubs2·MIT·440★）
  - 契合门 **无现时工位→parked**：唯一映射面=R9 在案评估注「drawtext 多行=块居中行内左对齐（无逐行居中）→可评估换 ASS」=pysubs2 作 SRT→ASS 桥+libass 逐行居中；但该注 200+ 轮零激活——CEO 目检/E4/E8/帧验三律从未旗字幕对齐·v12-fleet+v15 重制带 46 件 drawtext 栈全绿·D-BS-03 视觉规格+§4.5/§5.5 系列件全锚定 drawtext 管线=**无痛点无工位**（「替谁省什么」答不出）。
  - 反重复门 命中不采：SRT 解析/钳重叠（srt_fix R-B）/CJK 折行 em 预算（render_card_video R9·前置适配 R380+·层 1.8 机检）全自研在役。
  - 许可门 PASS-in-principle：MIT=直用（未采故未验源页原文·未验明=不用律照守）。
  - 健康门 强：440★·56 forks·pushed 2026-08-16（~6 周）·readthedocs 在。
  - 成本/安全门 轻：纯 Python 薄依赖·无模型无外发。
  - **重开条件**：CEO/评审若旗字幕逐行对齐→ASS/libass 迁移预评启用（pysubs2=桥首选）。
  **②video-podcast-maker**（源=https://github.com/Agents365-ai/video-podcast-maker·MIT·1635★·pushed 2026-09-14）
  - 契合门 **FAIL（零第二管线工位）**：同域最近件（Topic→旁白视频·本地 edge TTS·五平台=我司同阵）但=Remotion/React/Node 全栈管线替换——我司 M2-M3 链=ffmpeg/drawtext 自研 297 测试+S2 三门+E8+CEO 目检批准视觉规格·双管线=双建禁令。
  - 反重复门 命中不采（同上主判）；**对标价值注记**：manifest-based Asset Engine/平台预设组织=自进清单 B5 对标池合法供源（策略思想类收获不走本机制采面→只供源留档）。
  - 许可门 PASS-in-principle（MIT）；健康门 强（1635★·170 forks·2026-09-14 push）；成本/安全门 重（Node 工具链=产线外栈）。
- **姊妹线咬合注记（禁双轨·只供源）**：anything2explainer（NOASSERTION=未验明不用+Claude Code 技能形态→P-20260926-01 技能律只供源）；voice-pro/openai-edge-tts/llm-subs/yuisub=GPL-3.0 禁入产品交付链（许可门登记簿口径）；easyVoice/edge-TTS-record=无 license 未验明不用。模型类零新断言（Ollama 面=JS 壳死面）=P-17/P-19 无触发零拉取。edge-tts 核心库在役健康续证（12078★·维护中）=产线基础面正向证据·非新采。
- **采用→落点**：**零采用**（本切片）——候选 2 项经五门评估全 parked，无工作流变更。
- **parked+理由**：pysubs2=parked（契合门无现时工位+反重复门自研覆盖·重开条件在案）｜video-podcast-maker=parked（零第二管线工位+栈外·B5 对标供源留档）。
- **下窗指针**：切片 3（窗内 ≤09-29 21:40·窗关前必做）换刀方向=①Ollama library 定向直连模型页（索引壳已判死→绕索引直取如 /library/qwen3）②`libass ass` CLI 渲染工艺对照（切片 2 pysubs2 重开条件的技术预研位）③B5 对标面补刀（video-podcast-maker 深读位）——礼貌节流每切片 ≤3 刀。

## 切片 2 结论应用表（research-protocol 强制·无表=未交付）

| # | 发现 | 判定 | 落点（工作流变更） | 后续 |
|---|------|------|------|------|
| 1 | pysubs2（MIT·440★·字幕格式库） | 五门评估→契合门无现时工位→parked | 无变更（不采） | 重开条件=字幕逐行对齐被旗（CEO/评审）→ASS/libass 迁移预评 |
| 2 | video-podcast-maker（MIT·1635★·同域 Remotion 管线） | 零第二管线工位→不采·对标供源 | 无变更 | B5 对标池留档（manifest Asset Engine/平台预设组织） |
| 3 | Ollama library 索引页 | JS 壳死面实录 | 无变更 | 切片 3 定向直连模型页换刀 |
| 4 | edge-tts 核心库健康续证 | 在役确认（非新采） | 无变更 | 产线基础面证据（403 波次处置口径 research v1.2 在案） |

- 三律自检：①业务契合=「替谁省什么」硬问收口（pysubs2=重开条件制·video-podcast-maker=零工位）②不重复造轮子=反重复门两候选皆命中自研覆盖/在役栈③科学使用=五门全过才采（本切片零采用=诚实零发现面）。
- 送达：本文件=R458 切片 2 落账（BigStream 仓 commit 含 P-20260926-08·backlog #70 留痕行）；本实体单文件·集团仓他件零接触（跨仓写禁令 CEO 令级例外·oss-harvest §六·一窗一文件多切片续写）。
