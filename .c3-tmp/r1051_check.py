import re, io, json, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
os.chdir(ROOT)
print('SHADOW_OS_IN_C3TMP', os.path.isfile(r'.c3-tmp\os.py') or os.path.isdir(r'.c3-tmp\os'))

# 1. latest order file
orders_dir = 'orders'
orders = sorted(os.listdir(orders_dir)) if os.path.isdir(orders_dir) else []
o_2026 = [f for f in orders if f.startswith('O-2026')]
print('LATEST_ORDER', o_2026[-1] if o_2026 else 'NONE')

# 2. daily report today
print('DAILY_10_03', os.path.isfile('data/intel/daily/2026-10-03.md'))

# 3. ledger scan (strict @-prefixed dispatch lines = rows starting with date)
led_path = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
led = io.open(led_path, encoding='utf-8', errors='replace').read().splitlines()
rows = [l for l in led if re.match(r'^\d{4}-', l)]
tg = [l for l in rows if ('@BigStream' in l) or ('@七线全司' in l) or ('@全司' in l) or ('@六司' in l) or ('@八线' in l)]
print('LEDGER_TOTAL_ROWS', len(rows))
print('LEDGER_TARGET_ROWS', len(tg))
# show last target row head (ascii-safe: write to utf8 file)
with io.open('.c3-tmp/r1051_ledger_tail.txt', 'w', encoding='utf-8') as f:
    for l in tg[-3:]:
        f.write(l[:300] + '\n')

# 4. decisions.md content-addressing set diff
dec_path = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
d = io.open(dec_path, encoding='utf-8', errors='replace').read()
nums = set(re.findall(r'D-20\d{6}-\d{2}|C-20\d{6}-\d{2}', d))
state = json.load(io.open('src/os/state.json', encoding='utf-8'))
w = set(state['decisions_watermark']['dnums'])
new = sorted(nums - w)
missing = sorted(w - nums)
print('NEW_DNUMS', new)
print('WATERMARK_MISSING_FROM_FILE', len(missing))

# 5. board 派工通告板 head check (for D-20260930-19 dispatch layer)
m = re.search(r'派工通告板', d)
print('DISPATCH_BOARD_PRESENT', bool(m))

# 6. orders.md CEO pending physical items zone (present-only)
om = r'C:\Users\sjs20\Desktop\FluxGroup\docs\orders.md'
print('GROUP_ORDERS_MD', os.path.isfile(om))

# 7. ledger P- rows with corrected pattern + target lines
prows = [x for x in led if re.match(r'^\|?P-20', x) or re.match(r'^- P-20', x)]
tga = [x for x in led if re.search(r'@(BigStream|七线全司|全司|六司|八线)', x)]
print('LEDGER_P_ROWS', len(prows))
print('LEDGER_TARGET_LINES', len(tga))
with io.open('.c3-tmp/r1051_ledger_tail.txt', 'a', encoding='utf-8') as f:
    f.write('--- P ROWS last 2 ---\n')
    for x in prows[-2:]:
        f.write(x[:300] + '\n')
    f.write('--- TARGET last 2 ---\n')
    for x in tga[-2:]:
        f.write(x[:300] + '\n')
