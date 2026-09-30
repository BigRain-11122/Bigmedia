# -*- coding: utf-8 -*-
# R682 verify (run-after-read law, R655 lesson)
import io, json, collections, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
out = []
ok = True

st = json.load(io.open(ROOT + r'\src\os\state.json', encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
checks = [
    ('tick==682', st.get('tick') == 682),
    ('ts_fresh', st.get('ts', '').startswith('2026-09-29 12:')),
    ('task_len==60', len(st.get('task', '')) == 60),
    ('task_head', st.get('task', '').startswith('R682: ')),
    ('logN==706', len(st['log']) == 706),
    ('log_tail_R682', 'R682: ' in st['log'][-1] and 'DIGEST-v10' in st['log'][-1]),
    ('log_tail_decisions74', '74\u226070' in st['log'][-1]),
    ('production_open', st.get('production') == 'open'),
    ('focus_R683', 'R683' in st.get('focus', '')),
]
for name, val in checks:
    out.append('%s=%s' % (name, val))
    ok = ok and val

se = json.load(io.open(ROOT + r'\docs\status-export.json', encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
osrow = se['outs'][0]
se_checks = [
    ('export_ts_fresh', se.get('export_ts', '').startswith('2026-09-29T12:')),
    ('os_row_tick682', any(isinstance(e, str) and e.startswith('tick 682') for e in osrow)),
    ('os_row_len2', len(osrow) == 2),
    ('results_45', len(se['results']) == 45),
    ('results_last_682', se['results'][-1][0] == '682' and 'DIGEST-v10' in se['results'][-1][1]),
]
for name, val in se_checks:
    out.append('%s=%s' % (name, val))
    ok = ok and val

bl = io.open(ROOT + r'\src\os\backlog.md', encoding='utf-8').read()
q = io.open(ROOT + r'\docs\self-improvement-queue.md', encoding='utf-8').read()
cards = io.open(ROOT + r'\data\storylines\cards\README.md', encoding='utf-8').read()
fin = io.open(ROOT + r'\output\finished.md', encoding='utf-8').read()
sr = io.open(ROOT + r'\docs\reviews\station-reviews.md', encoding='utf-8').read()
file_checks = [
    ('bl_R682_note', 'R682 claim+交付毕 2026-09-29' in bl),
    ('bl_R682_after_R631', bl.find('R682 claim+交付毕 2026-09-29') > bl.find('[R631 claim+交付毕')),
    ('bl_R681_not_duplicated', bl.count('R682 claim+交付毕 2026-09-29') == 1),
    ('queue_burn_line', 'E2 批活池首件兑现（R682' in q),
    ('cards_v10_line', 'MC-20260929-DIGEST-v10 登记（R682' in cards),
    ('finished_F056', 'F-056 登记（R682）' in fin),
    ('finished_F056_count1', fin.count('F-056 登记（R682）') == 1),
    ('sr_R682_row', 'DIGEST-v10=queue §E 批活池 E2 首件' in sr),
    ('render_mp4_moved', not os.path.exists(ROOT + r'\output\renders\mc-20260929-digest-v10-card.mp4')),
    ('tmp_mp4_in_place', os.path.exists(ROOT + r'\data\storylines\cards\MC-20260929-DIGEST-v10-tmp\mc-20260929-digest-v10-card.mp4')),
    ('cards_json_ok', os.path.exists(ROOT + r'\data\storylines\cards\MC-20260929-DIGEST-v10\cards.json')),
    ('png_ok', os.path.exists(ROOT + r'\data\storylines\cards\MC-20260929-DIGEST-v10\MC-20260929-DIGEST-v10.png')),
    ('review_file_ok', os.path.exists(ROOT + r'\docs\reviews\review-20260929-mcdigest-v10.md')),
]
for name, val in file_checks:
    out.append('%s=%s' % (name, val))
    ok = ok and val

out.append('VERIFY: ' + ('ALL PASS' if ok else 'FAIL'))
io.open(ROOT + r'\.c3-tmp\r682_verify.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
