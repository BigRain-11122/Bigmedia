# R312 fast-path scan: ledger anchor / decisions anchor / lock / novel ch5-v3 / daily / C-00029 anchor
import io, os, re, glob

def count_nonempty(path):
    n = 0
    with io.open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                n += 1
    return n

ledger = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
modes = ('@BigStream', '@七线全司', '@全司', '@六司')
hits = 0
tail_lines = []
with io.open(ledger, 'r', encoding='utf-8') as f:
    for line in f:
        if '@' in line and any(m in line for m in modes):
            hits += 1
            tail_lines.append(line.strip()[:80])
print('LEDGER_AT_LINES=%d (anchor=21)' % hits)
for t in tail_lines[-6:]:
    print('  ' + t)

dec = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
print('DECISIONS_NONEMPTY=%d (anchor=33)' % count_nonempty(dec))

lock = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.git\index.lock'
print('INDEX_LOCK=%s' % os.path.exists(lock))

novel = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\novel'
files = sorted(glob.glob(os.path.join(novel, '*')), key=os.path.getmtime, reverse=True)
print('--- novel top6 (mtime desc) ---')
for p in files[:6]:
    print('%s  mtime=%s' % (os.path.basename(p), os.path.getmtime(p)))

daily = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\intel\daily\2026-09-26.md'
print('DAILY_2026-09-26=%s' % os.path.exists(daily))

a29 = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00029.md'
print('C-00029_ANCHOR=%s' % os.path.exists(a29))

# bm-a recent activity: audio dir
audio = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\audio'
if os.path.isdir(audio):
    af = sorted(glob.glob(os.path.join(audio, '*')), key=os.path.getmtime, reverse=True)
    print('--- audio top4 ---')
    for p in af[:4]:
        print('%s  mtime=%s' % (os.path.basename(p), os.path.getmtime(p)))
