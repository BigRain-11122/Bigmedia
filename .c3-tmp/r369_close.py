# -*- coding: utf-8 -*-
"""R369 idle-fast close-out: state.json log line + tick/ts/task + status-export export_ts.
Window round 2/6 -> no commit this round (os-protocol S6 batch rule)."""
import json, io, os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "src", "os", "state.json")
EXPORT = os.path.join(ROOT, "docs", "status-export.json")

stamp = datetime.now()
log_ts = stamp.strftime("%Y-%m-%d %H:%M")        # log line leading stamp (single source)
ts_full = stamp.strftime("%Y-%m-%d %H:%M:%S")   # state.ts field (seconds-level ASCII)
export_ts = stamp.strftime("%Y-%m-%dT%H:%M:%S") + "+08:00"

line = (
    log_ts + " R369: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 2/6 不 commit）——"
    "①无新令（orders 顶=O-20260925-1931-HQ-C·R283 已记账）"
    "②backlog 顶行不可认领（#63 图鉴续件 C-00030 锚正典位轮首核=仍不在位〔r359_check.py 复用只读幂等："
    "python os.path.exists False+C-00031 同核 False 实证·anchors 尾三=C-00027/C-00028/C-00029 止 C-00029〕"
    "supply-gated 维持·#59 REACT 当日映射余量耗尽 R314 判定同日维持〔日报 mtime 09-26 00:02 未变=R313/R314 "
    "判据输入零变化·新热点窗=09-27 日报〕·#57 替代率首报 10-07 窗挂账·#21 周日立法件届日=明日 09-27 未到"
    "〔周日周轮立法流程·届日即领〕·自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+"
    "C 池 C1-C3 done·C4 常态位 blocked on 进链件〕）"
    "③树态=仅自产预期件（M state.json+M status-export.json=R368 idle-fast 并窗自记账预期态·"
    "?? .c3-tmp/r368_close.py+r368_taskfix.py 自产脚本件随窗满批 commit〔窗 R368-R373〕·"
    "无 index.lock python os.path.exists False 实证·HEAD=9e79ca0 未变）"
    "④ch.5 v3 稿未落（storylines python walk 扫描 novel/audio/comic 三子域 09-26 零新写盘实证"
    "〔r359_check.py 读数 0/0/0〕=ch.5 判定口径成立·bm-a 面）·日报 2026-09-26 在案不重跑"
    "（os.path.exists True·mtime 00:02 未变）·W39 周审在案；"
    "集团双锚静=ledger 行含 @ 四模式 21=锚零新转办（python 计数 21 实证）·decisions python 非空行 33=锚"
    "〔尾=D-20260926-04〕零新行零动作；"
    "三探针全绿（board 0 FAIL 5 题 10 稿 5 in production exit 0/readiness 3 阻塞皆外部 CEO 物理件+决策 "
    "0 发现=阻塞≠失败口径 exit 1〔renders 42/42 注账〕/loop_health 0 FAIL 19 WARN 皆在案史实"
    "〔12 log-order+7 heartbeat-gap〕·tick368=done368 对账平）；"
    "例行件=global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open "
    "问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·"
    "发布锁=M5 账号物理件不变（未上线=未测量）——"
    "一行收账即出（idle-fast 并窗轮 2/6〔窗 R368-R373 满 6 收账〕·本轮不 commit·P-61 导出步照刷 export_ts）。"
    "下轮快速路径首查：#21 周日立法件（09-27 周日届日即领·周日周轮立法流程）/REACT 09-27 日报热点窗届日即领/"
    "图鉴 C-00030 锚/ch.5 v3 稿落迹象/新令/集团转办——全静即 idle-fast（3/6）。"
)

with io.open(STATE, "r", encoding="utf-8") as f:
    state = json.load(f)

# sanity: log line must not start with a duplicated date (R351 lesson: single-source stamp)
assert line.startswith(log_ts + " R369:"), "log line stamp mismatch"
prev_ts = state["log"][-1].split(" R368:")[0]
assert prev_ts <= log_ts, "log order regression: %s -> %s" % (prev_ts, log_ts)

state["log"].append(line)
state["tick"] = 369
state["ts"] = ts_full
state["task"] = line[len(log_ts) + 1:][:60]  # strip leading stamp, first 60 chars

with io.open(STATE, "w", encoding="utf-8", newline="\n") as f:
    json.dump(state, f, ensure_ascii=False, indent=1)

with io.open(EXPORT, "r", encoding="utf-8") as f:
    exp = json.load(f)
exp["export_ts"] = export_ts
with io.open(EXPORT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(exp, f, ensure_ascii=False, indent=1)

# re-verify round-trip
with io.open(STATE, "r", encoding="utf-8") as f:
    chk = json.load(f)
assert chk["tick"] == 369 and chk["ts"] == ts_full, "state re-check failed"
assert chk["log"][-1] == line, "log tail mismatch"
with io.open(EXPORT, "r", encoding="utf-8") as f:
    echk = json.load(f)
assert echk["export_ts"] == export_ts, "export re-check failed"
print("R369 close ok: tick=%s ts=%s export_ts=%s log_lines=%d" % (chk["tick"], chk["ts"], echk["export_ts"], len(chk["log"])))
print("task=%s" % chk["task"])
