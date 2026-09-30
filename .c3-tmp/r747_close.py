# -*- coding: utf-8 -*-
# R747 LC-019 closeout ledger writer (absorbs R746 WIP; reads .c3-tmp/r747_asr.json)
import io, json, re, sys

A = json.load(io.open('.c3-tmp/r747_asr.json', encoding='utf-8'))

def W(path, text):
    io.open(path, 'w', encoding='utf-8').write(text)
    print('WROTE', path)

def edit(path, old, new, must=1):
    c = io.open(path, encoding='utf-8').read()
    n = c.count(old)
    if n != must:
        print('!! SKIP %s (match=%d expected=%d)' % (path, n, must)); return False
    W(path, c.replace(old, new, 1))
    return True

def append(path, text):
    c = io.open(path, encoding='utf-8').read()
    if not c.endswith('\n'): c += '\n'
    W(path, c + text)
    return True

# ---------- 1. renders README row upgrade ----------
RR_OLD = '**在链件·渲染腿毕（R745·queue §E 批活池 E16 件·冗余扩容位第十六件·源卡=CENSUS-v5 F-024 周浩宇·R743 起链→R744 定稿音轨→R745 渲染腿毕：S2 三门全绿+帧验三律全过+几何审计 problems=NONE·收官腿〔E8+ASR+E4+M4→F-074〕=R746 待领·第十对人物链互证闭环后半件=敬畏验证主题首件位）**'
RR_NEW = ('**成品·落位件·冗余扩容位第十六件（F-074 登记 R747·queue §E 批活池 E16 件收官·源卡=CENSUS-v5 F-024 周浩宇·'
          'R743 起链→R744 定稿音轨→R745 渲染腿→R746 断洞〔E4 8.0 落地+ASR QC 首跑 VAD 掉段 7 cues/1 dropped 诊断〕→R747 收官全链走门毕：'
          'E8 七席 ≥9+ASR 终轨 novad 补覆盖 ' + A['pct'] + ' 字位+E4 8.0+M4·第十对人物链互证闭环后半件=敬畏验证主题首件位）**')
edit('output/renders/README.md', RR_OLD, RR_NEW)

