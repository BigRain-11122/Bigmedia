# r502c_account.py - R502 agenda-1 kickoff addendum: state.json (4th log line + ts/task refresh, tick stays 502) + status-export.json (export_ts + outs[0][1]/results[0][1] append agenda-1 clause)
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
assert st_old["tick"] == 502 and old_ts == "2026-09-27 10:48:00"
assert st_old["log"][-1].startswith("2026-09-27 10:48 R502 轮末收令补记")

LOG_R502C = (
    TS_MIN + " R502 议程 1 起链腿（轮末续产·O-1050）：v0.1 交付=docs/research/R-20260927-bigstream-03-ai-forms-platform-algorithms.md"
    "（P-65 三件套齐：立项三问+四形态对位〔F1 三线 IP 在产/F2 机器叙述者在产/F3 直播 blocked 照守/F4 L-卡最强线〕"
    "+三平台算法指针〔视频号/公众号/B站全在册 A/B 级锚·抖音零断言卡点如实〕+四形态×三平台矩阵+「开号后 30 天打法」v0.1 框架"
    "〔周 1 测水温/周 2-3 双线日更+单点突破/周 4 复盘收敛·M6 反哺权重·未上线=未测量〕+应用表六行全挂承接+验证声明与补采清单）"
    "——零新外部采集全引在册锚·M 级决策假设 3 处显式标注·v1.0 升级位=§8 四刀补采（巨量算数换刀/B站创作学院/视频号创作者中心/公众号 2026Q4 时效复扫）+排期表 v1 联动；"
    "四议程状态：①v0.1 毕（v1.0 ≤09-28 10:50）②排期表 v1 未起（R503 起链）③城市叙事脚本未起（≤09-29 10:50）④调研部首件提前交卷位（原 ≤10-01 提速·随窗）。"
    "下轮=R503 议程 2 排期表 v1 起链（46 件库存对 30 天日更映射+每周栏目配比·消费 R-03 §6 框架）→议程 1 §8 补采刀→逐窗推进。"
)

new_task = LOG_R502C.split(" ", 2)[2][:60]
txt = sub1(txt, NL + ' ],' + NL + ' "ts": "' + old_ts + '",',
               ',' + NL + '  "' + LOG_R502C + '"' + NL + ' ],' + NL + ' "ts": "' + TS_FULL + '",')
txt = sub1(txt, '"task": "' + old_task + '"', '"task": "' + new_task + '"')
st = json.loads(txt)
assert st["tick"] == 502 and st["ts"] == TS_FULL
assert st["log"][-1].startswith(TS_MIN + " R502 议程 1 起链腿")
assert st["task"] == new_task and len(new_task) == 60
save_text(sp, txt)
print("state.json OK: tick=502 ts=%s log_tail=R502 agenda-1 kickoff" % TS_FULL)

# ---------- status-export.json ----------
sep = ROOT + r"\docs\status-export.json"
t2 = load_text(sep)
se_old = json.loads(t2)
old_out1 = se_old["outs"][0][1]
old_res1 = se_old["results"][0][1]
AMEND2_OUT = "；**议程 1 起链=v0.1 交付**（R-20260927-bigstream-03 方向研究首件·P-65 三件套齐·30 天打法框架 v0.1·全引在册锚零新外采·v1.0=§8 四刀补采+排期表联动 ≤09-28 10:50）"
AMEND2_RES = "·议程 1 方向研究首件 v0.1 交付（R-03·四形态×三平台矩阵+30 天打法框架·v1.0 ≤09-28 10:50）"
t2 = sub1(t2, '"export_ts": "2026-09-27T10:48:00+08:00"', '"export_ts": "' + TS_ISO + '"')
t2 = sub1(t2, '"' + old_out1 + '"', '"' + old_out1 + AMEND2_OUT + '"')
t2 = sub1(t2, '"' + old_res1 + '"', '"' + old_res1 + AMEND2_RES + '"')
se = json.loads(t2)
assert se["export_ts"] == TS_ISO and "R-20260927-bigstream-03" in se["outs"][0][1]
save_text(sep, t2)
print("status-export.json OK: export_ts=%s outs/results amended with agenda-1 v0.1" % TS_ISO)
