# -*- coding: utf-8 -*-
import io, json
d = json.load(io.open(r'src\os\state.json', encoding='utf-8'))
out = ['tick=%s' % d['tick'], 'ts=%s' % d['ts'], 'task=%s' % d['task'][:70], 'focus_head=%s' % d['focus'][:60]]
e = json.load(io.open(r'docs\status-export.json', encoding='utf-8'))
out.append('export_ts=%s' % e['export_ts'])
out.append('live_current=%s' % e['live'][0][0][:80])
io.open(r'.c3-tmp\r1322_verify.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok')
