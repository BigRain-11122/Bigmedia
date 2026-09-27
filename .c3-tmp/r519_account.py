# -*- coding: utf-8 -*-
# R519 idle-fast accounting: state.json (tick 518->519, log append, ts/task refresh, focus->R520 pointer 2/6) + status-export.json (P-61: export_ts + eng dept + outs/results tick faces); json.load/dump full rewrite (R504 canonical)
import io, json, time, subprocess

REPO = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
now = time.strftime('%Y-%m-%d %H:%M:%S')
stamp = time.strftime('%Y-%m-%d %H:%M')
ts_iso = time.strftime('%Y-%m-%dT%H:%M:%S+08:00')

body = (
    u'idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·并窗轮 1/6 不 commit）——'
    u'①无新令（orders 双 NONE=r519_check·锚=O-20260927-1050 mtime 13:53:11=R515 收行足迹·O- 35 件零新增零编辑）'
    u'+无新集团转办（ledger 五模式正典行数口径 31=锚零新行·r519_check 行数口径直计·内容寻址勿全文重读）'
    u'+无新决策行（decisions UTF8 非空行 56=锚·R511 决策批 11 行收讫后零新）·production=open 自愈核=在位零翻正（r519_check）；'
    u'②backlog 顶行不可认领（#75/#74/#71/#73/#79/#77/#64 done·#78 SC-003-01 渲染腿素材面前置维持 blocked'
    u'〔footage 顶=census-card-v7-vertical 12:32=R511 自产源件非 FluxVerse 实录·呈报状态行在案不催办〕'
    u'·#59 REACT 09-27 窗已毕〔R456 F-045〕09-28 窗届日即领〔daily_brief 09-28 缺则先补产〕'
    u'·#63 图鉴 C-00030/C-00031 锚正典位轮首核均不在位〔r519_check anchor False 双证·BigLife census/anchors 20 件尾三止 C-00029〕supply-gated 维持'
    u'·#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕'
    u'·#31 有声线 ch.5 v3 稿未落=会话创作腿 supply-gated 照守〔稿落即认领〕'
    u'·#57 替代率首报 10-07 挂账·W40 周自审 09-28 开周+月度统计注记首件 ≤09-30 随 W40 周审轮'
    u'·#67 DIGEST 史源耗尽待 ledger 新 CEO 令级事件〔反膨胀律照守〕·#80 global-benchmarks 10-01 并窗'
    u'·自进池 open 项全门控〔B5 账号期站内采样/B3 周更 W40/C4 首进链件触发位〕）；'
    u'③树态=仅自产预期件（无 index.lock False 实证·开轮 git status 零 M 行=HEAD=5b8e3e0 R518 实活轮 commit+push 后净态 git log 零插队=无 bm-a 活跃写盘迹象'
    u'·untracked .sc003 两 tmp=SC-003 批次未闭预期态+.c3-tmp r519 探针证据件随并窗批 commit〔R150 先例〕'
    u'·storylines 三子域 R518 收账后零新写盘〔novel/audio/comic 尾 09-25·video 尾 12:49=R512 自记账足迹〕=r519_check'
    u'·state mtime 14:36=R518 自记账足迹〔ts 14:36:44 一致〕）；'
    u'④例行件：日报 09-27 在案不重跑（R443 补产件·09-28 件=明届日随窗补产）·W39 周审在案（W40 明日 09-28 开周）'
    u'·global-benchmarks day3 ≤7 跳过（下期 10-01=#80 并窗）·T1 催办=已裁项停用口径'
    u'·当日无集团层面新 open 问题=HQ-FEEDBACK 不写（零膨胀·mtime 12:26=R511 F-20260927-05 回执行未动）'
    u'·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）；'
    u'三探针定谳=board 0 FAIL（5 题 10 稿·5 in production·exit 0）'
    u'/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1〔账号批次①+6/10 GATE+#17〕'
    u'/loop_health 2 FAIL+24 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min=R425 调度器漏触发同事件足迹 R426 已裁定不重复触发'
    u'·FAIL② account-lag done519>tick518=本轮在飞 done-beat 先行于收账 tick 瞬态 +1〔03-26 中断执行体恒态基线·R459/R462 在案·新断洞判据 lag ≥2 未破线·本轮收账 tick519 即平〕'
    u'·24 WARN=14 log-order+10 heartbeat-gap 全 ≤09-27 13:55 史实零新增·backlog 80 项 66 done 82% 燃尽）'
    u'——探针复制律第四十证（r519_check.py/r519_probes.py=write_file 新建+OUTP 改指·零 PS 往返零历史件覆写=R462 防再犯律+R466 write_file 预核 tracked 态律双守·本轮零操作红）；'
    u'一行收账即出（idle-fast 并窗轮 1/6〔窗 R519-R524 满 6 收账→R524 batch commit·跨日边界 09-28 00:00 先到即收〕'
    u'·本轮不 commit·P-61 导出步照刷 export_ts+机读 tick 面对齐）。'
    u'下轮=R520 快速路径首查（#78 素材实录到位核验/REACT 09-28 热点窗届日领〔daily_brief 09-28 缺则先补产〕'
    u'/W40 周自审开周+月度统计注记首件/新令/集团转办——全静即 idle-fast（并窗轮 2/6）。'
)
log_line = u'%s R519: %s' % (stamp, body)
task = body[:60]
focus_next = (
    u'R520: 快速路径首查（#78 素材实录到位核验/REACT 09-28 热点窗届日领〔daily_brief 09-28 缺则先补产〕'
    u'/W40 周自审开周+月度统计注记首件/新令/集团转办——全静即 idle-fast'
    u'（并窗轮 2/6·窗 R519-R524 满 6 收账→R524 batch commit·跨日边界 09-28 00:00 先到即收）'
)

