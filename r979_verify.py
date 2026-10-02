# -*- coding: utf-8 -*-
import io, json
st = json.load(io.open(r'src\os\state.json', encoding='utf-8'))
print('tick', st['tick'], 'dnums', len(st['decisions_watermark']['dnums']), 'ts', st['ts'])
print('task:', st['task'])
print('log tail:', st['log'][-1][:120])
ex = json.load(io.open(r'docs\status-export.json', encoding='utf-8'))
print('export_ts', ex['export_ts'], 'results', len(ex['results']))
print('live[0]:', ex['live'][0][0][:100])
# board/board_check/readiness probes
print('PROBES NEXT')
