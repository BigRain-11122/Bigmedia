# R981 group-transfer scan: decisions.md dnum content-addressed diff + evolution-ledger @BigStream lines
import re, os, json, datetime

wm = json.load(open('src/os/state.json', encoding='utf-8'))['decisions_watermark']['dnums']
p = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dec = open(p, encoding='utf-8').read()
cur = set(re.findall(r'[DC]-2026\d{4}-\d{2}', dec))
print('decisions mtime', datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%m-%d %H:%M:%S'))
print('now', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
new = sorted(cur - set(wm))
print('NEW DNUMS:', new if new else 'NONE', '| held:', len(wm), 'cur:', len(cur))

lp = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
led = open(lp, encoding='utf-8').read()
print('ledger mtime', datetime.datetime.fromtimestamp(os.path.getmtime(lp)).strftime('%m-%d %H:%M:%S'))
lines = [l for l in led.splitlines() if ('@BigStream' in l or '@七线全司' in l or '@全司' in l or '@六司' in l)]
print('BS-relevant lines total:', len(lines))
for l in lines[-5:]:
    print('LED:', l[:170])

# orders CEO physical-item zone (present-status only, no urging)
op = r'C:\Users\sjs20\Desktop\FluxGroup\docs\orders.md'
if os.path.exists(op):
    ot = open(op, encoding='utf-8').read()
    print('orders.md mtime', datetime.datetime.fromtimestamp(os.path.getmtime(op)).strftime('%m-%d %H:%M:%S'))
    m = re.findall(r'(账号|商户号|服务器)[^\n]{0,60}', ot)
    print('CEO physical-item mentions (last 3):', m[-3:] if m else 'none')
