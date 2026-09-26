# -*- coding: utf-8 -*-
# R450 five-check evidence (r447 pattern; anchors: ledger_at=28 (R441), decisions=45 (R444))
import os, io, glob, datetime

R = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
G = r'C:\Users\sjs20\Desktop\FluxGroup'

# 1) orders full-file scan (D-20260927-05(2) adoption): new after anchor + edited existing
orders = sorted(glob.glob(os.path.join(R, 'orders', '*.md')))
anchor = 'O-20260925-1931-HQ-C.md'
newer = [os.path.basename(p) for p in orders if os.path.basename(p) > anchor and os.path.basename(p).startswith('O-')]
print('orders_new_after_anchor=' + (','.join(newer) if newer else 'NONE'))
apath = os.path.join(R, 'orders', anchor)
if os.path.exists(apath):
    am = os.path.getmtime(apath)
    edited = [os.path.basename(p) for p in orders
              if os.path.basename(p) != anchor and os.path.basename(p) < anchor
              and os.path.getmtime(p) > am]
    print('orders_edited_since_anchor=' + (','.join(edited) if edited else 'NONE'))
else:
    print('orders_anchor_missing')

# 2) CENSUS supply anchor canonical position
anchors_dir = os.path.join(G, 'life', 'BigLife', 'census', 'anchors')
if os.path.isdir(anchors_dir):
    ids = sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(anchors_dir, 'C-*.md')))
    print('anchor_C00030=' + str('C-00030' in ids).lower())
    print('anchors_tail3=' + ','.join(ids[-3:]))
else:
    print('anchors_dir_missing')

# 3) storylines today scan (bm-a surface)
for sub in ('novel', 'audio', 'comic'):
    d = os.path.join(R, 'data', 'storylines', sub)
    files = [f for f in glob.glob(os.path.join(d, '**', '*'), recursive=True) if os.path.isfile(f)]
    today_new = [os.path.basename(f) for f in files
                 if datetime.date.fromtimestamp(os.path.getmtime(f)) >= datetime.date(2026, 9, 27)]
    print('storylines_%s_today_new=%d' % (sub, len(today_new)))

# 4) daily brief 09-27 in place -> no rerun
print('daily_brief_0927=' + str(os.path.exists(os.path.join(R, 'data', 'intel', 'daily', '2026-09-27.md'))).lower())

# 5) git lock
print('index_lock=' + str(os.path.exists(os.path.join(R, '.git', 'index.lock'))).lower())

# 6) group anchors: ledger @ five-mode count + decisions non-empty lines
pat = ('@BigStream', '@八线全量', '@七线全司', '@全司', '@六司')
n = 0
with io.open(os.path.join(G, 'cph4', 'evolution-ledger.md'), encoding='utf-8-sig') as f:
    for line in f:
        if any(p in line for p in pat):
            n += 1
print('ledger_at_count=' + str(n))
m = 0
with io.open(os.path.join(G, 'docs', 'decisions.md'), encoding='utf-8-sig') as f:
    for line in f:
        if line.strip():
            m += 1
print('decisions_nonempty=' + str(m))
