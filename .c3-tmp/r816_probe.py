# -*- coding: utf-8 -*-
import io
t = io.open(r'src/os/state.json', encoding='utf-8').read()
print('line-ending:', 'CRLF' if '\r\n' in t else 'LF')
print('bom:', 'yes' if t.startswith(u'\ufeff') else 'no')
print('tick815 count:', t.count(u'"tick": 815,'))
print('ts 07:13:58 count:', t.count(u'07:13:58'))
print('focus R815 count:', t.count(u'"focus": "R815:'))
print('task R815 count:', t.count(u'"task": "' + u'\u7b49\u5f85\u6001\u58f0\u660e\u6536\u8f6e\u00b7\u58f0\u660e\u8f6e\u5e76\u7a97\u7b2c 5 \u8f6e'))
anchor_lf = u'"\n  ],\n  "ts": "2026-10-01 07:13:58",'
anchor_crlf = u'"\r\n  ],\r\n  "ts": "2026-10-01 07:13:58",'
print('anchor_lf count:', t.count(anchor_lf))
print('anchor_crlf count:', t.count(anchor_crlf))
print('tail120:', repr(t[-120:]))
