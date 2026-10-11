# R2033 close accounting: waiting-window declaration round.
# Surgical text edits on state.json (no full re-dump); fail-closed anchors; JSON re-load validation.
import io, json, sys, datetime

STATE = r"src\os\state.json"

with io.open(STATE, "r", encoding="utf-8") as f:
    text = f.read()

def must_count(anchor, n):
    c = text.count(anchor)
    if c != n:
        print("ANCHOR-FAIL: %r count=%d expected=%d" % (anchor[:60], c, n))
        sys.exit(2)

# 1) tick 2032 -> 2033
must_count('"tick": 2032,', 1)
text = text.replace('"tick": 2032,', '"tick": 2033,')

# 2) append R2033 log entry after R2032 (last entry, currently ends without comma)
anchor2 = 'F-181 \u8bc4\u5ba1\u817f\u540e\u6bb5\u4f4d\uff09+tech#92 \u6743\u5a01\u7a97 08:00 \u5c4a\u65e5\u5373\u9886"\n ],'
must_count(anchor2, 1)

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
log_line = (
    "2026-10-12 07:05 R2033: 等待轮声明轮（GPU fire 卡 no-fire rc1·F-180 flight-4+F-181 评审腿维持结转·tech#92 权威窗 08:00 未到·三队 fresh 复读全 gated·P-2026-09-28-02 ②+O-20261009-1246 项 c+产品优先律 §2）"
    "——①轮首五查全静=own orders 顶 O-20260908-1105 mtime 12:08:14==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan 四面全静（decisions truly_new=0 水位 150 维持+ledger @BigStream==值守锚零新转办+ORDERS 行水位 quiet rows=270 tail_key='10-11 13:4x'==R1979 基线〔tech#103 连窗过〕+HQ orders 14:00:46==R1978 消费锚）+无 index.lock+树态=MV sprint 会话域在飞件零接触（mv0001/mv001 批件零碰·R1745 承继）；"
    "②tech#106 消费律+tech#121 消费序律执行=comfy_activity 07:02:53 quiet rc0（queue 0/0+cpu delta 0.0ms·PID 58200·ledger 行落账）→三探针毕后下一命令 fire_consume verbatim 正身直发（零预读零中步）=no-fire rc1（reason=card-no-fire: probe-face-busy-contended·ledger 行 07:02 落盘=no-fire 序列第 10 数据点〔R2020-R2023 四点+R2026/R2029/R2030/R2031/R2032 续·tech#121 判据窗=真窗捕获率对照续记〕）→F-180 SC-005-07 flight-4（s1_call preflight 三件+--wedge-probe 就位=tech#122 轻量缓释待真窗实弹）+F-181 REACT-v15 评审腿（tech#113 生成器发射器 staged·tech#123 preflight 正法重生成）双件维持 fire-ready 结转（R2032 指针照旧）；"
    "③tech#92 雷达标定权威窗 10-12 08:00 未到（07:02 时点 ~58min·届日即领不预扫〔zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〕）；"
    "④三队盘点=本轮 fresh 复读（backlog 顶行+tech.md/explore.md 尾实读·R2030 面 28min 龄后复核零漂移）=main 全 gated/查看位（#19 flight-4 gated fire 窗·#20 F-181 gated fire 窗·#7 krea2 R1978 锚禁重扫·#9 编年史下窗=meme V1 定版/成片闸事件窗）+tech 全 done/gated/观察位（#92 08:00 权威窗·#93 gated CEO 点头·#115/#116 观察位随件·#118 gated REACT-v20·#124 提取门槛未到两副本不提取禁凑数律）+explore 全 done/gated/到点未至（#14/#22 ≥10-17·#24 W4 ≤10-17·#26 回访 10-13/15·#27 gated 正片定版窗）→fire 项外真无可执行项=一行声明收轮合法（waiting: GPU fire 真窗〔ETA=util 面落 80 下即 F-180 flight-4 派发→F-181 评审腿〕+tech#92 雷达标定权威窗 2026-10-12 08:00+meme V1 成片落件）；"
    "⑤三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现（78 renders unannot=0）/loop_health 2F+265W 皆在案史实带内（两 outage 09-26/09-28 已裁定不重触发·drift 18≤adjudicated 基线 21）；"
    "⑥例行件=10-12 日报在案不重跑（R2008 一份为真相）·W42 周审第 4 期在案（R2008）·GB §④ v1.3 下期 10-15 ≤7d 跳过·export_ts R2025 05:36:09 <24h 零 CEO 可见成品态变化节流不刷（live 三行核读仍准：F-179 收官态/里程碑 08:00 判读窗+fire 双件未过期）·T1 催办无超线项（账号物理件=呈现状行不催办）·meme V1/krea2 双查看位承 R2028-R2032 锚禁重扫·MD-0002 T2I gated CEO 点头维持·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0（fire 卡读+探针只读零本地模型产出调用·P-54⑤ 计量律）；"
    "⑦队列补货步=真无独立新种子如实注记零膨胀（no-fire reason=tech#75/#121 既有判定面·三队盘点零状态变化·禁凑数律）·临时件清理钩=本轮零新临时件（探针读数会话内直读零落盘·fire-consume-ledger/comfy-activity-ledger 行=唯一持久踪迹随本 commit）"
    "——下轮=R2034 fire 窗项轮首命令 verbatim 正身照发：python src/os/fire_consume.py --launch data/storylines/audio/sc005-07-v1-tmp/s1_call.py --ledger（GO=fire→F-180 flight-4 派发〔preflight 三件首战〕→S1 判词 ≥9=TTS light 续链→F-180 登记·F-181 评审腿后段位；no-fire rc1=双件维持结转）+tech#92 雷达标定权威窗 08:00 届日即领（已过 08:00 时点即首查领做：zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补）"
)
assert '"' not in log_line.replace('\\"', ''), "log line contains raw double quote"

