import io

def read_any(p):
    raw = open(p, 'rb').read()
    for enc in ('utf-16', 'utf-8', 'gbk'):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode('utf-8', errors='replace')

out = []
b = read_any('.c3-tmp/r933_board.txt')
out.append('== BOARD ==')
out.append(b.strip())
r = read_any('.c3-tmp/r933_rd.txt')
rl = r.splitlines()
out.append('== READINESS == lines=%d' % len(rl))
key = [l for l in rl if ('FAIL' in l or 'PASS' in l or 'blocker' in l.lower() or 'finding' in l.lower() or 'CEO' in l)]
out.extend(key if key else rl[-15:])
lp = read_any('.c3-tmp/r933_loop.txt')
ll = lp.splitlines()
fails = [l for l in ll if 'FAIL' in l]
warns = [l for l in ll if 'WARN' in l]
out.append('== LOOP_HEALTH == lines=%d FAIL=%d WARN=%d' % (len(ll), len(fails), len(warns)))
out.extend(fails)
with io.open('.c3-tmp/r933_probe_summary.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('summary written, lines=%d' % len(out))
