# R750 quick five-check scan (read-only)
import re, os, json

BS = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
FG = r'C:\Users\sjs20\Desktop\FluxGroup'

st = json.load(open(os.path.join(BS, 'src', 'os', 'state.json'), encoding='utf-8'))
base_dnums = set(st['decisions_watermark']['dnums'])
print('BASE_DNUMS', len(base_dnums))

dec = open(os.path.join(FG, 'docs', 'decisions.md'), encoding='utf-8', errors='replace').read()
toks = sorted(set(re.findall(r'[DC]-\d{8}-\d{2}', dec)))
new = [t for t in toks if t not in base_dnums]
print('DEC_DNUM_TOTAL', len(toks), 'DEC_DNUM_NEW', len(new), '|'.join(new))

led = open(os.path.join(FG, 'cph4', 'evolution-ledger.md'), encoding='utf-8', errors='replace').read().splitlines()
pats = ['@BigStream', '@\u4e03\u7ebf\u5168\u53f8', '@\u5168\u53f8', '@\u516d\u53f8', '@\u516b\u7ebf\u5168\u91cf']
hits = [(i + 1, l) for i, l in enumerate(led) if any(p in l for p in pats)]
print('LEDGER_HITS', len(hits))
for i, l in hits[-3:]:
    print('LED', i, l[:100].encode('unicode_escape').decode('ascii')[:200])

od = os.path.join(BS, 'orders')
files = sorted(os.listdir(od))
print('ORDERS_COUNT', len(files))
print('ORDERS_LAST', files[-1] if files else 'none')

print('LOCK', os.path.exists(os.path.join(BS, '.git', 'index.lock')))
