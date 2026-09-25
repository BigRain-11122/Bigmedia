# -*- coding: utf-8 -*-
# R335 idle-fast accounting: state.json tick/log/ts/task + status-export.json P-61 refresh
import json, io, datetime

def load(p):
    raw = io.open(p, encoding='utf-8').read()
    return raw, json.loads(raw)

def save(p, obj, crlf):
    txt = json.dumps(obj, ensure_ascii=False, indent=1)
    if crlf:
        txt = txt.replace('\n', '\r\n')
    io.open(p, 'w', encoding='utf-8', newline='').write(txt)

p1 = r'src\os\state.json'
raw1, st = load(p1)
assert st['tick'] == 334, 'unexpected tick: %s' % st['tick']
now = datetime.datetime.now()
ts = now.strftime('%Y-%m-%d %H:%M:%S')
hhmm = now.strftime('%H:%M')

content = ("idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 4/6 不 commit）——"
"①无新令（orders 顶=O-20260925-1931-HQ-C·R283 已记账）"
"②backlog 顶行不可认领（#63 图鉴续件 C-00030 锚正典位轮首核=仍不在位〔Test-Path False+C-00031 同核 False 实证·anchors 止 C-00029〕supply-gated 维持·"
"#59 REACT 当日映射余量耗尽 R314 判定同日维持〔新热点窗=09-27 日报〕·#57 替代率首报 10-07 窗挂账·#21 周日立法件 09-27 届日未到·"
"自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕）"
"③树净零锁（HEAD=49e8375 R326-R331 batch·仅 M state.json+M status-export=R332-R334 idle-fast 并窗自记账预期态非 bm-a 迹象·无 index.lock Test-Path 实证）"
"④ch.5 v3 稿未落（novel 实证止 SC-001-04-v3+SC-001-05-v1·ch.6 未现·bm-a 面 09-26 零新写盘）·日报 2026-09-26 在案不重跑（Test-Path True）·W39 周审在案；"
"集团双锚静=ledger 行含 @ 四模式 21=锚零新转办·decisions python 非空行 33=锚〔尾=D-20260926-04〕零新行零动作；"
"三探针全绿（board 0 FAIL 5 题 10 稿 5 in production exit 0/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1/"
"loop_health 0 FAIL 19 WARN 皆在案史实〔12 log-order+7 heartbeat-gap〕·tick334=done334 对账平）；"
"例行件=global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·"
"tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）——"
"一行收账即出（idle-fast 并窗轮 4/6·本轮不 commit·P-61 导出步照刷 export_ts）。"
"下轮快速路径首查：图鉴 C-00030 锚/REACT 09-27 日报热点窗届日即领/ch.5 v3 稿落迹象/#21 周日立法件（09-27 届日即领·周日周轮立法流程）/新令/集团转办——"
"全静即 idle-fast（窗满 6 轮/跨日/异常/实活轮出现才收账 commit）。")

logline = "2026-09-26 %s R335: %s" % (hhmm, content)
st['tick'] = 335
st['log'].append(logline)
st['ts'] = ts
st['task'] = content[:60]
save(p1, st, '\r\n' in raw1)

p2 = r'docs\status-export.json'
raw2, se = load(p2)
se['export_ts'] = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
for d in se['depts']:
    if d.get('n') == '工程技术部':
        d['t'] = d['t'].replace('OS 循环 R334（idle-fast', 'OS 循环 R335（idle-fast').replace('并窗轮 3/6', '并窗轮 4/6')
for o in se['outs']:
    if o[0] == 'OS 循环':
        o[2] = o[2].replace('tick 334·R334（idle-fast', 'tick 335·R335（idle-fast').replace('tick333=done333', 'tick334=done334').replace('并窗轮 3/6', '并窗轮 4/6')
for r in se['results']:
    if r[1] == 'OS 轮次':
        r[0] = '335'
save(p2, se, '\r\n' in raw2)

for p in (p1, p2):
    json.loads(io.open(p, encoding='utf-8').read())
print('OK tick=335 ts=%s export_ts=%s task=%r' % (ts, se['export_ts'], st['task']))
