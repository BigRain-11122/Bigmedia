import os, json, subprocess, io, time
B = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
FG = r'C:\Users\sjs20\Desktop\FluxGroup'
rep = []
# 0. state.json production gate (self-heal check per task briefing)
d = json.load(io.open(os.path.join(B, 'src', 'os', 'state.json'), encoding='utf-8'))
rep.append('production=%s tick=%d' % (d.get('production'), d.get('tick')))
# 1. orders latest + edited since anchor (D-20260927-05 item-2 line)
od = os.path.join(B, 'orders')
fs = [f for f in os.listdir(od) if f.startswith('O-') and f.endswith('.md')]
fs.sort()
anchor = os.path.join(od, 'O-20260925-1931-HQ-C.md')
am = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(anchor))) if os.path.exists(anchor) else 'MISSING'
edited = [f for f in fs if os.path.getmtime(os.path.join(od, f)) > os.path.getmtime(anchor)] if os.path.exists(anchor) else []
rep.append('orders_n=%d last=%s' % (len(fs), fs[-1] if fs else 'NONE'))
rep.append('orders_anchor_mtime=%s edited_since_anchor=%s' % (am, edited if edited else 'NONE'))
# 2. ledger five-pattern @ scan (strict prefix set incl @八线全量)
L = os.path.join(FG, 'cph4', 'evolution-ledger.md')
t = open(L, encoding='utf-8', errors='replace').read().splitlines()
pats = ('@BigStream', '@七线全司', '@全司', '@六司', '@八线全量')
sel = [l for l in t if any(p in l for p in pats)]
rep.append('ledger_at_n=%d' % len(sel))
io.open(os.path.join(B, '.c3-tmp', 'r473_ledger_tail.txt'), 'w', encoding='utf-8').write('\n'.join(sel[-5:]))
# 3. decisions non-empty lines (UTF-8 anchor 45)
D = os.path.join(FG, 'docs', 'decisions.md')
dl = open(D, encoding='utf-8', errors='replace').read().splitlines()
ne = [l for l in dl if l.strip()]
rep.append('decisions_nonempty=%d' % len(ne))
# 4. BigLife census anchors (CENSUS supply gate C-00030/C-00031)
A = os.path.join(FG, 'life', 'BigLife', 'census', 'anchors')
an = sorted(os.listdir(A)) if os.path.isdir(A) else []
rep.append('anchors_n=%d last3=%s' % (len(an), ' | '.join(an[-3:]) if an else 'NONE'))
rep.append('anchor_C00030=%s anchor_C00031=%s' % (os.path.exists(os.path.join(A, 'C-00030.md')), os.path.exists(os.path.join(A, 'C-00031.md'))))
# 5. index.lock + git status + git log top (queue-jump check vs 161ad91 R468 batch)
rep.append('index_lock=%s' % os.path.exists(os.path.join(B, '.git', 'index.lock')))
g = subprocess.run(['git', '-C', B, 'status', '--short'], capture_output=True, text=True)
gl = g.stdout.splitlines()
rep.append('git_status_n=%d' % len(gl))
for l in gl:
    rep.append('  ' + l.encode('ascii', 'replace').decode())
lg = subprocess.run(['git', '-C', B, 'log', '--oneline', '-2'], capture_output=True, text=True)
rep.append('git_log_top:')
for l in lg.stdout.splitlines():
    rep.append('  ' + l)
# 6. storylines subdomain writes after R472 close 05:43 (bm-a activity check)
cut = '2026-09-27 05:43:00'
cnt = {'novel': 0, 'audio': 0, 'comic': 0}
for sub in cnt:
    p = os.path.join(B, 'data', 'storylines', sub)
    if os.path.isdir(p):
        for root, _, fns in os.walk(p):
            for fn in fns:
                mt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(os.path.join(root, fn))))
                if mt > cut:
                    cnt[sub] += 1
rep.append('storylines_new_writes_after_0543=%s' % json.dumps(cnt))
# 7. routine items: daily brief 09-27/09-28 / W39+W40 audit / monthly stats note
rep.append('daily_brief_0927=%s daily_brief_0928=%s' % (os.path.exists(os.path.join(B, 'data', 'intel', 'daily', '2026-09-27.md')), os.path.exists(os.path.join(B, 'data', 'intel', 'daily', '2026-09-28.md'))))
rep.append('audit_W39=%s audit_W40=%s' % (os.path.exists(os.path.join(B, 'docs', 'audits', '2026-W39-self-audit.md')), os.path.exists(os.path.join(B, 'docs', 'audits', '2026-W40-self-audit.md'))))
ms = [f for f in os.listdir(os.path.join(B, 'docs', 'research')) if f.startswith('R-202609') and 'monthly' in f.lower()] if os.path.isdir(os.path.join(B, 'docs', 'research')) else []
rep.append('monthly_stats_note=%s' % (ms if ms else 'NONE_due_0930'))
# 8. OH harvest next-window gate (09-29 21:40)
rep.append('oh_next_window_opens=2026-09-29_21:40 not_yet_due')
r = subprocess.run(['powershell', '-NoProfile', '-Command', 'Get-Date -Format yyyy-MM-dd_HH:mm:ss'], capture_output=True, text=True)
rep.append('now=' + r.stdout.strip())
print('\n'.join(rep))
