import re, io, json, os, time

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
os.chdir(ROOT)
out = []

# 1. latest order file + mtime
orders_dir = 'orders'
orders = sorted(os.listdir(orders_dir)) if os.path.isdir(orders_dir) else []
o_2026 = [f for f in orders if f.startswith('O-2026')]
latest = o_2026[-1] if o_2026 else 'NONE'
mt = time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(os.path.join(orders_dir, latest)))) if latest != 'NONE' else 'NA'
out.append('LATEST_ORDER %s mtime %s' % (latest, mt))

# 2. ledger target rows (strict @ patterns)
led_path = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
led_mt = time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(led_path)))
led = io.open(led_path, encoding='utf-8', errors='replace').read().splitlines()
tga = [x for x in led if re.search(r'@(BigStream|七线全司|全司|六司|八线)', x)]
out.append('LEDGER_MTIME %s' % led_mt)
out.append('LEDGER_TARGET_LINES %d' % len(tga))
with io.open('.c3-tmp/r1058_ledger_tail.txt', 'w', encoding='utf-8') as f:
    for x in tga[-2:]:
        f.write(x[:280] + '\n')

# 3. decisions dnum content-addressed diff
dec_path = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dec_mt = time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(dec_path)))
d = io.open(dec_path, encoding='utf-8', errors='replace').read()
nums = set(re.findall(r'D-20\d{6}-\d{2}|C-20\d{6}-\d{2}', d))
state = json.load(io.open('src/os/state.json', encoding='utf-8'))
w = set(state['decisions_watermark']['dnums'])
new = sorted(nums - w)
out.append('DECISIONS_MTIME %s' % dec_mt)
out.append('NEW_DNUMS %s' % new)
out.append('WATERMARK %d file_nums %d' % (len(w), len(nums)))

# 4. index.lock
out.append('INDEX_LOCK %s' % os.path.isfile('.git/index.lock'))

# 5. production self-heal
out.append('PRODUCTION %s tick %d' % (state.get('production'), state['tick']))

# 6. daily brief 10-03 present / 10-04 absent (day-boundary item)
out.append('DAILY_10_03 %s' % os.path.isfile('data/intel/daily/2026-10-03.md'))
out.append('DAILY_10_04 %s' % os.path.isfile('data/intel/daily/2026-10-04.md'))

# 7. W40 weekly audit
import glob as g
aud = g.glob('docs/audits/2026-W40*-self-audit.md') + g.glob('docs/audits/*40*self-audit*')
out.append('W40_AUDIT %s' % (len(aud) > 0))

# 8. OH w3 file (OSS window3 ledger)
out.append('OH_20261002 %s' % os.path.isfile(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\oss-harvest\OH-20261002-bigstream.md'))

# 9. CENSUS supply gate C-00030 anchor
out.append('CENSUS_C00030 %s' % os.path.isfile(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md'))

# 10. pools.json (BigLife #86 trigger face)
pj = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
if os.path.isfile(pj):
    out.append('POOLS_MTIME %s' % time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(pj))))

io.open('.c3-tmp/r1058_check.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
