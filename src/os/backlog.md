# BigStream OS 循环任务板（backlog）

> 一行一任务，循环从上往下取第一条未完成项；完成=标 `[done YYYY-MM-DD]` 并 commit。新任务=追加到末尾；P1 级提案入板须标 `[needs-CEO]`。
> 2026-09-23 重排：CEO 令 O-20260923-1602-bm-a 复工主线置顶（生产暂停已解除）；原 #4/#5/#6 顺延为 #8/#7/#6。

1. O-1602 主线①·用户调研 v1 续采：v1.1 已落（§3.2 视频号官方披露✅ + §3.3 B站官方公示页+Q3 财报 AI 数据✅ + §4 对标池通道已核·R6）——余项=§6 台账 P6 公众号文档中心首试、P2 抖音信任中心落地页、P3 B站公示页全文（JS 通道）、P4 小红书、D1 微信侧报告 + B1 对标创作者 benchmark 逐人四件×5（up-data.cn 对照平台页·可信级标注·无源不硬编）
2. [done 2026-09-23] O-1602 主线②·人设卡：`docs/persona-jason.md` v1.0 已落（身份卡/出镜形象嗓音/内容四柱含团结引擎第四柱/平台适配/出镜红线/受众对位 research §2.3）——范式引用 Biggame 人设卡结构律（引用不复制）；待 Qiqi 抽样终审；backlog#5 复检由此解锁
3. [done 2026-09-23] O-1602 主线③·素材生产线选型——交付=`docs/m2-local-stack.md` v1.0（CEO 本地算力优先令 O-20260923-1609-bm-a·本机实况盘点+四站本地方案+显存分时+PoC 阶梯）+缺口清单（ComfyUI 未装→首发走字卡/实录·TTS 纯本地替代 Piper 待 PoC·云兜底逐单报批）——已随 O-1609 回执呈 CEO
4. O-1602 主线④·存量弹药：✅ CEO 裁定 **N=6**（16:35 决裁·O-20260923-1602 批次2）——成片/半成品 6 条入库（账号到位即发·成品入库须过 M4·素材产线=本地算力链 PoC 先行）
5. [done 2026-09-23] 封存 10 稿人设对齐复检——交付=`docs/persona-alignment-v1.md`（10/10 存活·全部小改级·BS-005 升第四柱增强位·弹药映射建议=BS-001~005 成片×5+团结引擎增强版×1=N6）；动稿纪律=口吻改写批次须重过 lint+M4+Qiqi 抽样审
6. 自动周报生成器：src/os/state.json + git log → 周报 md（数据分析部归口·capabilities C-09）
7. 视频号 4 稿口播裁至 ≤60s（blocked-by-pause 已解除·排 #5 复检后）
8. M2 TTS 音色选型（参数随 docs/persona-jason.md 定·零预算链路默认·不再按三案）
9. O-1609 主线·M2 本地算力链 PoC：`src/render/` FFmpeg 时间线脚本（口播 txt+SRT+字卡模板→9:16 mp4 最小闭环·纯本地零安装）→ edge-tts 音色参数表+试录样件（音色随 docs/persona-jason.md 定·样件落 `data/sources/tts-samples/`）→ faster-whisper 字幕对轴脚本——全程 m2-local-stack.md §4 PoC 阶梯 R-A→R-B→R-C 逐项交付·显存分时礼仪 §2 照守
