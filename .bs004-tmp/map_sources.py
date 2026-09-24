import json, glob, io, sys

pats = glob.glob('data/sources/bs00*/cards*v*matched*.json') + glob.glob('.bs00*-tmp/cards*.json')
for f in pats:
    data = json.load(io.open(f, encoding='utf-8'))
    print(f)
    for i, c in enumerate(data['cards']):
        v = c.get('visual') or {}
        src = v.get('source') or ('CARDS-ONLY:' + v.get('reason', '')[:40])
        print('  beat%d: %.2f-%.2f (%.2fs) %s' % (i, c.get('start', 0), c.get('end', 0), c.get('end', 0) - c.get('start', 0), src))
