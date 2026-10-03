import io, subprocess, sys
out = subprocess.run([sys.executable, r'.c3-tmp\r1160_check.py'], capture_output=True)
io.open(r'.c3-tmp\r1160_check2.txt', 'w', encoding='utf-8').write(out.stdout.decode('utf-8', 'replace') + out.stderr.decode('utf-8', 'replace'))
keys = ['now=', 'LAST_COMMIT', 'ORDERS_TOP', 'LEDGER', 'DECISIONS_SET', 'index.lock', 'DAILY 2026-10']
t = io.open(r'.c3-tmp\r1160_check2.txt', encoding='utf-8').read()
picked = [l for l in t.splitlines() if any(k in l for k in keys)][:10]
print('\n'.join(picked))
