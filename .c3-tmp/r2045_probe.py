# r2040 round-opener probe (bm-a host: direct read of group ledgers, zero git ops on group tree)
import json, io, os, re, datetime

OUT = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r2040_probe.txt'), 'w', encoding='utf-8')

def w(s):
    OUT.write(unicode(s) if isinstance(s, str) else s)

def wl(s):
    OUT.write(s + '\n')

now = datetime.datetime.now()
wl('now=%s' % now.strftime('%Y-%m-%d %H:%M:%S'))

# 1. state.json tail
d = json.load(open('src/os/state.json', encoding='utf-8'))
wl('=== STATE ===')
wl('tick=%s' % d.get('tick'))
wl('ts=%s' % d.get('ts'))
wl('task=%s' % str(d.get('task'))[:150])
wl('production=%s' % d.get('production'))
dw = d.get('decisions_watermark') or {}
dnums = dw.get('dnums') or []
wl('dnums_count=%d' % len(dnums))
wl('dnums_tail=%s' % (dnums[-10:] if dnums else []))
lg = d.get('log') or []
wl('log_len=%d' % len(lg))
wl('--- log tail 3 ---')
for line in lg[-3:]:
    wl(line[:700])
    wl('---')
wl('--- end tail ---')

# 2. decisions.md content-addressed diff
dec = open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', encoding='utf-8', errors='replace').read()
nums = sorted(set(re.findall(r'[DC]-\d{8}-\d{2}', dec)))
new_nums = [n for n in nums if n not in dnums]
wl('=== DECISIONS ===')
wl('dec_total=%d new_count=%d' % (len(nums), len(new_nums)))
wl('new_nums=%s' % new_nums[:60])
# dispatch board top lines (派工通告板)
m = re.search(r'派工通告板(.*?)(##|\Z)', dec, re.S)
if m:
    wl('--- dispatch board tail ---')
    for l in m.group(1).splitlines()[-12:]:
        wl(l[:220])

# 3. evolution-ledger scan
led = open(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md', encoding='utf-8', errors='replace').read()
lines = led.splitlines()
hits = [l for l in lines if re.search(r'@BigStream|@七线全司|@全司|@六司|@八线', l)]
wl('=== LEDGER ===')
wl('ledger_at_hits=%d' % len(hits))
for l in hits[-6:]:
    wl(l[:220])

# 4. orders.md tail + mtime
omp = r'C:\Users\sjs20\Desktop\FluxGroup\docs\orders.md'
wl('=== ORDERS ===')
wl('orders_mtime=%s' % datetime.datetime.fromtimestamp(os.path.getmtime(omp)).strftime('%Y-%m-%d %H:%M:%S'))
om = open(omp, encoding='utf-8', errors='replace').read()
wl('orders_lines=%d' % len(om.splitlines()))
wl('--- orders tail 8 ---')
for l in om.splitlines()[-8:]:
    wl(l[:220])
OUT.close()
print('PROBE-OK')
