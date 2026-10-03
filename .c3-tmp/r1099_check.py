import json, re, os, subprocess, glob, time

S = 'C:/Users/sjs20/Desktop/FluxGroup'
B = 'C:/Users/sjs20/Desktop/FluxGroup/media/BigStream'
out = []

st = json.load(open(B + '/src/os/state.json', encoding='utf-8'))
out.append('ts=%s' % st.get('ts'))
out.append('tick=%s' % st.get('tick'))
out.append('production=%s' % st.get('production'))
logs = st.get('log', [])
out.append('log_count=%d' % len(logs))
for l in logs[-2:]:
    out.append('LOG: ' + l[:200])
wm = st.get('decisions_watermark', {})
wm_set = set(wm.get('dnums', [])) if isinstance(wm, dict) else set()
out.append('wm_dnums_count=%d' % len(wm_set))

g = subprocess.run(['git', '-C', B, 'status', '--short'], capture_output=True, text=True).stdout
out.append('--- git status ---')
out.append(g.strip() or '(clean)')
out.append('index_lock=%s' % os.path.exists(B + '/.git/index.lock'))

files = sorted(glob.glob(B + '/orders/*.md'), key=os.path.getmtime)
out.append('--- local orders latest 2 ---')
for f in files[-2:]:
    out.append('%s mtime=%s' % (os.path.basename(f), time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(f)))))

# ledger rows (strict @-prefix multi-mode scan)
led = open(S + '/cph4/evolution-ledger.md', encoding='utf-8').read()
rows = [ln for ln in led.splitlines() if re.search(r'@(BigStream|七线全司|全司|六司|八线)', ln)]
pnums = set()
for ln in rows:
    pnums.update(re.findall(r'P-\d{8}-\d+', ln))
out.append('--- ledger rows: %d (baseline 41) ---' % len(rows))
out.append('ledger_pnums=%d' % len(pnums))

# decisions content-addressed set-diff (D-20260930-19 law; NN two-digit canon regex)
dec = open(S + '/docs/decisions.md', encoding='utf-8').read()
dnums = set(re.findall(r'[DC]-\d{8}-\d+', dec))
new_dnums = sorted(dnums - wm_set)
out.append('--- decisions dnums: %d (wm %d) ---' % (len(dnums), len(wm_set)))
out.append('TRUE_NEW_DNUMS=%s' % (new_dnums if new_dnums else 'EMPTY'))
m = re.search(r'派工通告板(.*?)(\n#{1,3} |\Z)', dec, re.S)
if m:
    lines = [l for l in m.group(1).splitlines() if l.strip()]
    bs = [l for l in lines if ('BigStream' in l or '七司' in l or '全司' in l)]
    out.append('--- board nonempty lines: %d, bs-relevant: %d ---' % (len(lines), len(bs)))

# group file mtimes (fresh-change detection)
for p in ['/docs/orders.md', '/cph4/evolution-ledger.md', '/docs/decisions.md']:
    fp = S + p
    out.append('mtime %s = %s' % (p, time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(fp)))))

# group orders.md: dated 10-02/10-03 lines tail
ords = open(S + '/docs/orders.md', encoding='utf-8').read()
olines = ords.splitlines()
dated = [(i + 1, ln) for i, ln in enumerate(olines) if re.search(r'2026-10-0[23]', ln)]
out.append('--- group orders.md 10-02/10-03 dated lines: %d ---' % len(dated))
for i, ln in dated[-4:]:
    out.append('OL%d: %s' % (i, ln[:170]))

# export freshness
try:
    ex = json.load(open(B + '/docs/status-export.json', encoding='utf-8'))
    ets = ex.get('export_ts', '')
    out.append('export_ts=%s' % ets)
except Exception as e:
    out.append('export_ts read error: %r' % e)

# daily briefs
out.append('daily_1003=%s daily_1004=%s' % (
    os.path.exists(B + '/data/intel/daily/2026-10-03.md'),
    os.path.exists(B + '/data/intel/daily/2026-10-04.md')))

# backlog / queue mtimes
for p in ['/src/os/backlog.md', '/docs/self-improvement-queue.md']:
    out.append('mtime %s = %s' % (p, time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(B + p)))))

# #86 three legs fresh machine check (correct cross-repo paths)
try:
    pool = json.load(open(S + '/life/BigLife/cognition/pools.json', encoding='utf-8'))
    total = 0
    axes = pool.get('axes', {})
    for axis, ax in axes.items():
        for bucket, items in ax.items():
            if isinstance(items, list):
                total += len(items)
    for bucket, items in pool.get('sprite', {}).items():
        if isinstance(items, list):
            total += len(items)
    out.append('pools TOTAL_CONTENT_ENTRIES=%d (baseline 1440)' % total)
except Exception as e:
    out.append('pools count error: %r' % e)
try:
    ic = open(S + '/life/BigLife/cognition/interchat-ledger.jsonl', encoding='utf-8').read()
    out.append('interchat rows=%d (baseline 22)' % len([l for l in ic.splitlines() if l.strip()]))
except Exception as e:
    out.append('interchat read err %r' % e)
try:
    cens = sorted(glob.glob(S + '/life/BigLife/census/anchors/C-*.md'))
    out.append('CENSUS anchors=%d (C-00030 gate: absent = closed)' % len(cens))
    if cens:
        out.append('last anchor=%s' % os.path.basename(cens[-1]))
except Exception as e:
    out.append('census glob err %r' % e)

open(B + '/.c3-tmp/r1099_check.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('CHECK rows=%d dnums=%d new=%d' % (len(rows), len(dnums), len(new_dnums)))

# three probes (must run every round)
for name, cmd, res in [
    ('board', ['python', B + '/src/board_check.py'], B + '/.c3-tmp/r1099_board.txt'),
    ('rd', ['python', B + '/src/readiness.py'], B + '/.c3-tmp/r1099_rd.txt'),
    ('loop', ['python', B + '/src/os/loop_health.py'], B + '/.c3-tmp/r1099_loop.txt'),
]:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    open(res, 'w', encoding='utf-8').write(r.stdout + ('\n[stderr]\n' + r.stderr if r.stderr.strip() else ''))
    tail = [l for l in r.stdout.splitlines() if ('FAIL' in l or 'PASS' in l or 'WARN' in l or '阻塞' in l)][-6:]
    print('PROBE %s rc=%s | %s' % (name, r.returncode, ' / '.join(tail[-3:])[:300]))
