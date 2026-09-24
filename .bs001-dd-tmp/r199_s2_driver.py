# R199 S2 three-gate enforcement driver for BS-001-DD v1 (bilibili 16:9
# deep-dive). Same channel as .bs004-tmp/r197_driver.py: subprocess python
# calls, UTF-8 results to .bs001-dd-tmp/s2-results-r199.md (PS5.1 GBK
# console bypass). ASCII source (encoding law).
import io
import subprocess
import sys

REPO = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
import os
os.chdir(REPO)

video = r'output\renders\bs-001-dd-v1-bilibili-16x9.mp4'
plan = video + '.plan.json'
beats = r'data\sources\bs001-dd\voiceover-dd-v1.beats.txt'
srt = r'.bs001-dd-tmp\subs.srt'
out = io.open(r'.bs001-dd-tmp\s2-results-r199.md', 'w', encoding='utf-8')
checks = [
    ('ai_feel', [sys.executable, 'src\\ai_feel_check.py', '--beats', beats, '--srt', srt]),
    ('edit_craft_l18', [sys.executable, 'src\\edit_craft_check.py', '--plan', plan, '--srt', srt, '--profile', 'bilibili']),
    ('platform_spec', [sys.executable, 'src\\platform_spec_check.py', '--video', video, '--platform', 'B\u7ad9']),
]
for name, cmd in checks:
    r = subprocess.run(cmd, capture_output=True)
    out.write('## BS-001-DD v1 | %s | rc=%d\n' % (name, r.returncode))
    out.write(r.stdout.decode('utf-8', 'replace'))
    if r.stderr.strip():
        out.write('[STDERR] ' + r.stderr.decode('utf-8', 'replace')[-600:] + '\n')
    out.write('\n')
d = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                    '-show_entries', 'stream=width,height',
                    '-show_entries', 'format=duration', '-of', 'csv=p=0',
                    video], capture_output=True)
out.write('## BS-001-DD v1 | ffprobe: %s\n' % d.stdout.decode('utf-8', 'replace').strip().replace('\n', ' | '))
out.close()
print('s2 driver done')
