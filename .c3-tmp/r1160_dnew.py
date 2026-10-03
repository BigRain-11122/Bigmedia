import io, re
t = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', encoding='utf-8').read()
lines = t.splitlines()
out = []
hits = [i for i, l in enumerate(lines) if re.search(r'D-20261004-0[12]', l)]
for i in hits:
    out.append('L%d: %s' % (i+1, lines[i]))
io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1160_dnew.txt', 'w', encoding='utf-8').write('\n\n'.join(out))
print('written', len(hits))
