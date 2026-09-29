# -*- coding: utf-8 -*-
# R728 close-out: E15 LC-015 air-budget trim chain final + TTS final track
# (v2 60.259s -> v3 57.615s in-window 2.385s) -> ledgers + state + export.
import io, json, time, re

def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

NOW = time.strftime('%Y-%m-%d %H:%M:%S')
print('NOW', NOW)

# ---------- 0. m1_v2 evidence file: PS-redirect wrote UTF-16 BOM -> convert ----------
p = '.c3-tmp/r728_m1_v2.txt'
raw = open(p, 'rb').read()
if raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
    txt = raw.decode('utf-16')
    wr(p, txt)
    print('m1_v2 converted utf16->utf8')
else:
    print('m1_v2 already utf8/ascii')

# ---------- 0b. health FAIL count for honest log ----------
h = rd('.c3-tmp/r728_health.txt')
fails = re.findall(r'\[FAIL\] ([a-z-]+)', h)
warns = len(re.findall(r'\[WARN\]', h))
print('health FAILs:', fails, 'WARNs:', warns)

# ---------- 1. lc015 README: production record + gate block ----------
p = 'data/sources/lc015/README.md'; s = rd(p)
anchor = "- TTS light v1 实测 **64.409s 超窗**（242 字·数字密度件如预期·fleet 带外初读）→空气预算机械裁链（v1→v2/v3 定稿·卡片锚点列零动+信条零动约束）=R728 首位。"
assert anchor in s, 'lc015 README v1 row anchor missing'
r728row = ("- [2026-09-30 06:2x R728 空气预算裁链定稿+TTS 定稿音轨毕（R727 承接·R724 同型）] v2 机械裁 23 字（弄堂派/铺里/那晚/他/也要/铺子下午才开/就给人→压缩分载归卡锚列）=60.259s 仍薄超窗 0.259s（-23 字省 4.15s=0.18s/字实证）→R513/R693 防翻窗续裁先例执行 v3 再裁 12 字（北外滩/工位/前的/他说/校准师全归卡承载·粥铺画面保）=**57.615s 定稿入窗 2.385s 余量**（fleet 带内·LC-011 2.24s 同位带）——col2 卡片锚点列 verbatim 零动 12/12 断言过（v1↔v2↔v3 三档）+信条零动+事实数字全保（三十年/一九七五年/微秒/两个徒弟/七十四岁/每周三）+M1 v2/v3 双复检 0 FAIL 0 WARN（b2/b8 三逗长句 WARN 随裁链销账）+口播列 276→240 字符（含标点）+TTS light 定稿音轨 .lc015-tmp/（audio.mp3 57.615s+subs.srt 12 cues+cards.json 基线·--order LC-015-v3·--template=.lc014-tmp/cards.json 链式承继·cyber light+human 42 产线默认·BGM-A 纯净）——v1-v3 beats 全留档·渲染腿（R710/R725 同型五步+全卡几何审计）=R729 首位。\n")
s = s.replace(anchor, anchor + "\n" + r728row)
gate_old = "- S1=10/10 PASS（十四连满分·判词档 20260930-053858）·M1 v1=0F2W（b2/b8 长句=裁链收口位）·空气预算=v1 64.409s 超窗→机械裁链=R728 首位（fleet 带=1.2-2.6s 余量目标）·渲染腿/收官腿=后续轮领（R710/R725 渲染五步+E8+ASR+E4+M4→F-070→冗余池第十二件→E15 出池）。发布锁=M5 账号物理件不变（未上线=未测量）。"
gate_new = "- S1=10/10 PASS（十四连满分·判词档 20260930-053858）·M1 终稿 v3=0 FAIL 0 WARN（b2/b8 三逗长句 WARN 随裁链销账）·空气预算=**v3 57.615s 定稿入窗 2.385s 余量**（fleet 带=1.2-2.6s·LC-011 2.24s 同位带·col2 verbatim 零动 12/12 断言+信条零动+事实数字全保）·渲染腿/收官腿=后续轮领（R710/R725 渲染五步+E8+ASR+E4+M4→F-070→冗余池第十二件→E15 出池）。发布锁=M5 账号物理件不变（未上线=未测量）。"
assert gate_old in s, 'gate block anchor missing'
s = s.replace(gate_old, gate_new)
wr(p, s)
print('lc015 README updated')

