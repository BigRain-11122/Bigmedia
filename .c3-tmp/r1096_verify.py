import io, json
st = json.load(io.open(r'src\os\state.json', encoding='utf-8'))
out = io.open(r'.c3-tmp\r1096_verify.txt', 'w', encoding='utf-8')
out.write('tick=%s\nts=%s\nlog_count=%d\n\n' % (st['tick'], st['ts'], len(st['log'])))
out.write('task=%s\n\n' % st['task'])
out.write('focus=%s\n\n' % st['focus'])
out.write('log_tail_last=%s\n' % st['log'][-1][:400])
out.close()
print('verify written')
