# R227 ASR noise quantifier for SC-001-03 (char-level diff, source vs asr-check)
import io, re, difflib

PUNCT = '，。、,。《》「」『』()（）？！?;；:：~—-…·\u3000'

def flat(p):
    t = io.open(p, encoding='utf-8').read().splitlines()
    body = [l for l in t if l.strip() and '-->' not in l and not l.strip().isdigit()]
    s = ''.join(body)
    for ch in PUNCT:
        s = s.replace(ch, '')
    s = s.replace(' ', '').replace('AI', 'AI')
    return s

src = flat(r'data/storylines/audio/SC-001-03-v1.srt')
asr = flat(r'data/storylines/audio/sc001-03-v1-tmp/asr-check.srt')
sm = difflib.SequenceMatcher(None, src, asr, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
diffchars = sum(max(b - a, d - c) for tag, a, b, c, d in ops)
out = ['src_len=%d asr_len=%d sites=%d diff_chars=%d' % (len(src), len(asr), len(ops), diffchars)]
out += ['%s src[%d:%d]=%r asr[%d:%d]=%r' % (t, a, b, src[a:b], c, d, asr[c:d]) for t, a, b, c, d in ops]
io.open(r'.bs005-tmp/asr-diff-r227.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('src', len(src), 'asr', len(asr), 'sites', len(ops), 'diffchars', diffchars)
