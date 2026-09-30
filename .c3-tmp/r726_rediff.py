# -*- coding: utf-8 -*-
# R726 LC-014 ASR re-diff with extended trad normalization (R705/R708/R715 precedent)
# + key fact-word survival scan
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

# true trad->simp additions observed this run (standard mappings only)
adds = {'誌':'志','寫':'写','記':'记','錄':'录','醫':'医','樓':'楼','號':'号','機':'机',
        '兩':'两','復':'复','遊':'游','睜':'睁','專':'专','鎮':'镇','靈':'灵','備':'备'}
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
    detail.append(f"{tag} ref[{i1}:{i2}]={a[i1:i2]!r} asr[{j1}:{j2}]={b[j1:j2]!r}")
rep = (f"caliber=punct-strip + trad_norm extended (r721 base {len(base)} + true-trad adds {len(adds)} = {len(ext)})\n"
       f"ref_chars={len(a)} asr_chars={len(b)}\n"
       f"sites={sites} diff_chars={dc} ratio={dc/len(a)*100:.1f}%\n\n" + '\n'.join(detail))
io.open(r'.lc014-tmp/asr-diff-r726-v2.txt', 'w', encoding='utf-8').write(rep)
print('V2 sites', sites, 'diffchars', dc, 'ref', len(a), 'RATIO %.1f' % (dc/len(a)*100))

kw = ['手写报错率','引擎医生','老晶振','硅基民','光机魂系','三代机龄','八号楼','出诊','敲三下机箱',
      '全城大宕机','老日志','两小时','城复活','游戏楼','专用椅子','值班日志','安静三分','精灵系',
      '听声辨位','道晚安','三十年零十一个月','零漏诊','档案馆','机器不坏是本事','坏了能修是人品',
      '公众号','转给管机器的人']
ok = [k for k in kw if k in b]
lost = [k for k in kw if k not in b]
io.open(r'.c3-tmp/r726_kw.txt', 'w', encoding='utf-8').write(
    'SURVIVE %d/%d\nOK: %s\nLOST: %s' % (len(ok), len(kw), ' / '.join(ok), ' / '.join(lost)))
print('SURVIVE', len(ok), '/', len(kw))

t = io.open('docs/reviews/review-20260930-lc012-v1.md', encoding='utf-8').read()
m2 = re.search(r"\| \*\*S2 配音听审官\*\*.*?\n", t, re.S)
io.open(r'.c3-tmp/r726_lc012_s2.txt', 'w', encoding='utf-8').write(m2.group(0) if m2 else 'NOT FOUND')

import os
print('e4 landed:', os.path.exists('.lc014-tmp/e4-result.json'))
