import io, re
lines = io.open('state/queue/tech.md', encoding='utf-8').read().splitlines()
for l in lines:
    if re.match(r'^\d+\.', l) and '[done' not in l:
        print(l[:220])
print('=== explore (open, head) ===')
el = io.open('state/queue/explore.md', encoding='utf-8').read().splitlines()
n = 0
for l in el:
    if l.startswith('#') or not l.strip() or '[done' in l:
        continue
    print(l[:220]); n += 1
    if n >= 8:
        break
