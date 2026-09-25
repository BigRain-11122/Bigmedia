# -*- coding: utf-8 -*-
# R267 idle-fast accounting (data-only edit, json round-trip).
# state.json: tick 266->267, focus->R268, log append, ts/task refresh.
# status-export.json (P-61 step): export_ts + engineering dept / OS-loop
# out / results tick refreshed. Runtime-fresh timestamps.
import datetime
import io
import json

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = ROOT + r"\src\os\state.json"
EXPORT = ROOT + r"\docs\status-export.json"

now = datetime.datetime.now()
TS = now.strftime("%Y-%m-%d %H:%M:%S")
TS_EXPORT = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
LP = now.strftime("%Y-%m-%d %H:%M")

FOCUS = (
    "R268: 快速路径首查（新令/集团转办/素材窗〔Biggame 总控窗 R267 仍被 CEO 硅基仪表盘 F11 覆盖〔bm-c 告警 1117min 延续态〕·安全窗=覆盖层关闭后取帧核 D-BS-08 复活条款·面板扩容〕/ch.6 网文稿落盘迹象）→全静即 idle-fast（3/6）；可选项=O-1327 P2 图像类（梗图/贺图/壁纸）云通道 PoC=bm-a 会话协作面（MCP 通道会话独占·循环只备材料）；锚：ledger @15/decisions 29（总 32·D-BS 系新增=本仓 docs/decisions.md 非集团件）/orders 尾 O-20260925-1327-HQ-C；readiness 预期=3 blocker+0 finding（弃件清账新基线维持）；探针脚本复制律=Python UTF-8 通道（PS Get-Content 无 -Encoding 触编码律违例 R266 案）"
)

LOG = LP + (
    " R267: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 2/6）——①无新令（orders 顶=O-20260925-1327-HQ-C·R249 已记账）②backlog 顶行不可认领（#29 ①②③④+E4 全毕〔R250-R253〕·P2 图像类 PoC=bm-a 会话协作面〔MCP 通道会话独占〕不可领·ch.6 网文稿未落=novel 实证止 ch.5〔SC-001-05 09:10:33〕+comic 止 ep.2=零新落盘迹象·#15 随量产逐件·#17 needs-CEO·#21 周日件今周五不到）③树态=并窗自记账预期态（M state.json+M status-export.json）+自产 tmp 探针件未提交（批闭收账惯例维持）·无 index.lock（Test-Path 实证）·无 bm-a 活跃写盘迹象④素材窗迹象核=Biggame 总控窗开态延续但仍被 CEO 硅基仪表盘 F11 覆盖（r267_biggame_probe.py=r266 同型免 focus 取帧 rc=0〔Python UTF-8 通道复制律执行·R266 教训生效零操作红〕·会话验图定谳：覆盖层=硅基生命元宇宙仪表盘〔6 家公司/18 款游戏+bm-c 心跳 1117min 告警=R266 1107min+10min 延续态+里程碑 M1 在建+M1.5 萌发黄点+指令通道离线+等你拍板卡「视频号、公众号，开号」媒体公司行与在案口径一致·同屏他司 CEO 物理件卡三张=不涉本司零动作〕·帧内零 软著账本/12 条约束/玩法机制 新面板=D-BS-08 复活条款零触发·脱敏四项全无零敏感面）→留档观察待覆盖层关闭后安全窗复核；集团扫描=ledger 严格行含 @ 四模式 15 行=锚零新转办·decisions UTF8 非空行 29（总 32 双口径）=锚零新行零动作（r267_scan.py 实跑）；例行件=日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks 更新记录 2026-09-24 day2 ≤7 天跳过刷新（下期 ~10-01）·T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=0（探针纯脚本+会话内建验图零本地模型调用·P-54⑤ 计量律如实记）·自进清单真锚核=清单文件零变化（mtime 06:17=R206 自产写·判据维持=无可领真锚项不凑活）；三探针全绿=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+0 发现（弃件清账新基线维持·阻塞≠失败口径 exit 1）/loop_health 0 FAIL 17 WARN 皆在案史实（11 log-order+6 heartbeat-gap·tick266=done266 对账平=R266 预判命中·state-ts 门零红零滞后）——一行收账即出（本轮不 commit·并窗轮 2/6·P-61 导出步照刷 export_ts+实况派生轻量·收账后 loop_health 复跑预期 account-ahead 18th WARN=轮内在途瞬态〔R256/R257/R260 同型·beat 落地即平〕+JSON_OK 双件验）。下轮=R268 快速路径首查（新令/集团转办/素材窗〔覆盖层关闭后安全窗复核〕/ch.6 落盘迹象），全静即 idle-fast（3/6）。"
)

