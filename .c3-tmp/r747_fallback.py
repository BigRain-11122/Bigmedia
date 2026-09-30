# -*- coding: utf-8 -*-
# R747 fallback close: gap-hole fix + half-closeout honest accounting (F-074 deferred to R748)
import io, json, re, sys

TS_FULL = '2026-09-30 12:55:00'
TS_HM = '12:5x'

def W(path, text):
    io.open(path, 'w', encoding='utf-8').write(text)
    print('WROTE', path)

R746 = ('2026-09-30 12:3x R746 断洞修复（账目·R747 承办·R712/R714/R718/R720/R722 先例）：11:5x 起跑轮（R745 收账 11:51 后）被 25 分钟硬帽杀于收官腿中段零 state 写盘'
 '（可见足迹=r746_launch.ps1 12:03:58+ASR QC 首跑 12:05:36=7 cues/1 dropped〔b6-b10 区 26.94-47.54s 丢段·当时归因 VAD〕+e4_call.py E4 参考仪 8.0 落判 12:04:04+判词净本 expert-verdicts/20260930-120404-E4-audience+'
 'probe-seg-mid.wav 12:08:51+r746_vad_diag.py 12:14:47〔两跑对照诊断半程被杀〕+r746_asr_novad.py 12:21:37+r746_asr_diff.py 12:22:11 诊断与补覆盖脚本备妥后被杀·round.lock 由启动器硬帽回收·台账零落笔·expert-calls 行亦未落=R748 回填位）'
 '——盘上 WIP=E4 判词档（净本已存档）+VAD 诊断+novad 补覆盖脚本全部由 R747 吸收复核零重做，tick 745→747 断洞双记（R689/R690/R712/R713/R714/R715 先例）。')
R747 = ('2026-09-30 ' + TS_HM + ' R747: 生产轮·LC-019 周浩宇拆条收官腿半程=断洞修复+E4 吸收+ASR 双跑通道定谳（queue §E E16 件收官顺延 R748·R746 断洞承接·实活轮·产品优先律对位=本轮新实物=ASR 双跑证据链+诊断定谳在案·F-074 未登记=如实记）'
 '——①轮首快速路径五查静（r694_probe 口径：orders 顶 O-20260928-1910 42 件锚未动/ledger 六模式 CaseSensitive 41=锚零新 CEO 令级事件/decisions UTF8 非空行 75=锚零新行/production=open 自愈核在位 tick745/无 index.lock·树态=bm-a codex 批未闭让位维持〔README/city-humanities mtime 09-29 04:06 未动=#86 c+d 判据未达·两文件零接触〕+R746 断洞 WIP=自产预期态）'
 '+三探针=board 0 FAIL/readiness 3 阻塞皆外部 CEO 面+1 发现（render-unannot lc-019=在链预期红·F-074 登记即清·本轮未清如实）/loop_health 2 FAIL+WARN 皆在案史实类（tick747 断洞双记自平）；'
 '②满载机面定谳=他工作区 2dlive-spike c4_gen13b.py 图像生成作业（PID 61704·12:21:06 起·CPU 2239s+）占核=R746 vad_diag 5.5min 零输出+本循环直挂 5min 零输出的根因〔零接触不杀·如实记〕→长任务脱壳律 R176/R195+绝对路径启动器重飞（R728 律·首飞 CWD 笔误即改实证）；'
 '③E4 参考仪吸收=8.0（R746 断洞轮 12:04:04 落地·e4_call.py 脱壳·三意愿两明一条件〔会看完+点赞/转发条件式「对金融市场和技术感兴趣的朋友」分享对象具名〕·「内容新颖且有创意·科技感×人文关怀」正面定性=拆条带 8.0 回稳位·'
 '旗①=「每晚给爹娘报平安」+「他爹说钱的事最讲天理·策略就是把道理验一万遍」两句被旗空洞缺直接关联扣 2=家训+报平安拍 verbatim 卡锚·MC-003 语境门槛族**家训位变体**·吸收位=M5 图文页语境+系列语境·最弱=情感深度和细节描绘〔60s 固有·M6 校准位〕·净本 expert-verdicts/20260930-120404-E4-audience·expert-calls 行=R748 回填位）；'
 '④ASR 双跑通道定谳（本Round 实物证据链）：QC 首跑〔R746·vad_filter=True〕=7 cues/1 dropped〔26.94→47.54s 丢段〕→novad 补覆盖重飞〔R747·vad_filter=False·12:41 脱壳 12:50 落地 asr-check-novad.srt〕=**7 cues/1 dropped 同形定谳**〔两跑确定性同间隙·b6-b10 区 20.6s 稳定丢失〕→'
 '**VAD 因果假设证伪**〔R746 novad 通道设计前提=vad_filter=True 为根因·两跑同形否定之·假设更正留痕〕→真根因=模型层对该音轨中段的确定性跳段=**R711 型完全同族**〔R711：整轨 run1=run2 确定性 6 cues 27-54s 丢段+三探针定谳音轨完好+两段拼接 12 cues 全覆盖根修=R638/R701 通道先例〕→**下通道=R711 两段拼接**（split ~30s 两半各自转写拼接 12 cues 全覆盖·满载机面下两段 ~8-15min=R748 首位）；'
 '⑤WIP 保护盘上存续=R748 吸收零重做清单：评审单草稿 .c3-tmp/r747_review_draft.md（ASR 位占位符·**S2 口径含已证伪的 VAD 因果框=R748 按两段拼接定谳重写后落 docs/reviews/**）+收官脚本套件 .c3-tmp/r747_close.py/r747_review.py（读 r747_asr.json 填数·同须先修正 ASR 口径文本）+E4 判词档净本+asr-check.srt/asr-check-novad.srt 双证据件；'
 '⑥例行件：日报 09-30 在案不重跑（R713 补产）/W40 周审在案（R576）/global-benchmarks day6 ≤7 跳过（10-01=#80 并窗勿提前触碰）/#70 OSS 窗 2=10-02 21:40 前随轮领（R644 切片 1 在案）/#86 c+d 判据未达（codex mtime 04:06 未动）/T1 催办=已裁项停用口径/HQ-FEEDBACK 不写（无集团层新 open 问题·双锚静零膨胀）·'
 'tokens:local=5（faster-whisper medium ×4〔R746 首跑 7c/R746 vad_diag 半程被杀/R747 直挂 5min 自动取消/novad 落地 7c·满载机面空转实况如实记〕+E4 qwen2.5:14b ×1=R746 起飞落地补记账·全本地零 API token·P-54⑤ 计量律如实记）'
 '——下轮=R748 可领序：①LC-019 收官腿续（R711 两段拼接 ASR 通道→S2 9.0→评审单/收官脚本套件口径修正后跑→F-074 登记→冗余池第十六件→E16 出池+补池义务·expert-calls E4 行回填）②queue §E 补池义务（lane=E20 单条<2·选优轮评估）③#70 OSS 窗 2 切片（≤10-02 21:40）④#86 c+d 让位判据⑤global-benchmarks 10-01 刷新（#80 并窗）。收账显式列文件 commit+push')

