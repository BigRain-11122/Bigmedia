# -*- coding: utf-8 -*-
"""Verify R1134 state close: log tail order + tick/ts/task/focus fields."""
import io, json

p = r'src/os/state.json'
lines = io.open(p, encoding='utf-8').readlines()
idx = [i for i, l in enumerate(lines) if l.lstrip().startswith(u'"2026-')]
print('total lines', len(lines))
print('dated-line idx tail:', idx[-3:], 'of', len(lines))
# show context around last dated line
for i in range(idx[-1] - 1, min(idx[-1] + 3, len(lines))):
    print(i, repr(lines[i][:60])[:90], '...TAIL:', repr(lines[i][-40:])[:70])
st = json.load(io.open(p, encoding='utf-8'))
print('log array len', len(st['log']))
print('log[-1] head-esc:', st['log'][-1][:50].encode('unicode_escape')[:100])
print('log[-2] head-esc:', st['log'][-2][:50].encode('unicode_escape')[:100])
print('tick', st['tick'], '| ts', st['ts'])
print('task-esc:', st['task'].encode('unicode_escape')[:80])
print('focus-esc head:', st['focus'][:40].encode('unicode_escape')[:80])
