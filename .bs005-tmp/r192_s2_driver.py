# R192 S2 three-gate enforcement driver for BS-005 v1 (ai_feel/layer1.8/spec)
# Writes UTF-8 results to .bs005-tmp/s2-results.md (PS5.1 console GBK bypass)
import io
import os
import subprocess
import sys

os.chdir(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream')
video = r'output\renders\bs-005-v1-shipinhao-60s.mp4'
plan = video + '.plan.json'
beats = r'data\sources\bs005\voiceover-v3.beats.txt'
srt = r'.bs005-tmp\subs.srt'
out = io.open(r'.bs005-tmp\s2-results.md', 'w', encoding='utf-8')
checks = [
    ('ai_feel', [sys.executable, 'src\\ai_feel_check.py', '--beats', beats, '--srt', srt]),
    ('edit_craft_l18', [sys.executable, 'src\\edit_craft_check.py', '--plan', plan, '--srt', srt, '--profile', 'shipinhao']),
    ('platform_spec', [sys.executable, 'src\\platform_spec_check.py', '--video', video, '--platform', '微信视频号']),
]
for name, cmd in checks:
    r = subprocess.run(cmd, capture_output=True)
    out.write('## bs-005-v1 | %s | rc=%d\n' % (name, r.returncode))
    out.write(r.stdout.decode('utf-8', 'replace'))
    if r.stderr.strip():
        out.write('[STDERR] ' + r.stderr.decode('utf-8', 'replace')[-400:] + '\n')
    out.write('\n')
out.close()
print('driver done')
