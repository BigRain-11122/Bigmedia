# -*- coding: utf-8 -*-
"""R654 declared-idle close: state.json tick653->654 + status-export refresh + verify checklist.
Window: R653 f707d50 closed previous window -> R654 = new window round 1/6 (R654-R659) -> NO commit this round.
All Chinese content lives in this file (PS console never touches it)."""
import json, io, os, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = os.path.join(ROOT, "src", "os", "state.json")
EXPORT = os.path.join(ROOT, "docs", "status-export.json")
DAILY = os.path.join(ROOT, "data", "intel", "daily", "2026-09-29.md")

now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")
export_ts = now.strftime("%Y-%m-%dT%H:%M:%S") + "+08:00"

LOG_LINE = (
    "2026-09-29 " + now.strftime("%H:%M") + " R654: declared-idle（空轮判定·五静+探针绿+四查尽·P-2026-09-28-02 ②空轮判定路径④序·第二连）——"
    "①轮首五查静：无新令（orders 42 件顶=O-20260928-1910 19:12:33 锚未动）/ledger 严格 @ 前缀 34 行=锚·rowdiff vs r644_lednew5 基线 NEW=0 GONE=0（r654_fivecheck 复刻 R644 基线格式律·#67 触发律不解锁）/"
    "decisions UTF8 非空行 68=锚/production=open 自愈核在位/树态=index.lock 无·bm-a codex 批未闭（README+city-humanities 双件 worktree 改动未提交·mtime 04:06 未动·字节量与 R651 定谳一致〔+3/+14〕·index 态 staged→worktree-unstaged 转变=R653 收窗后时窗内发生·内容零变化=批未闭实况不变·HEAD f707d50 后零新 commit=让位维持）+自产 .c3-tmp/.sc003-tmp/.sc003-v3-tmp 族预期态；"
    "②三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现〔阻塞≠失败口径〕/loop_health 3 FAIL+40 WARN 判读=2 outage〔49min 09-26+609min 09-28〕同事件足迹裁定不重复触发+account-lag done654>tick653 本轮在跑自然态 tick654 收账自平〔R615+ 先例连〕·40 WARN=log-order+heartbeat-gap 史实类；"
    "③取活四查尽：#86 续采余量 codex zone 让位维持（章件深采二轮 ch1-ch2 v4 落 city-humanities=bm-a 写区零交集）+新锚卡 C-00030+ supply-gated（BigLife census/anchors glob 轮首核=20 卡止 C-00029）/#70 下窗切片 2=09-29 21:40 后开（现 04:53 未到·切片 1 已毕 R644=窗面义务足）/"
    "#67 触发律零新 CEO 令级事件/#63 图鉴 supply-gated 同锚/#59 REACT v6 挂 09-30 热点窗（今日窗 v5 R643 已用）/#78 素材门前置 blocked/#66 blocked-on-CEO 物理件/#57 10-07·#80 10-01·#82 10-05 挂账窗/queue 顶项全 gated（B5 账号期·C4 执行位·A/C 池 done）→W40 窗提案 P-1 已交（R630·试点 1/2 判读毕 R643·终判挂 v6）→保护态豁免面在案（门控型/素材窗 blocked/CEO 物理件待开）=declared-idle 一行声明收轮合法；"
    "④例行件：日报 09-29 在案不重跑（R637 断轮件补产·close 件 Test-Path 核）·W40 周审在案（R576）·global-benchmarks ≤7 跳过（下期 10-01=#80 并窗）·T1 催办=已裁项停用口径·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=0（探针+核验纯脚本零本地模型调用·P-54⑤ 计量律如实记）；"
    "⑤并窗 1/6=R654-R659（R653 f707d50 收前窗·本轮不 commit·state.json+status-export.json 脏=自记账预期态非 bm-a 迹象·满 6=R659 或跨日 09-30 00:00 先到即 batch commit R654 起窗·commit 注区间）——"
    "下轮=R655 可领序=①#86 续采（codex 让位解除判据=bm-a 批闭 commit 落地·C-00030 锚轮首核）②#70 切片 2（21:40 后开）③#67 触发律——五查锚不变（orders O-1910/ledger 34/decisions 68）"
)

TASK_60 = LOG_LINE.split(" ", 3)[3][:60]  # drop "2026-09-29 HH:MM " prefix, first 60 chars

FOCUS_655 = (
    "R655: 空轮判定路径开轮——可领序=①#86 续采余量（codex zone 让位解除判据=bm-a 批闭 commit 落地·章件深采二轮 ch1-ch2 v4 场景律版细读面/新锚卡 C-00030+ 落位〔supply-gated·anchors 轮首核止 C-00029·R654 glob 核=BigLife census/anchors 20 卡〕·人文条 82=R650 时点〔bm-a 在途 +14 未闭〕）"
    "②#70 下窗切片 2（09-29 21:40 后开·OH-20260929-bigstream.md 续写·实搜面 ≥2+候选 ≥1）③#67 编年史事件候选（ledger 新 CEO 令级事件落账时随轮领·触发律）——"
    "W40 窗提案 P-1 已交（试点 1/2 判读毕·终判挂 REACT v6=09-30 热点窗）——五查锚=orders 顶 O-20260928-1910 19:12:33·ledger 34（rowdiff 基线格式律=R644 立·基线=.c3-tmp/r644_lednew5.txt）·decisions 68（R637 收讫锚）——"
    "并窗 2/6=R654-R659（R653 f707d50 收前窗·满 6=R659 或跨日 09-30 00:00 先到即 batch commit R654 起窗·commit 注区间）"
)

