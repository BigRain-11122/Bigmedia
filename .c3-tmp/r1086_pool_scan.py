# -*- coding: utf-8 -*-
"""R1086 E30 DAILY v63 attempt -> fresh supply-face scan (fleet includes DAILY-v62).
Context: 2026-10-03 Saturday National Day holiday day 3, production ~11:0x LITERAL MORNING
(late-morning window). Gate deltas vs R1032 deep-night scan:
  * MORNING gate: deep-night weak-adjacency LIFTED at literal morning hours (R1031 pre-registration
    fired at R1062/v62 ~07:0x; THIS round ~11:0x = same morning window, still literal).
    Per-row residue gates stay: market-stall/business rows = 3-LINK-ISO at any hour (R1032 close-out
    note); angling rows = post-v62 future-blocked registration (R1062); xiaoyao/morning/1 consumed v62.
  * WEEKEND gate: four-peat RESET ACHIEVED - v61 (market_close) + v62 (morning) = two non-weekend
    interventions after the v58/v59/v60 three-run -> weekend rows RE-OPEN (R1032 unlock-window line
    "weekend/3+4 (sprite) blocked until >=1 non-weekend piece intervenes" condition met, DOUBLE).
  * Standing gates unchanged: season (heatwave/coldsnap in Oct), event buckets need same-day anchor
    (10-03 daily brief: no rain/typhoon/CEO-order event; D-20261003 batch = admin decisions R1031
    ruling), market_open holiday closure until 10-08, night/dusk no adjacency at 11:0x.
Rotation post-v62 (xiaoyao consumed): qiuxin 10 / huaijiu 9 / xiaqi 10 / yanhuo 10 / zhixu 9 /
xiaoyao 11 -> minimum pair huaijiu 9 + zhixu 9 -> longest gap = zhixu (last v53, gap v54..v62 = 9).
Same probe standard as r1032/r1023-r1031: 2-5 char punctuation-inclusive shingles, card-face level
(lines + source_quote, R1010 law), city-spirit.md included. Output: .c3-tmp/r1086_pool_scan.txt.
"""
import io, json, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
BASE = os.path.join(ROOT, 'data', 'storylines', 'cards')

pool = json.load(io.open(os.path.join(ROOT, '..', '..', 'life', 'BigLife', 'cognition', 'pools.json'), encoding='utf-8'))
spirit = io.open(os.path.join(ROOT, 'data', 'storylines', 'codex', 'city-spirit.md'), encoding='utf-8').read()

faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, 'cards.json')
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding='utf-8'))
        face = u'\n'.join(u'\n'.join(c.get('lines', [])) for c in cfg.get('cards', []))
        sq = cfg.get('meta', {}).get('source_quote', u'')
        faces[d] = face + u'\n' + sq

def shingles(text, lo=2, hi=5):
    s = set()
    n = len(text)
    for L in range(lo, hi + 1):
        for i in range(0, n - L + 1):
            s.add(text[i:i + L])
    return s

SEASONAL = [u'年味', u'过年', u'春联', u'春雨', u'除夕', u'拜年', u'红包', u'元宵', u'汤圆', u'年年有余']
ISO_MARKET = [u'生意', u'买卖', u'早市', u'摊', u'市集', u'菜场', u'粥', u'开店', u'开市']
ISO_ANGLING = [u'钓', u'竿']

def probe(text):
    hits = {}
    for sh in sorted(shingles(text), key=len, reverse=True):
        if len(sh) < 2:
            continue
        where = sorted(d for d, f in faces.items() if sh in f)
        spirit_hit = sh in spirit
        if not where and not spirit_hit:
            continue
        hits[sh] = (u','.join(where) if where else u'city-spirit')
    kept = []
    for sh in sorted(hits, key=len, reverse=True):
        if any(sh != k and sh in k for k in [x[0] for x in kept]):
            continue
        kept.append((sh, hits[sh]))
    return kept

AXES = [u'求新', u'怀旧', u'侠气', u'烟火', u'秩序', u'逍遥']
BUCKETS = [u'night', u'festival', u'dusk', u'market_close', u'morning', u'weekend',
           u'rain', u'typhoon', u'heatwave', u'coldsnap', u'market_open', u'ceo_order']
SEASON_BLOCKED = {u'heatwave', u'coldsnap'}
EVENT_BLOCKED = {u'rain', u'typhoon', u'ceo_order'}
CLOSURE_BLOCKED = {u'market_open'}

out = io.StringIO()
def w(s):
    out.write(s)
    out.write(u'\n')

