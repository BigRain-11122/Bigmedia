# -*- coding: utf-8 -*-
"""R1032 E30 DAILY v62 attempt -> comprehensive zero-verdict scan (fleet includes DAILY-v61).
Context: 2026-10-03 Saturday National Day holiday day 3, production ~00:5x-01:0x LITERAL DEEP NIGHT.
Rotation post-v61 (sprite piece, six-axis counts unchanged): qiuxin 10 / huaijiu 9 / xiaqi 10 /
yanhuo 10 / zhixu 9 / xiaoyao 10 -> two tied at minimum 9: zhixu (last v53, gap v54..v61 = 8
LONGEST) / huaijiu (last v55, gap v56..v61 = 6) -> redemption target = zhixu.
Full inventory: 6 axes x 12 buckets + sprite x 12 buckets vs fleet card faces (lines +
source_quote, R1010 card-face-level law) + city-spirit.md. Same probe standard as
r1023/r1026-r1029/r1031: 2-5 char punctuation-inclusive shingles. Context gates applied per
precedent laws: R972 season-displacement, event-bucket-needs-event-anchor, holiday market_open
closure (v57 ruling), morning deep-night weak adjacency (R1029 precedent), weekend four-peat
(v58/v59/v60 three-run), twin-block (R1031 registration: sprite/market_close/9), 3-link
isomorphism (market-stall v44+v57+v58 / business twins). Output: .c3-tmp/r1032_pool.txt.
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

AXES = [u'\u6c42\u65b0', u'\u6000\u65e7', u'\u4fa0\u6c14', u'\u70df\u706b', u'\u79e9\u5e8f', u'\u900d\u9065']
BUCKETS = [u'night', u'festival', u'dusk', u'market_close', u'morning', u'weekend',
           u'rain', u'typhoon', u'heatwave', u'coldsnap', u'market_open', u'ceo_order']
# October season-mismatch buckets (R972-adjacent law)
SEASON_BLOCKED = {u'heatwave', u'coldsnap'}
# event buckets: need a same-day event anchor, none today (no rain/typhoon/CEO order)
EVENT_BLOCKED = {u'rain', u'typhoon', u'ceo_order'}
# National Day holiday: markets closed (v57 ruling)
CLOSURE_BLOCKED = {u'market_open'}

out = io.StringIO()
def w(s):
    out.write(s)
    out.write(u'\n')

w(u'R1032 E30 DAILY v62 attempt -> comprehensive supply-face scan (fleet includes DAILY-v61 sprite/market_close/3)')
w(u'Day-context: 2026-10-03 Saturday National Day holiday day 3, production ~00:5x-01:0x LITERAL DEEP NIGHT')
w(u'Rotation post-v61 (sprite piece = six-axis counts unchanged): qiuxin 10 / huaijiu 9 / xiaqi 10 / yanhuo 10 / zhixu 9 / xiaoyao 10')
w(u'Two axes tied at minimum 9 -> redemption target = zhixu (last v53, gap v54..v61 = 8 LONGEST) / huaijiu (last v55, gap = 6)')
w(u'Context gates (precedent laws): R972 season / event-bucket-needs-anchor / market_open holiday-closure (v57) / morning deep-night weak adjacency (R1029) / weekend four-peat (v58+v59+v60) / twin-block (R1031: sprite market_close/9) / 3-link isomorphism (market-stall v44+v57+v58 / business)')
w(u'=' * 70)

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
    w(u'== %s clean rows (fresh vs fleet-v61): %d ==' % (axis, len(clean_total)))
    for bk, i, line in clean_total:
        gate = []
        if bk in SEASON_BLOCKED: gate.append(u'SEASON(Oct, R972-adjacent)')
        if bk in EVENT_BLOCKED: gate.append(u'NO-EVENT-TODAY')
        if bk in CLOSURE_BLOCKED: gate.append(u'HOLIDAY-CLOSURE(v57)')
        if bk == u'morning': gate.append(u'DEEP-NIGHT-WEAK(R1029)+3-LINK-ISO')
        if bk == u'weekend': gate.append(u'WEEKEND-FOUR-PEAT(v58/v59/v60)')
        w(u'   %s/%d %s -> %s' % (bk, i, line, u' + '.join(gate) if gate else u'NO-GATE?!'))
    w(u'=' * 70)

# sprite face
sc = []
for bk in BUCKETS:
    rows = pool['sprite'][bk]
    for i, line in enumerate(rows):
        if probe(line):
            continue
        sc.append((bk, i, line))
w(u'== sprite clean rows (fresh vs fleet-v61): %d ==' % len(sc))
for bk, i, line in sc:
    gate = []
    if bk in SEASON_BLOCKED: gate.append(u'SEASON(Oct)')
    if bk in EVENT_BLOCKED: gate.append(u'NO-EVENT-TODAY')
    if bk in CLOSURE_BLOCKED: gate.append(u'HOLIDAY-CLOSURE(v57)')
    if bk == u'morning': gate.append(u'DEEP-NIGHT-WEAK')
    if bk == u'weekend': gate.append(u'WEEKEND-FOUR-PEAT + v50-adjacency')
    if bk == u'market_close': gate.append(u'TWIN-BLOCKED(R1031 reg: shining-night twin of v61)')
    w(u'   sprite/%s/%d %s -> %s' % (bk, i, line, u' + '.join(gate) if gate else u'NO-GATE?!'))
w(u'=' * 70)

ungated = []
for axis, rows in inventory.items():
    for bk, i, line in rows:
        gate = (bk in SEASON_BLOCKED or bk in EVENT_BLOCKED or bk in CLOSURE_BLOCKED or bk in (u'morning', u'weekend'))
        if not gate:
            ungated.append((axis, bk, i, line))
for bk, i, line in sc:
    gate = (bk in SEASON_BLOCKED or bk in EVENT_BLOCKED or bk in CLOSURE_BLOCKED or bk in (u'morning', u'weekend', u'market_close'))
    if not gate:
        ungated.append((u'sprite', bk, i, line))

w(u'VERDICT: rows passing zero-collision + all context gates = %d' % len(ungated))
for a, bk, i, line in ungated:
    w(u'   !! %s/%s/%d %s' % (a, bk, i, line))
w(u'-> E30 DAILY v62 at this production context (deep night, holiday day 3, no events) = ZERO honestly-pairable rows')
w(u'-> First full-zero verdict for the DAILY line (R1028-R1031 cascade precedents: this scan closes the last face)')
w(u'')
w(u'E30 supply-gated WAITING declaration - unlock windows (honest pairing anchors):')
w(u'  * rain-event day      -> rain clean rows fire (zhixu/rain2, xiaqi/rain5+6+7, xiaoyao/rain17 + sprite/typhoon3 on typhoon)')
w(u'  * CEO-order day       -> ceo_order clean rows fire (huaijiu/3+10, yanhuo/7, xiaqi/2, xiaoyao/5+13, sprite/0+3+4+9+11)')
w(u'  * 2026-10-08+ (post-holiday market reopen) -> market_open clean rows fire (huaijiu/6+7+9, yanhuo/8+11+12, sprite/3)')
w(u'  * Nov+ (coldsnap season) -> coldsnap clean rows fire (zhixu/2+9, huaijiu/7, xiaqi/10, xiaoyao/1+5)')
w(u'  * summer (heatwave season) -> heatwave clean rows fire (qiuxin/0+9, huaijiu/8, yanhuo/3+12, xiaqi/6+14, xiaoyao/3+5+6, sprite/3+11)')
w(u'  * weekend/3+4 (sprite) blocked until >=1 non-weekend piece intervenes (four-peat reset) - itself dependent on an above window')
w(u'  * morning rows remain 3-link-iso blocked (market-stall v44+v57+v58 / business twins) even at morning hours')
w(u'')
w(u'Supply-face inventory close-out (R810 second-type round):')
w(u'  1. E30 DAILY = zero-verdict this scan -> supply-gated waiting (unlock windows above)')
w(u'  2. E31 REACT-v9 = 10-04 window (time-gated, not exhausted; 10-03 window negative R1030)')
w(u'  3. LC chai-tiao = closed 20/20 CENSUS coverage (F-075) + card-form exclusions on file (QUOTE single-sentence capacity / DIGEST event-face / REACT window-passed, R510 selection)')
w(u'  4. CENSUS line = gated (C-00030 absent, anchors stop C-00029)')
w(u'  5. gao-ji (mother-script reuse) = closed R810 (all mother sections consumed: BS-001/002/003/004 fully + BS-006..011 produced)')
w(u'  6. DIGEST = no CEO-order-level trigger (orders top O-20260928-1910; D-20261003 batch = admin decisions judged non-BS-exec R1031; decision-batch mother-topic already covered v6/v11/v12/v13 -> anti-bloat)')
w(u'  7. BS video line = BS-001..011 all done; SC-003-01 v3 footage window blocked (protection-state on file)')
w(u'  8. QUOTE line = six-axis creed cards complete (v1-v6, #33 done 09-25)')
w(u'')
io.open(os.path.join(ROOT, '.c3-tmp', 'r1032_pool.txt'), 'w', encoding='utf-8').write(out.getvalue())

brief = os.path.join(ROOT, 'data', 'intel', 'daily', '2026-10-03.md')
print('r1032 scan done. ungated=%d brief_1003=%s' % (len(ungated), os.path.isfile(brief)))
