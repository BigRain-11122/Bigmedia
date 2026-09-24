# -*- coding: utf-8 -*-
"""R192 ledger consolidation: S2 three-gate results (incl layer-1.8 FAIL honest
record), renders row, station-reviews row, bs005 README S2 state, backlog #4
amendment, state.json log rewrite. UTF-8 file writes only (encoding law)."""
import io
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def sub(path, old, new, count=1):
    t = io.open(path, encoding="utf-8").read()
    assert old in t, "MISS in %s: %s..." % (path, old[:60])
    io.open(path, "w", encoding="utf-8").write(t.replace(old, new, count))


def sub_line(path, prefix, new_lines):
    lines = io.open(path, encoding="utf-8").read().splitlines()
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(hits) == 1, "prefix hits %d in %s" % (len(hits), path)
    lines[hits[0]:hits[0] + 1] = new_lines
    io.open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")


# 1) renders README: mp4 row + tmp declaration line expansion
RD = REPO / "output" / "renders" / "README.md"
new_decl = ["> BS-005 批中间件（D-BS-06 量产·微信视频号 第五件·起链 2026-09-25）：批中间件 `.bs005-tmp/`（S1 门 1500s 脱壳包装件 s1_call.py[.bs004-tmp 同型·**S1 v1.5 违律扣分制首件真门**]+s1-result.json[判分式落档·轮间异步落地·R176→R177 先例]+**R192 生产链**：voiceover-v2/v3.beats 空气预算裁稿[66.16→61.03→58.39s·正位留档]+TTS light 定稿音轨[audio.mp3/subs.srt 12 cues/cards.json 基线·--template=bs004 v14 批口径]+probe-src/[biggame-cockpit 10 帧多时点探针 tile×2·R186 段中尾帧教训执行]+build_matched.py[对位表构建件·cards-only 注理由逐拍]+r192_s2_driver.py/s2-results.md[S2 三门执法件·层 1.8 FAIL 如实在档]+r192_state.py/r192_export.py/r192_ledgers.py[收账步脚本·PS5.1 中文转义坑规避]）——成品后中间件同盘史深盘；正位数据件=`data/sources/bs005/`（**入 git**）+`bs-005-v1-shipinhao-60s.mp4.plan.json`（**入 git**）",
            "| bs-005-v1-shipinhao-60s.mp4 | **在链·批次①（D-BS-06 第五件·R192 渲染·F-005 登记前在链态）** | **R-E shipinhao 12 段 11 柔转场 0 硬切**（9:16 1080×1920·58.41s 实测·1.6s 余量·cards-v1-matched 对位 2/12·hits=[]）·S2 三门=ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·pacing CV 0.219·prosody 9 档·copy CV 0.231）+spec 微信视频号双 PASS+**层 1.8 FAIL（visual-ratio 0.17<0.80：cards-only 10 拍——结构诊断=游戏公司主题×源池单源 45s·数字错位避用律禁硬贴·E8/M4/F-005 待素材源扩充后闭环）**·plan.json 入 git |"]
sub_line(RD, "> BS-005 ", new_decl)

# 2) station-reviews: S2 enforcement row (honest FAIL record)
SR = REPO / "docs" / "reviews" / "station-reviews.md"
row = ("\n| 2026-09-25 | **S2 三门循环独立执法·BS-005 v1 首战（层 1.8 visual-ratio FAIL 如实入账）** | "
       "bs-005-v1-shipinhao-60s | 循环独立执法（ai_feel+层 1.8+spec·纯脚本机检零 LLM） | "
       "**2 PASS+1 FAIL** | R192 渲染首战：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·pacing CV 0.219·"
       "prosody 9 档 12 拍·copy CV 0.231）+spec 微信视频号双 PASS（9:16+58.41s 入 30-60s 窗 1.6s 余量·"
       "fleet 同族第 5 件）+**层 1.8 六面=5 PASS+1 FAIL（visual-ratio 0.17<0.80）**——beat-align 11/11+"
       "camera 12 段全动+transition-share 1.00 无连排+timeline 代数过皆绿；FAIL 定性=**结构性真发现非误报**："
       "BS-005=游戏公司（Biggame）主题·源池唯一直接源=biggame-cockpit 单源 45s（探针 10 帧多时点定谳："
       "全程像素园区+总控弹窗）·b5 AI 军团+b7 像素小镇唯二直接证据面·**数字错位避用律**（HUD 待审 4 款/"
       "公告栏 8 项/2 分钟刷新/¥0 ≠ 拍稿 8 款/12 条/10 分钟/无收入主张）禁硬贴 BigStream 面源（声画错位="
       "CEO 工作流令红线·R186 同法执行）·诚实对位上限 4/12 仍远低于 0.80 门线；处置=**门线不动**（利益回避·"
       "BS-005 在途·门线校准背景=BS-003/004 本司富源主题 83%）+闭环路径=素材源扩充（Biggame 驾驶舱多面板"
       "实录·宪法/账本面板若有）→对位表重构→重渲→S2 复跑→E8→M4→F-005 | **FAIL=源池缺口探测器的正确触发**"
       "（跨司主题单源=真实缺口锚·素材采集线候选·非门线误报） | `.bs005-tmp/s2-results.md`+"
       "`.bs005-tmp/probe-src/`（10 帧探针）+`data/sources/bs005/cards-v1-matched.json`+"
       "`bs-005-v1-shipinhao-60s.mp4.plan.json`（入 git） |")
