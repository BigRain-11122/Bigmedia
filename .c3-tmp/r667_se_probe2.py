import io, json
d = json.load(io.open(r'docs\status-export.json', encoding='utf-8-sig'))
out = []
for key in ('outs', 'chips'):
    v = d[key]
    out.append('%s type=%s' % (key, type(v).__name__))
    if isinstance(v, list):
        out.append('  len=%d' % len(v))
        for it in v:
            sv = json.dumps(it, ensure_ascii=False)
            out.append('  ITEM: %s' % sv[:300])
    elif isinstance(v, dict):
        for k2, v2 in v.items():
            out.append('  %s: %s' % (k2, json.dumps(v2, ensure_ascii=False)[:300]))
full = json.dumps(d, ensure_ascii=False)
i = full.find('OS')
out.append('first OS ctx: %s' % full[max(0,i-100):i+200])
out.append('results[0]: %s' % json.dumps(d['results'][0], ensure_ascii=False)[:200])
io.open(r'.c3-tmp\r667_se_probe2.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('WROTE', len(out))
