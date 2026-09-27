# -*- coding: utf-8 -*-
# R520 postscript: honest operation-red addendum line + ts refresh (append-only, no history rewrite)
import json, io, os, datetime

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
now = datetime.datetime.now()
stamp = now.strftime('%Y-%m-%d %H:%M')
ts = now.strftime('%Y-%m-%d %H:%M:%S')

ADD = (stamp + u' R520 轮末补记（操作红如实更账·本行前 R520 行内「轮内零操作红」口径作废）：'
u'①轮首 PS && 链 ParserError（R457/R471/R472 在案坑族·分跑即过·零盘面副作用）；'
u'②收账脚本首跑 %s 占位未替换 IndexError（模板串含 82% 字面量故 % 格式化不可用→改 stamp 字符串拼接即过·异常先于写盘=state.json 零污染·修复后 CLOSE_OK·双 JSON 复验过）'
u'——两笔皆轮内闭环如实入账；探针复制律第四十一证方法论维持（两红皆非探针复制面·r520 探针件 write_file 新建+OUTP 改指照执行）。')

sp = os.path.join(ROOT, 'src', 'os', 'state.json')
st = json.load(io.open(sp, 'r', encoding='utf-8'))
st['log'].append(ADD)
st['ts'] = ts
with io.open(sp, 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(st, fh, ensure_ascii=False, indent=1)
    fh.write('\n')
print('ADDENDUM_OK tick=%s ts=%s log_entries=%d' % (st['tick'], st['ts'], len(st['log'])))
