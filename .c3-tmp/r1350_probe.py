# -*- coding: utf-8 -*-
# r1350 probe suite: three probes fresh run + backlog open-item parse + queue top scan (independent OUT per R1311)
import json, os, re, subprocess, io, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []
def w(s): OUT.append(str(s))

w('now=%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# decisions set-diff confirm (content addressing)
dec = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dtxt = io.open(dec, encoding='utf-8', errors='replace').read()
dnow = set(re.findall(r'[DC]-\d{8}-\d{2}', dtxt))
state = json.load(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
wm = set(state.get('decisions_watermark', {}).get('dnums', []))
new = sorted(dnow - wm)
w('DECISIONS_SET: now=%d wm=%d NEW=%s' % (len(dnow), len(wm), new if new else '[]'))
gone = sorted(wm - dnow)
w('DECISIONS_GONE_FROM_WM: %s' % (gone if gone else '[]'))

# backlog open-item parse (entry header lines with/without [done)
bt = io.open(os.path.join(ROOT, 'src', 'os', 'backlog.md'), encoding='utf-8').read()
w('--- backlog entries ---')
for ln in bt.splitlines():
    m = re.match(r'^(\d+)\.\s', ln)
    if m:
        done = '[done' in ln
        w(('%s ' % m.group(1)) + ('DONE ' if done else 'OPEN ') + ln[:150])

# queue top scan
q = os.path.join(ROOT, 'docs', 'self-improvement-queue.md')
if os.path.exists(q):
    qt = io.open(q, encoding='utf-8', errors='replace').read()
    w('--- queue mtime %s len=%d ---' % (time_str := __import__('time').strftime('%m-%d %H:%M', __import__('time').localtime(os.path.getmtime(q))), len(qt)) if False else '--- queue present ---')
    w('QUEUE mtime %s' % __import__('time').strftime('%m-%d %H:%M', __import__('time').localtime(os.path.getmtime(q))))
    w('QUEUE first 40 lines:')
    for ln in qt.splitlines()[:40]:
        w('Q| ' + ln[:170])
else:
    w('QUEUE MISSING')

# three probes fresh
def run(label, args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (p.stdout or "") + (p.stderr or "")
    w('=== %s (rc=%d) ===' % (label, p.returncode))
    w(out.strip()[-1800:])

run('BOARD', ['python', 'src/board_check.py'])
run('READINESS', ['python', 'src/readiness.py'])
run('LOOP_HEALTH', ['python', 'src/os/loop_health.py'])

io.open(os.path.join(ROOT, '.c3-tmp', 'r1350_probe.txt'), 'w', encoding='utf-8').write('\n'.join(OUT))
print('written lines:', len(OUT))
