# R219 idle-fast close: state.json tick/log/focus + status-export.json export_ts refresh
import json, io, re
from datetime import datetime

now = datetime.now()
stamp = "%02d:%02d" % (now.hour, now.minute)
decade = "%02d:%dx" % (now.hour, now.minute // 10)
ts_iso = now.strftime("%Y-%m-%dT%H:%M:00+08:00")

# ---- state.json ----
p = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
st = json.load(io.open(p, encoding="utf-8"))
assert st["tick"] == 218, "tick anchor mismatch: %s" % st["tick"]
st["tick"] = 219
st["focus"] = (
    "R220: ①快速路径五查（素材窗迹象优先：新令/ledger 严格行含 @ 前缀锚 14/decisions UTF8 非空行锚 24/树态/bm-a 写盘迹象）"
    "——任一不静转全任务书②生产线=BS-005 原版+bs005e 双 blocked 维持（共享开窗实录批·素材窗一开即续链：对位表重构→重渲→S2 复跑→E8→M4→F-005/F-007·新源规格化 prep_vertical --batch 一跑直达）"
    "③无在途生产件时按空转规则取 docs/self-improvement-queue.md 顶项执行（真锚核·不凑工作量造活）"
    "④例行=探针三件套照跑（readiness 预期=bs-005/bs-005e 双 render-unannot blocked 在链预期红维持·双件登记即清）"
    "⑤idle-fast 并窗计数=R220 第 2/6（R218 窗满已 batch commit R213-R218·R219 起 1/6）——跨日边界/任一异常/实活轮出现即收账。"
)
log_line = (
    "2026-09-25 " + decade + " R219: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 1/6）——"
    "①无新令（orders 顶=O-2126·R170 已记账）"
    "②backlog 顶行不可认领（生产队列=N6 收官六件在库 F-001~F-004 视频号+F-005 B站深纵+F-006 抖音快剪·BS-005 原版/bs005e 双 blocked 待素材窗·#15 随量产逐件·#17 needs-CEO·#21 周日件今周五不到）"
    "③树净=R218 batch commit 后零 M 追踪件·仅自产 blocked 批中间件未提交（.bs005-tmp/.bs005e-tmp 批闭收账惯例维持）·无 index.lock·无 bm-a 活跃写盘迹象"
    "④素材窗迹象核=窗口枚举 15 窗零 Biggame 总控窗（Tuanjie 态=Unity Error+Game+GUIAgentUnity DemoScene+Tuanjie Cowork+HMI by Jason Sun Unity Version Control·R193/R206/R208-R218 定谳线维持·windows-R219.txt 留档·probe 脚本 R218 复用改写）→双 blocked 维持·"
    "自进清单真锚核=R207-R218 判据全维持（A 池 A1-A5 全 done+B2/B4 素材生成线 P1 门后+JS 壳风险+B3 周一件不到+B5 账号期站内采样 blocked+C3 拣式已定档无新 FAIL 锚+C4 S1 v1.5 三连 10/10 无新旗锚+C1 集成腿无下批件在队=无可领真锚项·不凑工作量造活）；"
    "例行件=日报 2026-09-25+W39 周审在案不重跑（Test-Path True）·global-benchmarks 更新记录 2026-09-24 day1 ≤7 天跳过刷新（下期 ~10-01）·T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）；"
    "集团扫描=ledger 严格行含 @ 四模式 14 行=锚零新转办·decisions UTF8 非空行 24=锚零新行零动作；"
    "三探针全绿=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+2 发现=bs-005/bs-005e render-unannot blocked 在链预期红维持·F-005/F-007 登记即清·阻塞≠失败口径 exit 1/"
    "loop_health 0 FAIL 14 WARN 皆在案史实（tick218=done218 对账平·beats222 含 skip4·log 225 条·backlog 27 项 85% 燃尽）"
    "——一行收账即出（本轮不 commit·并窗轮 1/6·P-61 导出步照刷 export_ts " + stamp + "+实况派生轻量）。下轮=R220 快速路径首查（素材窗迹象优先/新令/集团转办），全静即 idle-fast（2/6）。"
)
st["log"].append(log_line)
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(st, ensure_ascii=False, indent=2) + "\n")

# ---- status-export.json ----
q = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\docs\status-export.json"
ex = json.load(io.open(q, encoding="utf-8"))
ex["export_ts"] = ts_iso
for d in ex["depts"]:
    if d["n"] == "工程技术部":
        d["t"] = ("OS 循环在飞（R219 idle-fast 并窗轮 1/6：五静+三探针绿·生产线双 blocked 维持待素材窗（15 窗枚举零 Biggame 总控窗）·自进池无可领真锚项；"
                  "R206 C1 学习腿+R205 A5 批处理交付在案·244 全回归绿）")
for row in ex["outs"]:
    if row[0] == "OS 循环":
        row[2] = ("tick 219·R219（idle-fast 快速路径·五静+三探针绿·素材窗 15 窗枚举零 Biggame 总控窗双 blocked 维持·自进池真锚项待新锚；并窗轮 1/6）")
for row in ex["results"]:
    if row[1] == "OS 轮次":
        row[0] = "219"
io.open(q, "w", encoding="utf-8", newline="\n").write(json.dumps(ex, ensure_ascii=False, indent=2) + "\n")

print("R219 close ok: tick=219, export_ts=%s, log_stamp=%s" % (ts_iso, decade))
