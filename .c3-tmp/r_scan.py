import json, re, os, io, glob

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
GRP = r'C:\Users\sjs20\Desktop\FluxGroup'
os.makedirs(os.path.join(ROOT, '.c3-tmp'), exist_ok=True)
out = io.StringIO()
def w(s=''): out.write(str(s) + '\n')

# 1. state.json tail
try:
    st = json.load(open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8-sig'))
    w('== state ==')
    w('tick=%s | ts=%s | production=%s' % (st.get('tick'), st.get('ts'), st.get('production')))
    t = st.get('task')
    w('task=%s' % (str(t)[:160] if t else None))
    dw = st.get('decisions_watermark') or {}
    dn = dw.get('dnums') or []
    w('dnums_count=%d | last8=%s' % (len(dn), sorted(dn)[-8:]))
    logs = st.get('log') or []
    w('log_count=%d' % len(logs))
    for l in logs[-3:]:
        w('LOG: ' + str(l)[:650])
except Exception as e:
    w('state ERR %r' % e)

# 2. backlog items (all headers in file order)
try:
    bg = open(os.path.join(ROOT, 'src', 'os', 'backlog.md'), encoding='utf-8-sig').read().splitlines()
    w('== backlog items (total lines %d) ==' % len(bg))
    for i, ln in enumerate(bg):
        m = re.match(r'^(\d+)\.\s+', ln)
        if m:
            w('L%d #%s done=%s claim=%s | %s' % (i + 1, m.group(1), '[done' in ln, '[claim' in ln, ln[:100]))
except Exception as e:
    w('backlog ERR %r' % e)

# 3. orders dir top5 by mtime
try:
    od = os.path.join(ROOT, 'orders')
    fs = sorted(os.listdir(od), key=lambda f: os.path.getmtime(os.path.join(od, f)), reverse=True)
    w('== orders top5 ==')
    for f in fs[:5]:
        w(f)
except Exception as e:
    w('orders ERR %r' % e)

# 4. group evolution-ledger @hits
try:
    el = open(os.path.join(GRP, 'cph4', 'evolution-ledger.md'), encoding='utf-8-sig').read().splitlines()
    pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
    hits = [(i + 1, ln) for i, ln in enumerate(el) if pat.search(ln)]
    w('== ledger @hits=%d ==' % len(hits))
    for n, ln in hits[-3:]:
        w('L%d: %s' % (n, ln[:250]))
except Exception as e:
    w('ledger ERR %r' % e)

# 5. group decisions watermark diff + board block
try:
    dc = open(os.path.join(GRP, 'docs', 'decisions.md'), encoding='utf-8-sig').read()
    nums = set(re.findall(r'\b([DC]-\d{8}-\d{2})\b', dc))
    new = nums - set(dn)
    w('== decisions nums=%d | new_vs_watermark=%d %s ==' % (len(nums), len(new), sorted(new)))
    lines = dc.splitlines()
    w('== decisions top 60 lines ==')
    for i, ln in enumerate(lines[:60]):
        w('BD%d: %s' % (i + 1, ln[:200]))
except Exception as e:
    w('decisions ERR %r' % e)

# 6. group orders.md CEO physical-items zone
try:
    go = open(os.path.join(GRP, 'docs', 'orders.md'), encoding='utf-8-sig').read().splitlines()
    w('== group orders.md lines=%d ==' % len(go))
    idx = None
    for i, ln in enumerate(go):
        if '物理件' in ln:
            idx = i
            break
    if idx is not None:
        for ln in go[max(0, idx - 2):idx + 6]:
            w('GO: ' + ln[:180])
    else:
        w('GO: no 物理件 line found')
except Exception as e:
    w('gorders ERR %r' % e)

# 7. probe scripts discovery
w('== probes ==')
for pat in ['*board*.py', 'readiness.py', '*loop_health*.py']:
    for p in glob.glob(os.path.join(ROOT, 'src', '**', pat), recursive=True):
        w(p)

open(os.path.join(ROOT, '.c3-tmp', 'r_scan.md'), 'w', encoding='utf-8').write(out.getvalue())
print('OK')
