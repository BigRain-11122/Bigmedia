import json
p = r'docs\status-export.json'
d = json.load(open(p, encoding='utf-8'))
print('keys:', list(d.keys()))
for k in d:
    v = d[k]
    if isinstance(v, list):
        print(k, 'list len', len(v), '->', json.dumps(v[-2:], ensure_ascii=False)[:300] if v else '')
    elif isinstance(v, dict):
        print(k, 'dict keys', list(v.keys())[:12])
    else:
        print(k, '=', json.dumps(v, ensure_ascii=False)[:200])
