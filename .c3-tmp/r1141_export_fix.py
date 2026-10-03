# -*- coding: utf-8 -*-
"""R1141 export-only fix: r1141_close.py applied state.json successfully then
failed on outs[0][2] (OS-loop row is a 2-element array: name + text, unlike
the 3-element rows). This script redoes ONLY the status-export.json update.
Texts re-loaded from r1141_texts.txt (UTF-8 data file, ASCII body)."""
import io, json, datetime

EXP = r'docs\status-export.json'
STP = r'src\os\state.json'
TXP = r'.c3-tmp\r1141_texts.txt'

stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
hhmm = stamp[11:16]

# state sanity: the log append must be exactly once, tick already 1141
st = json.load(io.open(STP, encoding='utf-8'))
assert st['tick'] == 1141, 'tick must already be 1141, got %s' % st['tick']
n1141 = sum(1 for x in st['log'] if x.startswith(u'2026-10-03 20:') and u' R1141:' in x[:40])
assert n1141 == 1, 'R1141 log line must appear exactly once, got %d' % n1141
print('state ok: tick=%s, R1141 log lines=%d, ts=%s' % (st['tick'], n1141, st['ts']))

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

RESULT = secs['RESULT'].replace('20:4x', hhmm)
LIVE1 = secs['LIVE1'].replace('20:4x', hhmm)
OUTS_OS = secs['OUTS_OS']

ex = json.load(io.open(EXP, encoding='utf-8'))
assert ex['export_ts'] == '2026-10-03 19:33:49', 'unexpected export_ts anchor: %s' % ex['export_ts']
assert ex['outs'][0][0] == u'OS 循环', 'outs[0] anchor mismatch: %s' % ex['outs'][0][0]
assert len(ex['outs'][0]) == 2, 'outs[0] expected 2 elements, got %d' % len(ex['outs'][0])
ex['export_ts'] = stamp
ex['results'].append(['1141', RESULT])
ex['live'][0][0] = LIVE1
ex['outs'][0][1] = OUTS_OS
with io.open(EXP, 'w', encoding='utf-8', newline='') as f:
    json.dump(ex, f, ensure_ascii=False, indent=1)
    f.write(u'\n')

ex2 = json.load(io.open(EXP, encoding='utf-8'))
print('export_ts=%s results=%d' % (ex2['export_ts'], len(ex2['results'])))
print('live1=%s' % ex2['live'][0][0][:70])
print('outs_os_head=%s' % ex2['outs'][0][1][:60])
