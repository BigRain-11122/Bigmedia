# r1985: get exact tail of tech.md (append anchor for new item 105)
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('state/queue/tech.md', encoding='utf-8').read()
last = t.rstrip('\n').splitlines()[-1]
print('LEN=', len(last))
print('TAIL:', last[-200:])
