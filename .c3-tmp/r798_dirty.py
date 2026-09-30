import subprocess, collections, os

r = subprocess.run(['git', 'status', '--porcelain', '--ignored=matching', '-uall'],
                  capture_output=True, text=True, encoding='utf-8', errors='replace')
lines = [l for l in r.stdout.splitlines() if l.strip()]
print('total per-file porcelain+ignored lines:', len(lines))
cnt = collections.Counter()
bydir = collections.Counter()
sizes = collections.Counter()
for l in lines:
    path = l[3:].strip().strip('"')
    top = path.split('/')[0] if '/' in path else path
    bydir[top] += 1
    cnt[l[:2]] += 1
    try:
        if os.path.isfile(path):
            sizes[top] += os.path.getsize(path)
    except OSError:
        pass
print('by status:', dict(cnt))
print('top 30 dirs (count, MB):')
for d, c in bydir.most_common(30):
    print(' %5d  %8.1fMB  %s' % (c, sizes[d] / 1e6, d))

# git log search for D-20260930-06 / XL-14 receipts
for pat in ['D-20260930-06', 'XL-14', 'XL-13~18']:
    r2 = subprocess.run(['git', 'log', '--format=%h %s', '--grep=' + pat, '-i', '-n', '200'],
                        capture_output=True, text=True, encoding='utf-8', errors='replace')
    hits = [x for x in r2.stdout.splitlines() if x.strip()]
    print('LOG grep %r hits: %d' % (pat, len(hits)))
    for h in hits[:5]:
        print('   ', h[:150])
