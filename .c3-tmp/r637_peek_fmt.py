# -*- coding: utf-8 -*-
import io, re
p = r'src\render\emotive_tts.py'
with io.open(p, encoding='utf-8') as f:
    src = f.read()
lines = src.splitlines()
out = []
for i, l in enumerate(lines):
    if re.search(r'BEAT_TYPES|def parse|\.split\(|cyber|voice|--beats|prosody', l):
        out.append('%d: %s' % (i + 1, l.rstrip()))
with io.open(r'.c3-tmp\r637_tts_fmt.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out[:60]))
print('WROTE %d' % len(out))
