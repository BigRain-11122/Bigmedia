# -*- coding: utf-8 -*-
"""R234 idle-fast closeout: state.json tick/log/focus + docs/status-export.json refresh.
Window 3/6 -> NO commit per os-protocol sec.6 batch rule (R232-start window, same day, no anomaly)."""
import json, io
from datetime import datetime

now = datetime.now()
stamp = now.strftime('%Y-%m-%d %H:%M')
export_ts = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')

# --- state.json ---
p = 'src/os/state.json'
d = json.load(io.open(p, encoding='utf-8'))
assert d['tick'] == 233, 'tick drifted: %s' % d['tick']
d['tick'] = 234

line = (
    stamp + " R234: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 3/6）——"
    "①无新令（orders 顶=O-20260925-0850 R222 已记账）"
    "②backlog 顶行不可认领（#27 ①②③ 全毕·④发布锁内挂账·ch.6 网文稿未落=novel 目录实证 ch.1-05〔bm-a 稿落即随轮认领〕"
    "·BS-005/bs005e 双 blocked 待素材窗·#15 随量产逐件·#21 周日周轮自领·#17 needs-CEO"
    "·#14 done 复核=R197 wrapper PID 58052 R204 已回读 9/10 PASS 闭环零悬尾）"
    "③树净零锁（仅自产 tmp·M state.json/status-export.json=R232/R233 idle 累积预期态）"
    "④bm-a 写盘迹象核=零（state mtime 10:53=R233 收账后零动·漫画止 ep.2〔comic 目录实证·ep.3 未现〕）"
    "·素材窗迹象核=7 窗枚举零 Biggame 总控窗（Tuanjie 态=Unity Error+UGit+Cowork·R193-R233 定谳线维持→BS-005/bs005e 双 blocked 维持）"
    "⑤集团扫描=ledger 严格行含 @ 四模式 14 行=锚零新转办·decisions UTF8 非空行 24=锚零新行零动作；"
    "三探针=board 0 FAIL（5 题 10 稿 5 in production·exit 0）"
    "/readiness exit 1=3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+2 发现（bs-005/bs005e render-unannot=blocked 在链预期红维持·阻塞≠失败口）"
    "/loop_health 0 FAIL 17 WARN（在案史实+新 2=log-order 叙事分钟近似 R230/R231 同型·非操作红）；"
    "例行件=日报 0925+W39 周审在案不重跑·global-benchmarks day2 ≤7 跳过（下次 ~10-01）"
    "·P1 催办=已裁项停用无超线项·HQ-FEEDBACK 不写（无集团层新 open 问题·零膨胀）"
    "·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）；"
    "idle 并窗=3/6 不 commit（并窗律：窗满 6 轮/跨日/异常/实活即收账）；"
    "下轮 R235 首查=orders 顶/素材窗迹象/ch.6 网文稿落盘迹象（先/新令/集团转办），全静即 idle-fast（4/6）。"
)
d['log'].append(line)

d['focus'] = (
    "R235: ①快速路径五查（素材窗迹象优先：新令/ledger 严格行含 @ 前缀锚 14/decisions UTF8 非空行锚 24/树态/bm-a 写盘迹象）"
    "②生产线=BS-005 原版+bs005e 双 blocked 维持（共享开窗实录批·素材窗一开即续链：对位表重构→重渲→S2 复跑→E8→M4→登记〔bs005e=F-007 预留位·BS-005 原版=编号顺延〕）"
    "③#27 ①有声线=ch.6 网文稿待 bm-a 落盘（cta 周浩宇/陈雅雯双钩已埋·稿落即新连载节律随轮认领）+②③ bm-a 进度复核（网文 ch.6 待落·漫画 ep.3 待见）"
    "④例行=探针三件套照跑（readiness 预期=bs-005/bs005e 双 render-unannot blocked 在链预期红维持）"
    "⑤idle-fast 并窗计数=3/6（R232 起计·窗满 6 轮/跨日/异常/实活即收账）"
)
io.open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2))

# --- status-export.json (P-61 export step: export_ts mandatory, depts/outs/results derived) ---
q = 'docs/status-export.json'
e = json.load(io.open(q, encoding='utf-8'))
e['export_ts'] = export_ts
for dept in e['depts']:
    if dept['n'] == '工程技术部':
        dept['t'] = (
            "OS 循环 idle-fast R234（快速路径五静+探针绿·不进开轮四步·并窗 3/6："
            "素材窗 7 窗枚举零 Biggame 总控窗=BS-005/bs005e 双 blocked 维持"
            "·bm-a 复核零新进展〔ch.6 未落/ep.3 未现〕·三探针全绿·集团双锚静〔ledger 14/decisions 24〕）"
        )
for row in e['outs']:
    if row[0] == 'OS 循环':
        row[2] = (
            "tick 234·R234（idle-fast 五静+探针绿：素材窗零 Biggame 总控窗=BS-005/bs005e 双 blocked 维持"
            "·bm-a 复核零新进展〔网文 ch.6 未落/漫画 ep.3 未现〕·三探针全绿·集团双锚静）"
        )
for row in e['results']:
    if row[1] == 'OS 轮次':
        row[0] = '234'
io.open(q, 'w', encoding='utf-8').write(json.dumps(e, ensure_ascii=False, indent=2))

print('closed tick=234 log_len=%d export_ts=%s' % (len(d['log']), export_ts))
