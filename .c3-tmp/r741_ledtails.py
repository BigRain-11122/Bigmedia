# -*- coding: utf-8 -*-
# R741 ledger tails dump (renders README LC-018 decl row + lc-017 in-chain row + station-reviews tail + lc018 README + queue E19 rows)
import io, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
OUT = os.path.join(ROOT, '.c3-tmp', 'r741_ledtails.txt')
buf = []

r = io.open(os.path.join(ROOT, 'output', 'renders', 'README.md'), encoding='utf-8').read()
lines = r.split('\n')
buf.append('===== renders README: LC-018 declaration rows =====')
for i, l in enumerate(lines):
    if 'LC-018' in l or 'lc-018' in l:
        buf.append('L%d: %s' % (i + 1, l))
buf.append('===== renders README: lc-017 in-chain table row (template) =====')
for i, l in enumerate(lines):
    if l.startswith('| lc-017'):
        buf.append('L%d: %s' % (i + 1, l))
buf.append('===== renders README tail structure (last 8 lines with index) =====')
for i in range(max(0, len(lines) - 8), len(lines)):
    buf.append('L%d: %s' % (i + 1, lines[i]))

sr = io.open(os.path.join(ROOT, 'docs', 'reviews', 'station-reviews.md'), encoding='utf-8').read()
sl = sr.split('\n')
buf.append('===== station-reviews tail 6 =====')
for i in range(max(0, len(sl) - 6), len(sl)):
    buf.append('L%d: %s' % (i + 1, sl[i][:400]))

lr = io.open(os.path.join(ROOT, 'data', 'sources', 'lc018', 'README.md'), encoding='utf-8').read()
buf.append('===== lc018 README full =====')
buf.append(lr)

q = io.open(os.path.join(ROOT, 'docs', 'self-improvement-queue.md'), encoding='utf-8').read()
ql = q.split('\n')
buf.append('===== queue E18 render-leg row (R737 template) =====')
for i, l in enumerate(ql):
    if 'R737' in l and '渲染腿' in l:
        buf.append('L%d: %s' % (i + 1, l))
buf.append('===== queue E19 rows =====')
for i, l in enumerate(ql):
    if 'E19' in l and ('R739' in l or 'R740' in l):
        buf.append('L%d: %s' % (i + 1, l[:600]))

io.open(OUT, 'w', encoding='utf-8').write('\n'.join(buf))
print('DONE ->', OUT)
