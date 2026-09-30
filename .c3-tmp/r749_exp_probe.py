# -*- coding: utf-8 -*-
import io, json
E = json.load(io.open('docs/status-export.json', encoding='utf-8'))
out = []
out.append('keys: ' + ', '.join(E.keys()))
for k, v in E.items():
    if isinstance(v, list):
        out.append('%s: list len=%d; first elem type=%s; sample=%s' % (k, len(v), type(v[0]).__name__ if v else '-', json.dumps(v[0], ensure_ascii=False)[:220] if v else '-'))
    else:
        out.append('%s: %s' % (k, json.dumps(v, ensure_ascii=False)[:220]))
io.open('.c3-tmp/r749_exp.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('OK')
