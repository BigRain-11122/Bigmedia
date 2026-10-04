# -*- coding: utf-8 -*-
# r1304: extract clean E4 verdict from polluted e4-result.json (pull-progress spam prefix)
import json, io, re, os

SRC = os.path.join('data', 'storylines', 'cards', 'MC-20261005-DIGEST-v15-tmp', 'e4-result.json')
OUT = os.path.join('.c3-tmp', 'r1304_e4_clean.txt')

d = json.load(io.open(SRC, encoding='utf-8'))
v = d.get('verdict', '')

# spam pattern: ollama pull progress tokens
spam = re.compile(r'pulling (manifest|2049f5674b1e)', re.IGNORECASE)
last = 0
for m in spam.finditer(v):
    last = m.end()
# tail after last spam token is the real verdict region; but the real text may
# start right at the end of the last progress line. Take generous slice:
# walk back from last spam end to previous newline boundary not needed; instead
# cut at last spam end, then strip residual progress fragments on that boundary.
tail = v[last:]
# strip leading fragments like "   39 MB/s   3m49s" or percent tokens
tail = re.sub(r'^[\s\d.,%/a-zA-Z:]*?(?=[\u4e00-\u9fff\[(])', '', tail, count=1)
io.open(OUT, 'w', encoding='utf-8').write('ts=%s\nmodel=%s\nlen_total=%d len_clean=%d\n---VERDICT---\n%s' % (
    d.get('ts'), d.get('model'), len(v), len(tail), tail))
print('total_len=%d clean_len=%d' % (len(v), len(tail)))
print('head300=', tail[:300].encode('unicode_escape').decode()[:600])
print('---')
# score mining
for m in re.finditer(r'(\d+(?:\.\d+)?)\s*/\s*10|(\d+(?:\.\d+)?)\s*[分点]', tail):
    print('SCORE_HIT:', m.group(0).encode('unicode_escape').decode())
