import os, re, io, glob, datetime

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
f = io.open(os.path.join(ROOT, '.c3-tmp', 'r660_e4check.txt'), 'w', encoding='utf-8')

# 1. all expert-verdicts dirs
f.write("EXPERT_VERDICTS DIRS:\n")
for d in glob.glob(os.path.join(ROOT, '**', 'expert-verdicts'), recursive=True):
    if os.path.isdir(d):
        xs = os.listdir(d)
        f.write(f"  {os.path.relpath(d, ROOT)} files={len(xs)}\n")
        newest = sorted(xs, key=lambda x: os.path.getmtime(os.path.join(d, x)))[-4:]
        for x in newest:
            mt = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(d, x)))
            f.write(f"    {mt.strftime('%m-%d %H:%M')} {x}\n")

# 2. review files E4 status
for name in ['review-20260929-mcreact-v5.md', 'review-20260928-mcdigest-v9.md']:
    p = os.path.join(ROOT, 'docs', 'reviews', name)
    f.write(f"\n=== {name} exists={os.path.exists(p)}\n")
    if os.path.exists(p):
        txt = io.open(p, encoding='utf-8').read()
        f.write(f"  len={len(txt)} E4_mentions={txt.count('E4')} backfill={txt.count('回填')}\n")
        for l in txt.splitlines():
            if 'E4' in l or '回填' in l:
                f.write("  | " + l[:150] + "\n")

# 3. finished.md F-053/F-054 rows
p = os.path.join(ROOT, 'output', 'finished.md')
txt = io.open(p, encoding='utf-8').read().splitlines()
f.write("\nFINISHED rows F-053/F-054:\n")
for l in txt:
    if re.search(r'F-05[34]', l):
        f.write("  | " + l[:200] + "\n")

# 4. cards README v9/v5 rows
p = os.path.join(ROOT, 'data', 'storylines', 'cards', 'README.md')
txt = io.open(p, encoding='utf-8').read().splitlines()
f.write("\nCARDS README v9/v5 rows:\n")
for l in txt:
    if re.search(r'(DIGEST[- ]?v9|盘点 009|REACT[- ]?v5|速报 005)', l):
        f.write("  | " + l[:200] + "\n")

# 5. e4-result contents (scores)
for d in ['MC-20260928-DIGEST-v9-tmp', 'MC-20260929-REACT-v5-tmp']:
    p = os.path.join(ROOT, 'data', 'storylines', 'cards', d, 'e4-result.json')
    f.write(f"\n=== E4 RESULT {d}:\n")
    if os.path.exists(p):
        raw = io.open(p, encoding='utf-8').read()
        f.write(f"  len={len(raw)}\n")
        m = re.search(r'(评分|总分|打分|分数|score)[^\n]{0,60}', raw)
        if m:
            f.write("  score-ish: " + m.group(0)[:150] + "\n")

# 6. station-reviews tail
p = os.path.join(ROOT, 'docs', 'reviews', 'station-reviews.md')
if os.path.exists(p):
    txt = io.open(p, encoding='utf-8').read().splitlines()
    f.write(f"\nSTATION-REVIEWS total_lines={len(txt)} tail 6:\n")
    for l in txt[-6:]:
        f.write("  | " + l[:170] + "\n")

# 7. queue section D P-1
p = os.path.join(ROOT, 'docs', 'self-improvement-queue.md')
if os.path.exists(p):
    txt = io.open(p, encoding='utf-8').read()
    f.write(f"\nQUEUE file len={len(txt)}\n")
    m = re.search(r'§?D[^\n]*提案[^\n]*\n(.{0,1500})', txt)
    if m:
        for l in m.group(1).splitlines()[:22]:
            f.write("  | " + l[:170] + "\n")

f.close()
print('done')
