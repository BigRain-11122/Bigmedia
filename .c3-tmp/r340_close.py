# -*- coding: utf-8 -*-
# R340 idle-fast close: state.json (tick/log/ts/task) + status-export.json (P-61)
import json, re, datetime

now = datetime.datetime.now()
ts_full = now.strftime('%Y-%m-%d %H:%M:%S')
ts_min = now.strftime('%H:%M')

entry = (
    "2026-09-26 " + ts_min + " R340: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 3/6 不 commit）——"
    "①无新令（orders 顶=O-20260925-1931-HQ-C·R283 已记账）"
    "②backlog 顶行不可认领（#63 图鉴续件 C-00030 锚正典位轮首核=仍不在位〔python os.path.exists False+C-00031 同核 False 实证·anchors 20 止 C-00029〕supply-gated 维持·"
    "#59 REACT 当日映射余量耗尽 R314 判定同日维持〔新热点窗=09-27 日报〕·#57 替代率首报 10-07 窗挂账·#21 周日立法件 09-27 届日未到〔明日周日届日=下轮首查〕·"
    "自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕）"
    "③树态=仅自产预期件（M state.json+M status-export.json=R338/R339 idle-fast 并窗自记账预期态·os-protocol §6·?? .c3-tmp/r338_close.py+r339_close.py+r340_check.py=自产脚本件随窗满批 commit·无 index.lock 实证·HEAD=b7aba8b）"
    "④ch.5 v3 稿未落（novel 实证止 SC-001-04-v3 09-25 17:58+SC-001-05-v1·audio/comic 同核 09-26 零新写盘·bm-a 面）·日报 2026-09-26 在案不重跑（Test-Path True）·W39 周审在案；"
    "集团双锚静=ledger 行含 @ 四模式 21=锚零新转办（python 计数 21 实证）·decisions python 非空行 33=锚〔尾=D-20260926-04〕零新行零动作；"
    "三探针全绿（board 0 FAIL 5 题 10 稿 5 in production exit 0/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1/loop_health 0 FAIL 19 WARN 皆在案史实〔12 log-order+7 heartbeat-gap〕·tick339=done339 对账平）；"
    "例行件=global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·"
    "tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）——"
    "一行收账即出（idle-fast 并窗轮 3/6·本轮不 commit·P-61 导出步照刷 export_ts）。"
    "下轮快速路径首查：#21 周日立法件（09-27 届日即领·周日周轮立法流程）/REACT 09-27 日报热点窗届日即领/图鉴 C-00030 锚/ch.5 v3 稿落迹象/新令/集团转办——"
    "全静即 idle-fast（窗满 6 轮/跨日/异常/实活轮出现才收账 commit）。"
)

prefix_re = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2} R\d+: ')
task = prefix_re.sub('', entry, count=1)[:60]

# ---- state.json (CRLF-preserving text edit, R322 lesson) ----
sp = r'src\os\state.json'
raw = open(sp, encoding='utf-8', newline='').read()
NL = '\r\n' if '\r\n' in raw else '\n'
assert raw.count(NL + ' ],') == 1, 'log array close pattern not unique'
assert '"tick": 339' in raw, 'tick anchor missing'
quoted = json.dumps(entry, ensure_ascii=False)
new = raw.replace(NL + ' ],', ',' + NL + '  ' + quoted + NL + ' ],', 1)
new = new.replace('"tick": 339', '"tick": 340', 1)
new = re.sub(r'"ts": "[^"]*"', '"ts": ' + json.dumps(ts_full, ensure_ascii=False), new, count=1)
new = re.sub(r'"task": "[^"]*"', '"task": ' + json.dumps(task, ensure_ascii=False), new, count=1)
json.loads(new)  # validate before write
assert '"tick": 340' in new and 'R340' in new
open(sp, 'w', encoding='utf-8', newline='').write(new)
json.loads(open(sp, encoding='utf-8').read())
print('state.json OK tick=340 ts=' + ts_full)
print('task=' + task)

# ---- status-export.json (P-61, full regenerate) ----
ep = r'docs\status-export.json'
se = json.load(open(ep, encoding='utf-8'))
se['export_ts'] = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
dept_t = ("OS 循环 R340（idle-fast·五静+探针绿——产线全 supply-gated 维持：图鉴 C-00030 锚正典位仍不在位〔anchors 20 止 C-00029〕"
          "+REACT 当日映射余量耗尽〔R314 判定·新热点窗=09-27 日报〕+ch.5 v3 稿未落〔bm-a〕+#57 10-07 窗+#21 周日件届日未到·"
          "自进池 open 真锚项全闭=idle-fast 一行收账〔并窗轮 3/6 不 commit〕）·state.ts/task 心跳面刷新")
for d in se['depts']:
    if d['n'] == '工程技术部':
        d['t'] = dept_t
outs_t = ("tick 340·R340（idle-fast·五静+探针绿——产线全 supply-gated 维持〔图鉴 C-00030 锚正典位轮首核仍不在位 anchors 20 止 C-00029·"
          "供给门只查 census/anchors/ 正典位+REACT 当日映射余量耗尽维持 R314 判定·新热点窗=09-27 日报+ch.5 v3 稿未落 bm-a 面"
          "+#57 10-07 窗挂账+#21 周日件届日未到〕·自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控"
          "+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕：①五查静=无新令〔orders 顶=O-1931 R283 已记账〕"
          "+集团双锚静〔ledger 行含 @ 四模式 21=锚零新转办·decisions python 非空行 33=锚零新行〕+树态=仅自产预期件〔M state.json+M status-export=R338/R339 并窗自记账预期态〕"
          "②三探针全绿=board 0 FAIL 5 题 10 稿 5 in production/readiness 3 阻塞皆外部 CEO 面 0 发现/"
          "loop_health 0 FAIL 19 WARN 皆在案史实·tick339=done339 对账平③并窗轮 3/6 不 commit〔os-protocol §6 并窗律〕"
          "+P-61 导出步刷 export_ts）")
assert se['outs'][0][0] == 'OS 循环'
se['outs'][0][2] = outs_t
assert se['results'][0][1] == 'OS 轮次'
assert se['results'][0][0] == '339'
se['results'][0][0] = '340'
open(ep, 'w', encoding='utf-8', newline='\n').write(json.dumps(se, ensure_ascii=False, indent=1) + '\n')
json.loads(open(ep, encoding='utf-8').read())
print('status-export.json OK export_ts=' + se['export_ts'])
