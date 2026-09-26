# R350 idle-fast close: state.json (tick 349->350, log append, ts/task refresh)
# + P-61 export step (status-export.json export_ts/depts/outs/results derived refresh)
# Window 1/6 -> NO commit this round (os-protocol S6 batching rule).
# Pattern reuse: r349_close.py (R322 lesson: state.json multi-line edits via one-shot python).
import json, datetime, os

BS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = os.path.join(BS, "src", "os", "state.json")
EP = os.path.join(BS, "docs", "status-export.json")

now = datetime.datetime.now()
ts_full = now.strftime("%Y-%m-%d %H:%M:%S")
log_prefix = now.strftime("%Y-%m-%d %H:%M") + " R350: "

BODY = (
    "idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 1/6 不 commit）——"
    "①无新令（orders 顶=O-20260925-1931-HQ-C·R283 已记账）"
    "②backlog 顶行不可认领（#63 图鉴续件 C-00030 锚正典位轮首核=仍不在位〔python os.path.exists False+C-00031 同核 False 实证·anchors 20 止 C-00029 尾二=C-00028/C-00029〕supply-gated 维持·"
    "#59 REACT 当日映射余量耗尽 R314 判定同日维持〔新热点窗=09-27 日报〕·#57 替代率首报 10-07 窗挂账·#21 周日立法件 09-27 届日未到〔明日周日届日=下轮首查〕·"
    "自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕）"
    "③树净零锁（HEAD=180af8a R344-R349 batch 收账后净态·git status 空输出·无 index.lock python os.path.exists False 实证·"
    "本轮自产 M state.json+M status-export.json+?? .c3-tmp/r350_check.py=并窗自记账预期态非 bm-a 迹象〔r350_close.py 同随窗满批 commit〕）"
    "④ch.5 v3 稿未落（storylines python walk 扫描 novel/audio/comic 三子域 09-26 零新写盘实证=ch.5 判定口径成立·bm-a 面）·"
    "日报 2026-09-26 在案不重跑（os.path.exists True）·W39 周审在案；"
    "集团双锚静=ledger 行含 @ 四模式 21=锚零新转办（python 计数 21 实证）·decisions python 非空行 33=锚〔计数持平=R349 锚维持·尾行多 D 号行内嵌非新行〕零新行零动作；"
    "三探针全绿（board 0 FAIL 5 题 10 稿 5 in production exit 0/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1/loop_health 0 FAIL 19 WARN 皆在案史实〔12 log-order+7 heartbeat-gap〕·tick349=done349 对账平）；"
    "例行件=global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·"
    "tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）——"
    "一行收账即出（idle-fast 并窗轮 1/6·本轮不 commit·P-61 导出步照刷 export_ts）。"
    "下轮快速路径首查：#21 周日立法件（09-27 周日届日即领·周日周轮立法流程）/REACT 09-27 日报热点窗届日即领/图鉴 C-00030 锚/ch.5 v3 稿落迹象/新令/集团转办——全静即 idle-fast（6/6 窗满→batch commit R350-R355）。"
)
log_line = log_prefix + BODY

ENG_T = (
    "OS 循环 R350（idle-fast·五静+探针绿——产线全 supply-gated 维持：图鉴 C-00030 锚正典位仍不在位〔anchors 20 止 C-00029〕"
    "+REACT 当日映射余量耗尽〔R314 判定·新热点窗=09-27 日报〕+ch.5 v3 稿未落〔storylines 三子域 09-26 零新写盘 python 实证〕+#57 10-07 窗+#21 周日件届日未到〔09-27=明日〕"
    "·自进池 open 真锚项全闭=idle-fast 收账〔并窗 1/6·本轮不 commit〕）·state.ts/task 心跳面刷新"
)
OS_T = (
    "tick 350·R350（idle-fast·五静+探针绿——产线全 supply-gated 维持〔图鉴 C-00030 锚正典位轮首核仍不在位 anchors 20 止 C-00029·供给门只查 census/anchors/ 正典位"
    "+REACT 当日映射余量耗尽维持 R314 判定·新热点窗=09-27 日报+ch.5 v3 稿未落〔storylines novel/audio/comic 09-26 零新写盘 python 实证〕+#57 10-07 窗挂账+#21 周日件届日未到〕"
    "·自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕："
    "①五查静=无新令〔orders 顶=O-1931 R283 已记账〕+集团双锚静〔ledger 行含 @ 四模式 21=锚零新转办·decisions python 非空行 33=锚零新行〕"
    "+树净零锁〔HEAD=180af8a R344-R349 batch 收账后净态·无 index.lock〕"
    "②三探针全绿=board 0 FAIL 5 题 10 稿 5 in production/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 0 FAIL 19 WARN 皆在案史实·tick349=done349 对账平"
    "③并窗 1/6=不 commit（窗满 6 轮/跨日/异常/实活轮出现才收账）+P-61 导出步刷 export_ts）"
)

def load_raw(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()

def dump_keep(raw, obj, path):
    crlf = "\r\n" in raw
    out = json.dumps(obj, indent=1, ensure_ascii=False)
    if crlf:
        out = out.replace("\n", "\r\n")
    if raw.endswith("\r\n"):
        out += "\r\n"
    elif raw.endswith("\n"):
        out += "\n"
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(out)

# --- state.json ---
raw = load_raw(SP)
st = json.loads(raw)
assert st["tick"] == 349, "tick mismatch: %r" % st["tick"]
assert st["log"][-1].startswith("2026-09-26 07:33 R349"), "tail log is not R349"
st["tick"] = 350
st["log"].append(log_line)
st["ts"] = ts_full
st["task"] = BODY[:60]
dump_keep(raw, st, SP)
chk = json.loads(load_raw(SP))
assert chk["tick"] == 350 and chk["ts"] == ts_full and chk["task"] == BODY[:60]

# --- status-export.json (P-61) ---
eraw = load_raw(EP)
ex = json.loads(eraw)
ex["export_ts"] = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
eng_hit = os_hit = False
for d in ex["depts"]:
    if d["n"] == "工程技术部":
        d["t"] = ENG_T
        eng_hit = True
for row in ex["outs"]:
    if row[0] == "OS 循环":
        row[2] = OS_T
        os_hit = True
res_hit = False
for r in ex["results"]:
    if r[0] == "349":
        r[0] = "350"
        res_hit = True
assert eng_hit and os_hit and res_hit, "export targets missing (eng=%s os=%s res=%s)" % (eng_hit, os_hit, res_hit)
dump_keep(eraw, ex, EP)
echk = json.loads(load_raw(EP))
assert echk["export_ts"] == ex["export_ts"]

print("STATE-OK tick=%d ts=%s" % (chk["tick"], chk["ts"]))
print("TASK-OK len=%d" % len(chk["task"]))
print("EXPORT-OK ts=%s" % echk["export_ts"])
print("CLOSE-DONE idle-fast window-1of6 no-commit R350")
