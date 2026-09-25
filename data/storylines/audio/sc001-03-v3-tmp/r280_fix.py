# R280 fix: remove trailing comma after last log entry (r280_state.py tail pattern bug; UTF-8 channel)
import io, json

P = r'src/os/state.json'
t = io.open(P, encoding='utf-8').read()
bad = u'\u6536\u8d26\u663e\u5f0f\u5217\u6587\u4ef6 commit+push\u3002",' + '\n ],'
good = u'\u6536\u8d26\u663e\u5f0f\u5217\u6587\u4ef6 commit+push\u3002"' + '\n ],'
cnt = t.count(bad)
assert cnt == 1, 'bad anchor count=%d' % cnt
t = t.replace(bad, good)
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
j = json.load(io.open(P, encoding='utf-8'))
print('JSON_OK tick=%d log=%d ts=%s' % (j['tick'], len(j['log']), j['ts']))
print('task:', j['task'])
print('log_tail_ok:', j['log'][-1][-40:])
