# R278 fix trailing comma in state.json log array (R256-lesson instant repair + JSON_OK revalidate)
import io, json

P = r'src/os/state.json'
t = io.open(P, encoding='utf-8').read()
bad = '收账显式列文件 commit+push。",\n ],'
good = '收账显式列文件 commit+push。"\n ],'
assert t.count(bad) == 1, 'bad pattern count=%d' % t.count(bad)
t = t.replace(bad, good)
io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
j = json.load(io.open(P, encoding='utf-8'))
print('JSON_OK tick=%d log=%d ts=%s' % (j['tick'], len(j['log']), j['ts']))
print('task:', j['task'])
