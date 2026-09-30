# -*- coding: utf-8 -*-
# R748 LC-019 ASR root-fix: R711-type two-segment splice channel.
# R746 QC run (vad=True) and R747 novad run (vad=False) both deterministically drop
# 26.94-47.54s (7 cues/1 dropped, identical shape) => VAD causal hypothesis falsified
# (R747), model-layer deterministic skip = R711-type same-family. Root fix per R638/R701
# precedent: transcribe isolated mid window, splice head/mid/tail into full coverage.
# Then diff vs edge-tts ground truth (punct-stripped char-position + trad norm, R685-R715
# caliber) and write summary JSON for the ledger writers.
import io, json, re, subprocess, sys, os

TMP = r'.lc019-tmp'
MID_MP3 = TMP + r'/mid-26-48.mp3'
MID_SRT = TMP + r'/mid-check.srt'
RUN1_SRT = TMP + r'/asr-check-run1.srt'
FINAL_SRT = TMP + r'/asr-check.srt'
DIFF_TXT = TMP + r'/asr-diff-r748.txt'
SUM_JSON = r'.c3-tmp/r748_asr.json'

WIN_START = 26.7   # gap starts at 26.940 (run1 cue5 end); 0.24s lead-in margin
WIN_END = 47.8     # run1 cue6 (tail) starts 47.540; window tail margin 0.26s
TAIL_START = 47.540

def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if r.returncode != 0:
        print('CMD_FAIL', cmd, r.stderr[-500:]); sys.exit(1)
    return r.stdout

# 1. preserve R746 QC-run evidence copy (novad copy already on disk)
io.open(RUN1_SRT, 'w', encoding='utf-8').write(io.open(TMP + r'/asr-check.srt', encoding='utf-8-sig').read())

# 2. extract isolated mid window
sh('ffmpeg -y -ss %s -to %s -i %s/audio.mp3 -c:a libmp3lame -q:a 4 %s' % (WIN_START, WIN_END, TMP, MID_MP3))

# 3. transcribe mid window (R169 QC recipe: medium int8 + beam5 + noctx)
os.environ['HF_HUB_OFFLINE'] = '1'
sys.argv = ['whisper_to_srt.py', '--audio', MID_MP3, '--out', MID_SRT,
            '--model', 'medium', '--beam-size', '5', '--no-context']
import runpy
try:
    runpy.run_path(r'src/render/whisper_to_srt.py', run_name='__main__')
except SystemExit as e:
    print('mid exit=', e.code)

# 4. parse helpers
def parse_cues(path):
    txt = io.open(path, encoding='utf-8-sig').read()
    cues = []
    for b in re.split(r'\n\s*\n', txt.strip()):
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

run1 = parse_cues(RUN1_SRT)
mid = parse_cues(MID_SRT)
assert len(run1) == 7, 'run1 cue count %d != 7' % len(run1)

merged = []
# head: run1 cues 1-5 (0 - 26.940s)
for ts, text in run1[:5]:
    merged.append((ts, text))
# mid: isolated window cues, +WIN_START offset, clipped before tail
for ts, text in mid:
    a, b = ts.split(' --> ')
    a2, b2 = WIN_START + ts_to_s(a), WIN_START + ts_to_s(b)
    if a2 >= TAIL_START - 0.1:
        continue
    if b2 > TAIL_START:
        b2 = TAIL_START
    merged.append(('%s --> %s' % (s_to_ts(a2), s_to_ts(b2)), text))
# tail: run1 cues 6-7 (47.540 - 56.920s)
for ts, text in run1[5:]:
    merged.append((ts, text))

out = []
for i, (ts, text) in enumerate(merged, 1):
    out.append('%d\n%s\n%s\n' % (i, ts, text))
io.open(FINAL_SRT, 'w', encoding='utf-8').write('\n'.join(out))
print('MERGED_CUES', len(merged))

# 5. diff vs ground truth (punct-stripped char-position + trad norm)
PUNCT = set(u'，。：、！？；·""\'\'（）《》【】, .:;!?()[]{}"\'\n\t-_~…—|/\\')
def srt_chars(path):
    res = []
    for ln in io.open(path, encoding='utf-8-sig').read().splitlines():
        s = ln.strip()
        if not s or '-->' in s or s.isdigit():
            continue
        res.extend(ch for ch in s if ch not in PUNCT)
    return ''.join(res)

