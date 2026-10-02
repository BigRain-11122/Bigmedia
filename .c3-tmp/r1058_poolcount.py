import io, json, os

pj = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
d = json.load(io.open(pj, encoding='utf-8'))

def count_leaves(obj):
    # pools structure: axes -> axis -> bucket -> list of strings; sprite -> bucket -> list
    total = 0
    def walk(x):
        nonlocal total
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                if isinstance(v, str):
                    total += 1
                else:
                    walk(v)
    walk(obj)
    return total

axes = d.get('axes', {})
sprite = d.get('sprite', {})
na = count_leaves(axes)
ns = count_leaves(sprite)
print('AXES_LEAVES %d (baseline 1296)' % na)
print('SPRITE_LEAVES %d (baseline 144)' % ns)
print('TOTAL %d (baseline 1440)' % (na + ns))
print('VERDICT', 'MATCH' if (na, ns) == (1296, 144) else 'DRIFT')
