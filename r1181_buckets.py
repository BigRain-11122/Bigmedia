import json, io
p = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json"
out = io.StringIO()
d = json.load(open(p, encoding='utf-8'))
for ax, buck in d.items():
    if isinstance(buck, dict):
        for bk, lst in buck.items():
            n = len(lst) if isinstance(lst, list) else -1
            out.write("AXES=%s BUCKET=%s n=%d\n" % (ax, bk, n))
    else:
        out.write("AXES=%s n=%d\n" % (ax, len(buck) if isinstance(buck, list) else -1))
io.open(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\r1181_buckets.txt", 'w', encoding='utf-8').write(out.getvalue())
print("ok")