TRAD = {u'統':u'统',u'擁':u'拥',u'貓':u'猫',u'場':u'场',u'羅':u'罗',u'壯':u'壮',u'門':u'门',u'訊':u'讯',u'斷':u'断',u'類':u'类',u'鋪':u'铺',u'葉':u'叶',u'畫':u'画',u'燙':u'烫',u'鵰':u'雕',u'邊':u'边',u'條':u'条',u'電':u'电',u'話':u'话',u'遷':u'迁',u'數':u'数',u'寵':u'宠',u'師':u'师',u'車':u'车',u'長':u'长',u'時':u'时',u'間':u'间',u'歲':u'岁',u'藝':u'艺',u'術':u'术',u'開':u'开',u'關':u'关',u'點':u'点',u'為':u'为',u'與':u'与',u'從':u'从',u'這':u'这',u'個':u'个',u'們':u'们',u'來':u'来',u'對':u'对',u'麼':u'么',u'見':u'见',u'觀':u'观',u'讓':u'让',u'還':u'还',u'進':u'进',u'過':u'过',u'發':u'发',u'給':u'给',u'聽':u'听',u'說':u'说',u'錢':u'钱',u'雲':u'云',u'廠':u'厂',u'學':u'学',u'轉':u'转',u'幹':u'干'}
def norm(s):
    return ''.join(TRAD.get(ch, ch) for ch in s)

import difflib
a = norm(srt_chars(TMP + r'/subs.srt'))
b = norm(srt_chars(FINAL_SRT))
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
sites = 0; diff_chars = 0; detail = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    sites += 1
    diff_chars += (i2 - i1) + (j2 - j1)
    detail.append(u'%s ref[%d:%d]=%r asr[%d:%d]=%r' % (tag, i1, i2, a[i1:i2], j1, j2, b[j1:j2]))
ratio = diff_chars / float(len(a)) * 100
report = (u'caliber=punctuation-stripped char-position (R685-R715 precedent) + trad_norm_set=%d chars\n'
          u'mode=R711-type two-segment splice full coverage (QC vad=True run + novad vad=False run both 7cues/1dropped '
          u'stable 26.94-47.54s skip = VAD causal falsified R747, model-layer deterministic skip; head5+mid-window+tail2)\n'
          u'ref_chars=%d asr_chars=%d merged_cues=%d\n'
          u'sites=%d diff_chars=%d ratio=%.1f%%\n\n') % (len(TRAD), len(a), len(b), len(merged), sites, diff_chars, ratio)
report += u'\n'.join(detail)
io.open(DIFF_TXT, 'w', encoding='utf-8').write(report)

# 6. keyword survival check (fact words + names + creed + CTA positioning)
KEYS = [u'周浩宇', u'二十八', u'扭塔', u'策略研究员', u'泡面', u'敬畏', u'工位', u'川渝', u'尾音',
        u'钻到底', u'章硬', u'报平安', u'天理', u'验一万遍', u'徐根福', u'多打一勺', u'长身体',
        u'陈雅雯', u'最怕', u'信条', u'回撤', u'行情', u'谦虚', u'公众号', u'敬畏市场', u'讣告', u'研究']
survive = {k: (k in b) for k in KEYS}

summary = {'merged_cues': len(merged), 'ref_chars': len(a), 'asr_chars': len(b),
           'sites': sites, 'diff_chars': diff_chars, 'pct': u'%.1f%%' % ratio,
           'survive': survive,
           'asr_full': u''.join(b.split()),
           'detail': detail}
io.open(SUM_JSON, 'w', encoding='utf-8').write(json.dumps(summary, ensure_ascii=False, indent=1))
print('SITES', sites, 'DIFFCHARS', diff_chars, 'REF', len(a), 'RATIO %.1f' % ratio)
print('SURVIVE_MISS', [k for k, v in survive.items() if not v])
print('SPLICE_OK')
