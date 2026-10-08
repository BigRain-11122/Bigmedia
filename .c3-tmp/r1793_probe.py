import json
p = json.load(open(r'data\storylines\drama\md0001\t2i\PACK-v1.json', encoding='utf-8'))
for s in p['shots']:
    if s['id'] in (6, 7, 9, 12):
        print('SHOT', s['id'], s.get('char'), 'seed', s['seed'])
        print('  prompt:', s['prompt'])
for f in ('data\storylines\drama\md0001\storyboard-schema-v0.1.json',
          'data\storylines\drama\md0001\SCRIPT-v1.md'):
    try:
        txt = open(f, encoding='utf-8').read()
        for kw in ('shot06', 'shot07', '6.', '7.'):
            pass
        print('--- file:', f, 'len', len(txt))
        break
    except Exception as e:
        print('skip', f, e)
# storyboard shots 6/7/9/12 narration
try:
    sb = json.load(open(r'data\storylines\drama\md0001\storyboard-schema-v0.1.json', encoding='utf-8'))
    shots = sb.get('shots') if isinstance(sb, dict) else sb
    for sh in shots:
        if isinstance(sh, dict) and sh.get('id') in (6, 7, 9, 12):
            print('SB', json.dumps(sh, ensure_ascii=False)[:500])
except Exception as e:
    print('sb err', e)
