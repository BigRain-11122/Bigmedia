# -*- coding: utf-8 -*-
# R745 probe: b8 subtitle wrap behavior at ladder sizes (decide fix before touching cards)
import sys, io, os
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
sys.path.insert(0, os.path.join(ROOT, 'src', 'render'))
from render_card_video import wrap_for_width

FW = 1080
TXT = u"从川渝小城考出来那年，他爹说「钱的事最讲天理」。进了扭塔他才懂：策略不是赌运气，是把一个道理验一万遍。他最信门禁链——过不了的策略就是没道理，市场早晚教做人"
TITLE = u"一个道理验一万遍"
print('subtitle chars =', len(TXT))
out = io.open(os.path.join(ROOT, '.c3-tmp', 'r745_wrap_probe.txt'), 'w', encoding='utf-8')
for size in (60, 56, 54, 52, 50, 48, 46, 44, 42, 40, 38, 36):
    wrapped = wrap_for_width(TXT, size, FW)
    rows = wrapped.split('\n')
    n_sub = len(rows)
    n_total = len(wrap_for_width(TITLE, size, FW).split('\n')) + n_sub
    pitch = size * 1.2 + 14
    top = (1920 - n_total * pitch) / 2.0
    line = u"size=%d budget_em=%.2f sub_rows=%d total_rows=%d pitch=%.1f top=%.1f net=%.1f -> %s" % (
        size, (FW - 160.0) / size, n_sub, n_total, pitch, top, top - 767,
        'CLEAN' if top >= 787 else ('THIN' if top >= 767 else 'INTRUDES'))
    print(line.encode('gbk', 'replace').decode('gbk'))
    out.write(line + u"\n")
    for r in rows:
        out.write(u"    |" + r + u"\n")
out.close()
print('done')
