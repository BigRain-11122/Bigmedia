# -*- coding: utf-8 -*-
# r1356 state accounting: append log line, tick+1, ts+task refresh,
# focus refresh, decisions_watermark advance (dnums +6, board_rows 49->51)
import json, io, re, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = os.path.join(ROOT, 'src', 'os', 'state.json')

line = io.open(os.path.join(ROOT, '.c3-tmp', 'r1356_logline.txt'), encoding='utf-8').read().strip()

focus = ("R1356 集团决策批消费轮毕（decisions 水位差集 NEW=6=D-20261005-06~11 科学判断闸全过审零驳回·涉司行 D-06=席 6 收讫注记零新执行面·"
         "派工板 49→51〔+D-20261005-05①②③ 三行皆非本司面·05① OSS 欠七实体不含本司=w3 义务已满〕·水位 dnums 142→148·ack 三载体 commit 含双律号）——"
         "下轮可领序：①~18:00 傍晚窗 DAILY v68 standby（怀旧/dusk/13·R1337 注册行）②今晚 21:40 OSS 窗 4 首切片（OH-20261005 台账件+收益透镜 3 型标注首用）"
         "③10-06 日界批（10-06 日报补产→E31 REACT-v9 择优·F-155 预指位维持）④10-07 #57 替代率首报终报→异常即转全任务书")

st = json.load(io.open(SP, encoding='utf-8'))
assert st.get('tick') == 1355, 'unexpected tick %s' % st.get('tick')
st['tick'] = st.get('tick', 0) + 1
st['ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
task_src = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}x?\s*', '', line)
st['task'] = task_src[:60]
st['focus'] = focus
st.setdefault('log', []).append(line)

wm = st['decisions_watermark']
new_dnums = ['D-20261005-06', 'D-20261005-07', 'D-20261005-08', 'D-20261005-09', 'D-20261005-10', 'D-20261005-11']
dset = set(wm.get('dnums', []))
added = [d for d in new_dnums if d not in dset]
assert len(added) == 6, 'expected 6 new dnums, got %s' % added
wm['dnums'] = sorted(dset | set(new_dnums))
assert wm.get('board_rows') == 49, 'unexpected board_rows %s' % wm.get('board_rows')
wm['board_rows'] = 51
wm['ts'] = st['ts']

io.open(SP, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2) + '\n')
print('tick=%s ts=%s' % (st['tick'], st['ts']))
print('task=%s' % st['task'])
print('wm dnums=%d board_rows=%s wm.ts=%s' % (len(wm['dnums']), wm['board_rows'], wm['ts']))
print('log_len=%d last_line_len=%d' % (len(st['log']), len(st['log'][-1])))
