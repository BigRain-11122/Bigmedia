import json, re, io, os, datetime
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
G = r"C:\Users\sjs20\Desktop\FluxGroup"
out = io.StringIO()
now = datetime.datetime.now()
out.write("NOW=%s\n" % now.strftime("%Y-%m-%d %H:%M:%S"))

st = json.load(open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
out.write("tick=%s ts=%s\n" % (st.get('tick'), st.get('ts')))
out.write("task=%s\n" % str(st.get('task', ''))[:150])
log = st.get('log', [])
out.write("log_len=%d\n" % len(log))
for e in log[-3:]:
    s = e if isinstance(e, str) else json.dumps(e, ensure_ascii=False)
    out.write("LOG: %s\n" % s[:300])
wm = st.get('decisions_watermark', {})
dn = wm.get('dnums', []) if isinstance(wm, dict) else []
out.write("watermark_n=%d\n" % len(dn))

dec_path = os.path.join(G, 'docs', 'decisions.md')
dec = open(dec_path, encoding='utf-8').read()
nums = set(re.findall(r'[DC]-\d{8}-\d+', dec))
new = sorted(nums - set(dn))
out.write("decisions_total=%d new_vs_wm=%d\n" % (len(nums), len(new)))
for n in new[:20]:
    out.write("NEWDEC: %s\n" % n)

lines = dec.splitlines()
for i, l in enumerate(lines[:60]):
    if l.strip():
        out.write("DECTOP L%d: %s\n" % (i + 1, l[:180]))

led = open(os.path.join(G, 'cph4', 'evolution-ledger.md'), encoding='utf-8').read().splitlines()
hits = [(i + 1, l) for i, l in enumerate(led) if '@BigStream' in l or '@七线全司' in l or '@全司' in l or '@六司' in l or '@八线' in l]
out.write("ledger_group_lines=%d\n" % len(hits))
for i, l in hits[-8:]:
    out.write("LED L%d: %s\n" % (i, l[:200]))

od = os.path.join(ROOT, 'orders')
fs = sorted(os.listdir(od), key=lambda f: os.path.getmtime(os.path.join(od, f)))
out.write("orders_latest=%s\n" % str(fs[-4:]))

for d in ['2026-10-05', '2026-10-04']:
    p = os.path.join(ROOT, 'data', 'intel', 'daily', d + '.md')
    out.write("daily %s exists=%s\n" % (d, os.path.exists(p)))

ap = os.path.join(ROOT, 'life_anchor_check')
for cid in ['C-00030', 'C-00031']:
    p = os.path.join(G, 'life', 'BigLife', 'census', 'anchors', cid + '.md')
    out.write("anchor %s exists=%s\n" % (cid, os.path.exists(p)))

lock = os.path.join(ROOT, '.git', 'index.lock')
out.write("index_lock=%s\n" % os.path.exists(lock))

gord = os.path.join(G, 'docs', 'orders.md')
if os.path.exists(gord):
    gl = open(gord, encoding='utf-8').read().splitlines()
    out.write("group_orders_lines=%d\n" % len(gl))
    for i, l in enumerate(gl[-12:]):
        if l.strip():
            out.write("GORD T%d: %s\n" % (len(gl) - 12 + i + 1, l[:180]))

open(os.path.join(ROOT, 'r1181_probe.txt'), 'w', encoding='utf-8').write(out.getvalue())
print("probe ok")
