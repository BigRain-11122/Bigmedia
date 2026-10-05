# -*- coding: utf-8 -*-
# r1343 fix: restore JSON validity of state.json log array
# issue A: previous last element (R1342 line) has no trailing comma before newly appended R1343 line
# issue B: newly appended R1343 line carries a trailing comma before ] (invalid JSON)
import sys

p = 'src/os/state.json'
raw = open(p, 'rb').read()

def ctx(b, i, n=40):
    return repr(b[max(0,i-n):i+n])

# diagnostics: show boundary around R1343 line start
i = raw.find('2026-10-05 09:5x R1343'.encode('utf-8'))
print('R1343 line start found at byte', i)
print('CTX_BEFORE_START:', ctx(raw, i, 50))

def try_fix(raw, left, right, repl_left, repl_right):
    for nl in (b'\r\n', b'\n'):
        m = left + nl + right
        r = repl_left + nl + repl_right
        c = raw.count(m)
        if c == 1:
            return raw.replace(m, r, 1), True, nl
    return raw, False, None

# fix A: add comma after R1342 closing quote
rawA, okA, nlA = try_fix(raw, b'"', b'    "2026-10-05 09:5x R1343:',
                              b'",', b'    "2026-10-05 09:5x R1343:')
print('fixA ok=%s nl=%s' % (okA, nlA))

# fix B: remove trailing comma after R1343 closing quote before ]
tail = '\u9010\u9879\u89e3\u9501",'.encode('utf-8')
rawB, okB, nlB = try_fix(rawA, tail, b'  ],', tail[:-1], b'  ],')
print('fixB ok=%s nl=%s' % (okB, nlB))

if okA and okB:
    open(p, 'wb').write(rawB)
    print('WRITTEN')
else:
    print('ABORT - no write; inspect manually')
