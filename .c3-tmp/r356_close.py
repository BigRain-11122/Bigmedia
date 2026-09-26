# -*- coding: utf-8 -*-
# R356 idle-fast close: tick+1, log append, ts/task refresh, export_ts refresh (no commit, window 1/6)
import json, time, io

STAMP = time.strftime("%Y-%m-%d %H:%M")
TS = time.strftime("%Y-%m-%d %H:%M:%S")

body = (
    "idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 1/6 不 commit）——"
    "①无新令（orders 顶=O-20260925-1931-HQ-C·R283 已记账）"
    "②backlog 顶行不可认领（#63 图鉴续件 C-00030 锚正典位轮首核=仍不在位〔BigLife census/anchors 20 件尾二=C-00028/C-00029 python 实证·C-00031 同核不在位〕supply-gated 维持·#59 REACT 当日映射余量耗尽 R314 判定同日维持〔新热点窗=09-27 日报〕·#57 替代率首报 10-07 窗挂账·#21 周日立法件届日=明日 09-27 未到〔明日周日届日=下轮首查〕·自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕）"
    "③树净零锁（HEAD=5a9ee5c R350-R355 batch 收账后净态·git status 空输出·无 index.lock python os.path.exists False 实证·本轮自产 M state.json+M status-export.json+?? .c3-tmp/r356_check.py=并窗自记账预期态非 bm-a 迹象〔r356_close.py 同随窗满批 commit〕）"
    "④ch.5 v3 稿未落（storylines python walk 扫描 novel/audio/comic 三子域 09-26 零新写盘实证=ch.5 判定口径成立·bm-a 面）·日报 2026-09-26 在案不重跑（os.path.exists True 实证）·W39 周审在案；"
    "集团双锚静=ledger 行含 @ 四模式 21=锚零新转办（python 计数 21 实证）·decisions python 非空行 33=锚零新行〔naive 尾 ID 误报 D-20260925-06=尾行行内嵌旧号引用口径 R352/R353 同型·行数 33=锚实证〕；"
    "三探针全绿（board 0 FAIL 5 题 10 稿 5 in production exit 0/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1〔renders 42/42 注账〕/loop_health 0 FAIL 19 WARN 皆在案史实〔12 log-order+7 heartbeat-gap〕·tick355=done355 对账平）；"
    "例行件=global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）——"
    "一行收账即出（idle-fast 并窗轮 1/6·本轮不 commit·P-61 导出步照刷 export_ts）。"
    "下轮快速路径首查：#21 周日立法件（09-27 周日届日即领·周日周轮立法流程）/REACT 09-27 日报热点窗届日即领/图鉴 C-00030 锚/ch.5 v3 稿落迹象/新令/集团转办——全静即 idle-fast（6/6 窗满→batch commit R356-R361）。"
)

entry = "%s R356: %s" % (STAMP, body)

with io.open(r"src\os\state.json", encoding="utf-8") as f:
    st = json.load(f)
assert st["tick"] == 355, "tick anchor mismatch: %r" % (st["tick"],)
st["tick"] = 356
st["log"].append(entry)
st["ts"] = TS
st["task"] = body[:60]
with io.open(r"src\os\state.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
    f.write("\n")

with io.open(r"docs\status-export.json", encoding="utf-8") as f:
    ex = json.load(f)
ex["export_ts"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
with io.open(r"docs\status-export.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(ex, f, ensure_ascii=False, indent=1)
    f.write("\n")

# post-write verification: reload both files, confirm json validity + fields
with io.open(r"src\os\state.json", encoding="utf-8") as f:
    st2 = json.load(f)
with io.open(r"docs\status-export.json", encoding="utf-8") as f:
    ex2 = json.load(f)
assert st2["tick"] == 356 and st2["log"][-1].startswith(STAMP + " R356:") and st2["ts"] == TS and st2["task"] == body[:60]
assert ex2["export_ts"] == time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
print("R356 close ok: tick=%d ts=%s export_ts=%s log_entries=%d task_len=%d" % (st2["tick"], st2["ts"], ex2["export_ts"], len(st2["log"]), len(st2["task"])))
