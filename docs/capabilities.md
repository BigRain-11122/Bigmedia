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
| C-17 | 本地算力链 PoC（FFmpeg 时间线+TTS 参数表+字幕对轴） | 工程技术部+内容生产部 | live | backlog #9 · m2-local-stack.md §4——**全梯 done（R-A/R-B/R-C·R12）**：R-A 渲染器 `render_card_video.py`（1080×1920 实渲染+抽帧实证）；R-B TTS 双轨台账 `data/sources/tts-samples/`（edge-tts 6 样件+piper1-gpl 真装真录·T3 解锁·音色定档待人耳 #8）；R-C 双路字幕对轴：B 路 `srt_fix.py` 钳重叠=合成稿正路（strict 过）·A 路 `whisper_to_srt.py` small-int8-cpu=真人原声件（ASR 错字在案·**C2 校准 R169**：S2 QC recipe=`--model medium --beam-size 5 --no-context`=CER 13.07%→5.53%·三旋钮落工具·small 默认快道）·BS-001 v2 音轨重渲（59.93s·像素实证）·连带修红 drawtext CRLF 行距翻倍（LF+回归锁·tests 14+18 绿）·台账=`data/sources/bs001/README.md`·**深纵律装配 R195**：`emotive_tts --deepdive`（#14 B站线·段界 ①-⑳+段间 ≥2s+滚动 60s ≤55s 求解器·BS-001-DD 首战全绿） |
| C-14 | 自动化生产全链路（七站表+生产闸门+生产模式协议） | 总裁办公室+工程技术部 | live | `docs/production-chain.md` · 闸门拒稿实测 exit=3 |
| C-15 | 草稿骨架生成器 make_draft（M1/M3 站） | 内容生产部+平台运营部 | live | `python src/make_draft.py` · 三类骨架 lint 0 FAIL 实测 |
| C-16 | 全链量产生产轮（M0-M3 无人值守量产） | 全部门 | blocked | 卡点=生产暂停令（state.json production=paused）·开闸=CEO 令 |
| C-18 | 调研能力（双线·协议化） | 选题研究部+工程技术部 | live | `docs/research-protocol.md` v1.0（O-20260923-1719-bm-a）·市场线=user-research v1.6（R22·P4 h5 定谳=运行时 fetch·静态层不可采；R20·P6《推荐运营规范》子文档全文 A 级闭环：推荐场景/质量几率/原创资格/误导标题/低创作度/低价值 AIGC/虚假人设/导流禁域+120 位线索池）·技术线=local-stack-research v1.2（R18 补采：403 风控史四波+许可证更正 LGPLv3·A级源 A1-A10+本机 M1 实测） |
| C-19 | 发布准备度探针（readiness probe） | 平台运营部 | live | `python src/readiness.py` · backlog#10（R14）——四只读源聚合（accounts 亮灯=状态流自台账解析·GATE 态=GATE_RE 复用 draft_lint·renders 测试件「测试件·非成品」标注核验·backlog 决策标记）→距离首发阻塞清单·stdout/--out·24 测试用例全绿·真跑 3 阻塞 0 发现 exit 1（阻塞=批次①账号未开+10 稿 GATE PENDING+#7 [needs-CEO]） |
| C-20 | OS 循环健康探针（loop_health） | 工程技术部 | live | `python src/os/loop_health.py` · backlog#11（R17）——os-protocol §5 判据机器化：心跳新鲜度/间隔（SLA 20 分钟=WARN·锁龄 40 分钟=FAIL 停跳线）+tick↔done 轮次对账（账目滞后=FAIL·防 R4/R5 型断洞）+台账时间戳卫生（乱序/缺行=WARN·近似分钟 17:2x 合法）+backlog 燃尽率（info）——28 测试用例全绿·真跑 0 FAIL 4 WARN（皆为在案史实：R8/R9+R10/R11 叙事时间戳漂移、R4+R5 修复行、R5 26 分钟长轮间隙）；首战自检闭环=真跑揭心跳文件 UTF-8 BOM（PowerShell 5.1 Add-Content 所写）致首行失解析→utf-8-sig 修复+回归锁；**R241 增 state-ts 机读心跳面门**（PT-20260925-02 巡检整改：STATE_REQUIRED 增 ts/task·缺失/畸形=FAIL·滞后 >40min/未来戳=WARN·33 用例绿——fleet-audit 判活直读 state.json ts/task·os-protocol v1.10） |
| C-21 | 去 AI 感人味链（human-feel dial+gate） | 工程技术部 | live | `emotive_tts --human <seed>`（逐段微抖动/变长呼吸间隙/呼吸声/房间底噪·种子可复现）+`render_card_video --grain/--bg`（胶片颗粒+暗角+深灰底）+`python src/ai_feel_check.py`（四指纹机检门=M4 层 1.6·gap-zero/gap-uniform/pacing-metronome/prosody-flat·首战 A/B：v9 gap-zero FAIL→v10 全 PASS）——O-20260923-2210-bm-a·规格=human-feel-spec.md·13 新测试（总 140 绿） |
| C-22 | 平台规格门（platform_spec_check） | 工程技术部 | live | `python src/platform_spec_check.py --video FILE --platform NAME`（M4 层 1.7·时长实测红线工具化）——ffprobe 时长/画幅 vs `docs/platform-playbook.md` 规格表**实解析**（单一真相零漂移·多画幅平台/无时长窗平台=INFO）；10 单测绿·首战舰队体检 14 件：视频号线 9 PASS+2 时长超窗在案（v5 60.58s/v10 64.06s）+**B站三件全低于 3-15min 窗=B站纵深格式重制定位修正（backlog #14）**；v9 仅 0.7s 余量=空气预算律（L15）必要性再证 |
| C-23 | 情报日报采集器（daily_brief） | 选题研究部（P-62 ②·原情报部并入） | live | `python src/intel/daily_brief.py`（O-20260923-2304-bm-a·零 key 零 token）——B站热门 API+知乎热榜 API 双源实采（2026-09-23 带浏览器 UA 实测双通·B站此前 412 风控在案·带 UA 后通）；日报=`data/intel/daily/YYYY-MM-DD.md`（重跑=当日最新真相）·四路赋能（S0 选题弹药/copy-craft 校准/评审 rubric/S4 风险雷达）·负结果如实入报（零断言）；6 解析单测绿·首份日报 20 条实采在案；循环接线=当日缺任意轮补产（任务书铁律区）——**无人值守实证：2026-09-24 日报由 OS 循环夜间自动产出** |
| C-24 | 专职专家调用器（call_expert） | 全部门（工程技术部供工具） | live | `python src/call_expert.py --expert <id> --material <文件>`（O-20260924-1033-bm-a）——七部门 11 席名册（`docs/expert-roster.md` v1.2·P-62 ② 后八部门并七部门+粉丝数据部三席设计态块（P-76·人名 CEO 保留面·不进调用表）·registry+提示词外置数据件）·本地 Ollama 零 token·**UTF-8 子进程管道=PS5.1 GBK 管道乱码坑根治**（09-23 原生管道实证）·调用自动落 `docs/reviews/expert-calls.md` 台账（行级追加）；6 单测绿·首调实证=hot-intel×2026-09-24 日报（赛道 top3+红线预警+一句话结论·expert-calls 在案） |
| C-25 | 周自审数据包（self_audit） | 总裁办公室（循环归口执行） | live | `python src/os/self_audit.py`（O-20260924-1057 周期自审令·os-protocol §7）——零 token 自动采集：三探针+state/backlog/orders/环节台账/renders 盘账/全量测试/git 7 日→`docs/audits/packs/<ISO周>-pack.md`；判读层=循环轮按五清单填 `docs/audits/<ISO周>-self-audit.md`（当周缺=任意轮补产·与日情报报同款触发律）；4 单测绿·首期 W39 数据包+报告在案（首跑路径 bug=REPO parents 少一级→src\docs 误落·同 daily_brief 型坑当场修——**src/ 下建仓根引用件必须 parents[2] 起步**·两案实证入工程教训） |
| C-26 | 屏录采集站（record_screen+bgvideo） | 内容生产部（工程技术部供仪器） | live | `python src/render/record_screen.py --open-app <URL> --title <窗口题> --seconds N --out FILE [--close]`（O-20260924-1115 实录素材令）——ctypes 精确找窗取形+FFmpeg gdigrab 区域采集（零安装）+开窗/关窗辅助（CEO 令授权临时窗·录毕即关·静默律外例）；偶数尺寸修复在案（x264 拒奇数·首跑 1366x1079 崩）；**渲染器 `--bgvideo` 实拍底版**（滤镜链头 scale 插链修复在案）+`--no-cards` 纯实录版；首录实证=Biggame 总控 45s（像素看板·验图过）·live-A/live-B 双版本试跑呈 CEO |
| C-27 | 封面快路（--poster 封面帧导出） | 平台运营部（工程技术部供仪器） | live | `render_card_video.py --poster <out.png>`（O-20260924-1043 审计 R1·backlog#16·R116）——M5 发布物「封面」零新依赖代用产线：封面帧=首卡满可见位 t=start+0.15s（字面首帧=淡入 150ms 空帧·超短卡回退中点·--no-cards t=0）；4 单测（render 27 例）+全回归 176 绿；v10 时间线集成实证=`output/renders/bs-001-poster-v10-cover.png`（1080×1920·验图过·S2 双门在案：ai_feel all-PASS+spec 视频号画幅 PASS/时长超窗同 v10 线读数）；C-16 ComfyUI 图像生成线留远期 |
| C-28 | 剪辑工艺站+门（edit_craft+edit_craft_check） | 平台运营部（工程技术部供仪器） | live | `python src/render/edit_craft.py --profile <shipinhao/bilibili/douyin> --cards --srt --bgvideo --audio [--grain N]`（CEO 剪辑反馈令 2026-09-24「剪辑 卡点 转场 特效什么都没有，而且每个平台用户喜好都不一样」）——R-E 剪辑站三段式：分段子渲染（zoompan Ken Burns 推拉/punch 台阶强调+命中拍白闪）→拼接段（**绝对时间轴保持代数**：d_k=span_k+incoming fade·转场在拍点完成·**硬切=concat 真直拼 cut fade_s=0**——A3 2026-09-24 引擎升级：0.05s 二帧淡入近似退役·边界帧量化+per-run trim 帧精确落点）→R-A 文字层合成（**长 deck 传输门控 R199**：fc_args ≥28K 字符走 `-/filter_complex` 文件传输=CreateProcess 32K 上限根修）；**平台口味三 profile**（转场:硬切比/命中拍上限/白闪·editing-craft-spec §4）；`python src/edit_craft_check.py --plan <mp4>.plan.json --srt <subs> --profile <名>`（M4 层 1.8·**独立常量门=执行侧不得自证**·cut-blended 回归断言：0.05 复辟=FAIL）；27 单测绿；首战=BS-001 同稿双平台样件（11/11 边界落 cue 锚·时间线保持过）·A3 重渲实证=bs-001-v13 双件（MAD 切点单帧全距跳验图） |
| C-29 | 素材对位工作流（分镜对位表+多源选镜+脱敏探针） | 内容生产部+平台运营部（工程技术部供仪器） | live | **CEO 工作流令 2026-09-24「录制的内容也和说辞文案完全不匹配，反思工作流，建立正确严谨专业的工作流」**——①分镜对位契约：cards.json 每拍 `visual`（source+req 或 cards-only+reason·缺声明=引擎拒+门 FAIL·footage-matching-spec §1）；②`edit_craft.py` 多源选镜（每拍绑定素材·短素材循环·cards-only=深灰 flat）；③`edit_craft_check.py` 对位面（visual-undeclared/missing-file/no-reason/ratio≥0.80·层 1.8）；④采集站硬化：`focus_window` 置顶+`prep_vertical.py` 竖版规格化（+`--batch` 目录批处理幂等模式 2026-09-25）+`show_loop_log.ps1` 日志展示窗；**两实证入规格**：BigMoney 总控渲染现持仓面=脱敏作废换合规素材（源码扫描≠渲染探针）/两镜录穿第三方窗口=隐私作废（活动桌面律）；8 新单测（23 绿）；首战=bs-001-v11-match（12 拍抽帧对位核验零不匹配·对位率 83%·正典示范件=`data/sources/bs001/cards-v10-matched.json`） |
| C-30 | 故事线爆款工艺（storyline-craft T1-T9/C1-C3/A1-A2） | 内容生产部（总裁办公室立制·循环收账入册） | live | **CEO 反馈令 O-20260925-1720「要大众喜闻乐见的，要有爆款潜质的」**——视频线工艺资产（H1-H8/P1-P8/趣律）向文字/图像/音频三介质移植：文字线 T1-T9（黄金百字/赌局骨架/冲突密度/爽点节拍/金句配额/当事人感/卧槽位/章尾冲突钩/真实瑕疵=爽点）+漫画 C1-C3（尾格 PUNCH/字幕带=梗位/反差前置）+有声 A1-A2（前 30 秒定留存/单集完整钩+悬念尾）+随件自检表（产稿即检·缺表=草案未完成）；**T1/T2/T3/T8=M4 硬门**（✗=不过）·T4-T7=抽审·红线五条+三重标注照旧前置；首证双落=ch.1 v2 文字版（SC-001-01-v2·bm-a 闭环·v2=产线默认）+ch.1 v2 有声版（SC-001-01-v2.mp3·R271 循环音频腿：A1 钩位 17.8s 实证+pacing CV 0.666/copy CV 0.719 双高于 v1 散文版 0.396/0.425=爆款节拍机检读数）；charter v1.3 §5 门禁接线（三线+L-卡 四列全接）。 |

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
- 2026-09-23: v1.11 调研闭环批（OS 循环 R20）——C-18 市场线引用升 v1.5：P6 余项闭环——《微信公众号和服务号推荐运营规范》子文档 URL 从 opshowpage 原始 HTML 直采取得并全文 A 级实采（推荐场景三处/质量=推荐几率/转载分组不推荐/关闭不可逆/误导类标题/低创作度含低价值 AIGC/虚假人设/导流禁域）。live×15 不变。
- 2026-09-23: v1.12 调研定谳批（OS 循环 R22）——C-18 市场线引用升 v1.6：P4 小红书 h5 terms 通道四探针深挖定谳=纯 React SPA 壳（服务端零正文）+三 bundle 解包（main=内部 OA 端点·vendor grep 零命中）→运行时 fetch·静态层不可采（负结果如实入账·research §6 P4 通道收窄）。live×15 不变。
- 2026-09-23: v1.15 情报部批（CEO 令 O-20260923-2304-bm-a）——C-23 `daily_brief.py` 入册 live（零 key 双源热榜采集·首份日报 20 条实采）+**情报部编制成立**（org-structure v2.0 七部一办→八部一办）+顶层设计统摄件（BLUEPRINT v1.0）。live×18。
- 2026-09-24: v1.16 专职专家批（CEO 令 O-20260924-1033-bm-a）——C-24 `call_expert.py` 入册 live（八部门 11 席名册+一键调用+调用台账+UTF-8 管道修复·首调 hot-intel 实证）+名册正典 `docs/expert-roster.md` v1.0；循环任务书接线（按需调用纪律）。live×19。
- 2026-09-24: v1.17 周期自审批（CEO 令 O-20260924-1057-bm-a）——C-25 `self_audit.py` 入册 live（周自审数据包零 token+判读五清单·os-protocol §7 立法）+首期 W39 数据包与报告在案+BLUEPRINT §7 节律行+任务书接线（当周缺任意轮补产）。live×20。
- 2026-09-24: v1.18 结论存档修（自治续·C-24 补强）——专家调用**结论全文落盘** `docs/reviews/expert-verdicts/<时间>-<id>.md`+台账行显链（首调 hot-intel 结论曾因控制台 GBK 乱码全文丢失=可审计性缺口实证）；hot-intel 重调补档成功；+2 单测（总 168）。
- 2026-09-24: v1.19 实录素材批（CEO 令 O-20260924-1115-bm-a）——C-26 屏录采集站入册 live（record_screen 录制站+渲染器 `--bgvideo`/`--no-cards`）+Biggame 总控 45s 首录+live-A/live-B 双版本试跑（素材层=去 AI 感最强一环落地）。live×21。
- 2026-09-24: v1.19 实录素材批（CEO 令 O-20260924-1115-bm-a）——C-26 屏录采集站入册 live（record_screen 录制站+渲染器 `--bgvideo`/`--no-cards`）+Biggame 总控 45s 首录+live-A/live-B 双版本试跑（素材层=去 AI 感最强一环落地）。live×21。
- 2026-09-23: v1.13 人味机制批（O-20260923-2210-bm-a）——C-21 去 AI 感人味链入册 live：`--human` 种子化配音微抖动+呼吸间隙+呼吸声+房间底噪、`--grain/--bg` 画面质感层、`ai_feel_check.py` 四指纹机检门（M4 层 1.6·首战 v9 FAIL→v10 PASS）；规格=human-feel-spec.md。live×16。
- 2026-09-23: v1.14 平台规格门批（O-2210 自治续）——C-22 `platform_spec_check.py` 入册 live（M4 层 1.7·时长实测红线工具化·playbook 实解析单一真相）；首战舰队体检=B站三件低于 3-15min 窗→B站纵深格式重制定位修正（backlog #14）。live×17。
- 2026-09-24: v1.20 封面快路批（O-1043 审计 R1·backlog#16·OS 循环 R116）——C-27 `--poster` 封面帧导出入册 live（M5「封面」零新依赖代用产线·首卡满可见机律+4 单测+v10 集成实证+S2 双门在案）。live×22。
- 2026-09-24: v1.21 剪辑工艺批（CEO 剪辑反馈令「剪辑 卡点 转场 特效什么都没有，而且每个平台用户喜好都不一样」）——C-28 R-E 剪辑站+层 1.8 机检门入册 live（平台口味三 profile+xfade 时间轴保持代数+E8 评审席接线·zoomin 转场本 build 未实现实证在案即修）；live-A 假绿灯更账（评审通过未知项教训）。live×23。
- 2026-09-24: v1.22 素材对位工作流批（CEO 令「录制的内容也和说辞文案完全不匹配，反思工作流，建立正确严谨专业的工作流」）——C-29 入册 live（分镜对位表契约+多源选镜+对位机检面+采集站硬化 focus_window/prep_vertical）；脱敏渲染探针律+活动桌面律两实证入规格（bigmoney 总控持仓面/fleetmon+bigmoney-town 隐私作废）；首战=bs-001-v11-match 对位核验零不匹配。live×24。
- 2026-09-24: v1.23 组织精简批（集团 ledger P-20260924-62）——C-23 归口随情报部并入选题研究部（八部一办→七部一办·机制与命令零变更）；评审四重面合一（评审法条单一真相=dept-review-mechanism §6·review-panel 退役为指针·C 册引用面同步）。
- 2026-09-24: v1.24 A3 真直切引擎升级批（自进清单 A3·OS 循环 R168）——C-28 行同步：硬切 0.05s 二帧淡入近似退役→concat 真直拼（cut fade_s=0·run 分组=fade 链内接+cut 处 concat·边界帧量化+per-run tpad/trim 帧精确落点+段渲染+1 安全帧防混合饥饿）+层 1.8 新代数 d_k=span_k+incoming fade+cut-blended 回归断言（0.05 复辟=FAIL·独立常量律）；4 新单测（27 edit 门测绿·203 全回归绿）；实证=bs-001-v13 双件重渲（层 1.8 双 PASS+MAD 切点单帧全距跳 79-136 验图·fade 对照组成立·B站时长窗 FAIL=#14 口径不变）。live×24 不变（存量升级非新席）。
- 2026-09-24: v1.25 C2 ASR 仪器校准批（自进清单 C2·OS 循环 R169）——C-17 行同步：A 路 `whisper_to_srt.py` 参数面校准（基准=v12 母版音轨·v11-trim beats 对拍·字符级 CER）——**模型档位=主因子**（small int8 基线 13.07%→medium int8+beam5+noctx 5.53%·同音位点 12→8·事实词零损）；参数面噪声级（beam5 零增益·noctx +1 字+提速 30%·域 initial_prompt 反劣化=负结果入档）；工具落三旋钮 --beam-size/--no-context/--initial-prompt（默认不动=无实测增益不改行为）+S2 asr-check QC recipe=`--model medium --beam-size 5 --no-context`（small 默认=快道）；4 新单测（fake 模型注入·207 全回归绿）。live×24 不变（存量校准非新席）。
- 2026-09-25: v1.26 深纵律装配批（OS 循环 R195·#14 B站线）——C-17 行同步：`emotive_tts.py --deepdive` 模式=段界检测（card 行首 ①-⑳ 标记·未标记段内拍承前零伪界）+段间呼吸 ≥2.0s+滚动 60s 口播 ≤54.5s 定律求解器（interior_scale 自升至定律过·不可满足=exit 1 有牙·--deepdive 须配 --human）；9 新单测+**228 全回归绿**；首战=BS-001-DD 69 拍（初测 FAIL 段间 0.13-0.66s+56-57s/60s→deepdive 全绿 472.58s=7:52 ∈ 窗·滚动最大 54.29s≤55·五界 2.04-2.59s≥2·非 deepdive 路径零动=fleet 线零回归）。live×24 不变（存量升级非新席）。
- 2026-09-25: v1.27 compose 传输门控批（OS 循环 R199·#14 B站线·渲染双 FAIL 根因修）——C-28/C-17 行同步：`render_card_video.py` 新 `fc_args()` 门控传输（<28,000 字符内联 `-filter_complex` 原路径·≥阈值落 `fc.txt` 走 **`-/filter_complex <file>`** 通用读值语法——本机 ffmpeg 9.0.1 已删 `-filter_complex_script`·R9 在案复证·读值语法 smoke rc=0 实证）+`edit_craft.py` compose 与 `render_card_video.py` 主渲染**双调用点接线**；根因=BS-001-DD 69 拍 deck=208 drawtext 条 74,825 字符·总命令行 75,119 **>32,767 CreateProcess 上限**→spawn 拒绝浮现为误导性 FileNotFoundError（两跑 ~105s 同点死=段渲染+xfade 过·compose 死·60s 件 12 拍 ~13K 未触线=隐含 ~35 拍内联上限）；fleet 短件门控下走原路径零行为变更；4 新单测（inline/boundary/roundtrip/DD 规模锁·**232 全回归绿**）；fleet grain 口径实证=grain 0（F-003/F-004 平坦区 std=0.00）。live×24 不变（存量修复非新席）。
- 2026-09-25: v1.28 A5 prep 批处理批（自进清单 A5·OS 循环 R205·空转规则默认工作面）——C-29 行同步：`prep_vertical.py` 新 `--batch <dir>` 目录批处理（目录内每视频文件同链一跑·输出=`<stem><suffix>.mp4` 就位源旁；幂等=已有输出 skip+`--force` 重做+**已带后缀件永不作输入**=防回环自吞；汇总退出码=0 全成/2 坏参无件/3 任一 FAIL·`--suffix` 默认 -vertical·配 `--w 1920 --h 1080` 可作 16:9 批）+`build_chain` 单源化（模块级 CHAIN 死件退役）；**单文件模式行为零变更**（dry-run/ffprobe/--out 全旧律）；12 新单测（fake ffmpeg 注入零真渲染·**244 全回归绿**）。缺口锚=对位批手工 ×6 次效率缺口（BS-002~005 采集站逐源手跑实测）·BS-005/bs005e 素材窗一开即新源批直达。live×24 不变（存量升级非新席）。
- 2026-09-25: v1.29 storyline-craft 爆款工艺入册（O-20260925-1720 CEO 反馈令·bm-a 交互会话立制+循环 R271 收账步升表）——C-30 新席：T1-T9/C1-C3/A1-A2+随件自检表（T1/T2/T3/T8=M4 硬门）·正典=docs/storyline-craft.md v1.0（证据底座=research/storyline-virality-research-v1.md·现产五篇诚实终诊全违 H1=散文化病根在案）；首证双落=ch.1 v2 文字版（bm-a·v2=产线默认）+ch.1 v2 有声版（R271·A1/A2 适配机检实证）。live×25。
