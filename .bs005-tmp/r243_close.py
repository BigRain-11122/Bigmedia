import json, os, datetime

REPO = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

now = datetime.datetime.now()
ts_str = now.strftime("%Y-%m-%d %H:%M:%S")
min_str = now.strftime("%Y-%m-%d %H:%M")
hhmm = now.strftime("%H:%M")

daily_ok = os.path.exists(os.path.join(REPO, 'data', 'intel', 'daily', '2026-09-25.md'))
week_ok = os.path.join(REPO, 'docs', 'audits', '2026-W39-self-audit.md')

log_line = (
    f"{min_str} R243: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 2/6）——"
    "①无新令（orders 顶=O-20260925-1153-BG-C·R241 已记账）"
    "②backlog 顶行不可认领（#28 done〔PT-02 整改 R241 毕〕·#27 ①②③ 全毕·④发布锁内挂账·ch.6 网文稿未落=bm-a 面〔novel 实证止 ch.5〕·BS-005/bs005e 双 blocked 待素材窗·#15 随量产逐件·#17 needs-CEO·#21 周日件今周五不到）"
    "③树态=仅并窗自记账（M state.json+M status-export.json=预期态）+自产 blocked 批中间件未提交（.bs005-tmp/.bs005e-tmp 批闭收账惯例维持）·无 index.lock·无 bm-a 活跃写盘迹象（novel 止 ch.5/comic 止 ep.2 零新进展）"
    "④素材窗迹象核=窗口枚举 14 窗零 Biggame 总控窗（Tuanjie 态=Cowork/Game/DemoScene/HMI Version Control+豆包/Lovart/硅基生命元宇宙 Edge·R193-R242 定谳线维持·r243-scan-all.txt 留档）→双 blocked 维持·自进清单真锚核=清单文件零变化（mtime 06:17=R206 自产写·R207-R242 判据全维持=无可领真锚项·不凑工作量造活）；"
    "集团扫描=ledger 严格行含 @ 四模式 15 行=锚零新转办·decisions UTF8 非空行 29（总行 32 双口径）=锚零新行零动作；"
    "三探针全绿=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+2 发现（bs-005/bs-005e render-unannot=blocked 在链预期红维持·F-005/F-007 登记即清·阻塞≠失败口径 exit 1）/loop_health 0 FAIL 17 WARN 皆在案史实（11 log-order+6 heartbeat-gap·tick242=done242 对账平·state-ts 门执法第二轮零红零滞后）；"
    f"例行件=日报 2026-09-25{'在案不重跑（实证）' if daily_ok else '缺失！'}·W39 周审在案不重跑·global-benchmarks 更新记录 2026-09-24 day1 ≤7 天跳过刷新（下期 ~10-01）·T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）——"
    "一行收账即出（本轮不 commit·并窗轮 2/6·P-61 导出步照刷 export_ts+实况派生轻量）。下轮=R244 快速路径首查（素材窗迹象优先/新令/集团转办），全静即 idle-fast（3/6）。"
)

task_line = log_line.split("R243: ", 1)[1] if "R243: " in log_line else log_line
task_field = ("R243: " + task_line)[:60]

sp = os.path.join(REPO, 'src', 'os', 'state.json')
with open(sp, encoding='utf-8') as fh:
    state = json.load(fh)

state['tick'] = state.get('tick', 0) + 1
state['log'].append(log_line)
state['ts'] = ts_str
state['task'] = task_field
state['focus'] = (
    "R244: 快速路径判定轮（锚：ledger @行 15·decisions 非空行锚 29〔UTF8 口径·总行 32 双口径〕·orders 尾 O-20260925-1153-BG-C·"
    "树态自账预期态〔M state/export+tmp 工件〕·state.ts/task 心跳面逐轮刷新执法）→五静+探针绿=idle-fast 3/6；"
    "素材窗=窗口枚举零 Biggame 总控窗定谳线 R193-R243·BS-005/bs005e 双 blocked（bs005e=F-007 预点位）；"
    "#27 音频线=ch.6 网文稿未落（bm-a 面·cta 周浩宇/陈雅雯双钩已埋）·已产 F-008~F-012 五件；"
    "readiness 预期=3 blocker+2 finding 同集；承诺：窗满 6 轮/跨日/异常/实活即收账"
)

with open(sp, 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(state, fh, ensure_ascii=False, indent=1)
    fh.write("")

# P-61 export step
ep = os.path.join(REPO, 'docs', 'status-export.json')
with open(ep, encoding='utf-8') as fh:
    exp = json.load(fh)

exp['export_ts'] = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
for d in exp['depts']:
    if d['n'] == '工程技术部':
        d['t'] = ("OS 循环 R243（idle-fast 快速路径·五静+探针绿：orders 顶 O-1153 维持·ledger 15/decisions 29 双锚零新转办·"
                  "素材窗 14 窗零 Biggame 总控窗双 blocked 维持·ch.6 未落/ep.3 未现零新进展·state.ts/task 心跳面第二轮刷新零红·并窗轮 2/6 不 commit）")
for row in exp['outs']:
    if row[0] == 'OS 循环':
        row[2] = ("tick 243·R243（idle-fast：五静〔orders 顶 O-1153·backlog 顶 #28 done·树净零锁·bm-a 零新写盘〕+探针绿"
                  "〔board 0 fail/readiness 3+2 同集预期/loop 0 fail 17 warn 历史·state-ts 第二轮过〕·素材窗零 Biggame 总控窗·"
                  "ch.6 未落/ep.3 未现零新进展·并窗 2/6）")
for row in exp['results']:
    if row[1] == 'OS 轮次':
        row[0] = str(state['tick'])

with open(ep, 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(exp, fh, ensure_ascii=False, indent=2)
    fh.write("")

print("CLOSED tick=%s ts=%s daily=%s" % (state['tick'], ts_str, daily_ok))
