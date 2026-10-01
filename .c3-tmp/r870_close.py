# -*- coding: utf-8 -*-
# R870 close: queue E27 entry + export refresh + state.json accounting (tick 869->870)
import io, json, datetime

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

LOG = (
    u'2026-10-01 17:1x R870: 生产轮·供给盲区修正轮=MC-20261001-DIGEST-v11《城市盘点 011·产品优先令数字盘点》'
    u'全链走门毕=F-082 登记+queue §E E27 入池（#67 R870 claim 兑现·产品优先律对位=本轮新实物=DIGEST v11 成品卡入库 2 分位·'
    u'R864-R869 声明窗后首实活轮）——①轮首五查静=r870_scan.py 内容寻址 16:38 留档（orders 42=锚零新令〔顶=O-20260928-1910〕·'
    u'ledger 46=基线带内 r845_regression caught=True·decisions dnum 差集 NONE=117 基线〔D-13 SLA 无触发〕·'
    u'production=open 自愈核 tick869〔pre-close〕·无 index.lock·树态=3 M 成员维持〔CODELY.md R767 定谳+codex 两件 mtime 09-29 04:06 bm-a 让位零接触〕）'
    u'+三探针=board 0 FAIL（5 ideas 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面/loop_health 3 FAIL+105 WARN 皆在案史实类；'
    u'②供给盲区修正定谳=R810 供给侧五面盘点（锚卡/稿集/LC/ideas/REACT 窗）遗漏 DIGEST 通道——最后消费 R682 v10（09-29 11:21）后'
    u'产品优先令 P-2026-09-29-07（09-29 ~13:0x·CEO 直令·ledger 正行在册）在池满期〔LC E1-E21+稿集 E22-E26 在产〕未被评估为 DIGEST 候选·'
    u'R810-R869 四路复活判据按新事件口径漏未消费存量面=等待态声明窗的供给侧盲区·本轮修正=通道重开首件'
    u'（#67 留痕行开板合法面·R379 §5 判据=编年史 A 级事件+数字密度双过·非造活凑数）；'
    u'③全链=史源六指针逐条可机核（ledger 正行 CEO 原话 verbatim 全句+诊断读数 8 仓 7 天 10,524 commit/本司文档簿记 46%'
    u'+iteration_prompt 产品优先律块计分三档 2/1/0·记账帽 ≤5·export 三行窗 ≤48h·24h 全 0 分判负'
    u'+finished F-057~F-081 令后 25 件 40 小时+state R685/R809 时间戳锚）→M0 7/8 A 档（十连母题续+三组反差链+本卡第 26 件自指收束）'
    u'→M1 引文=CEO 原话 verbatim 连续子串零改字跨两行（v5 先例·全句入 source_facts·批评面照录禁软化）'
    u'→M2 em 机核 32 档全行 OK（引文行 28.00em +0.75em·36 档排除·VERT +130px·em-check-r870.txt）+--poster exit 0'
    u'+验图五检 5/5 一次过（「令」字降采样误读全分辨率定谳=2x 裁剪复验）→M3 城市盘点 011 四禁零中→M4 四检过'
    u'（三重标注双落·脱敏分界=治理审计读数 v10 同型·P1 边界=纪实档案）→M4.5 七席 6×9.0+E7 N/A'
    u'（review-20261001-mcdigest-v11.md）→E4 异步在飞（PID 80000·1500s 窗·下轮回填 R682 追加制先例）'
    u'→F-082 登记（成品库第八十二件·L-卡 第四十四件·DIGEST 形态第十一件）；'
    u'④queue §E=E27 入池+E28/E29 备注位（09-30 D-20260930 批 41 决+10-01 D-20261001 批 11 行=v6/v8 决策批先例可承·备货非造活）'
    u'+backlog #67 R870 claim 行落账；⑤例行件=日报 10-01 在案不重跑/GB 闸 10-08/W41 周轮 10-05/'
    u'#70 OSS 窗 3=10-02 21:40/REACT 10-02 热点窗=届日领（10-02 日报缺=先补产 daily_brief）/'
    u'HQ-FEEDBACK 不写〔无集团层新 open 问题〕·tokens:local=1（E4 qwen2.5:14b 在飞记账·本地 Ollama 零 API token·P-54⑤）'
    u'——下轮=R871 可领序：①REACT 10-02 热点窗届日领②#70 OSS 窗 3 切片（10-02 21:40 后开）'
    u'③DIGEST E28/E29 存量候选随轮领④W41 周轮件（10-05）。'
).replace('17:1x', now[11:16])

assert '"' not in LOG and '\\' not in LOG, 'json-unsafe chars in log line'
assert ' R870: ' in LOG

