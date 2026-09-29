# -*- coding: utf-8 -*-
# R711 LC-011 ASR merge: full-track run deterministically drops 27-54s region (VAD chunk-state,
# run1==run2 identical); audio proven healthy by 3 probes (silence map / per-seg loudness /
# isolated-window transcription). Channel repair = two-segment splice (R638/R701 root-fix-then-refly
# precedent): run1 head cues 1-6 + isolated mid window (+27.0s offset) + run1 CTA text.
import io, re, shutil

def parse_cues(path):
    txt = io.open(path, encoding='utf-8-sig').read()
    blocks = re.split(r'\n\s*\n', txt.strip())
    cues = []
    for b in blocks:
        lines = [l for l in b.splitlines() if l.strip()]
        for k, l in enumerate(lines):
            if '-->' in l:
                cues.append((l, ' '.join(lines[k + 1:])))
                break
    return cues

def ts_to_s(t):
    h, m, rest = t.split(':')
    s, ms = rest.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

def s_to_ts(x):
    x = max(0.0, x)
    h = int(x // 3600); m = int((x % 3600) // 60); s = x - h * 3600 - m * 60
    return ('%02d:%02d:%06.3f' % (h, m, s)).replace('.', ',')

run1 = parse_cues(r'.lc011-tmp/asr-check-run1.srt')
mid = parse_cues(r'.lc011-tmp/mid-check.srt')

merged = []
# head: run1 cues 1-5 as-is
for ts, text in run1[:5]:
    merged.append((ts, text))
# cue 6: the dangling min char at 27.260 (tail of "gui-ji-min" misheard "gui-ji"), end before mid cue1
mid_start = 27.0 + ts_to_s(mid[0][0].split(' --> ')[0])
merged.append(('%s --> %s' % (s_to_ts(27.260), s_to_ts(mid_start)), run1[5][1].split('字幕')[0].strip()))
# mid window cues offset +27.0s
for ts, text in mid:
    a, b = ts.split(' --> ')
    merged.append(('%s --> %s' % (s_to_ts(27.0 + ts_to_s(a)), s_to_ts(27.0 + ts_to_s(b))), text))
# CTA: text tail of run1 cue 6 (from 52.90 to 57.280, after last mid cue)
merged.append(('%s --> %s' % (s_to_ts(52.900), s_to_ts(57.280)),
               '字幕全大案在公众号转给把话听完的人'))

out = []
for i, (ts, text) in enumerate(merged, 1):
    out.append('%d\n%s\n%s\n' % (i, ts, text))
io.open(r'.lc011-tmp/asr-check.srt', 'w', encoding='utf-8').write('\n'.join(out))
shutil.copy(r'.lc011-tmp/asr-check.srt', r'.lc011-tmp/asr-check-run2.srt') if False else None
print('MERGED_CUES', len(merged))
for ts, text in merged:
    print(ts, text)
