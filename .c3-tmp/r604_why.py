# r604_why.py -- diagnose which five-mode pattern hits each matched ledger row (ASCII source)
import os, io
SCRIPT = os.path.abspath(__file__)
TMP = os.path.dirname(SCRIPT)
ROOT = os.path.dirname(TMP)
GROUP = os.path.dirname(os.path.dirname(ROOT))
PATS = ['@BigStream', '\u4e03\u7ebf\u5168\u53f8', '\u5168\u53f8', '\u516d\u53f8', '\u516b\u7ebf\u5168\u91cf']
ledger = os.path.join(GROUP, 'cph4', 'evolution-ledger.md')
out = []
with io.open(ledger, encoding='utf-8', errors='replace') as fh:
    for i, raw in enumerate(fh, 1):
        line = raw.rstrip('\r\n')
        hits = [p for p in PATS if p in line]
        if hits:
            pids = ','.join(str(PATS.index(p)) for p in hits)
            out.append('L%d PATS=%s' % (i, pids))
            for p in hits:
                j = line.find(p)
                out.append('   CTX[%s] %s' % (str(PATS.index(p)), line[max(0, j - 25):j + len(p) + 25]))
with io.open(os.path.join(TMP, 'r604_why.txt'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(out) + '\n')
print('WROTE %d result lines' % len(out))
