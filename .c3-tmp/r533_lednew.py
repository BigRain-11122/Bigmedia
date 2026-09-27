# -*- coding: utf-8 -*-
# R533 ledger five-mode line dump (investigate 31 vs anchor 22)
import io, os, re, time
LED = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
mt = os.path.getmtime(LED)
pat = re.compile(u'@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf\u5168\u91cf)')
lines = io.open(LED, encoding='utf-8').read().splitlines()
out = []
out.append('LEDGER_MTIME=%s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mt)))
out.append('LEDGER_TOTAL_LINES=%d' % len(lines))
n = 0
for i, l in enumerate(lines, 1):
    if pat.search(l):
        n += 1
        tags = sorted(set(pat.findall(l)))
        ps = re.findall(r'P-\d{4}-\d{2}-\d{2}-\d{2}', l)
        us = re.findall(r'U\d{3}', l)
        body = l.strip()
        if len(body) > 420:
            body = body[:420] + ' <...TRUNC...>'
        out.append('L%d TAGS=%s P=%s U=%s' % (i, '+'.join(tags), ','.join(ps), ','.join(us)))
        out.append('    %s' % body)
out.insert(1, 'FIVEMODE_LINES=%d' % n)
txt = '\n'.join(out)
io.open(os.path.join(ROOT, '.c3-tmp', 'r533_lednew.txt'), 'w', encoding='utf-8').write(txt)
print('LEDGER_MTIME=%s FIVEMODE_LINES=%d dump=r533_lednew.txt' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mt)), n))
