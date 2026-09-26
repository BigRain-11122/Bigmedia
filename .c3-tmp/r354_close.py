# -*- coding: utf-8 -*-
"""R354 idle-fast close: state.json log/tick/ts/task + status-export refresh.
Fast-path round (5/6 merge window, no commit). Abort on any anchor mismatch
without writing (R322 lesson). Single-shot script per state.json edit law."""
import io, json, re, subprocess, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = ROOT + r"\src\os\state.json"
EXPORT = ROOT + r"\docs\status-export.json"

# --- verify preconditions -------------------------------------------------
head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                      capture_output=True, text=True).stdout.strip()
assert head == "180af8a", "HEAD changed: " + head
import os
assert not os.path.exists(ROOT + r"\.git\index.lock")
assert not os.path.exists(r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md")
assert os.path.exists(ROOT + r"\data\intel\daily\2026-09-26.md")

stamp = time.strftime("%Y-%m-%d %H:%M:%S")
hm = time.strftime("%Y-%m-%d %H:%M")

line = (
    hm + " R354: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 5/6 不 commit）——"
    "①无新令（orders 顶=O-20260925-1931-HQ-C·R283 已记账）"
    "②backlog 顶行不可认领（#63 图鉴续件 C-00030 锚正典位轮首核=仍不在位〔Test-Path False 实证·anchors 止 C-00029〕supply-gated 维持·"
    "#59 REACT 当日映射余量耗尽 R314 判定同日维持〔新热点窗=09-27 日报〕·#57 替代率首报 10-07 窗挂账·"
    "#21 周日立法件届日=明日 09-27 未到·自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕）"
    "③树态=仅自产预期件（M state.json+M status-export.json=R350~R353 idle-fast 并窗自记账预期态·?? .c3-tmp/r350~r353 自产脚本件随窗满批 commit·"
    "无 index.lock Test-Path 实证·HEAD=180af8a 未变）"
    "④ch.5 v3 稿未落（storylines audio glob 实证最新写盘=sc001-04-v3-tmp 09-25 19:35·novel 止 SC-001-04-v3+SC-001-05-v1·"
    "git 树零新文件=零新写盘迹象·bm-a 面）·日报 2026-09-26 在案不重跑（Test-Path True）·W39 周审在案；"
    "集团双锚静=ledger 行含 @ 四模式 21=锚零新转办（rg 计数 21 实证）·decisions 非空行 33=锚〔尾=D-20260926-04〕零新行零动作；"
    "三探针全绿（board 0 FAIL 5 题 10 稿 5 in production exit 0/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1〔renders 42/42 注账〕/"
    "loop_health 0 FAIL 19 WARN 皆在案史实〔12 log-order+7 heartbeat-gap〕·tick353=done353 对账平）；"
    "例行件=global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·"
    "tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）——"
    "一行收账即出（idle-fast 并窗轮 5/6·本轮不 commit·P-61 导出步照刷 export_ts）。"
    "下轮快速路径首查：R355=并窗 6/6 窗满收账 commit（区间消息注明 R350-R355 idle-fast batch）+"
    "#21 周日立法件（09-27 周日届日即领·周日周轮立法流程）/REACT 09-27 日报热点窗届日即领/图鉴 C-00030 锚/ch.5 v3 稿落迹象/新令/集团转办——异常或实活轮出现即提前收账。"
)
assert '"' not in line and "\n" not in line and "\r" not in line
prefix = hm + " R354: "
assert line.startswith(prefix)
task = line[len(prefix):][:60]

# --- state.json ------------------------------------------------------------
with io.open(STATE, "r", encoding="utf-8", newline="") as f:
    text = f.read()
d = json.loads(text)
prev_len = len(d["log"])
assert d["tick"] == 353 and d["log"][-1].startswith("2026-09-26 08:13 R353:")

closes = re.findall(r"\r?\n \],", text)
assert len(closes) == 1, closes
nl = "\r\n" if closes[0].startswith("\r\n") else "\n"
entry = json.dumps(line, ensure_ascii=False)
new_text = text.replace(closes[0], "," + nl + " " + entry + nl + " ],", 1)
assert new_text.count('"tick": 353') == 1
new_text = new_text.replace('"tick": 353', '"tick": 354', 1)
new_text = re.sub(r'"ts": "[^"]*"', '"ts": ' + json.dumps(stamp), new_text, count=1)
new_text = re.sub(r'"task": "[^"]*"', '"task": ' + json.dumps(task, ensure_ascii=False), new_text, count=1)

d2 = json.loads(new_text)
assert d2["tick"] == 354 and d2["ts"] == stamp and d2["task"] == task
assert len(d2["log"]) == prev_len + 1 and d2["log"][-1] == line
with io.open(STATE, "w", encoding="utf-8", newline="") as f:
    f.write(new_text)

# --- status-export.json (P-61 export step, light derived refresh) -----------
with io.open(EXPORT, "r", encoding="utf-8", newline="") as f:
    et = f.read()
json.loads(et)

def rep(s, old, new, n=1):
    cnt = s.count(old)
    assert cnt == n, (old, cnt)
    return s.replace(old, new, n)

iso = time.strftime("%Y-%m-%dT%H:%M:%S") + "+08:00"
et = re.sub(r'"export_ts": "[^"]*"', '"export_ts": ' + json.dumps(iso), et, count=1)
et = rep(et, "OS 循环 R353（idle-fast", "OS 循环 R354（idle-fast")
et = rep(et, "〔并窗 4/6·本轮不 commit〕", "〔并窗 5/6·本轮不 commit〕")
et = rep(et, "tick 353·R353（idle-fast", "tick 354·R354（idle-fast")
et = rep(et, "③并窗 4/6=不 commit", "③并窗 5/6=不 commit")
et = rep(et, "tick352=done352 对账平", "tick353=done353 对账平")
et = rep(et, '"353",', '"354",', 1)
json.loads(et)
with io.open(EXPORT, "w", encoding="utf-8", newline="") as f:
    f.write(et)

print("R354 close OK: tick=354 log=%d ts=%s task_len=%d export_ts=%s head=%s"
      % (len(d2["log"]), stamp, len(task), iso, head))
