# r631_rowdiff.py -- character-level diff of the edited P-2026-09-25-18 row (ASCII source)
import io, re, difflib

def rows(path):
    out = []
    for l in io.open(path, encoding='utf-8'):
        if l.strip():
            out.append(re.sub(r'^L\d+\t', '', l.rstrip('\n')))
    return out

a = rows('.c3-tmp/r630_lednew5.txt')
b = rows('.c3-tmp/r631_lednew5.txt')
old = [l for l in a if l not in b]
new = [l for l in b if l not in a]
res = []
if old and new:
    sm = difflib.SequenceMatcher(None, old[0], new[0])
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal':
            res.append('OP=%s OLD[%d:%d]=%r NEW[%d:%d]=%r' % (tag, i1, i2, old[0][i1:i2], j1, j2, new[0][j1:j2]))
    res.append('SAME_PREFIX_LEN=%d OLD_LEN=%d NEW_LEN=%d' % (sm.find_longest_match(0, len(old[0]), 0, len(new[0])).size, len(old[0]), len(new[0])))
else:
    res.append('old=%d new=%d' % (len(old), len(new)))
with io.open('.c3-tmp/r631_rowdiff.txt', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(res) + '\n')
print('\n'.join(l for l in res if all(ord(c) < 128 for c in l)))