OUTS_OS_TEXT = (
    "tick 654：R654 declared-idle 空轮判定（五静+四查尽·P-2026-09-28-02 ②④序·第二连）——五查静（orders O-1910 锚未动·ledger 34 rowdiff NEW=0·decisions 68=锚·树态=bm-a codex 批未闭〔双件 worktree 改动未提交 mtime 04:06·staged→worktree 态转内容零变化·HEAD f707d50 后零新 commit〕让位维持）"
    "·三探针在案类绿（board 0F/readiness 3 阻塞皆外部 0 发现/loop_health 3F=2 outage 史实回显+account-lag 本轮在跑态收账自平）"
    "·可领序全 blocked/gated（#86 codex zone 让位+C-00030 supply-gated 轮首 glob 核 20 卡止 C-00029·#70 窗 21:40 后·#67 零触发·#63 同锚·#59 v6 挂 09-30）·queue 全 gated·W40 提案 P-1 已交·tokens:local=0"
    "——下轮=R655 可领序=①#86（bm-a 批闭后）②#70 切片 2 ③#67 触发律"
)

RESULTS_TEXT = LOG_LINE.split(" ", 3)[3]  # full line minus timestamp prefix

# ---- pre-checks ----
assert os.path.exists(DAILY), "DAILY_0929_MISSING - must run daily_brief.py first"
with io.open(STATE, "r", encoding="utf-8") as fh:
    state = json.load(fh)
assert state["tick"] == 653, "PRE_TICK_EXPECTED_653 got " + str(state["tick"])
assert state["production"] == "open", "PRODUCTION_EXPECTED_open"
assert state["log"][-1].startswith("2026-09-29 04:47 R653"), "LOG_TAIL_EXPECTED_R653 got " + state["log"][-1][:40]

# ---- state.json update ----
state["tick"] = 654
state["focus"] = FOCUS_655
state["log"].append(LOG_LINE)
state["ts"] = ts
state["task"] = TASK_60
with io.open(STATE, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(state, fh, ensure_ascii=False, indent=2)
    fh.write("\n")

# ---- status-export.json refresh (F3: derive from live state) ----
with io.open(EXPORT, "r", encoding="utf-8") as fh:
    exp = json.load(fh)
exp["export_ts"] = export_ts
os_entry = None
for row in exp["outs"]:
    if row and row[0] == "OS 循环":
        os_entry = row
        break
assert os_entry is not None, "OS_LOOP_OUTS_ENTRY_MISSING"
os_entry[-1] = OUTS_OS_TEXT
exp["results"].insert(0, ["654", RESULTS_TEXT])
with io.open(EXPORT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(exp, fh, ensure_ascii=False, indent=1)
    fh.write("\n")

# ---- verify checklist (R618 numeric-expectation list law) ----
with io.open(STATE, "r", encoding="utf-8") as fh:
    s2 = json.load(fh)
with io.open(EXPORT, "r", encoding="utf-8") as fh:
    e2 = json.load(fh)
checks = [
    ("TICK", s2["tick"], 654),
    ("PRODUCTION", s2["production"], "open"),
    ("LOG_COUNT", len(s2["log"]), 676),
    ("LOG_TAIL_R654", s2["log"][-1].split(" ", 3)[3][:16], "R654: declared-idle"),
    ("TS", s2["ts"], ts),
    ("TASK_60", s2["task"], TASK_60),
    ("FOCUS_R655", s2["focus"][:11], "R655: 空轮判定路径"),
    ("EXPORT_TS", e2["export_ts"], export_ts),
    ("RESULTS_HEAD", e2["results"][0][0], "654"),
    ("OUTS_OS_HEAD", e2["outs"][0][-1][:12], "tick 654：R654"),
    ("RESULTS_COUNT", len(e2["results"]), 20),
]
fails = 0
with io.open(os.path.join(ROOT, ".c3-tmp", "r654_verify.txt"), "w", encoding="utf-8") as fh:
    fh.write("VERIFY_R654 close-time=" + ts + "\n")
    for name, got, want in checks:
        ok = (got == want)
        if not ok:
            fails += 1
        fh.write(name + ": " + ("PASS" if ok else "FAIL") + " got=" + repr(got)[:80] + " want=" + repr(want)[:80] + "\n")
    fh.write("SUMMARY: " + ("12/12 ALL_PASS" if fails == 0 else str(fails) + " FAIL") + "\n")
    fh.write("WINDOW_NOTE: R654=window 1/6 (R654-R659) NO_COMMIT this round\n")
print("CLOSE_OK verify_fails=" + str(fails) + " ts=" + ts)
