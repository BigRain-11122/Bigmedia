# output/renders 产线测试件台账（Render Test-Piece Ledger）

> O-20260923-1756-bm-a：本目录只放产线测试件（渲染试跑/TTS 试录/字幕对轴/样件产出），一律标注「测试件·非成品」，不入发布队列（M5 闸不变）。
> 探针 `src/readiness.py` 逐件核验本表标注（缺标注=FAIL）；媒体二进制不入 git（.gitignore `*.mp4` 等），以本表为账。

| 文件 | 标注 | 说明 |
|---|---|---|
| bs-001-card.mp4 | 测试件·非成品 | R9 渲染试跑 v1：字卡视频（1080×1920·58.8s·无音轨·ffprobe 实证） |
| bs-001-card-v2.mp4 | 测试件·非成品 | R12 音轨重渲 v2：Yunyang 试配音轨+真轴 SRT（1080×1920·59.93s·aac 24k）——兼 O-1830 音色对比组 A（Yunyang 沉稳档） |
| bs-001-voice-B-yunxi.mp4 | 测试件·非成品 | O-1830 音色对比组 B：Yunxi 全长试配（55.97s·索引=data/sources/samples-review.md） |
| bs-001-voice-C-yunjian.mp4 | 测试件·非成品 | O-1830 音色对比组 C：Yunjian 全长试配（57.53s·同上） |
| bs-001-voice-D-huayan-local.mp4 | 测试件·非成品 | O-1830 纯本地备份组 D：piper huayan 全长试配（48.83s·ASR 对轴路·免 strict·错字在案 bs001/README §2） |

> 中间件（独立临时音轨/SRT）存 `output/renders/.samples-tmp/`——O-1830 复现用（samples-review.md §四声明）·非渲染成品·不入本表。
