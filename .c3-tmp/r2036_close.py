# r2036_close.py -- waiting-round declaration close (tech#81 self-contained evidence)
# R2036: five-checks quiet (own orders top O-20261008-1105 mtime 12:08:14 == R1733
#        anchor; origin_gap QUIET ahead0 behind0; group_scan four faces quiet --
#        decisions truly_new=0 watermark 150 maintained with D-20261012-01/02
#        already consumed, hq-decisions mtime 00:12:04 silent vs watermark;
#        ledger @BigStream 5 lines == standing anchor; ORDERS watermark quiet
#        rows=270 tail_key='10-11 13:4x' == R1979 baseline, tech#103 pass-through;
#        HQ orders 14:00:46 == R1978 consumed anchor); probes in-band;
#        fire_consume verbatim no-fire rc1 (13th no-fire point, card-no-fire:
#        probe-face-busy-contended, ledger row 23 at 07:35:20); comfy_activity
#        07:35:40 quiet rc0 advisory read (no new row = same-verdict TTL family);
#        F-180 flight-4 + F-181 review leg stay fire-ready; tech#92 radar
#        authoritative window due 08:00 not yet (07:33 timepoint ~27min);
#        queues gated (this round did a FRESH tech+explore item-by-item inventory;
#        main carried from R2035 read ~13min age, zero state change); no new
#        seeds zero-inflation.
import io, json, datetime, sys, os

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
assert lines[idx_ts].strip() == '"ts": "2026-10-12 07:28:17",', lines[idx_ts]

LOG = (
    '  "2026-10-12 07:4x R2036: 等待轮声明轮（GPU fire 卡 no-fire rc1·F-180 flight-4+F-181 评审腿维持结转·tech#92 权威窗 08:00 未到·P-2026-09-28-02 ②+O-20261009-1246 项 c+产品优先律 §2）——'
    '①轮首五查全静=own orders 顶 O-20261008-1105 mtime 12:08:14==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan 四面全静'
    '（decisions truly_new=0 水位 150 维持〔D-20261012-01/02 前轮已入水位·hq-decisions mtime 00:12:04 对水位静默〕+ledger @BigStream 5 行==值守锚零新转办+ORDERS 行水位 quiet '
    'rows=270 tail_key=\'10-11 13:4x\'==R1979 基线〔tech#103 连窗过〕+HQ orders 14:00:46==R1978 消费锚）'
    '+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继）；②三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面'
    '（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现/loop_health 2F+265W 皆在案史实带内（两 outage 09-26/09-28 已裁定不重触发·drift 18≤adjudicated 基线 21）；'
    '③tech#121 消费序律执行=三探针毕后 fire_consume verbatim 正身直发（probe_capture 单调用紧凑面消费）=no-fire rc1'
    '（reason=card-no-fire: probe-face-busy-contended·ledger 行 07:35:20 落盘=第 23 行=no-fire 序列第 13 数据点〔R2020-R2035 十二点续〕）'
    '+comfy_activity 07:35:40 quiet rc0 后置 advisory 读（queue 0/0+cpu delta 0.0ms·PID 58200·同判 dedup 无新行=07:16 行后 TTL 族维持）'
    '→F-180 SC-005-07 flight-4（s1_call preflight 三件+--wedge-probe 就位=tech#122 轻量缓释待真窗实弹）+F-181 REACT-v15 评审腿'
    '（tech#113 生成器发射器 staged·tech#123 preflight 正法重生成）双件维持 fire-ready 结转；'
    '④tech#92 雷达标定权威窗 10-12 08:00 未到（07:33 时点 ~27min·届日即领不预扫〔zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〕）'
    '+meme V1/krea2 双查看位承 R2028-R2030 锚禁重扫+MD-0002 T2I gated CEO 点头维持；'
    '⑤三队盘点=本轮 fresh 复读面（tech+explore 逐项分类盘点：open 位全 gated〔#1/#3/#9 GPU 独占窗+#14/#15/#17/#18/#29/#42/#59/#63/#93 gated〕'
    '+#92 08:00 权威窗+#115/#116/#118 观察位随件/到点未至+#34 判负留痕+#124 门槛未到+explore 全 done/gated/到点〔#14/#22 ≥10-17/#24 W4 ≤10-17/#26 回访 10-13/15〕'
    '+main 承 R2035 盘点面 ~13min 龄零状态变化）→fire 项外真无可执行项=一行声明收轮合法'
    '（waiting: GPU fire 真窗〔ETA=util 面落 80 下即 F-180 flight-4 派发→F-181 评审腿〕+tech#92 雷达标定权威窗 2026-10-12 08:00+meme V1 成片落件）；'
    '⑥例行件=10-12 日报在案不重跑（R2008 一份为真相）·W42 周审第 4 期在案·GB §④ v1.3 下期 10-15 ≤7d 跳过·export_ts 05:36:09 <24h 零 CEO 可见成品态变化节流不刷'
    '（live 三行核读仍准：F-179 收官态/里程碑 08:00 判读窗+fire 双件未过期）·T1 催办无超线项·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）'
    '·tokens:local=0（探针只读+fire 卡读零本地模型产出调用·P-54⑤ 计量律）；'
    '⑦队列补货步=真无独立新种子如实注记零膨胀（no-fire reason=tech#75/#121 既有判定面·三队盘点零状态变化·禁凑数律）'
    '·临时件清理钩=r2036_close.py 证据件随本 commit 收口（tech#81 自含律·探针读数会话内直读零落盘·fire-consume-ledger 行 23 随账）'
    '——下轮=R2037 fire 窗项轮首命令 fire_consume verbatim 正身直发维持（GO=F-180 flight-4 派发〔preflight 三件首战〕→S1 判词 ≥9=TTS light 续链→F-180 登记·F-181 后段位）'
    '+tech#92 雷达标定权威窗 08:00 届日即领并读（zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补）"'
)

