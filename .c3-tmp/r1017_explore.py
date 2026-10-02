import json, re, os, glob, io

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
out = io.StringIO()
def w(s): out.write(str(s) + '\n')

st = json.load(open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
log = st['log']
w('=== R1016 FULL LOG ===')
w(log[-1])
w('')
w('=== R1015 LOG HEAD (1200) ===')
w(log[-2][:1200])

w('=== src/os py ===')
w(sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, 'src', 'os', '*.py'))))
w('=== src py ===')
w(sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, 'src', '*.py'))))

w('=== root r9xx/r10xx ===')
w(sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, 'r9*')) + glob.glob(os.path.join(ROOT, 'r10*'))))

w('=== queue E30 / DAILY / rihao mentions ===')
q = open(os.path.join(ROOT, 'docs', 'self-improvement-queue.md'), encoding='utf-8').read()
qlines = q.splitlines()
for i, l in enumerate(qlines):
    if 'E30' in l or ('E2' in l and 'DAILY' in l) or 'OSS w3' in l:
        w('L%d: %s' % (i + 1, l[:400]))

w('=== cards dir newest 18 ===')
for f in sorted(glob.glob(os.path.join(ROOT, 'data', 'storylines', 'cards', '*')), key=os.path.getmtime)[-18:]:
    w('%s | %s' % (os.path.basename(f), os.path.getmtime(f)))

open(os.path.join(ROOT, '.c3-tmp', 'r1017_explore.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('done')
