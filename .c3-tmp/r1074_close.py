# -*- coding: utf-8 -*-
# R1074 declared-idle close (window 6/6 = FULL) -> batch close R1069-R1074.
# Sub-checks (board rows / briefs / W40 / GB gate / #86 content-addressing) + state tick+1
# + log append + ts/task/focus refresh + export refresh (export_ts + results append + live row1).
# Per os-protocol S6 window law + R1073 focus. Commit lands right after this script (single window batch).
import json, io, os, re, glob
from datetime import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
HQ = r"C:\Users\sjs20\Desktop\FluxGroup"
LIFE = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife"

now = datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")
tsm = now.strftime("%H:%M") + "x"

# ---------- Part A: remaining sub-checks -> r1074_check2.txt ----------
out = []
p = out.append
p("[sub-check time] " + ts)

dtxt = io.open(os.path.join(HQ, "docs", "decisions.md"), encoding="utf-8", errors="replace").read()
m = re.search(r"派工通告板(.*?)(?:\n#{1,3} |\Z)", dtxt, re.S)
board = m.group(1) if m else ""
brows = [ln.strip() for ln in board.splitlines() if re.search(r"BigStream|七司", ln)]
p("board BigStream/七司 rows = %d (baseline 8, collected set D-20261003-01~04 per R1031)" % len(brows))
for ln in brows:
    p("  BOARD: " + ln[:180])

p("brief 10-03 exists = %s / 10-04 exists = %s (day-boundary item)" % (
    os.path.exists(os.path.join(ROOT, "data/intel/daily/2026-10-03.md")),
    os.path.exists(os.path.join(ROOT, "data/intel/daily/2026-10-04.md"))))
p("W40 self-audit exists = %s" % os.path.exists(os.path.join(ROOT, "docs/audits/2026-W40-self-audit.md")))
gb = io.open(os.path.join(ROOT, "docs/global-benchmarks.md"), encoding="utf-8", errors="replace").read()
mm = re.search(r"2026-\d{2}-\d{2}", gb)
p("global-benchmarks latest date = %s (gate due 10-08)" % (mm.group(0) if mm else "NONE"))

pj = os.path.join(LIFE, "cognition", "pools.json")
t = io.open(pj, encoding="utf-8").read()
mw = re.search(r"TOTAL_LINES[^0-9]*(\d+)", t)
p("pools.json TOTAL_LINES marker = %s (baseline 1440, content-addressing law) / phys_lines = %d" % (
    mw.group(1) if mw else "?", t.count("\n")))
il = os.path.join(LIFE, "cognition", "interchat-ledger.jsonl")
ti = io.open(il, encoding="utf-8").read().strip()
p("interchat entries = %d (baseline 22)" % (ti.count("\n") + 1 if ti else 0))
p("CENSUS C-00030 present = %s (gate closed expected False)" % os.path.exists(
    os.path.join(LIFE, "census", "anchors", "C-00030.md")))

io.open(os.path.join(ROOT, ".c3-tmp", "r1074_check2.txt"), "w", encoding="utf-8").write("\n".join(out))
print("CHECK2 OK board_rows=%d pools=%s interchat_ok" % (len(brows), mw.group(1) if mw else "?"))

