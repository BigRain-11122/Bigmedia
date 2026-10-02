import json, re, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
GRP  = r"C:\Users\sjs20\Desktop\FluxGroup"
o = []

def rd(p):
    return open(p, encoding='utf-8', errors='replace').read()

st = json.load(open(os.path.join(ROOT,'src','os','state.json'), encoding='utf-8'))
o.append('tick=%s ts=%s' % (st.get('tick'), st.get('ts')))
o.append('task=%s' % st.get('task'))
o.append('production=%s' % st.get('production'))
log = st.get('log', [])
o.append('log_len=%d' % len(log))
for l in log[-5:]:
    o.append('LOG|' + l)

wm = st.get('decisions_watermark', {}) or {}
dn = wm.get('dnums', []) or []
o.append('wm_dnums_count=%d tail=%s' % (len(dn), ','.join(dn[-12:])))

o.append('index_lock=%s' % os.path.exists(os.path.join(ROOT,'.git','index.lock')))
o.append('round_lock=%s' % os.path.exists(os.path.join(ROOT,'logs','iteration-loop','round.lock')))

led = rd(os.path.join(GRP,'cph4','evolution-ledger.md')).splitlines()
pref = [(i+1, l) for i, l in enumerate(led) if re.match(r'@[A-Za-z\u4e00-\u9fff]', l)]
o.append('ledger_at_prefix_count=%d' % len(pref))
for n, l in pref[-4:]:
    o.append('LED|%d|%s' % (n, l[:240]))

dec = rd(os.path.join(GRP,'docs','decisions.md'))
dset = set(re.findall(r'[DC]-\d{8}-\d{2}', dec))
new = sorted(dset - set(dn))
o.append('decisions_total=%d new_vs_wm=%s' % (len(dset), ','.join(new) if new else 'NONE'))
dl = dec.splitlines()
for i, l in enumerate(dl):
    if '派工通告板' in l:
        for l2 in dl[i:i+60]:
            if ('BigStream' in l2) or ('七司' in l2) or ('全司' in l2) or ('六司' in l2):
                o.append('BOARD|' + l2[:260])
        break

god = rd(os.path.join(GRP,'docs','orders.md'))
gol = god.splitlines()
phys = [l for l in gol if ('BigStream' in l) or ('物理件' in l)]
for l in phys[-6:]:
    o.append('GORDER|' + l[:240])

od = os.path.join(ROOT,'orders')
o.append('orders_files=' + ','.join(sorted(os.listdir(od))[-12:]))

bl = rd(os.path.join(ROOT,'src','os','backlog.md')).splitlines()
o.append('backlog_lines=%d' % len(bl))
seen = 0
for i, l in enumerate(bl):
    if re.match(r'^\d+\.\s', l):
        if '[done' not in l:
            o.append('UNFIN|%d|%s' % (i+1, l[:240]))
            seen += 1
            if seen >= 12:
                break

fin = rd(os.path.join(ROOT,'output','finished.md')).splitlines()
o.append('finished_lines=%d' % len(fin))
for l in fin[-4:]:
    o.append('FIN|' + l[:240])

q = rd(os.path.join(ROOT,'docs','self-improvement-queue.md')).splitlines()
o.append('queue_lines=%d' % len(q))
for l in q[-26:]:
    o.append('Q|' + l[:200])

try:
    se = json.load(open(os.path.join(ROOT,'docs','status-export.json'), encoding='utf-8'))
    o.append('export_ts=%s' % se.get('export_ts'))
except Exception as e:
    o.append('export_ts_read_err=%s' % e)

open(os.path.join(ROOT,'.c3-tmp','fastcheck_out.txt'), 'w', encoding='utf-8').write('\n'.join(o))
print('DONE rows=%d' % len(o))
