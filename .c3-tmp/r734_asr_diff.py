# -*- coding: utf-8 -*-
# R734 LC-016 ASR final-caliber diff (r721 base 58 + r726 adds 20 = 78, R730 terminal table reuse;
# LC-016 run observed = zero new trad drift, simplified output throughout)
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
ext = dict(base); ext.update(adds)

def norm(s):
    return ''.join(ext.get(c, c) for c in s)

a = norm(srt_chars(r'.lc016-tmp/subs.srt'))
b = norm(srt_chars(r'.lc016-tmp/asr-check.srt'))
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
sites = dc = 0
detail = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    sites += 1
    dc += (i2 - i1) + (j2 - j1)
    detail.append(f"{tag} ref[{i1}:{i2}]={a[i1:i2]!r} asr[{j1}:{j2}]={b[j1:j2]!r}")
rep = (f"caliber=punct-strip + trad_norm (r721 base {len(base)} + r726 adds {len(adds)} = ext {len(ext)}·LC-016 run zero new trad drift)\n"
       f"ref_chars={len(a)} asr_chars={len(b)}\n"
       f"sites={sites} diff_chars={dc} ratio={dc/len(a)*100:.1f}%\n\n" + '\n'.join(detail))
io.open(r'.lc016-tmp/asr-diff-r734.txt', 'w', encoding='utf-8').write(rep)
print('sites', sites, 'diffchars', dc, 'ref', len(a), 'RATIO %.1f' % (dc/len(a)*100))

kw = ['系统日志','全城唯一','早班信使','摊主','顾阿凤','碳基市民','六十八岁','脑环广场',
      '数据粥铺','凌晨四点半','开档','收摊','进城第三年','台风','街坊凑料','帮她重搭',
      '这条街就是家','一九九二年','早点摊','老照片','蒸笼','铺头','天没亮','早上的城最真',
      '夸人不重样','句句真心','儿子在现实世界','每年来住半个月','第一口热乎气',
      '比什么口号都金贵','棋友','时空校准师','朱鸿奎','每周三','杀一盘','信条',
      '灶上留一壶','路过的都是客','全档案在公众号','转给惦记热乎早饭的人']
ok = [k for k in kw if k in b]
lost = [k for k in kw if k not in b]
print('SURVIVE', len(ok), '/', len(kw))
print('LOST:', ' / '.join(lost))
with io.open(r'.lc016-tmp/asr-diff-r734.txt', 'a', encoding='utf-8') as f:
    f.write('\n\nSURVIVE %d/%d\nLOST: %s\n' % (len(ok), len(kw), ' / '.join(lost)))
