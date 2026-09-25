# -*- coding: utf-8 -*-
# R269 idle-fast close-out surgery: state.json (tick/log/ts/task/focus) +
# P-61 status-export refresh. Text surgery preserves one-line-per-log format.
import io
import json
import re
import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = ROOT + r"\src\os\state.json"
EP = ROOT + r"\docs\status-export.json"

now = datetime.datetime.now()
ts_full = now.strftime("%Y-%m-%d %H:%M:%S")
ts_min = now.strftime("%Y-%m-%d %H:%M")
ts_iso = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

line = (
    "2026-09-25 " + ts_min.split(" ")[1] + " R269: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 4/6）——"
    "①无新令（orders 顶=O-20260925-1327-HQ-C·R249 已记账）"
    "②backlog 顶行不可认领（#29 ①②③④+E4 全毕〔R250-R253〕·P2 图像类 PoC=bm-a 会话协作面〔MCP 通道会话独占〕不可领·"
    "ch.6 网文稿未落=novel 实证止 ch.5〔SC-001-05 09:10:33〕+comic 止 ep.2〔SC-002-02 09:09:35〕零新落盘·"
    "#15 随量产逐件·#17 needs-CEO·#21 周日件今周五不到）"
    "③树态=并窗自记账预期态（M state.json+M status-export.json）+自产 tmp 探针件未提交（批闭收账惯例维持）·"
    "无 index.lock（Test-Path 实证）·无 bm-a 活跃写盘迹象"
    "④素材窗迹象核=Biggame 总控窗开态延续但仍被 CEO 硅基仪表盘 F11 覆盖（r269_biggame_probe.py=r268 同型免 focus 取帧 rc=0"
    "〔Python UTF-8 通道复制律执行零违例〕·会话验图定谳：覆盖层=硅基生命元宇宙仪表盘延续态〔6 家公司/18 款游戏+"
    "bm-c 心跳 1137min 告警=R268 1127min+10min 延续态+里程碑轴 M0-M4 在帧+指令通道面板延续态+"
    "等你拍板卡「视频号、公众号，开号（媒体公司）」行与在案口径一致〔10 篇成稿/11 平台模板〕〕·"
    "帧内零 软著账本/12 条约束/玩法机制 新面板=D-BS-08 复活条款零触发·脱敏四项全无零敏感面）"
    "→留档观察待覆盖层关闭后安全窗复核；"
    "集团扫描=ledger 严格行含 @ 四模式 15 行=锚零新转办·decisions UTF8 非空行 29（总 32 双口径）=锚零新行零动作（python 扫描实证）；"
    "例行件=日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks 更新记录 2026-09-24 day2 ≤7 天跳过刷新（下期 ~10-01）·"
    "T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·"
    "tokens:local=0（探针纯脚本+会话内建验图零本地模型调用·P-54⑤ 计量律如实记）·"
    "自进清单真锚核=清单文件零变化（mtime 06:17=R206 自产写·判据维持=无可领真锚项不凑活）；"
    "三探针全绿=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+"
    "0 发现（弃件清账新基线维持·阻塞≠失败口径 exit 1）/loop_health 0 FAIL 17 WARN 皆在案史实（11 log-order+6 heartbeat-gap·"
    "tick268=done268 对账平·state-ts 门零红零滞后）；"
    "轮内操作注记=三探针输出件首跑经 PS `>` 管道重定向触 PS5.1 UTF-16 再编码乱码（探针自身读数无损·文件即重制）→"
    "python 内部 io.open 重定向重跑全绿=编码律 PS 管道面新案型（教训=探针输出件一律 python 内部重定向·已入 focus 行）；"
    "——一行收账即出（本轮不 commit·并窗轮 4/6·P-61 导出步照刷 export_ts+实况派生轻量·"
    "收账后 loop_health 复跑预期 account-ahead 20th WARN=轮内在途瞬态〔R256/R257/R260/R267/R268 同型·beat 落地即平〕+JSON_OK 双件验）。"
    "下轮=R270 快速路径首查（新令/集团转办/素材窗〔覆盖层关闭后安全窗复核〕/ch.6 落盘迹象），全静即 idle-fast（5/6）。"
)