w(u'R1086 E30 DAILY v63 attempt -> fresh supply-face scan (fleet includes DAILY-v62 xiaoyao/morning/1)')
w(u'Day-context: 2026-10-03 Saturday National Day holiday day 3, production ~11:0x LITERAL MORNING (late-morning window)')
w(u'Gate deltas vs R1032: MORNING literal-window OPEN (R1031 pre-registration fired v62; ~11:0x same window) / WEEKEND four-peat RESET achieved (v61+v62 double intervention) / per-row residue gates stay (market-stall-business 3-link-iso any hour, angling post-v62 future-block, v62 line consumed)')
w(u'Rotation post-v62: qiuxin 10 / huaijiu 9 / xiaqi 10 / yanhuo 10 / zhixu 9 / xiaoyao 11 -> minimum pair huaijiu+zhixu 9 -> longest gap = zhixu (v53..v62 = 9)')
w(u'=' * 70)

ungated = []
inventory = {}
for axis in AXES:
    clean_total = []
    for bk in BUCKETS:
        rows = pool['axes'][axis][bk]
        for i, line in enumerate(rows):
            if any(s in line for s in SEASONAL):
                continue
            if probe(line):
                continue
            clean_total.append((bk, i, line))
    inventory[axis] = clean_total
    w(u'== %s clean rows (fresh vs fleet-v62): %d ==' % (axis, len(clean_total)))
    for bk, i, line in clean_total:
        gate = []
        if bk in SEASON_BLOCKED: gate.append(u'SEASON(Oct, R972-adjacent)')
        if bk in EVENT_BLOCKED: gate.append(u'NO-EVENT-TODAY')
        if bk in CLOSURE_BLOCKED: gate.append(u'HOLIDAY-CLOSURE(v57)')
        if bk == u'night': gate.append(u'NO-NIGHT-ADJACENCY-11AM')
        if bk == u'dusk': gate.append(u'NO-DUSK-ADJACENCY-11AM')
        if bk == u'morning':
            if any(m in line for m in ISO_MARKET): gate.append(u'MARKET-STALL/BIZ-3LINK-ISO(any-hour,R1032)')
            if any(m in line for m in ISO_ANGLING): gate.append(u'ANGLING-POSTV62-FUTURE-BLOCK(R1062-reg)')
            if line == u'鱼竿一甩，梦醒时分': gate.append(u'CONSUMED-v62')
            if not gate: gate.append(u'MORNING-WINDOW-OPEN')
        if bk == u'weekend':
            gate.append(u'WEEKEND-RESET(v61+v62)-OPEN' if not gate else u'')
            gate = [g for g in gate if g]
        w(u'   %s/%d %s -> %s' % (bk, i, line, u' + '.join(gate) if gate else u'NO-GATE?!'))
        if not gate:
            ungated.append((axis, bk, i, line))
    w(u'=' * 70)

sc = []
for bk in BUCKETS:
    rows = pool['sprite'][bk]
    for i, line in enumerate(rows):
        if probe(line):
            continue
        sc.append((bk, i, line))
w(u'== sprite clean rows (fresh vs fleet-v62): %d ==' % len(sc))
for bk, i, line in sc:
    gate = []
    if bk in SEASON_BLOCKED: gate.append(u'SEASON(Oct)')
    if bk in EVENT_BLOCKED: gate.append(u'NO-EVENT-TODAY')
    if bk in CLOSURE_BLOCKED: gate.append(u'HOLIDAY-CLOSURE(v57)')
    if bk == u'night': gate.append(u'SPRITE-NIGHT-BUCKET-NO-ADJ-11AM')
    if bk == u'night' or (u'夜' in line and bk != u'night'):
        if u'夜' in line: gate.append(u'NIGHT-CONTENT-AT-DAY-WEAK(R1020-literal-law)')
    if bk == u'market_close': gate.append(u'TWIN-BLOCKED(R1031-reg: shining-night twin of v61)')
    if bk == u'weekend':
        gate.append(u'WEEKEND-RESET-OPEN(R1032 unlock window: >=1 non-weekend piece intervenes -> v61+v62 DOUBLE)')
        if u'夜' in line: gate.append(u'NIGHT-CONTENT-AT-DAY-WEAK')
        if u'晨' in line: gate.append(u'MORNING-CONTENT-LITERAL-11AM')
    w(u'   sprite/%s/%d %s -> %s' % (bk, i, line, u' + '.join(gate) if gate else u'NO-GATE?!'))
    weak = (u'夜' in line)
    if not weak and bk == u'weekend':
        ungated.append((u'sprite', bk, i, line))

w(u'=' * 70)
w(u'VERDICT: rows passing zero-collision + all context gates (excl. weak-adjacency night-content rows) = %d' % len(ungated))
for a, bk, i, line in ungated:
    w(u'   !! %s/%s/%d %s' % (a, bk, i, line))
io.open(os.path.join(ROOT, '.c3-tmp', 'r1086_pool_scan.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('r1086 scan done. ungated=%d fleet_dirs=%d' % (len(ungated), len(faces)))