# ---------- 2. finished.md F-074 block ----------
FIN = ('- 2026-09-30: F-074 登记（R747）——**L-卡衍生视频线第十九件=拆条系列节律第十八续件=第十对人物链互证闭环后半件=敬畏验证主题首件位=冗余扩容位第十六件**（queue §E 批活池 E16 件收官）。'
 '**LC-019-v1-shipinhao-60s（拆条 019·源城市图鉴 005）全链走门全档**：源卡=CENSUS-v5 F-024《城市图鉴 005·周浩宇》（R295 登记·E4 8.0 三意愿明说在案）·素材正源=C-00014 手写展示锚（非荣誉席·跨仓只读）。'
 '+R742 出池注记+R743 选优入池（四胜位 over 徐根福：前件点名兑现位 direct=决定位〔LC-018 F-073 当日 ~2h 收官+LC-018 b10 已引 C-00014 关系字段+双卡年轮 09-30 相遇句双端=第十对闭环后半件〕+题材零重复零负担〔讣告 LC-002/LC-012 双重叠+棋三连同构+量化合规三落负担四轮注记——缓解面三件=LC-018 三零断言先例当日承继+差异化角度位敬畏验证主轴+下棋行为字段选材排除〕+跨载体触点徐根福胜位如实注记+源卡双过平位）'
 '+R743 起链（拍稿 v1 12 拍 ≈292 字·逐拍溯源对表·盲评律合规·S1 v1.5+L18-L20 门 10/10 零违律一次过=**拆条系列十八连满分**〔11:02:04 落判·判词档 20260930-110204-S1-script〕·col2 纯 verbatim 零〔〕=R737/R741 剥离案起链前置规避）'
 '+R744 定稿音轨（两道机械裁链 v1 79.696→v2 64.460→**v3 57.235s 定稿 2.765s 余量**·col1/col2 verbatim 零动 12/12 双基断言+信条 verbatim+事实数字〔二十八岁/一万遍〕+互证双名〔徐根福/陈雅雯〕+CTA 受众定位词「敬畏市场」全保·TTS light〔Yunyang+cyber light+human 42·BGM-A 纯净〕）'
 '+R745 渲染腿（F-024 派生源件 census-card-v5-vertical 13.000s+对位表 12/12 visual-ratio 1.00+**R720 律前置修第六件**〔b4/b5/b6/b7 per-card 56/54/50/46+**b8=78 字 fleet 最长 col2 语义预拆 5 段+size 36 下探地板首例**·全卡几何审计 FINAL problems=NONE〕+R-E shipinhao 57.235s 音轨分毫一致·角标拆条 019·源城市图鉴 005+§4.5 三开关+S2 三门全绿〔ai_feel 0F0W CV 0.282/0.291+层 1.8 六面+spec 双 PASS〕+帧验三律全过〔拍头 12/12+段中尾 6/6+回环 crossings={}+AIGC 双标识+b8 专项帧全分辨率实证+tile 误读 ×4 全分辨率定谳+SRT cue9 byte-check 12/12〕）'
 '+R746 断洞〔E4 参考仪 8.0 落地 12:04:04+ASR QC 首跑 VAD 掉段 7 cues/1 dropped 诊断=WIP 全存续〕→R747 收官腿（'
 '**ASR 终轨 novad 全覆盖补读**：R169 QC recipe 参数位 medium-int8+beam5+noctx·vad_filter=False 补覆盖〔R746 首跑 VAD 掉段=**tool-layer finding 首档**：whisper_to_srt.py 硬编码 vad_filter=True 从未属 recipe 文本·R711 型复发第二证·补读非降级〕·HF_HUB_OFFLINE=1·满载机面=他工作区图像生成作业占核·脱壳轮间落地·'
 + A['fin_full'] + '→S2 9.0；'
 '**E4 参考仪 8.0**〔R746 断洞轮落地 12:04:04·e4_call.py 脱壳·三意愿两明一条件〔会看完+点赞/转发条件式「对金融市场和技术感兴趣的朋友」分享对象具名〕·「内容新颖且有创意·科技感×人文关怀」正面定性=拆条带 8.0 回稳位·旗①=「每晚给爹娘报平安」+「他爹说钱的事最讲天理·验一万遍」两句被旗空洞缺关联扣 2=家训+报平安拍 verbatim 卡锚·MC-003 语境门槛族家训位变体·与 ASR 家训拍同句双通道·吸收位=M5 图文页语境+系列语境·最弱=情感深度细节融合〔60s 固有·M6 校准位〕·净本 expert-verdicts/20260930-120404-E4-audience〕'
 '+E8 终审七席全 9.0〔review-20260930-lc019-v1.md·E6=产品优先律+b8 前置专项修=周全性预期律+R746 断洞如实入账=假绿灯律①·E7=对位率 1.00 最高并列+problems=NONE+前置修第六件·E8=零发布后修红=前置预防通道连续第六件〕→M4 完成态）'
 '——**冗余池第十六件落位**（release-schedule v3.1·视频号冗余弹药 16 件=LC-004 F-058~LC-019 F-074·M6 调仓弹药/30 天日更冗余·预产窗=开号前）+queue §E E16 出池（lane=E20 徐根福 standby 单条<2·补池义务随轮领=R726 先例）·发布锁=M5 账号物理件不变（未上线=未测量）。\n')
append('output/finished.md', FIN)

