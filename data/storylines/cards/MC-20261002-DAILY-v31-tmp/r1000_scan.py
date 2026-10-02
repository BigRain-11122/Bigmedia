# quick round scan: state + group consumption + existence checks (ASCII only per encoding law)
import json, re, io, os, datetime

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup'
BM = os.path.join(ROOT, 'media', 'BigStream')
OUT = os.path.join(BM, 'r_quick_scan_out.txt')
res = []
wm = {}

def rd(p):
    with io.open(p, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

res.append('now=%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# -- state.json --
try:
    st = json.loads(rd(os.path.join(BM, 'src', 'os', 'state.json')))
    res.append('== state ==')
    res.append('tick=%s ts=%s' % (st.get('tick'), st.get('ts')))
    res.append('task=%s' % st.get('task'))
    res.append('production=%s' % json.dumps(st.get('production'), ensure_ascii=False))
    wm = st.get('decisions_watermark') or {}
    res.append('wm_meta=%s' % json.dumps({k: v for k, v in wm.items() if k != 'dnums'}, ensure_ascii=False))
    res.append('dnums=%s' % json.dumps(wm.get('dnums'), ensure_ascii=False))
    log = st.get('log') or []
    res.append('log_len=%d' % len(log))
    for e in log[-5:]:
        res.append('LOG| ' + (e if isinstance(e, str) else json.dumps(e, ensure_ascii=False)))
except Exception as ex:
    res.append('state ERR %r' % ex)

# -- group decisions.md --
try:
    dec = rd(os.path.join(ROOT, 'docs', 'decisions.md'))
    nums = sorted(set(re.findall(r'[DC]-\d{8}-\d+', dec)))
    dnums = set(wm.get('dnums') or [])
    new = [n for n in nums if n not in dnums]
    res.append('== group decisions ==')
    res.append('total_nums=%d new_vs_wm=%s' % (len(nums), new))
    dl = dec.splitlines()
    res.append('-- decisions top 50 lines --')
    for i, ln in enumerate(dl[:50]):
        res.append('%d| %s' % (i + 1, ln))
except Exception as ex:
    res.append('dec ERR %r' % ex)

# -- group orders.md CEO physical items area --
try:
    od = rd(os.path.join(ROOT, 'docs', 'orders.md')).splitlines()
    res.append('== group orders.md ==')
    idx = None
    key = '\u5f85\u529e\u7269\u7406\u4ef6'
    for i, ln in enumerate(od):
        if key in ln:
            idx = i
            break
    if idx is None:
        res.append('physical section header not found; top 35 lines:')
        for i, ln in enumerate(od[:35]):
            res.append('%d| %s' % (i + 1, ln))
    else:
        res.append('physical area from line %d:' % (idx + 1))
        for i in range(idx, min(idx + 25, len(od))):
            res.append('%d| %s' % (i + 1, od[i]))
except Exception as ex:
    res.append('orders ERR %r' % ex)

# -- evolution ledger tagged lines (last 12) --
try:
    ev = rd(os.path.join(ROOT, 'cph4', 'evolution-ledger.md')).splitlines()
    tags = ['@BigStream', '@\u4e03\u7ebf\u5168\u53f8', '@\u516d\u53f8', '@\u5168\u53f8']
    hits = [(i + 1, ln) for i, ln in enumerate(ev) if any(t in ln for t in tags)]
    res.append('== evolution-ledger tagged: total=%d (last 12) ==' % len(hits))
    for i, ln in hits[-12:]:
        res.append('%d| %s' % (i, ln[:280]))
except Exception as ex:
    res.append('ev ERR %r' % ex)

# -- local orders dir --
try:
    odr = os.path.join(BM, 'orders')
    fs = [(os.path.getmtime(os.path.join(odr, f)), f) for f in os.listdir(odr)]
    fs.sort()
    res.append('== local orders last 8 ==')
    res.extend('%s| %s' % (datetime.datetime.fromtimestamp(m).strftime('%m-%d %H:%M'), f) for m, f in fs[-8:])
except Exception as ex:
    res.append('odr ERR %r' % ex)

# -- existence checks --
res.append('== checks ==')
res.append('intel_today=%s' % os.path.exists(os.path.join(BM, 'data', 'intel', 'daily', '2026-10-02.md')))
try:
    aud = os.path.join(BM, 'docs', 'audits')
    res.append('audits_recent=%s' % sorted(os.listdir(aud))[-6:])
except Exception as ex:
    res.append('audits ERR %r' % ex)
try:
    g = rd(os.path.join(BM, 'docs', 'global-benchmarks.md')).splitlines()
    for i, ln in enumerate(g):
        if '\u2463' in ln:
            res.append('-- benchmarks sec4 @line %d --' % (i + 1))
            res.extend(g[i:i + 10])
            break
except Exception as ex:
    res.append('bench ERR %r' % ex)

# -- backlog top 30 --
try:
    bg = rd(os.path.join(BM, 'src', 'os', 'backlog.md')).splitlines()
    res.append('== backlog top 30 ==')
    res.extend(bg[:30])
except Exception as ex:
    res.append('bg ERR %r' % ex)

io.open(OUT, 'w', encoding='utf-8').write('\n'.join(res))
print('OK lines=%d' % len(res))
