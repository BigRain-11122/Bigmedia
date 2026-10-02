import io, re, json, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
os.chdir(ROOT)
out = []

# pools.json content stability (#86 a-leg trigger face adjudication)
pj = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
t = io.open(pj, encoding='utf-8').read()
lines = t.splitlines()
n_axes = len(re.findall(r'"axes"', t))
n_sprite = len(re.findall(r'"sprite"', t))
out.append('POOLS lines %d axes %d sprite %d (baseline 1440 total leaves: axes 1296 + sprite 144)' % (len(lines), n_axes, n_sprite))

# loop_health FAIL/WARN counts + account-lag tail
lt = io.open('.c3-tmp/r1021_loop.txt', encoding='utf-8').read()
fails = re.findall(r'\[FAIL\]', lt)
warns = re.findall(r'\[WARN\]', lt)
out.append('LOOP FAIL %d WARN %d (baseline R1057: 3 FAIL + 123 WARN)' % (len(fails), len(warns)))
lag = [l for l in lt.splitlines() if 'account-lag' in l]
out.append('ACCOUNT_LAG_LINES %d' % len(lag))
for l in lag[-2:]:
    out.append('LAG_TAIL: ' + l[:220])

io.open('.c3-tmp/r1058_pool_verify.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
