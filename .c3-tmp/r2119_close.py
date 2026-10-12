# -*- coding: utf-8 -*-
"""R2119 close: honest evidence fix + queue seed + main#12 note + state.json account + git."""
import io, os, sys, json, subprocess, datetime

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
GIT = r'C:\Program Files\Git\cmd\git.exe'

# ---------- 1. honest evidence file (corrected point 3) ----------
EV = os.path.join(ROOT, '.c3-tmp', 'r2119_supply_check.txt')
with io.open(EV, 'w', encoding='utf-8') as f:
    f.write('R2119 supply-gate + queue-health recheck evidence (2026-10-13 06:3x-07:0x)\n')
    f.write('1) BigLife tai-ci pool unlock gate (R1848 one-command recheck, first since 10-10 R1848):\n')
    f.write('   worktree unique strings = 1440 ; HEAD:cognition/pools.json unique = 1440 ; new-vs-HEAD = 0\n')
    f.write('   gate (unique>1440 OR row-diff non-empty) = LOCKED -> main#12 gated stance holds, recheck note appended, next >= 10-17\n')
    f.write('2) QUOTE supply (BigLife docs/CODEX.md sec.8 six-axis creed table):\n')
    f.write('   rows = 6, all consumed by QUOTE-v1..v6 (F-013..F-018) -> QUOTE supply exhausted, zero-action honest note\n')
    f.write('3) queue done-marker re-verify verdict: NO bookkeeping debt.\n')
    f.write('   full-line regex finds done-marks in place: tech#26 [done R2005] / #31 [done R1839] / #84 [done R1936] /\n')
    f.write('   #114 [done R2006] / #129 [done R2051] / #135 [done R2116] / #42 gate-note (R1951 W3 precondition closed).\n')
    f.write('   R2119 initial misread (280-char truncated view judged them undelivered) -> r2119_backfill.py fail-closed\n')
    f.write('   ANCHOR-MISS exit prevented a wrong write; 6 verify probes = the repeat-scan tax that seeds tech#145.\n')
    f.write('4) fire_consume routine: no-fire rc1 reason=cold-skip-no-admissible-credit;load-class-starved\n')
    f.write('   (F-180..183 four fire-ready items held; MV deadline-window yield = correct side)\n')
    f.write('5) five-checks quiet: origin_gap QUIET (ahead0 behind0); group_scan six faces fresh 06:39\n')
    f.write('   (DECISIONS truly_new=0 watermark=154; LEDGER @BigStream 5==anchor, @liu-si line = P-2026-10-09-01 historical;\n')
    f.write('    ORDERS 341 tail 10-13 04:3x==stored; ORIGIN-DELTA 0). Probes in-band: loop_health 3F/284W all adjudicated\n')
    f.write('   historical; readiness 3 blockers external CEO-side + render-unannot react-v16 expected in-chain red.\n')

# ---------- 2. queue seed (tech#145) + main#12 recheck note ----------
TECH = os.path.join(ROOT, 'state', 'queue', 'tech.md')
MAIN = os.path.join(ROOT, 'state', 'queue', 'main.md')

SEED145 = ('145. [R2119 补货·本轮真发现种子] 队列面消费紧凑读数器（缺口锚=R2119 实录：三队消费需全文件 dump'
           '〔tech.md 175 行×长行 ~1700 字·本轮 3 次全读〕+done 判定被 280 字符截断视图误判→6 次重扫探针税'
           '——队列行=单行长文形态·fast-path 消费面无紧凑摘要器）——候选=`src/os/queue_status.py` 一键读数器'
           '（三队 done/gated/可领计数+可领队头一行+按号全行正则 done 判定〔R2119 fail-closed 实证正法〕·输出 ≤15 行）'
           '——判据=轮首 P2/P3 消费面 token 降（对照本轮 3 dump 实耗）+零全文件读+done 判定零误报·判负留痕合法）'
           '——CPU 面可即领·随轮领\n')

with io.open(TECH, encoding='utf-8') as f:
    tech = f.read()
if '145. [R2119' in tech:
    print('seed145 already present, skip')
else:
    if not tech.endswith('\n'):
        tech += '\n'
    tech += SEED145
    with io.open(TECH, 'w', encoding='utf-8', newline='') as f:
        f.write(tech)
    print('tech#145 seeded')

NOTE12 = (' ——**[R2119 复读 2026-10-13]**：gate locked 维持（worktree==HEAD==1440 unique·0 新行·R1848 判据族'
          '·证据 .c3-tmp/r2119_supply_check.txt）·下次复读 ≥10-17 或 BigLife 侧增量呈报')
with io.open(MAIN, encoding='utf-8') as f:
    lines = f.read().splitlines(True)
hit = False
for i, ln in enumerate(lines):
    if ln.lstrip().startswith('12. [R1848') and '[R2119 复读' not in ln:
        lines[i] = ln.rstrip('\r\n') + NOTE12 + '\n'
        hit = True
        break
if not hit:
    print('ANCHOR-MISS main#12'); sys.exit(1)
with io.open(MAIN, 'w', encoding='utf-8', newline='') as f:
    f.writelines(lines)
print('main#12 recheck note appended')

