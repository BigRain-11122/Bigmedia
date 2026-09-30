# -*- coding: utf-8 -*-
# R748 LC-019 closeout: (1) finalize review doc (two-segment splice wording, R747 novad
# causal frame falsified per R747 dual-run), (2) ledger writes F-074 registration,
# (3) state.json tick 748 + log + focus, (4) status-export refresh.
import io, json, re, sys
from datetime import datetime

NOW = datetime.now()
TS_FULL = NOW.strftime('%Y-%m-%d %H:%M:%S')
TS_HM = NOW.strftime('%H:%M')

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

# ============ 1. review doc finalize ============
d = io.open('.c3-tmp/r747_review_draft.md', encoding='utf-8').read()

# A. chain-integrity note
A_OLD = '→R747 收官腿〔断洞承接=no-VAD 全覆盖补读+diff 量化〕——五轮链含一断洞如实入账（R712-R721 先例族·假绿灯律① 执法面）。'
A_NEW = ('→R747 半程收官腿〔ASR 双跑证伪 VAD 因果：QC vad=True 与 novad vad=False 双跑同形 7 cues/1 dropped·稳定跳段 26.94-47.54s=模型层确定性跳段定谳（R711 型同族）〕'
         '→R748 收官腿〔断洞承接=**R711 型两段拼接根修**+diff 量化〕——六轮链含一断洞如实入账（R712-R721 先例族·假绿灯律① 执法面）。')
if d.count(A_OLD) != 1: print('!! A mismatch', d.count(A_OLD)); sys.exit(1)
d = d.replace(A_OLD, A_NEW, 1)

# B. S2 score cell
B_OLD = '**9.0**（R747 ASR 终轨·novad 全覆盖补读〔R746 QC recipe 首跑 VAD 掉段=7 cues/1 dropped·b7-b10 27.667-47.516s 稳定丢失=R711 型复发+**tool-layer finding=whisper_to_srt.py 硬编码 vad_filter=True 从未属 R169 recipe 文本**·novad 通道补读全 cues〕）'
B_NEW = ('**9.0**（R748 ASR 终轨·R711 型两段拼接全覆盖〔R746 QC vad=True 首跑与 R747 novad vad=False 双跑同形 7 cues/1 dropped·稳定跳段 26.94-47.54s=VAD 因果证伪→模型层确定性跳段定谳；'
         'R748 隔窗 26.7-47.8s 转写 4 cues dropped=0+QC 整轨头 5 cues+尾 2 cues=**11 cues 全覆盖拼接**（R638/R701 根修-再飞先例·asr-check-run1.srt QC 证据件留档）〕）')
if d.count(B_OLD) != 1: print('!! B mismatch', d.count(B_OLD)); sys.exit(1)
d = d.replace(B_OLD, B_NEW, 1)

# C. S2 evidence cell
C_OLD = 'ASR 事实词核验（R169 QC recipe 参数位 medium-int8+beam5+noctx·vad_filter=False 补覆盖·HF_HUB_OFFLINE=1·满载机面=他工作区 2dlive-spike c4_gen13b 图像生成作业占核·脱壳轮间落地）：【ASR-量化行：sites/diff/ref 字位=系列带位读数·关键存活清单·实质退化清单·字幕轨=edge-tts 直出 12/12 零损兜底】'
C_NEW = ('ASR 事实词核验（R169 QC recipe medium-int8+beam5+noctx·两段拼接通道·HF_HUB_OFFLINE=1·asr-check.srt 11 cues 全覆盖+asr-diff-r748.txt）：'
         '=30 sites/88 diff chars/196 字≈**44.9% 字位=系列带上缘之上新峰**（LC-015 43.2% 峰上再升·量化词域+专名密度件）：'
         '关键存活（策略研究员/泡面/工位/尾音/饭都能忘/报平安/天理/验一万遍/多打一勺/二十八了/最怕也最服/信条/行情…谦虚/公众号/「敬畏市场」CTA 定位词+数字形差值存活〔二十八→28〕+周浩/宇专名分 cue 值存活）'
         '+实质退化如实（hook 双损〔全城→玄城+讣告→报告=hook 位损族〕/QUANT→晃土+扭塔→牛塔=专名损/盯盘→冰盘+百毒不侵→摆渡不清/敬畏→静谓〔b5 位〕=信条前字损/钻到底→算到底+章硬→张应=问题拍组损/川渝腔→穿鱼腔=方言锚损/'
         '徐根福→徐敦福+陈雅雯→陈亚文+风控官→封控官=互证拍三连损/回撤教人→回车叫人=信条核心字损/长身体→涨身体/全档案→全答案=CTA 档案族第十二发/碳基→探机=物种行损族第十六证/尾插入「他们的信条回」=处理尾残响）'
         '·字幕轨=edge-tts 直出 12/12 零损兜底')
