# -*- coding: utf-8 -*-
# R721 fix v2: move R720/R721 log entries after R719 (array-order) + trailing-comma surgery + ts fix
import io, json

def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

p = 'src/os/state.json'; s = rd(p)
i720 = s.find('    "2026-09-30 03:2x R720 断洞修复')
i721 = s.find('    "2026-09-30 04:0x R721:')
assert i720 != -1 and i721 != -1, 'entries not found'
end720 = s.find('\n', i720) + 1
end721 = s.find('\n', i721) + 1
e720 = s[i720:end720]
e721 = s[i721:end721].replace('2026-09-30 04:0x R721:', '2026-09-30 03:4x R721:')
# remove both
s = s[:i720] + s[end720:]
i721b = s.find('    "2026-09-30 04:0x R721:')
end721b = s.find('\n', i721b) + 1
s = s[:i721b] + s[end721b:]
# R719 becomes non-last: append comma to its line
i719 = s.find('    "2026-09-30 02:5x R719:')
assert i719 != -1, 'R719 anchor missing'
end719 = s.find('\n', i719) + 1
assert s[end719-2:end719] == '"\n', 'R719 line does not end with bare quote'
s = s[:end719-1] + ',\n' + e720 + e721.rstrip('\n').rstrip(',') + '\n' + s[end719:]
json.loads(s)  # validate
wr(p, s)
print('state.json v2: order R719->R720->R721 + commas fixed + JSON valid')

p = 'docs/status-export.json'; d = json.loads(rd(p))
d['live'][1][0] = d['live'][1][0].replace('2026-09-30 04:0x', '2026-09-30 03:44')
io.open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=1))
print('export: live ts fixed + JSON valid')
