import json, re, io

OUT = io.open('.c3-tmp/scan_r798.txt', 'w', encoding='utf-8')
W = OUT.write

def rd(p):
    return io.open(p, encoding='utf-8', errors='replace').read()

# 1) state.json summary
st = json.loads(rd('src/os/state.json'))
W('== STATE ==\n')
W('tick=%s\n' % st.get('tick'))
W('production=%s\n' % st.get('production'))
W('ts=%s\n' % st.get('ts'))
W('task=%s\n' % st.get('task'))
W('keys=%s\n' % sorted(st.keys()))
wm = st.get('decisions_watermark')
W('decisions_watermark=%s\n' % json.dumps(wm, ensure_ascii=False))
log = st.get('log')
W('log_len=%s\n' % (len(log) if isinstance(log, list) else type(log).__name__))
if isinstance(log, list):
    for e in log[-3:]:
        W('LOG: %s\n' % (e if isinstance(e, str) else json.dumps(e, ensure_ascii=False)))

# 2) group decisions.md: D/C set + dispatch board head
dtxt = rd(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md')
W('\n== GROUP DECISIONS ==\n')
dnums = sorted(set(re.findall(r'[DC]-\d{8}-\d+', dtxt)))
W('dnum_count=%d\n' % len(dnums))
W('dnums=%s\n' % ','.join(dnums))
dl = dtxt.splitlines()
W('total_lines=%d head_25:\n' % len(dl))
for l in dl[:25]:
    W('  |%s\n' % l[:300])

# 3) evolution-ledger: @BigStream / group-wide tags
ltxt = rd(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md')
ll = ltxt.splitlines()
pat = re.compile('@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf)')
hits = [(i, l) for i, l in enumerate(ll, 1) if pat.search(l)]
W('\n== LEDGER ==\ntotal_lines=%d hits=%d\n' % (len(ll), len(hits)))
for i, l in hits[-6:]:
    W('L%d: %s\n' % (i, l[:400]))

# 4) group orders.md: physical-item section mentions
otxt = rd(r'C:\Users\sjs20\Desktop\FluxGroup\docs\orders.md')
ol = otxt.splitlines()
pat2 = re.compile('\u7269\u7406\u4ef6|\u8d26\u53f7|\u5546\u6237\u53f7|\u670d\u52a1\u5668')
h2 = [(i, l) for i, l in enumerate(ol, 1) if pat2.search(l)]
W('\n== GROUP ORDERS ==\ntotal_lines=%d hits=%d\n' % (len(ol), len(h2)))
for i, l in h2[-8:]:
    W('L%d: %s\n' % (i, l[:280]))

OUT.close()
print('ok')