if d.count(C_OLD) != 1: print('!! C mismatch', d.count(C_OLD)); sys.exit(1)
d = d.replace(C_OLD, C_NEW, 1)

# D. E6 row
D_OLD = '（E4 判词档+novad 通道盘上存续·断洞承接零重做=假绿灯律① 执法面）'
D_NEW = '（E4 判词档+双跑诊断与拼接证据件盘上存续·断洞承接零重做=假绿灯律① 执法面）'
if d.count(D_OLD) != 1: print('!! D mismatch', d.count(D_OLD)); sys.exit(1)
d = d.replace(D_OLD, D_NEW, 1)

# E. verdict ASR note
E_OLD = '- **ASR 口径注记（如实全档）**：【ASR-注记行：novad 补覆盖=tool-layer finding 首档〔whisper_to_srt.py 硬编码 vad_filter=True 非R169 recipe 文本·本件 b7-b10 稳定掉段=R711 型复发第二证·novad 通道=补读非降级（参数位 medium-int8+beam5+noctx 全同）·工具面修复候选=--no-vad CLI 选项位提案随行〕；关键正面+实质退化清单全档；发布轨字幕=edge-tts 直出 12/12 零损】。'
E_NEW = ('- **ASR 口径注记（如实全档）**：两段拼接根修=R711 型 model-layer 确定性跳段处置正法〔R746 QC vad=True 与 R747 novad vad=False 双跑同形证伪 VAD 因果·跳段 26.94-47.54s 稳定复现；'
         'R748 隔窗转写 4 cues dropped=0+头尾拼接=11 cues 全覆盖·R638/R701 根修-再飞先例·asr-check-run1.srt/-novad.srt 双证据件留档〕；'
         '44.9% 字位=系列带新峰（量化词域+专名密度件·关键正面+实质退化清单全档）；互证拍三连损=双名+职衔同音形损（字幕轨兜底在位）；发布轨字幕=edge-tts 直出 12/12 零损。')
if d.count(E_OLD) != 1: print('!! E mismatch', d.count(E_OLD)); sys.exit(1)
d = d.replace(E_OLD, E_NEW, 1)

# F. changelog
F_OLD = '- 2026-09-30: v1.0（R747）——S1 10/10（R743·十八连满分）/S2 9.0（R747 ASR 终轨·【novad 补覆盖读数】）/S3 9.0/S4 9.0+终审七席全 9.0（E4 8.0 R746 断洞轮落地·旗①=家训位语境门槛族变体）→ M4 完成态→F-074 登记+冗余池第十六件落位（release-schedule v3.1）。'
F_NEW = '- 2026-09-30: v1.0（R748）——S1 10/10（R743·十八连满分）/S2 9.0（R748 ASR 终轨·R711 型两段拼接全覆盖 44.9% 字位=系列带新峰）/S3 9.0/S4 9.0+终审七席全 9.0（E4 8.0 R746 断洞轮落地·旗①=家训位语境门槛族变体）→ M4 完成态→F-074 登记+冗余池第十六件落位（release-schedule v3.1·R748）。'
if d.count(F_OLD) != 1: print('!! F mismatch', d.count(F_OLD)); sys.exit(1)
d = d.replace(F_OLD, F_NEW, 1)

