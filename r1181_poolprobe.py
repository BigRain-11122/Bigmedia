import json, io
p = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
out = io.StringIO()
d = json.load(open(p, encoding='utf-8'))
out.write("top_type=%s\n" % type(d).__name__)

buckets = {}
def walk(o, axes=None, bucket=None):
    if isinstance(o, dict):
        ax = o.get('axes', axes)
        bk = o.get('bucket', o.get('situ', bucket))
        for k, v in o.items():
            if k in ('axes', 'axis'):
                ax = v
            if k in ('bucket', 'situ', 'situation'):
                bk = v
            walk(v, ax, bk)
    elif isinstance(o, list):
        for x in o:
            walk(x, axes, bucket)
    else:
        if isinstance(o, str) and o.strip():
            key = (str(axes), str(bucket))
            buckets.setdefault(key, []).append(o)

walk(d)
for k in sorted(buckets, key=lambda x: -len(buckets[x])):
    out.write("AXES=%s BUCKET=%s n=%d sample=%s\n" % (k[0], k[1], len(buckets[k]), buckets[k][0][:40]))

io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\r1181_poolprobe.txt", 'w', encoding='utf-8').write(out.getvalue())
print("ok buckets=%d" % len(buckets))
