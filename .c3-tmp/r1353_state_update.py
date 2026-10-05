# -*- coding: utf-8 -*-
# R1353 state accounting: append log line, tick+1, refresh ts+task+focus fields (PT-20260925-02 law)
import json, io, re, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = os.path.join(ROOT, 'src', 'os', 'state.json')

line = io.open(os.path.join(ROOT, '.c3-tmp', 'r1353_logline.txt'), encoding='utf-8').read().strip()

st = json.load(io.open(SP, encoding='utf-8'))
assert st.get('tick') == 1352, 'unexpected tick %s' % st.get('tick')
st['tick'] = st.get('tick', 0) + 1
st['ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
task_src = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}x?\s*', '', line)
st['task'] = task_src[:60]
st['focus'] = (u'R1353 生产轮交付毕（#86 a 腿三批 city-spirit v1.3 +19 条·盲区修正轮·声明窗重置 0/6）——下轮可领序：'
               u'①~18:00 傍晚窗 DAILY v68 standby（怀旧/dusk/13·R1337 注册行）②今晚 21:40 OSS 窗 4 首切片'
               u'（OH-20261005 台账件+收益透镜 3 型标注=P-20261026-08+P-2026-10-04-02）③10-06 日界批'
               u'（10-06 日报补产→E31 REACT-v9 择优·F-155 预指位维持）④10-07 #57 替代率首报终报'
               u'（一命令复跑刷新数据窗+底稿升 v1.0+HQ-FEEDBACK 行）⑤#86 a 腿四批随轮评估'
               u'（剩余 414 候选谚语级密度显著降·或待 BigLife 池扩容）→异常即转全任务书')
st.setdefault('log', []).append(line)

io.open(SP, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2) + '\n')
print('tick=%s ts=%s' % (st['tick'], st['ts']))
print('log_len=%d last_line_len=%d' % (len(st['log']), len(st['log'][-1])))