# ---------- 3. release-schedule v3.1 ----------
RS = ('- v3.1 2026-09-30 R747：**冗余池扩容第十六件视频入池**（LC-019《城市图鉴 005·周浩宇》拆条=F-074·成品库 73→74 件·L-卡衍生视频线第十九件=拆条系列节律第十八续件·'
 '**第十对人物链互证闭环后半件**〔陈雅雯×周浩宇「最怕又最服」对·LC-018 b10 关系字段点名直连+双卡年轮 09-30 相遇句双端=系列最快直连〕+**敬畏验证主题首件位**〔28 岁最年轻策略研究员×全城唯一讣告写手=差异化角度位·信条「回撤教人做人，行情教人谦虚」·量化近域三零断言承继件〕·'
 'R742 出池注记→R743 选优入池〔S1 10/10 十八连满分〕→R744 定稿音轨〔两道裁链 57.235s 2.765s 余量〕→R745 渲染腿〔**b8=78 字 fleet 最长 col2 语义预拆+size 36 下探地板首例=R720 律预执行第六件**·全卡几何审计 problems=NONE〕→R746 断洞〔E4 8.0 落地+ASR VAD 掉段诊断〕→R747 收官全链走门：ASR 终轨 novad 补覆盖 ' + A['pct'] + ' 字位〔**tool-layer finding 首档**·字幕轨 12/12 零损兜底〕+E4 8.0〔旗①=家训位语境门槛族变体〕+七席 ≥9→M4）；§四 盘点行同步（视频号冗余弹药 15→16 件·M6 调仓/日更冗余·预产窗=开号前）。\n')
append('docs/release-schedule-v1.md', RS)

# ---------- 4. queue E16 closeout row ----------
QU = ('- 2026-09-30: **E16 收官毕（R747·F-074 登记=成品库第七十四件·冗余池第十六件落位 release-schedule v3.1·视频号冗余弹药 16 件·第十对人物链互证闭环后半件=敬畏验证主题首件位〔'
 'R746 断洞承接：E4 8.0 断洞轮落地+ASR QC 首跑 VAD 掉段 7 cues/1 dropped=R711 型复发第二证·novad 全覆盖补读=**tool-layer finding 首档**（whisper_to_srt.py 硬编码 vad_filter=True 从未属 R169 recipe 文本·补读非降级·--no-vad CLI 选项位=工具面修复候选提案）〕·'
 '收官=E8 七席 ≥9+E4 8.0〔三意愿两明一条件·旗①=家训位语境门槛族变体〕+ASR 终轨 novad 补读 ' + A['pct'] + ' 字位〔' + A['fin_short'] + '〕·字幕轨 edge-tts 12/12 零损兜底〕）'
 '→E16 出池（lane=E20 徐根福 standby 单条<2·**补池义务随轮领**=R726 先例·候选=未拆存量卡〔CENSUS 库 C-00012 沈佩兰 等〕/BS-007 稿集件/徐根福前件直连位随选优轮评估）**\n')
append('docs/self-improvement-queue.md', QU)

# ---------- 5. station-reviews R747 row ----------
SR = ('| 2026-09-30 | **收官腿机检包（lc-019-v1-shipinhao=queue §E 批活池 E16 件收官·冗余扩容位第十六件·R746 断洞+R747 承接：ASR 终轨 novad 补覆盖+E4 参考仪+E8 评审单+M4→F-074 登记）** | '
 'lc-019-v1-shipinhao-60s.mp4（57.235s·音轨分毫一致 2.765s 余量）+.lc019-tmp/asr-check-novad.srt+asr-diff-r746.txt（R169 QC recipe 参数位 medium-int8+beam5+noctx·vad_filter=False 补覆盖〔R746 首跑 VAD 掉段 7 cues/1 dropped=tool-layer finding：whisper_to_srt.py 硬编码 vad_filter=True 非 recipe 文本·R711 型复发第二证〕·满载机面=他工作区图像生成作业占核·脱壳轮间落地） | '
 'ASR 终轨（faster-whisper 本地）+E4（Ollama qwen2.5:14b 本地·e4_call.py 脱壳 12:04:04 落地=R746 断洞轮）+E8 评审单 review-20260930-lc019-v1.md | ——（收官档） | '
 'ASR=' + A['sr_note'] + '+E4 8.0（三意愿两明一条件·旗①=家训+报平安拍=MC-003 语境门槛族家训位变体·最弱=情感深度细节融合·净本 20260930-120404-E4-audience）+E8 七席全 9.0→M4 完成态→F-074 登记=成品库第七十四件+冗余池第十六件落位 release-schedule v3.1 |\n')
