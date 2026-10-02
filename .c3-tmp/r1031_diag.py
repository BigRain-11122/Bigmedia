import io
p = r'data\storylines\cards\MC-20261003-DAILY-v61-tmp\build_daily_v61.py'
ls = io.open(p, encoding='utf-8').read().split('\n')
for i in range(210, 218):
    l = ls[i]
    tail = repr(l[-14:])
    print(i + 1, 'Q-END' if l.rstrip().endswith('"') else 'NO-Q', tail)
try:
    compile(io.open(p, encoding='utf-8').read(), p, 'exec')
    print('COMPILE OK')
except SyntaxError as e:
    print('SYNTAX ERR line', e.lineno, 'offset', e.offset)