new_focus = (
    "R270: 快速路径首查（新令/集团转办/素材窗〔Biggame 总控窗 R269 仍被 CEO 硅基仪表盘 F11 覆盖〔bm-c 告警 1137min 延续态〕·"
    "安全窗=覆盖层关闭后取帧核 D-BS-08 复活条款·面板扩容〕/ch.6 网文稿落盘迹象）→全静即 idle-fast（5/6）；"
    "可选项=O-1327 P2 图像类（梗图/贺图/壁纸）云通道 PoC=bm-a 会话协作面（MCP 通道会话独占·循环只备材料）；"
    "锚：ledger @15/decisions 29（总 32·D-BS 系新增=本仓 docs/decisions.md 非集团件）/orders 尾 O-20260925-1327-HQ-C；"
    "readiness 预期=3 blocker+0 finding（弃件清账新基线维持）；"
    "探针脚本复制律=Python UTF-8 通道（PS Get-Content 无 -Encoding 触编码律违例 R266 案）；"
    "探针输出重定向=python 内部 io.open（PS `>` 管道 PS5.1 触 UTF-16 乱码坑 R269 案）"
)

# ---- state.json text surgery ----
txt = io.open(SP, encoding="utf-8").read()
backup = txt

assert '"tick": 268,' in txt
txt = txt.replace('"tick": 268,', '"tick": 269,', 1)

idx = txt.rindex("\n ],")
q = txt.rindex('"', 0, idx)
txt = txt[:q] + '",\n "' + line + '"' + txt[idx:]

txt = re.sub(r'"ts": "[^"]*"', '"ts": "' + ts_full + '"', txt, count=1)
task60 = line.split(" ", 2)[2][:60] if False else line[len("2026-09-25 17:04 R269: ") - 13:][:60]
# task = log line minus "YYYY-MM-DD HH:MM " prefix, first 60 chars
prefix_len = len("2026-09-25 ") + len(ts_min.split(" ")[1]) + 1  # date + space + HH:MM + space
task60 = line[prefix_len:][:60]
txt = re.sub(r'"task": "[^"]*"', '"task": "' + task60 + '"', txt, count=1)

m = re.search(r'"focus": "[^"]*"', txt)
assert m
txt = txt.replace(m.group(0), '"focus": "' + new_focus + '"', 1)

json.loads(txt)  # validate
io.open(SP, "w", encoding="utf-8", newline="\n").write(txt)
json.loads(io.open(SP, encoding="utf-8").read())
print("state.json OK tick=269 ts=" + ts_full)
print("task=" + task60)

# ---- status-export P-61 refresh ----
se = json.load(io.open(EP, encoding="utf-8"))
se["export_ts"] = ts_iso
for d in se["depts"]:
    if d["n"] == "工程技术部":
        d["t"] = (
            "OS 循环 R269（idle-fast：五静+探针绿·并窗 4/6·素材窗安全窗复核=Biggame 总控窗开态延续但仍被 CEO 硅基仪表盘 F11 覆盖"
            "〔bm-c 告警 1137min 延续态〕·D-BS-08 复活条款零新面板触发=留档零扰动）·ledger @15/decisions 29 双锚稳·"
            "state.ts/task 心跳面刷新·探针复制律=Python UTF-8 通道执行零违例（R266 教训生效）+"
            "探针输出重定向=python 内部 io.open（R269 PS > 管道乱码案）"
        )
for o in se["outs"]:
    if o[0] == "OS 循环":
        o[2] = (
            "tick 269·R269（idle-fast：五静+探针绿·并窗 4/6——素材窗安全窗复核=Biggame 总控窗开态延续但仍被 CEO 硅基仪表盘 F11 全屏覆盖"
            "〔R252 事故窗禁触·bm-c 告警 1137min 延续态〕·D-BS-08 复活条款零新面板触发=留档零扰动待安全窗复核）"
        )
for r in se["results"]:
    if r[1] == "OS 轮次":
        r[0] = "269"
json.dump(se, io.open(EP, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
json.load(io.open(EP, encoding="utf-8"))
print("status-export.json OK export_ts=" + ts_iso)