append('docs/reviews/station-reviews.md', SR)

# ---------- 6. lc019 README gate update + prod record ----------
edit('data/sources/lc019/README.md',
     '·收官腿=待领（E8+ASR+E4+M4→F-074 登记→冗余池第十六件→E16 出池+补池）。',
     '·**收官腿=R746 断洞+R747 承接毕**（E4 8.0〔R746 落地 12:04:04〕+ASR 终轨 novad 补覆盖〔R746 首跑 VAD 掉段 7 cues/1 dropped=tool-layer finding 首档〕+E8 七席 ≥9+M4→**F-074 登记=成品库第七十四件**→冗余池第十六件→E16 出池）。')
append('data/sources/lc019/README.md',
       '- [2026-09-30 12:5x R746 断洞+R747 收官腿毕（R726/R730/R734/R738/R742 同型）] R746 收官腿被 25min 硬帽杀于 ASR 段（E4 参考仪 8.0 已落地 12:04:04 判词档 20260930-120404-E4-audience 净本存档+ASR QC 首跑 7 cues/1 dropped=VAD 掉段 b7-b10 27.667-47.516s 稳定丢失·R711 型复发第二证·vad_diag/novad/diff 诊断脚本备妥）→R747 承接：满载机面定谳=他工作区图像生成作业占核→novad 补覆盖脱壳重飞轮间落地→**ASR 终轨 ' + A['pct'] + ' 字位**（' + A['fin_short'] + '·字幕轨 edge-tts 12/12 零损兜底）→S2 9.0+E4 8.0 回填+E8 七席全 9.0（review-20260930-lc019-v1.md）→M4→F-074 登记=成品库第七十四件+冗余池第十六件（release-schedule v3.1）。\n')

# ---------- 7. state.json ----------
R746 = ('2026-09-30 12:3x R746 断洞修复（账目·R747 承办·R712/R714/R718/R720/R722 先例）：11:5x 起跑轮（R745 收账 11:51 后）被 25 分钟硬帽杀于收官腿中段零 state 写盘'
 '（可见足迹=r746_launch.ps1 12:03:58+ASR QC 首跑 12:05:36=7 cues/1 dropped〔VAD 掉段·b7-b10 27.667-47.516s 稳定丢失=R711 型复发第二证〕+e4_call.py E4 参考仪 8.0 落判 12:04:04+判词净本 expert-verdicts/20260930-120404-E4-audience+probe-seg-mid.wav 12:08:51+r746_vad_diag.py 12:14:47+r746_asr_novad.py 12:21:37+r746_asr_diff.py 12:22:11 诊断与补覆盖通道备妥后被杀·round.lock 由启动器硬帽回收·台账零落笔）'
 '——盘上 WIP=E4 判词档（净本已存档）+ASR VAD 诊断+novad 补覆盖脚本全部由 R747 吸收复核零重做，tick 745→747 断洞双记（R689/R690/R712/R713/R714/R715 先例）。')
