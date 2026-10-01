# -*- coding: utf-8 -*-
# R870 five-check scan (content-addressed, r807 lineage)
import io, os, re, json, datetime

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup'
out = []
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
out.append('r870 five-check scan (content-addressed %s):' % now)

# 1) orders anchor
od = os.path.join(ROOT, 'media', 'BigStream', 'orders')
ofiles = sorted([f for f in os.listdir(od) if f.startswith('O-') and f.endswith('.md')])
out.append('orders=%d O-*.md +README=%d anchor, top=%s' % (len(ofiles), len(ofiles) + 1, ofiles[-1]))

# 2) ledger six-mode scan (task-modes + machine-modes, R845 re-baseline)
led = io.open(os.path.join(ROOT, 'cph4', 'evolution-ledger.md'), encoding='utf-8').read()
led_lines = led.split('\n')
task_modes = re.compile(r'@BigStream|@七线全司|@全司|@六司|@八线全量')
mach_modes = re.compile(r'@bm-a|@bm-b')
tm = [l for l in led_lines if task_modes.search(l)]
mm = [l for l in led_lines if mach_modes.search(l)]
p_rows = re.findall(r'P-2026-\d{2}-\d{2}-\d+', led)
out.append('ledger_scan_hits=%d (task-modes=%d + machine-modes=%d; R845 re-baseline band=46) last_p=%s p20260930_rows=%d p20261001_max=%d' % (
    len(tm) + len(mm), len(tm), len(mm), max(p_rows) if p_rows else 'NONE',
    len(set(re.findall(r'P-20260930-\d+', led))), len(set(re.findall(r'P-20261001-\d+', led)))))
dash_row = any('@bm-a' in l and 'P-2026-10-01-01' in l.replace(' ', '') or 'P-2026-10-01-01' in l and '@bm-a' in l for l in mm)
out.append('r845_regression: P-2026-10-01-01 @bm-a dash row caught=%s' % dash_row)

# 3) decisions dnum content-addressed diff (D-20260930-19 watermark set-diff)
dec = io.open(os.path.join(ROOT, 'docs', 'decisions.md'), encoding='utf-8').read()
dnums = sorted(set(re.findall(r'[DC]-\d{8}-\d{2}', dec)))
st = json.load(io.open('src/os/state.json', encoding='utf-8'))
wm = set(st['decisions_watermark']['dnums'])
new = [d for d in dnums if d not in wm]
out.append('decisions_dnum_total=%d baseline=%d new_rows=%s (D-20260930-19 watermark diff, D-13 SLA check)' % (
    len(dnums), len(wm), ','.join(new) if new else 'NONE'))
board = re.findall(r'^\|.*@?BigStream.*\|', dec, re.M)
out.append('dispatch_board_rows=%d bigstream_rows=%s' % (st['decisions_watermark'].get('board_rows', -1), len(board)))

# 4) production + tick + lock
out.append('production=%s tick=%d (pre-close read) / index.lock=%s' % (
    st['production'], st['tick'], os.path.exists('.git/index.lock')))

# 5) tree yield-state mtimes
for p, tag in [('data/storylines/codex/README.md', 'codex README'),
               ('data/storylines/codex/city-humanities.md', 'codex city-humanities'),
               ('CODELY.md', 'CODELY.md')]:
    out.append('%s mtime=%s' % (tag, datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%Y-%m-%d %H:%M:%S')))

# 6) GB gate head date
gb = io.open('docs/global-benchmarks.md', encoding='utf-8').read().split('\n')
gb_head = next((l for l in gb if re.match(r'^\d{4}-\d{2}-\d{2}', l)), 'NONE')
out.append('gb_head_date_probe=%s (7-day gate due 10-08 per R798)' % gb_head[:10])

# 7) daily brief today
out.append('daily brief: 2026-10-01.md %s' % ('PRESENT' if os.path.exists('data/intel/daily/2026-10-01.md') else 'ABSENT'))

# 8) census anchor top (supply gate)
try:
    anc_dir = os.path.join(ROOT, 'life', 'BigLife', 'census', 'anchors')
    anchors = sorted(f for f in os.listdir(anc_dir)) if os.path.isdir(anc_dir) else []
    top = anchors[-1] if anchors else 'NONE'
    out.append('census_anchors_top=%s (C-00030 present: %s) -> CENSUS-v21 supply gate %s' % (
        top, 'C-00030' in ' '.join(anchors), 'OPEN' if any('C-00030' in a for a in anchors) else 'CLOSED'))
except Exception as e:
    out.append('census_anchors probe error: %s' % e)

# 9) HQ-FEEDBACK recent mentions
hq = io.open('HQ-FEEDBACK.md', encoding='utf-8').read().split('\n')
mentions = [l[:120] for l in hq[-40:] if 'BigStream' in l or 'D-20261001' in l]
out.append('HQ-FEEDBACK recent bigstream/D-20261001 lines: %s' % (mentions[-3:] if mentions else 'none'))

io.open('.c3-tmp/r870_scan.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('SCAN-OK new_rows=%s hits=%d' % (','.join(new) if new else 'NONE', len(tm) + len(mm)))
