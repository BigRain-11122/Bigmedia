# -*- coding: utf-8 -*-
# R680 verify: json integrity + content anchors post-close
import json, io, collections

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
ok = []
fails = []

st = json.load(io.open(ROOT + r'\src\os\state.json', encoding='utf-8'))
ok.append(('tick', st['tick'] == 680))
ok.append(('logN', len(st['log']) == 704))
ok.append(('tail_is_R680', st['log'][-1].startswith('2026-09-29 11:') and 'R680' in st['log'][-1][:40]))
ok.append(('ts', st['ts'].startswith('2026-09-29 11:4')))
ok.append(('task_len', len(st['task']) == 60))
ok.append(('focus_R681', st['focus'].startswith('R681:')))
ok.append(('production', st['production'] == 'open'))

se = json.load(io.open(ROOT + r'\docs\status-export.json', encoding='utf-8'))
ok.append(('export_ts', se['export_ts'].startswith('2026-09-29T11:4')))
ok.append(('results_tail_680', se['results'][-1][0] == '680'))
tickels = [el for el in se['outs'][0] if isinstance(el, str) and el.startswith('tick ')]
ok.append(('os_tick_680', tickels and tickels[0].startswith('tick 680')))

rd = io.open(ROOT + r'\output\renders\README.md', encoding='utf-8').read()
ok.append(('renders_row', 'lc-002-v1-shipinhao-60s.mp4' in rd and rd.count('| lc-002-v1-shipinhao-60s.mp4 |') == 1))
ok.append(('renders_chain_note', 'R680 渲染链毕' in rd))
ok.append(('v8_decl', 'census-card-v8-vertical' in rd))

sr = io.open(ROOT + r'\docs\reviews\station-reviews.md', encoding='utf-8').read()
ok.append(('station_row', 'lc-002-v1-shipinhao=#79 尾注 D22 缺口续补首件' in sr))

lr = io.open(ROOT + r'\data\sources\lc002\README.md', encoding='utf-8').read()
ok.append(('lc002_readme', 'R680 渲染腿毕' in lr))

bk = io.open(ROOT + r'\src\os\backlog.md', encoding='utf-8').read()
ok.append(('backlog_r680', 'R680 渲染腿毕 2026-09-29' in bk))
ok.append(('backlog_89_unlock', 'R680 过会核收 2026-09-29' in bk))

cm = json.load(io.open(ROOT + r'\data\sources\lc002\cards-v1-matched.json', encoding='utf-8'))
ok.append(('matched_12', len(cm['cards']) == 12 and all('visual' in c for c in cm['cards'])))

for name, val in ok:
    print('%s: %s' % (name, 'True' if val else 'False'))
    if not val:
        fails.append(name)
print('FAILS=%s' % fails)
print('ALL_PASS' if not fails else 'HAS_FAIL')
