# -*- coding: utf-8 -*-
# R447: build cards-v15-matched.json for the F-001 two-law remake
# inherit: v12-matched lines+visuals (card anchors = v11 originals, R446
# rollback), timings from the v15 TTS baseline (v15 audio clock).
import json, io

base = json.load(io.open('.bs001-v15-tmp/cards.json', encoding='utf-8'))
v12 = json.load(io.open('data/sources/bs001/cards-v12-matched.json',
                        encoding='utf-8'))
assert len(base['cards']) == len(v12['cards']) == 12

# line diffs expected only where the TTS baseline kept draft glosses
# (b3/b4/b7); the matched file must carry the v11 anchor lines
for i, (a, b) in enumerate(zip(base['cards'], v12['cards'])):
    if a['lines'] != b['lines']:
        print('line_diff card %d: baseline=%s v12_anchor=%s'
              % (i, ' / '.join(a['lines']), ' / '.join(b['lines'])))

out = json.loads(json.dumps(v12))          # deep copy: lines + visuals
for i, c in enumerate(out['cards']):
    c['start'] = base['cards'][i]['start']  # v15 audio clock
    c['end'] = base['cards'][i]['end']

out['meta']['variant'] = ('v15 window-compliant matched cut (9:16 shipinhao '
                          '30-60s) - #71 two-law remake (L18/L19/L20 '
                          'plain-language + S5.5 series badge + S4.5 dials)')
out['meta']['beats'] = 'data\\sources\\bs001\\voiceover-v15.beats.txt'
out['meta']['order'] = ('P-20260926-11 #71 remake leg-3 F-001: two-law '
                        'remake of the v14b shipinhao piece')

with io.open('data/sources/bs001/cards-v15-matched.json', 'w',
             encoding='utf-8') as f:
    f.write(json.dumps(out, indent=2, ensure_ascii=False))
print('written cards-v15-matched.json cards=%d last_end=%.2f'
      % (len(out['cards']), out['cards'][-1]['end']))
