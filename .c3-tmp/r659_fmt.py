# -*- coding: utf-8 -*-
import io, os, json, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
h = subprocess.run(['git', 'show', 'HEAD:docs/status-export.json'], capture_output=True).stdout.decode('utf-8', 'replace')
c = io.open('docs/status-export.json', encoding='utf-8').read()

out = io.open(os.path.join('.c3-tmp', 'r659_fmt.txt'), 'w', encoding='utf-8')
out.write('HEAD len %d lines %d\n' % (len(h), len(h.splitlines())))
out.write('CUR  len %d lines %d\n' % (len(c), len(c.splitlines())))
out.write('HEAD raw_chinese_early=%s escape_u=%s\n' % ('\u5a92' in h[:2000], '\\\\u' in h[:2000]))
out.write('CUR  raw_chinese_early=%s escape_u=%s\n' % ('\u5a92' in c[:2000], '\\\\u' in c[:2000]))
hl = h.splitlines()
cl = c.splitlines()
out.write('HEAD line2: %r\n' % hl[2][:70] if len(hl) > 2 else 'HEAD short\n')
out.write('CUR  line2: %r\n' % cl[2][:70] if len(cl) > 2 else 'CUR short\n')
# semantic equality check: parse both, compare ignoring my known changes
dh = json.loads(h)
dc = json.loads(c)
out.write('HEAD keys %s\n' % sorted(dh.keys()))
out.write('CUR  keys %s\n' % sorted(dc.keys()))
out.write('HEAD results n=%d first_tick=%s last_tick=%s\n' % (len(dh.get('results', [])), dh['results'][0][0] if dh.get('results') else '-', dh['results'][-1][0] if dh.get('results') else '-'))
out.write('CUR  results n=%d first_tick=%s last_tick=%s\n' % (len(dc.get('results', [])), dc['results'][0][0] if dc.get('results') else '-', dc['results'][-1][0] if dc.get('results') else '-'))
out.close()
print('ok')
