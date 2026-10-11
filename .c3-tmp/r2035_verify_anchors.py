# r2035_verify_anchors.py -- ASCII-only anchor verification before close
import io, os, re

ns = os.listdir('orders')
print('has-1008:', 'O-20261008-1105-bm-a.md' in ns)
print('has-0908:', 'O-20260908-1105-bm-a.md' in ns)
tops = sorted(ns, key=lambda f: os.path.getmtime(os.path.join('orders', f)), reverse=True)
print('top3:', tops[:3])

t = io.open('src/os/state.json', encoding='utf-8-sig').read()
print('log-ref-tail:', re.findall(r'O-202\d{5}-1105 mtime 12:08:14', t)[-1])
print('cur-ts:', re.findall(r'"ts": "[^"]+"', t)[-1])
print('cur-task:', re.findall(r'"task": "[^"]+"', t)[-1])
print('tick:', re.findall(r'"tick": \d+', t)[0])
print('r2034-last-log:', t.count('07:16 R2034:'))
print('r2034-committed-line:', re.findall(r'07:16 R2034:[^\n]{0,80}', t)[-1][:100])
