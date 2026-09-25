# r232_close.py - idle-fast R232 close: state.json tick/log/focus + status-export refresh
# (P-61 export step; batch-window round 1/6, no commit per os-protocol S6)
import json, io, datetime, os

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
now = datetime.datetime.now()
hhmm = now.strftime('%H:%M')
iso = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')

loop_txt = io.open(os.path.join(ROOT, r'.bs005-tmp\probe-r232-loop.txt'), encoding='utf-8').read()
warns = loop_txt.count('[WARN]')
fails = loop_txt.count('[FAIL]')
assert fails == 0, 'loop_health FAIL nonzero: %d' % fails

log_line = (
    f"2026-09-25 {hhmm} R232: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 1/6）——"
    "①无新令（orders 顶=O-0850 R222 已记账）"
    "②backlog 顶行不可认领（#27 ①②③ 全毕·④发布锁内挂账·ch.6 网文稿未落=bm-a 面随轮认领·BS-005/bs005e 双 blocked 待素材窗·#15 随量产逐件·#17 needs-CEO·#21 周日件今周五不到）"
    "③树态=仅自产 tmp（.bs005-tmp/.bs005e-tmp 批闭收账惯例维持）+并窗自记账预期态·无 index.lock·无 bm-a 活跃写盘迹象"
    "④素材窗迹象核=窗口枚举 8 窗零 Biggame 总控窗（Tuanjie 态=Unity Error+Cowork+HMI Version Control+豆包/Lovart/UGit/tbAgent·R193-R231 定谳线维持）→BS-005/bs005e 双 blocked 维持"
    "·②③ bm-a 复核=盘上实证零新进展（网文止 ch.5·ch.6 未落/漫画止 ep.2·ep.3 未现）"
    "·自进清单真锚核=清单文件零变化（mtime 06:17=R206 自产写·R207-R221 判据全维持：A 池 A1-A5 全 done+B2/B4 素材生成线 P1 门后+B3 周一件不到+B5 账号期站内采样 blocked+C3 拣式已定档无新 FAIL 锚+C4 S1 v1.5 三连 10/10 无新旗锚+C1 集成腿无下批件在队=无可领真锚项·不凑工作量造活）；"
    "例行件=日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks 更新记录 2026-09-24 day1 ≤7 天跳过刷新（下期 ~10-01）·T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）；"
    "集团扫描=ledger 严格行含 @ 四模式 14 行=锚零新转办（首扫误用行首 @ 过滤得 0 行=R163/R216 同型操作红·行含口径重扫定谳）·decisions UTF8 非空行 24=锚零新行零动作；"
    "三探针全绿=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+2 发现=bs-005/bs-005e render-unannot blocked 在链预期红维持·F-005/F-007 登记即清·阻塞≠失败口径 exit 1"
    f"/loop_health 0 FAIL {warns} WARN 皆在案史实（tick231=done231 对账平·beats235 含 skip4·log 239 条·backlog 28 项 23 done 82% 燃尽）"
    "——一行收账即出（本轮不 commit·并窗轮 1/6·P-61 导出步照刷 export_ts+实况派生轻量）。下轮=R233 快速路径首查（素材窗迹象优先/新令/集团转办），全静即 idle-fast（2/6）。"
)

new_focus = (
    "R233: ①快速路径五查（素材窗迹象优先：新令/ledger 严格行含 @ 前缀锚 14/decisions UTF8 非空行锚 24/树态/bm-a 写盘迹象）"
    "②生产线=BS-005 原版+bs005e 双 blocked 维持（共享开窗实录批·素材窗一开即续链：对位表重构→重渲→S2 复跑→E8→M4→登记〔bs005e=F-007 预留位·BS-005 原版=编号顺延〕·新源规格化 prep_vertical --batch 一跑直达）"
    "③#27 ①有声线=ch.5 收官毕（F-012 五件在库 F-008~F-012）——ch.6 网文稿未落（cta 周浩宇/陈雅雯双钩已埋·bm-a 稿落盘后新连载节律随轮认领）+②③ bm-a 进度复核（网文 ch.6 待落·漫画 ep.3 待见）"
    "④例行=探针三件套照跑（readiness 预期=bs-005/bs005e 双 render-unannot blocked 在链预期红维持·双件登记即清）"
    "⑤idle-fast 并窗计数=1/6（R232 起重计·R231 实活轮已收账）。"
)

sp = os.path.join(ROOT, r'src\os\state.json')
raw = io.open(sp, encoding='utf-8').read()
st = json.loads(raw)
assert st['tick'] == 231, 'unexpected tick %s' % st['tick']
st['tick'] = 232
st['focus'] = new_focus
assert st['log'][-1].startswith('2026-09-25 10:4x R231'), 'unexpected log tail'
st['log'].append(log_line)
out = json.dumps(st, ensure_ascii=False, indent=2)
if raw.endswith('\n'):
    out += '\n'
io.open(sp, 'w', encoding='utf-8', newline='').write(out)

ep = os.path.join(ROOT, r'docs\status-export.json')
raw2 = io.open(ep, encoding='utf-8').read()
ex = json.loads(raw2)
ex['export_ts'] = iso
for d in ex['depts']:
    if d['n'] == '工程技术部':
        d['t'] = ("OS 循环 idle-fast R232（快速路径五静+探针绿·不进开轮四步·并窗 1/6：素材窗 8 窗零 Biggame 总控窗"
                  "=BS-005/bs005e 双 blocked 维持·bm-a 复核零新进展〔ch.6 未落/ep.3 未现〕·三探针全绿·集团双锚静〔ledger 14/decisions 24〕）")
for row in ex['outs']:
    if row[0] == 'OS 循环':
        row[1] = 'on'
        row[2] = ("tick 232·R232（idle-fast 五静+探针绿：素材窗零 Biggame 总控窗=BS-005/bs005e 双 blocked 维持"
                  "·bm-a 复核零新进展〔网文 ch.6 未落/漫画 ep.3 未现〕·三探针全绿·集团双锚静）")
for row in ex['results']:
    if row[1] == 'OS 轮次':
        row[0] = '232'
out2 = json.dumps(ex, ensure_ascii=False, indent=2)
if raw2.endswith('\n'):
    out2 += '\n'
io.open(ep, 'w', encoding='utf-8', newline='').write(out2)
print('R232 close done: tick=232, warns=%d, log entries=%d, export_ts=%s' % (warns, len(st['log']), iso))