R747 = ('2026-09-30 ' + A['ts_hm'] + ' R747: 生产轮·LC-019 周浩宇拆条收官腿毕=F-074 登记+冗余池第十六件落位（queue §E 批活池 E16 件收官·R746 断洞承接·R726/R730/R734/R738/R742 同型·实活轮·产品优先律 P-20260929-07 对位=本轮新实物=lc-019 成片 F-074 入成品库）'
 '——①轮首快速路径五查静（r694_probe 口径：orders 顶 O-20260928-1910 42 件锚未动/ledger 六模式 CaseSensitive 41=锚零新 CEO 令级事件/decisions UTF8 非空行 75=锚零新行/production=open 自愈核在位 tick745/无 index.lock·树态=bm-a codex 批未闭让位维持〔README/city-humanities mtime 09-29 04:06 未动=#86 c+d 判据未达·两文件零接触〕+R746 断洞 WIP=自产预期态）'
 '+三探针=board 0 FAIL/readiness 3 阻塞皆外部 CEO 面+1 发现（render-unannot lc-019=在链预期红·R730/R734/R738/R742 同型·F-074 登记+renders 行升成品即清）/loop_health 2 FAIL+WARN 皆在案史实类（tick747 断洞双记自平）；'
 '②满载机面定谳=他工作区 2dlive-spike c4_gen13b.py 图像生成作业（PID 61704·12:21:06 起·CPU 2239s+）占核=ASR 首跑直挂 5min 零输出根因〔R746 vad_diag 5.5min 零输出同源·零接触不杀〕→长任务脱壳律 R176/R195+r747 novad 重飞（绝对路径启动器=R728 律·首飞 CWD 笔误即改）；'
 '③ASR 终轨 novad 全覆盖补读〔R746 首跑 VAD 掉段定谳=whisper_to_srt.py 硬编码 vad_filter=True 从未属 R169 recipe 文本=**tool-layer finding 首档**·R711 型复发第二证·novad 参数位 medium-int8+beam5+noctx 全同=补读非降级·--no-vad CLI 选项位=工具面修复候选提案〕：'
 + A['fin_full'] + '→S2 9.0；'
 '④E4 参考仪回填 8.0（R746 断洞轮落地 12:04:04·e4_call.py 脱壳·三意愿两明一条件〔会看完+点赞/转发条件式「对金融市场和技术感兴趣的朋友」分享对象具名〕·「内容新颖且有创意·科技感×人文关怀」正面定性=拆条带 8.0 回稳位·旗①=「每晚给爹娘报平安」+「他爹说钱的事最讲天理·验一万遍」两句被旗空洞缺关联扣 2=家训+报平安拍 verbatim 卡锚·MC-003 语境门槛族家训位变体·与 ASR 家训拍同句双通道·吸收位=M5 图文页语境+系列语境·最弱=情感深度细节融合〔60s 固有·M6 校准位〕·净本 expert-verdicts/20260930-120404-E4-audience）；'
 '⑤E8 评审单 review-20260930-lc019-v1.md（S1 10/10〔R743 十八连满分〕+S2 9.0+S3 9.0+S4 9.0+终审七席全 9.0·E6=产品优先律+b8 fleet 最长 col2 前置专项修=周全性预期律+R746 断洞如实入账=假绿灯律①·E7=对位率 1.00 最高并列+problems=NONE+前置修第六件·E8=零发布后修红=前置预防通道连续第六件）→M4 完成态；'
 '⑥F-074 登记（成品库第七十四件·L-卡衍生视频线第十九件=拆条系列节律第十八续件=第十对人物链互证闭环后半件=敬畏验证主题首件位）+冗余池第十六件落位（release-schedule v3.1·视频号冗余弹药 16 件）+renders 行升「成品·落位」+lc019 README 收口+station-reviews R747 行+queue §E E16 出池（lane=E20 徐根福 standby 单条<2·补池义务随轮领=R726 先例·候选=未拆存量卡/BS-007 稿集件随选优轮评估）+.lc019-tmp 批闭收账全批入 git（R721/R742 先例）；'
 '⑦例行件：日报 09-30 在案不重跑（R713 补产）/W40 周审在案（R576）/global-benchmarks day6 ≤7 跳过（10-01=#80 并窗勿提前触碰）/#70 OSS 窗 2=10-02 21:40 前随轮领（R644 切片 1 在案）/#86 c+d 判据未达（codex mtime 04:06 未动）/T1 催办=已裁项停用口径/HQ-FEEDBACK 不写（无集团层新 open 问题·双锚静零膨胀）·'
 'tokens:local=5（faster-whisper medium ×4〔R746 首跑/R746 vad_diag 诊断半程/R747 直挂自动取消/novad 补覆盖·满载机面三空转实况如实记〕+E4 qwen2.5:14b ×1=R746 起飞落地补记账·全本地零 API token·P-54⑤ 计量律如实记）'
 '——下轮=R748 可领序：①queue §E 补池义务（lane<2·选优轮评估：未拆存量卡/BS-007 稿集件/徐根福前件直连位）②#70 OSS 窗 2 切片（≤10-02 21:40）③#86 c+d 让位判据④global-benchmarks 10-01 刷新（#80 并窗）。收账显式列文件 commit+push')

