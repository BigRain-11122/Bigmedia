import json, subprocess, os

GIT = r'C:\Program Files\Git\cmd\git.exe'
BIGLIFE = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife'
POOL_REL = os.path.join('cognition', 'pools.json')

def flat(d):
    lines = []
    for axis, scenes in d['axes'].items():
        for scene, ls in scenes.items():
            for ln in ls:
                lines.append(ln.strip())
    for scene, ls in d.get('sprite', {}).items():
        for ln in ls:
            lines.append(ln.strip())
    return lines

cur_path = os.path.join(BIGLIFE, POOL_REL)
cur = json.load(open(cur_path, encoding='utf-8'))
cur_lines = flat(cur)
cur_unique = set(cur_lines)

raw = subprocess.run([GIT, '-C', BIGLIFE, 'show', 'HEAD:' + POOL_REL.replace('\\', '/')],
                     capture_output=True).stdout
head = json.loads(raw.decode('utf-8'))
head_unique = set(flat(head))

diff = cur_unique - head_unique
cur_n = len(cur_unique)
head_n = len(head_unique)

gate_open = (cur_n > 1440) or (len(diff) > 0)
print('gate12-check: cur_unique=%d head_unique=%d new_lines=%d gate_open=%s' % (
    cur_n, head_n, len(diff), gate_open))
if diff:
    for ln in sorted(diff)[:10]:
        print('NEW:', ln[:60])