c = io.open('src/os/state.json', encoding='utf-8').read()
anchor = '"\n ],\n "ts":'
if c.count(anchor) != 1:
    print('!! anchor=%d' % c.count(anchor)); sys.exit(1)
ins = '",\n  "' + R746.replace('\\', '\\\\').replace('"', '\\"') + '",\n  "' + R747.replace('\\', '\\\\').replace('"', '\\"') + '"\n ],\n "ts":'
c = c.replace(anchor, ins, 1)
c = c.replace('"tick": 745,', '"tick": 747,', 1)
m = re.search(r'"focus": "R746: [^"]*"', c)
if not m: print('!! focus'); sys.exit(1)
FOCUS = ('R748: ①LC-019 收官腿续（R711 两段拼接 ASR 通道：audio.mp3 split ~30s 两半转写拼接 12 cues→S2 9.0→r747_review_draft/close/review 脚本套件 ASR 口径修正'
         '〔已证伪 VAD 因果框→R711 型确定性跳段+两段拼接根修〕后跑→E8 七席→M4→F-074 登记→冗余池第十六件落位 release-schedule v3.1→E16 出池+补池义务〔lane=E20 徐根福 standby 单条<2·候选=未拆存量卡/BS-007 稿集件/前件直连位随选优轮评估〕+expert-calls E4 行回填）'
         '②#70 OSS 窗 2 切片（≤10-02 21:40·R644 切片 1 在案）③#86 c+d 让位判据（bm-a codex 批闭 commit 落地）④global-benchmarks 10-01 刷新（#80 并窗）'
         '——五查锚=orders O-20260928-1910 42·ledger 41（L189/L190/L245 注）·decisions 75')
c = c[:m.start()] + '"focus": "' + FOCUS + '"' + c[m.end():]
c = re.sub(r'"ts": "2026-09-30 11:51:11",', '"ts": "' + TS_FULL + '",', c, count=1)
task_line = R747.split('R747: ', 1)[1][:60]
m2 = re.search(r'"task": "[^"]*"', c)
c = c[:m2.start()] + '"task": "R747: ' + task_line.replace('\\', '\\\\').replace('"', '\\"') + '"' + c[m2.end():]
W('src/os/state.json', c)

E = json.load(io.open('docs/status-export.json', encoding='utf-8'))
E['export_ts'] = TS_FULL
E['outs'][0][2] = ('tick 747，R747 收官腿半程：E4 8.0（R746 断洞轮落地）吸收+ASR 双跑通道定谳——QC 首跑与 novad 补覆盖同形 7 cues/1 dropped（26.94→47.54s 确定性丢段）'
 '=VAD 因果假设证伪·真根因=R711 型模型层确定性跳段→下通道=R711 两段拼接（R638/R701 先例）=R748 首位；F-074 未登记=收官顺延 R748（评审单草稿+收官脚本套件 WIP 在盘）·'
 'lane=E20 徐根福 standby 单条<2·发布锁=M5 账号物理件不变（未上线=未测量）')
E['results'].insert(0, ['747', R747])
E['live'] = [
 ['当前活：LC-019 周浩宇拆条收官腿半程毕（R747）——E4 8.0 吸收+ASR 双跑定谳（VAD 假设证伪·R711 两段拼接=R748 首位）·F-074 登记顺延 R748'],
 ['最近实物：ASR 双跑证据件 .lc019-tmp/asr-check.srt+asr-check-novad.srt（7c 同形·2026-09-30 12:50）+E4 判词净本 expert-verdicts/20260930-120404-E4-audience.md+lc-019-v1-shipinhao-60s.mp4 成片在链（R745·57.235s）'],
 ['下个里程碑：LC-019 F-074 登记（≤48h 窗·R748 两段拼接通道）·#70 OSS 窗 2 切片（≤10-02 21:40）·global-benchmarks 7 日刷（10-01 #80 并窗）'],
]
W('docs/status-export.json', json.dumps(E, ensure_ascii=False, indent=1) + '\n')
print('FALLBACK_CLOSE_OK')
