# output/renders 产线测试件台账（Render Test-Piece Ledger）

> O-20260923-1756-bm-a：本目录只放产线测试件（渲染试跑/TTS 试录/字幕对轴/样件产出），一律标注「测试件·非成品」，不入发布队列（M5 闸不变）。
> 探针 `src/readiness.py` 逐件核验本表标注（缺标注=FAIL）；媒体二进制不入 git（.gitignore `*.mp4` 等），以本表为账。

| 文件 | 标注 | 说明 |
|---|---|---|
| bs-001-card-v2.mp4 | 测试件·非成品 | R12 音轨重渲 v2：Yunyang 试配音轨+真轴 SRT（1080×1920·59.93s·aac 24k）——兼 O-1830 音色对比组 A（Yunyang 沉稳档）；R9 无音轨 v1 已被本件取代清盘（盘上无此文件·R21 台账修红移行·历史在 git） |
| bs-001-voice-B-yunxi.mp4 | 测试件·非成品 | O-1830 音色对比组 B：Yunxi 全长试配（55.97s·索引=data/sources/samples-review.md） |
| bs-001-voice-C-yunjian.mp4 | 测试件·非成品 | O-1830 音色对比组 C：Yunjian 全长试配（57.53s·同上） |
| bs-001-voice-D-huayan-local.mp4 | 测试件·非成品 | O-1830 纯本地备份组 D：piper huayan 全长试配（48.83s·ASR 对轴路·免 strict·错字在案 bs001/README §2） |
| bs-001-v3-emotive.mp4 | 测试件·非成品 | O-1918 工艺迭代垂直切片 v3：情感 TTS 九档 profile+拍稿卡点+合成 BGM sidechain ducking（1080×1920·51.26s·strict 全过·commit 28d0c3f·R21 补账） |
| bs-001-v4-bilibili-style.mp4 | 测试件·非成品 | O-1924 B 站风格 v4：作死挑战叙事全真实事故（文案三轮被拦/432 全灭/AI 自审）（1080×1920·71.26s·strict 全过+BGM ducking·commit 7609adf）——评审团首战样本（FAIL 8.0·docs/reviews/·R21 补账） |
| bs-001-v5-shipinhao.mp4 | 测试件·非成品 | v5 整改 R1-R4·视频号版：≤60s 规格 60.58s·尾拍 BGM 淡出·三家公司人格化（1080×1920·commit d1cf224·面板复评 FAIL 8.0·弱项收敛 E4 门槛·R21 补账） |
| bs-001-v5b-bilibili.mp4 | 测试件·非成品 | v5 整改 R1-R4·B 站版：64.0s·系列钩收尾（1080×1920·commit d1cf224·同批评审·R21 补账） |

> 中间件（独立临时音轨/SRT）存 `output/renders/.samples-tmp/`——O-1830 复现用（samples-review.md §四声明）·非渲染成品·不入本表。
> 工艺迭代批中间件（O-1918/O-1924/v5）存 `.v3-tmp/`/`.v4-tmp/`/`.v5-tmp/`/`.v5b-tmp/`（分句音频段+BGM+无 BGM 底版+beats 三栏稿）——同性质非成品·不入本表（R21 声明）。
