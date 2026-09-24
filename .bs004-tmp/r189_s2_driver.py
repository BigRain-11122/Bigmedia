# R189 S2 three-gate re-run driver for v14 batch (4 pieces x ai_feel/layer1.8/spec)
# Writes UTF-8 results to .bs004-tmp/s2-results.md (PS5.1 console GBK bypass)
import io
import os
import subprocess
import sys

os.chdir(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream')
PIECES = [
    ('bs-001-v14-shipinhao-60s.mp4', r'data\sources\bs001\voiceover-v11-trim.beats.txt', r'output\renders\.v11-trim\subs.srt'),
    ('bs-002-v2-shipinhao-60s.mp4', r'data\sources\bs002\voiceover-v5.beats.txt', r'.bs002-tmp\subs.srt'),
    ('bs-003-v2-shipinhao-60s.mp4', r'data\sources\bs003\voiceover-v5.beats.txt', r'.bs003-tmp\subs.srt'),
    ('bs-004-v2-shipinhao-60s.mp4', r'data\sources\bs004\voiceover-v6.beats.txt', r'.bs004-tmp\subs.srt'),
]
out = io.open(r'.bs004-tmp\s2-results.md', 'w', encoding='utf-8')
for mp4, beats, srt in PIECES:
    video = r'output\renders' + '\\' + mp4
    plan = video + '.plan.json'
    checks = [
        ('ai_feel', [sys.executable, 'src\\ai_feel_check.py', '--beats', beats, '--srt', srt]),
        ('edit_craft_l18', [sys.executable, 'src\\edit_craft_check.py', '--plan', plan, '--srt', srt, '--profile', 'shipinhao']),
        ('platform_spec', [sys.executable, 'src\\platform_spec_check.py', '--video', video, '--platform', '微信视频号']),
    ]
    for name, cmd in checks:
        r = subprocess.run(cmd, capture_output=True)
        out.write('## %s | %s | rc=%d\n' % (mp4, name, r.returncode))
        out.write(r.stdout.decode('utf-8', 'replace'))
        if r.stderr.strip():
            out.write('[STDERR] ' + r.stderr.decode('utf-8', 'replace')[-400:] + '\n')
        out.write('\n')
out.close()
print('driver done')