# ---------- state.json ----------
sp = REPO + r'\src\os\state.json'
st = json.load(io.open(sp, encoding='utf-8'))
assert st['tick'] == 518, 'tick drift: %s' % st['tick']
assert st['production'] == 'open', 'production not open: %s' % st['production']
assert st['ts'] == '2026-09-27 14:36:44', 'ts drift: %s' % st['ts']
assert st['log'][-1].startswith('2026-09-27 14:36 R518:'), 'log tail drift: %s' % st['log'][-1][:40]
assert st['focus'].startswith('2026-09-27 14:36 R518:'), 'focus drift: %s' % st['focus'][:40]
st['tick'] = 519
st['focus'] = focus_next
st['log'].append(log_line)
st['ts'] = now
st['task'] = task
io.open(sp, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=1))
chk = json.load(io.open(sp, encoding='utf-8'))
assert chk['tick'] == 519 and chk['ts'] == now and chk['task'] == task and len(task) == 60
assert chk['log'][-1].startswith(stamp + ' R519:') and chk['focus'].startswith('R520:')
print('state OK tick=519 ts=%s task_len=%d focus=R520 2/6' % (now, len(task)))

# ---------- status-export.json ----------
xp = REPO + r'\docs\status-export.json'
ex = json.load(io.open(xp, encoding='utf-8'))
ex['export_ts'] = ts_iso
eng = (
    "R519: idle-fast (fast path - five quiet checks + probes adjudicated green, no four-step entry, batching window 1/6 "
    "no commit) - five quiet: no new order (orders 35 O-files, top O-1050 mtime 13:53:11 unchanged, "
    "edited-since-anchor NONE), no new group transfer (ledger five-pattern 31 = anchor), no new decision row "
    "(decisions non-empty 56 = anchor), production=open self-heal verified, tree clean no lock (HEAD=5b8e3e0 R518 "
    "commit+push, zero M-lines, untracked .sc003 tmp = SC-003 unclosed-batch expected state, .c3-tmp r519 probe "
    "evidence batched per R150 precedent); backlog top not claimable (#78 render leg blocked on FluxVerse "
    "live-capture not arrived, #63 C-00030/31 supply-gated, #59 REACT 09-28 window not due, #70 OSS next window "
    "09-29 21:40, #31 ch.5 v3 draft = session-side supply gate, W40 weekly audit opens 09-28, #80 benchmarks "
    "10-01); probes: board 0 FAIL / readiness 3 external blockers 0 findings (exit 1 = blockers-not-failures "
    "canon) / loop_health 2F+24W all in-case (49min=R425 adjudicated; account-lag +1 in-flight transient, tick519 "
    "levels); routine: daily 09-27 in place, benchmarks day3 <=7 skip, no HQ-FEEDBACK write (zero bloat), "
    "tokens:local=0, publish lock unchanged (not live = not measured). Next R520: fast-path first (footage check "
    "/ REACT 09-28 window / W40 weekly audit + monthly stats note) - all quiet = idle-fast 2/6."
)
for d in ex['depts']:
    if d.get('n') == u'工程技术部':
        d['s'] = eng
