import subprocess, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
REPO = Path('.').resolve()
TMP = REPO / '.c3-tmp/asm-r1794'
edited = TMP / 'edited_bg.mp4'
audio = TMP / 'audio-asm.m4a'
FONT = 'C:/Windows/Fonts/msyh.ttc'


def dtext(textfile, size, color, x, y, enable=None, shadow=True):
    f = ("drawtext=expansion=none:fontfile='%s':textfile='%s':"
         "fontsize=%d:fontcolor=%s" % (FONT, textfile, size, color))
    if shadow:
        f += ":shadowcolor=black@0.75:shadowx=2:shadowy=2"
    f += ":x=%s:y=%s" % (x, y)
    if enable:
        f += ":enable='%s'" % enable
    return f


# minimal repro: single subtitle drawtext + aigc
c01 = dtext('.c3-tmp/asm-r1794/c00.txt', 36, 'white', '(w-text_w)/2', 'h-140',
            'between(t,0.200,3.000)')
aigc = dtext('.c3-tmp/asm-r1794/aigc.txt', 22, 'white@0.9', 'w-tw-24', 'h-36', None, shadow=False)
fc = '[0:v]' + c01 + ',' + aigc + '[v]'
out = TMP / 'debug-min.mp4'
cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
       '-i', str(edited), '-i', str(audio),
       '-filter_complex', fc, '-map', '[v]', '-map', '1:a',
       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
       '-pix_fmt', 'yuv420p', '-t', '3', str(out)]
r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
print('RC', r.returncode)
print('STDERR-HEAD:', r.stderr[:2000])
