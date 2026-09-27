# -*- coding: utf-8 -*-
# R539 addendum: operation-red honest accounting (R536 precedent) - main-line "one red" claim voided, actual two
import json, io, time

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
SP = ROOT + r'\src\os\state.json'

ts_full = time.strftime('%Y-%m-%d %H:%M:%S')
hm = time.strftime('%H:%M')

addline = (
 '2026-09-27 ' + hm + ' R539 轮末补记（操作红如实更账·本行前 R539 行内「随行操作红一笔」口径作废→实为两笔）：'
 '②轮末收账验证链 PS `>` 重定向落 r539_close_out.txt 非 UTF-8 显示件（R532/R536 在案同型·零盘面副作用）'
 '——数据件全 Python io.open UTF-8 直写不受影响（state.json/status-export.json json.load 复验过）；'
 '正法=python subprocess capture 直写 UTF-8 件（下轮收账验证步照执行）；'
 '①PS && ParserError 笔已在主行如实记（R524/R536/R537/R538 同型）——两笔皆轮内闭环零遗留。'
)

st = json.load(io.open(SP, encoding='utf-8'))
assert st['tick'] == 539, 'tick unexpected: %s' % st['tick']
assert st['log'][-1].find('R539: ') >= 0, 'main R539 line not at tail'
st['log'].append(addline)
st['ts'] = ts_full
io.open(SP, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=1) + '\n')

st2 = json.load(io.open(SP, encoding='utf-8'))
print('ADDENDUM_OK tick=%d log_total=%d ts=%s' % (st2['tick'], len(st2['log']), st2['ts']))
print('tail_is_addendum=%s' % (st2['log'][-1].find('R539 round-end addendum') >= 0))
