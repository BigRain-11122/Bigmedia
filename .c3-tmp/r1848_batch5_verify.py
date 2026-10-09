import json, re, os, subprocess

BIGLIFE = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife'
CAND = '精准计算，也计算不来的便是这人间烟火'
OUT = []
A = OUT.append
ok = True

cur = json.load(open(os.path.join(BIGLIFE, 'cognition', 'pools.json'), encoding='utf-8'))
pool = []
for axis, scenes in cur['axes'].items():
    for scene, ls in scenes.items():
        pool.extend(ls)
found = [(axis, scene) for axis, scenes in cur['axes'].items() for scene, ls in scenes.items() if CAND in ls]
A('V1 verbatim_in_pool=%s axis_scene=%s' % (bool(found), found))
ok &= bool(found)

spirit = open('data/storylines/codex/city-spirit.md', encoding='utf-8').read()
rows = re.findall(r'^\|\s*(\d+)\s*\|\s*(.+?)\s*\|', spirit, re.M)
adopted = set(re.sub(r'\*\*', '', t).strip() for _, t in rows)
dup_adopted = CAND in adopted or (CAND + '。') in adopted
A('V2 zero_dup_vs_spirit_1_100=%s' % (not dup_adopted))
ok &= not dup_adopted

tri_hits = []
for f in ('city-culture.md', 'city-humanities.md', 'city-residents.md'):
    c = open('data/storylines/codex/' + f, encoding='utf-8').read()
    if CAND in c or (CAND + '。') in c:
        tri_hits.append(f)
A('V3 zero_dup_vs_三志=%s hits=%s' % (not tri_hits, tri_hits))
ok &= not tri_hits

# V4 fleet card-level dedup: repo-wide rg (fixed string), excluding .c3-tmp/.git
GIT = r'C:\Program Files\Git\cmd\git.exe'
r = subprocess.run(['git', '-C', '.', 'grep', '-n', '-F', CAND, '--', 'data', 'output', 'docs'],
                   capture_output=True)
hits = r.stdout.decode('utf-8', 'replace').strip()
A('V4 fleet_card_dedup_repo_grep hits=%s rc=%d' % (hits if hits else 'NONE', r.returncode))
ok &= (r.returncode == 1)

# V5 supply premise evidence: pool unchanged vs HEAD
raw = subprocess.run([GIT, '-C', BIGLIFE, 'show', 'HEAD:cognition/pools.json'], capture_output=True).stdout
head = json.loads(raw.decode('utf-8'))
def total(d):
    return sum(len(v) for sc in d['axes'].values() for v in sc.values()) + sum(len(v) for v in d['sprite'].values())
A('V5 supply_premise cur_total=%d head_total=%d expanded=%s' % (total(cur), total(head), total(cur) > total(head)))

# V6 near-twin: motif words vs adopted (manual rule documented: 计算/人间烟火 motif absent from adopted)
motif_absent = not any(('计算' in a or '人间烟火' in a) for a in adopted)
A('V6 near_twin_motif_check (计算/人间烟火 absent in #1-100)=%s' % motif_absent)
ok &= motif_absent

A('VERIFY_RESULT=%s' % ('PASS' if ok else 'FAIL'))
open('.c3-tmp/r1848_verify_out.txt', 'w', encoding='utf-8').write('\n'.join(OUT))
print('VERIFY %s' % ('PASS' if ok else 'FAIL'))
