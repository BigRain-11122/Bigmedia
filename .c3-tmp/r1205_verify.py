import io, json, re, subprocess, os
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
d = json.load(io.open(os.path.join(ROOT, 'src', 'os', 'state.json'), encoding='utf-8'))
out = []
out.append('tick=%s ts=%s' % (d['tick'], d['ts']))
out.append('task=%s' % d['task'])
out.append('focus=%s' % d.get('focus', '')[:260])
last = d['log'][-1]
out.append('LOG_LAST_LEN=%d' % len(last))
out.append('LOG_LAST_HEAD=%s' % last[:150])
out.append('typo_token_present=%s' % ('P-20260-09-28-02' in last))
out.append('has_R1205=%s' % ('R1205:' in last))
out.append('morning_rows_claim=%s' % ('morning 残行 5 行' in last))
# watermark unchanged check
wm = d.get('decisions_watermark', {}).get('dnums', [])
out.append('wm_count=%s' % len(wm))
# git status snapshot
r = subprocess.run(['git', 'status', '--short'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
out.append('GIT=%s' % (r.stdout.strip().replace('\n', ' | ')[:600]))
# r1180 misnamed files really gone?
gone = [f for f in ('r1180_check.py', 'r1180_check.txt', 'r1180_dec.txt') if os.path.exists(os.path.join(ROOT, f))]
out.append('r1180_residue=%s' % (gone if gone else 'NONE'))
io.open(os.path.join(ROOT, '.c3-tmp', 'r1205_verify.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('verify written')
