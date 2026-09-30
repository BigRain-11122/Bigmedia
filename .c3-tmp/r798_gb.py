import re
t = open(r'docs/global-benchmarks.md', encoding='utf-8').read()
out = open(r'.c3-tmp/r798_gb.txt', 'w', encoding='utf-8')
out.write('total chars %d, lines %d\n' % (len(t), len(t.splitlines())))
# find W2 / knife mentions
for m in re.finditer(r'(?m)^.*(?:W2|下扫刀|余刀|刀[①②③④⑤]).*$', t):
    out.write('L: ' + m.group(0)[:500] + '\n\n')
out.write('==== update-record section head ====\n')
i = t.find('更新记录')
out.write(t[i:i+3000])
out.close()
print('ok')
