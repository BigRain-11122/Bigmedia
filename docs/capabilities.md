# BigStream 自动化能力注册表（Capabilities Registry）

> CEO 令 O-20260923-1536-bm-a：「底层技术等一系列的自动化开发能力」。
> 归口=工程技术部；入列规则如下，任何能力宣称必须有实证。

## §1 入列规则

- **live**：已入库且有实测证据（命令/日志/commit）。
- **in-dev**：backlog 已排、OS 循环在建。
- **planned**：已定方向未排期。
- **blocked**：被外部前置卡住（账号未开/CEO 待决/生产暂停令）——须注明卡点。
- 状态变更=改表+commit；宣称 live 而无证据=违规（诚实律）。

## §2 注册表

| ID | 能力 | 归属部门 | 状态 | 入口/证据 |
|---|---|---|---|---|
| C-01 | M4 机审门（draft_lint） | 合规审查部 | live | `python src/draft_lint.py` · 10 稿 0 FAIL 实测（首战拦 1 FAIL 1 脱敏） |
| C-02 | OS 自迭代循环（10 分钟/轮） | 工程技术部 | live | BigStream-OSLoop · 15:32 首轮 spawn 实证（run log） |
| C-03 | CEO 令牌台账（/CEO→O 文件） | 总裁办公室 | live | `orders/` 5 令实录 |
| C-04 | 三级记忆体系 | 工程技术部 | live | 媒体线 CODELY.md + 本仓 CODELY.md |
| C-05 | 发布/数据台账结构 | 平台运营部+数据分析部 | live | `output/schedule.md`+`output/analytics.md` |
| C-06 | draft_lint 测试件 | 工程技术部 | live | `tests/test_draft_lint.py` · 12 用例全绿（R1 commit e4c55dc） |
| C-07 | 11 平台变体骨架模板 | 平台运营部 | live | `docs/variant-templates.md` · 11 骨架块+登记块+检查单（backlog#2·R2 commit） |
| C-08 | 选题-台账一致性探针 | 选题研究部 | live | `python src/board_check.py` · 真板 5 题 10 稿 0 FAIL 实测（backlog#3·R3 commit） |
| C-09 | 自动周报生成器（state+commits→周报） | 数据分析部 | live | `python src/weekly_report.py` · backlog#6（R13）——四机器源（state.json+git log+backlog+orders）→`output/reports/weekly-<ISOyear>-W<ww>.md`·重跑覆盖制·模板件 `src/os/report_template.md`·12 测试用例全绿·首份 weekly-2026-W39.md 实测（10 轮/33 commits/令 10 条） |
| C-10 | 视频号口播裁剪（4 稿 67-77s） | 内容生产部 | blocked | 卡点=O-1756 不量产令（批量内容编辑须 CEO 令）·R14 转 [needs-CEO] 提案 backlog#7：裁剪应并入 #5 口吻改写批一次过（反重复） |
| C-11 | M2 素材链路（TTS/画面/剪辑/字幕） | 内容生产部 | in-dev | 选型已裁：本地算力优先（O-20260923-1609-bm-a·`docs/m2-local-stack.md` 四站本地方案+PoC 阶梯·backlog #9） |
| C-12 | 平台 API 发布对接 | 平台运营部 | blocked | 卡点=账号未开（批次①） |
| C-13 | 数据回流自动化（后台导出→对账） | 数据分析部 | planned | 待上线后实况定通道 |
| C-17 | 本地算力链 PoC（FFmpeg 时间线+TTS 参数表+字幕对轴） | 工程技术部+内容生产部 | live | backlog #9 · m2-local-stack.md §4——**全梯 done（R-A/R-B/R-C·R12）**：R-A 渲染器 `render_card_video.py`（1080×1920 实渲染+抽帧实证）；R-B TTS 双轨台账 `data/sources/tts-samples/`（edge-tts 6 样件+piper1-gpl 真装真录·T3 解锁·音色定档待人耳 #8）；R-C 双路字幕对轴：B 路 `srt_fix.py` 钳重叠=合成稿正路（strict 过）·A 路 `whisper_to_srt.py` small-int8-cpu=真人原声件（ASR 错字在案）·BS-001 v2 音轨重渲（59.93s·像素实证）·连带修红 drawtext CRLF 行距翻倍（LF+回归锁·tests 14+18 绿）·台账=`data/sources/bs001/README.md` |
| C-14 | 自动化生产全链路（七站表+生产闸门+生产模式协议） | 总裁办公室+工程技术部 | live | `docs/production-chain.md` · 闸门拒稿实测 exit=3 |
| C-15 | 草稿骨架生成器 make_draft（M1/M3 站） | 内容生产部+平台运营部 | live | `python src/make_draft.py` · 三类骨架 lint 0 FAIL 实测 |
| C-16 | 全链量产生产轮（M0-M3 无人值守量产） | 全部门 | blocked | 卡点=生产暂停令（state.json production=paused）·开闸=CEO 令 |
| C-18 | 调研能力（双线·协议化） | 选题研究部+工程技术部 | live | `docs/research-protocol.md` v1.0（O-20260923-1719-bm-a）·市场线=user-research v1.4（R19·P6 公众号官方运营规范 A 级破壳+120 位线索池）·技术线=local-stack-research v1.2（R18 补采：403 风控史四波+许可证更正 LGPLv3·A级源 A1-A10+本机 M1 实测） |
| C-19 | 发布准备度探针（readiness probe） | 平台运营部 | live | `python src/readiness.py` · backlog#10（R14）——四只读源聚合（accounts 亮灯=状态流自台账解析·GATE 态=GATE_RE 复用 draft_lint·renders 测试件「测试件·非成品」标注核验·backlog 决策标记）→距离首发阻塞清单·stdout/--out·24 测试用例全绿·真跑 3 阻塞 0 发现 exit 1（阻塞=批次①账号未开+10 稿 GATE PENDING+#7 [needs-CEO]） |
| C-20 | OS 循环健康探针（loop_health） | 工程技术部 | live | `python src/os/loop_health.py` · backlog#11（R17）——os-protocol §5 判据机器化：心跳新鲜度/间隔（SLA 20 分钟=WARN·锁龄 40 分钟=FAIL 停跳线）+tick↔done 轮次对账（账目滞后=FAIL·防 R4/R5 型断洞）+台账时间戳卫生（乱序/缺行=WARN·近似分钟 17:2x 合法）+backlog 燃尽率（info）——28 测试用例全绿·真跑 0 FAIL 4 WARN（皆为在案史实：R8/R9+R10/R11 叙事时间戳漂移、R4+R5 修复行、R5 26 分钟长轮间隙）；首战自检闭环=真跑揭心跳文件 UTF-8 BOM（PowerShell 5.1 Add-Content 所写）致首行失解析→utf-8-sig 修复+回归锁 |

