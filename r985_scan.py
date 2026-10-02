# R985 round-open scan: five-check (orders anchor / ledger / decisions dnum diff / lock / production / CENSUS anchor / 10-03 brief / OSS w3 file)
import re, os, json, datetime

st = json.load(open('src/os/state.json', encoding='utf-8'))
print('tick', st['tick'], '| production', st.get('production'), '| ts', st.get('ts'))
wm = st['decisions_watermark']['dnums']

p = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dec = open(p, encoding='utf-8').read()
cur = set(re.findall(r'[DC]-2026\d{4}-\d{2}', dec))
print('decisions mtime', datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%m-%d %H:%M:%S'))
new = sorted(cur - set(wm))
print('NEW DNUMS:', new if new else 'NONE', '| held:', len(wm), 'cur:', len(cur))

lp = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
led = open(lp, encoding='utf-8').read()
print('ledger mtime', datetime.datetime.fromtimestamp(os.path.getmtime(lp)).strftime('%m-%d %H:%M:%S'))
lines = [l for l in led.splitlines() if ('@BigStream' in l or '@七线全司' in l or '@全司' in l or '@六司' in l or '@八线' in l)]
print('BS-relevant lines total:', len(lines))
for l in lines[-3:]:
    print('LED:', l[:150])

orders = sorted(os.listdir('orders'), key=lambda f: os.path.getmtime(os.path.join('orders', f)), reverse=True)
print('orders top:', orders[0], '| count:', len(orders))

print('index.lock:', os.path.exists('.git/index.lock'))
print('CENSUS C-00030:', os.path.exists(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md'))
print('10-03 brief:', os.path.exists(r'data\intel\daily\2026-10-03.md'))
print('10-02 brief:', os.path.exists(r'data\intel\daily\2026-10-02.md'))
oh = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\oss-harvest'
ohs = [f for f in os.listdir(oh) if 'bigstream' in f] if os.path.isdir(oh) else []
print('OH bigstream files:', ohs)
