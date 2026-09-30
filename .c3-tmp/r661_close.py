# -*- coding: utf-8 -*-
"""R661 declared-idle accounting: state.json + status-export.json (P-61 export step).
Laws enforced: R659 export-rewrite law (add-only + format follows HEAD;
state.json indent=2 / status-export indent=1). Round-trip fidelity checked first.
"""
import json, io, sys
from datetime import datetime

now = datetime.now()
ts = now.strftime('%Y-%m-%d %H:%M:%S')
ts_iso = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')

log_line = (
    "R661: declared-idle 空轮判定（五静+探针绿+可领序尽·P-20260928-02 ②④序·新窗 3/6=R659-R664 本窗不 commit·满 6/跨日/异常/实活即收）——"
    "①五查静：无新令（orders 顶=O-20260928-1910 19:12:33 锚未动）+无新集团转办（ledger 严格 @ 前缀 34 行=锚·rowdiff vs r644_lednew5 基线〔L 前缀剥离正法〕NEW=0 GONE=0=零新 CEO 令级事件〔#67 触发律不解锁〕——首查大小写不敏感计数 35=L123 旧行 @bigstream 小写机器位伪命中·CaseSensitive 复核 34=R639/R647 在案陷阱复核定谳）"
    "+无新决策行（decisions UTF8 非空行 68=锚·mtime 03:20:29 未动）+production=open 自愈核在位零翻正+无 index.lock；"
    "②树态=bm-a codex 批未闭（README+3/city-humanities+14 worktree 未暂存态=R659 轮末补记定谳口径·mtime 04:06 未动·HEAD b8344d0 R658 后零新 commit）=五维计数台账共享面让位维持+untracked 全属自产 tmp 族（.c3-tmp 探针族/.sc003-tmp 09-27 史实批 41 件/.sc003-v3-tmp）预期态零外族路径；"
    "③可领序尽（本轮复核较 R660 增一读数核=E4 双回填段 finished.md 实读核毕零悬置〔DIGEST-v9=R632 落判 8.0+REACT-v5=R643 同轮回填 7.0——P-1 试点判据①套路化零再现 ✓〔旗型迁移=MC-003 语境门槛族〕②7.0<8.0 ✗ 判负留痕·终判挂 REACT v6=09-30 热点窗〕）；"
    "#86 四腿全 gated（a 腿源闭〔pools.json 叶数 1440 零增量·R659 定谳〕/b 腿锚止 C-00029 supply-gated〔C-00030 存在性 False 轮首核=anchors 正典位〕/c 腿+d 腿=bm-a 让位区〔章件深采二轮 ch1/ch2 v4 落 city-humanities=同写区零交集〕）·"
    "#70 OSS 下窗切片 2=09-29 21:40 后开未到（切片 1 已毕 R644=窗面义务足）·#67 触发律零新事件·#63 图鉴 supply-gated 同锚·#59 REACT v6 挂 09-30 窗（今日窗 v5 R643 已用）·#31 ch5 稿未落 supply-gated（bm-a 面）·#78 素材门前置 blocked·#17 needs-CEO 提案面·#66 blocked-on-CEO 物理件·#57 10-07/#80 10-01/#82 10-05 挂账窗·"
    "queue 顶项全 gated（B5 账号期门控·C4 触发位=首个进链件·A/C 池 done）→W40 窗提案 P-1 已交=保护态豁免面在案（门控型/素材窗 blocked/bm-a 在途批/CEO 物理件待开）→一行声明收轮合法（禁以声明代取活自检=可领项逐件核过非「想不出活」）；"
    "④三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞 0 发现（账号批次①+GATE 6/10+#17 皆外部 CEO 面·阻塞≠失败口径）/loop_health 3 FAIL+42 WARN 全在案类（2 outage=09-26 49min+09-28 609min 同事件足迹已裁定不重复触发+account-lag beat661>tick660=轮内瞬态 tick661 收账自平 R615-R657 先例连·42 WARN 较 R660 41 新增 1=R659 补记 06:13→R660 06:34 21min 轮间隙合法 WARN 级）；"
    "⑤例行件：日报 09-29 在案不重跑（R637 断轮件补产）/W40 周审在案（R576）/W41 周报=10-05 后首个周轮/global-benchmarks ≤7 跳过（下期 10-01=#80 并窗）/T1 催办=已裁项停用口径/当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）/tokens:local=0（探针+核验纯脚本零本地模型调用·P-54⑤ 计量律）·发布锁=M5 账号物理件不变（未上线=未测量）；"
    "⑥P-61 导出步照走（export_ts 刷+results 661 行末位追加+OS 行升 tick 661=三面·add-only+格式随 HEAD indent=1=R659 补记导出件重写律执行）——"
    "下轮=R662 可领序=①#86 codex 续采（让位解除判据=bm-a 批闭 commit 落地·C-00030 锚轮首核）②#70 OSS 下窗切片 2（21:40 后）③#67 触发律。"
)
full_log = now.strftime('%Y-%m-%d %H:%M') + " " + log_line
task = log_line[:60]

