# -*- coding: utf-8 -*-
# R536 postscript: honest-accounting amendment (R520 precedent - operational reds after the round line was written)
import json, io, time

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
SP = ROOT + r'\src\os\state.json'

hm = time.strftime('%H:%M')
note = (
 '2026-09-27 ' + hm + ' R536 轮末补记（操作红如实更账·本行前 R536 行内「本轮零操作红」口径作废）：'
 '①轮末 diff 复核链 PS `>` 重定向落 UTF-16 件（R532 在案同型·零盘面副作用）→python subprocess capture 正法即过；'
 '②r536_close.py 尾部核验 print 一处 depts[6] 整型下标误用 TypeError（异常后置=两文件写盘与 json.load 复验皆已完成·零损·独立复核补齐）；'
 '③r536_prewrite.py 一处变量名笔误 write 后即修（盘面零运行红）；'
 '——三笔皆轮内闭环如实入账；探针复制律第四十九证方法论维持（三红皆非探针复制面·r536_all.py 新建+OUTP 改指照执行）。'
)

st = json.load(io.open(SP, encoding='utf-8'))
assert st['tick'] == 536
st['log'].append(note)
io.open(SP, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=1) + '\n')
st2 = json.load(io.open(SP, encoding='utf-8'))
print('POSTSCRIPT_OK tick=%d log_n=%d' % (st2['tick'], len(st2['log'])))
