# -*- coding: utf-8 -*-
"""R388 idle-fast close-out: state.json log line + tick/ts/task + status-export export_ts.
Window round 6/6 FULL (window R383-R388) -> this round does the batch commit per os-protocol S6."""
import json, io, os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "src", "os", "state.json")
EXPORT = os.path.join(ROOT, "docs", "status-export.json")

stamp = datetime.now()
log_ts = stamp.strftime("%Y-%m-%d %H:%M")
ts_full = stamp.strftime("%Y-%m-%d %H:%M:%S")
export_ts = stamp.strftime("%Y-%m-%dT%H:%M:%S") + "+08:00"

FOCUS = (
    u"R389: #21 周日立法件 09-27 届日即领（周日周轮立法流程）→"
    u"REACT 09-27 日报热点窗届日即领（轴位映射律+热点转述律 R309 双律复用·政治敏感面回避律照守）→"
    u"#63 图鉴 C-00030 锚轮首核（supply-gated 照守·锚落即领）→"
    u"#67 DIGEST 编年史候选（research §5 在册三件已耗尽=开闸 F-042/三线 F-043/技能动员 F-044 全制毕·"
    u"下件候选=新 CEO 令级事件落 ledger 即入池或 research §5 增补件·无候选不硬造=反膨胀律）——"
    u"新令/集团转办/探针红出现即优先；全静即 idle-fast（新窗 1/6）"
)

line = (
    log_ts + " R388: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗 6/6 满=本窗 batch commit R383-R388）——"
    u"①无新令（orders 顶=O-20260925-1931-HQ-C·R283 已记账）"
    u"②backlog 顶行不可认领（#67 DIGEST 编年史候选=research §5 在册三件已耗尽〔开闸 F-042/三线 F-043/"
    u"技能动员 F-044 全制毕〕+ledger 零新 CEO 令级事件=无候选不硬造〔反膨胀律〕·#63 图鉴 C-00030 锚正典位"
    u"轮首核=仍不在位〔r359_check.py anchor_C00030 False+C-00031 同核 False 双证·anchors 尾三=C-00027/"
    u"C-00028/C-00029 止 C-00029〕supply-gated 维持·#59 REACT 新热点窗=09-27 日报〔明日届日即领〕·"
    u"#21 周日立法件=09-27 届日〔明日周日届日即领〕·#57 替代率首报 10-07 窗挂账·#66③ 常态门控面·"
    u"自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·"
    u"C4 常态位 blocked on 进链件〕）"
    u"③树态=仅自产预期件（M state.json+M status-export.json=R383~R387 idle-fast 并窗自记账预期态·"
    u"?? .c3-tmp/r383_close.py+r385_close.py+r386_close.py+r387_close.py+r388_close.py 自产脚本件"
    u"随本窗满批 commit〔窗 R383-R388〕·无 index.lock r359_check.py False 实证·HEAD=d784e51 未变）"
    u"④ch.5 v3 稿未落（storylines python walk 扫描 novel/audio/comic 三子域 09-26 零新写盘实证"
    u"〔r359_check.py 读数 0/0/0〕=ch.5 判定口径成立·bm-a 面）·日报 2026-09-26 在案不重跑"
    u"（os.path.exists True·mtime 00:02 未变）·W39 周审在案；"
    u"集团双锚静=ledger @ 五模式 23=锚零新转办（r359_check.py python 计数 23 实证·尾=P-20260926-03 "
    u"R377 已收讫）·decisions python 非空行 40=锚〔尾=D-20260926-11 R377 已定谳〕零新行零动作；"
    u"三探针全绿（board 0 FAIL 5 题 10 稿 5 in production exit 0/readiness 3 阻塞皆外部 CEO 物理件+决策 "
    u"0 发现=阻塞≠失败口径 exit 1〔renders 42/42 注账〕/loop_health 0 FAIL 20 WARN 皆在案史实"
    u"〔12 log-order+8 heartbeat-gap 含 R382 已入账 beat gap 28min 12:53→13:21 长轮 WARN 级合法〕·"
    u"tick387=done387 对账平）；"
    u"例行件=global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 "
    u"open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律"
    u"如实记）·发布锁=M5 账号物理件不变（未上线=未测量）——"
    u"窗满 6 轮触发=batch commit R383-R388（os-protocol §6 并窗律·commit 注区间·窗重置 1/6）·"
    u"P-61 导出步照刷 export_ts。下轮快速路径首查：#21 周日立法件（09-27 周日届日即领·周日周轮立法流程）/"
    u"REACT 09-27 日报热点窗届日即领/图鉴 C-00030 锚/ch.5 v3 稿落迹象/新令/集团转办——全静即 idle-fast"
    u"（新窗 1/6）。"
)

with io.open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)

assert state["tick"] == 387, "tick drift: %s" % state["tick"]
assert line.startswith(log_ts + " R388:"), "log line stamp mismatch"
prev_ts = state["log"][-1].split(" R387:")[0]
assert prev_ts <= log_ts, "log order regression: %s -> %s" % (prev_ts, log_ts)

state["log"].append(line)
state["tick"] = 388
state["focus"] = FOCUS
state["ts"] = ts_full
state["task"] = line[len(log_ts) + 1:][:60]

with io.open(STATE, "w", encoding="utf-8", newline="\n") as f:
    json.dump(state, f, ensure_ascii=False, indent=1)

with io.open(EXPORT, "r", encoding="utf-8") as f:
    exp = json.load(f)
exp["export_ts"] = export_ts
with io.open(EXPORT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(exp, f, ensure_ascii=False, indent=1)

with io.open(STATE, "r", encoding="utf-8") as f:
    chk = json.load(f)
assert chk["tick"] == 388 and chk["ts"] == ts_full, "state re-check failed"
assert chk["log"][-1] == line, "log tail mismatch"
assert chk["focus"].startswith(u"R389:"), "focus refresh failed"
with io.open(EXPORT, "r", encoding="utf-8") as f:
    echk = json.load(f)
assert echk["export_ts"] == export_ts, "export re-check failed"
print("R388 close ok: tick=%s ts=%s export_ts=%s log_lines=%d" % (chk["tick"], chk["ts"], echk["export_ts"], len(chk["log"])))
print("task=%s" % chk["task"])