focus_new = (
    "R662: 空轮判定路径开轮——可领序=①#86 codex 续采余量（让位解除判据=bm-a 批闭 commit 落地·四腿态：a 腿源闭〔pools.json 叶数 1440 零增量〕/"
    "b 腿锚止 C-00029 supply-gated〔C-00030 实存位=registry/OR 非手写锚·R316 裁定勿重蹈〕/c+d 腿=bm-a 让位区〔章件深采二轮 ch1/ch2 v4=同写区〕）"
    "②#70 OSS 下窗切片 2（09-29 21:40 后开·OH-20260929-bigstream.md 续写·实搜面 ≥2+候选 ≥1 五门评估）③#67 编年史事件候选（ledger 新 CEO 令级事件落账触发律·反膨胀律照守）"
    "——W40 窗提案 P-1 已交（试点 1/2 判读毕·终判挂 REACT v6=09-30 热点窗）——五查锚=orders 顶 O-20260928-1910 19:12:33·ledger 34（rowdiff 基线=.c3-tmp/r644_lednew5.txt·L 前缀剥离正法·CaseSensitive 计数律）·decisions 68"
    "——R659 declared-idle 窗 3/6=R659-R664（满 6=R664 或跨日 09-30 00:00 先到即 batch commit·commit 注区间）"
)

# ---- state.json ----
with io.open('src/os/state.json', encoding='utf-8') as f:
    raw_state = f.read()
d = json.loads(raw_state)
old_tick = d['tick']
assert old_tick == 660, old_tick
rt = json.dumps(d, ensure_ascii=False, indent=2)
if rt != raw_state:
    if rt + '\n' == raw_state:
        state_trail = '\n'
    elif rt == raw_state.rstrip('\n') and not raw_state.endswith('\n'):
        state_trail = ''
    else:
        print('STATE ROUNDTRIP MISMATCH len', len(rt), len(raw_state))
        # locate first diff
        for i, (a, b) in enumerate(zip(rt, raw_state)):
            if a != b:
                print('first diff at', i, repr(rt[i-30:i+30]), '||', repr(raw_state[i-30:i+30]))
                break
        sys.exit(2)
else:
    state_trail = ''
print('state roundtrip OK')
d['tick'] = 661
d['focus'] = focus_new
d['log'].append(full_log)
d['ts'] = ts
d['task'] = task
with io.open('src/os/state.json', 'w', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(d, ensure_ascii=False, indent=2) + state_trail)
print('state.json written: tick 661, log R661 appended, ts/task/focus refreshed')

# ---- status-export.json ----
with io.open('docs/status-export.json', encoding='utf-8') as f:
    raw_exp = f.read()
e = json.loads(raw_exp)
rt2 = json.dumps(e, ensure_ascii=False, indent=1)
if rt2 != raw_exp:
    if rt2 + '\n' == raw_exp:
        exp_trail = '\n'
    elif rt2 == raw_exp.rstrip('\n') and not raw_exp.endswith('\n'):
        exp_trail = ''
    else:
        print('EXPORT ROUNDTRIP MISMATCH len', len(rt2), len(raw_exp))
        for i, (a, b) in enumerate(zip(rt2, raw_exp)):
            if a != b:
                print('first diff at', i, repr(rt2[i-30:i+30]), '||', repr(raw_exp[i-30:i+30]))
                break
        sys.exit(3)
else:
    exp_trail = ''
print('export roundtrip OK')
e['export_ts'] = ts_iso

res_desc = (
    "R661 declared-idle 空轮判定（五静+探针绿+可领序尽·窗 3/6）：五查锚静（orders O-1910/ledger 34 rowdiff 0〔CaseSensitive 计数律：不敏感 35=L123 机器位伪命中复核 34〕/decisions 68）"
    "·E4 双回填段 finished.md 实读核毕零悬置（DIGEST-v9 R632 8.0/REACT-v5 R643 7.0·P-1 ①✓②✗ 判负留痕终判挂 v6）"
    "·bm-a codex 批未闭让位维持（README+3/city-humanities+14 worktree 态 mtime 04:06 未动）"
    "·可领序尽（#86 四腿 gated：a 源闭/b 锚止 C-00030 False/c+d 让位区/#70 未到窗/#67 零新事件/#63 同锚/#59 v6 挂 09-30/#31 稿未落/#78 素材门/queue 顶项 gated/W40 提案已交）"
    "=保护态豁免面在案·三探针 board 0F/readiness 3 外部 0 发现/loop 3F+42W 在案类（account-lag tick661 收账自平·新 1 WARN=06:13→06:34 21min 轮间隙合法）"
    "·tokens:local=0·下轮可领序 #86 让位判据/#70 21:40/#67 触发律"
)
e['results'].append(["661", res_desc])

os_row_new = (
    "tick 661：R661 declared-idle 空轮判定（五静+探针绿+可领序尽·P-02 ②④序·窗 3/6=R659-R664 本窗不 commit）："
    "E4 双回填态核已毕（DIGEST-v9 R632/REACT-v5 R643·P-1 判据①②读毕终判挂 v6）·bm-a codex 批未闭让位维持（worktree +3/+14 mtime 04:06 未动）"
    "·三探针 board 0F/readiness 3 皆外部 0 发现/loop 3F+42W 在案类（account-lag 轮内瞬态 tick661 收账自平）·tokens:local=0"
    "——下轮 R662 可领序=①#86（bm-a 批闭判据）②#70 切片 2（21:40 后）③#67 触发律"
)
assert e['outs'][0][0] == 'OS 循环', e['outs'][0][0]
e['outs'][0][1] = os_row_new

with io.open('docs/status-export.json', 'w', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(e, ensure_ascii=False, indent=1) + exp_trail)
print('status-export.json written: export_ts + results 661 + OS row tick 661')
print('DONE ts=' + ts)
