# -*- coding: utf-8 -*-
# R1346 post-commit integrity verify: HEAD state.json valid JSON, tick/log/ts/task/focus correct, no log loss
import json, io, subprocess

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
raw = subprocess.run(['git','show','HEAD:src/os/state.json'], capture_output=True, cwd=ROOT).stdout.decode('utf-8')
state = json.loads(raw)
out = []
out.append('HEAD state.json: VALID JSON')
out.append('tick=%s' % state.get('tick'))
out.append('ts=%s' % state.get('ts'))
out.append('task(first 70)=%s' % state.get('task','')[:70])
out.append('log_entries=%d' % len(state.get('log',[])))
out.append('log[-1] head 120: %s' % state.get('log',[])[-1][:120])
out.append('log[-2] head 120: %s' % state.get('log',[])[-2][:120])
out.append('log[-3] head 120: %s' % state.get('log',[])[-3][:120])
out.append('log[-7] head 80: %s' % state.get('log',[])[-7][:80])
out.append('focus head 150: %s' % state.get('focus','')[:150])
# round sequence sanity: extract RNNNN tokens from log tail 12
import re
tails = state.get('log',[])[-12:]
seq = []
for l in tails:
    m = re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}x? R(\d+):', l)
    seq.append(int(m.group(1)) if m else None)
out.append('round seq tail12: %s' % seq)
out.append('production=%s' % state.get('production'))
out.append('dnums wm count=%d' % len(state.get('decisions_watermark',{}).get('dnums',[])))

# count log entries mentioning each of R1341..R1346 to confirm all six in log
for rn in range(1341, 1347):
    hits = sum(1 for l in state.get('log',[]) if ('R%d:' % rn) in l[:40] or ('R%d ' % rn) in l[:40] or l.startswith('2026-10-05') and ('R%d:' % rn) in l[:30])
    out.append('log entry R%d present rows=%d' % (rn, hits))

io.open(ROOT + r'\.c3-tmp\r1346_verify.txt','w',encoding='utf-8').write('\n'.join(out))
print('verify written, log_entries=%d tick=%s' % (len(state.get('log',[])), state.get('tick')))