assert '【' not in d, 'unfilled placeholder: ' + [l for l in d.splitlines() if '【' in l][0][:200]
assert 'novad 全覆盖' not in d and 'novad 通道补读全 cues' not in d, 'falsified frame remains'
W('docs/reviews/review-20260930-lc019-v1.md', d)
print('REVIEW_OK')

# ============ 2. renders README row upgrade ============
RR_OLD = '**在链件·渲染腿毕（R745·queue §E 批活池 E16 件·冗余扩容位第十六件·源卡=CENSUS-v5 F-024 周浩宇·R743 起链→R744 定稿音轨→R745 渲染腿毕：S2 三门全绿+帧验三律全过+几何审计 problems=NONE·收官腿〔E8+ASR+E4+M4→F-074〕=R746 待领·第十对人物链互证闭环后半件=敬畏验证主题首件位）**'
RR_NEW = ('**成品·落位件·冗余扩容位第十六件（F-074 登记 R748·queue §E 批活池 E16 件收官·源卡=CENSUS-v5 F-024 周浩宇·'
          'R743 起链→R744 定稿音轨→R745 渲染腿→R746 断洞〔E4 8.0 落地+ASR QC 首跑 7 cues/1 dropped 诊断〕→R747 半程〔双跑证伪 VAD 因果〕'
          '→R748 收官全链走门毕：E8 七席 ≥9+ASR 终轨 R711 型两段拼接 44.9% 字位+E4 8.0+M4·第十对人物链互证闭环后半件=敬畏验证主题首件位）**')
edit('output/renders/README.md', RR_OLD, RR_NEW)

