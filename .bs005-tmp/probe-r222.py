# R222 quick-path probe: ledger match lines + group decisions nonempty count + window enumeration (material-window signal)
# ASCII-only stdout; Chinese window titles written to UTF-8 file (PS5.1 GBK console rule).
import io
import ctypes
import ctypes.wintypes

BASE = r'C:\Users\sjs20\Desktop\FluxGroup'
LEDGER = BASE + r'\cph4\evolution-ledger.md'
DECISIONS = BASE + r'\docs\decisions.md'
OUT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.bs005-tmp\windows-R222.txt'

tokens = ('@BigStream', '@七线全司', '@全司', '@六司')

ledger_lines = []
with io.open(LEDGER, encoding='utf-8', errors='replace') as f:
    for line in f:
        if any(t in line for t in tokens):
            ledger_lines.append(line.rstrip('\n'))

n_dec = 0
with io.open(DECISIONS, encoding='utf-8', errors='replace') as f:
    for line in f:
        if line.strip():
            n_dec += 1

user32 = ctypes.windll.user32
titles = []

@ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
def cb(hwnd, lparam):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            titles.append(buf.value)
    return True

user32.EnumWindows(cb, 0)

biggame_hits = [t for t in titles if ('Biggame' in t) or ('小游戏公司' in t)]

with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write('R222 window enumeration %d visible titled windows\n' % len(titles))
    for t in titles:
        f.write(t + '\n')

print('ledger_match_lines: %d' % len(ledger_lines))
print('decisions_nonempty: %d' % n_dec)
print('visible_windows: %d' % len(titles))
print('biggame_totalctrl_hits: %d' % len(biggame_hits))
