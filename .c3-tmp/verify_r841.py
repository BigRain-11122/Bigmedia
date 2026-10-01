import json, re, io, os, time

OUT = io.open('.c3-tmp/verify_r841.txt', 'w', encoding='utf-8')
W = OUT.write

def fmt(p):
    try:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p)))
    except Exception as e:
        return 'ERR %s' % e

# 1) group file mtimes (change detection vs R840 scan 11:34)
for p in [r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md',
          r'C:\Users\sjs20\Desktop\FluxGroup\docs\orders.md',
          r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md']:
    W('mtime %s = %s\n' % (p.split('\\')[-1], fmt(p)))

# 2) context of 'D-20260930-1' (non 2-digit ref) in decisions.md
dtxt = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', encoding='utf-8', errors='replace').read()
dl = dtxt.splitlines()
W('\n== D-20260930-1 contexts ==\n')
for i, l in enumerate(dl, 1):
    if re.search(r'D-20260930-1(?!\d)', l):
        W('L%d: %s\n' % (i, l[:400]))

# 3) board rows count + BigStream/qisI rows
W('\n== BOARD ROWS ==\n')
board = False
rows = []
for i, l in enumerate(dl, 1):
    if l.startswith('## ') and 'D-20260930-13' in l:
        board = True
    if board and re.match(r'\|\s*[DC]-\d{8}-\d+', l):
        rows.append((i, l))
W('board_row_count=%d\n' % len(rows))
for i, l in rows:
    W('L%d: %s\n' % (i, l[:200]))

# 4) full ledger tag-hit list (line numbers only + first 60 chars)
ltxt = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md', encoding='utf-8', errors='replace').read()
ll = ltxt.splitlines()
pat = re.compile('@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf)')
hits = [(i, l) for i, l in enumerate(ll, 1) if pat.search(l)]
W('\n== LEDGER HITS (%d) ==\n' % len(hits))
for i, l in hits:
    W('L%d: %s\n' % (i, l[:80]))

OUT.close()
print('ok')