TASK = (
    "R267: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 2/6）——①无新令（orders 顶=O-20260925-1327-HQ-C·R249 已记账）②backlog 顶行不可认领（#29 ①②③④+E4 全毕·P2 图像类 PoC=bm-a 会话协作面不可领·ch.6 网文稿未落=novel 止 ch.5+comic 止 ep.2 零新落盘·#15 随量产逐件·#17 needs-CEO·#21 周日件今周五不到）③树态=并窗自记账预期态·无 index.lock·无 bm-a 活跃写盘迹象④素材窗迹象核=Biggame 总控窗延续被 CEO 硅基仪表盘 F11 覆盖（r267 免 focus 取帧+会话验图：bm-c 告警 1117min 延续态·零 软著账本/12 条约束/玩法机制 新面板=D-BS-08 复活条款零触发·零敏感面）；三探针全绿（board 0 FAIL·readiness 3 阻塞皆外部 CEO 面 0 发现·loop_health 0 FAIL·17 WARN 在案史实+tick266=done266 对账平）；集团双锚静（ledger @15/decisions 29〔总 32〕）；例行件全静（日报/W39 周审在案·benchmarks day2 ≤7 跳过·T1 无超线项·HQ-FEEDBACK 不写·tokens:local=0）；并窗 2/6 不 commit。"
)

ENG_T = (
    "OS 循环 R267（idle-fast：五静+探针绿·并窗 2/6·素材窗安全窗复核=Biggame 总控窗开态延续但仍被 CEO 硅基仪表盘 F11 覆盖〔bm-c 告警 1117min 延续态·里程碑 M1 在建+M1.5 萌发黄点〕·D-BS-08 复活条款零新面板触发=留档零扰动）·ledger @15/decisions 29 双锚稳·state.ts/task 心跳面刷新·探针复制律=Python UTF-8 通道执行零违例（R266 教训生效）"
)

OUT_OS = (
    "tick 267·R267（idle-fast：五静+探针绿·并窗 2/6——素材窗安全窗复核=Biggame 总控窗开态延续但仍被 CEO 硅基仪表盘 F11 全屏覆盖〔R252 事故窗禁触·bm-c 告警 1117min 延续态〕·D-BS-08 复活条款零新面板触发=留档零扰动待安全窗复核）"
)


def rewrite(path, obj, indent):
    raw = open(path, "rb").read()
    crlf = b"\r\n" in raw
    with io.open(path, "w", encoding="utf-8",
                 newline=("\r\n" if crlf else "\n")) as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
        f.write("\n")


with io.open(STATE, encoding="utf-8") as f:
    st = json.load(f)
assert st["tick"] == 266, "tick drift: %r" % (st["tick"],)
assert st["log"][-1].startswith("2026-09-25 16:35 R266"), "unexpected tail"
st["tick"] = 267
st["focus"] = FOCUS
st["log"].append(LOG)
st["ts"] = TS
st["task"] = TASK
rewrite(STATE, st, 1)

with io.open(EXPORT, encoding="utf-8") as f:
    se = json.load(f)
se["export_ts"] = TS_EXPORT
hit = 0
for d in se["depts"]:
    if d.get("n") == "工程技术部":
        d["t"] = ENG_T
        hit += 1
for o in se["outs"]:
    if o[0] == "OS 循环":
        o[2] = OUT_OS
        hit += 1
for r in se["results"]:
    if r[1] == "OS 轮次":
        r[0] = "267"
        hit += 1
assert hit == 3, "export patch hits=%d" % hit
rewrite(EXPORT, se, 2)

for p in (STATE, EXPORT):
    with io.open(p, encoding="utf-8") as f:
        json.load(f)
print("OK tick=267 ts=%s export_ts=%s log=%d" % (TS, TS_EXPORT, len(st["log"])))