# ============ 3. finished.md F-074 ============
FIN = ('- 2026-09-30: F-074 登记（R748）——**L-卡衍生视频线第十九件=拆条系列节律第十八续件=第十对人物链互证闭环后半件=敬畏验证主题首件位=冗余扩容位第十六件**（queue §E 批活池 E16 件收官）。'
 '**LC-019-v1-shipinhao-60s（拆条 019·源城市图鉴 005）全链走门全档**：源卡=CENSUS-v5 F-024《城市图鉴 005·周浩宇》（R295 登记·E4 8.0 三意愿明说在案）·素材正源=C-00014 手写展示锚（非荣誉席·跨仓只读）。'
 '+R742 出池注记+R743 选优入池（四胜位 over 徐根福：前件点名兑现位 direct=决定位〔LC-018 F-073 当日 ~2h 收官+LC-018 b10 已引 C-00014 关系字段+双卡年轮 09-30 相遇句双端=第十对闭环后半件〕+题材零重复零负担〔讣告 LC-002/LC-012 双重叠+棋三连同构+量化合规三落负担四轮注记——缓解面三件=LC-018 三零断言先例当日承继+差异化角度位敬畏验证主轴+下棋行为字段选材排除〕+跨载体触点徐根福胜位如实注记+源卡双过平位）'
 '+R743 起链（拍稿 v1 12 拍 ≈292 字·逐拍溯源对表·盲评律合规·S1 v1.5+L18-L20 门 10/10 零违律一次过=**拆条系列十八连满分**〔11:02:04 落判·判词档 20260930-110204-S1-script〕·col2 纯 verbatim 零〔〕=R737/R741 剥离案起链前置规避）'
 '+R744 定稿音轨（两道机械裁链 v1 79.696→v2 64.460→**v3 57.235s 定稿 2.765s 余量**·col1/col2 verbatim 零动 12/12 双基断言+信条 verbatim+事实数字〔二十八岁/一万遍〕+互证双名〔徐根福/陈雅雯〕+CTA 受众定位词「敬畏市场」全保·TTS light〔Yunyang+cyber light+human 42·BGM-A 纯净〕）'
 '+R745 渲染腿（F-024 派生源件 census-card-v5-vertical 13.000s+对位表 12/12 visual-ratio 1.00+**R720 律前置修第六件**〔b4/b5/b6/b7 per-card 56/54/50/46+**b8=78 字 fleet 最长 col2 语义预拆 5 段+size 36 下探地板首例**·全卡几何审计 FINAL problems=NONE〕'
 '+R-E shipinhao 57.235s 音轨分毫一致·角标拆条 019·源城市图鉴 005+§4.5 三开关+S2 三门全绿〔ai_feel 0F0W CV 0.282/0.291+层 1.8 六面+spec 双 PASS〕+帧验三律全过〔拍头 12/12+段中尾 6/6+回环 crossings={}+AIGC 双标识+b8 专项帧全分辨率实证+tile 误读 ×4 全分辨率定谳+SRT cue9 byte-check 12/12〕）'
 '+R746 断洞〔E4 参考仪 8.0 落地 12:04:04+ASR QC 首跑 7 cues/1 dropped 诊断=WIP 全存续〕→R747 半程〔ASR 双跑证伪 VAD 因果：QC vad=True 与 novad vad=False 同形跳段=模型层确定性跳段定谳（R711 型）〕→R748 收官腿（'
 '**ASR 终轨 R711 型两段拼接根修**：隔窗 26.7-47.8s 转写 4 cues dropped=0+QC 整轨头 5+尾 2=**11 cues 全覆盖拼接**〔R638/R701 根修-再飞先例·asr-check-run1.srt 证据件留档〕·HF_HUB_OFFLINE=1·asr-diff-r748.txt=30 sites/88 diff/196 字≈**44.9% 字位=系列带上缘之上新峰**〔LC-015 43.2 峰上·量化+专名词域密度件〕：'
 '关键存活（策略研究员/泡面/工位/报平安/天理/验一万遍/多打一勺/最怕也最服/信条/公众号/「敬畏市场」CTA+二十八→28 数字形差值存活）+实质退化如实（hook 双损〔全城→玄城+讣告→报告〕/QUANT→晃土+扭塔→牛塔/徐根福→徐敦福+陈雅雯→陈亚文+风控官→封控官=互证拍三连损/回撤教人→回车叫人=信条核心字损/全档案→全答案=CTA 档案族第十二发/碳基→探机=物种行损族第十六证）·字幕轨=edge-tts 直出 12/12 零损兜底→S2 9.0；'
 '**E4 参考仪 8.0**〔R746 断洞轮落地 12:04:04·e4_call.py 脱壳·三意愿两明一条件〔会看完+点赞/转发条件式「对金融市场和技术感兴趣的朋友」分享对象具名〕·「内容新颖且有创意·科技感×人文关怀」正面定性=拆条带 8.0 回稳位·旗①=「每晚给爹娘报平安」+「他爹说钱的事最讲天理·验一万遍」两句被旗空洞缺关联扣 2=家训+报平安拍 verbatim 卡锚·MC-003 语境门槛族家训位变体·吸收位=M5 图文页语境+系列语境·最弱=情感深度细节融合〔60s 固有·M6 校准位〕·净本 expert-verdicts/20260930-120404-E4-audience〕'
 '+E8 终审七席全 9.0〔review-20260930-lc019-v1.md·E6=产品优先律+b8 前置专项修=周全性预期律+断洞如实入账=假绿灯律①·E7=对位率 1.00 最高并列+problems=NONE+前置修第六件·E8=零发布后修红=前置预防通道连续第六件〕→M4 完成态）'
 '——**冗余池第十六件落位**（release-schedule v3.1·视频号冗余弹药 16 件=LC-004 F-058~LC-019 F-074·M6 调仓弹药/30 天日更冗余·预产窗=开号前）+queue §E E16 出池（lane=E20 徐根福 standby 单条<2·补池义务随轮领=R726 先例）·发布锁=M5 账号物理件不变（未上线=未测量）。\n')
append('output/finished.md', FIN)

