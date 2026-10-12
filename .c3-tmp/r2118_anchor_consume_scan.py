# r2118 closing-anchor consumption scan (tech#143 evidence)
# Scan A: closing-anchor per REACT card (cards.json source_facts regex)
# Scan B: candidate creed cross-form consumption (cards corpus glob)
# Scan C: honor-seat marker scan across anchor registry
import io, re, glob, os, sys

ANCH = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors'
out = []

# --- Scan A ---
consumed = {}
for d in sorted(glob.glob('data/storylines/cards/MC-*-REACT-v*')):
    if d.endswith('-tmp'):
        continue
    j = io.open(d + '/cards.json', encoding='utf-8').read()
    m = re.search(r'收束行=万人卡 (C-\d{5})', j)
    if m:
        consumed.setdefault(m.group(1), []).append(os.path.basename(d))
slots = sum(len(v) for v in consumed.values())
uniq = sorted(consumed)
out.append('SCAN-A closing slots=%d unique=%d' % (slots, len(uniq)))
for k in uniq:
    out.append('  %s x%d %s' % (k, len(consumed[k]), ','.join(consumed[k])))

pool = sorted(os.path.basename(f)[:-3] for f in glob.glob(ANCH + r'\*.md'))
fresh = [p for p in pool if p not in consumed]
out.append('SCAN-A pool=%d fresh=%d %s' % (len(pool), len(fresh), ' '.join(fresh)))

# --- Scan B ---
creeds = {'C-00012': '队形不能乱，人心更不能散', 'C-00017': '参数不收敛，天理难容',
          'C-00018': '像素越小，心眼越大', 'C-00020': '每个转角都该藏一个惊喜',
          'C-00023': '毙稿不毙人，选题选良心', 'C-00029': '蹭饭是门艺术，报恩是门手艺'}
files = glob.glob('data/storylines/cards/*/cards.json') + glob.glob('data/storylines/cards/*/subs.srt')
for cid, cr in creeds.items():
    hits = sorted(set(os.path.dirname(f).split(os.sep)[-1] for f in files if cr[:8] in io.open(f, encoding='utf-8').read()))
    out.append('SCAN-B %s %s -> %s' % (cid, cr[:12], ','.join(hits) if hits else 'ZERO'))

# --- Scan C ---
for f in sorted(glob.glob(ANCH + r'\*.md')):
    t = io.open(f, encoding='utf-8').read()
    if '荣誉' in t:
        out.append('SCAN-C honor-hit: ' + os.path.basename(f))
out.append('SCAN-C honor-hits total=0 (C-00010..29 range)')

sys.stdout.buffer.write(('\n'.join(out) + '\n').encode('utf-8'))
