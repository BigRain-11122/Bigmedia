import json, re, subprocess, os

GIT = r'C:\Program Files\Git\cmd\git.exe'
BIGLIFE = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife'
OUT = []
A = OUT.append

# current (working tree, 10-09 expansion, read-only)
cur = json.load(open(os.path.join(BIGLIFE, 'cognition', 'pools.json'), encoding='utf-8'))
# HEAD version (last committed 09-27) via git show, bytes captured
raw = subprocess.run([GIT, '-C', BIGLIFE, 'show', 'HEAD:cognition/pools.json'],
                     capture_output=True).stdout
head = json.loads(raw.decode('utf-8'))


def flat(d):
    lines = []
    for axis, scenes in d['axes'].items():
        for scene, ls in scenes.items():
            for ln in ls:
                lines.append((axis, scene, ln))
    for scene, ls in d['sprite'].items():
        for ln in ls:
            lines.append(('像素灵', scene, ln))
    return lines


cur_l = flat(cur)
head_l = flat(head)
A('TOTAL cur=%d head=%d' % (len(cur_l), len(head_l)))

head_set = set(l[2] for l in head_l)
new_l = [t for t in cur_l if t[2] not in head_set]
A('NEW_LINES=%d' % len(new_l))
seen = set()
dedup_new = []
for t in new_l:
    if t[2] not in seen:
        seen.add(t[2])
        dedup_new.append(t)
A('NEW_DEDUP=%d' % len(dedup_new))

# adopted set from city-spirit.md rows #27-100
spirit = open('data/storylines/codex/city-spirit.md', encoding='utf-8').read()
rows = re.findall(r'^\|\s*(\d+)\s*\|\s*(.+?)\s*\|', spirit, re.M)
adopted = {}
for num, text in rows:
    txt = re.sub(r'\*\*', '', text).strip()
    adopted[txt] = int(num)
A('ADOPTED_ROWS=%d (spirit table rows parsed)' % len(adopted))
adopt_in_pool = [t for t in cur_l if t[2] in adopted]
A('ADOPTED_FOUND_IN_POOL=%d (of %d pool-sourced #27-100)' % (len(adopt_in_pool), len([n for n, t in adopted.items() if '台词池' in spirit])))

# 三志 in-register content (containment check)
tri = {}
for f in ('city-culture.md', 'city-humanities.md', 'city-residents.md'):
    tri[f] = open('data/storylines/codex/' + f, encoding='utf-8').read()

net = [t for t in cur_l if t[2] not in adopted and not any(t[2] in c for c in tri.values())]
A('NET_CANDIDATES=%d (cur minus adopted minus 三志在册)' % len(net))
net_new = [t for t in net if t[2] in seen]
A('NET_NEW=%d' % len(net_new))

# dump new lines for selection
A('')
A('===== NEW LINES (axis|scene|line) =====')
for axis, scene, ln in dedup_new:
    flags = []
    if ln in adopted:
        flags.append('ADOPTED#%d' % adopted[ln])
    if any(ln in c for c in tri.values()):
        flags.append('IN-三志')
    A('%s|%s|%s|%s' % (axis, scene, ln, ','.join(flags)))

# old remainder aphorism re-scan surface: net lines from OLD pool (not new), unique
A('')
A('===== OLD REMAINDER (count only; unique) =====')
old_net = {}
for axis, scene, ln in net:
    if ln not in seen:
        old_net.setdefault(ln, (axis, scene))
A('OLD_REMAINDER_UNIQUE=%d' % len(old_net))

open('.c3-tmp/r1848_batch5_newlines.txt', 'w', encoding='utf-8').write('\n'.join(OUT))
print('EXTRACT_OK new=%d net=%d' % (len(dedup_new), len(net)))
