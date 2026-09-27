# r502b_account.py - R502 end-of-round order-receipt addendum: state.json (third log line O-20260927-1050-HQ-C receipt + focus rewire to four-agenda mode + ts/task refresh, tick stays 502) + status-export.json (export_ts, outs[0][1]/results[0][1] append order-receipt faces); anchors for old long strings extracted from parsed JSON; json.load validation built in
import io, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

now = datetime.datetime.now()
TS_MIN = now.strftime("%Y-%m-%d %H:%M")
TS_FULL = TS_MIN + ":00"
TS_ISO = now.strftime("%Y-%m-%dT%H:%M") + ":00+08:00"

def load_text(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()

def save_text(p, t):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)

def sub1(t, old, new):
    n = t.count(old)
    assert n == 1, "anchor not unique (%d): %r" % (n, old[:80])
    return t.replace(old, new)

# ---------- state.json ----------
sp = ROOT + r"\src\os\state.json"
txt = load_text(sp)
NL = "\r\n" if "\r\n" in txt else "\n"
st_old = json.loads(txt)
old_task = st_old["task"]
old_ts = st_old["ts"]
assert st_old["tick"] == 502 and st_old["production"] == "open" and old_ts == "2026-09-27 10:46:00"
assert st_old["log"][-1].startswith("2026-09-27 10:46 R502:")

LOG_R502B = (
    TS_MIN + " R502 轮末收令补记（O-20260927-1050-HQ-C 媒体司自驱动员令·P-202609-27-07·U255·CEO 交互直令 ~10:4x「有公司一直闲着，给我调动起来，好好研究方向，自己动起来」）："
    "本轮回执 push 拒绝揭远端 bm-c 直推新令（681ece6·orders/O-20260927-1050-HQ-C.md 单件·与本轮写区零交集）→pull --rebase 整合（9f892ee 落其顶零冲突）"
    "→**ack ≤15min 时限内**=执行回执落令尾（四议程全认领）+本轮 commit 含令号（P-51 送达）；"
    "**idle-fast 空转快速路径对四议程面即时停用**（队列空→拉议程产出·每窗 ≥1 实质产出·U222 禁待命常设律）——"
    "四议程时限挂账：①方向研究首件 ≤09-28 10:50（R-件《AI 内容形态与平台算法方向研究》P-65 三件套·AI 短剧/数字人播报/无人直播/自动化栏目四形态 × 抖音/视频号/B站→「开号后 30 天打法」决策件）"
    "②库存与排期 ≤09-28 10:50（实况=成品库 46 件≠10 基数·HQ 疑旧快照如实注记·落地件=发布排期表 v1+46 件对 30 天日更映射+缺口补件清单）"
    "③城市叙事首件样片脚本 ≤09-29 10:50（互聊台账 ≤09-28 12:00 到位前先消费 charter 既有立法面·派生非编造）"
    "④调研部首件选题提前交卷（原 ≤10-01）；"
    "边界照守（账号=CEO 物理件不启动不催办·未上线=未测量·hit-chain 承接不替代律）；"
    "实况注记=今日 00:35-08:15 实活批在案（#71 重制四件+DIGEST×2+REACT+调研部回执+商业化映射）·08:15 后 15 轮空转批=本令点破面如实认领。"
    "下轮=R503 议程 1 起链（P-65 立项三问+骨架+存量源映射先落）。"
)

new_task = LOG_R502B.split(" ", 2)[2][:60]

txt = sub1(txt, '"focus": "R503: 快速路径首查（新令/集团转办/探针红）→#59 REACT 09-28 热点窗届日领',
               '"focus": "R503: **O-20260927-1050 四议程常设面优先**（①方向研究首件 ≤09-28 10:50〔R-件《AI 内容形态与平台算法方向研究》P-65 三件套〕→②发布排期表 v1+库存 46 件对 30 天日更映射+缺口补件清单 ≤09-28 10:50→③城市叙事首件样片脚本 ≤09-29 10:50〔U243 互聊台账到位前先消费 charter 既有立法面〕→④调研部首件选题提前交卷〔原 ≤10-01〕·队列空→拉议程产出·每窗 ≥1 实质产出·**idle-fast 空转路径四议程面停用**）→例行窗照排：#59 REACT 09-28 热点窗届日领')
txt = sub1(txt, '新令/集团转办/探针红出现即优先；全静即 idle-fast（并窗轮 1/6·新窗 R503-R508 满 6 收账→R508 batch commit·跨日边界 09-28 00:00 先到即收）',
               '新令/集团转办/探针红出现即优先；全静=拉四议程产出（O-1050 议程面停用令·禁空转收轮）；收账并窗律照行（实活轮=逐轮 commit·纯记账轮并窗照旧·窗 R503-R508 满 6 或跨日 09-28 00:00 先到即收）')
txt = sub1(txt, NL + ' ],' + NL + ' "ts": "' + old_ts + '",',
               ',' + NL + '  "' + LOG_R502B + '"' + NL + ' ],' + NL + ' "ts": "' + TS_FULL + '",')
txt = sub1(txt, '"task": "' + old_task + '"', '"task": "' + new_task + '"')
st = json.loads(txt)
assert st["tick"] == 502 and st["production"] == "open" and st["ts"] == TS_FULL
assert st["log"][-1].startswith(TS_MIN + " R502 轮末收令补记")
assert st["task"] == new_task and len(new_task) == 60
assert st["focus"].startswith("R503:") and "O-20260927-1050 四议程常设面优先" in st["focus"] and "全静=拉四议程产出" in st["focus"]
save_text(sp, txt)
print("state.json OK: tick=502 ts=%s log_tail=R502 order-addendum focus=4-agenda mode" % TS_FULL)

# ---------- status-export.json ----------
sep = ROOT + r"\docs\status-export.json"
t2 = load_text(sep)
se_old = json.loads(t2)
old_out1 = se_old["outs"][0][1]
old_res1 = se_old["results"][0][1]
assert old_out1.startswith("tick 502·R502") and old_res1.startswith("R502 ")

AMEND_OUT = (
    "；**轮末收令 O-20260927-1050-HQ-C 媒体司自驱动员令（P-202609-27-07）ack ≤15min 时限内**（执行回执落令尾+commit 含令号=P-51 送达）"
    "·**idle-fast 四议程面停用**（队列空→拉议程产出·每窗 ≥1 实质产出：①方向研究首件 ≤09-28 10:50②发布排期表 v1+库存 46 件对 30 天日更映射+缺口清单 ≤09-28 10:50③城市叙事首件样片脚本 ≤09-29 10:50④调研部首件选题提前交卷）"
)
AMEND_RES = (
    "·轮末收令 O-20260927-1050-HQ-C 四议程自驱令 ack 时限内（idle-fast 议程面停用·方向研究首件+排期表 ≤09-28 10:50·城市叙事脚本 ≤09-29 10:50·调研部提前交卷）"
)

t2 = sub1(t2, '"export_ts": "2026-09-27T10:46:00+08:00"', '"export_ts": "' + TS_ISO + '"')
t2 = sub1(t2, '"' + old_out1 + '"', '"' + old_out1 + AMEND_OUT + '"')
t2 = sub1(t2, '"' + old_res1 + '"', '"' + old_res1 + AMEND_RES + '"')
se = json.loads(t2)
assert se["export_ts"] == TS_ISO
assert "O-20260927-1050-HQ-C" in se["outs"][0][1] and "O-20260927-1050-HQ-C" in se["results"][0][1]
save_text(sep, t2)
print("status-export.json OK: export_ts=%s outs/results amended with order receipt" % TS_ISO)
