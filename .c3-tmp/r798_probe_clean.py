import io, re

def clean(t):
    t = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', t)
    t = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', t)
    return t

out = io.open(r'.c3-tmp\r798_probe_clean.txt', 'w', encoding='utf-8')
for n in ['board', 'ready', 'loop']:
    t = clean(io.open(r'.c3-tmp\r798_probe_%s.txt' % n, encoding='utf-8', errors='replace').read())
    out.write('==== %s ====\n' % n)
    lines = [l for l in t.splitlines() if l.strip()]
    out.write('\n'.join(lines[:14]) + '\n...\n' + '\n'.join(lines[-30:]) + '\n\n')
out.close()
print('ok')