# ============ 4. release-schedule v3.1 ============
RS = ('- v3.1 2026-09-30 R748：**冗余池扩容第十六件视频入池**（LC-019《城市图鉴 005·周浩宇》拆条=F-074·成品库 73→74 件·L-卡衍生视频线第十九件=拆条系列节律第十八续件·'
 '**第十对人物链互证闭环后半件**〔陈雅雯×周浩宇「最怕又最服」对·LC-018 b10 关系字段点名直连+双卡年轮 09-30 相遇句双端=系列最快直连〕+**敬畏验证主题首件位**〔28 岁最年轻策略研究员×全城唯一讣告写手=差异化角度位·信条「回撤教人做人，行情教人谦虚」·量化近域三零断言承继件〕·'
 'R742 出池注记→R743 选优入池〔S1 10/10 十八连满分〕→R744 定稿音轨〔两道裁链 57.235s 2.765s 余量〕→R745 渲染腿〔**b8=78 字 fleet 最长 col2 语义预拆+size 36 下探地板首例=R720 律预执行第六件**·全卡几何审计 problems=NONE〕'
 '→R746 断洞〔E4 8.0 落地+ASR 首跑跳段诊断〕→R747 半程〔双跑证伪 VAD 因果〕→R748 收官全链走门：ASR 终轨 R711 型两段拼接 44.9% 字位=系列带新峰〔模型层确定性跳段根修·字幕轨 12/12 零损兜底〕+E4 8.0〔旗①=家训位语境门槛族变体〕+七席 ≥9→M4）；§四 盘点行同步（视频号冗余弹药 15→16 件·M6 调仓/日更冗余·预产窗=开号前）。\n')
append('docs/release-schedule-v1.md', RS)
# sync the inventory line 15 -> 16
sc = io.open('docs/release-schedule-v1.md', encoding='utf-8').read()
m = re.findall(r'视频号冗余弹药 15 件', sc)
if len(m) == 1:
    sc = sc.replace('视频号冗余弹药 15 件', '视频号冗余弹药 16 件', 1)
    W('docs/release-schedule-v1.md', sc)
    print('SCHED_INV_SYNCED')
else:
    print('!! SCHED_INV count', len(m), '(left as-is, check manually)')

# ============ 5. queue E16 closeout ============
QU = ('- 2026-09-30: **E16 收官毕（R748·F-074 登记=成品库第七十四件·冗余池第十六件落位 release-schedule v3.1·视频号冗余弹药 16 件·第十对人物链互证闭环后半件=敬畏验证主题首件位'
 '〔R746/R747 断洞链+R748 承接：E4 8.0 断洞轮落地+ASR QC/novad 双跑证伪 VAD 因果=模型层确定性跳段（R711 型）→R748 两段拼接根修=11 cues 全覆盖 44.9% 字位系列带新峰·asr-check-run1/-novad.srt 双证据件留档〕'
 '·收官=E8 七席 ≥9+E4 8.0〔三意愿两明一条件·旗①=家训位语境门槛族变体〕+ASR 终轨两段拼接 44.9% 字位〔互证拍三连损=双名+职衔同音形损如实·字幕轨 edge-tts 12/12 零损兜底〕〕）'
 '→E16 出池（lane=E20 徐根福 standby 单条<2·**补池义务随轮领**=R726 先例·候选=未拆存量卡〔CENSUS 库 C-00012 沈佩兰 等〕/BS-007 稿集件/徐根福前件直连位随选优轮评估）**\n')
append('docs/self-improvement-queue.md', QU)

# ============ 6. station-reviews R748 row ============
SR = ('| 2026-09-30 | **收官腿机检包（lc-019-v1-shipinhao=queue §E 批活池 E16 件收官·冗余扩容位第十六件·R746/R747 断洞链+R748 承接：ASR R711 型两段拼接根修+E4 参考仪回填+E8 评审单+M4→F-074 登记）** | '
 'lc-019-v1-shipinhao-60s.mp4（57.235s·音轨分毫一致 2.765s 余量）+.lc019-tmp/asr-check.srt（11 cues 两段拼接全覆盖）+asr-diff-r748.txt（R169 QC recipe medium-int8+beam5+noctx·隔窗 26.7-47.8s 转写 4 cues dropped=0+QC 整轨头 5+尾 2=R638/R701 根修-再飞先例·QC vad=True 与 novad vad=False 双跑同形证伪 VAD 因果=R747 定谳·模型层确定性跳段 R711 型） | '
 'ASR 终轨（faster-whisper 本地）+E4（Ollama qwen2.5:14b 本地·e4_call.py 脱壳 12:04:04 落地=R746 断洞轮·expert-calls 行 R748 补账）+E8 评审单 review-20260930-lc019-v1.md | ——（收官档） | '
 'ASR=44.9% 字位系列带新峰（关键存活=策略研究员/验一万遍/多打一勺/最怕也最服/敬畏市场 CTA+二十八→28 形差值存活·实质退化=hook 双损+互证拍三连损〔徐根福→徐敦福/陈雅雯→陈亚文/风控官→封控官〕+回撤教人→回车叫人+全档案→全答案=CTA 档案族第十二发+碳基→探机=物种行损族第十六证·字幕轨 edge-tts 12/12 零损兜底）'
 '+E4 8.0（三意愿两明一条件·旗①=家训+报平安拍=MC-003 语境门槛族家训位变体·最弱=情感深度细节融合·净本 20260930-120404-E4-audience）+E8 七席全 9.0→M4 完成态→F-074 登记=成品库第七十四件+冗余池第十六件落位 release-schedule v3.1 |\n')
