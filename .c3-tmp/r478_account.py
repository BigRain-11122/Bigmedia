# -*- coding: utf-8 -*-
"""R478 idle-fast accounting (fast path, window 4/6 -> no commit per os-protocol v1.9 batch law):
state.json log append + tick 477->478 + ts/task refresh; docs/status-export.json export_ts light refresh (P-61).
Binary-safe read/write, newline-style preserving, self-verifying via json.loads."""
import json, re, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
ST = ROOT + r"\src\os\state.json"
SE = ROOT + r"\docs\status-export.json"

now = time.strftime("%Y-%m-%d %H:%M:%S")

content = (
 "idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·并窗轮 4/6 不 commit）——"
 "①无新令（orders 双 NONE=r478_check·锚=O-20260925-1931-HQ-C mtime 19:47:21·O- 34 件零新增零编辑）；"
 "②无新集团转办（ledger 五模式 29=锚零新行·r478_check python 计数实证·内容寻址勿全文重读）+无新决策行（decisions UTF8 非空行 45=锚）；"
 "③树态=仅并窗自产预期态（M state.json+M status-export=自记账预期态不算 bm-a 迹象·.c3-tmp r475-r478 探针证据件随批收账）+storylines 三线 newest 皆 09-25 静=零 bm-a 写盘迹象·零 index.lock；"
 "④backlog 顶行不可认领（#59 REACT 09-27 窗已产 F-045·09-28 窗届日领/#70 OSS 下窗 09-29 21:40 后开/#67 DIGEST 候选池耗尽待 ledger 新 CEO 令级事件/#63+#66③ C-00030/31 供给门本轮加固=跨仓正典位直查 BigLife census/anchors〔止 C-00029·20 件〕锚仍 absent=supply-gated 照守〔r475-r477 仅 repo 内引用扫弱探针补强=R316 查锚纪律执行〕/#57 10-07/#31 ch.5 v3 稿 bm-a 未落/#72 知悉挂账零动作）+daily_0927 在案不重跑·W40 周审+月度统计注记=09-28 起·global-benchmarks 下期 ~10-01；"
 "⑤三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）0 发现/loop_health 2F+21W 皆在案定谳零新增（FAIL① 49min 停跳=09-26 20:24→21:13 R425 足迹已裁定不重复触发·FAIL② account-lag done478>tick477=+1 恒态足迹〔新断洞判据 lag ≥2 未破线〕·WARN 13 log-order+8 heartbeat-gap 全 ≤09-27 03:15 史实零新增）；"
 "一行收账即出（idle-fast 并窗轮 4/6〔窗 R475-R480 满 6 收账·跨日边界 09-28 00:00 先到即收〕·本轮不 commit·P-61 导出步照刷 export_ts 轻量）。"
 "下轮快速路径首查：#59 REACT 09-28 热点窗届日领（daily_brief 09-28 缺则先补产）/W40 周自审开周+月度统计注记/C-00030 锚/新令/集团转办——全静即 idle-fast（5/6）。"
)
entry = "%s R478: %s" % (now[:16], content)
task = content[:60]

raw = open(ST, "rb").read()
txt = raw.decode("utf-8")
st = json.loads(txt)
assert st["tick"] == 477, "tick anchor mismatch: %r" % st["tick"]
assert len(st["log"]) == 490, "log len mismatch: %r" % len(st["log"])

nl = "\r\n" if "\r\n" in txt else "\n"
idx = txt.rindex(nl + " ],")
head = txt[:idx]
tail = txt[idx:]

# ts + task refresh (tail segment only)
tail2 = re.sub(r'("ts": ")[^"]*(")', lambda m: m.group(1) + now + m.group(2), tail, count=1)
tail2 = re.sub(r'("task": ")[^"]*(")',
               lambda m: m.group(1) + json.dumps(task, ensure_ascii=False)[1:-1] + m.group(2),
               tail2, count=1)

new_ent = json.dumps(entry, ensure_ascii=False)
txt2 = head + "," + nl + "  " + new_ent + tail2
txt2 = txt2.replace('"tick": 477,', '"tick": 478,', 1)

st2 = json.loads(txt2)
assert st2["tick"] == 478, st2["tick"]
assert len(st2["log"]) == 491
assert st2["log"][-1] == entry
assert st2["ts"] == now
assert st2["task"] == task
open(ST, "wb").write(txt2.encode("utf-8"))

# P-61 light refresh: export_ts only (established idle-window method; depts/outs/results unchanged this round)
seraw = open(SE, "rb").read()
se = seraw.decode("utf-8")
iso = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
se2 = re.sub(r'("export_ts": ")[^"]*(")', lambda m: m.group(1) + iso + m.group(2), se, count=1)
json.loads(se2)
open(SE, "wb").write(se2.encode("utf-8"))

print("OK r478 account: tick=%d log=%d ts=%s" % (st2["tick"], len(st2["log"]), st2["ts"]))
print("task=%s" % st2["task"])
print("export_ts=%s" % iso)
print("no commit (idle-fast window 4/6, R475-R480)")
