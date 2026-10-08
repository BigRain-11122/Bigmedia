import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
t = open('output/renders/README.md', encoding='utf-8').read().splitlines()
for i, l in enumerate(t):
    if l.startswith('| 文件') or l.startswith('| 名') or (i < 40 and l.startswith('|---')):
        print(i, l[:200])
for i, l in enumerate(t):
    if 'bs-016' in l:
        print('ROW', i)
        print(l)
        break
