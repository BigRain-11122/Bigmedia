# -*- coding: utf-8 -*-
import io
q = io.open(r'docs\self-improvement-queue.md', encoding='utf-8').read()
lines = q.splitlines()
idx = [i for i, l in enumerate(lines) if 'E30' in l]
print('E30 lines at:', idx)
for i in idx:
    for j in range(max(0, i - 2), min(len(lines), i + 4)):
        print(j, lines[j][:220])
    print('---')
