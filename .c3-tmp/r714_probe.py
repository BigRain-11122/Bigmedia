# -*- coding: utf-8 -*-
# R714 five-check probe: orders top / ledger / decisions / queue / backlog top / time
import io, os, re, glob, datetime

OUT = io.open('.c3-tmp/r714_probe.txt', 'w', encoding='utf-8')

def w(s):
    OUT.write(s + '\n')

now = datetime.datetime.now()
w('NOW = %s' % now.strftime('%Y-%m-%d %H:%M:%S'))

# 1. orders top (latest file by name prefix date)
orders = sorted(glob.glob('orders/*.md'))
w('\n== orders top 3 ==')
for f in orders[-3:]:
    w('%s (mtime %s)' % (f, datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M:%S')))

# 2. ledger: strictly-prefixed @BigStream / full-company rows (CaseSensitive, per R711/R713 anchor=41)
led = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
txt = io.open(led, encoding='utf-8').read()
lines = txt.splitlines()
pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
hits = [l for l in lines if pat.search(l)]
w('\n== ledger strict-mode @rows = %d (R713 anchor 41) ==' % len(hits))
new = []
for l in hits:
    m = re.match(r'^(P|O|D|C|T)-?2026', l.strip())
    # detect rows with date 09-30 or later that reference BigStream
    if '2026-09-30' in l or '09-30' in l:
        new.append(l)
w('rows mentioning 09-30: %d' % len(new))
for l in new[:5]:
    w('  ' + l[:200])
# last 2 ledger rows overall
w('\nledger last 2 lines:')
for l in lines[-2:]:
    w('  ' + l[:300])

# 3. decisions.md non-empty row count (anchor 75)
dec = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dt = io.open(dec, encoding='utf-8').read().splitlines()
n = len([l for l in dt if l.strip()])
w('\n== decisions UTF8 non-empty rows = %d (R713 anchor 75) ==' % n)

# 4. queue §E pool head + §D head
q = io.open('docs/self-improvement-queue.md', encoding='utf-8').read().splitlines()
w('\n== queue: first 40 lines ==')
for l in q[:40]:
    w(l[:160])

# 5. backlog top open item
bk = io.open('src/os/backlog.md', encoding='utf-8').read().splitlines()
w('\n== backlog: top open items ==')
count = 0
for l in bk:
    if l.startswith(tuple('0123456789')) and '.' in l[:5]:
        if '[done' not in l:
            w(l[:400])
            count += 1
            if count >= 3:
                break

# 6. LC-012 WIP state check
w('\n== LC-012 WIP dirs ==')
for d in ['data/sources/lc012', '.lc012-tmp']:
    if os.path.isdir(d):
        fs = sorted(os.listdir(d))
        w('%s: %d files: %s' % (d, len(fs), ', '.join(fs[:25])))
OUT.close()
print('probe done -> .c3-tmp/r714_probe.txt')
