# -*- coding: utf-8 -*-
# R910 close: decision batch consumption (D-20261002-01/02/03) + watermark advance
# + waiting-state declaration round. json.load reload + assertions (R899 lineage).
import io, json, datetime, re

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
SP = ROOT + r'\src\os\state.json'
DEC = r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md'

now = datetime.datetime.now()
stamp = now.strftime('%Y-%m-%d %H:%M:%S')
rmin = now.strftime('%H:%M')

st = json.loads(io.open(SP, 'r', encoding='utf-8-sig').read())

NEW = ['D-20261002-01', 'D-20261002-02', 'D-20261002-03']
for d in NEW:
    assert d not in st['decisions_watermark']['dnums'], d + ' already in watermark'
st['decisions_watermark']['dnums'].extend(NEW)

# board rows recount (content-addressed; between board heading and ledger heading)
dec = io.open(DEC, 'r', encoding='utf-8', errors='replace').read()
ll = dec.splitlines()
i0 = next(i for i, l in enumerate(ll) if l.startswith('## 派工通告板'))
i1 = next(i for i, l in enumerate(ll) if i > i0 and l.startswith('### 台账'))
rows = [l for l in ll[i0 + 1:i1] if l.startswith('|') and not re.match(r'^\|\s*[-:|]+\s*\|$', l) and '决策' not in l.split('|')[1]]
prev_rows = st['decisions_watermark']['board_rows']
st['decisions_watermark']['board_rows'] = len(rows)
st['decisions_watermark']['ts'] = stamp

LOG = (
    u"2026-10-02 " + rmin + u" R910: 收讫+等待态声明收轮·D-20261002 批 3 新行全读判读毕（decisions dnum 差集 117→120 检出 3 新行=D-20261002-01/02/03·r910_scan 00:14 检出→轮内处理=D-13 SLA 窗内·科学判断闸全过审零驳回）——"
    u"①D-20261002-01 回执核销批 13+集团台账冲突标记修复闭口（HQ 即办态）=本司切片 F-20261001-01 行内标注（closed）已核销+⑥注记 D-20260930-19 受单司 ack 判据 BigStream 到位=知悉零新动作；"
    u"②D-20261002-02 车道任务 principal 单源=缺省 principal 全线（S4U 0x80070005 实证放弃·bigmoney 司 48h 回执窗 10-04·CEO 翻案面保留）+③D-20261002-03 饱和引擎修法 ①per-tick 重读+②state CAS 门双采（bigmoney 司 48h 回执窗 10-04）=两行皆他司执行面知悉——派工通告板涉司行复核=D-20261002-02/03 均 BigMoney 行零 BigStream/七司全部行·D-20261002-01 不在板（台账节 HQ 即办）=三行皆非本司执行面零动作项；水位推进 dnums 117→120（内容寻址制·D-20260930-18 禁行数比对）+board_rows " + str(prev_rows) + u"→" + str(len(rows)) + u"；ack 三载体=本行+commit 含 (a)集团行号 (b)本司轮号 (c)下一动作（P-51/D-19 双载体律）；"
    u"②门控面复核维持（禁重扫同一等待对象·产品优先律 2）：REACT 10-02 热点窗已占（F-085·R909）·#70 OSS 窗 3=10-02 21:40 后开（窗 2 配额 R826+R762 双档在案）·CENSUS C-00030 锚缺供给闸闭（scan 实核 anchors 止 C-00029）·#94 记忆梳理=10-04 窗·W41 周轮件=10-05（周报+自驱提案窗+CLOUD_LINE 首测）·E-pool 空池豁免在案（R810 判负留痕定谳）·#86 四腿 supply-gated 维持（a 台词池 1440 两轮筛毕/b 锚池 20 卡收官/c ch6 未落盘/d 计数随 W41）·新令级事件=ledger last_p=10-01 零新 P 行·本批 3 D 行皆他司/HQ 执行面不构成 #67 DIGEST 触发律解锁（反膨胀律照守）=真无活可拉〔P-20260928-02 ②④序·供给侧全闭+全时闸=保护态豁免面在案非违规闲置〕；"
    u"③三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现（账号批次①+6/10 GATE+#17·72 renders 全注账·阻塞≠失败口径）/loop_health 3 FAIL+107 WARN 皆在案史实类（09-26 49min+09-28 609min 两 outage 已裁定不重复触发+account-lag done912>tick909=在轮 beat 瞬态·tick910 收账自平口径）；"
    u"④例行件：export R909 00:0x 刷新在 24h 窗内不刷（产品优先律 2·实况零变化）·日报 10-02 在案不重跑（R909 00:00:26 补产·一份为真相）·W40 周审在案·GB 闸 10-08（R798 v1.2·scan 头行 10-01 非到期）·T1 催办已裁项停用·HQ-FEEDBACK 不写（3 新行皆他司执行面零本司待决·零膨胀）·tokens:local=0（扫描+探针=纯脚本机检·P-54⑤ 计量律如实记）——waiting: supply-gated lane held（卡点=新锚卡 C-00030+/OSS w3 10-02 21:40/#94 10-04/W41 10-05，ETA 2026-10-02 21:40）。收账显式列文件 commit+push。"
)
st['log'].append(LOG)
st['tick'] = st['tick'] + 1
st['ts'] = stamp
st['task'] = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2} R910: ', '', LOG)[:60]

io.open(SP, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=1))

# reload + assertions (R899 root-fix clause: write-then-verify)
st2 = json.loads(io.open(SP, 'r', encoding='utf-8-sig').read())
assert st2['tick'] == 910, 'tick'
assert st2['log'][-1].startswith('2026-10-02 '), 'log line head'
assert all(d in st2['decisions_watermark']['dnums'] for d in NEW), 'watermark'
assert 'D-20261002-01' in st2['task'] or 'R910' in st2['task'], 'task field'
print('OK tick=%d board_rows=%d->%d dnums=%d log=%d ts=%s' % (
    st2['tick'], prev_rows, st2['decisions_watermark']['board_rows'],
    len(st2['decisions_watermark']['dnums']), len(st2['log']), st2['ts']))
