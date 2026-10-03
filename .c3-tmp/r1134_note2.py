# -*- coding: utf-8 -*-
"""R1134 second-red honest note: extend the existing amendment inside the R1134
log line (before the closing quote, which stays intact this time). One splice,
immediate json verify. ASCII-only source."""
import io, json

p = r'src/os/state.json'
TAILANCHOR = u'\u7ec8\u6001\u6b63\u786e'  # terminal state correct
ADD = (u'\uff1b\u4e8c\u7ea2=r1134_note.py \u622a\u951a\u542b\u6536\u5c3e\u5f15\u53f7\u672a\u56de\u8865'
       u'\u81f4 JSON \u77ac\u65f6\u7834\u635f\u2192r1134_repair.py \u884c\u5c3e\u8865\u5f15\u53f7\u590d\u9a8c\u8fc7'
       u'\uff08\u7ec8\u6001 json.load \u8fc7\u00b7log 1162\uff09\u2014\u2014\u4e24\u7ea2\u7686\u8f6e\u5185'
       u'\u6838\u9a8c\u5373\u63ed\u5373\u4fee\u96f6\u6b8b\u7559')

lines = io.open(p, encoding='utf-8', newline='').readlines()
logidx = max(i for i, l in enumerate(lines) if u'R1134:' in l and l.lstrip().startswith(u'"2026-'))
nl = u'\r\n' if lines[logidx].endswith(u'\r\n') else u'\n'
body = lines[logidx].rstrip(u'\r\n')
assert body.endswith(TAILANCHOR + u'"'), 'unexpected tail: ' + repr(body[-16:])
if u'\u4e8c\u7ea2=r1134_note.py' not in body:
    lines[logidx] = body[:-1] + ADD + u'"' + nl
    io.open(p, 'w', encoding='utf-8', newline='').writelines(lines)
    print('second-red note appended')
else:
    print('already present')

st = json.load(io.open(p, encoding='utf-8'))
assert st['tick'] == 1134 and len(st['log']) == 1162
print('loglines=%d tick=%s ts=%s' % (len(st['log']), st['tick'], st['ts']))
print('log[-1] tail-esc:', st['log'][-1][-90:].encode('unicode_escape')[-190:])
