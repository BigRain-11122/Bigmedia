import json, os, re, shutil
from datetime import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

now = datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")
ts_min = now.strftime("%H:%M") + "x"

LOG_LINE = (
    "2026-10-03 {tsm} R1054: declared-idle 声明轮（空轮判定路径④·五静+探针基线平+四查尽·声明轮并窗第五轮=R1053 后 5/6·零 commit 盘面即真相·os-protocol §6 窗满 6 轮/跨日边界/任一异常/实活轮出现即收）——"
    "①轮首五查静（r1035_scan.py fresh 实跑：orders 42 件顶=O-20260928-1910 零新令〔mtime 09-28 19:12 未动〕/ledger @BigStream 30 行零新派工行〔尾部两行=P-2026-09-29-13+09-27 值守轮皆旧锚·r1035_scan.txt 证据〕/decisions dnum 内容寻址差集 NONE=水位 131 维持〔D-20260930-19 水位差集制·D-13 SLA 无触发〕+派工通告板零新涉司行〔D-20261003-01~04=R1031 全收讫态〕/无 index.lock 实测 False/production=open 自愈核 tick1053/日报 10-03 在案〔R1030 补产·一份为真相〕·10-04 日报缺=日界件/W40 周审在案〔R576〕/GB 闸 10-08 非到期〔§④ 最近刷新=10-01 v1.1〕/OH-20261002 窗 3 切片义务满·窗 4=10-05 21:40 未开/树态=M state.json+M .c3-tmp 探针输出+?? r1050-1053/r1035 证据件=并窗自记账预期态零 bm-a 迹象）；"
    "②**R1049 根因注执法=queue 常态项独立复核**（r1035_qhead.py fresh 实跑 r1035_qhead.txt：§A A1-A5 全 done/§B B3 W40 期 done R1049·W41 期=10-10 周六·B5 账号期门控=保护态豁免面/§C C1-C4 全 done〔C4 常态项=S2/S3 校验位随进链件在役零独立可领项〕/§D P-1 终判毕〔判负留痕〕·W40 提案窗已交/§E E30 DAILY=供给窗等待态〔R1032 全池机核盘点 50 干净行全数 context 门控在案·r1032_pool.txt 承继〕+E31 REACT-v9=10-04 窗时间门控）→四查尽=无可领活·清单空·提案已交·保护态豁免面在案（E30 供给窗/E31 时间闸/CENSUS C-00030 supply-gated/B5 账号期/SC-003 素材窗 blocked）；"
    "③三探针=r1021_probes.py 复用实跑：board 0 FAIL（5 ideas 10 drafts 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE+#17）0 发现/loop_health 3 FAIL+123 WARN 皆在案史实——**account-lag 4 读数定谳**（r1035_lag.py 对账 r1035_lag.txt：beats 尾 18 条与 log 收账 ts 逐条一一对应〔02:07→R1037…05:13:35→R1053〕·10-03 当日 done beats 25 条全对应收账·gap=4=R1033 前历史断洞族净累计〔R651/R666/R689/R712/R871 家族〕非本轮新现〕+2 outage 09-26/09-28 已裁定不重复触发+log-order/heartbeat-gap WARN 级近似分钟叙事卫生不改写；"
    "④产品优先律对位=本轮 0 分位如实记〔纯记账 2 处（state log+export 刷）≤5 ✓·0 分=声明轮盘面即真相非空转判负〔R1031 最后 2 分位实物 F-146 距今 ~5h<24h 判负线〕〕·tokens:local=0（纯脚本探针零本地模型调用·P-54⑤ 计量律如实记）·HQ-FEEDBACK 不写（当日集团层零本司 open 项·D-20261003 批 R1031 全收讫·03:07 夜班点名面零本司项·零膨胀）——"
    "waiting: time-gated+supply-gated lanes held（卡点=10-04 日界 E31 REACT-v9 F-147〔10-04 日报先补产·连续第二窗判负=池扩容呈报〕/#94 记忆 ≤10KB 梳理/10-05 W41 周轮件〔周报+自驱提案窗+CLOUD_LINE 首测〕/OSS 窗 4=10-05 21:40/10-08 GB 刷+E30 解锁窗〔rain/CEO 令日/10-08 复市/Nov+ 寒潮〕均未触发）ETA 2026-10-04 00:00〔最近日界·10-04 窗三件开领·batch close 备触发点〕·声明轮并窗计数=5/6〔R1055=6/6 窗满即 batch close commit 区间 R1050-R1055；跨 10-04 日界即先行收〕"
).format(tsm=ts_min)

TASK = LOG_LINE.split("R1054: ", 1)[1][:60]

sp = os.path.join(ROOT, "src", "os", "state.json")
with open(sp, encoding="utf-8") as f:
    st = json.load(f)
assert st["tick"] == 1053, "unexpected tick %s" % st["tick"]
st["tick"] = 1054
st["ts"] = ts
st["task"] = TASK
st["log"].append(LOG_LINE)
with open(sp, "w", encoding="utf-8") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)

ep = os.path.join(ROOT, "docs", "status-export.json")
with open(ep, encoding="utf-8") as f:
    ex = json.load(f)
ex["export_ts"] = ts
res_row = [
    "1054",
    "2026-10-03 %s R1054: declared-idle 声明轮（空轮判定路径④·五静+探针基线平+四查尽·声明轮并窗第五轮 5/6 零 commit：R1049 根因注执法=queue 常态项独立复核全 gated+account-lag=4 历史断洞族定谳〔10-03 beats↔log 逐条对账零新增〕·waiting 10-04 日界三件 ETA 10-04 00:00）——详见 state.json log R1054 行"
    % ts_min,
]
ex["results"].append(res_row)
ex["live"] = [
    ["当前活：R1054 declared-idle 声明轮（并窗 5/6·全 lane 时间/供给门控维持·queue 常态项复核全 gated·2026-10-03 %s）" % ts_min],
    ["最近实物：DAILY v61 城市日签成品卡 F-146（2026-10-03 00:44·最近 2 分位实物）+渲染器字形覆盖门 ADOPT R1033（01:15·306 全回归绿）+B3-W40 B站热榜结构对标研究件 v1.1（2026-10-03 04:26x·研究件 0 分位如实计）"],
    ["下个里程碑：10-04 窗三件=10-04 日报先补产→E31 REACT-v9 热点窗全链 F-147+#94 记忆 ≤10KB 梳理+10-05 W41 周轮件（周报+自驱提案窗+CLOUD_LINE 首测）——窗 ≤48h（10-04）"],
]
with open(ep, "w", encoding="utf-8") as f:
    json.dump(ex, f, ensure_ascii=False, indent=1)

# move r1035 evidence files to .c3-tmp per declaration-window convention
c3 = os.path.join(ROOT, ".c3-tmp")
moved = []
for name in ["r1035_scan.py", "r1035_scan.txt", "r1035_probe2.py", "r1035_probe2.txt",
             "r1035_qhead.py", "r1035_qhead.txt", "r1035_lag.py", "r1035_lag.txt"]:
    src = os.path.join(ROOT, name)
    if os.path.exists(src):
        shutil.move(src, os.path.join(c3, name))
        moved.append(name)

print("CLOSE OK tick=1054 ts=%s moved=%d" % (ts, len(moved)))
