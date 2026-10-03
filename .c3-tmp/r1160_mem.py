# -*- coding: utf-8 -*-
import os, io, glob

def dir_size(p):
    tot = 0; files = []
    if os.path.isdir(p):
        for f in glob.glob(os.path.join(p,'*')):
            s = os.path.getsize(f)
            tot += s; files.append((os.path.basename(f), s))
    elif os.path.exists(p):
        tot = os.path.getsize(p); files.append((os.path.basename(p), tot))
    return tot, files

OUT=[]
for name, base in [
    ('BS-repo', r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'),
    ('media',   r'C:\Users\sjs20\Desktop\FluxGroup\media'),
    ('cph4',    r'C:\Users\sjs20\Desktop\FluxGroup\cph4'),
]:
    c = os.path.join(base,'CODELY.md')
    m = os.path.join(base,'.codely-cli','memory')
    cs, cf = dir_size(c)
    ms, mf = dir_size(m)
    OUT.append('%s: CODELY.md=%d B | .codely-cli/memory=%d B (%d files) | TOTAL=%d B' % (name, cs, ms, len(mf), cs+ms))
    for f,s in mf: OUT.append('   mem|%s %d B' % (f,s))

io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1160_mem.txt','w',encoding='utf-8').write('\n'.join(OUT))
print('ok')
