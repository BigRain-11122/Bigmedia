# -*- coding: utf-8 -*-
"""R234 fast-path state reader: dump state.json essentials to UTF-8 file (console GBK safe)."""
import json, re, io

d = json.load(io.open('src/os/state.json', encoding='utf-8'))
out = []
out.append('keys=%s' % ','.join(sorted(d.keys())))
out.append('tick=%s' % d.get('tick'))
for k in sorted(d.keys()):
    if k not in ('log',):
        v = d[k]
        if isinstance(v, (str, int, float, bool)) or v is None:
            out.append('%s=%s' % (k, v))
        elif isinstance(v, dict):
            out.append('%s=%s' % (k, json.dumps(v, ensure_ascii=False)[:300]))

log = d.get('log', [])
out.append('log_len=%d' % len(log))
for e in log[-4:]:
    s = e if isinstance(e, str) else json.dumps(e, ensure_ascii=False)
    out.append('===ENTRY len=%d===' % len(s))
    out.append('HEAD: ' + s[:200])
    for kw in ('ledger', 'decisions', 'idle', '探针', 'board'):
        hits = list(re.finditer(kw, s))
        for m in hits[:2]:
            frag = s[max(0, m.start() - 15):m.start() + 100].replace('\n', ' ')
            out.append('FRAG[%s]: %s' % (kw, frag))

res = '\n'.join(out)
io.open('.bs005-tmp/r234-fast-u8.txt', 'w', encoding='utf-8').write(res)
print('written chars=%d entries=%d' % (len(res), len(log)))
