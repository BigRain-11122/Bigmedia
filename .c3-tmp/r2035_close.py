# r2035_close.py -- waiting-round declaration close (tech#81 self-contained evidence)
# R2035: five-checks quiet (own orders top O-20261008-1105-bm-a.md real file verified
#        boolean double-check; historical log lines carried 0608 typo family, this
#        round's log line corrects to real ID); origin_gap QUIET; group_scan four
#        faces quiet; probes in-band; fire_consume verbatim no-fire rc1 (12th
#        no-fire point, probe-face-busy-contended, ledger 07:25:38 row 22);
#        comfy_activity 07:25:47 quiet rc0 advisory read; F-180 flight-4 + F-181
#        review leg stay fire-ready; tech#92 radar window due 08:00 not yet
#        (07:23 timepoint ~37min); queues gated per R2033 07:02 fresh read carry;
#        no new seeds zero-inflation.
import io, json, datetime

P = 'src/os/state.json'
raw = io.open(P, 'rb').read()
has_bom = raw.startswith(b'\xef\xbb\xbf')
txt = raw.decode('utf-8-sig')
nl = '\r\n' if '\r\n' in txt else '\n'
lines = txt.split(nl)

# --- locate array close + ts + task lines (tail window only) ---
idx_close = idx_ts = idx_task = None
for i in range(len(lines) - 1, max(len(lines) - 30, 0), -1):
    st = lines[i].strip()
    if st == '],':
        idx_close = i
    elif st.startswith('"ts":'):
        idx_ts = i
    elif st.startswith('"task":'):
        idx_task = i
assert idx_close is not None and idx_ts == idx_close + 1 and idx_task == idx_close + 2, \
    (idx_close, idx_ts, idx_task)
assert lines[idx_ts].strip() == '"ts": "2026-10-12 07:18:43",', lines[idx_ts]

