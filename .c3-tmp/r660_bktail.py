import os, re, io

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
p = os.path.join(ROOT, 'src', 'os', 'backlog.md')
lines = io.open(p, encoding='utf-8').read().splitlines()

f = io.open(os.path.join(ROOT, '.c3-tmp', 'r660_bktail.txt'), 'w', encoding='utf-8')
f.write(f"backlog total_lines={len(lines)}\n\n")
for i, l in enumerate(lines[241:], start=242):
    m = re.match(r'^(\d+)\.\s*(.{0,130})', l)
    if m:
        done = '[done' in l[:400] or '[done' in l
        f.write(f"L{i} #{m.group(1)} done={done} | {m.group(2)}\n")
    elif re.match(r'^\*\*\[', l):
        f.write(f"L{i}   note | {l[:110]}\n")
f.close()
print('done')
