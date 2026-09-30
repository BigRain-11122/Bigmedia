# -*- coding: utf-8 -*-
# R741 probe: dump LC-018 cards.json card9 (annotation check) + anchor C-00015 fields + F-025 PNG size
import json, io, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
OUT = os.path.join(ROOT, '.c3-tmp', 'r741_probe.txt')
buf = []

j = json.load(io.open(os.path.join(ROOT, '.lc018-tmp', 'cards.json'), encoding='utf-8'))
cards = j['cards']
buf.append('n_cards=%d cards_size=%d width=%d' % (len(cards), j['font']['cards_size'], j['video']['width']))
for i, c in enumerate(cards):
    buf.append('--- card %d (size=%s, start=%.2f end=%.2f dur=%.2f) ---' % (
        i, c.get('size', 'default'), c['start'], c['end'], c['end'] - c['start']))
    for k, ln in enumerate(c['lines']):
        buf.append('  line[%d] (%d chars): %s' % (k, len(ln), ln))
durs = [(i, round(c['end'] - c['start'], 2)) for i, c in enumerate(cards)]
buf.append('beat_durations=%s' % durs)
buf.append('max_dur=%s' % max(d for _, d in durs))

# anchor C-00015 cross-repo read-only
ANC = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00015.md'
buf.append('anchor_exists=%s' % os.path.exists(ANC))
if os.path.exists(ANC):
    buf.append('===== ANCHOR C-00015 =====')
    buf.append(io.open(ANC, encoding='utf-8').read())

# F-025 PNG
PNG = os.path.join(ROOT, 'data', 'storylines', 'cards', 'MC-20260925-CENSUS-v6', 'MC-20260925-CENSUS-v6.png')
buf.append('PNG exists=%s size=%d' % (os.path.exists(PNG), os.path.getsize(PNG) if os.path.exists(PNG) else -1))

# beats v3 col2 lengths (anchor card lines) for audit prep
beats = io.open(os.path.join(ROOT, 'data', 'sources', 'lc018', 'voiceover-v3.beats.txt'), encoding='utf-8').read().strip().split('\n')
buf.append('n_beats_lines=%d' % len(beats))

# audio duration check
import subprocess
pr = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                     '-of', 'default=nw=1', os.path.join(ROOT, '.lc018-tmp', 'audio.mp3')], capture_output=True)
buf.append('audio_dur=' + pr.stdout.decode('utf-8', 'replace').strip())

io.open(OUT, 'w', encoding='utf-8').write('\n'.join(buf))
print('PROBE_DONE ->', OUT)