## §3 能力建设循环

新能力＝工程技术部（或归口部门）在 backlog 立项 → OS 循环按轮开发 → 实测证据落 logs/commit → 本表升 live。禁止跳过证据直接宣称。

## 变更记录

- 2026-09-23: v1.0 建册（CEO 令 O-20260923-1536-bm-a）——live×5 / in-dev×4 / blocked×3 / planned×1。
- 2026-09-23: v1.1 全链批（CEO 令 O-20260923-1600-bm-a）——C-06 升 live（R1）；OS 循环 R2/R3 自主升 C-07/C-08 live；新增 C-14/C-15 live、C-16 闸门 blocked。现 live×8 / in-dev×1 / blocked×4。
- 2026-09-23: v1.2 本地算力批（CEO 令 O-20260923-1609-bm-a）——C-11 解除 CEO 待决卡点转 in-dev（本地算力优先·选型=v1 四站本地）；新增 C-17 本地链 PoC in-dev（backlog #9）。现 live×8 / in-dev×3 / blocked×3 / planned×1。
- 2026-09-23: v1.3 调研远征批（CEO 令 O-20260923-1719-bm-a）——新增 C-18 调研能力（双线协议化）live：research-protocol v1.0 立制+技术线首采 local-stack-research v1.0（含撤回 m2 一条无源断言）。现 live×11 / in-dev×3 / blocked×3 / planned×1。
- 2026-09-23: v1.4 R-B 批（OS 循环 R11）——C-17 之 R-B 转 live（TTS 双轨试录：edge-tts 参数表+6 样件·piper1-gpl 本地备份真装真录）；C-17 整体仍 in-dev 至 R-C；卡点 T3 解锁/T2 起录/T4 呈样（local-stack-research §6）。
- 2026-09-23: v1.5 R-C 批（OS 循环 R12）——C-17 整体转 live：双路字幕对轴（B 路 edge-tts 直出+srt_fix 钳重叠=A 路更快-whisper small int8 CPU）+BS-001 v2 音轨重渲；连带修红 drawtext CRLF 行距翻倍（LF 写出+回归测试锁）；PoC 全梯 done·R-D 后置。现 live×12 / in-dev×2 / blocked×3 / planned×1。
- 2026-09-23: v1.6 周报批（OS 循环 R13）——C-09 转 live：自动周报生成器（src/weekly_report.py·四机器源→output/reports/·重跑覆盖制）；output/reports/ 解封入 git（台账=产出即证据）；首份周报 weekly-2026-W39.md 生成实测。现 live×13 / in-dev×1 / blocked×3 / planned×1。
- 2026-09-23: v1.7 就绪度批（OS 循环 R14）——新增 C-19 发布准备度探针 live（backlog#10·四只读源聚合→阻塞清单·24 用例·真跑 3 阻塞 0 发现）；C-10 卡点刷新（O-1756 边界外·R14 转 [needs-CEO] 提案并入口吻改写批）；output/renders/README.md 测试件台账解封入 git（mp4 二进制仍 ignored·R9/R12 两件补「测试件·非成品」标注）。现 live×14 / in-dev×1 / blocked×3 / planned×1。
- 2026-09-23: v1.8 循环健康批（OS 循环 R17）——新增 C-20 OS 循环健康探针 live（os-protocol §5 判据机器化·28 用例·全回归 119 绿·真跑 0 FAIL 4 WARN 皆为在案史实的顾问级记录·首战揭 BOM 解析坑即修+回归锁）。现 live×15 / in-dev×1 / blocked×3 / planned×1。
- 2026-09-23: v1.9 调研续采批（OS 循环 R18）——C-18 技术线引用升 v1.2：edge-tts 403/风控官方 issues 史补采（T2 卡点·12 件四波全关·#286 仅大陆复现·修复-发版对应）+许可证更正（GPL-3.0→LGPLv3·LICENSE 直采）+T2 数据点续录 6/6；m2-local-stack v1.2 同步（备份线升产线刚性依赖）。live×15 不变。
- 2026-09-23: v1.10 调研破壳批（OS 循环 R19）——C-18 市场线引用升 v1.4：P6 公众号官方《运营规范》A 级直链破壳（「可选推荐」分发功能官方确认+阶梯处罚+内容红线·首发批次①机制面齐）；P4 小红书官方协议域定位（h5 JS 壳）。live×15 不变。
