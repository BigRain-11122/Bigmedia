# -*- coding: utf-8 -*-
# R870: claim backlog #67 (DIGEST v11) - append claim line to #67 block
import io

p = 'src/os/backlog.md'
t = io.open(p, encoding='utf-8').read()
nl = '\r\n' if '\r\n' in t else '\n'
lines = t.split(nl)

claim = ('   **[R870 claim 2026-10-01：循环认领（两步制 claim 先落防撞·供给盲区修正轮）——DIGEST 续件第十一件='
         '《城市盘点 011·产品优先令数字盘点》（史源锚=CEO 直令 P-2026-09-29-07 2026-09-29 ~13:0x〔cph4/evolution-ledger.md '
         '正行 CEO 原话 verbatim 全句+诊断读数 8 仓 7 天 10,524 commit/本司文档簿记占比 46%〕+本司台账链〔iteration_prompt.txt '
         '产品优先律块=计分三档 2/1/0/记账帽 ≤5/export 三行窗 ≤48h/24h 零实物判负+finished.md F-057→F-081 令后 25 件 40 '
         '小时+state R685→R809 时间戳链〕）·全链=M0 四维分→M1 纪实数字汇编律复用→M2 --poster+em 预算前置适配+垂直栈预算律+'
         '验图五检→M3 标题四禁→M4 四检→M4.5 七席→E4 参考仪→F-082 登记。**供给面修正注记=R810 供给侧五面盘点遗漏 DIGEST '
         '通道**（最后消费 R682 v10=09-29 11:21 云端 token 令·此后产品优先令 13:0x 落账=E-pool『新令级事件』路径在池满期'
         '〔LC 拆条 E1-E21+稿集 E22-E26 在产〕未被评估为 DIGEST 候选·R810 四路复活判据按『新事件』口径漏『未消费存量』面'
         '——本件=通道重开首件·判据=R379 §5 编年史 A 级事件+数字密度双过·非造活凑数）]**')

out = []
inserted = False
for l in lines:
    if not inserted and l.startswith('66. '):
        out.append(claim)
        out.append('')
        inserted = True
    out.append(l)
assert inserted, 'anchor line "66. " not found'
io.open(p, 'w', encoding='utf-8', newline='').write(nl.join(out))
print('CLAIM-OK')
