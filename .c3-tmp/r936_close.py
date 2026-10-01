import json, io, datetime

p = 'src/os/state.json'
st = json.load(io.open(p, encoding='utf-8'))
assert st.get('production') == 'open', 'production self-heal check'
assert st['tick'] == 935, 'unexpected tick: %s' % st['tick']
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
hhmm = now[11:16]

logline = (
    "2026-10-02 " + hhmm + " R936: 等待态声明收轮·声明轮并窗第 6/6 轮=窗满即收（R935 04:35 同判承接·五查静核=轻量 mtime 证实链承接〔禁重扫同一等待对象=产品优先律 2〕："
    "evolution-ledger mtime 10-02 03:17:36==R928 全量扫描时点未动=ledger 46 基线带内维持〔task-modes 41+machine-modes 5·last_p=10-01·R845 re-baseline 承接〕/"
    "decisions mtime 10-02 00:06:16 未动=dnum 差集 NONE=120 基线维持〔R935 04:35 r910_open.py 全文正则集合差集 new=0 承接·D-20260930-19 水位差集制·D-13 SLA 无触发·派工通告板涉司行全收讫态维持〕/"
    "orders 顶=O-20260928-1910=锚静零新令〔本轮实测 mtime 顺位头〕/无 index.lock 实测〔04:42〕/"
    "CENSUS C-00030 present: False=供给闸闭〔本轮新鲜实核：anchors 目录直读锚顶=C-00029.md·C-00030+ 计数=0·dir mtime 09-24 00:06:50 未动=R934/R935 承接读数升级实核〕/"
    "production=open 自愈核在位 tick935〔pre-close〕·"
    "树态=M CODELY.md〔09-30 18:55:34 R767 平台记忆压缩波定谳零接触·窗收不卷=R918/R924/R930 先例〕+M state.json=并窗自账预期态+自产证据件 r931-r936 批内=零 bm-a 活跃写盘迹象）"
    "+三探针=board 0 FAIL（5 意见/10 草稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次① 未注册+M4 GATE 6/10+#17）0 发现〔72 renders 全注账·阻塞≠失败口径〕/"
    "loop_health 3 FAIL+110 WARN 皆在案史实类〔09-26 49min+09-28 609min 两 outage 已裁定不重复触发+account-lag done938>tick935=启动器在轮 beat 瞬态·tick936 收账自平口径·WARN 计数与 R934/R935 持平零新增〕——"
    "门槛未达四查尽维持〔R935 fresh 同判承接·实核零变化〕：OSS w3=10-02 21:40 未至〔本轮 " + hhmm + "〕·REACT 10-03=日闸〔10-03 日报缺先补产〕·#94 记忆窗=10-04·W41 周轮件=10-05〔周报+自驱提案窗+CLOUD_LINE 首测·W40 提案 P-1 已 pilot-closed 判负留痕在案〕·GB 基准闸=10-08·"
    "backlog 顶行钳位维持（#67/#63/#66③=供给闸·#59 REACT=10-03 日闸·#70=21:40 时闸·#94=10-04·#57 替代率首报=10-07 到期不催·#15=needs-CEO·供给闸/时闸/日闸/CEO 物理件四路外部门槛=保护态豁免面在案非违规闲置〔P-2026-09-28-02 ③〕）"
    "+export R912 00:48:07 在案 24h 窗内不刷（实况无变化·产品优先律 2）+日报 10-02 在案不重跑〔R909 00:00:26 补产·一份为真相〕+HQ-FEEDBACK 无写入（无新增集团级 open 问题·零膨胀）+tokens:local=0（轻量证实+探针=纯脚本机检·P-54⑤ 计量律如实记）"
    "→窗满 6/6（R931-R936）即收=os-protocol §6 并窗律·batch close commit 注区间+push（six waiting rounds zero-product window·五静+探针绿+四查尽全档）·"
    "下轮=R937 起新窗：①OSS w3 切片 10-02 21:40 届窗即领（≥1 切片 ≤3 刀）②10-03 00:00 跨日先到=日界批收+10-03 日报补产+REACT 10-03 领件③#94 ① 10-04 记忆 ≤10KB 梳理窗④W41 周轮件=10-05（周报+自驱提案窗+CLOUD_LINE 首测）"
)

st['tick'] = 936
st['log'].append(logline)
st['ts'] = now
idx = logline.index('R936:')
st['task'] = logline[idx:idx + 60]
st['focus'] = (
    "R936: 等待态声明窗满 6/6 batch close（区间 R931-R936·五静+探针绿+四查尽全档·commit 注区间）——下轮 R937 起新窗："
    "①OSS w3 切片 10-02 21:40 届窗即领（≥1 切片 ≤3 刀）②10-03 00:00 跨日先到=日界批收+10-03 日报补产+REACT 10-03 领件③#94①10-04 记忆梳理④W41=10-05（周报+自驱提案窗+CLOUD_LINE 首测）"
)

with io.open(p, 'w', encoding='utf-8') as f:
    f.write(json.dumps(st, ensure_ascii=False, indent=1) + '\n')

print('R936 batch-closed: tick=%d log_len=%d ts=%s' % (st['tick'], len(st['log']), now))
print('task[:60]=%s' % st['task'])
