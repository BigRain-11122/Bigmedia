import json, re, io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = json.load(open(os.path.join(ROOT, 'src/os/state.json'), encoding='utf-8'))
o = io.open(os.path.join(ROOT, '.c3-tmp/r1035_probe_out.txt'), 'w', encoding='utf-8')
o.write('keys=%s\n' % sorted(s.keys()))
o.write('tick=%s ts=%s production=%s\n' % (s.get('tick'), s.get('ts'), s.get('production')))
o.write('task=%s\n' % s.get('task'))
wm = s.get('decisions_watermark') or {}
o.write('wm_keys=%s\n' % sorted(wm.keys()) if isinstance(wm, dict) else 'wm=%s\n' % wm)
try:
    dnums = wm.get('dnums') or []
except Exception:
    dnums = []
o.write('wm_dnums_count=%d\n' % len(dnums))
logs = s.get('log') or []
o.write('log_count=%d\n' % len(logs))
for l in logs[-4:]:
    o.write('--- LOGTAIL %s\n' % l)

# group decisions.md content-addressed diff
dpath = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'
if os.path.exists(dpath):
    d = io.open(dpath, encoding='utf-8').read()
    nums = set(re.findall(r'[DC]-\d{8}-\d+', d))
    old = set(dnums)
    o.write('DEC_TOTAL=%d WM_COUNT=%d\n' % (len(nums), len(old)))
    o.write('DEC_NEW=%s\n' % sorted(nums - old))
    o.write('DEC_GONE=%s\n' % sorted(old - nums))
else:
    o.write('DEC_FILE_MISSING\n')

# local orders dir newest
odir = os.path.join(ROOT, 'orders')
files = sorted(os.listdir(odir), key=lambda f: os.path.getmtime(os.path.join(odir, f)), reverse=True)[:6]
o.write('ORDERS_NEWEST=%s\n' % files)
o.close()
print('OK')