append('docs/reviews/station-reviews.md', SR)

# ============ 7. expert-calls E4 backfill row ============
EC = ('| 2026-09-30 12:04 | E4-audience | E4 直觉观众（参考仪·非拦截席） | C:\\Users\\sjs20\\Desktop\\FluxGroup\\media\\BigStream\\.lc019-tmp\\subs.srt | 1 | '
 'full text=expert-verdicts/20260930-120404-E4-audience.md / 8.0 三意愿两明一条件（会看完+点赞/转发条件式「对金融市场和技术感兴趣的朋友」分享对象具名·「内容新颖且有创意·科技感×人文关怀」正面定性=拆条带 8.0 回稳位·旗①=「每晚给爹娘报平安」+「他爹说钱的事最讲天理。策略就是把道理验一万遍」被旗空洞缺关联扣 2=MC-003 语境门槛族家训位变体·最弱=情感深度细节融合） | '
 'R748 补账（R746 断洞轮 e4_call.py 脱壳落地·行未落=R747 预注回填位） |\n')
append('docs/reviews/expert-calls.md', EC)

# ============ 8. lc019 README ============
edit('data/sources/lc019/README.md',
     '·收官腿=待领（E8+ASR+E4+M4→F-074 登记→冗余池第十六件→E16 出池+补池）。',
     '·**收官腿=R746/R747 断洞链+R748 承接毕**（E4 8.0〔R746 落地 12:04:04〕+ASR 双跑证伪 VAD 因果〔R747〕+R748 两段拼接根修 11 cues 全覆盖 44.9% 字位+E8 七席 ≥9+M4→**F-074 登记=成品库第七十四件**→冗余池第十六件→E16 出池）。')
append('data/sources/lc019/README.md',
       '- [2026-09-30 ' + TS_HM + ' R748 收官腿毕（R726/R730/R734/R738/R742 同型）] R746 断洞（E4 8.0 落地+ASR QC 首跑 7 cues/1 dropped 诊断）→R747 半程（QC vad=True 与 novad vad=False 双跑同形=VAD 因果证伪·模型层确定性跳段定谳 R711 型）→R748 承接：**ASR 终轨 R711 型两段拼接根修**'
       '（隔窗 26.7-47.8s 转写 4 cues dropped=0+QC 整轨头 5+尾 2=11 cues 全覆盖·asr-check-run1.srt 证据件留档·asr-diff-r748.txt=30 sites/88 diff/196 字≈**44.9% 字位=系列带上缘之上新峰**：'
       '关键存活=策略研究员/报平安/天理/验一万遍/多打一勺/最怕也最服/信条/公众号/敬畏市场 CTA+二十八→28 形差值存活；实质退化=hook 双损〔全城→玄城+讣告→报告〕+互证拍三连损〔徐根福→徐敦福/陈雅雯→陈亚文/风控官→封控官〕+回撤教人→回车叫人+全档案→全答案=CTA 档案族第十二发+碳基→探机=物种行损族第十六证·字幕轨 edge-tts 12/12 零损兜底）'
       '→S2 9.0+E4 8.0 回填（expert-calls 行 R748 补账）+E8 七席全 9.0（review-20260930-lc019-v1.md）→M4→F-074 登记=成品库第七十四件+冗余池第十六件（release-schedule v3.1）。\n')

