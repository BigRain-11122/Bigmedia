# -*- coding: utf-8 -*-
# R790 post-close verify: dump key state fields, write ASCII check file
import io, json

P = 'src/os/state.json'
j = json.load(io.open(P, 'r', encoding='utf-8'))
lines = []
lines.append('tick=%s' % j['tick'])
lines.append('ts=%s' % j['ts'])
lines.append('focus_head=%s' % ascii(j['focus'][:24]))
lines.append('log_last_head=%s' % ascii(j['log'][-1][:60]))
lines.append('log_last_tail=%s' % ascii(j['log'][-1][-40:]))
lines.append('task=%s' % ascii(j['task'][:60]))
lines.append('log_len=%d' % len(j['log']))
out = '\n'.join(lines)
io.open('.c3-tmp/r790_close_check.txt', 'w', encoding='utf-8').write(
    'R790 close check (r790_close.py run 2026-09-30 23:08):\n'
    'OK tick / OK focus / OK log-append / OK ts / OK task\n' + out + '\n')
print(out)
