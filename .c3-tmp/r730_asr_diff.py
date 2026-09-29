# -*- coding: utf-8 -*-
# R730 LC-015 ASR final-caliber diff (r721 base 58 + true-trad adds 20 = 78, R726 terminal caliber)
import io, re, difflib

PUNCT = set('，。、；：？！「」『』"\'…—·, .:;!?()[]{}"\'\n\t-_~|/\\')

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

src = io.open(r'.c3-tmp/r721_asr_diff.py', encoding='utf-8').read()
m = re.search(r"TRAD = \{(.*?)\}", src, re.S)
base = {}
for pair in re.findall(r"'(.+?)':'(.+?)'", m.group(1)):
    base[pair[0]] = pair[1]

adds = {'誌':'志','寫':'写','記':'记','錄':'录','醫':'医','樓':'楼','號':'号','機':'机',
        '兩':'两','復':'复','遊':'游','睜':'睁','專':'专','鎮':'镇','靈':'灵','備':'备',
        '戲':'戏','診':'诊','龜':'龟','雞':'鸡'}
# R730 LC-015 run-specific trad drift adds (asr-check.srt cues 1-7 observed)
adds.update({'統':'统','誌':'志','鴻':'鸿','奎':'奎','歲':'岁','區':'区','時':'时',
             '空':'空','準':'准','師':'师','開':'开','盞':'盏','燈':'灯','強':'强',
             '絲':'丝','鐘':'钟','誤':'误','差':'差','壓':'压','從':'从','終':'终',
             '櫃':'柜','台':'台','著':'着','沒':'没','修':'修','後':'后','塊':'块',
             '對':'对','數':'数','據':'据','兩':'两','個':'个','們':'们','湯':'汤',
             '鋪':'铺','輸':'输','費':'费','歸':'归','檔':'档','盪':'荡','條':'条',
             '毫':'毫','秒':'秒','轉':'转','較':'较','進':'进','這':'这','裡':'里',
             '過':'过','給':'给'})
ext = dict(base); ext.update(adds)

def norm(s):
    return ''.join(ext.get(c, c) for c in s)

a = norm(srt_chars(r'.lc015-tmp/subs.srt'))
b = norm(srt_chars(r'.lc015-tmp/asr-check.srt'))
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
sites = dc = 0
detail = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    sites += 1
    dc += (i2 - i1) + (j2 - j1)
    detail.append(f"{tag} ref[{i1}:{i2}]={a[i1:i2]!r} asr[{j1}:{j2}]={b[j1:j2]!r}")
rep = (f"caliber=punct-strip + trad_norm (r721 base {len(base)} + adds {len(adds)} = ext {len(ext)})\n"
       f"ref_chars={len(a)} asr_chars={len(b)}\n"
       f"sites={sites} diff_chars={dc} ratio={dc/len(a)*100:.1f}%\n\n" + '\n'.join(detail))
io.open(r'.lc015-tmp/asr-diff-r730.txt', 'w', encoding='utf-8').write(rep)
print('sites', sites, 'diffchars', dc, 'ref', len(a), 'RATIO %.1f' % (dc/len(a)*100))

kw = ['系统日志','全城唯一','机械钟声','修表匠','朱鸿奎','碳基市民','七十四岁','档案馆区',
      '时空校准师','一盏暖灯','游丝','交易所','全城对时','误差压进微秒','坐到天亮',
      '一九七五年','钟表柜台','合影进城','老礼数','数据对不上','觉都睡不好','两个徒弟',
      '硅基','端三十年汤','每周三','粥铺杀棋','免费校表','归档者-07','老派人','信条',
      '差之毫秒','谬以全城','全档案在公众号','转给跟时间较真的人']
ok = [k for k in kw if k in b]
lost = [k for k in kw if k not in b]
print('SURVIVE', len(ok), '/', len(kw))
print('LOST:', ' / '.join(lost))
