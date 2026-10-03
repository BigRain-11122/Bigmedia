# -*- coding: utf-8 -*-
"""R1135 declared-idle 6/6 batch close: state.json (tick/log/focus/ts/task)
+ status-export.json (export_ts / outs[0] / results append / live 3 lines).
Chinese text read from r1135_texts.txt (UTF-8 data file) so this script
body stays ASCII per encoding law. Evidence: r1135_check.txt + probes."""
import io, json, datetime

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
STP = ROOT + r'\src\os\state.json'
EXP = ROOT + r'\docs\status-export.json'
TXP = ROOT + r'\.c3-tmp\r1135_texts.txt'

now = datetime.datetime.now()
stamp = now.strftime('%Y-%m-%d %H:%M:%S')

# parse sections
sec = {}
cur = None
for ln in io.open(TXP, encoding='utf-8').read().splitlines():
    if ln.startswith('===') and ln.endswith('==='):
        cur = ln[3:-3]
        sec[cur] = []
    elif cur:
        sec[cur].append(ln)
TXT = dict((k, u'\n'.join(v).strip()) for k, v in sec.items())

LOG = TXT['LOG'].replace('{TS}', stamp)
FOCUS = TXT['FOCUS']
LIVE1 = TXT['LIVE1'].replace('{TS}', stamp)
LIVE2 = TXT['LIVE2']
LIVE3 = TXT['LIVE3']
OUTS = TXT['OUTS']
RESULT = TXT['RESULT']
TASK = LOG.split(u' ', 2)[2][:60]

# ---- state.json ----
lines = io.open(STP, encoding='utf-8', newline='').readlines()
logidx = max(i for i, l in enumerate(lines) if l.lstrip().startswith('"2026-'))
nl = u'\r\n' if lines[logidx].endswith(u'\r\n') else u'\n'
body = lines[logidx].rstrip(u'\r\n')
if not body.endswith(u','):
    lines[logidx] = body + u',' + nl
indent = u'    '
lines.insert(logidx + 1, indent + u'"' + LOG.replace(u'"', u'\\"') + u'"' + nl)

out = []
for l in lines:
    ls = l.lstrip()
    if ls.startswith(u'"tick":'):
        out.append(u'  "tick": 1135,' + nl)
    elif ls.startswith(u'"ts":'):
        out.append(u'  "ts": ' + json.dumps(stamp, ensure_ascii=False) + u',' + nl)
    elif ls.startswith(u'"task":'):
        out.append(u'  "task": ' + json.dumps(TASK, ensure_ascii=False) + nl)
    elif ls.startswith(u'"focus":'):
        out.append(u'  "focus": ' + json.dumps(FOCUS, ensure_ascii=False) + u',' + nl)
    else:
        out.append(l)
io.open(STP, 'w', encoding='utf-8', newline='').writelines(out)

# ---- status-export.json ----
ex = json.load(io.open(EXP, encoding='utf-8'))
ex['export_ts'] = stamp
ex['outs'][0][1] = OUTS
ex['results'].append([u'1135', RESULT])
ex['live'] = [[LIVE1], [LIVE2], [LIVE3]]
io.open(EXP, 'w', encoding='utf-8', newline='').write(
    json.dumps(ex, ensure_ascii=False, indent=1) + u'\n')

# ---- verify ----
st = json.load(io.open(STP, encoding='utf-8'))
ex2 = json.load(io.open(EXP, encoding='utf-8'))
print('tick=%s ts=%s' % (st['tick'], st['ts']))
print('loglines=%d last head: %s' % (len(st['log']), st['log'][-1][:50]))
print('task=%s' % st['task'])
print('focus head: %s' % st['focus'][:50])
print('export_ts=%s results=%d live1=%s' % (ex2['export_ts'], len(ex2['results']), ex2['live'][0][0][:60]))
