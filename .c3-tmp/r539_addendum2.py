# -*- coding: utf-8 -*-
# R539 addendum #2: third operation red - tmp verify pattern literal mismatch (non-ASCII literal in probe script
# violated R533 canon); ground truth independently verified (find_pos=17 via \u-escape + disk read)
import json, io, time

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
SP = ROOT + r'\src\os\state.json'

ts_full = time.strftime('%Y-%m-%d %H:%M:%S')
hm = time.strftime('%H:%M')

addline = (
 '2026-09-27 ' + hm + ' R539 轮末补记第二笔（操作红如实更账·第一笔补记「实为两笔」口径再作废→实为三笔）：'
 '③r539_addendum.py 尾部验证 find pattern 非中文字面落盘为英文字面量（与中文补记行不匹配→find −1→tail_is_addendum=False 假阴性打印）'
 '——盘上真值独立双通道复核定谳=python -X utf8 \\u 转义通道 find_pos=17+read_file 磁盘直读=补记行在位完整·state 数据件零损；'
 '根因类=探针脚本非 ASCII pattern 字面量律违例（R533 立法同族·r531/r532 tag 腐蚀案同源）'
 '→防再犯=收账验证 pattern 一律 ASCII 切片或 \\u 转义（本笔验证即执行）·补记行本体中文内容落盘正确=仅 pattern 行字面不匹配；'
 '三笔操作红（①PS && ParserError ②PS `>` 重定向 ③pattern 字面）皆轮内闭环零遗留。'
)

st = json.load(io.open(SP, encoding='utf-8'))
assert st['tick'] == 539, 'tick unexpected: %s' % st['tick']
assert st['log'][-1].find('R539 ' + u'\u8f6e\u672b\u8865\u8bb0') >= 0, 'addendum #1 not at tail'
st['log'].append(addline)
st['ts'] = ts_full
io.open(SP, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=1) + '\n')

st2 = json.load(io.open(SP, encoding='utf-8'))
tail_ok = st2['log'][-1].find(u'\u7b2c\u4e8c\u7b14') >= 0  # 'di-er bi' marker via escapes
print('ADDENDUM2_OK tick=%d log_total=%d tail_is_addendum2=%s ts=%s' % (st2['tick'], len(st2['log']), tail_ok, st2['ts']))
