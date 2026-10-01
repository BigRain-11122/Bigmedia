# -*- coding: utf-8 -*-
# R910 task-field fix: strip date-time only, keep 'R910: ' prefix (R909 convention)
import io, json, re, datetime

SP = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json'
st = json.loads(io.open(SP, 'r', encoding='utf-8-sig').read())
line = st['log'][-1]
assert line.startswith('2026-10-02 ') and 'R910: ' in line[:40], 'unexpected log tail'
body = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2} ', '', line)  # strip date-time only
st['task'] = body[:60]
st['ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
io.open(SP, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=1))

st2 = json.loads(io.open(SP, 'r', encoding='utf-8-sig').read())
assert st2['task'].startswith('R910: '), st2['task'][:20]
assert st2['tick'] == 910
io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r910_task_check.txt', 'w', encoding='utf-8').write(
    'tick=%d\nts=%s\ntask=%s\nwm_new=%s\nboard_rows=%d\nlog_head=%s\n' % (
        st2['tick'], st2['ts'], st2['task'],
        ','.join(d for d in ['D-20261002-01', 'D-20261002-02', 'D-20261002-03'] if d in st2['decisions_watermark']['dnums']),
        st2['decisions_watermark']['board_rows'], st2['log'][-1][:30]))
print('OK')
