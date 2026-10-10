import io, json
d = json.load(io.open('docs/status-export.json', encoding='utf-8'))
print('export_ts:', d.get('export_ts'))
for row in d.get('live', []):
    print(repr(row))
