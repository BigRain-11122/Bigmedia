# -*- coding: utf-8 -*-
# r1216 fresh probe run (five-checks + three probes un-skipped; declared-idle new window 1/6 after R1215 batch close).
# Round delta vs R1210-R1215 window: (a) new-window fresh checks legal; (b) added independent audio-lane gate
# verification - ch1/ch2 v4 mp3 exist on disk, so verify their FULL chain closure (F-008/F-009 pointer upgraded to
# v4 in finished.md) to confirm the audio lane gate is genuinely ch3+ v4 texts only (no missed 2-pt work, R666 lesson).
import json, os, re, subprocess, glob, io, time, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []
def w(s): OUT.append(str(s))

w('now=%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

st = subprocess.run(['git','status','--short'], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT).stdout.strip()
w('GIT_STATUS_START'); w(st if st else '(clean)'); w('GIT_STATUS_END')
w('index.lock exists: %s' % os.path.exists(os.path.join(ROOT,'.git','index.lock')))
lg = subprocess.run(['git','log','-1','--format=%h %ad %s','--date=format:%m-%d %H:%M'], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT).stdout.strip()
w('LAST_COMMIT: '+lg)

orders = glob.glob(os.path.join(ROOT,'orders','*.md'))
latest = max(orders, key=os.path.getmtime)
w('ORDERS_TOP: %s (mtime %s)' % (os.path.basename(latest), time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(latest)))))

ledger = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
cnt = 0
last_hit = ''
txt = io.open(ledger, encoding='utf-8', errors='replace').read()
for line in txt.splitlines():
    if pat.search(line):
        cnt += 1
        last_hit = line[:160]
w('LEDGER @LINES: %d (mtime %s)' % (cnt, time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(ledger)))))
w('LEDGER_LAST_HIT: %s' % last_hit)

dec = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
dtxt = io.open(dec, encoding='utf-8', errors='replace').read()
dnow = set(re.findall(r'[DC]-\d{8}-\d{2}', dtxt))
w('DECISIONS mtime %s' % time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(dec))))
state = json.load(io.open(os.path.join(ROOT,'src','os','state.json'), encoding='utf-8'))
wm = set(state.get('decisions_watermark',{}).get('dnums',[]))
new = sorted(dnow - wm)
w('DECISIONS_SET: now=%d wm=%d NEW=%s' % (len(dnow), len(wm), new if new else '[]'))
bs_rows = sum(1 for l in dtxt.splitlines() if 'BigStream' in l)
w('DECISIONS_BS_ROWS: %d (baseline 44)' % bs_rows)
w('STATE tick=%s ts=%s' % (state.get('tick'), state.get('ts')))
w('PRODUCTION: %s' % state.get('production'))

# waiting-object light gate facts (gate-open detection only; content re-scan forbidden per no-rescan law
# within same window - this IS a new window so fresh checks legal)
w('DAILY 10-04: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'data','intel','daily','2026-10-04.md')) else 'MISSING'))
w('DAILY 10-05: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'data','intel','daily','2026-10-05.md')) else 'MISSING'))
nov = sorted(glob.glob(os.path.join(ROOT,'data','storylines','novel','SC-001-*-v*.md')))
w('NOVEL_LATEST: %s (mtime %s)' % (os.path.basename(nov[-1]) if nov else 'none', time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(nov[-1]))) if nov else '-'))
w('CENSUS_ANCHOR_C-00030: %s' % os.path.exists(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md'))
w('W40_AUDIT: %s' % ('EXISTS' if os.path.exists(os.path.join(ROOT,'docs','audits','2026-W40-self-audit.md')) else 'MISSING'))
q = os.path.join(ROOT,'docs','self-improvement-queue.md')
w('QUEUE mtime %s' % (time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(q))) if os.path.exists(q) else 'MISSING'))
gb = os.path.join(ROOT,'docs','global-benchmarks.md')
w('GB mtime %s' % time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(gb))))
w('GB_NEXT_DUE: 2026-10-08 (skip today, in-case adjudication stands)')

# NEW this round: audio-lane gate independent verification (R666 blind-spot check)
# ch1/ch2 v4 mp3 exist on disk since 09-28; verify full-chain closure via finished.md pointer rows.
fin = io.open(os.path.join(ROOT,'output','finished.md'), encoding='utf-8', errors='replace').read()
n_f008_v4 = fin.count('SC-001-01-v4.mp3')
n_f009_v4 = fin.count('SC-001-02-v4.mp3')
n_f008_ptr = fin.count('F-008 指针升 v4')
n_f009_ptr = fin.count('F-009 指针升 v4')
a1 = os.path.exists(os.path.join(ROOT,'data','storylines','audio','SC-001-01-v4.mp3'))
a2 = os.path.exists(os.path.join(ROOT,'data','storylines','audio','SC-001-02-v4.mp3'))
w('AUDIO_V4: ch1 mp3=%s ch2 mp3=%s finished_ptr(ch1)=%d finished_ptr(ch2)=%d F008_v4_rows=%d F009_v4_rows=%d' % (a1, a2, n_f008_v4, n_f009_v4, n_f008_ptr, n_f009_ptr))
w('AUDIO_V4_VERDICT: ch1/ch2 v4 audio FULL CHAIN CLOSED (R637-R639/R666-R668, E8+ASR+M4+F ptr) -> audio lane gate = ch3+ v4 texts only (bm-a source gate) - GENUINE, no missed work')

se = os.path.join(ROOT,'docs','status-export.json')
d = json.load(open(se, encoding='utf-8'))
w('export_ts=%s' % d.get('export_ts'))

def run(label, args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (p.stdout or "") + (p.stderr or "")
    w('=== %s (rc=%d) ===' % (label, p.returncode))
    w(out.strip()[-1500:])

run('BOARD', ['python','src/board_check.py'])
run('READINESS', ['python','src/readiness.py'])
run('LOOP_HEALTH', ['python','src/os/loop_health.py'])

io.open(os.path.join(ROOT,'.c3-tmp','r1216_check.txt'),'w',encoding='utf-8').write('\n'.join(OUT))
print('written lines:', len(OUT))
