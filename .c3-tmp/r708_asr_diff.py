# -*- coding: utf-8 -*-
# R708 LC-010 ASR diff quantification (difflib char-level, punctuation-stripped char-position
# caliber per R685-R705 precedent + trad->simp normalized per R705; rerun v2: punct strip fix)
import io, difflib

PUNCT = set('，。：、！？；·""\'\'（）《》【】, .:;!?()[]{}"\'\n\t-_~…—|/\\')

def srt_chars(path):
    lines = io.open(path, encoding='utf-8-sig').read().splitlines()
    out = []
    for ln in lines:
        s = ln.strip()
        if not s or '-->' in s or s.isdigit():
            continue
        for ch in s:
            if ch not in PUNCT:
                out.append(ch)
    return ''.join(out)

TRAD = {'統':'统','擁':'拥','貓':'猫','場':'场','羅':'罗','壯':'壮','門':'门','訊':'讯','斷':'断','類':'类','鋪':'铺','葉':'叶','畫':'画','燙':'烫','鵰':'雕','邊':'边','條':'条','電':'电','話':'话','遷':'迁','數':'数','寵':'宠','師':'师','車':'车','長':'长','時':'时','間':'间','歲':'岁','藝':'艺','術':'术','開':'开','關':'关','點':'点','為':'为','與':'与','從':'从','這':'这','個':'个','們':'们','來':'来','對':'对','麼':'么','見':'见','觀':'观','讓':'让','還':'还','進':'进','過':'过','發':'发','給':'给','聽':'听','說':'说','錢':'钱','雲':'云','廠':'厂','學':'学','轉':'转','幹':'干'}

def norm(s):
    return ''.join(TRAD.get(ch, ch) for ch in s)

a = norm(srt_chars(r'.lc010-tmp/subs.srt'))
b = norm(srt_chars(r'.lc010-tmp/asr-check.srt'))
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
sites = 0; diff_chars = 0
detail = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    sites += 1
    diff_chars += (i2 - i1) + (j2 - j1)
    detail.append(f"{tag} ref[{i1}:{i2}]={a[i1:i2]!r} asr[{j1}:{j2}]={b[j1:j2]!r}")
report = (f"caliber=punctuation-stripped char-position (R685-R705 precedent) + trad_norm_set={len(TRAD)} chars\n"
          f"ref_chars={len(a)} asr_chars={len(b)}\n"
          f"sites={sites} diff_chars={diff_chars} ratio={diff_chars/len(a)*100:.1f}%\n\n")
report += '\n'.join(detail)
io.open(r'.lc010-tmp/asr-diff-r708.txt', 'w', encoding='utf-8').write(report)
print('SITES', sites, 'DIFFCHARS', diff_chars, 'REF', len(a), 'RATIO %.1f' % (diff_chars/len(a)*100))
