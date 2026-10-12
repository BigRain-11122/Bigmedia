# -*- coding: utf-8 -*-
# R2094 deathline-window readings (O-20261012-2305 film deadline 08:30, MV sprint session owns assembly)
import os
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
HANDOVER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\fleet\mv0001-handover"
REL = os.path.join(ROOT, 'data', 'storylines', 'drama', 'mv0001', 'release')
CV = os.path.join(HANDOVER, 'outbound', 'krea2', 'kf-demo-20261012', 'cloudv2')
BMC = os.path.join(HANDOVER, 'outbound', 'krea2', 'kf-demo-20261012', 'bmc')

now = datetime.now()
print('readings-time %s' % now.strftime('%Y-%m-%d %H:%M:%S'))

# 1. local release/ scan (234s full film detection)
if os.path.isdir(REL):
    files = sorted(
        ((f, os.path.getmtime(os.path.join(REL, f)), os.path.getsize(os.path.join(REL, f)))
         for f in os.listdir(REL) if os.path.isfile(os.path.join(REL, f))),
        key=lambda x: -x[1])
    print('local-release count=%d' % len(files))
    for f, m, s in files[:4]:
        print('  %-42s %10d  %s' % (f, s, datetime.fromtimestamp(m).strftime('%m-%d %H:%M:%S')))
    full234 = any('234' in f or 'full' in f.lower() for f, _, _ in files)
    print('full234=%s' % full234)
else:
    print('local-release ABSENT')

# 2. handover release/ (canon delivery face)
hr = os.path.join(HANDOVER, 'release')
if os.path.isdir(hr):
    fs = os.listdir(hr)
    print('handover-release count=%d %s' % (len(fs), fs[:3]))
else:
    print('handover-release ABSENT')

# 3. cloudv2 CLOUDWAVE-2 wave freshness
if os.path.isdir(CV):
    fs = sorted(
        ((f, os.path.getmtime(os.path.join(CV, f))) for f in os.listdir(CV)
         if os.path.isfile(os.path.join(CV, f))),
        key=lambda x: -x[1])
    newest_age = (now - datetime.fromtimestamp(fs[0][1])).total_seconds() / 60.0
    print('cloudv2 count=%d newest=%s age_min=%.1f' % (len(fs), fs[0][0], newest_age))
    for f, m in fs[:3]:
        print('  %-28s %s' % (f, datetime.fromtimestamp(m).strftime('%m-%d %H:%M:%S')))
else:
    print('cloudv2 ABSENT')

# 4. bmc/i2v lane presence in handover tree (bm-c delivery face)
if os.path.isdir(BMC):
    print('bmc/i2v count=%d (bm-c lane landed)' % len(os.listdir(BMC)))
else:
    print('bmc/i2v ABSENT (bm-c lane via orders/CDN, not yet landed)')

# 5. local tree untracked MV batch (zero-contact note)
mvdir = os.path.join(ROOT, 'data', 'storylines', 'drama', 'mv0001')
print('mv0001-tree note: MV sprint session in-flight files, zero-contact per R1745')
