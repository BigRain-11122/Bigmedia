import json, subprocess, os

os.chdir(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream')
out = []

with open('src/os/state.json', encoding='utf-8') as f:
    st = json.load(f)
meta = {k: v for k, v in st.items() if k != 'log'}
log = st.get('log', [])
out.append('== META ==')
out.append(json.dumps(meta, ensure_ascii=False, indent=1)[:2000])
out.append('== LOG_TAIL last 3 ==')
for e in log[-3:]:
    out.append(e)
out.append('== log total: %d ==' % len(log))

# git log
r = subprocess.run(['git', 'log', '--oneline', '-8'], capture_output=True, text=True, encoding='utf-8', errors='replace')
out.append('== GIT LOG ==')
out.append(r.stdout)

# orders latest by mtime
try:
    import datetime
    entries = sorted(os.listdir('orders'), key=lambda n: os.path.getmtime(os.path.join('orders', n)))
    out.append('== orders by mtime (last 5):')
    for n in entries[-5:]:
        out.append('%s  %s' % (n, datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join('orders', n))).strftime('%Y-%m-%d %H:%M')))
except Exception as e:
    out.append('ORD ERR: %s' % e)

# group ledger scan: count @BigStream lines
led = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
try:
    with open(led, encoding='utf-8') as f:
        lines = f.readlines()
    atbs = [l for l in lines if '@BigStream' in l]
    out.append('== LEDGER @BigStream lines: %d ==' % len(atbs))
    out.append('last @BigStream line: ' + (atbs[-1][:300] if atbs else 'none'))
    out.append('== ledger total lines: %d ==' % len(lines))
    out.append('== ledger last 3 lines ==')
    for l in lines[-3:]:
        out.append(l.strip()[:300])
except Exception as e:
    out.append('LEDGER ERR: %s' % e)

# decisions.md non-empty line count
dec = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
try:
    with open(dec, encoding='utf-8') as f:
        dl = [l for l in f.readlines() if l.strip()]
    out.append('== DECISIONS non-empty lines: %d ==' % len(dl))
    out.append('last line: ' + dl[-1][:300])
except Exception as e:
    out.append('DEC ERR: %s' % e)

with open('.c3-tmp/r749_probe.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