# ---------- 3. state.json account ----------
ST = os.path.join(ROOT, 'src', 'os', 'state.json')
with io.open(ST, encoding='utf-8') as f:
    d = json.load(f)
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
logline = ('2026-10-13 07:0x R2119: 死线窗值守轮·轻台账轮（三队盘点=可领面零·main#28/tech#42/explore#27 皆 gated 正确态·禁凑数执行）'
           '——①供给门双查 locked（BigLife 台词池 R1848 判据族复读 10-10 后首查：1440==HEAD==worktree·0 新行→main#12 gated 维持+复读注回写·下次 ≥10-17；'
           'QUOTE 供给=CODEX §八 六轴信条例全消费〔F-013~018〕零动作·证据 .c3-tmp/r2119_supply_check.txt）；'
           '②fire_consume 例行 no-fire rc1 reason=cold-skip-no-admissible-credit;load-class-starved（F-180~183 四件 fire-ready 结转·死线窗让路正确侧）；'
           '③队列健康复核=六项 done 标〔tech#26/31/84/114/129/135〕+tech#42 前置注全在位——本轮 280 字符截断视图误判「缺 done 标」→r2119_backfill.py fail-closed ANCHOR-MISS 防错写实证'
           '〔诚实勘正：零台账债·6 探针重扫税=读数手段问题〕→tech#145 队列紧凑读数器种子入队（缺口锚=本轮 3 次全队列 dump+6 探针 token 成本·三队补货步）；'
           '④五查静（own orders 锚 O-20261008-1105 维持+origin_gap QUIET ahead0 behind0+group_scan 六面 06:39 fresh：DECISIONS truly_new=0 水位 154+'
           'LEDGER @BigStream 5==锚〔@六司 1=P-2026-10-09-01 史行非新转办〕+ORDERS 341 tail 10-13 04:3x==stored+ORIGIN-DELTA 0）'
           '+三探针带内（loop_health 3F284W 皆在案史实/readiness 3 阻塞皆外部 CEO 面+render-unannot react-v16 在链预期红 F-183 登记即清/export 06:12 新鲜 <24h 不刷）；'
           '⑤MV-lane 熟悉脏面维持零接触（06:43 首装配 cron 已过窗→07:33 终版重装配→08:30 死线=MV sprint 会话在执）'
           '——下轮=08:30 main#27 死线收口判读三连（成片呈报核→撤 AIHOT pause 旗→worker-restart main#21→F-180 接力首试+tech#92 顺延窗重定+main#28 DIGEST-v20 解锁即领）。收账显式列文件 commit+push。')
d['tick'] = int(d.get('tick', 0)) + 1
d['ts'] = now
d['task'] = logline.split('R2119: ', 1)[1][:60]
d['focus'] = ('死线窗值守续（O-2305 成片死线 08:30·06:43 首装配已过窗→07:33 终版重装配=MV 会话 cron 在案·本循环零接触；'
              '08:30 后 main#27 收口判读三连：成片呈报核→撤 AIHOT pause 旗→worker-restart main#21→F-180~183 fire 接力序+tech#92 顺延窗重定'
              '+main#28 DIGEST-v20 CPU 预置腿解锁即领；台词池 gate locked 复读 ≥10-17〔R2119 注〕；tech#145 队列紧凑读数器=下窗 CPU 候选；'
              'watermark 154/341 tail 10-13 04:3x 静')
d.setdefault('log', []).append(logline)
with io.open(ST, 'w', encoding='utf-8', newline='') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('state.json: tick=%d ts=%s' % (d['tick'], now))

# ---------- 4. transient cleanup ----------
tp = os.path.join(ROOT, '.c3-tmp', 'r2119_tail.txt')
if os.path.exists(tp):
    os.remove(tp)
    print('transient r2119_tail.txt removed')

# ---------- 5. git add(pathspec) + commit + push ----------
FILES = [
    '.c3-tmp/r2119_supply_check.txt',
    '.c3-tmp/r2119_backfill.py',
    '.c3-tmp/r2119_close.py',
    'state/queue/tech.md',
    'state/queue/main.md',
    'src/os/state.json',
]
MSG = ('R2119 watch round: supply-gate recheck locked (pool 1440==HEAD 0 new rows; QUOTE 6-axis exhausted, zero-action), '
       'fire routine no-fire load-class-starved (F-180..183 held), queue-health reverify all done-marks in place '
       '(fail-closed script caught truncated-view false alarm), tech#145 compact queue readout seed + main#12 recheck note, '
       'ts/task/tick refresh [via bm-a]')
if len(MSG) > 500:
    print('commit msg too long'); sys.exit(1)
r = subprocess.run([GIT, 'add', '--'] + FILES, cwd=ROOT, capture_output=True)
if r.returncode != 0:
    print('ADD-FAIL', r.stderr.decode('utf-8', 'replace')); sys.exit(1)
print('git add ok')
r = subprocess.run([GIT, 'commit', '-m', MSG, '--'] + FILES, cwd=ROOT, capture_output=True)
out = (r.stdout + r.stderr).decode('utf-8', 'replace')
print(out.strip().splitlines()[-1] if out.strip() else 'commit silent')
if r.returncode != 0 and 'nothing to commit' in out:
    print('NOTHING-TO-COMMIT -> state files mismatch, abort'); sys.exit(1)
r = subprocess.run([GIT, 'push', 'origin'], cwd=ROOT, capture_output=True)
out = (r.stdout + r.stderr).decode('utf-8', 'replace')
pushed = ('..' in out and 'main -> main' in out) or ('Everything up-to-date' in out)
print('PUSH-OK' if pushed else ('PUSH-CHECK-NEEDED: ' + out.strip()[-200:]))
