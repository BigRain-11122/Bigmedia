# -*- coding: utf-8 -*-
# R660 declared-idle closeout: state.json (tick/ts/task/log append) + status-export.json (add-only surgical)
import json, io, os, re, datetime, sys

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
SP = os.path.join(ROOT, 'src', 'os', 'state.json')
EP = os.path.join(ROOT, 'docs', 'status-export.json')
DIAG = os.path.join(ROOT, '.c3-tmp', 'r660_close_diag.txt')

now = datetime.datetime.now()
ts = now.strftime('%Y-%m-%d %H:%M:%S')
stamp = now.strftime('%Y-%m-%d %H:%M')  # approximate-minute narrative prefix

logline = (
    stamp + " R660: declared-idle 空轮判定（五静+探针绿+可领序尽·P-2026-09-28-02 ②④序·新窗 2/6=R659-R664 本窗不 commit·满 6/跨日/异常/实活即收）——"
    "①五查静：无新令（orders 顶=O-20260928-1910 19:12:33 锚未动）+无新集团转办（ledger 严格 @ 前缀 34 行=锚·R659 06:0x rowdiff NEW=0 基线同晨沿用）+无新决策行（decisions UTF8 非空行 68=锚）+production=open 自愈核在位零翻正+无 index.lock；"
    "②树态=bm-a codex 批未闭（README+3/city-humanities +14 worktree 未暂存态=R659 轮末补记定谳口径·mtime 04:06 未动·HEAD b8344d0 R658 05:56 后零新 commit）=五维计数台账共享面让位维持+untracked 全属自产 tmp 三族（.c3-tmp 本轮探针族/.sc003-tmp 09-27 史实批 41 件/.sc003-v3-tmp）预期态零外族路径；"
    "③可领序尽（本轮复核较 R659 增三件核）：E4 双回填态核=已毕零补办（DIGEST-v9=R632 回填 8.0+REACT-v5=R643 同轮回填 7.0·P-1 试点判据①套路化零再现 ✓②7.0<8.0 ✗ 判负留痕·终判挂 REACT v6=09-30 热点窗）·"
    "#15 口吻改写批可领性裁定=不领（R170 实况注记正源：余 9 稿「随量产逐件拍稿压缩过门·逐件 S1 必对声线正典」=绑定未来生产件非独立改写批·N=6 已收官+慢产门 O-20260928-1725+TOP1 重构令 O-20260928-1836 下新起件=逐件重构对照基准件交卷属 bm-a 创作线辖区·循环不越线自起件·假绿灯律历史件诚实维持开板不造活）；"
    "#86 四腿全 gated（a 腿 pools.json 06:06 重写叶数 1440=1440 源闭/b 腿 registry 生成卡≠手写锚 R316 裁定·anchors 正典位止 C-00029/c 腿+d 腿=bm-a 让位区）·#70 OSS 下窗切片 2=09-29 21:40 后开未到（切片 1 已毕 R644=窗面义务足）·#67 触发律零新 CEO 令级事件·"
    "#63 图鉴 supply-gated 同锚（R659 同晨 06:06 轮首核 anchors 止 C-00029·本轮沿用未重采）·#59 REACT v6 挂 09-30 热点窗（今日窗 v5 R643 已用）·#31 ch5 v3 稿未落 supply-gated（bm-a 面）·#78 素材门前置 blocked·#17 needs-CEO 提案面·#66 blocked-on-CEO 物理件·#57 10-07/#80 10-01/#82 10-05 挂账窗·queue 顶项全 gated（B5 账号期门控·C4 触发位=首个进链件·A/C 池 done）→W40 窗提案 P-1 已交=保护态豁免面在案（门控型/素材窗 blocked/bm-a 在途批/CEO 物理件待开）→一行声明收轮合法（禁以声明代取活自检=可领项逐件核过非「想不出活」）；"
    "④三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞 0 发现（账号批次①+GATE 6/10+#17 皆外部 CEO 面·阻塞≠失败口径）/loop_health 3 FAIL+41 WARN 全在案类（2 outage=09-26 49min+09-28 609min 同事件足迹已裁定不重复触发+account-lag beat660>tick659=轮内瞬态 tick660 收账自平 R615-R657 先例连·41 WARN 较 R658 40 新增 1=R658 05:30→05:56 26min 长实活轮合法 WARN 级）；"
    "⑤例行件：日报 09-29 在案不重跑（R637 断轮件补产）/W40 周审在案（R576）/W41 周报=10-05 后首个周轮/global-benchmarks ≤7 跳过（下期 10-01=#80 并窗）/T1 催办=已裁项停用口径/当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）/tokens:local=0（探针+核验纯脚本零本地模型调用·P-54⑤ 计量律）；"
    "⑥P-61 导出步照走（export_ts 刷+results 660 行末位追加+OS 行升 tick 660=三面·add-only+格式随 HEAD indent=1=R659 补记导出件重写律执行）——下轮=R661 可领序=①#86 codex 续采（让位解除判据=bm-a 批闭 commit 落地·C-00030 锚轮首核）②#70 OSS 下窗切片 2（21:40 后）③#67 触发律。"
)