# ============ 9. state.json ============
R748 = ('2026-09-30 ' + TS_HM + ' R748: 生产轮·LC-019 周浩宇拆条收官腿毕=F-074 登记+冗余池第十六件落位（queue §E 批活池 E16 件收官·R746/R747 断洞链承接·R726/R730/R734/R738/R742 同型·实活轮·产品优先律 P-20260929-07 对位=本轮新实物=lc-019 成片 F-074 入成品库 74 件）'
 '——①轮首五查静（r694_probe 口径：orders 顶 O-20260928-1910 42 件锚未动/ledger 六模式 CaseSensitive 41=锚/decisions UTF8 非空行 75=锚/production=open 自愈核在位 tick747/无 index.lock·树态=bm-a codex 批未闭让位维持〔README/city-humanities mtime 09-29 04:06 未动=#86 c+d 判据未达·两文件零接触〕+自产 tmp 族预期态）；'
 '②ASR 根修=R711 型两段拼接通道落地（R746 QC vad=True 与 R747 novad vad=False 双跑同形 7 cues/1 dropped 稳定跳段 26.94-47.54s=VAD 因果已证伪〔R747〕·模型层确定性跳段定谳→r748_asr_splice.py 隔窗 26.7-47.8s 转写 4 cues dropped=0+QC 整轨头 5+尾 2=**11 cues 全覆盖拼接**〔R638/R701 根修-再飞先例·asr-check-run1.srt QC 证据件留档〕）'
 '→asr-diff-r748.txt=30 sites/88 diff/196 字≈**44.9% 字位=系列带上缘之上新峰**（LC-015 43.2 峰上·量化+专名词域密度件）：关键存活（策略研究员/泡面/工位/报平安/天理/验一万遍/多打一勺/最怕也最服/信条/公众号/敬畏市场 CTA+二十八→28 数字形差）+实质退化如实（hook 双损〔全城→玄城+讣告→报告〕/QUANT→晃土+扭塔→牛塔/徐根福→徐敦福+陈雅雯→陈亚文+风控官→封控官=互证拍三连损/回撤教人→回车叫人=信条核心字损/全档案→全答案=CTA 档案族第十二发/碳基→探机=物种行损族第十六证）·字幕轨=edge-tts 直出 12/12 零损兜底→S2 9.0；'
 '③E4 参考仪 8.0 回填（R746 断洞轮 12:04:04 落地·expert-calls 行 R748 补账=R747 预注回填位兑现）+E8 评审单 review-20260930-lc019-v1.md（S1 10/10〔R743 十八连满分〕+S2 9.0+S3 9.0+S4 9.0+终审七席全 9.0·E4 8.0 参考线·六轮链 R743→R748 含断洞如实入账=假绿灯律①）→M4 完成态；'
 '④F-074 登记（成品库第七十四件·L-卡衍生视频线第十九件=拆条系列节律第十八续件=第十对人物链互证闭环后半件=敬畏验证主题首件位）+冗余池第十六件落位（release-schedule v3.1·视频号冗余弹药 16 件）+renders 行升「成品·落位」+station-reviews R748 行+queue §E E16 出池（lane=E20 徐根福 standby 单条<2·补池义务随轮领）+lc019 README 收口+.lc019-tmp 批闭收账全批入 git（R721/R742 先例）；'
 '⑤例行件：日报 09-30 在案不重跑（R713 补产）/W40 周审在案（R576）/global-benchmarks day6 ≤7 跳过（下期 10-01=#80 并窗勿提前触碰）/#70 OSS 窗 2=10-02 21:40 前随轮领（R644 切片 1 在案）/#86 c+d 让位判据未达（codex mtime 04:06 未动）/T1 催办=已裁项停用口径/HQ-FEEDBACK 不写（无集团层新 open 问题·双锚静零膨胀）'
 '·tokens:local=1（faster-whisper medium 隔窗转写 ×1=ASR 校准用·本地零 API token·P-54⑤ 计量律如实记）'
 '——下轮=R749 可领序：①queue §E 补池义务（lane<2·选优轮评估：未拆存量卡/BS-007 稿集件/徐根福前件直连位）②#70 OSS 窗 2 切片（≤10-02 21:40）③#86 c+d 让位判据④global-benchmarks 10-01 刷新（#80 并窗）。收账显式列文件 commit+push')

