# -*- coding: utf-8 -*-
# r1352 state accounting: append log line, tick+1, refresh ts+task+focus fields (PT-20260925-02 law)
import json, io, re, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = os.path.join(ROOT, 'src', 'os', 'state.json')

line = io.open(os.path.join(ROOT, '.c3-tmp', 'r1352_logline.txt'), encoding='utf-8').read().strip()

st = json.load(io.open(SP, encoding='utf-8'))
assert st.get('tick') == 1351, 'unexpected tick %s' % st.get('tick')
st['tick'] = st.get('tick', 0) + 1
st['ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
task_src = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}x?\s*', '', line)
st['task'] = task_src[:60]
st['focus'] = u'R1352 声明窗 6/6 窗满批闭（R1347~R1352 批收·并窗重置 0/6）·取活顺序：~18:00 傍晚窗 DAILY v68 standby 兑现（怀旧/dusk/13·2 分位实物）→今晚 21:40 OSS 窗 4 首切片（OH-20261005 台账件+收益透镜 3 型标注首用 P-20260926-08+P-2026-10-04-02）→REACT-v9 10-06 窗（10-06 日报先补产·F-155 预指位）→10-07 #57 替代率终报（一命令复跑刷新数据窗+底稿升 v1.0+HQ-FEEDBACK 行）→10-08 GB 闸/复市 DAILY 三面（烟火/13+market_open/close）→10-10 B3 W41 期；festival 季节门控行=春节窗解锁位；P-2 观察窗至 11-04；异常即转全任务书'
st.setdefault('log', []).append(line)

io.open(SP, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2) + '\n')
print('tick=%s ts=%s' % (st['tick'], st['ts']))
print('task=%s' % st['task'])
print('log_len=%d last_line_len=%d' % (len(st['log']), len(st['log'][-1])))
