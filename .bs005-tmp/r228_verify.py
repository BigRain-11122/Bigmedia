# -*- coding: utf-8 -*-
# R228 same-text mechanical verification for ch.4 beats (R226 r226_verify pattern)
import io, re

novel = io.open(r'data\storylines\novel\SC-001-04-v1.md', encoding='utf-8').read()
beats = io.open(r'data\storylines\audio\SC-001-04-v1.beats.txt', encoding='utf-8').read()

# novel body = between the tri-label blockquote and the '---' separator
m = re.search(r'---\s*\n', novel)
body = novel[:m.start()] if m else novel
# strip title line and tri-label blockquote lines
body_lines = [l.strip() for l in body.splitlines()]
paras = []
for l in body_lines:
    if not l or l.startswith('#') or l.startswith('>'):
        continue
    paras.append(l)

spoken = ' '.join(l.split(' | ', 2)[2] for l in beats.splitlines() if ' | ' in l)

miss = [p for p in paras if p not in spoken]
print('novel paras:', len(paras))
print('miss count:', len(miss))
for p in miss:
    print('MISS:', p[:60])

# cta de-paren check: novel preview line (口播化 = 下一章预告：X -> 下一章：X)
mp = re.search(r'（下一章预告：(.+?)）\s*$', novel, re.S)
cta_beat = [l for l in beats.splitlines() if l.startswith('cta |')][0]
cta_text = cta_beat.split(' | ', 2)[2]
print('cta de-paren+spokenize OK:', cta_text == '下一章：' + mp.group(1))
hook_line = [l for l in beats.splitlines() if l.startswith('hook |')][0].split(' | ', 2)[2]
sents = [s + '。' for s in hook_line.split('。')[:-1]]
print('hook sentence count:', len(sents))
print('hook has AIGC decl:', any('本节目由 AI 参与生成' in s for s in sents))
print('hook has factual-line decl:', any('基于硅基城市真实事件改编' in s for s in sents))
print('hook has source pointer:', any('完整来源清单见图文页' in s for s in sents))
print('hook has chapter anchor:', any('第四章，纪念碑田' in s for s in sents))
