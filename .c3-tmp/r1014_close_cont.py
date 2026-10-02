# -*- coding: utf-8 -*-
"""R1014 close continuation: state.json already committed (tick=1014) in the first run;
the finished.md assert tripped on the legitimate forward-reference 'REACT-v9 顺延 F-130'
inside the F-129 block (R1013 same-type precedent r1013_close_cont.py). Correct guard =
no 'F-130 登记' registration block yet. Run the remaining five ledger updates idempotently."""
import io, json, time

src = io.open(r'.c3-tmp\r1014_close.py', encoding='utf-8').read()
cut = src.find("# --- state.json")
ns = {}
exec(compile(src[:cut], 'r1014_consts', 'exec'), ns)  # defines NOW/RNUM/LOG/FOCUS/FIN_BLOCK/CARDS_LINE/SR_ROW/QUEUE_LINE

NOW = ns['NOW']
FIN_BLOCK = ns['FIN_BLOCK']
CARDS_LINE = ns['CARDS_LINE']
SR_ROW = ns['SR_ROW']
QUEUE_LINE = ns['QUEUE_LINE']
LOG = ns['LOG']

# state.json: already updated in first run; verify idempotence
p = 'src\\os\\state.json'
s = json.load(io.open(p, encoding='utf-8'))
assert s['tick'] == 1014, 'tick drift: %s' % s['tick']
assert s['log'][-1].startswith(u'2026-10-02 19:5x R1014'), 'last log is not R1014'

# finished.md F-130 block - correct guard: registration block, not forward reference
p1 = 'output\\finished.md'
t1 = io.open(p1, encoding='utf-8').read()
assert u'F-130 登记（R1014 生产轮）' not in t1, 'F-130 block already registered'
io.open(p1, 'a', encoding='utf-8', newline='\n').write(FIN_BLOCK + u'\n')

# cards README line
p2 = 'data\\storylines\\cards\\README.md'
t2 = io.open(p2, encoding='utf-8').read()
assert u'MC-20261002-DAILY-v45 登记' not in t2, 'cards line already present'
io.open(p2, 'a', encoding='utf-8', newline='\n').write(CARDS_LINE + u'\n')

# station-reviews row
p3 = 'docs\\reviews\\station-reviews.md'
t3 = io.open(p3, encoding='utf-8').read()
assert u'DAILY-v45' not in t3, 'station-reviews row already present'
io.open(p3, 'a', encoding='utf-8', newline='\n').write(SR_ROW + u'\n')

# queue section-E line
p4 = 'docs\\self-improvement-queue.md'
t4 = io.open(p4, encoding='utf-8').read()
assert u'R1014 E30 standby 续领' not in t4, 'queue line already present'
io.open(p4, 'a', encoding='utf-8', newline='\n').write(QUEUE_LINE + u'\n')

# status-export.json (P-61)
p5 = 'docs\\status-export.json'
e = json.load(io.open(p5, encoding='utf-8'))
e['export_ts'] = NOW
e['outs'][0][1] = (u"tick 1014，R1014 生产轮=E30 standby DAILY 续件《城市日签 045》F-130 登记（台词池怀旧/festival/16 "
                   u"verbatim「老物件里藏着故事」·festival 桶当日直配第四十五证〔桶级·场景级=假日居家翻检老物件面·v44 晨面后"
                   u"第二件非灯面=反同构变奏续证〕·线级新鲜度第四十二证=同轴异行第四十证〔line16≠v2/v10/v16/v22/v25/v33/v39 "
                   u"全部怀旧已采行〕·旋转律=四轴并列最少最久未采回补怀旧赎回〔v39 后 5 件首回〕·FREE 面逐行机核排除后唯一零"
                   u"机核词面旗行胜出〔老物件/故事 fleet 零命中+藏着 v10 构式层诚实邻接注记〕·物×事金句位〔族三十一连〕·"
                   u"QUOTE-v2 零模板复用第四十五证·h2_size=60 零模板直配〔10.00em 驱动 margin +5.33em〕·验图 5/5·E4 同轮回填 "
                   u"8.0 三意愿正面〔旗①=wrapper 场景叙述句离靶旗〕·festival 余 56 行〔59 基线〕）。下轮=R1015 可领序："
                   u"#70 OSS 窗 3〔10-02 21:40 后〕/10-03 日界批收+E31 REACT-v9〔F-131 顺延〕/E30 DAILY 续件 standby。"
                   u"真发布=blocked-on-CEO 账号物理件·发布锁=M5 不变")
e['results'].append(['1014', LOG])
e['live'] = [
    [u"当前活：R1014 生产轮=E30 standby DAILY 续件《城市日签 045》全链走门毕 F-130 登记（%s）" % NOW],
    [u"最近实物：data/storylines/cards/MC-20261002-DAILY-v45/MC-20261002-DAILY-v45.png（成品卡 F-130·L-卡 第九十一件·DAILY 形态第四十五件·2026-10-02）"],
    [u"下个里程碑：#70 OSS 窗 3 切片 10-02 21:40 后开窗+E31 REACT-v9 10-03 日界轮全链=F-131 顺延（日报日界补产）——窗 ≤48h"],
]
io.open(p5, 'w', encoding='utf-8', newline='\n').write(
    json.dumps(e, ensure_ascii=False, indent=1) + '\n')
print('CLOSE-CONT OK ts=%s' % NOW)
