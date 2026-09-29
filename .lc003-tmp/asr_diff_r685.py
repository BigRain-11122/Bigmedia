# R685 ASR noise quantifier for LC-003 v1 (char-level diff, edge-tts truth vs asr-check)
# pattern: .lc002-tmp/asr_diff_r681.py (R681 quantified precedent) + trad->simp normalization
# (BS-006 F-049 precedent: whisper zh decode drifts to traditional glyphs = same word/sound,
#  non-semantic damage, normalized before counting)
import io, difflib

PUNCT = '，。、,。《》「」『』()（）？！?;；:：~—-…·\u3000'
TRAD = {'開':'开','時':'时','間':'间','終':'终','對':'对','齊':'齐','絲':'丝','說':'说',
        '盤':'盘','溫':'温','計':'计','將':'将','復':'复','來':'来','親':'亲','筆':'笔',
        '過':'过','編':'编','輯':'辑','發':'发','籌':'筹','備':'备','給':'给','條':'条',
        '燈':'灯','漁':'渔','眾':'众','號':'号','釘':'钉','進':'进','標':'标','題':'题',
        '師':'师','員':'员','攤':'摊','寫':'写','檔':'档','轉':'转'}

def flat(p):
    t = io.open(p, encoding='utf-8').read().splitlines()
    body = [l for l in t if l.strip() and '-->' not in l and not l.strip().isdigit()]
    s = ''.join(body)
    for ch in PUNCT:
        s = s.replace(ch, '')
    s = s.replace(' ', '')
    s = ''.join(TRAD.get(ch, ch) for ch in s)
    return s

src = flat(r'.lc003-tmp/subs.srt')
asr = flat(r'.lc003-tmp/asr-check.srt')
sm = difflib.SequenceMatcher(None, src, asr, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
diffchars = sum(max(b - a, d - c) for tag, a, b, c, d in ops)
out = ['src_len=%d asr_len=%d sites=%d diff_chars=%d' % (len(src), len(asr), len(ops), diffchars)]
out += ['%s src[%d:%d]=%r asr[%d:%d]=%r' % (t, a, b, src[a:b], c, d, asr[c:d]) for t, a, b, c, d in ops]
io.open(r'.lc003-tmp/asr-diff-r685.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('src', len(src), 'asr', len(asr), 'sites', len(ops), 'diffchars', diffchars)
