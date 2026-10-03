# -*- coding: utf-8 -*-
"""R1141 declared-idle 6/6 BATCH CLOSE state+export append (window R1136-R1141
one-commit per os-protocol section 6). Adapted from r1140_close.py with the
batch-close additions: tick 1141, focus refresh (batch-close convention per
R1135/R1129/R1123), export refresh (export_ts + results append + live line 1 +
outs OS-loop line, F3 rule batch-close 4th-round refresh precedent R1135).
Chinese text loaded from r1141_texts.txt (UTF-8 data file) so this script
body stays ASCII per encoding law."""
import io, json, datetime

STP = r'src\os\state.json'
EXP = r'docs\status-export.json'
TXP = r'.c3-tmp\r1141_texts.txt'

stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
hhmm = stamp[11:16]

# --- parse sections ---
raw = io.open(TXP, encoding='utf-8').read()
secs = {}
cur = None
for ln in raw.splitlines():
    if ln.startswith('===') and ln.endswith('==='):
        cur = ln[3:-3].strip()
        secs[cur] = []
    elif cur:
        secs[cur].append(ln)
for k in secs:
    secs[k] = '\n'.join(secs[k]).strip()

LOG = secs['LOG']
assert LOG.count('20:4x') == 1, 'LOG placeholder must appear exactly once'
LOG = LOG.replace('20:4x', hhmm)
TASK = LOG.split(u' ', 2)[2][:60]
FOCUS = secs['FOCUS']
RESULT = secs['RESULT'].replace('20:4x', hhmm)
LIVE1 = secs['LIVE1'].replace('20:4x', hhmm)
OUTS_OS = secs['OUTS_OS']

# --- state.json: append log, tick 1141, ts/task, focus ---
lines = io.open(STP, encoding='utf-8', newline='').readlines()
logidx = max(i for i, l in enumerate(lines) if l.lstrip().startswith(u'"2026-'))
nl = u'\r\n' if lines[logidx].endswith(u'\r\n') else u'\n'
body = lines[logidx].rstrip(u'\r\n')
assert body.endswith(u'"'), 'last log line must end with quote, got: %r' % body[-12:]
if not body.endswith(u','):
    lines[logidx] = body + u',' + nl
indent = u'    '
newlog = indent + u'"' + LOG.replace(u'"', u'\\"') + u'"' + nl
lines.insert(logidx + 1, newlog)

out = []
for l in lines:
    ls = l.lstrip()
    if ls.startswith(u'"tick":'):
        out.append(u'  "tick": 1141,' + nl)
    elif ls.startswith(u'"ts":'):
        out.append(u'  "ts": ' + json.dumps(stamp, ensure_ascii=False) + u',' + nl)
    elif ls.startswith(u'"task":'):
        out.append(u'  "task": ' + json.dumps(TASK, ensure_ascii=False) + nl)
    elif ls.startswith(u'"focus":'):
        out.append(u'  "focus": ' + json.dumps(FOCUS, ensure_ascii=False) + u',' + nl)
    else:
        out.append(l)
io.open(STP, 'w', encoding='utf-8', newline='').writelines(out)

# --- status-export.json: export_ts + results append + live1 + outs OS line ---
ex = json.load(io.open(EXP, encoding='utf-8'))
assert ex['export_ts'] == '2026-10-03 19:33:49', 'unexpected export_ts anchor: %s' % ex['export_ts']
ex['export_ts'] = stamp
ex['results'].append(['1141', RESULT])
ex['live'][0][0] = LIVE1
# live[1] latest product line unchanged (F-150 DAILY v64); live[2] milestone unchanged (10-04 trio in window)
assert ex['outs'][0][0] == u'OS 循环', 'outs[0] anchor mismatch: %s' % ex['outs'][0][0]
ex['outs'][0][2] = OUTS_OS
with io.open(EXP, 'w', encoding='utf-8', newline='') as f:
    json.dump(ex, f, ensure_ascii=False, indent=1)
    f.write(u'\n')

# --- verify parse ---
st = json.load(io.open(STP, encoding='utf-8'))
print('tick=%s ts=%s' % (st['tick'], st['ts']))
print('loglines=%d' % len(st['log']))
print('last log head: %s' % st['log'][-1][:80])
print('task=%s' % st['task'])
print('focus head: %s' % st['focus'][:60])
ex2 = json.load(io.open(EXP, encoding='utf-8'))
print('export_ts=%s results=%d live1=%s' % (ex2['export_ts'], len(ex2['results']), ex2['live'][0][0][:60]))
