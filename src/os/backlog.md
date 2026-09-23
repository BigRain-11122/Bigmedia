# BigStream OS 循环任务板（backlog）

> 一行一任务，循环从上往下取第一条未完成项；完成=标 `[done YYYY-MM-DD]` 并 commit。新任务=追加到末尾；P1 级提案入板须标 `[needs-CEO]`。
> 2026-09-23 重排：CEO 令 O-20260923-1602-bm-a 复工主线置顶（生产暂停已解除）；原 #4/#5/#6 顺延为 #8/#7/#6。

0. [done 2026-09-23] O-1719 调研远征令执行（R10·五件全落地）：①O 件落册随轮 commit ②`research/local-stack-research-v1.md` v1.0（TTS/STT/文生图三站官方 A 级证据+本机 M1 实测锚点·卡点 T1-T5 台账在件 §6）③`docs/research-protocol.md` v1.0（源分级/零断言/台账/限时/双线归口五律·R4-R8+本轮实践固化）④m2-local-stack 升 v1.1（撤回「可载 SDXL 级」无源断言）⑤C-18 入册 live
1. [done 2026-09-23] O-1602 主线①·用户调研 v1 续采（名单阶段收官 R8·aicoder 六平台 120 位线索池落 research §4·调研件现态 v1.3）：v1.2 已落（R7——aicoder 线索页破壳：B站+公众号 20+20 名单线索入 §4·线索级不作引用；trust.douyin.com/up-data.cn JS 壳空、pro.weixin.qq.com 连接失败如实入 §6）——R8 后实况（aicoder 名单通道已耗尽·YouTube 无该站子报告须另寻通道；官方原文通道卡点 P2/P3/P4/P6/D1 移交 §6 台账常驻跟踪·通道解锁或账号到位即采；逐人四件对照=账号开通后·§6 B1 替代通道在案）；v1.2 时点余项清单＝ P6 公众号官方原文、P2 抖音信任中心落地页（官方转载存档通道）、P3 B站公示页全文（JS 通道）、P4 小红书、D1 微信侧报告 + B1 余下三平台名单（aicoder reports/shipinhao·douyin·xiaohongshao.html）+全量逐人四件对照（账号开通后平台内检索）
2. [done 2026-09-23] O-1602 主线②·人设卡：`docs/persona-jason.md` v1.0 已落（身份卡/出镜形象嗓音/内容四柱含团结引擎第四柱/平台适配/出镜红线/受众对位 research §2.3）——范式引用 Biggame 人设卡结构律（引用不复制）；待 Qiqi 抽样终审；backlog#5 复检由此解锁
3. [done 2026-09-23] O-1602 主线③·素材生产线选型——交付=`docs/m2-local-stack.md` v1.0（CEO 本地算力优先令 O-20260923-1609-bm-a·本机实况盘点+四站本地方案+显存分时+PoC 阶梯）+缺口清单（ComfyUI 未装→首发走字卡/实录·TTS 纯本地替代 Piper 待 PoC·云兜底逐单报批）——已随 O-1609 回执呈 CEO
4. O-1602 主线④·存量弹药：✅ CEO 裁定 **N=6**（16:35 决裁·O-20260923-1602 批次2）——成片/半成品 6 条入库（账号到位即发·成品入库须过 M4·素材产线=本地算力链 PoC 先行）
5. [done 2026-09-23] 封存 10 稿人设对齐复检——交付=`docs/persona-alignment-v1.md`（10/10 存活·全部小改级·BS-005 升第四柱增强位·弹药映射建议=BS-001~005 成片×5+团结引擎增强版×1=N6）；动稿纪律=口吻改写批次须重过 lint+M4+Qiqi 抽样审
6. 自动周报生成器：src/os/state.json + git log → 周报 md（数据分析部归口·capabilities C-09）
7. 视频号 4 稿口播裁至 ≤60s（blocked-by-pause 已解除·排 #5 复检后）
8. M2 TTS 音色选型（参数随 docs/persona-jason.md 定·零预算链路默认·不再按三案）
9. O-1609 主线·M2 本地算力链 PoC：**R-A done 2026-09-23**（`src/render/render_card_video.py` FFmpeg 时间线渲染器——口播 txt+SRT+字卡 JSON→9:16 mp4·AIGC 标识常驻烧录=红线内置·CJK 折行防裁·voiceover↔SRT 一致性校验（--strict）·--audio 轨位留好待 R-B·18 测试用例全绿·BS-001 实渲染 1080×1920/58.8s 落 output/renders/·三段抽帧目检过）→ **R-B** edge-tts 音色参数表+试录样件（音色随 docs/persona-jason.md 定·样件落 `data/sources/tts-samples/`·**piper1-gpl** 本地替代备份验证——旧 Piper 仓 2025-10-06 官方归档·后继 `pip install piper-tts`·zh_CN huayan 候选·证据=research/local-stack-research-v1.md §1）→ **R-C** faster-whisper 字幕对轴（口播 wav→SRT→替换 bs001 占位 SRT 入流水·逐行居中可评估换 ASS）——m2-local-stack.md §4 阶梯照走·显存分时礼仪 §2 照守（本渲染纯 CPU 实测 0 VRAM）
