# -*- coding: utf-8 -*-
# R240 three-probe run + window enumeration + scan-side mtimes (R219/R234/R236/R237 conventions)
import io, os, subprocess, sys, datetime

BS = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
probes = [
    ('board', [sys.executable, 'src/board_check.py']),
    ('readiness', [sys.executable, 'src/readiness.py']),
    ('loop_health', [sys.executable, 'src/os/loop_health.py']),
]
out = []
for name, cmd in probes:
    p = subprocess.run(cmd, cwd=BS, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    txt = p.stdout.decode('utf-8', errors='replace')
    out.append('===== %s exit=%d =====' % (name, p.returncode))
    out.append(txt)
io.open(BS + r'\.bs005-tmp\probe-r240-all.txt', 'w', encoding='utf-8').write('\n'.join(out))

# window enumeration (Biggame master-console watch, R193-R239 line)
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
io.open(BS + r'\.bs005-tmp\windows-R240.txt', 'w', encoding='utf-8').write('\n'.join(titles))
biggame = [t for t in titles if 'Biggame' in t or '总控' in t]
tuanjie = [t[:60] for t in titles if ('Tuanjie' in t or 'Unity' in t or 'Game' in t)]

# scan-side mtimes: group decisions/ledger + storylines newest (bm-a write-sign check)
grp_dec = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
grp_led = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
dec_nonempty = sum(1 for ln in io.open(grp_dec, encoding='utf-8', errors='replace') if ln.strip())
dec_total = sum(1 for _ in io.open(grp_dec, encoding='utf-8', errors='replace'))
led_at = sum(1 for ln in io.open(grp_led, encoding='utf-8', errors='replace')
             if ('@BigStream' in ln or '@七线全司' in ln or '@全司' in ln or '@六司' in ln))
story_root = BS + r'\data\storylines'
newest = []
for sub in ('novel', 'comic', 'audio'):
    d = os.path.join(story_root, sub)
    for fn in os.listdir(d):
        fp = os.path.join(d, fn)
        if os.path.isfile(fp):
            newest.append((datetime.datetime.fromtimestamp(os.path.getmtime(fp)).strftime('%m-%d %H:%M'), sub + '/' + fn))
newest.sort(reverse=True)

mt = lambda p: datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%m-%d %H:%M')
queue_path = os.path.join(BS, 'docs', 'self-improvement-queue.md')
gb_path = os.path.join(BS, 'docs', 'global-benchmarks.md')
daily_path = os.path.join(BS, 'data', 'intel', 'daily', '2026-09-25.md')
audit_path = os.path.join(BS, 'docs', 'audits', '2026-W39-self-audit.md')
summary = [
    'decisions nonempty=%d total=%d mtime=%s' % (dec_nonempty, dec_total, mt(grp_dec)),
    'ledger @lines=%d mtime=%s' % (led_at, mt(grp_led)),
    'biggame_window=%s' % biggame,
    'tuanjie_titles=%s' % tuanjie,
    'storylines newest 6=%s' % newest[:6],
    'audio README mtime=%s' % mt(os.path.join(story_root, 'audio', 'README.md')),
    'queue mtime=%s' % mt(queue_path),
    'global-benchmarks mtime=%s' % mt(gb_path),
    'daily 0925 exists=%s' % os.path.exists(daily_path),
    'W39 audit exists=%s' % os.path.exists(audit_path),
]
io.open(BS + r'\.bs005-tmp\r240-scan-side.txt', 'w', encoding='utf-8').write('\n'.join(summary))
print('done')
