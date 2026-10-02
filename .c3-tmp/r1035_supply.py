# -*- coding: utf-8 -*-
"""R1035 supply-gate probe: all lane unlock faces fresh check."""
import io, os, re, glob, json

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
LIFE = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife'
out = io.open(os.path.join(ROOT, '.c3-tmp', 'r1035_supply_gates.txt'), 'w', encoding='utf-8')
def w(s): out.write(str(s) + '\n')

# 1) CENSUS gate: anchors dir
anch = sorted(glob.glob(os.path.join(LIFE, 'census', 'anchors', 'C-*.md')))
w('anchors_count=%d top3=%s' % (len(anch), [os.path.basename(a) for a in anch[-3:]]))
w('C00030_present=%s' % os.path.exists(os.path.join(LIFE, 'census', 'anchors', 'C-00030.md')))

# 2) pools.json TOTAL_LINES (baseline 1440)
pj = os.path.join(LIFE, 'cognition', 'pools.json')
if os.path.exists(pj):
    t = io.open(pj, encoding='utf-8').read()
    m = re.search(r'TOTAL_LINES[^0-9]*(\d+)', t)
    lines = t.count('\n')
    w('pools.json mtime=%s TOTAL_LINES_marker=%s phys_lines=%d bytes=%d' % (
        __import__('datetime').datetime.fromtimestamp(os.path.getmtime(pj)).strftime('%m-%d %H:%M'),
        m.group(1) if m else '?', lines, len(t)))
else:
    w('pools.json MISSING')

# 3) interchat-ledger count (baseline 22, mtime 09-27)
il = os.path.join(LIFE, 'cognition', 'interchat-ledger.jsonl')
if os.path.exists(il):
    t = io.open(il, encoding='utf-8').read().strip()
    w('interchat mtime=%s entries=%d' % (
        __import__('datetime').datetime.fromtimestamp(os.path.getmtime(il)).strftime('%m-%d %H:%M'),
        t.count('\n') + 1 if t else 0))
else:
    w('interchat MISSING')

# 4) novel chapters on disk (baseline: ch1/ch2 v4 in册, ch6 absent)
nd = os.path.join(ROOT, 'data', 'storylines', 'novel')
nov = sorted(os.path.basename(f) for f in glob.glob(os.path.join(nd, '*.md')))
w('novel_files=%s' % nov)

# 5) audio dir current registered versions
ad = os.path.join(ROOT, 'data', 'storylines', 'audio')
aud = sorted(os.path.basename(f) for f in glob.glob(os.path.join(ad, '*.md')) or [])
w('audio_readme=%s' % aud)
au3 = sorted(set(os.path.basename(f) for f in glob.glob(os.path.join(ad, 'SC-001-0*.mp3'))))
w('audio_mp3=%s' % au3)

# 6) comic texts (baseline ep1/ep2 texts done)
cd = os.path.join(ROOT, 'data', 'storylines', 'comic')
com = sorted(os.path.basename(f) for f in glob.glob(os.path.join(cd, '*')))
w('comic_files=%s' % com[:20])

# 7) drafts (BS 稿集) newest
dr = sorted(glob.glob(os.path.join(ROOT, 'data', 'sources', '20260923-BS-*.md')) + glob.glob(os.path.join(ROOT, 'data', 'sources', '*', '20260923-BS-*.md')))
w('drafts=%s' % [os.path.basename(f) for f in dr])

# 8) finished.md tail: last F entries
fm = io.open(os.path.join(ROOT, 'output', 'finished.md'), encoding='utf-8').read()
fnums = re.findall(r'F-(\d{3}) 登记', fm)
w('F_registered_max=%s count=%d' % (max(fnums) if fnums else None, len(fnums)))
tail_block = fm[fm.rfind('F-146'):]
w('--- finished.md from F-146 (first 1200 chars) ---')
w(tail_block[:1200])

# 9) release-schedule (video号冗余池) current count
rs = os.path.join(ROOT, 'docs', 'release-schedule.md')
if os.path.exists(rs):
    t = io.open(rs, encoding='utf-8').read()
    m = re.search(r'v(\d+\.\d+)', t)
    w('release_schedule_version=%s 冗余弹药行=%s' % (m.group(1) if m else '?', len(re.findall(r'冗余弹药 (\d+) 件', t))))

out.close()
print('ok')
