import io, sys

for f in ('src/render/edit_craft.py', 'src/render/render_card_video.py'):
    lines = io.open(f, encoding='utf-8').read().splitlines()
    print('=== ' + f + ' ===')
    seen = set()
    for i, l in enumerate(lines):
        if 'drawtext' in l and i not in seen:
            for j in range(max(0, i - 3), min(len(lines), i + 7)):
                if j not in seen:
                    seen.add(j)
                    print('%5d: %s' % (j + 1, lines[j]))
            print('---')
