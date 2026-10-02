# -*- coding: utf-8 -*-
"""R1029 patch (pre-commit correction): close ran at 23:53:24 = production stayed inside
2026-10-02; remove the speculative day-boundary-crossing notes from the just-written ledger
drafts. Nothing committed yet, so this is a draft correction, not a history rewrite."""
import io, json

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'

REPL = [
    (u"2026-10-03 00:1x R1029", u"2026-10-02 23:5x R1029"),
    (u"2026-10-03 00:1x", u"2026-10-02 23:5x"),
    (u"·**日界跨日诚实注=生产窗 23:42-00:1x 跨 10-03 日界·本件=10-02 日签（件号与日期行=10-02 生产窗起算·R909 日界轮先例口径）**",
     u"·生产窗 23:42-23:53 全程 10-02 窗内（无日界跨越）"),
    (u"**日界跨日诚实注=生产窗 23:42-00:1x 跨 10-03 日界·本件=10-02 日签**",
     u"生产窗 23:42-23:53 全程 10-02 窗内（无日界跨越）"),
    (u"日界跨日诚实注=生产窗 23:42-00:1x 本件=10-02 日签",
     u"生产窗 23:42-23:53 全程 10-02 窗内（无日界跨越）"),
    (u"·生产窗 23:42-00:1x 跨日界·本件=10-02 日签",
     u"·生产窗 23:42-23:53 全程 10-02 窗内"),
    (u"·日界跨日注=本件为 10-02 日签）", u"）"),
]

FILES = [
    u'src/os/state.json',
    u'docs/status-export.json',
    u'output/finished.md',
    u'data/storylines/cards/README.md',
    u'docs/self-improvement-queue.md',
    u'src/os/backlog.md',
]

for fp in FILES:
    p = ROOT + u'\\' + fp.replace(u'/', u'\\')
    t = io.open(p, encoding='utf-8').read()
    n = 0
    for a, b in REPL:
        if a in t:
            n += t.count(a)
            t = t.replace(a, b)
    io.open(p, 'w', encoding='utf-8').write(t)
    print('%s: %d replacements' % (fp, n))

# verify no leftovers
bad = [u"00:1x", u"日界跨日", u"2026-10-03 00:"]
for fp in FILES:
    p = ROOT + u'\\' + fp.replace(u'/', u'\\')
    t = io.open(p, encoding='utf-8').read()
    left = [b for b in bad if b in t]
    if left:
        print('LEFTOVER in %s: %s' % (fp, left))
print('patch done')
