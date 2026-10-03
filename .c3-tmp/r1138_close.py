# -*- coding: utf-8 -*-
"""R1138 declared-idle 3/6 state append: tick/log/ts/task only (no commit per
os-protocol section 6 window rule; no export refresh, export_ts age <24h and
zero live change per F3 rule, R1130/R1136 precedent). Chinese text loaded from
r1138_texts.txt (UTF-8 data file) so this script body stays ASCII per
encoding law. Clone of r1137_close.py."""
import io, json, datetime

STP = r'src\os\state.json'
TXP = r'.c3-tmp\r1138_texts.txt'

stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

raw = io.open(TXP, encoding='utf-8').read().strip()
lines_in = [l for l in raw.splitlines() if l.strip() and not l.startswith('===')]
LOG = lines_in[0]
assert '20:0x' in LOG, '20:0x placeholder missing'
LOG = LOG.replace('20:0x', stamp[11:16])
TASK = LOG.split(u' ', 2)[2][:60]

lines = io.open(STP, encoding='utf-8', newline='').readlines()
logidx = max(i for i, l in enumerate(lines) if l.lstrip().startswith(u'"2026-'))
nl = u'\r\n' if lines[logidx].endswith(u'\r\n') else u'\n'
body = lines[logidx].rstrip(u'\r\n')
assert body.endswith(u'"'), 'last log line must end with quote, got: %r' % body[-12:]
if not body.endswith(u','):
    lines[logidx] = body + u',' + nl
indent = u'    '
newlog = indent + u'"' + LOG.replace(u'"', u'\\"') + u'"' + nl
assert u'\\"' in newlog or u'"' not in LOG, 'quote check'
lines.insert(logidx + 1, newlog)

out = []
for l in lines:
    ls = l.lstrip()
    if ls.startswith(u'"tick":'):
        out.append(u'  "tick": 1138,' + nl)
    elif ls.startswith(u'"ts":'):
        out.append(u'  "ts": ' + json.dumps(stamp, ensure_ascii=False) + u',' + nl)
    elif ls.startswith(u'"task":'):
        out.append(u'  "task": ' + json.dumps(TASK, ensure_ascii=False) + nl)
    else:
        out.append(l)
io.open(STP, 'w', encoding='utf-8', newline='').writelines(out)

# verify parse
st = json.load(io.open(STP, encoding='utf-8'))
print('tick=%s ts=%s' % (st['tick'], st['ts']))
print('loglines=%d' % len(st['log']))
print('last log head: %s' % st['log'][-1][:80])
print('task=%s' % st['task'])
