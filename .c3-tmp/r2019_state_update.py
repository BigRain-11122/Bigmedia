# -*- coding: utf-8 -*-
# R2019 round accounting: tick+1, log append, ts/task refresh (PT-20260925-02)
# Format-preserving text surgery; full JSON parse validation before write.
# Also appends queue restock seed tech#121 to state/queue/tech.md.
import json, re
from datetime import datetime

PATH = r"src\os\state.json"
QPATH = r"state\queue\tech.md"

raw = open(PATH, "rb").read()
had_bom = raw.startswith(b"\xef\xbb\xbf")
text = raw.decode("utf-8-sig")
nl = "\r\n" if "\r\n" in text else "\n"

now = datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")
masked = now.strftime("%Y-%m-%d %H:") + str(now.minute // 10) + "x"

CONTENT = (u"生产轮·fire 窗消费序实弹=F-180 flight-3 fire_consume 原子派发→内读卡 no-fire rc1"
u"（预读 GO 04:14:04〔B-eviction-credit·gate go=True free_min 4979/util 44/band 7·fire-valid 120s〕"
u"→派发内读 04:15:23 no-fire〔gate-credit-no-go+util-face worst-case 97>80 单翻转〕"
u"=「GO 后零中步立即发」律第三复发案〔R1995 首案/R1999 二案→tech#112 原子消费器已根治卡读-发射间 agent 延迟"
u"·残余面=agent 预读 GO 后的验证中步〔--help+Select-String 两命令 79s〕·fire_consume fail-closed 拦截正确=工具面无恙〕"
u"·fire-consume-ledger no-fire 行落盘）→F-180 SC-005-07 flight-3 维持 fire-ready 绷结"
u"（发射器 wedge-probe 接参+材料+e4-material/asr_diff/same_text 全在位=下个真窗单命令派发）；"
u"轮首五查全静（own orders O-20260908-1105==R1733 锚+origin_gap_check QUIET ahead0 behind0〔R1500 前置位〕"
u"+group_scan 四面全静〔decisions truly_new=0 水位 150 维持+ledger @BigStream 5 行=值守锚"
u"·@六司 1 行 Select-String 实查=P-2026-10-09-01 命令下发机制令=C-20261009-04 已过会旧锚零新转办"
u"+ORDERS 行水位 quiet rows=270=='10-11 13:4x'==R1979 基线 tech#103 连窗过〕+无 index.lock"
u"+树=mv001/mv0001 MV sprint 会话域在飞件零接触维持 R1745）；"
u"三探针=probe_capture 证据件 .c3-tmp/r2019_probes.txt（board 0 FAIL 5 题 10 纯 5 in production"
u"/readiness 3 阻塞的皆外部 CEO 面+M4 GATE 6/10+#17 needs-CEO/发现 18 renders unannot=0"
u"/loop_health 2F+263W 皆在案史实带内〔两 outage=09-26/09-28 已裁定不重触发·drift 18≤adjudicated 基线 21 带内〕）；"
u"meme V1 成片查看位双路径回归 *.mp4 零新到件（R1899 锚维持·装配腿 bm-a 会话域在飞零接触）；"
u"三队盘点=main 全 gated/查看位（#19 flight-3 gated fire 窗·#20 REACT-v15 评审膝 gated fire 窗·#7 krea2 禁重扫·#9 编年史下窗）"
u"+tech 全 done/gated/观察位（#92 权威窗 08:00 届日未到不预扫·#115/#116 观察位·#118 gated v20）"
u"+explore 全 done/gated/到期未至（#14/#22 ≥10-17·#18 10-16·#26 10-13/15·#27 gated）→fire 项外真无可执行项=等待窗维持；"
u"队列补货步=tech#121 真种子（fire 窗项消费序律：轮首命令=fire_consume 直发·预读卡=信息件非门"
u"·判据=下真窗单命令直发零中步窗捕获率对照）；"
u"例行件=10-12 日报在案不重跑（R2008 一份为真相）+W42 周审第 4 期在案（R2008）+GB §④ 下期 10-15；"
u"export_ts R2017 03:07 <24h 零 CEO 可见成品态变化节流不刷（R1997/R2004 内部工具件先例）；"
u"HQ-FEEDBACK 不写（零集团层新 open 问题）；tokens:local=0（纯探针只读+fire 卡读=档架读写零本地模型调用 P-54 计量纪律）；"
u"临时件清理钩=r2019_probes.txt 证据件随本 commit 收口（tech#81 自含律）；"
u"——下轮 R2020 快速路径首查（fire 窗项轮首命令=fire_consume 直发 sc005-07 s1_call〔tech#121 判据·零预读零中步〕"
u"→GO=判词≥9=TTS light 续链 F-180 登记；no-fire=等待窗取活；"
u"tech#92 权威窗 08:00 届日即领〔zhihu-hot 头部 ≥3 件 ≥60=文本脏吸收为 FAIL=阈值分层腿速补〕"
u"+F-181 评审膝后段位+meme V1 成片查看位）。收账显式列文件 commit+push")

LINE = masked + u" R2019: " + CONTENT
TASK = CONTENT[:60]

# 1) tick
assert text.count('"tick": 2018,') == 1, "tick anchor not unique"
text = text.replace('"tick": 2018,', '"tick": 2019,', 1)

# 2) log append before last '\n ],'
close_marker = nl + " ]," + nl
idx = text.rfind(close_marker)
assert idx > 0, "log close marker missing"
prev = text[idx - 1]
entry = json.dumps(LINE, ensure_ascii=False)
if prev == '"':
    # last element has no trailing comma (json.dumps style): add one before the new entry
    text = text[:idx] + "," + nl + "  " + entry + text[idx:]
elif prev == ",":
    text = text[:idx] + nl + "  " + entry + text[idx:]
else:
    raise AssertionError("log close anchor unexpected: %r" % prev)

# 3) ts (top-level ts is the LAST "ts" field in the file, after the log array)
matches = list(re.finditer(r'"ts": "[^"]*",', text))
assert matches, "ts anchor missing"
m = matches[-1]
text = text[:m.start()] + '"ts": ' + json.dumps(ts, ensure_ascii=False) + "," + text[m.end():]

# 4) task (anchored to the following account_drift_adjudicated field)
pat = re.compile(r'"task": "(.*?)",' + re.escape(nl) + r' "account_drift_adjudicated"')
m = pat.search(text)
assert m, "task anchor missing"
text = text[:m.start(1)] + TASK + text[m.end(1):]

# 5) validate full JSON parse
data = json.loads(text)
assert data["tick"] == 2019
assert data["ts"] == ts
assert data["task"] == TASK
assert data["log"][-1] == LINE

out = (u"\ufeff" if had_bom else u"") + text
open(PATH, "wb").write(out.encode("utf-8"))

# 6) queue restock: append tech#121
qraw = open(QPATH, "rb").read()
qbom = qraw.startswith(b"\xef\xbb\xbf")
qtext = qraw.decode("utf-8-sig")
qnl = "\r\n" if "\r\n" in qtext else "\n"
ITEM = (u"121. [R2019 补货·本轮真发现] fire 窗项消费序律候选：fire-gated 队头项轮内消费=fire_consume 单命令直发"
u"（缺口锚=R2019 实锚：预读 fire_window_card GO 04:14:04〔B-eviction-credit·gate go=True util 44·fire-valid 120s〕"
u"→派发前验证中步〔--help+Select-String 两命令 79s〕→fire_consume 内读卡 04:15:23 已 no-fire〔util-face worst-case 97>80 单翻转〕"
u"=「GO 后零中步立即发」律〔R1995 立·R1999 二案→tech#112 原子消费器根治卡读-发射间 agent 延迟〕第三复发案"
u"·残余面=agent 预读 GO 后的中步窗·工具面自身无恙〔fail-closed 拦截正确〕）"
u"——候选：fire-gated 项〔现役=main#19 SC-005-07 flight-3〕轮内消费序=五查/探针后下一命令即 fire_consume 直发"
u"（其内读卡=唯一权威判定·独立 fire_window_card 预读=信息件非门·预读 GO 锚不构成派发前提）；"
u"判据=下个真窗单命令直发零中步·fire-consume-ledger 内读卡 verdict 序列窗捕获率对照；判负留痕合法"
u"——按认领制随轮领做（CPU 面·零工程）")
assert u"121. [R2019" not in qtext, "tech#121 already present"
assert u"120. [R2012" in qtext, "tech queue tail anchor missing"
if not qtext.endswith(qnl):
    qtext += qnl
qtext += ITEM + qnl
open(QPATH, "wb").write(((u"\ufeff" if qbom else u"") + qtext).encode("utf-8"))

print("OK tick=2019 ts=" + ts + " task_len=" + str(len(TASK)) + " log_line_len=" + str(len(LINE)) + " queue_item=121 bom=" + str(h_bom) if False else "OK tick=2019 ts=" + ts + " task_len=" + str(len(TASK)) + " log_line_len=" + str(len(LINE)) + " queue_item=121 state_bom=" + str(had_bom))
