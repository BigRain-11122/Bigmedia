import io, json
d = json.load(io.open(r'docs\status-export.json', encoding='utf-8-sig'))
out = []
out.append('depts type: %s' % type(d['depts']).__name__)
dep = d['depts']
if isinstance(dep, dict):
    out.append('depts keys: %s' % list(dep.keys()))
    for k, v in dep.items():
        sv = json.dumps(v, ensure_ascii=False)
        if '666' in sv or 'tick' in sv.lower() or 'OS' in str(k):
            out.append('KEY=%s -> %s' % (k, sv[:400]))
elif isinstance(dep, list):
    out.append('depts len: %d' % len(dep))
    for it in dep:
        sv = json.dumps(it, ensure_ascii=False)
        if '666' in sv or 'OS' in sv:
            out.append('ITEM -> %s' % sv[:400])
io.open(r'.c3-tmp\r667_se_probe.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('WROTE', len(out), 'lines')
