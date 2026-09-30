# -*- coding: utf-8 -*-
# R670 addendum: record close-sequence op-red (verify expectation off-by-one) per R655/R659/R669 precedent
import io, json, datetime, collections

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
ST = ROOT + r'\src\os\state.json'
now = datetime.datetime.now()
ts_min = now.strftime('%Y-%m-%d %H:%M')

ADDENDUM = (ts_min + u" R670 轮末补记（操作红如实入账·追加制原行不改写·R655/R659/R669 补记先例）——"
u"close 后 verify 首跑 12/13 PASS+1 FAIL=log_count 预期 692≠实读 693：根因=预期链漏算 R669 轮末补记行自身"
u"（R669 权威复验 logN691=补记追加前时点读数·补记 +1→692·R670 +1→693）·数据链零损伤"
u"（log[-2]=R669 补记位 PASS·log[-1]=R670 位 PASS·tick/ts/task/focus/export 12 项全 PASS）→"
u"预期修正 693 复跑 13/13 ALL_PASS（r670_verify2.txt 留档·r670_verify.txt 首跑件留档不删=R655 先例）——"
u"verify 预期清单律增补：轮末补记行自身计入 log 计数基线（本轮收口基线 693+本笔=694·下轮 close 预期=当前实读+1）")

st = json.load(io.open(ST, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
assert st['tick'] == 670 and len(st['log']) == 693, 'precondition drift: tick=%s logN=%d' % (st['tick'], len(st['log']))
st['log'].append(ADDENDUM)
io.open(ST, 'w', encoding='utf-8').write(json.dumps(st, indent=2, ensure_ascii=False) + '\n')
print('addendum done logN=%d' % len(st['log']))
