import io, json
s = json.load(io.open(r'src/os/state.json', encoding='utf-8'))
hits = [(i, l) for i, l in enumerate(s['log']) if 'day-close' in l or 'DAILY v64' in l]
out = ['day-close mentions: %d' % len(hits)]
for i, l in hits[-4:]:
    out.append('---')
    out.append(l[:800])
io.open(r'.c3-tmp/r1122_dclose.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('OK')