c = io.open('src/os/state.json', encoding='utf-8').read()
anchor = '"\n ],\n "ts":'
if c.count(anchor) != 1:
    print('!! state.json anchor mismatch=%d' % c.count(anchor)); sys.exit(1)
c = c.replace(anchor, '",\n  "' + R746.replace('\\', '\\\\').replace('"', '\\"') + '",\n  "' + R747.replace('\\', '\\\\').replace('"', '\\"') + '"\n ],\n "ts":', 1)
c = c.replace('"tick": 745,', '"tick": 747,', 1)
# focus
m = re.search(r'"focus": "R746: [^"]*"', c)
if not m: print('!! focus not found'); sys.exit(1)
FOCUS = ('R748: ①queue §E 补池义务（lane=E20 徐根福 standby 单条<2·选优轮评估：未拆存量卡〔CENSUS 库 C-00012 沈佩兰 等〕/BS-007 稿集件/徐根福前件直连位=LC-019 b10 埋点兑现·随选优定谳入池）'
         '②#70 OSS 窗 2 切片（≤10-02 21:40·R644 切片 1 在案）③#86 c+d 让位判据（bm-a codex 批闭 commit 落地）④global-benchmarks 10-01 刷新（#80 并窗）'
         '——五查锚=orders O-20260928-1910 42·ledger 41（L189/L190/L245 注）·decisions 75')
c = c[:m.start()] + '"focus": "' + FOCUS + '"' + c[m.end():]
# ts + task
c = re.sub(r'"ts": "2026-09-30 11:51:11",', '"ts": "' + A['ts_full'] + '",', c, count=1)
task_line = R747.split('R747: ', 1)[1][:60]
m2 = re.search(r'"task": "[^"]*"', c)
c = c[:m2.start()] + '"task": "R747: ' + task_line.replace('\\', '\\\\').replace('"', '\\"') + '"' + c[m2.end():]
W('src/os/state.json', c)

# ---------- 8. status-export.json ----------
E = json.load(io.open('docs/status-export.json', encoding='utf-8'))
E['export_ts'] = A['ts_full']
E['outs'][0][2] = ('tick 747，R747 生产轮·LC-019 周浩宇拆条收官腿毕=F-074 登记+冗余池第十六件落位（产品优先律对位=本轮实物增量=lc-019 成片 F-074 入成品库 74 件·'
 'R746 断洞承接：E4 8.0 断洞轮落地+ASR QC 首跑 VAD 掉段=tool-layer finding 首档→novad 全覆盖补读 ' + A['pct'] + ' 字位·E8 七席 ≥9+M4）'
 '——lane=E20 徐根福 standby 单条<2·补池义务随轮领·发布锁=M5 账号物理件不变（未上线=未测量）')
E['results'].insert(0, ['747', R747])
E['live'] = [
 ['当前活：LC-019 周浩宇拆条收官腿毕（R747）——F-074 登记=成品库第七十四件·冗余池第十六件落位（视频号冗余弹药 16 件）·lane=E20 徐根福 standby 单条<2·补池义务随轮领'],
 ['最近实物：lc-019-v1-shipinhao-60s.mp4 成品落位 output/renders/（57.235s·2026-09-30 ' + A['ts_hm'] + '）+评审单 review-20260930-lc019-v1.md+E4 判词档 20260930-120404'],
 ['下个里程碑：queue §E 补池选优入池（≤48h 窗·lane<2）·#70 OSS 窗 2 切片（≤10-02 21:40）·global-benchmarks 7 日刷（10-01 #80 并窗）'],
]
W('docs/status-export.json', json.dumps(E, ensure_ascii=False, indent=1) + '\n')

print('CLOSEOUT_OK')
