# -*- coding: utf-8 -*-
# R1960 explore#23 material extraction (read-only): finished.md consumption map + anchor fields
import io, sys, re, os, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
OUT = []

# --- 1. finished.md: split into F-blocks, map CENSUS-vN + C-ids ---
t = open('output/finished.md', encoding='utf-8').read()
blocks = re.split(r'(?m)^(?=## F-\d+)', t)
fmap = {}
for b in blocks:
    m = re.match(r'## (F-\d+)', b)
    if not m:
        continue
    fid = m.group(1)
    ids = sorted(set(re.findall(r'C-000\d\d', b)))
    cvs = sorted(set(re.findall(r'CENSUS-v(\d+)', b)))
    if ids or cvs:
        fmap[fid] = (cvs, ids)
OUT.append('=== finished.md consumption map (F-blocks with C-ids / CENSUS-vN) ===')
for fid in sorted(fmap, key=lambda x: int(x[2:])):
    cvs, ids = fmap[fid]
    OUT.append(f'{fid}: CENSUS-v{cvs} anchors={ids}')

# --- 2. anchor files: compact fields for the 13 audio-vacant candidates + 3 typhoon consumed ---
BASE = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors'
targets = [f'C-{n:05d}' for n in list(range(12, 16)) + list(range(18, 27))]
OUT.append('')
OUT.append('=== anchor compact fields (candidates C-00012~15, C-00018~26) ===')
for cid in targets:
    p = os.path.join(BASE, cid + '.md')
    if not os.path.exists(p):
        OUT.append(cid + ' MISSING'); continue
    s = open(p, encoding='utf-8').read()
    def grab(pat):
        m = re.search(pat, s)
        return m.group(1).strip() if m else ''
    name = re.match(r'# ' + cid + r' · (.+)', s).group(1).strip() if re.match(r'# ' + cid, s) else '?'
    species = grab(r'\*\*物种\*\* ([^|]+?) ?\|')
    job = grab(r'\*\*职业\*\* (.+)')
    creed = grab(r'\*\*信条\*\* (.+)')
    exp = grab(r'\*\*经历\*\* (.+)')
    hook = grab(r'\*\*钩子\*\* (.+)')
    lang = grab(r'\*\*语言\*\* (.+)')
    rings = re.findall(r'- (20\d\d-\d\d-\d\d) 「(.*?)」', s)
    evo = grab(r'\*\*进化\*\* (.+)')
    OUT.append('')
    OUT.append(f'--- {cid} {name} | {species} | 职业: {job}')
    OUT.append(f'    信条: {creed}')
    OUT.append(f'    经历: {exp}')
    OUT.append(f'    钩子: {hook}')
    OUT.append(f'    语言: {lang[:90]}')
    OUT.append(f'    年轮: {len(rings)} 圈 -> ' + ' / '.join(f'{d}:{q[:34]}' for d, q in rings))
    OUT.append(f'    进化: {evo}')

# --- 3. typhoon trio consumed by SC-004-01 (context) ---
OUT.append('')
OUT.append('=== typhoon trio (consumed by SC-004-01, excluded) ===')
for cid in ['C-00027', 'C-00028', 'C-00029']:
    p = os.path.join(BASE, cid + '.md')
    s = open(p, encoding='utf-8').read()
    name = re.match(r'# ' + cid + r' · (.+)', s).group(1).strip()
    job = grab(r'\*\*职业\*\* (.+)') if False else (re.search(r'\*\*职业\*\* (.+)', s).group(1).strip())
    OUT.append(f'{cid} {name} | {job}')

print('\n'.join(OUT))
