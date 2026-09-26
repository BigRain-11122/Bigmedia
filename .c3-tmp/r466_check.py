import os, json, subprocess, io, re, time
B = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
FG = r'C:\Users\sjs20\Desktop\FluxGroup'
rep = []
# 1. state head + last 3 log entries -> UTF-8 file (console-safe ASCII summary only)
sp = os.path.join(B, 'src', 'os', 'state.json')
d = json.load(open(sp, encoding='utf-8'))
out = []
for k in d:
    if k != 'log':
        out.append('%s: %s' % (k, json.dumps(d[k], ensure_ascii=False)))
log = d.get('log', [])
out.append('log_n=%d' % len(log))
out.append('=== LAST 3 LOG ENTRIES ===')
for e in log[-3:]:
    out.append(e if isinstance(e, str) else json.dumps(e, ensure_ascii=False))
io.open(os.path.join(B, '.c3-tmp', 'r466_state_tail.md'), 'w', encoding='utf-8').write('\n\n'.join(out))
rep.append('tick=%s ts=%s log_n=%d' % (d.get('tick'), d.get('ts'), len(log)))
# 2. orders latest (O- prefix files only, README.md sorting artifact excluded)
od = os.path.join(B, 'orders')
fs = [f for f in os.listdir(od) if f.startswith('O-') and f.endswith('.md')]
fs.sort()
rep.append('orders_n=%d last=%s' % (len(fs), fs[-1] if fs else 'NONE'))
# 3. ledger @-mention scan (five-pattern set incl @八线全量)
L = os.path.join(FG, 'cph4', 'evolution-ledger.md')
t = open(L, encoding='utf-8', errors='replace').read().splitlines()
pats = ('@BigStream', '@七线全司', '@全司', '@六司', '@八线全量')
sel = [l for l in t if any(p in l for p in pats)]
rep.append('ledger_at_n=%d' % len(sel))
# 4. decisions non-empty line count
D = os.path.join(FG, 'docs', 'decisions.md')
dl = open(D, encoding='utf-8', errors='replace').read().splitlines()
ne = [l for l in dl if l.strip()]
rep.append('decisions_nonempty=%d' % len(ne))
# 5. BigLife census anchors (CENSUS supply gate: C-00030)
A = os.path.join(FG, 'life', 'BigLife', 'census', 'anchors')
an = sorted(os.listdir(A)) if os.path.isdir(A) else []
rep.append('anchors_n=%d last3=%s' % (len(an), ' | '.join(an[-3:]) if an else 'NONE'))
rep.append('anchor_C00030=%s anchor_C00031=%s' % (os.path.exists(os.path.join(A, 'C-00030.md')), os.path.exists(os.path.join(A, 'C-00031.md'))))
# 6. git status + index.lock
g = subprocess.run(['git', '-C', B, 'status', '--short'], capture_output=True, text=True)
gl = g.stdout.splitlines()
rep.append('git_status_n=%d' % len(gl))
for l in gl:
    rep.append('  ' + l)
rep.append('index_lock=%s' % os.path.exists(os.path.join(B, '.git', 'index.lock')))
# 7. git log queue-jump check (no commits since R462 batch anchor)
lg = subprocess.run(['git', '-C', B, 'log', '--oneline', '-3'], capture_output=True, text=True)
rep.append('git_log_top3:')
for l in lg.stdout.splitlines():
    rep.append('  ' + l)
# 8. storylines subdomain writes today after last close (bm-a activity check)
cut = '2026-09-27 04:33:15'
cnt = {'novel': 0, 'audio': 0, 'comic': 0}
for sub in cnt:
    p = os.path.join(B, 'data', 'storylines', sub)
    if os.path.isdir(p):
        for root, _, fns in os.walk(p):
            for fn in fns:
                fp = os.path.join(root, fn)
                mt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(fp)))
                if mt > cut:
                    cnt[sub] += 1
rep.append('storylines_new_writes_after_last_close=%s' % json.dumps(cnt))
# 9. daily brief today + tomorrow
rep.append('daily_brief_0927=%s daily_brief_0928=%s' % (os.path.exists(os.path.join(B, 'data', 'intel', 'daily', '2026-09-27.md')), os.path.exists(os.path.join(B, 'data', 'intel', 'daily', '2026-09-28.md'))))
# 10. W39/W40 audits + monthly stats note
rep.append('audit_W39=%s audit_W40=%s' % (os.path.exists(os.path.join(B, 'docs', 'audits', '2026-W39-self-audit.md')), os.path.exists(os.path.join(B, 'docs', 'audits', '2026-W40-self-audit.md'))))
# 11. global-benchmarks refresh dates
gb = os.path.join(B, 'docs', 'global-benchmarks.md')
if os.path.exists(gb):
    m = re.findall(r'2026-\d\d-\d\d', open(gb, encoding='utf-8', errors='replace').read())
    rep.append('gb_date_first=%s last=%s' % (m[0] if m else '?', m[-1] if m else '?'))
# 12. now
r = subprocess.run(['powershell', '-NoProfile', '-Command', 'Get-Date -Format yyyy-MM-dd_HH:mm:ss'], capture_output=True, text=True)
rep.append('now=' + r.stdout.strip())
print('\n'.join(rep))
