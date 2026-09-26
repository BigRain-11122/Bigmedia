# -*- coding: utf-8 -*-
# R445 smoke: real-render validation of the new series template + cyber
# sync layer syntax against this ffmpeg build (9.0.1 gyan) - plan-level
# tests cannot catch filter option spelling (tpad start_mode/drawgrid/
# adelay/borderw). Two renders: color-source path with every dial on +
# intro/audio shift, then bgvideo path with intro+badge+scanlines.
import json, os, subprocess, sys, tempfile

R = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
d = tempfile.mkdtemp(prefix='r445-smoke-')
FONT = 'C:/Windows/Fonts/msyh.ttc'

cfg = {
    'meta': {'topic': 'r445 smoke'},
    'video': {'width': 540, 'height': 960, 'fps': 30, 'bg': 'black'},
    'font': {'file': FONT, 'cards_size': 60, 'subs_size': 40,
             'aigc_size': 26, 'subs_bottom': 160, 'line_spacing': 12,
             'h1_font': FONT, 'h1_size': 72, 'h2_size': 36,
             'h1_color': 'accent', 'h2_color': 'gray60', 'h1_gap': 36},
    'aigc_notice': 'AI generated content',
    'tail': 0.3,
    'cards': [
        {'start': 0, 'end': 2, 'lines': ['hook line', 'sub line']},
        {'start': 2, 'end': 3.8, 'lines': ['second card']},
    ],
}
cards_p = os.path.join(d, 'smoke-cards.json')
with open(cards_p, 'w', encoding='utf-8') as f:
    json.dump(cfg, f, ensure_ascii=False, indent=1)

srt = '\n'.join([
    '1', '00:00:00,000 --> 00:00:02,000',
    '\u7cfb\u7edf\u65e5\u5fd7\u5f00\u673a', '',
    '2', '00:00:02,000 --> 00:00:03,800',
    '\u8ba4\u9886\u56de\u6267', '',
])
srt_p = os.path.join(d, 'subs.srt')
with open(srt_p, 'w', encoding='utf-8', newline='\n') as f:
    f.write(srt)

audio_p = os.path.join(d, 'audio.wav')
r = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                    '-f', 'lavfi', '-i', 'sine=frequency=440:duration=3.8',
                    '-ac', '1', audio_p], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[-500:]

argv = [sys.executable, os.path.join(R, 'src', 'render', 'render_card_video.py'),
        '--cards', cards_p, '--srt', srt_p, '--audio', audio_p,
        '--out', os.path.join(d, 'smoke1.mp4'),
        '--series-intro', '--series-id', 'BS-001 EP.01',
        '--series-badge', '--h1-glow', '--scanlines', '--sys-status']
r = subprocess.run(argv, capture_output=True, text=True, cwd=R)
print('--- smoke1 (color path, all dials + intro + adelay) exit=%d' % r.returncode)
print(r.stdout[-600:])
if r.returncode != 0:
    print(r.stderr[-600:])
    sys.exit(1)

bg = os.path.join(R, 'data', 'sources', 'footage', 'citywatch-vertical.mp4')
argv = [sys.executable, os.path.join(R, 'src', 'render', 'render_card_video.py'),
        '--cards', cards_p, '--srt', srt_p, '--audio', audio_p,
        '--out', os.path.join(d, 'smoke2.mp4'), '--bgvideo', bg,
        '--series-intro', '--series-id', 'BS-001 EP.01',
        '--series-badge', '--scanlines']
r = subprocess.run(argv, capture_output=True, text=True, cwd=R)
print('--- smoke2 (bgvideo path, intro+badge+scanlines) exit=%d' % r.returncode)
print(r.stdout[-600:])
if r.returncode != 0:
    print(r.stderr[-600:])
    sys.exit(1)

for name in ('smoke1.mp4', 'smoke2.mp4'):
    p = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'format=duration:stream=width,height',
                        '-of', 'default=noprint_wrappers=1',
                        os.path.join(d, name)], capture_output=True, text=True)
    print('--- %s probe: %s' % (name, ' '.join(p.stdout.split())))
print('SMOKE_DIR=' + d)
print('SMOKE OK')
