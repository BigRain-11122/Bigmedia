import io, re, glob, os, datetime, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .c3-tmp -> repo root
os.chdir(ROOT)
out = io.open(os.path.join('.c3-tmp', 'r659_probes.txt'), 'w', encoding='utf-8')

def w(*a):
    out.write(' '.join(str(x) for x in a) + '\n')

# 1) anchors top-card check (supply gate for #86/#63)
anchor_path = None
for f in sorted(glob.glob(r'.c3-tmp\r6*_all.py')):
    t = io.open(f, encoding='utf-8').read()
    m = re.search(r'r"[^"]*census[^"]*"', t) or re.search(r"C:[^\"']*census[^\"']*", t)
    if m:
        anchor_path = m.group(0)
        break
w('ANCHOR_PATH_FROM_PROBE:', anchor_path)

hits = glob.glob(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\data\census\cards\*')
if not hits:
    hits = glob.glob(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\**\C-000*', recursive=True)
names = sorted(os.path.basename(h) for h in hits if os.path.isfile(h) or os.path.isdir(h))
w('ANCHOR_FILES_COUNT', len(names), 'TOP', names[-3:] if names else 'NONE')
w('C00030_PRESENT', any('C-00030' in n for n in names))

# 2) three probes
for cmd in [
    ['python', 'src/board_check.py'],
    ['python', 'src/readiness.py'],
    ['python', 'src/os/loop_health.py'],
]:
    r = subprocess.run(cmd, capture_output=True)
    w('=== ', ' '.join(cmd), ' rc=', r.returncode)
    txt = (r.stdout or b'').decode('utf-8', 'replace')
    keep = [l for l in txt.splitlines() if re.search(r'FAIL|WARN|PASS|blocker|finding|OK|ready|结论|阻塞', l)]
    for l in keep[:25]:
        w('   ', l[:200])
out.close()
print('done -> .c3-tmp/r659_probes.txt')