# ---------- 2. queue burn row ----------
p = 'docs/self-improvement-queue.md'; s = rd(p)
if not s.endswith('\n'): s += '\n'
burn = ("- 2026-09-30: **E15 空气预算裁链定稿+TTS 定稿音轨毕（R728·R727 起链承接·R724 同型）：v2 机械裁 23 字=60.259s 薄超窗 0.259s→R513/R693 防翻窗续裁 v3 再裁 12 字（北外滩/工位/前的/他说/校准师全归卡承载·粥铺画面保）=57.615s 定稿入窗 2.385s 余量（fleet 带内·LC-011 2.24s 同位带）+col2 verbatim 零动 12/12 断言+信条零动+事实数字全保+M1 v2/v3 双 0F0W（b2/b8 长句 WARN 销账）+TTS light 定稿音轨 .lc015-tmp/（--order LC-015-v3·--template=.lc014-tmp 链式承继·BGM-A 纯净）——渲染腿（R710/R725 同型五步+全卡几何审计）+收官腿（E8+ASR+E4+M4→F-070→冗余池第十二件→E15 出池）=后续轮领；lane=E15 active+E16 standby 维持 ≥2**\n")
wr(p, s + burn)
print('queue burn row appended')

# ---------- 3. state.json ----------
p = 'src/os/state.json'; d = json.loads(rd(p))
d['tick'] = 728
d['ts'] = NOW
log_r728 = ("2026-09-30 " + NOW[11:16] + " R728: 生产轮·E15 LC-015 朱鸿奎拆条空气预算裁链定稿+TTS 定稿音轨毕（R727 claim 承接·R724 同型·实活轮·产品优先律 P-20260929-07 对位=本轮实物增量=LC-015 定稿音轨 57.615s+beats v2/v3 裁稿链）——"
 "①轮首快速路径五查静（probe 复跑 05:56：orders 顶 O-20260928-1910 42 件锚未动/ledger 六模式 CaseSensitive 41=锚零新 CEO 令级事件/decisions UTF8 非空行 75 实读·**R726 记账 82 定谳为计数口径漂移非内容丢失**〔D-20260928-01/C-20260928-02/C-20260929-01/02/03/D-20260929-07 逐行核在案=零新行·新锚=75·focus 陈值 82 更正〕/production=open 自愈核在位/无 index.lock·树态=bm-a codex 批未闭让位维持〔README/city-humanities mtime 09-29 04:06 未动=#86 c+d 判据未达·零接触〕+自产 tmp 族预期态）+三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现（阻塞≠失败口径）/loop_health %d FAIL+%d WARN 皆在案类（2 outage 同事件足迹已裁定+tick728 收账自平）；" % (len(fails), warns))
log_r728 += ("②空气预算三道裁链：v2 机械裁 23 字（弄堂派/铺里/那晚/他/也要/铺子下午才开/就给人=压缩分载归卡锚列·b2/b8 三逗长句句拆收口）=60.259s 仍薄超窗 0.259s（-23 字省 4.15s=0.18s/字实证）→R513/R693 防翻窗续裁先例执行 v3 再裁 12 字（北外滩/工位/前的/他说/校准师全归卡承载·粥铺画面保）=**57.615s 定稿入窗 2.385s 余量**（fleet 带内·LC-011 2.24s 同位带）——col2 卡片锚点列 verbatim 零动 12/12 断言过（v1↔v2↔v3 三档）+信条零动+事实数字全保（三十年/一九七五年/微秒/两个徒弟/七十四岁/每周三）+M1 v2/v3 双复检 0 FAIL 0 WARN+口播列 276→240 字符（含标点）+TTS light 定稿音轨 .lc015-tmp/（audio.mp3 57.615s+subs.srt 12 cues+cards.json 基线·--order LC-015-v3·--template=.lc014-tmp/cards.json 链式承继·cyber light+human 42 产线默认·BGM-A 纯净）——v1-v3 beats 全留档；"
 "③操作红三笔如实入账（PS5.1 壳层族）：首飞 TTS 脱壳启动器 Start-Process 相对路径未活（seg 零新写 8min 实证）→.ps1 绝对路径启动器复飞活性实证（seg00 0.6min 刷新）=**脱壳启动器须绝对路径律**+壳层引号吞（python -c 链式分号命令被 PS 解析破）→证据件全走 .py 文件通道+PS `>` 重定向落 UTF-16 BOM（读端 utf-8 崩）→M1 输出改 python 内写文件；"
 "④修红两件：**CON- 根目录 debris 清理**（201853B ffmpeg astats 输出=mtime 09-29 23:33 对位 R711 loudness 探针自产残件·Class-A 可再生·P-13 清理审计面·已删）+**.lc014-tmp E14 闭批收账缺口补 commit**（git ls-files 实证零 tracked vs .lc013-tmp R721 全入对照=R150 批闭收 tmp 升律漏执行·本轮补入）；"
 "⑤台账=lc015 README 生产记录+门禁块+queue §E burn 行+export 刷（OS 行 tick 728+results 728 行+live 三行）；例行件：日报 09-30 在案不重跑（R713 补产）/W40 周审在案（R576）/月度注记在案/global-benchmarks day6 ≤7 跳过（下期 10-01=#80 并窗勿提前触碰）/#70 OSS 窗 2=10-02 21:40 前随轮领（窗面义务足 R644）/#86 c+d 让位判据未达（codex mtime 04:06 未动）/T1 催办=已裁项停用口径/HQ-FEEDBACK 不写（无集团层新 open 问题）·tokens:local=0（M1+TTS=edge-tts 云端免费接口+纯脚本零本地模型调用·S1 qwen=R727 已记账·P-54⑤ 计量律如实记）——"
 "下轮=R729 可领序：①LC-015 渲染腿（R710/R725 同型五步：F-021 卡多模态读→census-card-v2-vertical 派生→对位表 12/12→R-E shipinhao〔拆条 015·源城市图鉴 002〕→S2 三门+帧验三律+全卡几何审计）→收官腿（E8+ASR+E4+M4→F-070→冗余池第十二件→E15 出池）②#70 OSS 窗 2 切片 ③#86 c+d 让位判据 ④global-benchmarks 10-01 刷新——五查锚=orders O-20260928-1910 42·ledger 41（L189/L190/L245 注）·decisions 75（R728 定谳新锚）")
