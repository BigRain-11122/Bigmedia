# R238: repair R237 doubled timestamp prefix in state.json log, tick+1, append R238 log, update focus; refresh status-export
import io, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = ROOT + r"\src\os\state.json"
EP = ROOT + r"\docs\status-export.json"

st = json.load(io.open(SP, encoding="utf-8"))

# 1. repair: log entry 245 (R237) leading "2026-09-25 2026-09-25 11:33" -> single prefix
BAD = "2026-09-25 2026-09-25 11:33 R237:"
GOOD = "2026-09-25 11:33 R237:"
fixed = 0
for i, e in enumerate(st["log"]):
    if isinstance(e, str) and e.startswith(BAD):
        st["log"][i] = GOOD + e[len(BAD):]
        fixed += 1
assert fixed == 1, "expected exactly 1 repair, got %d" % fixed

# 2. tick +1
st["tick"] = st.get("tick", 237) + 1

# 3. append R238 log entry
r238 = (
    "2026-09-25 11:4x R238: 修红轮·R237 自记账缺陷闭环（异常触发全任务书窄面处理·R235 先例）——"
    "①轮首快速路径五查静（orders 顶=O-0850 R222 已记账/ledger 严格行含 @ 四模式 14 行=锚零新转办/"
    "decisions UTF8 非空行 24〔总行 27 双口径〕=锚零新行/index.lock 无/树态=并窗自记账预期态+自产 tmp/"
    "storylines 实证 novel 止 ch.5·comic 止 ep.2=零新进展）+board 0 FAIL+readiness 3 阻塞皆外部+2 发现同集预期"
    "（bs-005/bs005e render-unannot=R193/R204 blocked 在链预期红）→三探针唯一红="
    "**loop_health 1 FAIL（log-ts：R237 行首时间戳前缀重复「2026-09-25 2026-09-25 11:33」=R237 收账脚本缺陷）**"
    "——异常即转全任务书（不进 idle-fast）；"
    "②修红=state.json log entry 245 机械去重前缀（双前缀→单前缀·行内容零改写=格式修复非历史改写）"
    "→复跑 loop_health=0 FAIL 17 WARN 皆在案史实（11 log-order+6 heartbeat-gap·tick237=done237 对账平）；"
    "③例行件全静：日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks day1 ≤7 跳过（下期 ~10-01）"
    "·T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）"
    "·素材窗核=窗口枚举零 Biggame 总控窗（windows-R238.txt 留档）→BS-005/bs005e 双 blocked 维持"
    "·②③ bm-a 复核=盘上实证零新进展（ch.6 未落/ep.3 未现）·自进清单真锚核=R207-R237 判据全维持无可领真锚项"
    "·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）；"
    "④收账=异常轮即收（idle-fast 并窗中断于 2/6）：R236-R238 一并 commit+push（区间注记）"
    "·P-61 导出步照刷 export_ts+实况派生轻量。下轮=R239 快速路径首查（素材窗迹象优先/新令/集团转办），全静即 idle-fast 1/6。"
)
st["log"].append(r238)

# 4. update focus for R239
st["focus"] = (
    "R239: 快速路径判定轮（锚：ledger @行 14·decisions 非空行锚 24〔UTF8 口径·总行 27 双口径注记〕·"
    "orders 尾 O-20260925-0850·树态自账预期态〔M state/export+tmp 工件〕·bm-a 写盘迹象〔novel ch.6/comic ep.3〕）"
    "→五静+探针绿=idle-fast 1/6；素材窗=BS-005 原件已出窗·bs005e=F-007 预点位维持·窗口枚举零 Biggame 总控窗定谳线 R193-R238；"
    "#27 音频线=ch.6 网文稿未落（bm-a 面·cta 周浩宇/陈雅雯双钩已埋）·已产 F-008~F-012 五件；"
    "readiness 预期=3 blocker+2 finding 同集；承诺：窗满 6 轮/跨日/异常/实活即收账"
)

io.open(SP, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=1))

# 5. status-export: refresh export_ts + engineering dept + OS loop out + results tick
ex = json.load(io.open(EP, encoding="utf-8"))
now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
ex["export_ts"] = now
for d in ex["depts"]:
    if d["n"] == "工程技术部":
        d["t"] = ("OS 循环 R238（修红轮：loop_health log-ts FAIL=R237 行首时间戳双前缀收账脚本缺陷"
                  "→机械去重修复+复跑 0 FAIL 17 WARN 全历史·R236-R238 并窗随异常轮一并收账）")
for o in ex["outs"]:
    if o[0] == "OS 循环":
        o[2] = ("tick 238·R238（修红轮：五查静+board 0 fail/readiness 3+2 同集/loop 1 FAIL→修复后 0 FAIL 17 warn 全历史"
                "·decisions 24 非空行锚稳〔总 27 双口径〕·bm-a 零新写盘〔ch.6 未落/ep.3 未现〕·素材窗零 Biggame 总控窗）")
for r in ex["results"]:
    if r[1] == "OS 轮次":
        r[0] = "238"
io.open(EP, "w", encoding="utf-8").write(json.dumps(ex, ensure_ascii=False, indent=2))
print("ok tick=%d export_ts=%s" % (st["tick"], now))
