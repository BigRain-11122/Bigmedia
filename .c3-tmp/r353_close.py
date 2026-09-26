# R353 idle-fast close: state.json (tick/log/ts/task) + status-export.json (P-61)
# single-shot python per R322 lesson; date-stamp single-source per R351 lesson (no double-date)
import json, os
from datetime import datetime

R = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(R, ".."))
SP = os.path.join(ROOT, "src", "os", "state.json")
XP = os.path.join(ROOT, "docs", "status-export.json")

now = datetime.now()
stamp = now.strftime("%Y-%m-%d %H:%M")
ts_full = now.strftime("%Y-%m-%d %H:%M:%S")

prefix = "%s R353: " % stamp
body = (
    "idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 4/6 不 commit）——"
    "①无新令（orders 顶=O-20260925-1931-HQ-C·R283 已记账）"
    "②backlog 顶行不可认领（#63 图鉴续件 C-00030 锚正典位轮首核=仍不在位〔python os.path.exists False+C-00031 同核 False 实证·anchors 20 止 C-00029 尾二=C-00028/C-00029〕supply-gated 维持·"
    "#59 REACT 当日映射余量耗尽 R314 判定维持〔日报 mtime 09-26 00:02 未变=R313/R314 判据输入零变化·新热点窗=09-27 日报〕·#57 替代率首报 10-07 窗挂账·#21 周日立法件届日=明日 09-27 未到·"
    "自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕）"
    "③树态=仅自产预期件（M state.json+M status-export.json=R350~R352 idle-fast 并窗自记账预期态·?? .c3-tmp/r350~r353 自产脚本件随窗满批 commit·无 index.lock os.path.exists False 实证·HEAD=180af8a 未变）"
    "④ch.5 v3 稿未落（storylines python walk 扫描 novel/audio/comic 三子域 09-26 零新写盘实证=ch.5 判定口径成立·bm-a 面）·日报 2026-09-26 在案不重跑（os.path.exists True·mtime 00:02）·W39 周审在案；"
    "集团双锚静=ledger 行含 @ 四模式 21=锚零新转办（python 计数 21 实证）·decisions python 非空行 33=锚零新行〔naive 尾 ID 误报 D-20260925-06=尾行行内嵌旧号引用口径 R352 同型·行数 33=锚实证〕；"
    "三探针全绿（board 0 FAIL 5 题 10 稿 5 in production exit 0/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1〔renders 42/42 注账〕/loop_health 0 FAIL 19 WARN 皆在案史实〔12 log-order+7 heartbeat-gap〕·tick352=done352 对账平）；"
    "例行件=global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）——"
    "一行收账即出（idle-fast 并窗轮 4/6·本轮不 commit·P-61 导出步照刷 export_ts）。"
    "下轮快速路径首查：#21 周日立法件（09-27 周日届日即领·周日周轮立法流程）/REACT 09-27 日报热点窗届日即领/图鉴 C-00030 锚/ch.5 v3 稿落迹象/新令/集团转办——全静即 idle-fast（6/6 窗满→batch commit R350-R355）。"
)
log_line = prefix + body

# --- state.json ---
with open(SP, encoding="utf-8") as f:
    st = json.load(f)
assert st["tick"] == 352, "tick anchor mismatch: %s" % st["tick"]
assert "R352" in st["log"][-1], "last log anchor mismatch"
st["tick"] = 353
st["log"].append(log_line)
st["ts"] = ts_full
st["task"] = body[:60]
tmp = SP + ".tmp"
with open(tmp, "w", encoding="utf-8", newline="\n") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
with open(tmp, encoding="utf-8") as f:
    json.load(f)
os.replace(tmp, SP)

# --- status-export.json (P-61) ---
with open(XP, encoding="utf-8") as f:
    ex = json.load(f)
assert ex["export_ts"].startswith("2026-09-26T08:03"), "export_ts anchor mismatch: %s" % ex["export_ts"]
ex["export_ts"] = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
eng_t = (
    "OS 循环 R353（idle-fast·五静+探针绿——产线全 supply-gated 维持：图鉴 C-00030 锚正典位仍不在位〔anchors 20 止 C-00029〕"
    "+REACT 当日映射余量耗尽〔R314 判定·日报 mtime 未变·新热点窗=09-27 日报〕+ch.5 v3 稿未落〔storylines 三子域 09-26 零新写盘 python 实证〕"
    "+#57 10-07 窗+#21 周日件届日明日 09-27·自进池 open 真锚项全闭=idle-fast 收账〔并窗 4/6·本轮不 commit〕）·state.ts/task 心跳面刷新"
)
found = False
for d in ex["depts"]:
    if d["n"] == "工程技术部":
        d["t"] = eng_t
        found = True
        break
assert found, "dept eng not found"
os_out = (
    "tick 353·R353（idle-fast·五静+探针绿——产线全 supply-gated 维持〔图鉴 C-00030 锚正典位轮首核仍不在位 anchors 20 止 C-00029·供给门只查 census/anchors/ 正典位"
    "+REACT 当日映射余量耗尽维持 R314 判定〔日报 mtime 未变〕·新热点窗=09-27 日报+ch.5 v3 稿未落〔storylines novel/audio/comic 09-26 零新写盘 python 实证〕"
    "+#57 10-07 窗挂账+#21 周日件届日明日 09-27〕·自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕："
    "①五查静=无新令〔orders 顶=O-1931 R283 已记账〕+集团双锚静〔ledger 行含 @ 四模式 21=锚零新转办·decisions python 非空行 33=锚零新行〔naive 尾 ID=行内嵌旧号口径·行数 33=锚实证〕〕"
    "+树静零锁〔HEAD=180af8a R344-R349 batch 后未变·仅自产预期件 M state.json+M status-export.json+?? .c3-tmp 自产脚本〕"
    "②三探针全绿=board 0 FAIL 5 题 10 稿 5 in production/readiness 3 阻塞皆外部 CEO 面 0 发现〔renders 42/42 注账〕/loop_health 0 FAIL 19 WARN 皆在案史实·tick352=done352 对账平"
    "③并窗 4/6=不 commit（窗满 6 轮/跨日/异常/实活轮出现才收账·窗满点=R355）+P-61 导出步刷 export_ts）"
)
assert ex["outs"][0][0] == "OS 循环", "outs[0] anchor mismatch"
ex["outs"][0][2] = os_out
assert ex["results"][0][1] == "OS 轮次", "results[0] anchor mismatch"
ex["results"][0][0] = "353"
tmp = XP + ".tmp"
with open(tmp, "w", encoding="utf-8", newline="\n") as f:
    json.dump(ex, f, ensure_ascii=False, indent=1)
with open(tmp, encoding="utf-8") as f:
    json.load(f)
os.replace(tmp, XP)

# --- re-validate both files ---
for pth in (SP, XP):
    with open(pth, encoding="utf-8") as f:
        json.load(f)
print("OK tick=353 ts=%s task_len=%d export_ts=%s" % (ts_full, len(body[:60]), ex["export_ts"]))
