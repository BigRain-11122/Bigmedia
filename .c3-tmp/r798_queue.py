import re, os, datetime

out = open(r'.c3-tmp\r798_queue.txt', 'w', encoding='utf-8')
out.write('NOW: %s\n\n' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

q = open(r'docs/self-improvement-queue.md', encoding='utf-8').read()
out.write('=== queue len %d ===\n' % len(q.splitlines()))
# dump section D and E headers + top rows
for sec in re.finditer(r'(?m)^#+ .*$', q):
    out.write('SEC: ' + sec.group(0) + '\n')
out.write('\n=== queue tail 120 lines ===\n')
out.write('\n'.join(q.splitlines()[-120:]) + '\n')
out.close()
print('ok')
