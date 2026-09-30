# -*- coding: utf-8 -*-
import io
s = io.open('src/os/state.json', 'r', encoding='utf-8', newline='').read()
i = s.rfind(u'\u3014')
print(ascii(s[i:i+60]))
print('cnt_full_anchor=', s.count(u'\u3014\u65b0\u7a97 2/6\u3011"\r\n  ],'))
print('cnt_brk=', s.count(u'\u3014\u65b0\u7a97 2/6\u3011'))
print('cnt_arrclose=', s.count(u'"\r\n  ],'))
print('cnt_logtail_r788=', s.count(u'R788:'))