# ---------- Part B: state.json ----------
LOG_LINE = (
 "2026-10-03 {tsm} R1074: declared-idle 声明轮并窗第六轮 6/6=窗满→batch close commit 区间 R1069-R1074（os-protocol §6 并窗律·六轮声明窗一盘收账·commit 消息注区间·并窗重置 1/6）——"
 "①轮首五查 fresh 实跑（r1074_check.txt 09:0x：orders 顶=O-20260928-1910 mtime 09-28 19:12:33 fresh 零新令/ledger @target 41 行==冻结基线零新派工行〔mtime 10-03 03:13:47=R1045 夜班例行条目承继〕/decisions dnum 内容寻址差集 NEW_DNUMS=[]·水位 131==file 131〔D-20260930-19 差集制〕+派工通告板涉司行 fresh 复核全在案收讫〔r1074_check2.txt〕/无 index.lock 实测 False/production=open 自核 ✓ tick1073/树态=M state.json+M .c3-tmp 探针输出+?? r1069-r1073 证据件=并窗自记账预期态零 bm-a 活跃写盘迹象）；"
 "②三探针 fresh 实跑（r1074_probe_digest.txt）：board 0 FAIL（5 ideas 10 drafts 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE+#17）0 findings〔阻塞≠失败口径〕/loop_health 3 FAIL+125 WARN==基线平零新增（两 outage=09-26/09-28 史实+account-lag done 1077>tick1073=+4 恒差承继 R981/R1054 定谳断洞族净累计非本轮新现·tick1074 收账自平口径）；"
 "③#86 三腿内容寻址 fresh 复核（r1074_check2.txt：a 腿 pools.json TOTAL_LINES 标记 1440==基线持平·c 腿 interchat 22==基线持平·CENSUS C-00030 absent 供给闸闭维持——pools mtime 3h 周期假信号族已注·内容寻址定谳律 R1069 同法）；"
 "④四查尽承继 R1069-R1073 fresh 链+backlog 开行全门控（#70 OSS 窗 4=10-05 21:40 未开/#67 DIGEST 触发律零新 CEO 令级事件〔ledger 冻结〕/#63 CENSUS 供给闸闭/#57 替代率首报=10-07 治理日/#59 REACT-v9=10-04 窗〔10-03 窗 R1030 判负在案·连续第二窗判负=池扩容呈报位〕/#94①=10-04 记忆 ≤10KB 梳理窗②=10-05 席 6 确认/#31+#27=bm-a 稿未落〔ch.5 v3/ch.6〕/queue §B B3 W41 期=10-10 未到期/§D 提案轨 W40 窗 P-1 pilot-closed 终判毕=每窗 ≥1 达标〔W41=10-05 起〕/§E 批活池=E30 DAILY 保护态维持〔解锁窗台账 R1032 承继·morning 桶开门件 v62 已耗 R1062·解锁窗均未触发〕）→真无活可拉+保护态豁免面在案（R1032/R810 供给侧盘点+R1069-R1073 fresh 承继链·结构性 blocked 非违规闲置·造活凑数=空转第四形态禁）；"
 "⑤时间闸核=当前 {tsm} 全程 10-03 窗内：10-04 日界未至（10-04 日报缺=日界件先补产→E31 REACT-v9 热点窗全链 F-148〔连续第二窗判负=池扩容呈报〕+#94 记忆 ≤10KB 梳理）·W41 周轮件=10-05·OSS 窗 4=10-05 21:40·W40 周审在案·GB 闸 10-08 非到期〔§④ 最近刷新=10-01〕；"
 "⑥记账预算=纯记账 2 处（state log+export 刷新）≤5 ✓·export 刷=batch close 惯例（export_ts+results 追加+live 当前活行·F3 律实况派生）·tokens:local=0（纯脚本探针零本地模型调用·P-54⑤ 计量律如实记）·HQ-FEEDBACK 不写（当日集团层零本司 open 项·D-20261003 批 R1031 全收讫态承继·零膨胀）"
 "——waiting: time-gated+supply-gated lanes held（卡点=10-04 日界三件〔10-04 日报先补产→E31 REACT-v9 热点窗全链 F-148+#94 记忆 ≤10KB 梳理〕/10-05 W41 周轮件+OSS 窗 4 21:40/10-07 替代率首报/10-08 GB 刷+E30 解锁窗〔rain/CEO 令日/10-08 复市/Nov+ 寒潮〕/#86 池扩容触发〔pools 1440/interchat 22 双基线持平〕均未发生）ETA 2026-10-04 00:00〔最近日界·10-04 窗三件开领〕·声明轮并窗计数=6/6 窗满本盘 commit 区间 R1069-R1074·并窗重置 1/6"
).format(tsm=tsm)

TASK = LOG_LINE.split("R1074: ", 1)[1][:60]

FOCUS = (
 "R1074: declared-idle 声明轮 6/6 → batch close R1069-R1074 收账毕（并窗重置 1/6·六轮声明窗一盘 commit·五静 fresh+探针基线平·decisions 水位 131 静·#86 pools 1440/interchat 22 内容寻址双持平）"
 "——下轮 R1075=新窗第一轮：①快速路径五查+三探针照跑（任一异常〔新令/派工行/探针 FAIL/可领活/脏树异常〕即转全任务书照走）"
 "②10-04 日界三件=10-04 日报先补产→E31 REACT-v9 热点窗全链 F-148〔连续第二窗判负=池扩容呈报〕+#94 记忆 ≤10KB 梳理"
 "③W41 周轮件=10-05·OSS w4=10-05 21:40 开窗即领④E30 DAILY 保护态维持（解锁窗台账 R1032 承继）"
 "⑤#86 三腿 fresh 核（pools mtime 3h 周期假信号族已注·内容寻址 1440/22 定谳律）"
)

sp = os.path.join(ROOT, "src", "os", "state.json")
with open(sp, encoding="utf-8") as f:
    st = json.load(f)
assert st["tick"] == 1073, "unexpected tick %s" % st["tick"]
st["tick"] = 1074
st["ts"] = ts
st["task"] = TASK
st["focus"] = FOCUS
st["log"].append(LOG_LINE)
with open(sp, "w", encoding="utf-8") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
print("STATE OK tick=1074 ts=%s" % ts)

# ---------- Part C: status-export.json ----------
ep = os.path.join(ROOT, "docs", "status-export.json")
ex = json.load(io.open(ep, encoding="utf-8"))
ex["export_ts"] = ts
RESULT_ROW = [
    "1074",
    ("2026-10-03 {tsm} R1074: declared-idle 声明轮 6/6 → batch close R1069-R1074（六轮声明窗一盘 commit·五静 fresh+探针基线平"
     "·decisions 水位 131 静·#86 pools 1440/interchat 22 内容寻址双持平·全 lane 时间/供给门控维持·waiting 10-04 日界三件 ETA 10-04 00:00）"
     "——详见 state.json log R1074 行").format(tsm=tsm),
]
if ex.get("results") and ex["results"][-1][0] == "1074":
    pass
else:
    ex["results"].append(RESULT_ROW)
ex["live"][0] = ["当前活：R1074 declared-idle 6/6 batch close R1069-R1074 收账毕（全 lane 时间/供给门控维持·2026-10-03 {tsm}）".format(tsm=tsm)]
with io.open(ep, "w", encoding="utf-8") as f:
    json.dump(ex, f, ensure_ascii=False, indent=1)
print("EXPORT OK export_ts=%s results=%d live1 updated" % (ts, len(ex["results"])))
