import json, re, io
d = json.load(open('src/os/state.json', encoding='utf-8'))
log = d['log']
pats = re.compile(u'\u76d8\u70b9 015|DIGEST-v15|E33|derive \u76f2\u533a|\u89e6\u53d1\u5f8b')
out = []
for x in log:
    m = re.match(r'\S+ \S+ (R\d+):', x)
    if m and int(m.group(1)[1:]) >= 1096 and pats.search(x):
        out.append(x[:500])
open('.c3-tmp/v15_grep.txt', 'w', encoding='utf-8').write('\n---\n'.join(out[-10:]) if out else 'NO trigger-law/DIGEST-v15/derive mentions in R1096+ logs')
print('hits=%d' % len(out))
