# -*- coding: utf-8 -*-
# R539 close: story-walk verify -> state.json tick 538->539 + log append + ts/task refresh + status-export P-61 light refresh
# (mirror of r538_close.py; probe-copy law 52nd proof: r539_check.py copied from r538_all.py + forensics additions)
import json, io, os, time

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
SP = ROOT + r'\src\os\state.json'
SE = ROOT + r'\docs\status-export.json'
OUT = os.path.join(ROOT, '.c3-tmp')

R538_CLOSE = time.mktime(time.strptime('2026-09-27 17:53:09', '%Y-%m-%d %H:%M:%S'))

# --- pre-close verify: storylines three sublines zero new writes since R538 close ---
lines = []
newer = []
for sub in ['video', 'novel', 'audio', 'comic']:
    d = os.path.join(ROOT, 'data', 'storylines', sub)
    mx, mf = 0.0, None
    for dp, _, fs in os.walk(d):
        for f in fs:
            p = os.path.join(dp, f)
            t = os.path.getmtime(p)
            if t > mx:
                mx, mf = t, os.path.relpath(p, d)
    lines.append('%s tail=%s @%s' % (sub, mf, time.strftime('%m-%d %H:%M:%S', time.localtime(mx))))
    if mx > R538_CLOSE:
        newer.append(sub)