with io.open(SR, "a", encoding="utf-8") as f:
    f.write(row)

# 3) bs005 README: S2 gate state section
RM = REPO / "data" / "sources" / "bs005" / "README.md"
sub(RM,
    "- S2 机检面：**待做（R-E shipinhao 渲染→ai_feel+层 1.8+spec 三门）**——对位表已落盘\n- E8 终审/M4/成品库：待续链（E4 参考仪=e4_call.py 通道·BS-004 同型）",
    ("- S2 机检面：**ai_feel PASS+spec PASS+层 1.8 FAIL（R192·visual-ratio 0.17<0.80）**——ai_feel 0 FAIL 0 WARN"
     "（gaps 11 处 0.220-0.558s·CV 0.219/0.231·prosody 9 档）+spec 微信视频号双 PASS（9:16+58.41s 入 30-60s·"
     "1.6s 余量）+层 1.8 六面 5 PASS+1 FAIL：对位率 2/12 结构性低于门线（游戏公司主题×源池单源 45s·"
     "数字错位避用律禁硬贴·探针定谳 b5/b7 唯二直接证据面·诚实上限 4/12）——**闭环路径=素材源扩充"
     "（Biggame 驾驶舱多面板实录：宪法/账本/软著面板若有）→对位表重构→重渲→S2 复跑**；门线修改="
     "利益回避不在本件在途时（BS-003/004 达标背景=本司富源主题 83%）；渲染件=bs-005-v1-shipinhao-60s.mp4"
     "（12 段 11 柔转场 0 硬切·58.41s）\n- E8 终审/M4/成品库：**待 S2 闭环后续链**（E4 参考仪=e4_call.py 通道·"
     "BS-004 同型）"))

# 4) backlog #4 R192 annotation amendment (render+S2 actually done this round)
BK = REPO / "src" / "os" / "backlog.md"
sub(BK,
    "下轮=R-E shipinhao 渲染→S2 三门→E8 终审（E4 参考仪 e4_call 通道）→M4→F-005 登记（批次① 第五件·视频号线收尾件）]**",
    ("R192 轮内续做：R-E shipinhao 渲染毕=bs-005-v1-shipinhao-60s.mp4（12 段 11 柔转场 0 硬切·58.41s 实测·"
     "1.6s 余量·plan.json 入 git）→**S2 三门=ai_feel PASS+spec PASS+层 1.8 FAIL（visual-ratio 0.17<0.80）**"
     "——结构性真发现：游戏公司主题×源池单源（biggame-cockpit 45s 唯一直接源）·数字错位避用律禁硬贴·"
     "诚实对位上限 4/12≠0.80 门线（门线校准背景=BS-003/004 本司富源主题 83%）·FAIL 如实入 station-reviews+"
     "renders 台账；**门线不动（利益回避·在途件）**；下轮闭环路径=①素材源扩充探查（Biggame 驾驶舱多面板"
     "实录：宪法/账本/软著面板若有·游戏窗在开则录）→对位表重构→重渲→S2 复跑→E8→M4→F-005；②游戏窗"
     "不可开=如实记 blocked+素材采集线候选呈报（源池缺口锚在案）；批次① 收尾件续做（claim e20fa27 沿用）]**"))

