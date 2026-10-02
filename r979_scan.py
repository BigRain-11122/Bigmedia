# -*- coding: utf-8 -*-
"""R979 group scan: extract new decision rows + dispatch board + ledger tail to UTF-8 file."""
import io, json, re

OUT = []
dec_path = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dec = io.open(dec_path, encoding='utf-8').read()

st = json.load(io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json', encoding='utf-8'))
known = set(st['decisions_watermark']['dnums'])

new_dnums = sorted(set(re.findall(r'[DC]-\d{8}-\d{2}', dec)) - known)
OUT.append('=== NEW DNUMS: %s ===' % (new_dnums if new_dnums else 'NONE'))

# extract full rows (table lines) containing new dnums
for nd in new_dnums:
    for line in dec.split('\n'):
        if nd in line:
            OUT.append('[%s] %s' % (nd, line.strip()[:2000]))
            break

# dispatch board block (top of decisions.md)
m = re.search(r'派工通告板(.*?)(\n## |\Z)', dec, re.S)
if m:
    board = m.group(1)
    OUT.append('=== DISPATCH BOARD (last 25 lines) ===')
    bl = [l for l in board.split('\n') if l.strip()]
    OUT.extend(bl[-25:])

# ledger: rows with P-20261002 / P-20261001 ids + @BigStream lines after 09-30
led = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md', encoding='utf-8').read()
OUT.append('=== LEDGER: rows dated 10-01/10-02 ===')
cnt = 0
for line in led.split('\n'):
    if re.search(r'P-2026-(1001|1002)-\d+', line):
        OUT.append(line.strip()[:1500]); cnt += 1
OUT.append('(10-01/10-02 rows: %d)' % cnt)
OUT.append('=== LEDGER: @BigStream matched lines mentioning 10-02 ===')
for line in led.split('\n'):
    if '@BigStream' in line and ('10-02' in line or '1002' in line):
        OUT.append(line.strip()[:1500])

io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\r979_scan.txt', 'w', encoding='utf-8').write('\n'.join(OUT))
print('WROTE %d lines' % len(OUT))
