# -*- coding: utf-8 -*-
"""R1134 note-append repair: the previous amendment split at an anchor that
included the JSON closing quote and did not re-add it, so the R1134 log line
lost its terminating quote (json invalid: control char at line end). Re-add
the closing quote and verify. ASCII-only source."""
import io, json

p = r'src/os/state.json'
lines = io.open(p, encoding='utf-8', newline='').readlines()
logidx = max(i for i, l in enumerate(lines) if u'R1134:' in l and l.lstrip().startswith(u'"2026-'))
nl = u'\r\n' if lines[logidx].endswith(u'\r\n') else u'\n'
body = lines[logidx].rstrip(u'\r\n')
print('line', logidx, 'tail before fix:', repr(body[-30:]))
if not body.endswith(u'"'):
    assert body.endswith(u'\u7ec8\u6001\u6b63\u786e'), 'unexpected tail: ' + repr(body[-12:])
    lines[logidx] = body + u'"' + nl
    io.open(p, 'w', encoding='utf-8', newline='').writelines(lines)
    print('closing quote re-added')
else:
    print('tail already quoted, no fix')

st = json.load(io.open(p, encoding='utf-8'))
print('loglines=%d tick=%s ts=%s' % (len(st['log']), st['tick'], st['ts']))
print('log[-1] tail-esc:', st['log'][-1][-100:].encode('unicode_escape')[-200:])
print('task-esc:', st['task'].encode('unicode_escape')[:70])
print('focus-head-esc:', st['focus'][:30].encode('unicode_escape')[:60])