# strip stamp prefix for task field (first 60 chars)
prefix_match = re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2} ', logline)
task = logline[prefix_match.end():][:60]

diag = io.open(DIAG, 'w', encoding='utf-8')
diag.write(f"ts={ts}\ntask60={task}\nlogline_len={len(logline)}\n")

# ---------- state.json ----------
raw = io.open(SP, encoding='utf-8').read()
obj = json.loads(raw)
rt = json.dumps(obj, ensure_ascii=False, indent=2)
format_ok = (rt.rstrip('\n') == raw.rstrip('\n'))
diag.write(f"state_roundtrip_ok={format_ok}\n")

if not format_ok:
    diag.write("ABORT: state.json serializer mismatch - surgical fallback required\n")
    diag.close()
    print('ABORT-STATE-FORMAT')
    sys.exit(2)

obj['tick'] = 660
obj['ts'] = ts
obj['task'] = task
assert isinstance(obj['log'], list)
obj['log'].append(logline)
new_state = json.dumps(obj, ensure_ascii=False, indent=2)
if raw.endswith('\n'):
    new_state += '\n'
io.open(SP, 'w', encoding='utf-8', newline='').write(new_state)
diag.write("state.json written (tick=660, log +" + str(len(logline)) + " chars)\n")

# ---------- status-export.json (surgical add-only) ----------
eraw = io.open(EP, encoding='utf-8').read()
trailing = ''
core = eraw
while core and core[-1] in '\r\n':
    trailing = core[-1] + trailing
    core = core[:-1]

# 1. export_ts
new_export_ts = ' "export_ts": "' + now.strftime('%Y-%m-%d') + 'T' + now.strftime('%H:%M:%S') + '+08:00",'
core2, n1 = re.subn(r'(?m)^ "export_ts": "[^"]*",$', new_export_ts, core, count=1)
assert n1 == 1, 'export_ts not replaced'

# 2. OS line (tick 659 -> tick 660)
os_line_new = ('   "tick 660：R660 declared-idle 空轮判定（五静+探针绿+可领序尽·P-02 ②④序·窗 2/6=R659-R664）：'
               'E4 双回填态核已毕（DIGEST-v9 R632/REACT-v5 R643·P-1 判据①②判读毕终判挂 v6）·#15 口吻改写批裁定不领（R170 注记=随量产逐件拍稿压缩过门非独立批·慢产门+TOP1 下新起件=bm-a 创作线辖区）·'
               'bm-a codex 批未闭让位维持·三探针 board 0F/readiness 3 皆外部 0 发现/loop 3F+41W 在案类（account-lag 轮内瞬态 tick660 收账自平）·tokens:local=0——下轮 R661 可领序=①#86（bm-a 批闭判据）②#70 切片 2（21:40 后）③#67 触发律"')
core3, n2 = re.subn(r'(?m)^   "tick 659：.*"$', lambda m: os_line_new, core2, count=1)
assert n2 == 1, 'OS line not replaced'

# 3. results append (after 659 entry, end of file)
suffix = '"\n  ]\n ]\n}'
assert core3.endswith(suffix), 'results tail mismatch'
summary660 = ('R660 declared-idle 空轮判定（五静+探针绿+可领序尽·窗 2/6）：五查锚静（orders O-1910/ledger 34/decisions 68）·'
              'E4 双回填核已毕（DIGEST-v9 R632/REACT-v5 R643 同轮回填+P-1 ①✓②✗ 判负留痕终判挂 v6）·'
              '#15 口吻改写批裁定不领（R170 注记=随量产逐件拍稿压缩过门非独立批·N6 收官+慢产门+TOP1=bm-a 创作线辖区）·'
              'bm-a codex 批未闭让位维持·可领序尽（#86 四腿 gated/#70 未到窗/#67 零新事件/#63 锚止 C-00029/#59 v6 挂 09-30/queue 顶项 gated/W40 提案已交）=保护态豁免面在案·'
              '三探针 board 0F/readiness 3 外部 0 发现/loop 3F+41W 在案类（account-lag tick660 收账自平）·tokens:local=0·下轮可领序 #86 让位判据/#70 21:40/#67 触发律')
new_block = ('",\n  [\n   "660",\n   ' + json.dumps(summary660, ensure_ascii=False) + '\n  ]\n ]\n}')
core4 = core3[:-len(suffix)] + new_block
io.open(EP, 'w', encoding='utf-8', newline='').write(core4 + trailing)
diag.write("status-export.json written (export_ts + OS line + results 660 append)\n")
diag.close()
print('done')
