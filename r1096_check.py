import json, re, os, subprocess, glob

S = 'C:/Users/sjs20/Desktop/FluxGroup'
B = 'C:/Users/sjs20/Desktop/FluxGroup/media/BigStream'
out = []

st = json.load(open(B + '/src/os/state.json', encoding='utf-8'))
out.append('ts=%s' % st.get('ts'))
out.append('tick=%s' % st.get('tick'))
out.append('production=%s' % st.get('production'))
out.append('task=%s' % st.get('task'))
logs = st.get('log', [])
out.append('log_count=%d' % len(logs))
for l in logs[-3:]:
    out.append('LOG: ' + l)
wm = st.get('decisions_watermark', {})
if isinstance(wm, dict):
    out.append('wm_dnums_count=%d' % len(wm.get('dnums', [])))
else:
    out.append('wm=%r' % (wm,))

g = subprocess.run(['git', '-C', B, 'status', '--short'], capture_output=True, text=True).stdout
out.append('--- git status ---')
out.append(g.strip() or '(clean)')
out.append('index_lock=%s' % os.path.exists(B + '/.git/index.lock'))

files = sorted(glob.glob(B + '/orders/*.md'), key=os.path.getmtime)
out.append('--- local orders latest 3 ---')
for f in files[-3:]:
    out.append(os.path.basename(f))

led = open(S + '/cph4/evolution-ledger.md', encoding='utf-8').read()
rows = [ln for ln in led.splitlines() if re.search(r'@(BigStream|七线全司|全司|六司|八线)', ln)]
pnums = set()
for ln in rows:
    pnums.update(re.findall(r'P-\d{8}-\d+', ln))
out.append('--- ledger rows: %d ---' % len(rows))
out.append('ledger_pnums=' + ','.join(sorted(pnums)))
for ln in rows[-4:]:
    out.append('LED: ' + ln[:180])

dec = open(S + '/docs/decisions.md', encoding='utf-8').read()
dnums = set(re.findall(r'[DC]-\d{8}-\d+', dec))
out.append('--- decisions dnums: %d ---' % len(dnums))
out.append('dec_dnums=' + ','.join(sorted(dnums)))
m = re.search(r'派工通告板(.*?)(\n#{1,3} |\Z)', dec, re.S)
if m:
    lines = [l for l in m.group(1).splitlines() if l.strip()]
    out.append('--- board nonempty lines: %d (last 5) ---' % len(lines))
    for l in lines[-5:]:
        out.append('BRD: ' + l[:180])

# group orders.md + ledger + decisions mtimes (fresh-change detection)
for p in ['/docs/orders.md', '/cph4/evolution-ledger.md', '/docs/decisions.md']:
    fp = S + p
    out.append('mtime %s = %s' % (p, os.path.getmtime(fp)))

open(B + '/.c3-tmp/r1096_check.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('OK rows=%d dnums=%d' % (len(rows), len(dnums)))
