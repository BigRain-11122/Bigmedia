# -*- coding: utf-8 -*-
"""R1134 log-line amendment: append honest note about the close-script write-order
bug (insert lost between passes) that was caught by in-round verify and fixed.
Operates on the R1134 log line only; re-verifies JSON. ASCII-only source."""
import io, json

p = r'src/os/state.json'
st = json.load(io.open(p, encoding='utf-8'))
last = st['log'][-1]
assert last.startswith(u'2026-10-03 19:2x R1134:'), 'unexpected last log line: ' + last[:30]

NOTE = (u'\uff1b\u968f\u884c\u4fee\u7ea2\u5982\u5b9e\u5165\u8d26=r1134_close.py '
        u'\u9996\u8d71 insert \u540e\u672a\u5199\u76d8\u5373\u88ab\u4e8c\u8d71\u91cd\u8bfb\u8986\u76d6'
        u'\uff08R1134 log \u884c\u4e00\u5ea6\u4e22\u5931\uff09\u2192r1134_verify \u6838\u9a8c\u5373\u63ed'
        u'\u2192r1134_fix.py \u8865\u63d2+\u524d\u884c\u5c3e\u9017\u53f7\u5355\u5199\u76d8\u590d\u9a8c\u8fc7'
        u'\uff08log 1161\u21921162\u00b7json.load \u8fc7\uff09\u00b7\u6839\u56e0=\u6536\u8d26\u5de5\u5177'
        u'\u5199\u76d8\u5e8f\u7f3a\u9677\u975e\u53f0\u8d26\u53d8\u5316\u00b7\u7ec8\u6001\u6b63\u786e')

if NOTE[:20] not in last:
    lines = io.open(p, encoding='utf-8', newline='').readlines()
    logidx = max(i for i, l in enumerate(lines) if u'R1134:' in l and l.lstrip().startswith(u'"2026-'))
    nl = u'\r\n' if lines[logidx].endswith(u'\r\n') else u'\n'
    body = lines[logidx].rstrip(u'\r\n')
    assert body.endswith(u'\uff3d"'), 'unexpected line tail: ' + repr(body[-8:])
    # insert note before the closing bracket of the trailing window note
    cut = body.rfind(u'\u7a97\u6ee1 batch close\uff3d"')
    assert cut > 0, 'anchor not found'
    newbody = body[:cut] + u'\u7a97\u6ee1 batch close\uff3d' + NOTE + body[cut + len(u'\u7a97\u6ee1 batch close\uff3d"'):]
    lines[logidx] = newbody + nl
    io.open(p, 'w', encoding='utf-8', newline='').writelines(lines)
    print('note appended, logidx', logidx)
else:
    print('note already present')

st = json.load(io.open(p, encoding='utf-8'))
print('loglines=%d tick=%s ts=%s' % (len(st['log']), st['tick'], st['ts']))
print('log[-1] tail-esc:', st['log'][-1][-80:].encode('unicode_escape')[-160:])
