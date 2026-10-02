# -*- coding: utf-8 -*-
"""R1031 round-opening check: light five-check (fresh) + DAILY v61 supply cascade scan.

Five-check (light, mtime-anchored, R1030 fresh check 00:03 was 25 min ago):
  orders count/top + group orders.md mtime, ledger mtime (frozen baseline
  2026-10-02 15:18:25), decisions mtime (frozen 12:09:58) + canonical dnum set
  diff vs state watermark (127), index.lock, production=open, 10-03 daily brief
  present (R1030 produced), CENSUS C-00030 anchor absent, OH-20261002 present.

Supply cascade for DAILY v61 (fleet includes DAILY-v60 F-145):
  post-v60 rotation: qiuxin 10 / huaijiu 9 / xiaqi 10 / yanhuo 10 / zhixu 9 /
  xiaoyao 10 -> TWO axes tied at 9 -> target zhixu (gap v54..v60 = 7 LONGEST)
  -> zhixu clean rows rain/2 + coldsnap/2+9 (event/season blocked)
  -> huaijiu (gap 5): heatwave/8 + coldsnap/7 + market_open/6+7+9 + ceo_order/3+10
  (season/holiday-closure/no-event blocked)
  -> qiuxin (gap 3): heatwave/0+9 (season blocked)
  -> yanhuo (gap 2): morning/6+7 (market-stall 3-link isomorphism with v57+v58,
  R1029 precedent + deep-night weak adjacency) ; others blocked
  -> xiaqi (gap 1): morning/0+15 (same market/business 3-link + twin-line note)
  -> xiaoyao (gap 0, just used v60): morning twins + rain/17 + blocked
  -> ALL SIX AXES blocked/excluded -> sprite backup face (R1022/R1024 precedent,
  R1030 pointer pre-registered sprite third-voice candidates)
  -> sprite clean rows: weekend/3+4 (weekend bucket FOUR-peat after v58/v59/v60
  three-run + deep-night/morning weak + v50 onomatopoeia+night construct adjacency)
  + typhoon/heatwave/market_open/ceo_order (event/season/holiday blocked)
  -> sprite/market_close/3 「灵光闪烁夜未央」 = UNIQUE honestly-pairable row
  (market_close bucket = National Day closed-market state, v55/v57 precedent +
  content ye-wei-yang = LITERAL deep-night match at ~00:3x production).
Output: .c3-tmp/r1031_check.txt (five-check) + .c3-tmp/r1031_pool.txt (cascade).
"""
import io, json, os, re, time

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
GRP = os.path.join(ROOT, '..', '..')
NOW = time.strftime('%Y-%m-%d %H:%M:%S')

out = io.StringIO()
def w(s):
    out.write(s if isinstance(s, str) else s.encode('utf-8').decode('utf-8'))
    out.write(u'\n')

# ---------- five-check (light) ----------
w(u'R1031 round-opening light five-check @ ' + NOW)
w(u'=' * 70)
orders_dir = os.path.join(ROOT, 'orders')
ofiles = sorted(f for f in os.listdir(orders_dir) if f.endswith('.md'))
top = sorted(ofiles, key=lambda f: -os.path.getmtime(os.path.join(orders_dir, f)))[0]
w(u'orders: %d files, top=%s (anchor 42 = 41 O- + README, top anchor O-20260928-1910-bm-a)' % (len(ofiles), top))

ledger = os.path.join(GRP, 'cph4', 'evolution-ledger.md')
lm = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(ledger)))
w(u'ledger mtime: %s (frozen baseline 2026-10-02 15:18:25; unchanged = zero new dispatch rows)' % lm)