# --- 1) queue E27 entry
q = 'docs/self-improvement-queue.md'
t = io.open(q, encoding='utf-8').read()
nlq = '\r\n' if '\r\n' in t else '\n'
e27 = (
    u'- 2026-10-01: **R870 E27 DIGEST v11 产品优先令盘点=F-082 登记（供给盲区修正轮=R810 五面盘点遗漏 DIGEST 通道重开首件·'
    u'#67 R870 claim·产品优先律对位=2 分位实物）**：史源=ledger P-2026-09-29-07 正行（CEO 直令 verbatim 全句+诊断读数 8 仓 7 天 '
    u'10,524 commit/本司 46%）+iteration_prompt 产品优先律块+finished F-057~F-081 令后 25 件 40 小时链→M0 7/8 A 档'
    u'→M2 32 档 em 机核+验图五检 5/5→M4.5 七席 6×9.0+E7 N/A→E4 异步在飞（PID 80000·下轮回填）'
    u'→F-082（成品库 82 件·L-卡 44 件·DIGEST 11 件）；**E-pool 复活条件更新=R810 四路补第五路：DIGEST 通道未消费存量候选**'
    u'（E28=09-30 D-20260930 集团批 41 决·E29=10-01 D-20261001 集团批 11 行·v6/v8 决策批先例可承·备货位非造活）'
    u'——下轮可领序：REACT 10-02 热点窗届日领（10-02 日报先补产 daily_brief）+#70 OSS 窗 3（10-02 21:40 后开）'
    u'+E28/E29 随轮领+W41 周轮件（10-05）。'
)
if not t.endswith(nlq):
    t += nlq
t += e27 + nlq
io.open(q, 'w', encoding='utf-8', newline='').write(t)
print('QUEUE-OK')

# --- 2) export refresh (live 3 rows + outs OS row + results append + export_ts)
e = 'docs/status-export.json'
d = json.load(io.open(e, encoding='utf-8'))
d['export_ts'] = now
d['live'] = [
    [u'当前活：R870 生产轮·供给盲区修正轮=DIGEST v11《城市盘点 011·产品优先令数字盘点》全链走门毕 F-082 登记（%s）' % now],
    [u'最近实物：data/storylines/cards/MC-20261001-DIGEST-v11/MC-20261001-DIGEST-v11.png（成品卡 F-082·L-卡 第四十四件·DIGEST 形态第十一件·2026-10-01）'],
    [u'下个里程碑：REACT 10-02 热点窗届日领=下一件成品 F-083（10-02 日报缺先补产 daily_brief）+#70 OSS 窗 3 切片（10-02 21:40 后开）——窗 ≤48h'],
]
d['outs'][0] = [
    u'OS 循环',
    u'tick 870，R870 生产轮·供给盲区修正轮=DIGEST v11 产品优先令盘点 F-082 登记'
    u'（R810 供给侧五面盘点遗漏 DIGEST 通道=本轮修正重开首件；E4 参考仪异步在飞下轮回填）。'
    u'下轮=R871 可领序：REACT 10-02 热点窗届日领（10-02 日报先补产）+OSS 窗 3（10-02 21:40）'
    u'+DIGEST E28/E29 存量候选+W41 周轮件（10-05）。真发布=blocked-on-CEO 账号物理件·发布锁=M5 不变',
]
d['results'].append(['870', LOG])
json.dump(d, io.open(e, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('EXPORT-OK')

# --- 3) state.json accounting (tick 869->870, log append, ts/task refresh)
p = 'src/os/state.json'
s = io.open(p, encoding='utf-8').read()
nls = '\r\n' if '\r\n' in s else '\n'
assert s.count('"tick": 869,') == 1, 'tick anchor not unique'
s = s.replace('"tick": 869,', '"tick": 870,', 1)

anchor = '"' + nls + ' ],' + nls + ' "ts": "2026-10-01 16:24:38",'
assert s.count(anchor) == 1, 'log close anchor count=%d' % s.count(anchor)
repl = '",' + nls + '  "' + LOG + '"' + nls + ' ],' + nls + ' "ts": "' + now + '",'
s = s.replace(anchor, repl, 1)

task = LOG.split(' R870: ', 1)[1][:60]
k = s.rfind('"task": "')
assert k != -1, 'task field missing'
v0 = k + len('"task": "')
k2 = s.find('"', v0)
assert k2 != -1, 'task closing quote missing'
rest = s[k2 + 1:]
assert rest.strip() == '}', 'unexpected tail after task: %r' % rest[:30]
new_tail = '"' + nls + '}' + (nls if rest.endswith(nls) else '')
s = s[:v0] + task + new_tail

d2 = json.loads(s)
assert d2['tick'] == 870 and d2['ts'] == now and d2['task'] == task
assert d2['log'][-1].startswith('2026-10-01 17:') and ' R870: ' in d2['log'][-1]
assert len(d2['log']) >= 2 and ' R869: ' in d2['log'][-2]
assert d2['production'] == 'open'
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ACCOUNT-OK tick=870 log_entries=%d ts=%s task_len=%d' % (len(d2['log']), now, len(task)))
