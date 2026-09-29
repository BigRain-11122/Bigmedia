# -*- coding: utf-8 -*-
# R721 fix: log entry order (must be after R719) + real timestamps + JSON validation
import io, json

def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

# ---- state.json ----
p = 'src/os/state.json'; s = rd(p)
i720 = s.find('    "2026-09-30 03:2x R720 断洞修复')
i721 = s.find('    "2026-09-30 04:0x R721:')
assert i720 != -1 and i721 != -1, 'entries not found'
# extract the two entries (each ends with ",\n")
end720 = s.find('\n', i720) + 1
end721 = s.find('\n', i721) + 1
e720 = s[i720:end720]
e721 = s[i721:end721]
# remove them
s = s[:i720] + s[end720:]
i721 = s.find('    "2026-09-30 04:0x R721:')
end721 = s.find('\n', i721) + 1
s = s[:i721] + s[end721:]
# fix timestamps 04:0x -> 03:4x
e721 = e721.replace('2026-09-30 04:0x R721:', '2026-09-30 03:4x R721:')
# re-insert AFTER the R719 line
i719 = s.find('    "2026-09-30 02:5x R719:')
assert i719 != -1, 'R719 anchor missing'
end719 = s.find('\n', i719) + 1
s = s[:end719] + e720 + e721 + s[end719:]
json.loads(s)  # validate
wr(p, s)
print('state.json: order fixed + ts 03:4x + JSON valid')

# ---- export live[1] ts text ----
p = 'docs/status-export.json'; d = json.loads(rd(p))
d['live'][1][0] = d['live'][1][0].replace('2026-09-30 04:0x', '2026-09-30 03:44')
io.open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=1))
print('export: live ts fixed + JSON valid')
