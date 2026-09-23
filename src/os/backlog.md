# BigStream OS 循环任务板（backlog）

> 一行一任务，循环从上往下取第一条未完成项；完成=标 `[done YYYY-MM-DD]` 并 commit。新任务=追加到末尾；P1 级提案入板须标 `[needs-CEO]`。
> 2026-09-23 重排：CEO 令 O-20260923-1602-bm-a 复工主线置顶（生产暂停已解除）；原 #4/#5/#6 顺延为 #8/#7/#6。

1. O-1602 主线①·用户调研 v1 续采：research/user-research-v1.md v1.0 已落（§2 受众画像 CNNIC 官方源+§3.1 YouTube 官方机制已采）——余项=§6 采集台账 P1-P6（视频号/抖音/B站/小红书/公众号官方机制文档·JS 壳受阻·替代通道在表）+ B1 对标创作者 benchmark×5（逐人 URL+数据+打法+选题结构·无源不硬编）
2. O-1602 主线②·人设卡：docs/persona-jason.md——Jason 本人出镜 build-in-public（一人+AI 劳动力+机队造 FLUX 超体宇宙）·人设卡+记忆点+内容三柱·Biggame《人设_首席制作人.md》范式引用不复制（令序：调研夯实后开工·数据已可支撑首版）
3. O-1602 主线③·素材生产线选型：零预算 AI 管线（文案/配音/画面/数据可视化·本机 ComfyUI/Ollama 同源复用）→ 选型清单+素材缺口清单报 CEO（C-14）
4. O-1602 主线④·存量弹药：成片/半成品 ≥N 条入库（提案 N=6 [needs-CEO 裁]·账号到位即发·成品入库须过 M4）
5. 封存 10 稿人设对齐复检：新令人设=Jason 本人出镜 vs 旧稿三案口吻——只读复检出对齐标注表；动稿须过 M4
6. 自动周报生成器：src/os/state.json + git log → 周报 md（数据分析部归口·capabilities C-09）
7. 视频号 4 稿口播裁至 ≤60s（blocked-by-pause 已解除·排 #5 复检后）
8. M2 TTS 音色选型（参数随 docs/persona-jason.md 定·零预算链路默认·不再按三案）
9. O-1609 主线·M2 本地算力链 PoC：`src/render/` FFmpeg 时间线脚本（口播 txt+SRT+字卡模板→9:16 mp4 最小闭环·纯本地零安装）→ 三案音色 edge-tts 参数表+试录样件（A/B/C 各一档·`data/sources/tts-samples/`）→ faster-whisper 字幕对轴脚本——全程 m2-local-stack.md §4 PoC 阶梯 R-A→R-B→R-C 逐项交付·显存分时礼仪 §2 照守
