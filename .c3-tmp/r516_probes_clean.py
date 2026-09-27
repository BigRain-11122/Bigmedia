import os, re

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
ANSI = re.compile(r'\x1b\[[0-9;]*[A-Za-z]|\x1b\][^\x07]*\x07')
CTRL = re.compile(r'[\x00-\x08\x0b-\x1f\x7f]')
out = []
KEY = re.compile(r'FAIL|ERROR|WARN|block|BLOCK|SUMMARY|PASS|distance|tick|account|heartbeat|GATE|renders', re.I)
for name in ['r516_board', 'r516_ready', 'r516_loop']:
    p = os.path.join(ROOT, '.c3-tmp', name + '.txt')
    raw = open(p, 'rb').read()
    txt = None
    for enc in ('utf-8', 'gbk'):
        try:
            txt = raw.decode(enc)
            break
        except Exception:
            continue
    if txt is None:
        txt = raw.decode('utf-8', errors='replace')
    txt = ANSI.sub('', txt)
    txt = CTRL.sub('', txt)
    lines = [l for l in txt.splitlines() if l.strip()]
    out.append(f'===== {name}: {len(lines)} lines =====')
    key = [l for l in lines if KEY.search(l)]
    for l in key[:45]:
        out.append(l[:180])
    out.append('--- tail 8 ---')
    for l in lines[-8:]:
        out.append(l[:180])
safe = [l.encode('ascii', errors='replace').decode('ascii') for l in out]
with open(os.path.join(ROOT, '.c3-tmp', 'r516_probes_clean.txt'), 'w', encoding='ascii', errors='replace') as fh:
    fh.write('\n'.join(safe))
print('WROTE', len(safe), 'lines')
