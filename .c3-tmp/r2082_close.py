# -*- coding: utf-8 -*-
# R2082 close: state.json tick/log/ts/task/focus + export live3/round + evidence file + two-segment commit
import json, io, os, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # repo root (script in .c3-tmp)
if not os.path.isdir(os.path.join(ROOT, 'src', 'os')):
    ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'

now = datetime.now()
ts = now.strftime('%Y-%m-%d %H:%M:%S')
ts_lo = now.strftime('%H:%M')[:4] + 'x'  # 23:2x style

LOG_LINE = (
    "2026-10-12 23:2x R2082: 死线窗值守轮（O-2305 让位维持·五查全静·收口判据未达·四查尽后守望如实）——"
    "①轮首五查=origin_gap_check QUIET ahead0 behind0+group_scan ORDERS rows 333==水位 tail '10-12 23:0x' 零新行"
    "+decisions truly_new=0 水位 152+ledger @BigStream 5 行==值守锚+DIGEST-SUPPLY quiet+ORIGIN-DELTA delta=0+无 index.lock"
    "+树态=MV 会话域在飞件零接触（R1745 承继）+tech#140 他窗在飞（fire_window_card.py+tests M·R1893 脏面两分律零接触）；"
    "②MV 死线窗读数=comfy_activity active（wave-gap-recent-output newest_age=470s）×mv_sprint_probe active（FRAME-GATE-WHITELIST-v1.md 36.5min 前写）"
    "=收口判据未达（O-2305 死线 10-13 08:30·导演席在执）→撤旗+worker-restart main#21+F-180/181/182 接力顺延维持；"
    "fire_consume verbatim 单命令直发=no-fire rc1 reason=card-no-fire: mv-active（CEO 死线优先线 yield 正确侧）"
    "+AIHOT pause 旗核验维持（reason=O-2025 夜窗 KF 分工·worker_restart_paused=true）；"
    "③tech#139 观察位当窗实弹首读（夜窗波进行期）=comfy_activity active+深度判别探针（.c3-tmp/r2082_output_face_probe.py·"
    "face 计数不区分深度故补独立扫）读本窗 fresh 唯一项 kf_bma/ L1 单层目录（age 852s）→两层深 face（output/<a>/<b>/file）未被实弹行使"
    "·i2v 正片波按 O-2305 落 bm-c lane=本机 face 结构性不可见·观察位维持开（bm-a i2v 腿开跑=后续轮实弹闭环位·收口窗末零两层深写=判负条款收口位）"
    "·tech.md R2082 注一行；"
    "④四查尽=backlog 顶 #111=MV 会话域在执零接触（ack 毕禁重扫）+P2 开放项全 gated/在飞/观察位未到触发"
    "（#139 判读毕维持开·#118 时间闸 v20 收官·#126 gated resume·#135 fire 窗+card 他窗在飞·#140 他窗在飞）"
    "+P3 开放项全时间闸/GPU gated（#14 B3 周更 10-17/#18 gated 10-16/#22 次读距基线 ≥7d/#27 歌词卡句库=MV 会话域在飞正典活稿零接触）"
    "→真无可领生产活=守望轮如实（保护态豁免面=O-2305 CEO 优先线·非违规闲置）；"
    "⑤三探针带内=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现"
    "（78 renders unannot=0）/loop_health 3F+282W 皆在案史实（09-26/09-28 outage+10-12 晨间窗·drift 18≤adjudicated 基线 21"
    "·export-do 121 字 WARN=本轮 export 刷新一并修）；"
    "⑥例行件=10-12 日报在案不重跑（R2008 一份为真相）+W42 周审在案（R2011）+GB §④ v1.3 下期 10-15 ≤7d 跳过"
    "+T1 催办无超线项（账号物理件=呈现状行不催办）+HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）"
    "+tokens:local=0（探针/扫描/git 直读=零本地模型产出调用·P-54⑤ 计量律）；"
    "⑦队列补货步=tech#139 R2082 实弹注=既有观察位读数回灌非新种子·真无独立新种子如实注记零膨胀（禁凑数律）"
    "·临时件清理钩=r2082 探针/读数证据件随 commit 入账（tech#81 自含律）零遗留"
    "——下轮=R2083 死线窗值守续（收口判据先行〔comfy output 持续闲 ≥30min 或显式收口+成片呈报轻扫〕"
    "→达成即撤旗+worker-restart main#21+F-180/181/182 fire 接力+tech#92 顺延律随行）+main#22 常务轮复读 10-13 00:00 窗。收账两段 commit+push"
)

FOCUS_LINE = (
    "死线窗值守（O-2305 明早 08:30 全曲成片死线·MV CEO 优先线独占·fire 三件 F-180/181/182 让位结转+AIHOT pause 维持）"
    "→收口判据达成即撤旗（watchdog pause 旗移除）+worker-restart main#21+F-180/181/182 fire 接力（tech#105 序律）"
    "+main#22 10-13 00:00 常务轮复读+tech#92 权威窗顺延随 resume 分叉（R2047 律）；"
    "R2082 读数=comfy active（output 470s）×mv active（白名单 36.5min）=未达；tech#139 实弹首读=L1-only 两层深 face 未行使"
)

# --- 1. state.json ---
sp = os.path.join(ROOT, 'src', 'os', 'state.json')
with io.open(sp, encoding='utf-8') as f:
    st = json.load(f)
