# -*- coding: utf-8 -*-
# R448 log-line correction before commit: E4 landed in-round (8min hot-cache),
# align the close-out line with actual facts (not yet committed).
import json
from pathlib import Path

sp = Path(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json')
st = json.loads(sp.read_text(encoding='utf-8'))
log = st['log']
assert log, 'no log lines'
line = log[-1]
assert 'R448:' in line, 'last log is not R448'

a_old = '轮间异步落地=下轮回填 R180/R187 追加制先例）'
a_new = ('01:04:52 落地 ~8min 热载快落=R448 同轮回填毕：**8.0 会看完+会点赞并转发'
         '=批次参考线带持平（DY 同带）·L18 观众侧零黑话旗零术语旗=易懂性三源证据链闭环'
         '（机检 0 WARN+ASR 释义位净读+E4 零听不懂旗）**·两旗（432 账本可查空洞感/吹牛'
         '检测缺执行细节）=M5 证据链语境信任校准位·净本 expert-verdicts/20260927-010452）')
assert a_old in line, 'anchor A missing'
line = line.replace(a_old, a_new)

b_old = 'E4 qwen 在飞=落地轮记账·本地 Ollama 零 API token'
b_new = 'E4 qwen 8.0 本轮落地记账·本地 Ollama 零 API token'
assert b_old in line, 'anchor B missing'
line = line.replace(b_old, b_new)

c_old = '=逐件随轮继+E4 回填下轮首读。收账显式列文件 commit+push。'
c_new = '=逐件随轮继（E4 已同轮回填毕·station-reviews 追记行在账）。收账显式列文件 commit+push。'
assert c_old in line, 'anchor C missing'
line = line.replace(c_old, c_new)

log[-1] = line
sp.write_text(json.dumps(st, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('log line corrected, ts=%s' % st['ts'])
