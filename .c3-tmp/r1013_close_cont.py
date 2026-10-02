# -*- coding: utf-8 -*-
"""R1013 close continuation: state.json already committed (tick=1013) in the first run;
the finished.md assert tripped on the legitimate forward-reference 'REACT-v9 顺延 F-129'
inside the F-128 block. Correct guard = no 'F-129 登记' block yet. Run the remaining five
ledger updates idempotently."""
import io, json, time, importlib.util, sys

spec = importlib.util.spec_from_file_location('r1013close', r'.c3-tmp\r1013_close.py')
# cannot import module (it executes); instead re-declare needed strings by exec of the
# constant definitions only: parse the file and exec up to the state.json section marker.
src = io.open(r'.c3-tmp\r1013_close.py', encoding='utf-8').read()
cut = src.find("# --- state.json")
ns = {}
exec(compile(src[:cut], 'r1013_consts', 'exec'), ns)  # defines NOW/RNUM/LOG/FOCUS/FIN_BLOCK/CARDS_LINE/SR_ROW/QUEUE_LINE

NOW = ns['NOW']
FIN_BLOCK = ns['FIN_BLOCK']
CARDS_LINE = ns['CARDS_LINE']
SR_ROW = ns['SR_ROW']
QUEUE_LINE = ns['QUEUE_LINE']
LOG = ns['LOG']

# state.json: already updated in first run; verify idempotence
p = 'src\\os\\state.json'
s = json.load(io.open(p, encoding='utf-8'))
assert s['tick'] == 1013, 'tick drift: %s' % s['tick']
assert s['log'][-1].startswith(u'2026-10-02 19:3x R1013'), 'last log is not R1013'

# finished.md F-129 block - correct guard: registration block, not forward reference
p1 = 'output\\finished.md'
t1 = io.open(p1, encoding='utf-8').read()
assert u'F-129 登记（R1013 生产轮）' not in t1, 'F-129 block already registered'
io.open(p1, 'a', encoding='utf-8', newline='\n').write(FIN_BLOCK + u'\n')

# cards README line
p2 = 'data\\storylines\\cards\\README.md'
t2 = io.open(p2, encoding='utf-8').read()
assert u'MC-20261002-DAILY-v44 登记' not in t2, 'cards line already present'
io.open(p2, 'a', encoding='utf-8', newline='\n').write(CARDS_LINE + u'\n')

# station-reviews row
p3 = 'docs\\reviews\\station-reviews.md'
t3 = io.open(p3, encoding='utf-8').read()
assert u'DAILY-v44' not in t3, 'station-reviews row already present'
io.open(p3, 'a', encoding='utf-8', newline='\n').write(SR_ROW + u'\n')

# queue section-E line
p4 = 'docs\\self-improvement-queue.md'
t4 = io.open(p4, encoding='utf-8').read()
assert u'R1013 E30 standby 续领' not in t4, 'queue line already present'
io.open(p4, 'a', encoding='utf-8', newline='\n').write(QUEUE_LINE + u'\n')

# status-export.json (P-61)
p5 = 'docs\\status-export.json'
e = json.load(io.open(p5, encoding='utf-8'))
e['export_ts'] = NOW
e['outs'][0][1] = (u"tick 1013，R1013 生产轮=E30 standby DAILY 续件《城市日签 044》F-129 登记（台词池烟火/festival/1 "
                   u"verbatim「热腾的豆浆配上油条，一整天都精神」·festival 桶当日直配第四十四证〔桶级·场景级=假日早晨早市"
                   u"过早面·四连灯带后首件非灯面=反同构变奏〕·线级新鲜度第四十一证=同轴异行第三十九证〔line1≠v4/v11/v19/v24/"
                   u"v27/v32/v38/REACT-v8 全部烟火已采行〕·旋转律=五轴并列最少最久未采回补烟火赎回〔v38 后 5 件首回〕·FREE 面"
                   u"全弱态逐行机核排除后唯一零卡面词面重复行胜出〔v38 meta 叙述面假命中定谳=R1010 整文匹配陷阱正面执行〕·"
                   u"闹×晨金句位〔族三十连〕·QUOTE-v2 零模板复用第四十四证·h2_size=50 梯档降档〔18.00em 驱动 margin +0.40em〕·"
                   u"验图 5/5·E4 同轮回填 8.0 三意愿无条件式〔旗①=来源行离靶旗=合规红线位〕·festival 余 57 行〔108 基线〕）。"
                   u"下轮=R1014 可领序：#70 OSS 窗 3〔10-02 21:40 后〕/10-03 日界批收+E31 REACT-v9〔F-130〕/E30 DAILY 续件 "
                   u"standby。真发布=blocked-on-CEO 账号物理件·发布锁=M5 不变")
e['results'].append(['1013', LOG])
e['live'] = [
    [u"当前活：R1013 生产轮=E30 standby DAILY 续件《城市日签 044》全链走门毕 F-129 登记（%s）" % NOW],
    [u"最近实物：data/storylines/cards/MC-20261002-DAILY-v44/MC-20261002-DAILY-v44.png（成品卡 F-129·L-卡 第九十件·DAILY 形态第四十四件·2026-10-02）"],
    [u"下个里程碑：#70 OSS 窗 3 切片 10-02 21:40 后开窗+E31 REACT-v9 10-03 日界轮全链=F-130（日报日界补产）——窗 ≤48h"],
]
io.open(p5, 'w', encoding='utf-8', newline='\n').write(
    json.dumps(e, ensure_ascii=False, indent=1) + '\n')
print('CLOSE-CONT OK ts=%s' % NOW)
