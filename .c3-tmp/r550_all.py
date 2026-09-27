# -*- coding: utf-8 -*-
# R549 fast-path five checks + three probes (probe-copy from r547_all.py, OUTP renamed per R462/R466 law)
import subprocess, sys, os, io, re, time, json

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
LED = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
DEC = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
OUT = os.path.join(ROOT, '.c3-tmp')

def now():
    return time.strftime('%Y-%m-%d %H:%M:%S')

res = []

# --- check 1: orders ---
od = os.path.join(ROOT, 'orders')
ofiles = sorted(f for f in os.listdir(od) if f.startswith('O-'))
latest = ofiles[-1]
res.append('ORDERS_COUNT=%d' % len(ofiles))
res.append('ORDERS_LATEST=%s' % latest)
res.append('ORDERS_LATEST_MTIME=%s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(os.path.join(od, latest)))))
anchor_t = time.mktime(time.strptime('2026-09-27 13:53:11', '%Y-%m-%d %H:%M:%S'))
edited = [f for f in ofiles if os.path.getmtime(os.path.join(od, f)) > anchor_t]
res.append('ORDERS_EDITED_SINCE_ANCHOR=%s' % (','.join(edited) if edited else 'NONE'))

# --- check 2/3: ledger five-mode line count + decisions non-empty count ---
pat = re.compile(u'@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf\u5168\u91cf)')
led_lines = io.open(LED, encoding='utf-8').read().splitlines()
n5 = sum(1 for l in led_lines if pat.search(l))
res.append('LEDGER_FIVEMODE_LINES=%d' % n5)
led_mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(LED)))
res.append('LEDGER_MTIME=%s' % led_mtime)
dec_lines = io.open(DEC, encoding='utf-8').read().splitlines()
nd = sum(1 for l in dec_lines if l.strip())
res.append('DECISIONS_NONEMPTY=%d' % nd)
dec_mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(DEC)))
res.append('DECISIONS_MTIME=%s' % dec_mtime)

# --- tree: index.lock + production self-heal ---
res.append('INDEX_LOCK=%s' % os.path.exists(os.path.join(ROOT, '.git', 'index.lock')))
st = json.load(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
res.append('STATE_PRODUCTION=%s TICK=%d' % (st.get('production'), st.get('tick')))

# --- key file mtimes (bm-a activity watch) ---
for rel in ['src/os/backlog.md', 'HQ-FEEDBACK.md', 'docs/reviews/station-reviews.md',
            'output/renders/README.md', 'output/finished.md', 'data/storylines/video/README.md',
            'data/storylines/cards/README.md']:
    p = os.path.join(ROOT, rel)
    res.append('MTIME|%s|%s' % (rel, time.strftime('%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p))) if os.path.exists(p) else 'NA'))

# --- storylines newest per subline ---
for sub in ['video', 'novel', 'audio', 'comic']:
    d = os.path.join(ROOT, 'data', 'storylines', sub)
    if os.path.isdir(d):
        items = [(os.path.getmtime(os.path.join(dp, f)), os.path.relpath(os.path.join(dp, f), d))
                 for dp, _, fs in os.walk(d) for f in fs]
        if items:
            t, f = max(items)
            res.append('STORY|%s|%s|%s' % (sub, time.strftime('%m-%d %H:%M', time.localtime(t)), f))

# --- BigLife anchors (CENSUS supply gate) ---
ad = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors'
if os.path.isdir(ad):
    an = sorted(f for f in os.listdir(ad) if f.endswith('.md'))
    res.append('ANCHORS_COUNT=%d TAIL3=%s' % (len(an), ','.join(an[-3:])))
    res.append('ANCHOR_C30=%s ANCHOR_C31=%s' % ('C-00030.md' in an, 'C-00031.md' in an))

# --- footage top (SC-003-01 material gate) ---
fd = os.path.join(ROOT, 'data', 'sources', 'footage')
if os.path.isdir(fd):
    items = sorted(((os.path.getmtime(os.path.join(fd, f)), f) for f in os.listdir(fd)), reverse=True)
    res.append('FOOTAGE_TOP3=' + '; '.join('%s@%s' % (f, time.strftime('%m-%d %H:%M', time.localtime(t))) for t, f in items[:3]))

# --- routine files ---
res.append('DAILY_0927=%s' % os.path.exists(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-09-27.md')))
aud = os.listdir(os.path.join(ROOT, 'docs', 'audits')) if os.path.isdir(os.path.join(ROOT, 'docs', 'audits')) else []
res.append('AUDITS=%s' % ','.join(sorted(aud)))

# --- git head + status ---
p = subprocess.run(['git', 'log', '-1', '--oneline'], cwd=ROOT, capture_output=True)
res.append('GIT_HEAD=' + p.stdout.decode('utf-8', 'replace').strip())
p = subprocess.run(['git', 'status', '--short'], cwd=ROOT, capture_output=True)
mod = [l for l in p.stdout.decode('utf-8', 'replace').splitlines() if l.strip()]
m_lines = [l for l in mod if l[:2].strip() == 'M']
untracked = [l for l in mod if l.startswith('??')]
res.append('GIT_MODIFIED=%d UNTRACKED=%d' % (len(m_lines), len(untracked)))
res.append('GIT_MODIFIED_LIST=' + '; '.join(l.strip() for l in m_lines))

summary = '\n'.join(res)
io.open(os.path.join(OUT, 'r550_check.txt'), 'w', encoding='utf-8').write(summary)

# --- three probes (output to UTF-8 files, no PS redirection) ---
probes = [('board', ['src/board_check.py']), ('readiness', ['src/readiness.py']), ('loop', ['src/os/loop_health.py'])]
pres = []
for name, cmd in probes:
    p = subprocess.run([sys.executable] + cmd, cwd=ROOT, capture_output=True)
    out = p.stdout.decode('utf-8', 'replace') + '\n[stderr]\n' + p.stderr.decode('utf-8', 'replace')
    io.open(os.path.join(OUT, 'r550_%s.txt' % name), 'w', encoding='utf-8').write(out)
    pres.append('PROBE|%s|exit=%d' % (name, p.returncode))

print(summary)
print('---')
print('\n'.join(pres))
print('RUN_TS=' + now())
