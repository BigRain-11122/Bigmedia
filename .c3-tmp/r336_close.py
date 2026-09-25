# -*- coding: utf-8 -*-
# R336 idle-fast accounting: state.json tick/log/ts/task + status-export.json P-61 refresh
# (same-pattern successor of r335_close.py; adds pre-replace assertions for drift detection)
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
assert st['tick'] == 335, 'unexpected tick: %s' % st['tick']
now = datetime.datetime.now()
ts = now.strftime('%Y-%m-%d %H:%M:%S')
hhmm = now.strftime('%H:%M')

content = ("idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 5/6 不 commit）——"
"①无新令（orders 顶=O-20260925-1931-HQ-C·R283 已记账）"
"②backlog 顶行不可认领（#63 图鉴续件 C-00030 锚正典位轮首核=仍不在位〔Test-Path False+C-00031 同核 False 实证·anchors 止 C-00029〕supply-gated 维持·"
"#59 REACT 当日映射余量耗尽 R314 判定同日维持〔新热点窗=09-27 日报〕·#57 替代率首报 10-07 窗挂账·#21 周日立法件 09-27 届日未到〔明日周日届日=下轮起首查〕·"
"自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕）"
"③树净零锁（HEAD=49e8375 R326-R331 batch·仅 M state.json+M status-export=R332-R335 idle-fast 并窗自记账预期态+?? .c3-tmp/r335_close.py=R335 自产收账脚本件〔mtime 05:13:27=收账 ts 05:13:30 对位·断言 tick334 写335 全对位核实=自产件非 bm-a 迹象〕随窗满批收账·无 index.lock Test-Path 实证）"
"④ch.5 v3 稿未落（novel 实证止 SC-001-04-v3+SC-001-05-v1·ch.6 未现·bm-a 面 09-26 零新写盘）·日报 2026-09-26 在案不重跑（Test-Path True）·W39 周审在案；"
"集团双锚静=ledger 行含 @ 四模式 21=锚零新转办（rg 四模式计数 21=锚实证）·decisions python 非空行 33=锚〔尾=D-20260926-04〕零新行零动作；"
"三探针全绿（board 0 FAIL 5 题 10 稿 5 in production exit 0/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1/"
"loop_health 0 FAIL 19 WARN 皆在案史实〔12 log-order+7 heartbeat-gap〕·tick335=done335 对账平）；"
"例行件=global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·"
"tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）——"
"一行收账即出（idle-fast 并窗轮 5/6·本轮不 commit·P-61 导出步照刷 export_ts·r336_close.py=同型自产脚本件与 r335_close.py 同随窗满批 commit）。"
"下轮快速路径首查：R337=并窗窗满 6 轮收账 commit（区间消息注明 R332-R337 idle-fast batch）+#21 周日立法件届日（09-27 周日=届日即领·周日周轮立法流程）/"
"图鉴 C-00030 锚/REACT 09-27 日报热点窗届日即领/ch.5 v3 稿落迹象/新令/集团转办——异常或实活轮出现即提前收账。")

logline = "2026-09-26 %s R336: %s" % (hhmm, content)
st['tick'] = 336
st['log'].append(logline)
st['ts'] = ts
st['task'] = content[:60]
save(p1, st, '\r\n' in raw1)

p2 = r'docs\status-export.json'
raw2, se = load(p2)
se['export_ts'] = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')

hits_t = 0
for d in se['depts']:
    if d.get('n') == '工程技术部':
        assert 'OS 循环 R335（idle-fast' in d['t'] and '并窗轮 4/6' in d['t'], 'dept t drift: %r' % d['t']
        d['t'] = d['t'].replace('OS 循环 R335（idle-fast', 'OS 循环 R336（idle-fast').replace('并窗轮 4/6', '并窗轮 5/6')
        hits_t += 1
assert hits_t == 1, 'dept hits: %d' % hits_t

hits_o = 0
for o in se['outs']:
    if o[0] == 'OS 循环':
        assert 'tick 335·R335（idle-fast' in o[2] and 'tick334=done334' in o[2] and '并窗轮 4/6' in o[2], 'out drift: %r' % o[2]
        o[2] = o[2].replace('tick 335·R335（idle-fast', 'tick 336·R336（idle-fast').replace('tick334=done334', 'tick335=done335').replace('并窗轮 4/6', '并窗轮 5/6')
        hits_o += 1
assert hits_o == 1, 'out hits: %d' % hits_o

hits_r = 0
for r in se['results']:
    if r[1] == 'OS 轮次':
        assert r[0] == '335', 'result drift: %r' % r
        r[0] = '336'
        hits_r += 1
assert hits_r == 1, 'result hits: %d' % hits_r

save(p2, se, '\r\n' in raw2)

# post-write validation
v1 = json.loads(io.open(p1, encoding='utf-8').read())
v2 = json.loads(io.open(p2, encoding='utf-8').read())
assert v1['tick'] == 336 and 'R336' in v1['log'][-1] and v1['ts'] == ts
assert v2['export_ts'] == now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
print('OK tick=336 ts=%s export_ts=%s loglen=%d' % (ts, v2['export_ts'], len(v1['log'])))
