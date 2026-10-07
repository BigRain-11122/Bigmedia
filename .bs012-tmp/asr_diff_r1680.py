# -*- coding: utf-8 -*-
# R1680 ASR noise quantifier for BS-012 v1 (char-level diff, edge-tts truth vs asr-check)
# pattern: asr_diff_r809.py (char-level difflib + trad->simp normalization)
import io, difflib

PUNCT = '，。、,。《》「」『』()（）？！?;；:：~—-…·\u3000'
TRAD = {'開':'开','時':'时','間':'间','終':'终','對':'对','齊':'齐','說':'说',
        '盤':'盘','溫':'温','計':'计','將':'将','復':'复','來':'来','親':'亲','筆':'笔',
        '過':'过','編':'编','輯':'辑','發':'发','籌':'筹','備':'备','給':'给','條':'条',
        '燈':'灯','漁':'渔','眾':'众','號':'号','釘':'钉','進':'进','標':'标','題':'题',
        '師':'师','員':'员','攤':'摊','寫':'写','檔':'档','轉':'转','傳':'传',
        '車':'车','馬':'马','鐘':'钟','聲':'声','緩':'缓','減':'减','霧':'雾',
        '響':'响','舊':'旧','銅':'铜','兩':'两','無':'无','價':'价',
        '們':'们','穩':'稳','這':'这','長':'长','裡':'里','點':'点','機':'机','學':'学',
        '遲':'迟','風':'风','傘':'伞','橋':'桥','頭':'头','藥':'药','腳':'脚',
        '冊':'册','軟':'软','歲':'岁','壓':'压','滅':'灭','運':'运','檢':'检','錄':'录',
        '證':'证','畢':'毕','萬':'万',
        '統':'统','誌':'志','個':'个','調':'调','從':'从','辦':'办','場':'场','沒':'没',
        '組':'组','註':'注','帶':'带','績':'绩','單':'单','換':'换','數':'数','據':'据',
        '還':'还','著':'着','當':'当','歷':'历','驗':'验','貨':'货',
        '賣':'卖','絕':'绝','壞':'坏','騙':'骗','錶':'表','殺':'杀',
        '亂':'乱','爾':'尔','滿':'满','經':'经','實':'实','畫':'画','寶':'宝',
        '講':'讲','義':'义','線':'线','億':'亿','償':'偿','慘':'惨','輪':'轮','諮':'咨',
        '記':'记','憶':'忆','結':'结','構':'构','讀':'读','幹':'干','丟':'丢','斷':'断','電':'电',
        '體':'体','喪':'丧','懶':'懒','態':'态','邊':'边','藍':'蓝'}

def flat(p):
    t = io.open(p, encoding='utf-8').read().splitlines()
    body = [l for l in t if l.strip() and '-->' not in l and not l.strip().isdigit()]
    s = ''.join(body)
    for ch in PUNCT:
        s = s.replace(ch, '')
    s = s.replace(' ', '')
    s = ''.join(TRAD.get(ch, ch) for ch in s)
    return s

src = flat(r'.bs012-tmp/subs.srt')
asr = flat(r'.bs012-tmp/asr-check.srt')
sm = difflib.SequenceMatcher(None, src, asr, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
diffchars = sum(max(b - a, d - c) for tag, a, b, c, d in ops)
out = ['src_len=%d asr_len=%d sites=%d diff_chars=%d' % (len(src), len(asr), len(ops), diffchars)]
out += ['%s src[%d:%d]=%r asr[%d:%d]=%r' % (t, a, b, src[a:b], c, d, asr[c:d]) for t, a, b, c, d in ops]
io.open(r'.bs012-tmp/asr-diff-r1680.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('src', len(src), 'asr', len(asr), 'sites', len(ops), 'diffchars', diffchars)
