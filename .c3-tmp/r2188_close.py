# -*- coding: utf-8 -*-
"""R2188 close: workday waiting-state round + tech#150 consumption (queue law:
inside the waiting window, skip truly-gated P2 head #126 and take the next
executable item = #150).

Real work this round:
- tech#150 criterion: subsequent-round close scripts grep `finalize_state` hit
  = gate in place. THIS close is the first post-wiring subsequent round and
  routes its own accounting through finalize_state (born gate), so the
  criterion is met with live evidence; #150 done-marked with date in the
  queue (consumption write-back law).
"""
import io
import json
import sys
from datetime import datetime

REPO = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
sys.path.insert(0, REPO + r"\src\os")
from close_commit import finalize_state, run_close_commit

STATE = REPO + r"\src\os\state.json"
TECH = REPO + r"\state\queue\tech.md"
LEDGER = REPO + r"\data\pipeline\fire-consume-ledger.jsonl"
CLOSE = REPO + r"\.c3-tmp\r2188_close.py"

# --- 0. anchor guard: last ledger line must be R2187 (concurrent-write law) ---
with io.open(STATE, "r", encoding="utf-8") as f:
    st = json.load(f)
if "R2187" not in st["log"][-1]:
    raise SystemExit("ANCHOR-GUARD-FAIL: last log line is not R2187: " + st["log"][-1][:80])
print("STEP anchor ok: last=R2187 tick=%d" % st["tick"])

# --- 1. tech#150 done-mark (surgical append to the #150 line, unique anchor) ---
ANCHOR = u"手写族再复发 ≥2 轮=升裁 lint 面（close 脚本 static check 候选）。"
DONE = (
    u"——[done 2026-10-13 R2188] ——已交付：**判据达成=R2188 收账正身实弹首证**"
    u"（r2188_close.py 走 finalize_state 正身=任务书面 tech#149 句落位后首个后续轮 "
    u"close 脚本 grep `finalize_state` 命中=闸在位·双载体闭环〔任务书面强制律+本轮正身示范〕"
    u"·手写族 R2186 后零复发·复发 ≥2 轮升裁 lint 面条款本条目内常设承继）"
)
with io.open(TECH, "r", encoding="utf-8", newline="") as f:
    tech_raw = f.read()
assert tech_raw.count(ANCHOR) == 1, "tech#150 tail anchor count != 1"
assert "[done 2026-10-13 R2188]" not in tech_raw, "tech#150 already done-marked"
patched_tech = tech_raw.replace(ANCHOR, ANCHOR + DONE, 1)
assert "[done 2026-10-13 R2188]" in patched_tech
with io.open(TECH, "w", encoding="utf-8", newline="") as f:
    f.write(patched_tech)
print("STEP tech.md #150 done-marked (consumption write-back)")