ex['outs'][0] = [
    u'OS 循环',
    u'tick 519：R519（idle-fast 空转快速路径轮·五静+探针定谳绿·零生产件·并窗轮 1/6 不 commit）——'
    u'①无新令（orders 顶=O-20260927-1050 零新增零编辑·O- 35 件·orders_edited_since_anchor NONE）'
    u'+无新集团转办（ledger 五模式正典行数口径 31=锚）+无新决策行（decisions UTF8 非空行 56=锚）'
    u'+production=open 在位零翻正；'
    u'②backlog 顶行不可认领（#78 SC-003-01 渲染腿维持素材面前置 blocked〔FluxVerse 实录未到位不催办〕'
    u'·#59 REACT 09-28 窗届日领〔daily_brief 09-28 缺则先补产〕·#63 C-00030/31 锚不在位 supply-gated 照守〔anchors 尾三止 C-00029〕'
    u'·#70 OH 下窗 09-29 21:40·#31 有声线 ch.5 v3 稿未落=会话创作腿 supply-gated·#57 替代率 10-07'
    u'·W40 周自审 09-28 开周+月度统计注记 ≤09-30·#67 史源耗尽反膨胀律照守·自进池 open 全门控）；'
    u'③树态=仅自产预期态（HEAD=5b8e3e0 R518 实活轮 commit+push 后零插队·storylines R518 后零写盘=无 bm-a 迹象·无 index.lock）；'
    u'④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现'
    u'/loop_health 2 FAIL+24 WARN 全定谳在案类零新增（49min 停跳=R425 足迹 R426 已裁定·account-lag +1=在飞瞬态·lag ≥2 未破线）；'
    u'例行件照旧（日报 09-27 在案·global-benchmarks day3 ≤7 跳过）·tokens:local=0'
    u'·发布锁=M5 账号物理件不变（未上线=未测量）'
]
res_row = [
    u'519',
    u'R519 idle-fast 空转快速路径轮：五静（ledger 31=锚/orders 35 件零新增零编辑/decisions 56=锚）'
    u'+三探针定谳绿（board 0 FAIL·readiness 3 皆外部 0 发现·loop_health 2 FAIL+24 WARN 皆在案类零新增）'
    u'·零生产件（backlog 各窗未到全门控·#78 blocked/#63/#31 supply-gated/#59 09-28 届日/W40 周自审+月度注记 09-28 起）'
    u'·idle-fast 并窗轮 1/6 不 commit（窗 R519-R524 满 6 收账→R524 batch commit·跨日 09-28 00:00 先到即收）'
]
ex['results'] = [res_row] + [r for r in ex['results'] if r[0] != u'519'][:6]
io.open(xp, 'w', encoding='utf-8').write(json.dumps(ex, ensure_ascii=False, indent=1))
chk2 = json.load(io.open(xp, encoding='utf-8'))
assert chk2['export_ts'] == ts_iso
assert chk2['outs'][0][1].startswith(u'tick 519：R519')
assert chk2['results'][0][0] == u'519' and chk2['results'][0][1].startswith(u'R519 idle-fast')
assert [r[0] for r in chk2['results']] == [u'519', u'518', u'517', u'516', u'515', u'514', u'35']
print('export OK ts=%s results_top=%s' % (ts_iso, [r[0] for r in chk2['results']][:7]))

# ---------- final verify: git status snapshot ----------
p = subprocess.run(['git', 'status', '--short'], cwd=REPO, capture_output=True, text=True, encoding='utf-8', errors='replace')
lines = [ln for ln in (p.stdout or '').splitlines() if ln.strip()]
m_lines = [ln for ln in lines if ln.startswith('M ') or ln.startswith(' M')]
print('git status lines=%d M-lines=%d' % (len(lines), len(m_lines)))
for ln in m_lines:
    print('  ' + ln)
