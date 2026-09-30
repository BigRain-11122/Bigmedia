# -*- coding: utf-8 -*-
# R726 LC-014 ASR v3 final caliber (no f-string subscript pitfalls)
import io, re, difflib, os

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
ext = dict(base); ext.update(adds)

def norm(s):
    return ''.join(ext.get(c, c) for c in s)

a = norm(srt_chars(r'.lc014-tmp/subs.srt'))
b = norm(srt_chars(r'.lc014-tmp/asr-check.srt'))
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
sites = dc = 0
detail = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    sites += 1
    dc += (i2 - i1) + (j2 - j1)
    detail.append("%s ref[%d:%d]=%r asr[%d:%d]=%r" % (tag, i1, i2, a[i1:i2], j1, j2, b[j1:j2]))
rep = ("caliber=punct-strip + trad_norm final (r721 base %d + true-trad adds %d = %d)\n"
       "ref_chars=%d asr_chars=%d\n"
       "sites=%d diff_chars=%d ratio=%.1f%%\n\n" % (len(base), len(adds), len(ext), len(a), len(b), sites, dc, dc/len(a)*100.0))
rep += '\n'.join(detail)
io.open(r'.lc014-tmp/asr-diff-r726-v3.txt', 'w', encoding='utf-8').write(rep)
print('V3 sites', sites, 'diffchars', dc, 'ref', len(a), 'RATIO %.1f' % (dc/len(a)*100))

kw = ['手写报错率','引擎医生','老晶振','硅基民','光机魂系','三代机龄','八号楼','出诊','敲三下机箱',
      '全城大宕机','老日志','两小时','城复活','游戏楼','专用椅子','值班日志','安静三分','精灵系',
      '听声辨位','道晚安','三十年零十一个月','零漏诊','档案馆','机器不坏是本事','坏了能修是人品',
      '公众号','转给管机器的人']
ok = [k for k in kw if k in b]
lost = [k for k in kw if k not in b]
print('SURVIVE', len(ok), '/', len(kw))
print('LOST:', ' / '.join(lost))
print('arch root:', os.path.exists('expert-verdicts/20260930-033954-E4-audience.md'),
      'arch reviews:', os.path.exists('docs/reviews/expert-verdicts/20260930-033954-E4-audience.md'))
