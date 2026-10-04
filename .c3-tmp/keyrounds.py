import json, re
d = json.load(open('src/os/state.json', encoding='utf-8'))
log = d['log']
out = []
for x in log:
    m = re.match(r'\S+ \S+ (R\d+):', x)
    if m and m.group(1) in ('R1096', 'R1123', 'R1160', 'R1229'):
        out.append(x[:2600])
open('.c3-tmp/keyrounds.txt', 'w', encoding='utf-8').write('\n\n=====\n\n'.join(out))
print('found=%d' % len(out))