# 5) state.json: rewrite R192 log entry + focus R193
ST = REPO / "src" / "os" / "state.json"
cfg = json.loads(ST.read_text(encoding="utf-8"))
assert cfg["log"][-1].startswith("2026-09-25 02:5x R192"), "last log not R192"
cfg["log"][-1] = (
    "2026-09-25 03:0x R192: 生产轮·BS-005 S1 v1.5 首件真门 10/10 PASS+空气预算 v3 定稿+对位表+渲染+S2 三门执法"
    "（claim e20fa27 续做·实活轮）——①S1 一审 02:42:40 落判（R191 wrapper PID 54232 落地首读·判词档 "
    "20260925-024240+expert-calls 行 wrapper 自动·台账 19 行）=10/10 PASS·违律清单「无」·一次过零整改——S1 v1.5 "
    "违律扣分制首件真门实证（对照 BS-004 同位旧制链 audit2b 5 旗 FAIL/audit3 4 旗核驳升裁=同材料判据差即机制"
    "缺陷差·#24 根修生产实证第二件·首件=R190 冒烟）；②空气预算两道裁口：v1 TTS 66.16s 超窗→v2 机械裁 22 字"
    "=61.03s 仍超→v3 再裁 14 字=58.39s 定稿（1.6s 余量·fleet 同族·卡片行零动·四系统日志标记位零动·事实 8/10/12 "
    "全保·b1 反写/b3 值得停留=卡锚原文对齐）+TTS light 定稿音轨 .bs005-tmp（audio.mp3+subs.srt 12 cues+cards.json "
    "基线·BGM-A 纯净·--template=bs004 v14 批口径·v1/v2/v3 beats 留档）；③分镜对位表 cards-v1-matched.json 落盘"
    "（探针先行=biggame-cockpit 10 帧多时点扫描·R186 段中尾帧教训执行：全程像素园区+总控弹窗·对位率 2/12——"
    "b5 AI 军团+b7 像素小镇唯二直接证据面·同源多用注记·余 10 拍 cards-only 逐拍注理由·数字错位避用律执行〔HUD "
    "待审4款/公告栏8项/2分钟刷新/¥0 vs b2 8款/b9 12条/b6 10分钟/b10 收入面〕）；④R-E shipinhao 渲染毕="
    "bs-005-v1-shipinhao-60s.mp4（12 段 11 柔转场 0 硬切·9:16 1080×1920·58.41s 实测·plan.json 入 git）；"
    "⑤S2 三门循环独立执法=ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s·pacing CV 0.219·prosody 9 档·copy CV "
    "0.231）+spec 微信视频号双 PASS（9:16+58.41s 入 30-60s·1.6s 余量）+**层 1.8 FAIL（visual-ratio 0.17<0.80）**"
    "——定性=结构性真发现非误报：游戏公司主题×源池单源 45s·诚实对位上限 4/12≠门线·FAIL 如实入 station-reviews+"
    "renders 台账·门线不动（利益回避·BS-005 在途·校准背景=BS-003/004 本司富源主题 83%）；⑥台账=bs005 README "
    "四节更新+backlog #4 R192 注+renders 行+station-reviews S2 行+status-export 刷（expert-calls 19 行·"
    "tick192）；三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面（+1 在链预期红="
    "render-unannot bs-005·R173 同型先例·F-005 登记即清）/loop_health 0 FAIL 9 WARN 皆在案史实（tick192=done192 "
    "对账同步）；例行件：日报 2026-09-25 在案不重跑（R180 补产）·W39 周审在案·global-benchmarks day1 ≤7 跳过"
    "（下期 ~10-01）·T1 催办线 v9/v10=09-25 22:0x 未到不催·CEO 拣式 v12-vs-live-A 仍无回示·HQ-FEEDBACK 不写"
    "（无集团层新 open 问题·ledger 14=锚·decisions 24=锚）·tokens:local=1（S1 一审 qwen2.5:14b=R191 起飞本轮落地"
    "记账·本地 Ollama 零 API token·P-54⑤ 计量律）。下轮=R193 BS-005 S2 FAIL 闭环（素材源扩充探查→Biggame "
    "驾驶舱多面板实录→对位表重构→重渲→S2 复跑→E8→M4→F-005）。")
cfg["focus"] = (
    "R193: BS-005 S2 FAIL 闭环（claim e20fa27 续做·批次① 第五件）——①素材源扩充探查：Biggame 游戏窗在开"
    "→record_screen 实录驾驶舱多面板（宪法/约束清单/账本/软著面板若有·每源三时点扫描防录穿·R186 教训）→"
    "对位表重构（b2/b9 等数字错位拍以真面板解锁）→重渲→S2 三门复跑（层 1.8 visual-ratio 复判）；②游戏窗"
    "不可开=如实记 blocked+源池缺口锚呈报（素材采集线候选·不造活）；S2 闭环→E8 终审（七席+E4 参考仪 e4_call "
    "通道）→M4→F-005 登记（批次① 视频号线收尾件）→下一件=N=6 第六件团结引擎增强版（#5 映射在案）或 #14 "
    "B站深纵认领判断；发布锁=M5 账号物理件（CEO 面·现状行不催办）。")
ST.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ledgers consolidated: renders+station+readme+backlog+state")
