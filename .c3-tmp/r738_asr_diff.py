# -*- coding: utf-8 -*-
# R738 LC-017 ASR final-caliber diff (trad 78 table reuse per R734 precedent)
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

a = norm(srt_chars(r'.lc017-tmp/subs.srt'))
b = norm(srt_chars(r'.lc017-tmp/asr-check.srt'))
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
sites = dc = 0
detail = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    sites += 1
    dc += (i2 - i1) + (j2 - j1)
    detail.append(f"{tag} ref[{i1}:{i2}]={a[i1:i2]!r} asr[{j1}:{j2}]={b[j1:j2]!r}")
rep = (f"caliber=punct-strip + trad_norm (r721 base {len(base)} + r726 adds {len(adds)} = ext {len(ext)}·R734 78-table reuse)\n"
       f"ref_chars={len(a)} asr_chars={len(b)}\n"
       f"sites={sites} diff_chars={dc} ratio={dc/len(a)*100:.1f}%\n\n" + '\n'.join(detail))
io.open(r'.lc017-tmp/asr-diff-r738.txt', 'w', encoding='utf-8').write(rep)
print('sites', sites, 'diffchars', dc, 'ref', len(a), 'RATIO %.1f' % (dc/len(a)*100))

kw = ['系统日志','全城唯一','手写提要','林之恒','碳基市民','二十六岁','北外滩','档案馆区',
      '编年史馆员','白手套','编目','不毁一个字节','馆长批注','出生那天的日志','站了一下午',
      '小本','三个月','五条街区','口述史','采风','一万个居民','真历史','三十年后',
      '便利店小票','史料','顾阿姨','粢饭摊','新令牌','誊进编目','出处齐','信条',
      '城市不会忘记','除非我们偷懒','馆员','全档案在公众号','转给相信小事也是历史的人']
ok = [k for k in kw if k in b]
lost = [k for k in kw if k not in b]
print('SURVIVE', len(ok), '/', len(kw))
print('LOST:', ' / '.join(lost))
with io.open(r'.lc017-tmp/asr-diff-r738.txt', 'a', encoding='utf-8') as f:
    f.write('\n\nSURVIVE %d/%d\nLOST: %s\n' % (len(ok), len(kw), ' / '.join(lost)))
