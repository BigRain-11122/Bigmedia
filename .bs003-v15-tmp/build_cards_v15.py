# -*- coding: utf-8 -*-
# R452: build cards-v15-matched.json for the F-003 two-law remake
# inherit: v1-matched lines+visuals (card anchors = v5 originals, R451
# card-column zero-move), timings from the v15 TTS baseline (v15 audio clock).
import json, io

base = json.load(io.open('.bs003-v15-tmp/cards.json', encoding='utf-8'))
v1 = json.load(io.open('data/sources/bs003/cards-v1-matched.json',
                       encoding='utf-8'))
assert len(base['cards']) == len(v1['cards']) == 12

# line diffs expected zero: v15 beats kept the card anchor column at v5
# originals (R451), the v1-matched file carries those same anchor lines
diffs = 0
for i, (a, b) in enumerate(zip(base['cards'], v1['cards'])):
    if a['lines'] != b['lines']:
        diffs += 1
        print('line_diff card %d: baseline=%s v1_anchor=%s'
              % (i, ' / '.join(a['lines']), ' / '.join(b['lines'])))

out = json.loads(json.dumps(v1))          # deep copy: lines + visuals
for i, c in enumerate(out['cards']):
    c['start'] = base['cards'][i]['start']  # v15 audio clock
    c['end'] = base['cards'][i]['end']

out['meta']['variant'] = ('v15 window-compliant matched cut (9:16 shipinhao '
                          '30-60s) - #71 two-law remake (L18/L19/L20 '
                          'plain-language + S5.5 series badge + S4.5 dials)')
out['meta']['beats'] = 'data\\sources\\bs003\\voiceover-v15.beats.txt'
out['meta']['order'] = ('P-20260926-11 #71 remake leg-3 F-003: two-law '
                        'remake of the v2b shipinhao piece')

with io.open('data/sources/bs003/cards-v15-matched.json', 'w',
             encoding='utf-8') as f:
    f.write(json.dumps(out, indent=2, ensure_ascii=False))
print('written cards-v15-matched.json cards=%d line_diffs=%d last_end=%.2f'
      % (len(out['cards']), diffs, out['cards'][-1]['end']))