d['log'].append(log_r728)
d['task'] = log_r728[log_r728.find('R728'):][:60]
d['focus'] = ("R729: ①LC-015 渲染腿（R710/R725 同型五步：F-021 卡多模态读→census-card-v2-vertical 派生→对位表 12/12→R-E shipinhao〔拆条 015·源城市图鉴 002〕→S2 三门+帧验三律+全卡几何审计）→收官腿（E8+ASR+E4+M4→F-070→冗余池第十二件→E15 出池）②#70 OSS 窗 2 切片（≤10-02 21:40·切片 1 已毕 R644）③#86 c+d 让位判据（bm-a codex 批闭 commit 落地）④global-benchmarks 10-01 刷新——五查锚=orders O-20260928-1910 42·ledger 41（L189/L190/L245 注）·decisions 75（R728 定谳新锚·82=R726 计数漂移陈值）")
wr(p, json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print('state.json: tick', d['tick'], 'logN', len(d['log']))

# ---------- 4. status-export ----------
p = 'docs/status-export.json'; d = json.loads(rd(p))
d['export_ts'] = NOW + '+08:00'
d['outs'][0][1] = ("tick 728，R728 生产轮·E15 LC-015 朱鸿奎拆条空气预算裁链定稿+TTS 定稿音轨毕（R727 起链承接·实活轮·产品优先律对位=本轮实物增量=LC-015 定稿音轨 57.615s+beats v2/v3 裁稿链）："
 "v2 机械裁 23 字=60.259s 薄超窗 0.259s→R513/R693 防翻窗续裁 v3 再裁 12 字（全归卡承载）=**57.615s 定稿入窗 2.385s 余量**（fleet 带内）+col2 verbatim 零动 12/12 断言+信条零动+事实数字全保+M1 v2/v3 双 0F0W（b2/b8 长句 WARN 销账）+TTS light 定稿音轨 .lc015-tmp/（--order LC-015-v3·链式承继·BGM-A 纯净）；"
 "修红=CON- 根目录 debris 清理（R711 astats 自产残件·Class-A·P-13 审计面）+.lc014-tmp E14 闭批收账缺口补 commit（R150 批闭收 tmp 升律）；decisions 锚定谳=75（R726 记账 82=计数漂移·七新行逐行核在·非内容丢失）；"
 "渲染腿/收官腿随轮领→F-070 登记（冗余池第十二件）；例行件=日报 09-30 在案/W40 周审在案/global-benchmarks day6 ≤7 跳过（10-01=#80 并窗）")
res728 = ["728", log_r728]
d['results'].insert(0, res728)
if len(d['results']) > 40:
    d['results'] = d['results'][:40]
d['live'] = [
 ["当前活：E15 LC-015 朱鸿奎拆条空气预算裁链定稿+TTS 定稿音轨毕（v3 57.615s 入窗 2.385s 余量·col2 零动断言过·M1 0F0W）→渲染腿/收官腿随轮领（lane=E15 active+E16 standby ≥2）"],
 ["最近实物：data/sources/lc015/voiceover-v3.beats.txt（定稿拍稿）+.lc015-tmp/audio.mp3（定稿音轨 57.615s·12 cues·BGM-A 纯净）·2026-09-30 " + NOW],
 ["下个里程碑：LC-015 渲染腿→收官腿 F-070 登记（冗余池第十二件·窗 ≤48h 即 2026-10-02 前）·#70 OSS 窗 2 切片 ≤10-02 21:40·global-benchmarks 7 日刷 10-01·C-20260928-02 义务窗=10-04 记忆 ≤10KB+10-05 C1 席6 确认"]
]
wr(p, json.dumps(d, ensure_ascii=False, indent=1) + '\n')
print('status-export refreshed')
print('ALL DONE', NOW)
