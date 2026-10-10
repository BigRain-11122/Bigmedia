import os, re, json, datetime
out = []
od = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\orders'
mt = 0; latest = ''
for f in os.listdir(od):
    p = os.path.join(od, f)
    if os.path.isfile(p):
        m = os.path.getmtime(p)
        if m > mt: mt, latest = m, f
out.append('OWN_ORDERS latest=%s mtime=%s' % (latest, datetime.datetime.fromtimestamp(mt).strftime('%m-%d %H:%M:%S')))
hq = r'C:\Users\sjs20\Desktop\FluxGroup\docs'
omt = os.path.getmtime(os.path.join(hq, 'orders.md'))
dmt = os.path.getmtime(os.path.join(hq, 'decisions.md'))
out.append('HQ orders.md mtime=%s (R1910 anchor 21:02:01)' % datetime.datetime.fromtimestamp(omt).strftime('%m-%d %H:%M:%S'))
out.append('HQ decisions.md mtime=%s' % datetime.datetime.fromtimestamp(dmt).strftime('%m-%d %H:%M:%S'))
txt = open(os.path.join(hq, 'decisions.md'), encoding='utf-8', errors='replace').read()
dset = set(re.findall(r'[DC]-\d{8}-\d{2}', txt))
wm = json.load(open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json', encoding='utf-8-sig'))
truly_new = dset - set(wm.get('decisions_watermark', {}).get('dnums', []))
out.append('decisions dnum total=%d truly_new=%d %s' % (len(dset), len(truly_new), sorted(truly_new)[:10]))
led = open(r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md', encoding='utf-8', errors='replace').read()
rows = [l for l in led.splitlines() if '@BigStream' in l or '@七线全司' in l or '@全司' in l or '@六司' in l or '@八线全量' in l]
out.append('ledger transfer-mention rows=%d' % len(rows))
import subprocess
r = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total,utilization.gpu', '--format=csv,noheader'], capture_output=True)
out.append('GPU: %s' % r.stdout.decode().strip())
meme = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\fleet\meme-daily-v1'
if os.path.isdir(meme):
    rec = []
    for root, dirs, files in os.walk(meme):
        for f in files:
            p = os.path.join(root, f)
            m = os.path.getmtime(p)
            if m > datetime.datetime(2026,10,10,15,41,53).timestamp():
                rec.append('%s %s' % (datetime.datetime.fromtimestamp(m).strftime('%H:%M:%S'), os.path.relpath(p, meme)))
    rec.sort()
    out.append('MEME new since 15:41:53 = %d' % len(rec))
    for r_ in rec[-15:]: out.append('  ' + r_)
k = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\fleet\mv0001-handover\outbound\krea2\30s-reel-v1'
if os.path.isdir(k):
    rec = []
    for root, dirs, files in os.walk(k):
        for f in files:
            p = os.path.join(root, f)
            m = os.path.getmtime(p)
            if m > datetime.datetime(2026,10,10,20,3,42).timestamp():
                rec.append('%s %s' % (datetime.datetime.fromtimestamp(m).strftime('%H:%M:%S'), os.path.relpath(p, k)))
    rec.sort()
    out.append('30s-reel new since 20:03:42 = %d' % len(rec))
    for r_ in rec[-15:]: out.append('  ' + r_)
open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1911_scan.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('OK rows=%d' % len(out))
