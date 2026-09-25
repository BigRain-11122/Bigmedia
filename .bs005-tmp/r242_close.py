# R242 close: idle-fast round. tick+1, R242 log, focus R243,
# state.ts/task heartbeat face refresh (PT-20260925-02 law),
# status-export light refresh (P-61 step).
import io, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = ROOT + r"\src\os\state.json"
EP = ROOT + r"\docs\status-export.json"

now_dt = datetime.datetime.now()
stamp_min = now_dt.strftime("%Y-%m-%d %H:%M")
ts_full = now_dt.strftime("%Y-%m-%d %H:%M:%S")

st = json.load(io.open(SP, encoding="utf-8"))

# 1) tick +1
st["tick"] = st.get("tick", 241) + 1

# 2) R242 log entry (idle-fast one-liner)
r242 = (
    "2026-09-25 12:2x R242: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 1/6）——"
    "①无新令（orders 顶=O-20260925-1153-BG-C·R241 已记账）"
    "②backlog 顶行不可认领（#28 done〔PT-02 整改 R241 毕〕·#27 ①②③ 全毕·④发布锁内挂账·ch.6 网文稿未落=bm-a 面〔novel 实证止 ch.5〕"
    "·BS-005/bs005e 双 blocked 待素材窗·#15 随量产逐件·#17 needs-CEO·#21 周日件今周五不到）"
    "③树态=仅自产 blocked 批中间件未提交（.bs005-tmp/.bs005e-tmp 批闭收账惯例维持）·无 index.lock·无 bm-a 活跃写盘迹象"
    "（novel 止 ch.5/comic 止 ep.2 零新进展）"
    "④素材窗迹象核=窗口枚举 39 窗零 Biggame 总控窗（Tuanjie 态=Cowork/Game/DemoScene/HMI Version Control+豆包/Lovart/硅基生命元宇宙 Edge"
    "·R193-R241 定谳线维持·r242-scan.txt 留档）→双 blocked 维持；"
    "集团扫描=ledger 严格行含 @ 四模式 15 行=锚零新转办·decisions UTF8 非空行 29（总行 32 双口径）=锚零新行零动作；"
    "三探针全绿=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）"
    "+2 发现（bs-005/bs005e render-unannot=blocked 在链预期红维持·F-005/F-007 登记即清·阻塞≠失败口径 exit 1）"
    "/loop_health 0 FAIL 17 WARN 皆在案史实（11 log-order+6 heartbeat-gap 与 R234-R241 同集零新增·tick241=done241 对账平·log 249 条"
    "·backlog 29 项 24 done 83% 燃尽·state-ts 门执法首验过=ts/task 字段在位零红零滞后 WARN）；"
    "例行件=日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks 更新记录 2026-09-24 day1 ≤7 天跳过刷新（下期 ~10-01）"
    "·T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）"
    "·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）——"
    "一行收账即出（本轮不 commit·并窗轮 1/6·P-61 导出步照刷 export_ts+实况派生轻量）。"
    "下轮=R243 快速路径首查（素材窗迹象优先/新令/集团转办），全静即 idle-fast（2/6）。"
)
st["log"].append(r242)

# 3) heartbeat face: ts + task (PT-20260925-02 law, refreshed every closing)
st["ts"] = ts_full
head = r242.split(" ", 2)  # ["2026-09-25", "12:2x", "R242: ..."]
task_text = (head[2] if len(head) > 2 else r242)[:60]
st["task"] = task_text

# 4) focus for R243
st["focus"] = (
    "R243: 快速路径判定轮（锚：ledger @行 15·decisions 非空行锚 29〔UTF8 口径·总行 32 双口径〕·"
    "orders 尾 O-20260925-1153-BG-C·树态自账预期态〔M state/export+tmp 工件〕·state.ts/task 心跳面 R241 落律后逐轮刷新执法）"
    "→五静+探针绿=idle-fast 2/6；素材窗=窗口枚举零 Biggame 总控窗定谳线 R193-R242·BS-005/bs005e 双 blocked（bs005e=F-007 预点位）；"
    "#27 音频线=ch.6 网文稿未落（bm-a 面·cta 周浩宇/陈雅雯双钩已埋）·已产 F-008~F-012 五件；"
    "readiness 预期=3 blocker+2 finding 同集；承诺：窗满 6 轮/跨日/异常/实活即收账"
)

io.open(SP, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=1))

# 5) status-export light refresh (P-61 step, idle round)
ex = json.load(io.open(EP, encoding="utf-8"))
ex["export_ts"] = now_dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")
for d in ex["depts"]:
    if d["n"] == "工程技术部":
        d["t"] = ("OS 循环 R242（idle-fast 快速路径·五静+探针绿：PT-02 整改后首轮 idle——state.ts/task 心跳面在位"
                  "·loop_health state-ts 门执法首验零红·ledger 15 行/decisions 29 双锚零新转办·素材窗零 Biggame 总控窗"
                  "双 blocked 维持·并窗轮 1/6 不 commit）")
for o in ex["outs"]:
    if o[0] == "OS 循环":
        o[2] = ("tick 242·R242（idle-fast：五静〔orders 顶 O-1153·backlog 顶 #28 done·树净零锁·bm-a 零新写盘〕"
                "+探针绿〔board 0 fail/readiness 3+2 同集预期/loop 0 fail 17 warn 历史·state-ts 首验过〕"
                "·素材窗零 Biggame 总控窗·ch.6 未落/ep.3 未现零新进展）")
for r in ex["results"]:
    if r[1] == "OS 轮次":
        r[0] = "242"
io.open(EP, "w", encoding="utf-8").write(json.dumps(ex, ensure_ascii=False, indent=2))
print("ok tick=%d ts=%s task=%s export_ts=%s" % (st["tick"], st["ts"], st["task"], ex["export_ts"]))
