# R763 fix: log line timestamp prefix was doubled ("2026-09-30 2026-09-30 18:x R763:")
import json

BAD = "2026-09-30 2026-09-30 18:x R763:"
GOOD = "2026-09-30 18:2x R763:"

p = 'src/os/state.json'
raw = open(p, encoding='utf-8').read()
st = json.loads(raw)
assert st['log'][-1].startswith(BAD), 'unexpected log tail: %r' % st['log'][-1][:60]
st['log'][-1] = GOOD + st['log'][-1][len(BAD):]
st['task'] = st['log'][-1].split('R763: ', 1)[1][:60]
open(p, 'w', encoding='utf-8', newline='\n').write(
    json.dumps(st, ensure_ascii=False, indent=2) + ('\n' if raw.endswith('\n') else ''))

q = 'docs/status-export.json'
raw2 = open(q, encoding='utf-8').read()
ex = json.loads(raw2)
assert ex['results'][-1][0] == '763' and ex['results'][-1][1].startswith(BAD)
ex['results'][-1][1] = GOOD + ex['results'][-1][1][len(BAD):]
open(q, 'w', encoding='utf-8', newline='\n').write(
    json.dumps(ex, ensure_ascii=False, indent=1) + ('\n' if raw2.endswith('\n') else ''))

import io
st2 = json.load(open(p, encoding='utf-8'))
ex2 = json.load(open(q, encoding='utf-8'))
o = io.open('.c3-tmp/r763_verify2.txt', 'w', encoding='utf-8')
o.write('log_tail=' + st2['log'][-1][:100] + '\n')
o.write('task=' + st2['task'] + '\n')
o.write('res763_head=' + ex2['results'][-1][1][:100] + '\n')
o.write('json_valid=True\n')
o.close()
print('FIX_OK')