LOG = (
    '  "2026-10-12 07:3x R2035: 等待轮声明轮（GPU fire 卡 no-fire rc1·F-180 flight-4+F-181 评审腿维持结转·'
    'tech#92 权威窗 08:00 未到·P-2026-09-28-02 ②+O-20261009-1246 项 c+产品优先律 §2）——'
    '①轮首五查全静=own orders 顶 O-20261008-1105 mtime 12:08:14==R1733 锚零新令（**ID 勘正**=r2035_verify '
    '布尔双查实身 O-20261008-1105-bm-a.md 在盘/O-20260908 不存在=历史 log 行 0608 笔误族·本轮起按实身·'
    'mtime+R1733 锚判据不变）+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan 四面全静'
    '（decisions truly_new=0 水位 150 维持+ledger @BigStream 5 行==值守锚零新转办+ORDERS 行水位 quiet '
    'rows=270 tail_key=\'10-11 13:4x\'==R1979 基线〔tech#103 连窗过〕+HQ orders 14:00:46==R1978 消费锚）'
    '+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继）；②三探针=board 0 FAIL（5 题 10 稿 '
    '5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现'
    '（78 renders unannot=0）/loop_health 2F+265W 皆在案史实带内（两 outage 09-26/09-28 已裁定不重触发·'
    'drift 18≤adjudicated 基线 21）；③tech#121 消费序律执行=三探针毕后下一命令 fire_consume verbatim '
    '正身直发（零预读零中步）=no-fire rc1（reason=card-no-fire: probe-face-busy-contended·ledger 行 '
    '07:25:38 落盘=第 22 行=no-fire 序列第 12 数据点〔R2020-R2023 四点+R2026/R2029/R2030/R2031/R2032/'
    'R2033/R2034 七点续〕）+comfy_activity 07:25:47 quiet rc0 后置 advisory 读（queue 0/0+cpu delta '
    '0.0ms·PID 58200·读序后置注记如实=no-fire 轮无 GO 消费·tech#106 GO 前置律未触发零违例·R1987 定谳'
    '维持=ComfyUI 空闲驻留+util 源=桌面 GUI 群让路正确侧）→F-180 SC-005-07 flight-4（s1_call '
    'preflight 三件+--wedge-probe 就位=tech#122 轻量缓释待真窗实弹）+F-181 REACT-v15 评审腿'
    '（tech#113 生成器发射器 staged·tech#123 preflight 正法重生成）双件维持 fire-ready 结转；'
    '④tech#92 雷达标定权威窗 10-12 08:00 未到（07:23 时点 ~37min·届日即领不预扫〔zhihu-hot 头部 '
    '≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〕）+meme V1/krea2 双查看位承 R2028-R2030 锚禁重扫+'
    'MD-0002 T2I gated CEO 点头维持；⑤三队盘点=承 R2033 07:02 fresh 复读面（~23min 龄零状态变化·'
    '禁逐轮重扫同一等待对象反重复律）=main 全 gated/查看位（#19 flight-4 gated fire 窗/#20 F-181 '
    'gated fire 窗/#7 krea2 禁重扫/#9 编年史下窗=meme V1 定版事件窗）+tech 全 done/gated/观察位'
    '（#92 08:00 权威窗/#93 gated CEO 点头/#115/#116 随件/#118 gated REACT-v20/#124 提取门槛未到）+'
    'explore 全 done/gated/到点未至（#14/#22 ≥10-17/#24 W4 ≤10-17/#26 回访 10-13/15/#27 gated '
    '正片定版窗）→fire 项外真无可执行项=一行声明收轮合法（waiting: GPU fire 真窗〔ETA=util 面落 '
    '80 下即 F-180 flight-4 派发→F-181 评审腿〕+tech#92 雷达标定权威窗 2026-10-12 08:00+'
    'meme V1 成片落件）；⑥例行件=10-12 日报在案不重跑（R2008 一份为真相）·W42 周审第 4 期在案'
    '（R2008）·GB §④ v1.3 下期 10-15 ≤7d 跳过·export_ts R2025 05:36:09 <24h 零 CEO 可见成品态变化'
    '节流不刷（live 三行核读仍准：F-179 收官态/里程碑 08:00 判读窗+fire 双件未过期）·T1 催办无超线项'
    '（账号物理件=呈现状行不催办）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0'
    '（fire 卡读+探针只读零本地模型产出调用·P-54⑤ 计量律）；⑦队列补货步=真无独立新种子如实注记'
    '零膨胀（no-fire reason=tech#75/#121 既有判定面·三队盘点零状态变化·禁凑数律）·临时件清理钩='
    'r2035_verify_anchors.py+r2035_close.py 证据件随本 commit 收口（tech#81 自含律·探针读数会话内'
    '直读零落盘）——下轮=R2036 fire 窗项轮首命令 fire_consume verbatim 正身直发维持'
    '（GO=F-180 flight-4 派发〔preflight 三件首战〕→S1 判词 ≥9=TTS light 续链→F-180 登记·'
    'F-181 后段位）+tech#92 雷达标定权威窗 08:00 届日即领并读（zhihu-hot 头部 ≥3 件 ≥60=文本腿'
    '收口·FAIL=阈值分层腿递补）"'
)

# previous last array element (R2034) gains a trailing comma; LOG becomes last (no comma)
prev = lines[idx_close - 1]
assert prev.strip().startswith('"2026-10-12 07:16 R2034:'), prev[:60]
if not prev.rstrip().endswith(','):
    lines[idx_close - 1] = prev + ','
assert not LOG.rstrip().endswith(','), 'LOG must be last element without trailing comma'

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TASK = ' "task": "等待轮声明轮·fire_consume no-fire rc1（第 12 数据点）+tech#92 08:00 届日即领",'

lines.insert(idx_close, LOG)
lines[idx_ts + 1] = ' "ts": "%s",' % now
lines[idx_task + 1] = TASK

out = nl.join(lines)
assert out.count('"tick": 2034,') == 1
out = out.replace('"tick": 2034,', '"tick": 2035,')

json.loads(out)  # validity gate (fail-closed before write)

data = out.encode('utf-8')
if has_bom:
    data = b'\xef\xbb\xbf' + data
io.open(P, 'wb').write(data)
print('r2035 close OK: tick=2035 ts=%s bom=%s nl=%r json=valid' % (now, has_bom, nl))
