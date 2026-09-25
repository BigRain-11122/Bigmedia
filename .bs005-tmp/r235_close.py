import json, io, datetime

base = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
p = json.load(io.open(base + r'\.bs005-tmp\r235-payload.json', encoding='utf-8'))
now = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
ts = now[:10] + ' ' + now[11:16]

# state.json: tick+1, append log line, refresh focus
sp = base + r'\src\os\state.json'
raw = io.open(sp, encoding='utf-8').read()
st = json.loads(raw)
assert st['production'] == 'open', 'production gate must stay open (D-BS-06)'
st['log'].append(p['log'].replace('{ts}', ts))
st['tick'] = int(st.get('tick', 0)) + 1
st['focus'] = p['focus']
out = json.dumps(st, ensure_ascii=False, indent=1)
if raw.endswith('\n'):
    out += '\n'
io.open(sp, 'w', encoding='utf-8', newline='\n').write(out)

# status-export.json: P-61 export step (export_ts + derived fields)
ep = base + r'\docs\status-export.json'
raw2 = io.open(ep, encoding='utf-8').read()
ex = json.loads(raw2)
ex['export_ts'] = now
ENG = '\u5de5\u7a0b\u6280\u672f\u90e8'
for d in ex['depts']:
    if d['n'] == ENG:
        d['t'] = p['dept_eng']
OSLOOP = 'OS \u5faa\u73af'
for row in ex['outs']:
    if row[0] == OSLOOP:
        row[2] = p['out_osloop']
ex['results'][0][0] = str(st['tick'])
out2 = json.dumps(ex, ensure_ascii=False, indent=2)
if raw2.endswith('\n'):
    out2 += '\n'
io.open(ep, 'w', encoding='utf-8', newline='\n').write(out2)

print('tick', st['tick'], '| ts', ts, '| log entries', len(st['log']), '| export_ts', ex['export_ts'])
