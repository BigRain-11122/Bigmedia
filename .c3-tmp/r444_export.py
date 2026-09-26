# -*- coding: utf-8 -*-
# R444 status-export refresh (P-61 step): export_ts + dept/OS/result fields derived from R444
import json, io, datetime

P = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\docs\status-export.json'
with io.open(P, encoding='utf-8') as f:
    se = json.load(f)

se['export_ts'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')

# dept: CEO office row appends the decisions-batch receipt; engineering row -> R444
for d in se['depts']:
    if d['n'] == u'总裁办公室':
        if 'D-20260927-01' not in d['t']:
            d['t'] += (u"+集团决策批 D-20260927-01~05 收讫（R444 五决科学判断闸全过审零驳回："
                u"D-01⑦ 技能动员令计数点名本司=回执 P-51 双载体核验在位→HQ-FEEDBACK F-20260927-01 更正行〔夜轮点名按行销项·计数应 6/8〕；"
                u"D-03=本司 OH 单文件实践正典确认合规；D-04=复审锚自评零违例〔复审门锚 commit 稳定产物件〕；"
                u"D-05②=orders 全文件扫采纳落件 r444_check.py〔编辑检测线〕；D-02/D-05①③=知悉）")
    if d['n'] == u'工程技术部':
        d['t'] = (u"OS 循环 R444（转办/决策收讫轮：decisions 40→45 五新行 D-20260927-01~05 处理+回执——"
            u"HQ-FEEDBACK F-20260927-01 技能动员令计数更正行〔P-51 双载体证据=commit 57dfce5/bfca664+state×5+finished×1〕"
            u"+D-05② 采纳 r444_check.py orders 全文件扫+编辑检测线+D-04 复审锚自评零违例+D-03 OH 合规确认·"
            u"ledger 28=锚零新转办〔PS 29 首查=编码误读轮内定谳〕·三探针与 R443 基线零漂移 board 0 FAIL/readiness 3 阻塞皆外部/loop_health 1 FAIL 在案史实零新增·"
            u"#71 重制腿③顺延 R445）·state.ts/task 心跳面刷新")

# outs[0]: OS loop headline -> R444 (previous kept as second slot per established two-slot pattern)
r444_out = (u"tick 444·R444（转办/决策收讫轮·decisions 五新行处理+回执：D-20260927-01~05 全过审零驳回——"
    u"①D-01⑦ 技能动员令计数「余 BigStream」更正=回执 P-51 双载体核验在位〔commit 57dfce5/bfca664+state.json×5+finished.md×1+backlog #65 done〕"
    u"→HQ-FEEDBACK F-20260927-01 行〔夜轮点名按行销项·计数应 6/8〕②D-05② orders 全文件扫令扫面采纳=r444_check.py 增 orders_edited_since_anchor 编辑检测线"
    u"〔防令扫面盲区·本司一令一文件结构自评达标〕③D-04 复审锚热票面禁令自评零违例〔S2/M4.5/E8 锚 commit 稳定产物件〕"
    u"④D-03 OH 台账位=本司实践合规确认⑤D-02/D-05①③=知悉——ledger 28=锚零新转办·#71 重制腿③顺延 R445〔批次①视频线两律重制+§4.5 赛博同步层首启用〕）")
if se['outs'] and se['outs'][0][0] == u'OS 循环':
    se['outs'][0][1] = r444_out

# results: OS round counter 443 -> 444
for r in se['results']:
    if r[1] == u'OS 轮次':
        r[0] = u'444'
        break

with io.open(P, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(se, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('export_ts=' + se['export_ts'])
