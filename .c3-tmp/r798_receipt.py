import subprocess, re

out = open(r'.c3-tmp\r798_receipt.txt', 'w', encoding='utf-8')

# 1. commit dates of R749/R750 + current HEAD + push state
for sha in ['5a07fe0', '96cebff', 'f042090']:
    r = subprocess.run(['git', 'show', '-s', '--format=%h %ci %s', sha],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    out.write('COMMIT: ' + r.stdout.strip()[:220] + '\n')
r = subprocess.run(['git', 'log', '-1', '--format=%h %ci', 'HEAD'], capture_output=True, text=True,
                   encoding='utf-8', errors='replace')
out.write('HEAD: ' + r.stdout.strip() + '\n')
r = subprocess.run(['git', 'status', '-sb'], capture_output=True, text=True, encoding='utf-8', errors='replace')
out.write('BRANCH: ' + r.stdout.splitlines()[0] + '\n')

# 2. full commit message of R750 (the XL-14 closeout)
r = subprocess.run(['git', 'log', '--format=%B', '-n', '1', '96cebff'],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
out.write('\n=== R750 full message ===\n' + r.stdout + '\n')

# 3. backlog #95 row
t = open(r'src/os/backlog.md', encoding='utf-8').read()
i = t.find('\n95.')
out.write('\n=== backlog #95 row ===\n' + t[i:i+2200] + '\n')

# 4. enforcement record context in group decisions (find the audit-check text with BigStream x)
dec = open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', encoding='utf-8').read()
for m in re.finditer(r'BigStream', dec):
    ctx = dec[max(0, m.start()-500):m.start()+300]
    if 'D-20260930-06' in ctx or 'XL-14' in ctx:
        out.write('\n=== enforcement ctx @%d ===\n' % m.start() + ctx + '\n')
out.close()
print('ok')