c = io.open('src/os/state.json', encoding='utf-8').read()
anchor = '"\n ],\n "ts":'
if c.count(anchor) != 1:
    print('!! state anchor mismatch=%d' % c.count(anchor)); sys.exit(1)
c = c.replace(anchor, '",\n  "' + R748.replace('\\', '\\\\').replace('"', '\\"') + '"\n ],\n "ts":', 1)
c = c.replace('"tick": 747,', '"tick": 748,', 1)
m = re.search(r'"focus": "R748: [^"]*"', c)
if not m: print('!! focus not found'); sys.exit(1)
FOCUS = ('R749: ①queue §E 补池义务（lane=E20 徐根福 standby 单条<2·选优轮评估：未拆存量卡〔CENSUS 库 C-00012 沈佩兰 等〕/BS-007 稿集件/徐根福前件直连位=LC-019 b10 埋点兑现·随选优定谳入池）'
         '②#70 OSS 窗 2 切片（≤10-02 21:40·R644 切片 1 在案）③#86 c+d 让位判据（bm-a codex 批闭 commit 落地）④global-benchmarks 10-01 刷新（#80 并窗）'
         '——五查锚=orders O-20260928-1910 42·ledger 41（L189/L190/L245 注）·decisions 75')
c = c[:m.start()] + '"focus": "' + FOCUS + '"' + c[m.end():]
c = re.sub(r'"ts": "2026-09-30 12:55:00",', '"ts": "' + TS_FULL + '",', c, count=1)
if '"ts": "' + TS_FULL + '"' not in c: print('!! ts not replaced'); sys.exit(1)
task_line = R748.split('R748: ', 1)[1][:60]
m2 = re.search(r'"task": "[^"]*"', c)
c = c[:m2.start()] + '"task": "R748: ' + task_line.replace('\\', '\\\\').replace('"', '\\"') + '"' + c[m2.end():]
W('src/os/state.json', c)

# ============ 10. status-export.json ============
E = json.load(io.open('docs/status-export.json', encoding='utf-8'))
E['export_ts'] = TS_FULL
E['outs'][0][2] = ('tick 748，R748 生产轮·LC-019 周浩宇拆条收官腿毕=F-074 登记+冗余池第十六件落位（产品优先律对位=本轮实物增量=lc-019 成片 F-074 入成品库 74 件·'
 'R746/R747 断洞链承接：E4 8.0 断洞轮落地+ASR 双跑证伪 VAD 因果→R748 R711 型两段拼接根修 11 cues 全覆盖 44.9% 字位·E8 七席 ≥9+M4）'
 '——lane=E20 徐根福 standby 单条<2·补池义务随轮领·发布锁=M5 账号物理件不变（未上线=未测量）')
E['results'].insert(0, ['748', R748])
E['live'] = [
 ['当前活：LC-019 周浩宇拆条收官腿毕（R748）——F-074 登记=成品库第七十四件·冗余池第十六件落位（视频号冗余弹药 16 件）·lane=E20 徐根福 standby 单条<2·补池义务随轮领'],
 ['最近实物：lc-019-v1-shipinhao-60s.mp4 成品落位 output/renders/（57.235s·2026-09-30 ' + TS_HM + '）+评审单 review-20260930-lc019-v1.md+ASR 拼接证据件 .lc019-tmp/asr-check.srt'],
 ['下个里程碑：queue §E 补池选优入池（≤48h 窗·lane<2）·#70 OSS 窗 2 切片（≤10-02 21:40）·global-benchmarks 7 日刷（10-01 #80 并窗）'],
]
W('docs/status-export.json', json.dumps(E, ensure_ascii=False, indent=1) + '\n')

print('CLOSEOUT_OK')
