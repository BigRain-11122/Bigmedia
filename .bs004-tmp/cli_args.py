import io, re, sys

src = io.open('src/render/edit_craft.py', encoding='utf-8').read()
ms = re.findall(r'add_argument\(\s*[\'"]([^\'"]+)[\'"]', src)
print('\n'.join(ms))
print('---example invocations in docs---')
for doc in ['docs/editing-craft-spec.md']:
    t = io.open(doc, encoding='utf-8').read()
    for line in t.splitlines():
        if 'edit_craft.py' in line and '--' in line:
            print(line.strip()[:300])
