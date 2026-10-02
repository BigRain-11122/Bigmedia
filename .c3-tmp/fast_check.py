import json, re, os, glob, io

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
out = io.StringIO()
def w(s): out.write(str(s) + '\n')

# 1) state.json core fields + log tail
st = json.load(open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
w('tick=%s ts=%s production=%s' % (st.get('tick'), st.get('ts'), st.get('production')))
w('task=%s' % str(st.get('task'))[:150])
log = st.get('log', [])
w('log_len=%d' % len(log))
for line in log[-5:-1]:
    w('LOGTAIL: ' + str(line)[:300])
if log:
    w('LOGLAST: ' + str(log[-1])[:900])
wm = st.get('decisions_watermark', {})
dn = wm.get('dnums', []) if isinstance(wm, dict) else []
w('wm_dnums_count=%s tail=%s' % (len(dn), dn[-10:]))

# 2) group decisions.md content-addressed watermark diff
try:
    txt = open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', encoding='utf-8').read()
    dnums = sorted(set(re.findall(r'[DC]-\d{8}-\d{2}', txt)))
    known = set(str(x) for x in dn)
    w('group_dnums_count=%d tail=%s' % (len(dnums), dnums[-12:]))
    w('NEW_DNUMS=%s' % [d for d in dnums if d not in known])
except Exception as e:
    w('decisions_err=%r' % e)

# 3) evolution-ledger transfer scan
try:
    etxt = open(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md', encoding='utf-8', errors='replace').read()
    elines = etxt.splitlines()
    pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
    at = [l for l in elines if pat.search(l)]
    w('ledger_at_count=%d' % len(at))
    for l in at[-3:]:
        w('LEDGER_TAIL: ' + l[:240])
    pl = [l for l in elines if re.match(r'\s*P-2026\d{4}', l)]
    w('ledger_P_count=%d' % len(pl))
    for l in pl[-3:]:
        w('PLINE_TAIL: ' + l[:200])
except Exception as e:
    w('ledger_err=%r' % e)

# 4) OSS harvest window files
oh = glob.glob(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\oss-harvest\OH-*-bigstream.md')
w('OH_files=%s' % sorted(os.path.basename(f) for f in oh))

# 5) daily brief / weekly audit / global benchmarks
w('daily_brief_1002=%s' % os.path.exists(os.path.join(ROOT, 'data', 'intel', 'daily', '2026-10-02.md')))
w('audit_W40=%s' % sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, 'docs', 'audits', '*W40*'))))
gb = os.path.join(ROOT, 'docs', 'global-benchmarks.md')
if os.path.exists(gb):
    t = open(gb, encoding='utf-8').read()
    m = re.findall(r'2026-\d\d-\d\d', t[:4000])
    w('benchmarks_head_dates=%s' % m[:5])

# 6) finished.md F count
fm = os.path.join(ROOT, 'output', 'finished.md')
t = open(fm, encoding='utf-8').read()
fnums = re.findall(r'F-(\d{3})', t)
w('finished_F_max=%s distinct=%d' % (max(fnums) if fnums else None, len(set(fnums))))

# 7) orders dir latest
od = sorted(glob.glob(os.path.join(ROOT, 'orders', '*')), key=os.path.getmtime)
w('orders_latest=%s' % [(os.path.basename(f), os.path.getmtime(f)) for f in od[-3:]])

# 8) probe scripts
w('probe_scripts=%s' % sorted(set(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, 'src', '*probe*.py')) + glob.glob(os.path.join(ROOT, 'src', 'os', '*probe*.py')))))

open(os.path.join(ROOT, '.c3-tmp', 'fast_check_out.txt'), 'w', encoding='utf-8').write(out.getvalue())
print('done')
