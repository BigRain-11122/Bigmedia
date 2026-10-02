# -*- coding: utf-8 -*-
# R996 round-open five-check scan (r995_scan.py lineage, UTF-8 file output): orders anchor /
# ledger mtime+BS lines / decisions dnum content-addressed diff vs watermark / index.lock /
# production self-heal check / CENSUS anchor / 10-03 brief / OSS w3 file presence.
import re, os, json, datetime, io

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
os.chdir(ROOT)

out = []
st = json.load(open('src/os/state.json', encoding='utf-8'))
out.append('tick %s | production %s | ts %s' % (st['tick'], st.get('production'), st.get('ts')))
wm = st['decisions_watermark']['dnums']

p = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dec = open(p, encoding='utf-8').read()
cur = set(re.findall(r'[DC]-2026\d{4}-\d{2}', dec))
cur.discard('D-20260930-1')  # single-digit wildcard artifact (R962/R987 precedent)
out.append('decisions mtime %s' % datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%m-%d %H:%M:%S'))
new = sorted(cur - set(wm))
out.append('NEW DNUMS: %s | held: %d cur: %d' % (new if new else 'NONE', len(wm), len(cur)))

lp = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
led = open(lp, encoding='utf-8').read()
out.append('ledger mtime %s' % datetime.datetime.fromtimestamp(os.path.getmtime(lp)).strftime('%m-%d %H:%M:%S'))
lines = [l for l in led.splitlines() if ('@BigStream' in l or '@七线全司' in l or '@全司' in l or '@六司' in l or '@八线' in l)]
out.append('BS-relevant lines total: %d' % len(lines))
for l in lines[-3:]:
    out.append('LED: %s' % l[:150])

orders = sorted(os.listdir('orders'), key=lambda f: os.path.getmtime(os.path.join('orders', f)), reverse=True)
out.append('orders top: %s | count: %d' % (orders[0], len(orders)))

out.append('index.lock: %s' % os.path.exists('.git/index.lock'))
out.append('CENSUS C-00030: %s' % os.path.exists(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md'))
out.append('10-03 brief: %s' % os.path.exists(os.path.join('data', 'intel', 'daily', '2026-10-03.md')))
out.append('10-02 brief: %s' % os.path.exists(os.path.join('data', 'intel', 'daily', '2026-10-02.md')))
oh = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\oss-harvest'
ohs = [f for f in os.listdir(oh) if 'bigstream' in f] if os.path.isdir(oh) else []
out.append('OH bigstream files: %s' % ohs)

io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r996_scan.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(x.encode('ascii', 'replace').decode('ascii') for x in out))
