import io, re

out = io.open(r'.c3-tmp\r798_probe_lines.txt', 'w', encoding='utf-8')
for n in ['board', 'ready', 'loop']:
    t = io.open(r'.c3-tmp\r798_probe_%s.txt' % n, encoding='utf-8', errors='replace').read()
    out.write('==== %s (len %d) ====\n' % (n, len(t)))
    for line in t.splitlines():
        s = line.strip()
        if (not s) or re.search(r'FAIL|WARN|PASS|阻塞|发现|OK|ERROR|fail|warn|pass', s):
            out.write(s[:200].encode('utf-8', 'replace').decode('utf-8') + '\n')
    out.write('\n')
out.close()
print('ok')
