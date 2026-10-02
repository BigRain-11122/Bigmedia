# -*- coding: utf-8 -*-
# r986 patch: v17 build script re-pick zhixu/festival/12 (line16 blocked by city-spirit #47)
import io
p = r'data/storylines/cards/MC-20261002-DAILY-v17-tmp/build_daily_v17.py'
t = io.open(p, encoding='utf-8').read()
orig = t

def rep(a, b, must=True):
    global t
    if a not in t:
        if must:
            raise SystemExit('PATTERN NOT FOUND: %r' % a[:80])
        return
    t = t.replace(a, b)

rep('QUOTE_CORE = u"守规矩也要有情味"', 'QUOTE_CORE = u"节日里，大家开心就好"')
rep('AXIS, BUCKET, IDX = u"秩序", u"festival", 16', 'AXIS, BUCKET, IDX = u"秩序", u"festival", 12')
rep('Axis pick = zhixu (order)/\nfestival/16:', 'Axis pick = zhixu (order)/\nfestival/12:')
rep('x admitting\nrules must also carry human warmth (the rule-keeper crowd giving way to warmth) =\nrule-x-warmth axis-internal tension',
    'x saying\nduring the festival "everyone just being happy is what counts" (the rule-keeper crowd\ngiving way to joy) = rule-x-joy axis-internal tension')
rep('"shou guiju ye yao you qingwei" = anti-AI-flavor authenticity.', '"jiu hao" colloquial closing = anti-AI-flavor authenticity.')
rep('same-axis-different-line twelfth proof (line16 !=\nDAILY-v5 line4)', 'same-axis-different-line twelfth proof (line12 !=\nDAILY-v5 line4)')
rep(u'线级新鲜行 line16·轴面', u'线级新鲜行 line12·轴面')
rep(u'×承认规矩之外还要情味〔规矩轴给情味让位〕=\n                u"规×情轴内张力金句位', u'×说大家开心就好〔规矩轴给开心让位〕=\n                u"规×情轴内自反差金句位')
rep(u'meta["source_quote"] = u"「守规矩也要有情味」"', u'meta["source_quote"] = u"「节日里，大家开心就好」"')
rep(u'axes[秩序][festival][16]', u'axes[秩序][festival][12]')
rep(u'①引文=台词池 axes[秩序][festival][16]', u'①引文=台词池 axes[秩序][festival][12]')
rep(u'=秩序轴 line16 非 DAILY-v5 "', u'=秩序轴 line12 非 DAILY-v5 "')
rep(u'⑥国庆语境核=本行无「年味」措辞（年味类行=过年语境与国庆假期"\n                         u"时点错位·选材排除·R972 制承继·本行=规矩×情味通用节庆语气·无过节时点错位）',
    u'⑥国庆语境核=本行无「年味」措辞（年味类行=过年语境与国庆假期"\n                         u"时点错位·选材排除·R972 制承继·本行=节日通用语气·无过节时点错位）')
rep(u'「守规矩」「也要」=大众口语让步句式真感=人味命中〔去 AI 感/制作感双对位〕', u'「开心就好」=大众口语收束句式真感=人味命中〔去 AI 感/制作感双对位〕')
rep(u'落位=最讲规矩的居民先讲情味=规矩轴给情味让位〔硅基城市语境独占位·真城生命感方向对位="\n                         u"城市在假期变得更有人情味的活证据〕',
    u'落位=最讲规矩的居民先说开心=规矩轴给开心让位〔硅基城市语境独占位·真城生命感方向对位="\n                         u"城市在假期变得更有人情味的活证据·city-spirit #47 守规矩也要有情味同轴同旨异行=轴内主题纵深面〕')
rep(u'u"「守规矩也要有情味」",', u'u"「节日里，大家开心就好」",')
rep(u'质量选优=「守规矩〔最讲规矩居民的立身之本〕×也要有情味〔规矩轴对情味的让位式"\n                            u"补充〕」规×情轴内张力金句位+短句让步句式口语真感=去 AI 感制作感对位',
    u'质量选优=「节日里〔值守语境的时间限定〕×大家开心就好〔规矩轴给开心的让位式"\n                            u"放行〕」规×情轴内自反差金句位+「就好」口语收束真感=去 AI 感制作感对位')
rep(u'×承认规矩之外还要情味〔规矩轴给情味让位〕=规×情轴内张力金句位〔v15 屏×真/v16 往×今="\n                          u"轴内张力金句位族三连〕+「也要」让步句式口语真感',
    u'×说大家开心就好〔规矩轴给开心让位〕=规×情轴内自反差金句位〔v15 屏×真/v16 往×今="\n                          u"轴内自反差金句位族三连〕+「就好」口语收束真感')
rep(u'情 1 假期值守与情味并重的温和共鸣"\n                          u"如实非强极点', u'情 1 假期值守放行开心的温和暖意"\n                          u"如实非强极点')
rep(u'（守规矩者=无称谓视角非登记居民名）', u'（值守者=无称谓视角非登记居民名）')
rep(u'（街面值守=群体秩序场景面非个体档案面·', u'（街面值守放行=群体秩序场景面非个体档案面·')
rep('axes[zhixu][festival][16] verbatim OK', 'axes[zhixu][festival][12] verbatim OK')
rep('zhixu line16 != DAILY-v5 line4', 'zhixu line12 != DAILY-v5 line4')
rep(u'中间引文「守规矩也要有情味」', u'中间引文「节日里，大家开心就好」')
rep(u'一位秩序轴居民看着满街节日灯和出行人流时说的：守规矩也要有情味。\'\n    u\'（台词池池级署名·无具体姓名）——最讲规矩的人先讲情味，规矩给情味让了位。\'',
    u'一位秩序轴居民看着满街节日灯和出行人流时说的：节日里，大家开心就好。\'\n    u\'（台词池池级署名·无具体姓名）——最讲规矩的人先说开心，规矩给开心让了位。\'')
rep('# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts).',
    '# REACT-v8 xiaoyao/festival/17 + yanhuo/festival/12 + zhixu/festival/14 (source_facts).\n'
    '# city-spirit v1.2 festival-scene trio: zhixu/festival/16 + qiuxin/festival/14 + xiaqi/festival/0.')

assert t != orig
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('patched OK, %d replacements applied' % (orig != t))
