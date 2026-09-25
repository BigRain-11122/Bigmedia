# R226 five-check scan: ledger @-lines / group decisions count / storylines review / window enumeration.
import io, os, re

OUT = r'.bs005-tmp'
lines_out = []

def log(s):
    lines_out.append(s)

# 1) Group ledger: strict line-contains @ four patterns
ledger = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
pat = re.compile(r'@(BigStream|七线全司|全司|六司)')
hits = []
if os.path.exists(ledger):
    for ln in io.open(ledger, 'r', encoding='utf-8', errors='replace'):
        if pat.search(ln):
            hits.append(ln.strip())
log('ledger @-lines: %d (anchor 14)' % len(hits))
for h in hits:
    log('  ' + h[:120])
if len(hits) != 14:
    log('  !! ANCHOR MISMATCH - full recheck needed')

# 2) Group decisions.md UTF8 non-empty lines (anchor 24)
dec = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
if os.path.exists(dec):
    n = sum(1 for ln in io.open(dec, 'r', encoding='utf-8') if ln.strip())
    log('group decisions non-empty lines: %d (anchor 24)' % n)
else:
    log('group decisions file MISSING')

# 3) storylines review: novel (ch.6?), comic (ep.3?), audio dir
for sub in ('novel', 'comic', 'audio'):
    d = os.path.join('data', 'storylines', sub)
    if os.path.isdir(d):
        files = sorted(os.listdir(d))
        log('%s dir (%d): %s' % (sub, len(files), ', '.join(files)))
    else:
        log('%s dir MISSING' % sub)

# 4) Novel manuscript ch.3 same-text source check
src = os.path.join('data', 'storylines', 'novel', 'SC-001-03-v1.md')
log('novel ch.3 manuscript on disk: %s' % os.path.exists(src))

# 5) Window enumeration (Biggame console check)
import ctypes
from ctypes import wintypes
user32 = ctypes.windll.user32
titles = []
@ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
def cb(hwnd, lparam):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            titles.append(buf.value)
    return True
user32.EnumWindows(cb, 0)
log('visible windows: %d' % len(titles))
log('Biggame console window present: %s' % any('Biggame' in t for t in titles))
for t in titles:
    if 'Tuanjie' in t or 'Unity' in t or 'Game' in t:
        log('  - %s' % t[:80])

with io.open(os.path.join(OUT, 'r226-scan.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines_out))
print('scan done, %d lines' % len(lines_out))
