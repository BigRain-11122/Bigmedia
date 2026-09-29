# -*- coding: utf-8 -*-
# R705 ASR noise quantifier for LC-009 v2 (trad drift normalization extended per this run's glyph set)
# pattern: asr_diff_r701.py + series precedent "trad->simp normalization" (BS-006 first-seen, extended per run)
import io, difflib

PUNCT = '，。、,。《》「」『』()（）？！?;；:：~—-…·\u3000'
TRAD = {'開':'开','時':'时','間':'间','終':'终','對':'对','齊':'齐','說':'说',
        '盤':'盘','溫':'温','計':'计','將':'将','復':'复','來':'来','親':'亲','筆':'笔',
        '過':'过','編':'编','輯':'辑','發':'发','籌':'筹','備':'备','給':'给','條':'条',
        '燈':'灯','漁':'渔','眾':'众','號':'号','釘':'钉','進':'进','標':'标','題':'题',
        '師':'师','員':'员','攤':'摊','寫':'写','檔':'档','轉':'转','傳':'传','齧':'啮',
        '車':'车','馬':'马','鳳':'凤','鐘':'钟','聲':'声','緩':'缓','減':'减','霧':'雾',
        '響':'响','舊':'旧','銅':'铜','丟':'丢','兩':'两','無':'无','恆':'恒','價':'价',
        '們':'们','穩':'稳','這':'这','長':'长','裡':'里','點':'点','機':'机','學':'学',
        '遲':'迟','風':'风','傘':'伞','橋':'桥','頭':'头','藥':'药','腳':'脚',
        # R705 extension (this run's trad glyph set)
        '統':'统','擁':'拥','貓':'猫','場':'场','羅':'罗','壯':'壮','門':'门','訊':'讯',
        '斷':'断','類':'类','鋪':'铺','葉':'叶','畫':'画','燙':'烫','鵰':'雕','邊':'边',
        '劃':'划'}

def flat(p):
    t = io.open(p, encoding='utf-8').read().splitlines()
    body = [l for l in t if l.strip() and '-->' not in l and not l.strip().isdigit()]
    s = ''.join(body)
    for ch in PUNCT:
        s = s.replace(ch, '')
    s = s.replace(' ', '')
    s = ''.join(TRAD.get(ch, ch) for ch in s)
    return s

src = flat(r'.lc009-tmp/subs.srt')
asr = flat(r'.lc009-tmp/asr-check.srt')
sm = difflib.SequenceMatcher(None, src, asr, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
diffchars = sum(max(b - a, d - c) for tag, a, b, c, d in ops)
out = ['src_len=%d asr_len=%d sites=%d diff_chars=%d' % (len(src), len(asr), len(ops), diffchars)]
out += ['%s src[%d:%d]=%r asr[%d:%d]=%r' % (t, a, b, src[a:b], c, d, asr[c:d]) for t, a, b, c, d in ops]
io.open(r'.lc009-tmp/asr-diff-r705.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('src', len(src), 'asr', len(asr), 'sites', len(ops), 'diffchars', diffchars,
      'pct=%.1f%%' % (100.0 * diffchars / len(src)))
