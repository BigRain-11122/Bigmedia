import io, re
t = io.open(r'state/queue/main.md', encoding='utf-8').read()
lines = [l for l in t.splitlines() if re.match(r'^9\. ', l) or re.match(r'^10\. ', l)]
out = ['=== MAIN 9/10 ===']
for l in lines: out.append(l)
e = io.open(r'state/queue/explore.md', encoding='utf-8').read()
out.append('=== EXPLORE 15/16/20/21/23/24/26 ===')
for l in e.splitlines():
    if re.match(r'^(15|16|20|21|23|24|26)\. ', l):
        out.append(l)
        out.append('')
io.open(r'.c3-tmp/r1911_qfull.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('rows=%d' % len(out))
