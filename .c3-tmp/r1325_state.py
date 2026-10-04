# -*- coding: utf-8 -*-
import io, json, datetime

p = r'src\os\state.json'
d = json.load(io.open(p, encoding='utf-8'))
now = datetime.datetime.now()
ts = now.strftime('%Y-%m-%d %H:%M:%S')
hm = now.strftime('%H:%M')[:4] + 'x'  # approximate-minute house style

log_line = (
    u"2026-10-05 %s R1325: declared-idle 一行声明收轮（空轮判定·五查静+探针基线平+四查尽·"
    u"P-2026-09-28-02 ②④序·声明窗 3/6=R1323/R1324 同窗续轮）——①五查 fresh 实证 .c3-tmp/r1325_check.txt "
    u"06:53（orders 顶=O-20260928-1910 未变 mtime 09-28 19:12/ledger @target 43==43 锚静〔mtime 10-05 "
    u"03:15 承继值守轮盘面行非匹配面·canonical 计数 43==43·CI_EXTRAS 1 伪差行承继 R1286 定谳〕/decisions "
    u"dnums 142==142 NEW=[] mtime 10-05 00:16 零漂移〔D-20260930-19 水位差集制〕·BS rows 47==47 持平"
    u"〔R1300 消费后基线〕/派工通告板零 BigStream 涉司新行/零 index.lock/production=open/树态=M state.json"
    u"+?? r1323*~r1325* 探针件=声明窗自记账预期态零 bm-a 活跃写盘迹象·LAST_COMMIT=8418b9e8 R1322 生产轮）；"
    u"②三探针照跑不省（r1325_check.py=r1324 同型复制独立 OUT 卫生律〔R1244/R1288 编码律·R1311〕：board "
    u"0 FAIL〔5 题 10 稿 5 in production〕/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17〕"
    u"0 发现·阻塞≠失败口径/loop_health 3 FAIL+138 WARN==R1324 基线持平零新增〔两 outage 09-26/09-28 已"
    u"裁定案史足迹不重复触发+account-lag done1330>tick1324=+6 在轮 beat 瞬态残差 R981/R1054 定谳族·"
    u"tick1325 收账后口径自平·heartbeat-gap WARN 皆在案史实长轮间隙合法〕）；③四查尽承 R1323/R1324 同窗"
    u"定谳禁重扫（距 R1324 06:46 机证 ~7 分钟零新事实·供给面 gate facts 与 R1324 逐项持平：post-v67 "
    u"weekend 面=烟火/13 门控行单行=日间窗面枯竭〔r1325 机证 YANHUO_WEEKEND_13「市场买卖讲价」在位·"
    u"10-08 复市解锁·R1322 供给诚实注承继〕+夜面双归零承继〔R1124/R1305〕+pools 1440==1440 QUIET"
    u"〔mtime 06:06 BigLife 重存零对话增量〕/interchat 22==22 QUIET/novel ch3+ v4 文本 0 件〔音频线 "
    u"bm-a 稿源门控维持〕/CENSUS C-00030 锚 absent supply-gated 维持/DIGEST 池空〔dnums NEW=[]+"
    u"ledger 43==43 零新 CEO 令级事件〕/OSS w4 21:40 时闸未开〔OH-20261005 未建=开窗后新建正常态〕+"
    u"REACT-v9 10-06 日闸〔10-05 窗已 R1299 判负第三窗不重扫·10-06 日报先补产〕+#57 10-07 治理日终报"
    u"〔R1307 prep 已毕·W41 整周读数窗未满不前拉=造活凑数禁〕+GB 闸 10-08 非到期〔§④ 最近刷新=10-01〕"
    u"+B3 W41 期=10-10·提案轨=P-2 已交 pilot-live 判据③观察窗至 11-04·W42 提案窗=10-12 起〕→无可领活="
    u"全 lane 时间闸/供给闸/CEO 闸·保护态豁免面在案（供给门控/时间闸/CEO 物理件三族·结构性满载≠闲置·"
    u"P-2026-09-28-02 ③）；④例行件全静（日报 10-05 在案不重跑〔R1299 00:00:09 一份为真相〕·10-06 "
    u"MISSING=10-06 日界批补产预指〔REACT-v9 前置〕/W41 周审在案〔R1301〕/HQ_ACK F-20261004-01 "
    u"EXISTS）·export 不刷（export_ts 06:23:20 <24h 无实况变化遵 F3 律·live 三行=F-154 实况 fresh "
    u"核对·声明轮非实况变化）·HQ-FEEDBACK 不写（当日集团层零本司 open 项零膨胀·D-20261005-01~05 已 "
    u"R1300 回执）·tokens:local=0（探针纯脚本+会话验读零本地模型调用·P-54⑤ 计量律·云计费=0）·24h "
    u"判负钟口径=严口径最后 2 分实物 F-154 10-05 06:19:26→判负钟窗 10-06 06:19·今晚 OSS w4 首切片窗内"
    u"先破合法（宽口径 R1322 06:24 生产 commit 起算）——waiting: 全 lane 时间闸至 OSS 窗 4 开窗（10-05 "
    u"21:40 后首切片=OH-20261005 台账件新建+收益透镜 3 型标注首用 P-20260926-08+P-2026-10-04-02→"
    u"10-06 日界批〔10-06 日报补产→E31 REACT-v9 择优 F-155 预指位〕→10-07 #57 替代率首报终报一命令"
    u"复跑定稿→10-08 GB 闸/复市 DAILY 烟火/13 门控行）ETA 2026-10-05 21:40（当前 06:5x）·next=R1326 "
    u"声明窗 4/6（异常即转全任务书·实活窗=今晚 21:40 OSS w4）·本窗 3/6 无 commit（并窗律 os-protocol "
    u"§6：6/6 窗满/跨日/异常/实活轮出现即收·r1323~r1325 证据件随窗满卷入）"
) % hm

d['tick'] = 1325
d['log'].append(log_line)
d['ts'] = ts
body = log_line[len('2026-10-05 %s ' % hm):]
d['task'] = body[:60]
# focus refresh (next-round pointer face)
d['focus'] = (u"R1325 declared-idle 声明窗 3/6（五查静+探针基线平·全 lane 时间闸：post-v67 日间窗面枯竭"
              u"〔烟火/13=10-08 复市门控〕·夜面双归零）——下轮可领序：①OSS 窗 4 首切片（10-05 21:40 后·"
              u"OH-20261005 台账件新建+收益透镜 3 型标注首用 P-20260926-08+P-2026-10-04-02）②REACT-v9 "
              u"10-06 窗（10-06 日报先补产·择优 F-155 预指位）③10-07 #57 替代率首报终报一命令复跑定稿 "
              u"④10-08 GB 闸/复市 DAILY（烟火/13 门控行）·P-2 判据③观察窗至 11-04·异常即转全任务书")
json.dump(d, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# verify reload
v = json.load(io.open(p, encoding='utf-8'))
out = []
out.append('tick=%s ts=%s' % (v['tick'], v['ts']))
out.append('task=%s' % v['task'])
out.append('log_len=%d last_line_head=%s' % (len(v['log']), v['log'][-1][:80]))
out.append('production=%s focus_head=%s' % (v['production'], v['focus'][:60]))
io.open(r'.c3-tmp\r1325_state_verify.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('state updated: tick=%s ts=%s' % (d['tick'], ts))
print('task:', d['task'])