io.open(os.path.join(OUT, 'r539_story.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
assert not newer, 'STORY NEW WRITES AFTER R538 CLOSE: %s' % newer

hm = time.strftime('%H:%M')
ts_full = time.strftime('%Y-%m-%d %H:%M:%S')
export_iso = time.strftime('%Y-%m-%dT%H:%M:%S+08:00')

logline = (
 '2026-09-27 ' + hm + ' R539: idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·并窗轮 5/6 不 commit）——'
 '①无新令（orders 35 件零新增=r539_check·锚=O-20260927-1050-HQ-C mtime 13:53:11=R515 收行足迹·edited 检测行=锚件自身小数秒伪差〔R534 在案口径〕）'
 '+无新集团转办（ledger 五模式 unicode-escape 正法复计 31=锚零新行·r539_check 行数口径直计·ledger mtime 15:15:21 未动·内容寻址勿全文重读）'
 '+无新决策行（decisions UTF8 非空行 56=锚零新·mtime 15:14:19 未动）·production=open 自愈核在位零翻正（r539_check·STATE_PRODUCTION=open TICK=538）；'
 '②backlog 顶行不可认领（#75/#74/#71/#73/#79/#77/#64 done 维持·#78 SC-003-01 渲染腿素材面前置维持 blocked〔footage 顶=census-card-v7-vertical 09-27 12:32=R511 自产源件非 FluxVerse 实录·r539 到位核验零新实录=呈报状态行在案不催办〕'
 '·#59 REACT 09-28 热点窗届日即领〔daily_brief 09-28 缺=明届日随窗补产·今日 09-27 未届〕'
 '·#63 图鉴 C-00030/C-00031 锚正典位直查双 False〔20 锚尾三止 C-00029〕supply-gated 照守'
 '·#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕'
 '·#31 有声线 ch.5 v3 稿未落=会话创作腿 supply-gated 照守〔novel 尾 09-25 17:58 零新写盘=r539_story 复核〕'
 '·#57 替代率首报 10-07 挂账·W40 周自审 09-28 开周+月度统计注记首件 ≤09-30 随 W40 周审轮'
 '·#67 DIGEST 史源耗尽待 ledger 新 CEO 令级事件〔反膨胀律照守〕·#80 global-benchmarks 10-01 并窗'
 '·自进池 open 项全门控〔B5 账号期站内采样/B3 周更 W40/C4 首进链件触发位〕）；'
 '③树态=仅自产预期态（无 index.lock False 实证·M state.json+M status-export.json=R535~R538 idle-fast 自记账并窗预期态非 bm-a 迹象〔os-protocol §6·R538 收账完整性取证=r539_state_diff：tick538/log R538 行/ts·task/focus R539 全落位零断洞〕'
 '+untracked .sc003 两 tmp=SC-003 批次未闭预期态+.c3-tmp r535~r539 探针证据件随并窗批 commit〔R150 先例〕'
 '·HEAD=ddec465 R531-R534 窗 batch commit 未变 git log 零插队=无 bm-a 活跃写盘迹象〔storylines 三子域零新写盘=video 尾 12:49=R512 足迹〔r539_story 复核通过〕/novel·audio·comic 尾 09-25·backlog 14:35=R517·HQ-FEEDBACK 12:26=R511·station-reviews 14:35=R517·renders README 13:53=R515·finished 14:35=R517 足迹全未动〕）；'
 '④例行件：日报 09-27 在案不重跑（09-28 件=明届日随窗补产）·W39 周审在案（W40 明日 09-28 开周+月度统计注记首件 ≤09-30）'
 '·global-benchmarks day3 ≤7 跳过（下期 10-01=#80 并窗）·T1 催办=已裁项停用口径·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）'
 '·tokens:local=0（五查+三探针纯脚本零本地模型调用·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）；'
 '三探针定谳=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现 exit 1〔账号批次①+6/10 GATE+#17〕=阻塞≠失败口径'
 '/loop_health 2 FAIL+24 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min=R425 调度器漏触发同事件足迹 R426 已裁定不重复触发'
 '·FAIL② account-lag done539>tick538=本轮在飞 done-beat 先行于收账 tick 瞬态 +1〔R527-R532/R535-R538 同型·新断洞判据 lag ≥2 未破线·本轮收账 tick539 即平〕'
 '·24 WARN=13 log-order+11 heartbeat-gap 全 ≤09-27 13:55 史实零新增·backlog 80 项 66 done 82% 燃尽）'
 '——探针复制律第五十二证（r539_check.py=r538_all.py 复制+断洞取证扩腿〔state 尾三行/git diff/decisions mtime〕+OUTP 改指·零 PS 往返零历史件覆写=R462 防再犯律+R466 预核律双守）'
 '+随行操作红一笔如实入账=轮首 PS && 链 ParserError ×1〔R524/R536/R537/R538 在案同型·改 ; 即过·零盘面副作用〕；'
 '一行收账即出（idle-fast 并窗轮 5/6〔窗 R535-R540 满 6 收账→R540 batch commit·跨日边界 09-28 00:00 先到即收〕·本轮不 commit·P-61 导出步照刷 export_ts+工程技术部 s 面轻量）。'
 '下轮=R540 快速路径首查（#78 素材实录到位核验/REACT 09-28 热点窗届日领〔daily_brief 09-28 缺则先补产〕/W40 周自审开周+月度统计注记首件），全静即 idle-fast 6/6 窗满收账（batch commit R535-R540 含 .c3-tmp 探针证据件）。'
)

task60 = logline.split('R539: ', 1)[1][:60]

# --- state.json ---
st = json.load(io.open(SP, encoding='utf-8'))
assert st['tick'] == 538, 'tick unexpected: %s' % st['tick']
st['tick'] = 539
st['focus'] = ('R540: 快速路径首查（#78 素材实录到位核验/REACT 09-28 热点窗届日领〔daily_brief 09-28 缺则先补产〕'
               '/W40 周自审开周+月度统计注记首件 ≤09-30/新令/集团转办——ledger 五模式锚=31〔R534 修正定谳·探针 tag 匹配须 unicode-escape 禁中文字面量〕'
               '——全静即 idle-fast 并窗轮 6/6 窗满收账〔batch commit R535-R540 含 .c3-tmp 探针证据件·跨日边界 09-28 00:00 先到即日界收账·窗满/跨日任一先至即 batch commit〕）')
st['log'].append(logline)
st['ts'] = ts_full
st['task'] = task60
io.open(SP, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=1) + '\n')

# --- status-export.json (P-61 light refresh per R535-R538 precedent: export_ts + engineering dept s) ---
se = json.load(io.open(SE, encoding='utf-8'))
se['export_ts'] = export_iso
for d in se['depts']:
    if d['n'] == '工程技术部':
        d['s'] = ('R539: idle-fast (fast path, five checks quiet + probes adjudicated green, no four-step entry) - '
                  'orders 35 files anchor O-20260927-1050 mtime 13:53:11 unchanged (edited-detection self-hit = known sub-second artifact per R534 canon); '
                  'ledger five-mode unicode-escape recount 31 = R534 corrected anchor, zero new rows (ledger mtime 15:15:21 unchanged); decisions 56 = anchor (mtime 15:14:19 unchanged); production=open intact; '
                  'backlog top gated (#78 FluxVerse footage still absent: footage top census-card-v7-vertical 09-27 12:32 = R511 self-produced, status-line in place, no nagging; '
                  '#59 REACT due 09-28 with daily_brief 09-28 to be produced on window day; #63 C-00030/31 anchors not in place supply-gated; #70 OSS 09-29; '
                  '#31 ch.5 v3 pending session leg; #57 10-07; W40 weekly audit opens 09-28 + monthly stats note <=09-30; #67 anti-bloat; #80 benchmarks 10-01); '
                  'tree = expected self state only (M state.json + M status-export.json = R535-R538 idle-fast self-accounting window-expected state, R538 close forensics via r539_state_diff = complete, no hole; '
                  'untracked .sc003 tmp batch-unclosed + .c3-tmp r535-r539 probe evidence for window batch commit, no index.lock, HEAD=ddec465 zero requeue = no bm-a activity: '
                  'storylines video tail 12:49=R512 (story-walk verified), novel/audio/comic 09-25, backlog 14:35=R517, HQ-FEEDBACK 12:26=R511, renders README 13:53=R515, finished 14:35=R517); '
                  'probes: board 0 FAIL (5 ideas 10 drafts 5 in production), readiness 3 external CEO blockers 0 findings (exit 1 = blockers-not-failures canon), '
                  'loop_health 2F+24W all in-case (outage 49min = R425 adjudicated footprint; account-lag done539>tick538 = in-flight done-beat transient +1, '
                  'lag>=2 hole threshold unbroken, closing tick539 balances); probe-copy law 52nd proof (r539_check.py from r538_all.py with forensics additions and OUTP rename, zero PS round-trip, '
                  'one in-case PS && ParserError at round start = R524/R536/R537/R538 known type, switched to ; with zero disk side-effect); '
                  'daily 09-27 in place, benchmarks day3 skip, tokens:local=0, publish lock unchanged (not live = not measured); '
                  'idle-fast window round 5/6, no commit (window R535-R540, cross-day boundary 09-28 00:00 first-arrival closes, window-full-6 closes)')
        break
io.open(SE, 'w', encoding='utf-8').write(json.dumps(se, ensure_ascii=False, indent=1) + '\n')

# --- verify ---
st2 = json.load(io.open(SP, encoding='utf-8'))
se2 = json.load(io.open(SE, encoding='utf-8'))
print('CLOSE_OK tick=%d log_tail_R=%s...' % (st2['tick'], st2['log'][-1][15:20]))
print('ts=%s task_len=%d task_head=%s' % (st2['ts'], len(st2['task']), st2['task'][:30]))
print('export_ts=%s' % (se2['export_ts'],))
for d in se2['depts']:
    if d['n'] == '工程技术部':
        print('eng_dept_found s_head=%s' % d['s'][:16])
