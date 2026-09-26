# -*- coding: utf-8 -*-
# R446 close-fix: S1 landed in-round (9/10 PASS) -> amend log line, task, focus
import json
import datetime
from pathlib import Path

R = Path(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream')
sp = R / 'src' / 'os' / 'state.json'
st = json.loads(sp.read_text(encoding='utf-8'))

st['focus'] = ("R447: 快速路径首查→#71 F-001 续链（S1 已过门 9/10 PASS=零违律顶格 9·判词档 20260927-003531）=对位表 cards-v15-matched（v12-matched 承继+卡面文本对齐）→R-E 渲染〔--series-badge/--series-id 角标常驻位路线=§5.5 二选一律·≤60s 短件不用片头帧〕+§4.5 三开关逐件启用→S2 三门→E8→M4→finished 更账 SUPERSEDED 处置→呈 CEO 目检；F-002~F-004 逐件随轮继→#73 调研部回执件（P-2026-09-26-18·≤09-28 12:00·复用选题研究部声明轻件）→#21 周日立法件 09-27 届日即领〔T2⑦ 慢直播合规注记与 #17 合流〕→#59 REACT 09-27 热点窗届日即领（日报 09-27 已在案）→#70 OH 切片 2（≤09-29 21:40·换刀·单窗 ≤3 刀）→#63 图鉴 C-00030 锚轮首核（supply-gated 照守）→#72 素材消费面知悉挂账→#57 替代率首报 10-07 挂账——新令/集团转办/探针红出现即优先（异常或实活轮出现即提前收账）；全静即 idle-fast（新窗 1/6）")

old = st['log'][-1]
fix_old = "③S1 v1.5+L18-L20 新旗面门起飞（.bs001-v15-tmp/s1_call.py 1500s 脱壳 PID 26496·00:35:14 起·材料=s1-review-material-v15.md 盲评律合规·判初稿〔空气预算机械裁不回炉·BS-002/003/004/005 先例〕·s1-result.json 轮间异步落地）"
fix_new = "③S1 v1.5+L18-L20 新旗面门**轮内落地过门=9/10 PASS**（.bs001-v15-tmp/s1_call.py 1500s 脱壳 PID 26496·00:35:14 起飞 00:35:31 落判 17s=热载快落〔R382 E4 11s 同型〕·材料=s1-review-material-v15.md 盲评律合规·判初稿〔空气预算机械裁不回炉·BS-002/003/004/005 先例〕·零违律顶格 9=C4 v2 刻度锚⑤〔无亮点引证=顶格 9 非 10〕·未测面=配音实听/视觉画面=对应席补·判词档 expert-verdicts/20260927-003531-S1-script+expert-calls 行 wrapper 自动+s1-result.json 留档）"
assert fix_old in old, 'log tail anchor not found'
st['log'][-1] = old.replace(fix_old, fix_new)
st['log'][-1] = st['log'][-1].replace(
    "tokens:local=1（S1 qwen2.5:14b 在飞未落=落地轮记账·本地 Ollama 零 API token·P-54⑤ 计量律）",
    "tokens:local=1（S1 qwen2.5:14b 一判=轮内落地已记账·本地 Ollama 零 API token·P-54⑤ 计量律）")
st['log'][-1] = st['log'][-1].replace(
    "下轮=R447 首读 s1-result.json→≥9 过门续链或 <9 整改。",
    "S1 过门=F-001 首件重制前三腿（拍稿/M1/空气预算）+判分毕·渲染腿（对位表→R-E→S2→E8→M4）=R447 续做。")
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
st['ts'] = now
st['task'] = st['log'][-1].split('R446: ', 1)[1][:60]
sp.write_text(json.dumps(st, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('amended tick=%d ts=%s' % (st['tick'], now))
print('task_head=' + st['task'][:40])
print('s1_landed_in_log=' + str('轮内落地过门' in st['log'][-1]))