# --- 2. this round's accounting through the born gate (finalize_state) ---
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
stamp = now[11:16]  # HH:MM real clock
log_line = (
    u"2026-10-13 " + stamp + u" R2188: 等待态+tech#150 消费轮"
    u"（工作日零排单窗 08:00-23:59·O-20261012-1505 续执·等待对象同上不重扫）"
    u"——①五查全静=own orders 锚 O-20260908-1105 mtime 10-08 12:08 维持"
    u"+origin_gap_check QUIET ahead0 behind0+group_scan 六面 fresh 20:02"
    u"（DECISIONS truly_new=0 水位 154+LEDGER @BigStream 5 行值守锚零新转办"
    u"+ORDERS rows=372 tail '10-13 18:5x'==stored 零新行"
    u"+ORDERS-ORIGIN-DELTA delta=1=R2186 已消化 row 373 残差〔FleetLink 未拉平·无 >373 新行〕"
    u"+DIGEST-SUPPLY advisory 1 row-date 10-13 age0d 已裁决面〔F-182 staged+夜窗 DIGEST-v20〕）"
    u"+树=MV-lane 预期脏面 14 件零锁（R1745 零接触承继）；"
    u"②三探针带内=board 0 FAIL（5 题 10 稿·5 in production）"
    u"/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17）"
    u"+1 发现 react-v16 unannot=F-183 夜窗登记即清（R2118 裁定维持）"
    u"/loop_health 3F+290W 皆在案史实（三 outage 窗+drift 18≤21 adjudicated）；"
    u"③fire_consume --ledger 正身直发=no-fire rc1 reason=bm-a-workday-hours-zero-dispatch"
    u"（20:03:33 收据·ledger 行随本 commit 入账）"
    u"→F-180 SC-005-07+F-181 REACT-v15+F-182 DIGEST-v19+F-183 REACT-v16 四件 fire-ready carried"
    u"·真窗=10-14 夜窗 00:00-08:00（撤 AIHOT pause 旗+worker-restart main#21+fire 接力"
    u"+tech#126 校准冒烟+DIGEST-v20 产线）或 CEO 下班旗再落；"
    u"④本轮取活=tech#150 消费收口（等待窗内 P2 队头跳过真 gated #126 取下一可执行项）"
    u"：判据达成=R2188 收账正身实弹（r2188_close.py 走 finalize_state 正身"
    u"=任务书面 tech#149 句落位后首个后续轮 close 脚本 grep 命中=闸在位·双载体闭环"
    u"·手写族 R2186 后零复发·复发 ≥2 轮升裁 lint 面条款条目内常设）——#150 done 标日期回写队列；"
    u"⑤队列盘点=queue_status fresh 20:03 实读（backlog claimable 8 皆他窗 lane/gated"
    u"〔head #110 Toonflow=夜窗装机位〕+main claimable 2 皆 MV 域零接触查看位"
    u"〔#7 krea2 R2144 冻结+#27b A/B GPU 独占窗〕+tech #150 消费后 claimable 1 gated"
    u"〔#126 夜窗校准·10-14 08:00 权威窗锚〕+explore 0）；"
    u"⑥例行件=10-13 日报在案不重跑（R2086 一份为真相）·W42 周审在案（R2011）"
    u"·GB §④ 下期 10-15 ≤7d 跳过+export=skip <24h（export_ts 12:44:35 ~7.3h 龄"
    u"·实况零变化·tech#148 强制律下 skip=零写入安全态）"
    u"·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）"
    u"·T1 催办无超线项（账号物理件=呈现状行不催办）"
    u"·tokens:local=0（探针/直读/fire 卡读=档案读写零本地模型产出调用·P-54⑤ 计量律）；"
    u"⑦队列补货步=tech#150 消费后真无独立新种子如实注记零膨胀（五查全静+探针稳·禁凑数律）"
    u"·临时件清理钩=本轮读数会话内直读零落盘·close 脚本照 tech#81 自含律入账"
    u"——下轮=等待态续（等待对象同上不重扫）"
    u"·10-14 夜窗 00:00 开窗即转收口三连（撤旗+main#21 重启+fire 接力+tech#126 冒烟+DIGEST-v20）"
)
summary = finalize_state(log_line=log_line, ts=now)
print("STATE-FINALIZED tick=%s ts=%s" % (summary["tick"], summary["ts"]))

msg = (
    "R2188: workday waiting-state + tech#150 consumption: P2 head (skip gated #126) -> "
    "#150 criterion met with live evidence, R2188 close routes accounting via "
    "finalize_state born gate (first post-wiring close-script grep hit = gate in place; "
    "hand-rolled family zero recurrence since R2186; lint escalation clause stands in queue "
    "entry); #150 done-marked; five checks quiet (orders rows 372==stored, origin delta=1 = "
    "R2186-digested residual), probes in-band, F-180~183 fire-ready carried, next window "
    "10-14 00:00 night relay [via bm-a]"
)
rc, lines = run_close_commit(
    files=[STATE, TECH, LEDGER, CLOSE],
    message=msg,
)
for l in lines:
    print(l)
print("R2188 close done rc=%d" % rc)
