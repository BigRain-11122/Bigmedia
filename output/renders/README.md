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
| bs-001-v6-shipinhao.mp4 | 测试件·非成品 | v6 术语平权版（CEO 裁 E4 维持路人标准后）：术语译路人语（软著→版权证书/策略→方案/代码库→留底）（1080×1920·55.13s·commit 2c8ddb9·面板三轮 FAIL·E4 锚 7 缺口号·R22 补账） |
| bs-001-v6b-bilibili.mp4 | 测试件·非成品 | v6 术语平权·B 站版（1080×1920·56.14s·commit 2c8ddb9·同轮评审·R22 补账） |
| bs-001-v7-shipinhao.mp4 | 测试件·非成品 | v7 口号回环版：「一个人上班，三家公司开工」首尾（1080×1920·52.82s·commit 2c8ddb9·面板四轮 FAIL 8.0 E4 唯一短板席→E4 双态裁后翻**放行候选**（173e286·开发期五席 9+·E4 参考读数 8.0 高于真爆款基线·docs/reviews/）·R22 补账） |
| bs-001-v7-vis.mp4 | 测试件·非成品 | O-1937 视觉批 v7 重渲：H1/H2 双字重排版引擎（msyhbd 锚+accent 强调+gray60 弱化+150ms 淡入出·visual-spec v1.0）（1080×1920·52.82s·commit 2c2d990·抽帧 E7 自检三重对比过·R22 补账） |
| bs-001-v8-cyber-light.mp4 | 测试件·非成品 | O-2136 赛博声线组 light：v8 系统日志体拍稿+轻机械纹理链（1080×1920·51.61s·strict 过·ASR 可懂度=基线同音字级·索引=samples-review §五） |
| bs-001-v8-cyber-mid.mp4 | 测试件·非成品 | O-2136 赛博声线组 **mid（评审推荐档）**：音高压平-8Hz+金属颤音链·事实词零损实证（1080×1920·53.17s·strict 过·评审=v8 台账方向首测 FAIL 8.5·待 CEO 拣音） |
| bs-001-v8-cyber-full.mp4 | 测试件·非成品 | O-2136 赛博声线组 full（极端参考端）：深度合成链（降调+52Hz 颤+位深压碎+窄频带）·ASR 实测打糊事实词（1080×1920·54.90s·strict 过） |
| bs-001-v9-cyber-light.mp4 | 测试件·非成品 | O-2136 定档版（CEO 点选 light+机器叙述者）：双整改（爽/累反转+甩锅交账梗回归）·12 拍（1080×1920·59.31s·strict 过·ASR 事实词全存活）——评审六席 9+ **PASS=放行候选**待 CEO 终审（docs/reviews/review-20260923-bs001-v9.md） |
| bs-001-v10-humanfeel.mp4 | 测试件·非成品 | O-2210 人味机制实证件：v9 同稿唯一变量=四站人味机制（微抖动/呼吸间隙/呼吸声/房间底噪/颗粒暗角深灰底·seed42·grain7）——机检门 A/B：v9 gap-zero FAIL→v10 全 PASS；**64.06s 超 60s=空气预算律立法诱因（机制演示件·量产按 L15 裁文本预算）**（1080×1920·strict 过·ASR 事实词全存活） |
| bs-001-live-A-pixelboard.mp4 | 测试件·非成品 | O-1115 实录素材试跑 A 版：**Biggame 总控真实录屏底版**（像素小镇看板 45s 实录·gdigrab 区域采集·blur-pad 竖版）+H1/H2 字卡+字幕+AIGC+grain7——复用 v10 全套音频/时间线（产线默认）·strict 过·抽帧验图过（卡可读/AIGC 在位）；spec 门=时长 64.06s 超窗同 v10 在案（机制演示件） |
| bs-001-live-B-puredoc.mp4 | 测试件·非成品 | O-1115 实录素材试跑 B 版：**纯实录纪录片式**（同底版无字卡·字幕+AIGC+grain4）——strict 过；同 A 版时长超窗在案；A/B 双版=「实拍+字卡」vs「纯实录」两种剪辑路线呈 CEO 拣式 |

> 中间件（独立临时音轨/SRT）存 `output/renders/.samples-tmp/`——O-1830 复现用（samples-review.md §四声明）·非渲染成品·不入本表。
> 工艺迭代批中间件（O-1918/O-1924/v5）存 `.v3-tmp/`/`.v4-tmp/`/`.v5-tmp/`/`.v5b-tmp/`（分句音频段+BGM+无 BGM 底版+beats 三栏稿）——同性质非成品·不入本表（R21 声明）。
> v6/v6b/v7 批中间件（E4 路人标准裁后术语平权→口号回环）存 `.v6-tmp/`/`.v6b-tmp/`/`.v7-tmp/`（分句音频段+BGM+cards 字卡+subs——同性质非成品·不入本表·R22 声明）；视觉批中间件（O-1937）存 `.v7vis-tmp/`（分句段+BGM+cards-vis 字卡重制+抽帧探针图）——同上。
> 赛博批中间件（O-2136）存 `.v8-light/`/`.v8-mid/`/`.v8-full/`/`.v9-light/`（分句段+赛博链前后音轨+BGM duck 混音+cards-vis 模板合并件+subs+ASR 可懂度检查 srt+抽帧图）——同性质非成品·不入本表。
> 人味批中间件（O-2210）存 `.v10-light/`（分句段+呼吸声件+间隙件+房间底噪前后音轨+BGM duck 混音+cards+subs+ASR 检查 srt+抽帧图）——同上。
> 实录批素材与中间件（O-1115）存 `data/sources/footage/`（raw 录屏+竖版预处理+探针帧·**素材层=源资产归档位**·retention R2）+ `output/renders/.live-tmp-frame-*.png`（验图帧）——素材入数据账·帧为中间件。