# previous last array element (R2035) gains a trailing comma; LOG becomes last (no comma)
prev = lines[idx_close - 1]
assert prev.strip().startswith('"2026-10-12 07:3x R2035:'), prev[:60]
if not prev.rstrip().endswith(','):
    lines[idx_close - 1] = prev + ','
assert not LOG.rstrip().endswith(','), 'LOG must be last element without trailing comma'

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TASK = ' "task": "等待轮声明轮·fire_consume no-fire rc1（第 13 数据点）+tech#92 08:00 届日即领",'

lines.insert(idx_close, LOG)
lines[idx_ts + 1] = ' "ts": "%s",' % now
lines[idx_task + 1] = TASK

out = nl.join(lines)
assert out.count('"tick": 2035,') == 1
out = out.replace('"tick": 2035,', '"tick": 2036,')

json.loads(out)  # validity gate (fail-closed before write)

data = out.encode('utf-8')
if has_bom:
    data = b'\xef\xbb\xbf' + data
io.open(P, 'wb').write(data)
print('r2036 close OK: tick=2036 ts=%s bom=%s nl=%r json=valid' % (now, has_bom, nl))

# --- script-internal accounting commit (tech#65: shrink kill window) ---
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'os'))
import close_commit
MSG = ("R2036 waiting-round: fire_consume no-fire rc1 (13th point, probe-face-busy-contended, ledger row 23); "
       "comfy quiet rc0; F-180 flight-4 + F-181 stay fire-ready; tech#92 radar window due 08:00 not yet (~17min); "
       "five-checks quiet (origin-gap QUIET, group_scan quiet, D-20261012-02 in watermark); probes in-band; "
       "queues gated (fresh tech/explore inventory, main carried); no new seeds zero-inflation [via bm-a]")
rc, log_lines = close_commit.run_close_commit(
    ['src/os/state.json', 'data/pipeline/fire-consume-ledger.jsonl', '.c3-tmp/r2036_close.py'], MSG)
for ln in log_lines:
    print(ln)
print('run_close_commit rc=%d' % rc)
