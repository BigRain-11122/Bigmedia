import io, re, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
OUT = os.path.join(ROOT, '.c3-tmp')
os.makedirs(OUT, exist_ok=True)

# 1) finished.md F-008 block
t = io.open(os.path.join(ROOT, 'output', 'finished.md'), encoding='utf-8').read()
i = t.find('F-008')
# capture until next F-0 marker or 2000 chars
j = t.find('F-009', i + 5)
seg = t[max(0, i - 50): j if j > 0 else i + 2000]
io.open(os.path.join(OUT, 'r637_f008.txt'), 'w', encoding='utf-8').write(seg)

# 2) audio README: find ch1 v3 production record + any render command lines
a = io.open(os.path.join(ROOT, 'data', 'storylines', 'audio', 'README.md'), encoding='utf-8').read()
# find command-like lines
lines = a.splitlines()
hits = [f'L{k+1}: {ln}' for k, ln in enumerate(lines) if ('python' in ln or 'emotive' in ln or 'ffmpeg' in ln or 'amix' in ln or '-pad' in ln)]
io.open(os.path.join(OUT, 'r637_audio_cmds.txt'), 'w', encoding='utf-8').write('\n'.join(hits[-80:]))
# also dump the ch1 v3 / v4 related rows
rows = [f'L{k+1}: {ln}' for k, ln in enumerate(lines) if ('ch.1' in ln or 'ch1' in ln or 'SC-001-01' in ln)]
io.open(os.path.join(OUT, 'r637_audio_ch1.txt'), 'w', encoding='utf-8').write('\n'.join(rows[-60:]))

# 3) list tmp dir of sc001-01-v3-tmp to see pipeline artifacts
d = os.path.join(ROOT, 'data', 'storylines', 'audio', 'sc001-01-v3-tmp')
names = sorted(os.listdir(d)) if os.path.isdir(d) else ['NO_DIR']
io.open(os.path.join(OUT, 'r637_v3tmp.txt'), 'w', encoding='utf-8').write('\n'.join(names))

# 4) check assets for ambient sound sources
for cand in [r'data\assets', r'data\assets\piper-models', r'data\storylines\audio']:
    p = os.path.join(ROOT, cand)
    if os.path.isdir(p):
        sub = [os.path.join(cand, n) for n in os.listdir(p)]
        io.open(os.path.join(OUT, 'r637_assets.txt'), 'a', encoding='utf-8').write(cand + ' :: ' + ' | '.join(sub[:40]) + '\n')

print('done')
