# -*- coding: utf-8 -*-
# R440 fast-path five-check evidence (orders/anchor/storylines/daily-brief/lock/inserts/baseline beats)
import os, io, glob, datetime

R = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
G = r'C:\Users\sjs20\Desktop\FluxGroup'

# 1) orders: any O-* file newer (by name-listing) than anchor order
orders = sorted(glob.glob(os.path.join(R, 'orders', '*.md')))
anchor = 'O-20260925-1931-HQ-C.md'
newer = [os.path.basename(p) for p in orders if os.path.basename(p) > anchor and os.path.basename(p).startswith('O-')]
print('orders_new_after_anchor=' + (','.join(newer) if newer else 'NONE'))

# 2) CENSUS supply anchor: canonical anchors dir only (R313-R316 ruling)
anchors_dir = os.path.join(G, 'life', 'BigLife', 'census', 'anchors')
if os.path.isdir(anchors_dir):
    ids = sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(anchors_dir, 'C-*.md')))
    print('anchor_C00030=' + str('C-00030' in ids).lower())
    print('anchor_C00031=' + str('C-00031' in ids).lower())
    print('anchors_tail3=' + ','.join(ids[-3:]))
else:
    print('anchors_dir_missing')

# 3) storylines ch.5 v3 draft scan (bm-a surface): novel/audio/comic zero new writes today
for sub in ('novel', 'audio', 'comic'):
    d = os.path.join(R, 'data', 'storylines', sub)
    files = glob.glob(os.path.join(d, '**', '*'), recursive=True)
    files = [f for f in files if os.path.isfile(f)]
    today_new = [os.path.basename(f) for f in files
                 if datetime.date.fromtimestamp(os.path.getmtime(f)) >= datetime.date(2026, 9, 26)]
    print('storylines_%s_files=%d_today_new=%d' % (sub, len(files), len(today_new)))
ch5 = os.path.join(R, 'data', 'storylines', 'novel', 'SC-001-05-v3.md')
print('ch5_v3_exists=' + str(os.path.exists(ch5)).lower())

# 4) daily brief today (09-26) in place -> no rerun
print('daily_brief_0926=' + str(os.path.exists(os.path.join(R, 'data', 'intel', 'daily', '2026-09-26.md'))).lower())

# 5) git lock + inserts after HEAD anchor (204b012)
print('index_lock=' + str(os.path.exists(os.path.join(R, '.git', 'index.lock'))).lower())

# 6) ledger @ five-mode count + decisions non-empty lines (group anchors)
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
