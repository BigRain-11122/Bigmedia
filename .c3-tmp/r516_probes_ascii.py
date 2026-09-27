import os, re

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
out = []
KEY = re.compile(r'FAIL|ERROR|WARN|block|BLOCK|SUMMARY|PASS|distance|tick|account|heartbeat|GATE|renders', re.I)
for name in ['r516_board', 'r516_ready', 'r516_loop']:
    p = os.path.join(ROOT, '.c3-tmp', name + '.txt')
    raw = open(p, 'rb').read()
    try:
        txt = raw.decode('utf-8')
    except Exception:
        txt = raw.decode('gbk', errors='replace')
    lines = txt.splitlines()
    out.append(f'===== {name}: {len(lines)} lines =====')
    key = [l for l in lines if KEY.search(l)]
    for l in key[:45]:
        out.append(l[:180])
    out.append('--- tail 6 ---')
    for l in lines[-6:]:
        out.append(l[:180])
# ascii-safe print
safe = []
for l in out:
    safe.append(l.encode('ascii', errors='replace').decode('ascii'))
print('\n'.join(safe))