dec = os.path.join(GRP, 'docs', 'decisions.md')
dm = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(dec)))
w(u'decisions mtime: %s (frozen baseline 2026-10-02 12:09:58)' % dm)
dtext = io.open(dec, encoding='utf-8').read()
dnums = set(re.findall(r'[DC]-\d{8}-\d{2}(?!\d)', dtext))
st = json.load(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
wm = set(st['decisions_watermark']['dnums'])
new = sorted(dnums - wm)
w(u'dnum content-addressed diff: %s (watermark %d)' % (u'NONE' if not new else u'NEW: ' + u','.join(new), len(wm)))

lock = os.path.exists(os.path.join(ROOT, '.git', 'index.lock'))
w(u'index.lock present: %s' % lock)
w(u'production: %s (self-heal check)' % st.get('production'))
brief = os.path.exists(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-10-03.md'))
w(u'10-03 daily brief present: %s (R1030 produced 00:0x, one-per-day truth)' % brief)
anchors = sorted(f for f in os.listdir(os.path.join(GRP, 'life', 'BigLife', 'census', 'anchors')) if f.endswith('.md'))
c30 = [a for a in anchors if re.match(r'C-\d{5}\.md', a) and int(a[2:7]) >= 30]
w(u'CENSUS anchors top=%s, C-00030+ count=%d (supply gate %s)' % (anchors[-1] if anchors else 'NONE', len(c30), u'CLOSED' if not c30 else 'OPEN'))
oh = os.path.exists(os.path.join(GRP, 'cph4', 'oss-harvest', 'OH-20261002-bigstream.md'))
w(u'OH-20261002 present: %s (window-3 slice-1 obligation met, slices 2+ optional)' % oh)
five_ok = (len(ofiles) == 42 and top == 'O-20260928-1910-bm-a.md' and lm == '2026-10-02 15:18:25'
           and not new and not lock and st.get('production') == 'open' and brief and not c30 and oh)
w(u'FIVE-CHECK: %s' % (u'ALL QUIET' if five_ok else u'DELTA FOUND - see lines above'))
io.open(os.path.join(ROOT, '.c3-tmp', 'r1031_check.txt'), 'w', encoding='utf-8').write(out.getvalue())

# ---------- supply cascade scan ----------
out2 = io.StringIO()
def v(s):
    out2.write(s)
    out2.write(u'\n')

BASE = os.path.join(ROOT, 'data', 'storylines', 'cards')
pool = json.load(io.open(os.path.join(GRP, 'life', 'BigLife', 'cognition', 'pools.json'), encoding='utf-8'))
spirit = io.open(os.path.join(ROOT, 'data', 'storylines', 'codex', 'city-spirit.md'), encoding='utf-8').read()

faces = {}
for d in sorted(os.listdir(BASE)):
    cj = os.path.join(BASE, d, 'cards.json')
    if os.path.isfile(cj):
        cfg = json.load(io.open(cj, encoding='utf-8'))
        face = u'\n'.join(u'\n'.join(c.get('lines', [])) for c in cfg.get('cards', []))
        sq = cfg.get('meta', {}).get('source_quote', u'')
        faces[d] = face + u'\n' + sq

v(u'R1031 DAILY v61 supply cascade scan (fleet includes DAILY-v60 xiaoyao/weekend/4 F-145)')
v(u'Day-context: 2026-10-03 Saturday National Day holiday day 3, production ~00:3x LITERAL DEEP NIGHT')
v(u'Rotation post-v60: qiuxin 10 / huaijiu 9 / xiaqi 10 / yanhuo 10 / zhixu 9 / xiaoyao 10')
v(u'Two axes tied at minimum 9: zhixu (gap v54..v60 = 7 LONGEST) / huaijiu (gap v56..v60 = 5)')
v(u'=' * 70)

def shingles(text, lo=2, hi=5):
    s = set()
    n = len(text)
    for L in range(lo, hi + 1):
        for i in range(0, n - L + 1):
            s.add(text[i:i + L])
    return s

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

SEASONAL = [u'年味', u'过年', u'春联', u'春雨', u'除夕', u'拜年', u'红包', u'元宵', u'汤圆', u'年年有余']
AXES = [u'秩序', u'怀旧', u'求新', u'烟火', u'侠气', u'逍遥']
BLOCK = {
    u'秩序': u'rain=no-rain-event(context) coldsnap=Oct-season(R972-adjacent)',
    u'怀旧': u'heatwave/coldsnap=season market_open=holiday-closure(v57 ruling) ceo_order=no-event',
    u'求新': u'heatwave=Oct-season(R972-adjacent)',
    u'烟火': u'morning6/7=market-stall 3-link isomorphism v57+v58(R1029 precedent)+deep-night weak; heatwave/market_open/ceo_order blocked',
    u'侠气': u'morning0/15=business 3-link(R1029 precedent)+twin-line note; rain/typhoon=no-event; heatwave/coldsnap=season; ceo_order=no-event',
    u'逍遥': u'gap 0 (just used v60); morning twins + rain/17 + season/event all blocked',
}
for ax in AXES:
    clean = []
    for bk, rows in pool['axes'][ax].items():
        for i, line in enumerate(rows):
            if any(s in line for s in SEASONAL):
                continue
            if not probe(line):
                clean.append(u'%s/%d %s' % (bk, i, line))
    v(u'== %s clean rows (fresh vs fleet-v60): %d == %s' % (ax, len(clean), u'; '.join(clean) if clean else u'NONE'))
    v(u'   block/exclude: %s' % BLOCK[ax])
v(u'=' * 70)

sp_clean = []
for bk, rows in pool.get('sprite', {}).items():
    for i, line in enumerate(rows):
        if any(s in line for s in SEASONAL):
            continue
        if not probe(line):
            sp_clean.append((bk, i, line))
v(u'== sprite clean rows (fresh vs fleet-v60): %d ==' % len(sp_clean))
for bk, i, line in sp_clean:
    v(u'  sprite/%s/%d %s' % (bk, i, line))
v(u'   sprite exclusions: weekend/3+4 = weekend bucket FOUR-peat after v58/v59/v60 three-run (bucket-level isomorphism R442) + morning/deep-night weak adjacency + weekend/4 v50 onomatopoeia+night construct adjacency; typhoon/3 no-typhoon-event; heatwave/3+11 Oct-season; market_open/3 holiday-closure; ceo_order/* no-CEO-order-event; market_close/9 = TWIN of winner (future-twin-blocked after this use)')
v(u'-> WINNER: sprite/market_close/3 (unique honestly-pairable row; market_close = National Day closed-market state v55/v57 precedent + ye-wei-yang content = literal deep-night double anchor at ~00:3x production)')
WIN = pool['sprite'][u'market_close'][3]
kept = probe(WIN)
v(u'-> winner zero-hit verification: %s' % (u'ALL 2-5 char shingles ZERO (9th fully-zero row candidate, v53-v60 eight precedents)' if not kept else u'HITS: %s' % kept))
v(u'-> twin note: sprite/market_close/9 %s becomes future-twin-blocked' % pool['sprite'][u'market_close'][9])
v(u'-> v54 family adjacency honest note: 闪闪灯辉照长廊 [sprite+light+night PLACE facet] vs 灵光闪烁夜未央 [sprite+light+night TIME facet] = same family heterogeneous facet; shingle-level distinct (闪闪 vs 闪烁)')
io.open(os.path.join(ROOT, '.c3-tmp', 'r1031_pool.txt'), 'w', encoding='utf-8').write(out2.getvalue())
print('r1031 check+pool done, five_ok=%s, winner=%s, zero_hit=%s' % (five_ok, WIN.encode('unicode_escape').decode()[:40], not kept))
