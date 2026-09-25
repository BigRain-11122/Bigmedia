# -*- coding: utf-8 -*-
# R273 idle-fast accounting: state.json (tick/log/focus/ts/task) + status-export.json
# (export_ts + light derivation). No commit this round (batch window 1/6).
import io
import json
import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = ROOT + r"\src\os\state.json"
XP = ROOT + r"\docs\status-export.json"

now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")
xts = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
prefix = now.strftime("%Y-%m-%d %H:%M")

log_line = (
    prefix + " R273: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 1/6）——"
    "①无新令（orders 顶=O-20260925-1720-bm-a·R271 已记账）"
    "②backlog 顶行不可认领（#30 done〔O-1720 音频重渲染腿 R271-R272 毕〕·#29 全毕·"
    "ch.2-ch.5 v2 稿未落盘=novel 实证止 ch.1 v2〔bm-a 面·稿落即随轮认领〕·"
    "#15 随量产逐件·#17 needs-CEO·#21 周日件今周五不到）"
    "③树净零锁（git status 空）·无 bm-a 活跃写盘迹象（audio 最新=17:36 R272 自产·novel 止 ch.1 v2）"
    "④素材窗迹象核=Biggame 总控窗开态延续但仍被 CEO 硅基仪表盘 F11 覆盖"
    "（r273_biggame_probe.py=r270 同型免 focus 取帧 rc=0〔Python UTF-8 通道复制律零违例〕·"
    "会话验图定谳：覆盖层=硅基生命元宇宙仪表盘延续态〔6 家公司/18 款游戏+bm-c 心跳 1177min 告警="
    "R270 1147min+30min 延续态+里程碑 M1 在建+M1.5 萌发黄点+指令通道离线+等你拍板卡「视频号、公众号，开号」媒体公司行与在案口径一致〕·"
    "帧内零 软著账本/12 条约束/玩法机制 新面板=D-BS-08 复活条款零触发·脱敏四项全无零敏感面）"
    "→留档观察待覆盖层关闭后安全窗复核；"
    "集团扫描=ledger 严格行含 @ 四模式 15 行=锚零新转办·decisions UTF8 非空行 29（总 32 双口径）=锚零新行零动作；"
    "例行件=日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·"
    "global-benchmarks 更新记录 2026-09-24 day2 ≤7 天跳过刷新（下期 ~10-01）·"
    "T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·"
    "tokens:local=0（探针纯脚本+会话内建验图零本地模型调用·P-54⑤ 计量律如实记）·"
    "自进清单真锚核=清单文件零变化（判据维持=无可领真锚项不凑活）；"
    "三探针全绿=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/"
    "readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+0 发现（弃件清账新基线维持·阻塞≠失败口径 exit 1）/"
    "loop_health 0 FAIL 17 WARN 皆在案史实（11 log-order+6 heartbeat-gap·tick272=done272 对账平·state-ts 门零红零滞后）"
    "——一行收账即出（本轮不 commit·并窗轮 1/6·P-61 导出步照刷 export_ts+实况派生轻量）。"
    "下轮=R274 快速路径首查（新令/集团转办/ch.2-ch.5 v2 稿落盘迹象/素材窗〔覆盖层关闭后安全窗复核〕），全静即 idle-fast（2/6）。"
)

task = log_line.split(" R273: ", 1)[1][:60]

st = json.load(io.open(SP, encoding="utf-8"))
st["tick"] = 273
st["focus"] = (
    "R274: 快速路径首查（新令/集团转办/ch.2-ch.5 v2 稿落盘迹象/素材窗覆盖层关闭后安全窗复核）"
    "→全静即 idle-fast；ch.2-ch.5 v2 稿落盘即随轮认领（v2=产线默认·O-1720 新连载节律）"
)
st["log"].append(log_line)
st["ts"] = ts
st["task"] = task
io.open(SP, "w", encoding="utf-8").write(
    json.dumps(st, ensure_ascii=False, indent=1) + "\n"
)

x = json.load(io.open(XP, encoding="utf-8"))
x["export_ts"] = xts
for d in x["depts"]:
    if d["n"] == "工程技术部":
        d["t"] = (
            "OS 循环 R273（idle-fast：五静+探针绿·素材窗延续态复核〔Biggame 总控窗仍被 CEO 仪表盘 F11 覆盖·"
            "零新面板=D-BS-08 复活条款零触发〕）·ledger @15/decisions 29 双锚稳·state.ts/task 心跳面刷新"
        )
for row in x["outs"]:
    if row[0] == "OS 循环":
        row[2] = (
            "tick 273·R273（idle-fast：五静+探针绿——O-1720 收官后静默窗·ch.2-ch.5 v2 稿未落盘〔bm-a 面〕·素材窗延续态）"
        )
for row in x["results"]:
    if row[1] == "OS 轮次":
        row[0] = "273"
io.open(XP, "w", encoding="utf-8").write(
    json.dumps(x, ensure_ascii=False, indent=2) + "\n"
)

# self-verify: reload both, assert JSON validity + key fields
st2 = json.load(io.open(SP, encoding="utf-8"))
x2 = json.load(io.open(XP, encoding="utf-8"))
assert st2["tick"] == 273 and st2["ts"] == ts and st2["task"] == task, "state fields"
assert st2["log"][-1] == log_line and len(st2["log"]) == 282, "log append"
assert x2["export_ts"] == xts, "export ts"
print("JSON_OK state tick=%d log=%d ts=%s" % (st2["tick"], len(st2["log"]), ts))
print("JSON_OK export_ts=%s" % x2["export_ts"])
