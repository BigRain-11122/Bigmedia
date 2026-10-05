# -*- coding: utf-8 -*-
# r1351 state accounting: append log line, tick+1, refresh ts+task fields (PT-20260925-02 law)
import json, io, re, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = os.path.join(ROOT, 'src', 'os', 'state.json')

line = io.open(os.path.join(ROOT, '.c3-tmp', 'r1351_logline.txt'), encoding='utf-8').read().strip()

st = json.load(io.open(SP, encoding='utf-8'))
assert st.get('tick') == 1350, 'unexpected tick %s' % st.get('tick')
st['tick'] = st.get('tick', 0) + 1
st['ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
task_src = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}x?\s*', '', line)
st['task'] = task_src[:60]
st.setdefault('log', []).append(line)

io.open(SP, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2) + '\n')
print('tick=%s ts=%s' % (st['tick'], st['ts']))
print('task=%s' % st['task'])
print('log_len=%d last_line_len=%d' % (len(st['log']), len(st['log'][-1])))
