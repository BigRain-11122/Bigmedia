# -*- coding: utf-8 -*-
# R226 ch.3 same-text mechanical verification: every novel narrative paragraph must appear
# verbatim in the beats file; the preview line maps to cta (paren-stripped per ep1/ep2 precedent).
import io, os

NOVEL = r'data/storylines/novel/SC-001-03-v1.md'
BEATS = r'data/storylines/audio/SC-001-03-v1.beats.txt'
OUT = r'data/storylines/audio/sc001-03-v1-tmp/r226-verify.txt'

novel = io.open(NOVEL, encoding='utf-8').read()
beats = io.open(BEATS, encoding='utf-8').read()

lines = [ln.strip() for ln in novel.split('\n')]
paras, preview = [], ''
in_body = False
for ln in lines:
    if not ln:
        continue
    if ln.startswith('>'):
        continue  # triple-label blockquote
    if ln.startswith('#'):
        continue
    if ln == '---':
        in_body = False
        continue
    if ln.startswith('**来源清单**'):
        in_body = False
        continue
    if ln.startswith('- '):
        continue  # source list rows
    if ln.startswith('（下一章预告：'):
        preview = ln
        continue
    if not in_body:
        in_body = True
    paras.append(ln)

results = []
miss = 0
for i, p in enumerate(paras):
    ok = p in beats
    if not ok:
        miss += 1
    results.append('para %02d verbatim=%s | %s...' % (i + 1, 'OK' if ok else 'MISS', p[:24]))

# preview -> cta mapping (paren stripped)
inner = preview.strip('（下一章预告：').rstrip('）')
cta_ok = ('下一章：' + inner) in beats
results.append('cta (preview, paren-stripped) verbatim=%s' % ('OK' if cta_ok else 'MISS'))
if not cta_ok:
    miss += 1

results.append('paras=%d miss=%d cta=%s' % (len(paras), miss, 'OK' if cta_ok else 'MISS'))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(results) + '\n')
print('\n'.join(results))
