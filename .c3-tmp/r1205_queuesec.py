import io, re
q = io.open(r'docs\self-improvement-queue.md', encoding='utf-8').read()
# split by section headers
parts = re.split(r'\n(?=## )', q)
out = []
for p in parts:
    h = p.strip().splitlines()[0] if p.strip() else ''
    if h.startswith('## A') or h.startswith('## C') or h.startswith('## D'):
        out.append('==== %s ====' % h)
        # drop consumed/burn lines (they start with '- 2026-' typically in burn section; keep first 60 lines of section)
        body = [l for l in p.strip().splitlines()[1:] if l.strip()]
        out.extend(l[:180] for l in body[:55])
        out.append('  ... (section total %d lines)' % len(body))
io.open(r'.c3-tmp\r1205_queuesec.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('sections:', len(out))
