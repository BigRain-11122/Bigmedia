# R448 ASR noise quantifier for bs-001-v15 (char-level diff, subs.srt vs asr-check)
import io, difflib

PUNCT = '，。、,。《》「」『』()（）？！?;；:：~—-…·\u3000'

def flat(p):
    t = io.open(p, encoding='utf-8').read().splitlines()
    body = [l for l in t if l.strip() and '-->' not in l and not l.strip().isdigit()]
    s = ''.join(body)
    for ch in PUNCT:
        s = s.replace(ch, '')
    return s.replace(' ', '')

src = flat(r'.bs001-v15-tmp/subs.srt')
asr = flat(r'.bs001-v15-tmp/asr-check.srt')
sm = difflib.SequenceMatcher(None, src, asr, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
diffchars = sum(max(b - a, d - c) for tag, a, b, c, d in ops)
out = ['src_len=%d asr_len=%d sites=%d diff_chars=%d' % (len(src), len(asr), len(ops), diffchars)]
out += ['%s src[%d:%d]=%r asr[%d:%d]=%r' % (t, a, b, src[a:b], c, d, asr[c:d]) for t, a, b, c, d in ops]
io.open(r'.bs001-v15-tmp/asr-diff-r448.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out[:30]))
print('... total sites:', len(ops))