replacement2 = ('F-181 \u8bc4\u5ba1\u817f\u540e\u6bb5\u4f4d\uff09+tech#92 \u6743\u5a01\u7a97 08:00 \u5c4a\u65e5\u5373\u9886",\n'
                '  ' + json.dumps(log_line, ensure_ascii=False) + '\n ],')
text = text.replace(anchor2, replacement2)

# 3) ts + task refresh (close-step law)
must_count('"ts": "2026-10-12 06:59:33",', 1)
text = text.replace('"ts": "2026-10-12 06:59:33",', '"ts": "%s",' % now)

old_task = ' "task": "\u7b49\u5f85\u8f6e\u58f0\u660e\u8f6e\u00b7fire_consume no-fire rc1\uff08\u7b2c 9 \u6570\u636e\u70b9\uff09+focus verbatim \u5185\u5d4c\u6536\u53e3",'
must_count(old_task, 1)
new_task = ' "task": "\u7b49\u5f85\u8f6e\u58f0\u660e\u8f6e\u00b7fire_consume no-fire rc1\uff08\u7b2c 10 \u6570\u636e\u70b9\uff09+tech#92 08:00 \u5c4a\u65e5\u5373\u9886",'
text = text.replace(old_task, new_task)

# validate JSON before write
obj = json.loads(text)
assert obj["tick"] == 2033, "tick mismatch"
assert len(obj["log"]) >= 2033, "log length"
assert obj["log"][-1].startswith("2026-10-12 07:"), "tail log entry mismatch"

with io.open(STATE, "w", encoding="utf-8", newline="") as f:
    f.write(text)

# re-load validation from disk
with io.open(STATE, "r", encoding="utf-8") as f:
    obj2 = json.load(f)
print("STATE-CLOSE-OK tick=%d ts=%s task=%s log_tail=%r" % (
    obj2["tick"], obj2["ts"], obj2["task"], obj2["log"][-1][:50]))
