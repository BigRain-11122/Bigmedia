# -*- coding: utf-8 -*-
"""R316 ledger close-out: C1 speed-ramp pilot (bs-001-v15-douyin) legs 3-4.
Updates: renders/README v15 row, capabilities C-28 + v1.31, queue C1 done +
burn record, station-reviews R316 row, status-export.json, state.json
(tick/focus/log/ts/task). UTF-8 throughout (encoding law; r312 pattern).
"""
import io, json, os, re, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
NOW = time.strftime('%Y-%m-%d %H:%M:%S')

# ---------- 1) renders/README.md v15 row ----------
rp = os.path.join(ROOT, 'output', 'renders', 'README.md')
lines = io.open(rp, encoding='utf-8').read().splitlines()
idx = next(i for i, l in enumerate(lines) if l.startswith('| bs-001-v14b-douyin-9x16.mp4 |'))
v15row = (
u"| bs-001-v15-douyin-9x16.mp4 | **C1 试点件·备件位（非 F 位·R316·speed-ramp 引擎试点=剪辑语言升档候选）** | "
u"**R316 C1 腿 3：R-E douyin 12 段同 v14b 语言+6 punch 拍速度爬坡**（idx 0,2,3,4,5,7·每拍 4 微块=头块 1.0+"
u"三窗 1.1429/1.6000/2.6667〔帧栅格量化实际速度·设计 ladder 1.2/1.6667/2.5〕·9:16 1080×1920·"
u"**ffprobe 57.388s=与 F-006 v14b 逐毫秒一致**〔1721 帧·时间线代数零动·cards/srt/audio 全源同链复用=反重复〕）；"
u"S2 三门 R316 独立执法全绿（ai_feel 0 FAIL 0 WARN〔CV 0.185/0.204 同音轴确定性〕+层 1.8 douyin 七面 PASS"
u"〔timeline 真直拼代数过=ramp 接线零检查面破坏〕+spec 抖音双 PASS〔57.39s ∈15-60s 窗 2.6s 余量〕）+"
u"ramp 代数 6/6 拍 sum_out=span_frames+1 精确+**窗连续性验图 54/54 PASS**（6 拍×3 内边界×pre/x/post·"
u"零跳变零冻结零黑帧零撕裂·爬坡特征可视验证〔低速边界帧间差小/高速边界帧间差大=1.0→2.67× 吻合〕·"
u"b3-o157-post/b4-o203-pre=白闪转场帧不计缺陷〔自动化白闪豁免规则建议〕·证据=`.bs001-dy-tmp/s2-results-r316.md`+`probe-r316/`）；"
u"**F-006 v14b 维持现行件·v15 候选待评审席决断**（内容面零动·剪辑语言面升档·换档=下批评审带裁决非自动） |")
lines.insert(idx + 1, v15row)
io.open(rp, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')

# ---------- 2) capabilities.md: C-28 row + v1.31 tail ----------
cp = os.path.join(ROOT, 'docs', 'capabilities.md')
t = io.open(cp, encoding='utf-8').read()
anchor = u"（MAD 切点单帧全距跳验图） |"
assert anchor in t, 'C-28 anchor missing'
t = t.replace(anchor, (
    u"（MAD 切点单帧全距跳验图）；**C1 speed-ramp 批件（R315 腿 1-2+R316 腿 3-4 毕）**：douyin punch 拍"
    u"速度爬坡=PROFILES ramp 配置〔window 0.5s/ladder 1.2/1.6667/2.5〕+build_micro_blocks 微块构造"
    u"〔Σ输出帧=span+1 安全帧·源帧栅格量化 n_src 整数·窗口 ≤40% span 钳位·退化拍返 None〕+"
    u"ramp_filter_complex〔split 多支/setsar=1/单 setpts 先减后除/fps=30/段内 concat 同链 zoompan 处理链〕·"
    u"试点实证=bs-001-v15-douyin（S2 三门全绿+ffprobe 57.388s 逐毫秒同 v14b+窗连续性验图 54/54·"
    u"备件位=F-006 v14b 维持现行） |"), 1)
v131 = (
u"- 2026-09-26: v1.31 C1 speed-ramp 引擎批（自进清单 C1·OS 循环 R315 腿 1-2+R316 腿 3-4 毕=C1 全腿闭环）——"
u"C-28 行同步：`edit_craft.py` douyin punch 拍速度爬坡落地（ramp 配置+build_micro_blocks 段构造律+"
u"ramp_filter_complex 坑三则内建·36 单测+271 回归绿·R315）·试点件=`bs-001-v15-douyin-9x16.mp4`"
u"（R316：S2 三门全绿+ffprobe 57.388s 逐毫秒同 v14b=时间线代数零动+ramp 代数 6/6+窗连续性验图 54/54 PASS·"
u"renders README v15 行）；备件位=F-006 v14b 维持现行件·换档待评审席\n")
t = t.rstrip('\n') + '\n' + v131
io.open(cp, 'w', encoding='utf-8', newline='\n').write(t)

# ---------- 3) self-improvement-queue.md: C1 leg 3-4 done + burn ----------
qp = os.path.join(ROOT, 'docs', 'self-improvement-queue.md')
q = io.open(qp, encoding='utf-8').read()
qa = u"·**腿 3-4 待领**（bs-001 douyin 试点重渲+层 1.8 复跑+ramp 窗连续性验图+台账四件） |"
assert qa in q, 'queue leg anchor missing'
q = q.replace(qa, (
    u"·**腿 3-4 done 2026-09-26（R316）=C1 全腿闭环**（bs-001-v15-douyin 试点=S2 三门全绿+ffprobe 57.388s "
    u"逐毫秒同 v14b=时间线代数零动+ramp 代数 6/6+窗连续性验图 54/54+台账四件毕·备件位=F-006 v14b 维持现行·"
    u"换档待评审席） |"), 1)
burn = (
u"- 2026-09-26: **C1 腿 3-4 done + C1 全腿闭环**（OS 循环 R316·图鉴供给门 registry 误判撤领后转 queue 顶项）——"
u"bs-001 douyin 试点重渲 v15：6 punch 拍速度爬坡〔idx 0,2,3,4,5,7·4 微块/拍·实际速度 1.1429/1.6000/2.6667="
u"帧栅格量化〕·S2 三门全绿〔ai_feel 0 FAIL 0 WARN+层 1.8 douyin 七面 PASS+spec 抖音双 PASS 2.6s 余量〕+"
u"ffprobe 57.388s=与 F-006 v14b 逐毫秒一致〔时间线代数零动〕+ramp 代数 6/6 sum_out=span+1+"
u"窗连续性验图 54/54 PASS〔`.bs001-dy-tmp/probe-r316/`·白闪转场帧不计缺陷+自动化豁免规则建议注记〕·"
u"备件位=v14b 维持现行件·换档待评审席·renders/capabilities/station-reviews/queue 台账四件毕\n")
q = q.rstrip('\n') + '\n' + burn
io.open(qp, 'w', encoding='utf-8', newline='\n').write(q)

# ---------- 4) station-reviews.md R316 row ----------
sp = os.path.join(ROOT, 'docs', 'reviews', 'station-reviews.md')
srow = (
u"| 2026-09-26 | **C1 speed-ramp 引擎试点验收（bs-001-v15-douyin=R316 腿 3-4·自进清单顶项·备件位非 F 位）** | "
u"bs-001-v15-douyin-9x16.mp4+`.bs001-dy-tmp/s2-results-r316.md`+`probe-r316/tile-r316.png` | "
u"引擎升级备件验收（非成品评审·F-006 内容面零动）：S2 三门独立执法全绿（ai_feel 0 FAIL 0 WARN〔CV 0.185/0.204="
u"同音轴确定性〕+层 1.8 douyin 七面 PASS〔beat-align 11/11+camera 12 段+visual-ratio 0.83+flash 6+share 0.64+"
u"variety+timeline 真直拼代数过=ramp 接线零检查面破坏〕+spec 抖音双 PASS〔57.39s ∈15-60s 窗 2.6s 余量〕）+"
u"ffprobe 57.388s=与 F-006 v14b 逐毫秒一致（1721 帧·时间线代数零动）+ramp 代数 6/6 拍 sum_out=span_frames+1"
u"精确（seg0 160/seg2 103/seg3 160/seg4 206/seg5 153/seg7 139）+窗连续性验图 54/54 PASS（6 拍×3 内边界×"
u"pre/x/post·零跳变零冻结零黑帧零撕裂·爬坡特征可视验证=低速边界帧间差小/高速边界差大与 1.0→2.67× 设计吻合·"
u"b3-o157-post/b4-o203-pre=白闪转场帧不计缺陷〔自动化白闪豁免规则建议如实注记〕）→**备件位判定：F-006 v14b "
u"维持现行件·v15 候选待评审席决断**（内容面零动·剪辑语言面升档·换档=下批评审带裁决非自动）；"
u"未测面如实列=受众反应面〔未上线=未测量〕+换档决策面〔评审席〕 |\n")
with io.open(sp, 'a', encoding='utf-8') as f:
    f.write(srow)

# ---------- 5) status-export.json ----------
se_path = os.path.join(ROOT, 'docs', 'status-export.json')
se = json.load(io.open(se_path, encoding='utf-8'))
se['export_ts'] = time.strftime('%Y-%m-%dT%H:%M:%S+08:00')
se['do'] += (u"+C1 引擎集成腿 3-4 毕=C1 全腿闭环（R316 bs-001-v15-douyin 试点：S2 三门全绿+ffprobe 57.388s "
             u"逐毫秒同 v14b=时间线代数零动+窗连续性验图 54/54）")
for d in se['depts']:
    if d['n'] == u'工程技术部':
        d['t'] = (u"OS 循环 R316（C1 引擎集成腿 3-4 毕=C1 全腿闭环：bs-001-v15-douyin 试点重渲〔6 punch 拍速度爬坡·"
                  u"4 微块/拍·实际速度 1.1429/1.6/2.6667=帧栅格量化〕S2 三门全绿+ffprobe 57.388s=与 v14b 逐毫秒一致"
                  u"〔时间线代数零动〕+ramp 代数 6/6+窗连续性验图 54/54〔probe-r316〕·备件位=F-006 v14b 维持现行件"
                  u"·换档待评审席）·前轮 R315 腿 1+2 引擎+单测在案·state.ts/task 心跳面刷新")
se['outs'][0][2] = (u"tick 316·R316（自进轮——图鉴供给门误判撤领〔registry/OR/C-00030.md=生成批次 P-0 登记卡≠"
                    u"anchors 手写展示锚·纪律修正=供给门轮首核只查 census/anchors/ 正典位·claim c644de6 留痕〕"
                    u"→转 C1 腿 3-4 交付=bs-001-v15-douyin 试点重渲：S2 三门全绿〔ai_feel 0 FAIL 0 WARN+层 1.8 douyin "
                    u"七面 PASS+spec 抖音双 PASS 2.6s 余量〕+ffprobe 57.388s=与 F-006 v14b 逐毫秒一致〔时间线代数零动〕+"
                    u"ramp 代数 6/6 sum_out=span+1+窗连续性验图 54/54 PASS〔零跳变零冻结零黑帧·爬坡特征可视验证·"
                    u"白闪转场帧不计缺陷〕→备件位=F-006 v14b 维持现行·v15 候选待评审席决断；台账四件="
                    u"renders/capabilities C-28+变更记录 v1.31/queue burn/station-reviews；量产线=anchors/C-00030 "
                    u"仍不在位〔supply-gated 维持〕·REACT 当日映射耗尽维持〔R314 判定〕·ch.5 v3 稿未落〔bm-a 面〕）")
se['results'][0][0] = "316"
json.dump(se, io.open(se_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- 6) state.json ----------
st_path = os.path.join(ROOT, 'src', 'os', 'state.json')
st = json.load(io.open(st_path, encoding='utf-8'))
log_entry = (
u"2026-09-26 02:xx R316: 生产轮尝试→撤领转自进轮·C1 引擎集成腿 3-4 交付=C1 全腿闭环（实活轮）——"
u"①轮首快速路径五查静（无新令 orders 顶=O-1931 R283 已记账/ledger 严格 @ 四模式 21 行=锚零新转办〔R313-R315 "
u"同锚·R316 首查正则口径误报 15 自纠=中文后缀不匹配 ASCII 类·substring 复核 21 平〕/decisions python 非空行 33="
u"锚零新行〔尾=D-20260926-04〕/树净零锁/日报 2026-09-26 在案不重跑）+三探针全绿（board 0 FAIL 5 题 10 稿 5 in "
u"production/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 0 FAIL 19 WARN 皆在案史实）；②量产线领件判断="
u"图鉴续件 C-00030 轮首核**误判**：registry/OR/C-00030.md 在位（熊简梨·感知塔站值守员卡）被当供给首开→claim "
u"c644de6 两步制落防撞+backlog #63 起件→**复核纠错撤领**：该文件=生成批次 P-0 登记卡（mtime 09-24 00:13=R313 "
u"前三轮已在位·生成卡非手写展示锚），供给门正典位=census/anchors/C-00030.md 仍不在位（anchors 止 C-00029）="
u"**供给门维持关闭 supply-gated·撤领如实注记**（查锚纪律修正=供给门轮首核只查 anchors/ 正典位·claim 留痕不删·"
u"零产出·#63 维持开板）；REACT=当日映射余量耗尽维持（R314 判定·同日）·ch.5 v3 稿未落（novel 实证止 "
u"SC-001-04-v3+SC-001-05-v1·bm-a 面）；③**C1 腿 3-4 执行**（R315 排程·queue 顶项）：腿 3=bs-001 douyin 试点"
u"重渲 v15=bs-001-v15-douyin-9x16.mp4（R202 v14b 全源同链复用=cards-v12-matched+.v11-trim subs/audio·"
u"时间线零动唯剪辑语言升档：6 punch 拍〔idx 0,2,3,4,5,7〕吃速度爬坡=4 微块/拍〔头块 1.0+三窗 1.1429/1.6000/"
u"2.6667=帧栅格量化实际速度·ladder 设计值 1.2/1.6667/2.5〕·后台 cmd 渲染 exit 0·duration_expected 58.167s 同 "
u"v14b）→腿 4=S2 三门+层 1.8 复跑+窗连续性验图：**S2 三门全绿**（ai_feel 0 FAIL 0 WARN〔gaps 11 处 0.220-0.558s·"
u"CV 0.185/0.204=与 R202 逐项一致同音轴确定性〕+层 1.8 douyin 七面 PASS〔beat-align 11/11+camera 12 段全动+"
u"visual-ratio 0.83+flash 6 on-profile+share 0.64+variety+timeline 真直拼代数过=**ramp 接线零检查面破坏实证**〕+"
u"spec 抖音双 PASS〔9:16+57.39s ∈15-60s 窗 2.6s 余量〕）+**ffprobe 57.388s=与 v14b 逐毫秒一致**（1721 帧·"
u"时间线代数零动实证）+ramp 代数报告 6/6 拍 sum_out=span_frames+1 精确（seg0 160/seg2 103/seg3 160/seg4 206/"
u"seg5 153/seg7 139）+**窗连续性验图 54/54 帧 PASS**（6 拍×3 内边界×pre/x/post·运动单调推进零跳变零冻结零黑帧"
u"零撕裂·爬坡特征可视验证=低速边界帧间差小/高速边界帧间差大与 1.0→2.67× 设计吻合·b3-o157-post/b4-o203-pre="
u"白闪转场帧不计缺陷〔验图注记=自动化时白闪需豁免规则〕·tile `.bs001-dy-tmp/probe-r316/`）；④台账四件="
u"renders README v15 行〔C1 试点件·备件位·F-006 v14b 维持现行件·v15 候选待评审席决断=非自动换档〕+"
u"capabilities C-28 行 ramp 备件注+变更记录 v1.31 行+queue C1 腿 3-4 done+burn 记录行〔C1 全腿闭环〕+"
u"station-reviews R316 行〔备件位验收·未测面如实列=受众反应面+换档决策面〕+status-export 刷（R316 面）；"
u"⑤例行件：日报 2026-09-26+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks day2 ≤7 跳过（下期 ~10-01）·"
u"T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=0（本地渲染+机检+"
u"验图零模型调用·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）。下轮=R317 快速路径首查→"
u"量产线按序领件判断（anchors/C-00030 正典位核/ch.5 v3 稿落迹象/REACT 翌日热点）→全静即自进池下一项"
u"（C1 毕=池剩余 C3 edge-tts 情感参数〔C 池〕/B5 账号期）。收账显式列文件 commit+push。")
log_entry = log_entry.replace(u'2026-09-26 02:xx', NOW)
st['tick'] = 316
st['focus'] = (u"R317: focus=快速路径首查：查新令/集团转办（ledger 锚 21/decisions 锚 33〔python 非空行口径·"
               u"尾=D-20260926-04〕）/量产线按序领件判断（图鉴续件=anchors/C-00030 正典位轮首核〔R316 registry "
               u"误判教训=供给门只查 census/anchors/ 正典位〕·REACT 续件=#59 按日热点随轮领〔轴位映射律+热点转述律 "
               u"R309 双律复用〕·ch.5 v3 稿落迹象〔bm-a 面·稿落即认领·音频线优先〕）/#57 替代率首报 10-07 窗挂账/"
               u"#21 周日立法件——全静即自进池下一项（C3 edge-tts 情感参数〔C 池〕·C1 全腿毕）")
st['log'].append(log_entry)
st['ts'] = NOW
st['task'] = re.sub(r'^\S+ \S+ ', '', log_entry)[:60]
json.dump(st, io.open(st_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('LEDGERS-OK', NOW)
