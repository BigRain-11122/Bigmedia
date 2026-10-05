# -*- coding: utf-8 -*-
# r1352 gates: supply-gate facts + export freshness (independent OUT, r1350_gates clone)
import json, os, io, time, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []
def w(s): OUT.append(str(s))

w('now=%s' % time.strftime('%Y-%m-%d %H:%M:%S'))

# pools leaf strings (baseline 1440)
POOLS = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
pd = json.load(io.open(POOLS, encoding='utf-8'))
leaves = []
def walk(node):
    if isinstance(node, dict):
        for v in node.values(): walk(v)
    elif isinstance(node, list):
        for v in node.values() if False else node: walk(v)
    elif isinstance(node, str):
        if node.strip(): leaves.append(node.strip())
    elif isinstance(node, (int, float)):
        leaves.append(str(node))
walk(pd)
w('POOLS_LEAF_STRINGS: %d (baseline 1440; mtime %s)' % (len(leaves), time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(POOLS)))))
w('POOLS_GATE: %s' % ('FIRED' if len(leaves) != 1440 else 'QUIET 1440==1440'))

# interchat rows (baseline 22)
inter = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\interchat-ledger.jsonl'
if os.path.exists(inter):
    n = sum(1 for l in io.open(inter, encoding='utf-8', errors='replace') if l.strip())
    w('INTERCHAT_ROWS: %d (baseline 22; mtime %s)' % (n, time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(inter)))))
    w('INTERCHAT_GATE: %s' % ('FIRED' if n != 22 else 'QUIET 22==22'))
else:
    w('INTERCHAT_ROWS: FILE MISSING')

# CENSUS anchor C-00030 (supply gate for #63)
anchor = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00030.md'
w('CENSUS_ANCHOR_C-00030: %s' % ('EXISTS' if os.path.exists(anchor) else 'ABSENT (supply-gated)'))
anchors_dir = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors'
if os.path.isdir(anchors_dir):
    w('ANCHORS_COUNT: %d' % len(glob.glob(os.path.join(anchors_dir, '*.md'))))

# dusk standby row (DAILY v68 lane gate) + weekend gated row (10-08 market re-open)
try:
    nb2 = pd['axes'][u'怀旧'][u'dusk']
    w('NOSTALGIA_DUSK_13: %r len=%d [dusk standby ~18:00 -> DAILY v68]' % (nb2[13], len(nb2)))
except Exception as e:
    w('NOSTALGIA_DUSK_13 ERR: %r' % e)
try:
    wk = pd['axes'][u'烟火'][u'weekend']
    w('YANHUO_WEEKEND_13: %r [gated row 10-08 market re-open]' % (wk[13],))
except Exception as e:
    w('YANHUO_WEEKEND_13 ERR: %r' % e)

# OSS window 4 ledger file gate
oh = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\oss-harvest\OH-20261005-bigstream.md'
w('OSS_W4_LEDGER_OH-20261005: %s (window opens 21:40 tonight)' % ('EXISTS' if os.path.exists(oh) else 'NOT-BUILT (normal pre-window)'))

# daily briefs
for d in ('2026-10-05', '2026-10-06'):
    p = os.path.join(ROOT, 'data', 'intel', 'daily', d + '.md')
    w('DAILY %s: %s' % (d, 'EXISTS' if os.path.exists(p) else 'MISSING'))

# novel ch6 v4 (bm-a gate)
p6 = os.path.join(ROOT, 'data', 'storylines', 'novel', 'SC-001-06-v4.md')
w('AUDIO_CH6_V4: %s' % ('EXISTS' if os.path.exists(p6) else 'MISSING (bm-a gate)'))

# export freshness + live three lines
se = os.path.join(ROOT, 'docs', 'status-export.json')
d = json.load(io.open(se, encoding='utf-8'))
w('export_ts=%s (mtime %s)' % (d.get('export_ts'), time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(se)))))
live = d.get('live') or {}
if isinstance(live, dict):
    for k, v in live.items():
        w('LIVE[%s]: %s' % (k, str(v)[:180]))

io.open(os.path.join(ROOT, '.c3-tmp', 'r1352_gates.txt'), 'w', encoding='utf-8').write('\n'.join(OUT))
print('written lines:', len(OUT))