assert st.get('tick') == 2081, 'tick drift: %s' % st.get('tick')
st['tick'] = 2082
st['log'].append(LOG_LINE)
st['ts'] = ts
st['focus'] = FOCUS_LINE
prefix = '2026-10-12 23:2x R2082: '
task_src = LOG_LINE[len(prefix):]
st['task'] = task_src[:60]
# orders watermark unchanged (group_scan quiet: rows 333 tail '10-12 23:0x')
with io.open(sp, 'w', encoding='utf-8', newline='') as f:
    json.dump(st, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('state.json: tick=2082 logN=%d ts=%s' % (len(st['log']), ts))

# --- 2. export live3 + round row ---
ep = os.path.join(ROOT, 'docs', 'status-export.json')
with io.open(ep, encoding='utf-8') as f:
    ex = json.load(f)
ex['export_ts'] = ts
ex['live'] = [
    '当前活：死线窗值守——MV 线 active×2（comfy 波间 output 470s+白名单 36.5min 前写）未达收口判据，fire 三件让位结转至 08:30 成片后；tech#139 实弹首读=两层深 face 未行使（L1-only）',
    '最近实物：tech#139 观察位实弹判读+深度探针 r2082_output_face_probe.py+tech.md 注一行 2026-10-12 23:2x',
    '下个里程碑：明早 08:30 MV 全曲成片呈 CEO（CEO 直令死线）；达成后撤旗+worker-restart+F-180 接力；main#22 常务轮复读 10-13 00:00',
]
for row in ex.get('results', []):
    if len(row) == 2 and row[1] == 'OS 轮次':
        row[0] = '2082'
with io.open(ep, 'w', encoding='utf-8', newline='') as f:
    json.dump(ex, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('export: ts=%s live3+round updated' % ts)

# --- 3. evidence file ---
ev = os.path.join(ROOT, '.c3-tmp', 'r2082_tech139_reading.txt')
ev_body = (
    "R2082 tech#139 real-artillery first reading evidence 2026-10-12 23:1x-23:2x\n"
    "=== probe: comfy_activity (23:13) ===\n"
    "verdict=active rc=1; queue running=0 pending=0; cpu delta=0.0ms; output recent=1 newest_age=470s; note=wave-gap-recent-output\n"
    "=== probe: mv_sprint_probe (23:13) ===\n"
    "verdict=active rc=1 threshold=90min; mv-outbound age=36.5min (FRAME-GATE-WHITELIST-v1.md)\n"
    "=== depth-discriminating scan (.c3-tmp/r2082_output_face_probe.py, recency 900s) ===\n"
    "852s  FRESH dir L1   kf_bma/\n"
    "total fresh: 1\n"
    "=> Only fresh entry is a ONE-LEVEL directory (KF reburn wave writes output/kf_bma/*.png).\n"
    "=> tech#138 depth-2 face (output/<a>/<b>/file) NOT exercised by real data on this machine.\n"
    "=> i2v production wave per O-20261012-2305 lands on bm-c lane (bmc/i2v) = structurally invisible to\n"
    "   this machine's local output face (negative-clause boundary in the queue item).\n"
    "=> Observation position stays open: bm-a i2v leg (main#25 original 32-slot plan, may start after KF\n"
    "   closure) = later-round real-artillery closure slot; if the post-08:30 window ends with zero\n"
    "   two-level writes, close per the negative clause.\n"
    "=== fire_consume verbatim (23:16) ===\n"
    "no-fire rc1 reason=card-no-fire: mv-active (CEO deadline-line yield, correct side)\n"
    "=== AIHOT watchdog pause flag (23:19) ===\n"
    "pause=true worker_restart_paused=true reason=O-20261012-2025 night KF resource split (held)\n"
)
with io.open(ev, 'w', encoding='utf-8', newline='') as f:
    f.write(ev_body)
print('evidence: %s' % ev)

# --- 4. two-segment close commit ---
sys.path.insert(0, os.path.join(ROOT, 'src', 'os'))
import close_commit

seg1_files = [
    os.path.join(ROOT, 'state', 'queue', 'tech.md'),
    os.path.join(ROOT, '.c3-tmp', 'r2082_output_face_probe.py'),
    os.path.join(ROOT, '.c3-tmp', 'r2082_tech139_reading.txt'),
    os.path.join(ROOT, '.c3-tmp', 'r2082_close.py'),
]
rc1, lines1 = close_commit.run_close_commit(
    seg1_files,
    "R2082 deliverable: tech#139 first real-artillery reading (L1-only fresh kf_bma, depth-2 face unexercised; "
    "bm-c i2v lane invisible per negative clause) + depth probe + evidence [via bm-a]",
    root=ROOT,
)
for ln in lines1:
    print(ln)
print('SEG1 rc=%d' % rc1)

seg2_files = [
    os.path.join(ROOT, 'src', 'os', 'state.json'),
    os.path.join(ROOT, 'docs', 'status-export.json'),
]
rc2, lines2 = close_commit.run_close_commit(
    seg2_files,
    "R2082 accounting: death-line watch round (closure criteria unmet comfy-active x mv-active; "
    "fire no-fire mv-active; AIHOT pause held; four checks exhausted) [via bm-a]",
    root=ROOT,
)
for ln in lines2:
    print(ln)
print('SEG2 rc=%d' % rc2)
print('R2082 close OK' if (rc1 == 0 and rc2 == 0) else 'R2082 close ISSUE rc1=%d rc2=%d' % (rc1, rc2))
