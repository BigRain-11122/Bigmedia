# -*- coding: utf-8 -*-
import io
t = io.open(r'output/finished.md', encoding='utf-8').read()
i = t.find('F-153')
io.open(r'.c3-tmp\r1322_f153.txt', 'w', encoding='utf-8').write(t[max(0, i - 200):i + 1400])
t2 = io.open(r'data/storylines/cards/README.md', encoding='utf-8').read()
j = t2.find('v66')
io.open(r'.c3-tmp\r1322_readme66.txt', 'w', encoding='utf-8').write(t2[max(0, j - 600):j + 900])
# also: last lines of finished.md tail structure and README tail (for append points)
io.open(r'.c3-tmp\r1322_tails.txt', 'w', encoding='utf-8').write(
    '--- finished.md tail 40 ---\n' + '\n'.join(t.splitlines()[-40:]) +
    '\n--- cards README tail 30 ---\n' + '\n'.join(t2.splitlines()[-30:]))
print('ok')
