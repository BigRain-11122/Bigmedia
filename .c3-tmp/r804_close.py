# -*- coding: utf-8 -*-
"""R804 closeout leg edit script (gap-hole absorption).
Crashed 02:52 intent-round products inherited; registration legs added here.
All edits UTF-8; verification printed ASCII-safe.
"""
import io, json, sys

R = lambda p: io.open(p, encoding='utf-8').read()
W = lambda p, s: io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
out = []
def log(m): out.append(m)

# ---------- 1) station-reviews.md: dedup R803 double-append + append R804 rows (idempotent) ----------
p = 'docs/reviews/station-reviews.md'
lines = R(p).splitlines()
if '台账修红=R803 双写去重' in R(p):
    log('station-reviews: already applied, skip')
else:
    dup_idx = [i for i, l in enumerate(lines) if 'R803' in l and 'S2 三门循环独立执法' in l and '渲染腿' in l]
    assert len(dup_idx) == 2 and dup_idx[1] == dup_idx[0] + 1, ('dup pair check', dup_idx)
    assert lines[dup_idx[0]] == lines[dup_idx[1]], 'identical dup rows'
    del lines[dup_idx[1]]
    row1 = "| 2026-10-01 | **台账修红=R803 双写去重（R804 断洞承接轮）** | 前执行者对 R803 轮重复追加了 station-reviews 行（原 L212/L213 完全同文）与 state.json log 行（02:48x/02:49x 两行时间前缀外同文 2944 chars）+status-export results 803 双条——假绿灯律① 台账卫生修红：**去重保一+本行附加说明**（原行内容史不改写·双写事实注记在案·判据=逐字 diff 实证 L212==L213 与 content-equal-after-ts=True） | 去重实证=python 逐字比对 | R804 收账行注记 |"
    row2 = "| 2026-10-01 | **E8 终审+M4+F-079 登记+E24 出池（bs-009-v1-shipinhao 收官腿·断洞承接：02:52 意图轮死于模型连接 503/500×4+流空闲 300s·03:09:42 exit=1 零收账·其 ASR 终轨+E4 判词+净本+E8 评审单产物承继〔R155/R156 断洞先例〕·登记腿本轮补齐）** | ASR 终轨整轨一次过 11 cues dropped=0（R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1 离线直过零缓存事故=R701/R761/R801 判例后首件干净落地）=5 sites/7 diff chars/192 字≈**3.6% 字位=BS 系带内新低位**（BS-006 5.6%/BS-001 v15 9.1%/BS-008 11.9%/BS-007 15.3% 族带·trad 字形漂移 0 处=归一后全真实同音带=fleet 最干净轨）+数字面值 100% 存活（年化 30%/第一条 全值在位）+合规拍 b11「不构成投资建议」全净读+红线原文「不许把过拟合，当优势出售」全净读+「系统在说真话」全净读；实质退化如实=拟合→你何（b10 红线收束 punch 词位·nǐhé 同音值存活·字幕轨 edge-tts 12/12 零损兜底）+日志→日制〔b0〕/日志→日治〔b6〕系列在案同音族复发〔BS-004 R187/BS-007 R761〕+条条→调调〔b1〕+防→房〔b11 CTA 位·LC-016/017 CTA 损族对照〕→S2 9.0 | E4 参考仪 8.0 同轮回填（02:55:50 落判热载快落·会看完明说+点赞/转发条件式+打 8 分明说=**量化域件 E4 新高位**〔BS-008/BS-007 7.0 受众窄位带后 8.0=红线声明件大众化位证据〕·旗①=「曲线漂亮不等于有本事」语境门槛族变体扣 1〔verbatim 卡锚·吸收位=M5 图文页语境〕·最弱=缺乏互动性和具体案例〔54s 固有〕·净本 expert-verdicts/20261001-025550-E4-audience）+E8 终审七席 E1/E2/E3/E5/E6/E7/E8 全 9.0（评审单 review-20261001-bs009-v1.md·S1 10/10〔R802〕+S2 9.0+S3 9.0+S4 9.0〔量化主题特别合规三落+量化近域三零断言〕）→M4 完成态→**F-079 登记**（成品库第七十九件·稿集视频线第四件·冗余池第二十件落位 release-schedule v3.5）+**E24 出池**（supply-gated 豁免面维持·补池义务随轮领·造活凑数禁） | asr-check.srt+asr-diff-r804.txt+e4-result.json 留档 .bs009-tmp·全批随收账入 git |"
    lines.extend(['', row1, row2])
    W(p, '\n'.join(lines) + '\n')
    log('station-reviews: dedup ok, rows now %d' % len(lines))

# ---------- 2) finished.md: append F-079 ----------
p = 'output/finished.md'
txt = R(p)
assert 'F-078 登记（R801）' in txt and 'F-079' not in txt, 'finished anchor / F-079 not yet present'
f079 = "\nF-079 登记（R804）——**稿集视频线第四件=冗余扩容位第二十件**（queue §E 批活池 E24 稿集件收官·BS-009《第一条红线》·成品库第七十九件·**断洞承接轮**：02:52 意图轮〔本循环 R804 首启〕死于模型连接故障〔503/500+流空闲 300s·03:09:42 exit=1 零收账〕·ASR 终轨+E4 判词+E8 评审单产物承继〔R155/R156 断洞先例〕·登记腿 03:12 重启轮补齐）。**bs-009-v1-shipinhao-60s（系列角标 BS-009 EP.09）全链走门全档**：源稿=data/drafts/20260923-BS-004-公众号-v1.md §为什么值得开酒后半+§标题候选 3+§AIGC 声明**曲线拟合红线切面**（一料多吃 charter §3·**R753 lesson 查重断言前置执法首件**〔池内稿集谱系零同切面+grep「曲线拟合/过拟合」全 fleet 口播零命中+F-004 v15/BS-008 已覆盖面全排除=展开角度零重叠·选优门先跑池内查重〕·稿集谱系第四件）→R802 起链（拍稿 v1 12 拍 ≈191 去标点字·单论点=漂亮曲线不是真本事——把拟合当优势卖，是我们立的第一条红线〔No curve-fitted strategies sold as edge〕·M0 四维分 7/8 A 档+M1 0F0W 一次过+**S1 v1.5+L18-L20 门 10/10 PASS 零违律一次过**〔02:27:34 落判·三段格式全落位=R735 材料尾格式锚续连·判词档 20261001-022734-S1-script〕+**TTS light v1 实测 54.229s 直接入窗 5.77s 余量=v1 即定稿零裁链=fleet 起链腿首件免裁**+ai_feel 早门 0F0W）→R803 渲染腿（素材探针三源三时点多模态零录穿+对位表 11/12=**0.92 层 1.8 面上探**〔looplog×6+reviewsdoc×4+editgrid×1+cards-only×1〕+全卡几何审计 12 卡 problems=NONE 零修红前置预防第十件+R-E shipinhao 54.229s 音轨分毫一致+角标 BS-009 EP.09+§4.5 三开关+调用面错门轮内咬住〔render_card_video R-A 直渲门误调→edit_craft R-E 重渲覆盖复绿=R381 同型〕+S2 三门全绿+帧验三律全过+回环 crossings={}）→R804 收官腿（**ASR 终轨整轨一次过 11 cues dropped=0**〔R169 QC recipe medium-int8+beam5+noctx·**HF_HUB_OFFLINE=1 离线直过零缓存事故=R701/R761/R801 判例后首件干净落地**〕=5 sites/7 diff chars/192 字≈**3.6% 字位=BS 系带内新低位**〔BS-006 5.6%/BS-001 v15 9.1%/BS-008 11.9%/BS-007 15.3% 族带·**trad 字形漂移 0 处=归一后全真实同音带=fleet 最干净轨**〕+**数字面值 100% 存活**〔年化 30%/第一条 全值在位〕+合规拍 b11「不构成投资建议」全净读+红线原文「不许把过拟合，当优势出售」全净读+「系统在说真话」全净读；实质退化如实=**拟合→你何 1 处=红线收束 punch 词位**〔b10「红线只有一句：拟合不卖」→「你何不卖」·nǐhé 同音值存活·字幕轨 edge-tts 直出 12/12 零损兜底〕/日志→日制〔b0 hook〕+日志→日治〔b6 判定位〕=系列在案同音族复发〔BS-004 R187/BS-007 R761 同词〕/条条→调调〔b1 满屏位〕/防→房〔b11 CTA 位·CTA 损族 LC-016/017 对照〕→S2 9.0；**E4 参考仪 8.0 同轮回填**〔02:55:50 落判热载快落·会看完明说+点赞/转发条件式+打 8 分明说=**量化域件 E4 新高位**〔BS-008/BS-007 7.0 受众窄位带后 8.0=红线声明件大众化位证据〕·「量化交易陷阱对金融知识感兴趣的人很有启发」+「剪辑配音相当专业」双正面定性·旗①=「曲线漂亮不等于有本事」语境门槛族变体扣 1〔verbatim 卡锚·MC-003 族·吸收位=M5 图文页语境〕·最弱=缺乏互动性和具体案例〔54s 固有·M5 图文页正解〕·净本 expert-verdicts/20261001-025550-E4-audience〕；E8 终审评审单 review-20261001-bs009-v1.md〔S1 10/10〔R802〕+S2 9.0+S3 9.0+S4 9.0〔**量化主题特别合规三落**=「不构成投资建议」口播 b11+字幕 SRT+M5 简介位三落=F-004 先例适用+**量化近域合规三零断言**：零策略推荐/零收益承诺/零投资建议·「年化 30%」=行业批判引述引号保留非本司承诺〕+终审七席 E1/E2/E3/E5/E6/E7/E8 全 9.0→M4 完成态〕）——**冗余池第二十件落位**（release-schedule v3.5·in-line 盘点行计数 19→20 正字+BS-009 件行落位=R801 修红律延续）+**E24 出池**（lane=supply-gated 豁免面维持·新锚卡 C-00030+/新令级事件落位即恢复 ≥2·补池义务随轮领·造活凑数禁=R756/R801 口径）+**稿集路径收口注记=本件后 BS-004 母稿三切面全耗**〔F-004 全灭庆祝+BS-008 幸存者档案+本件曲线拟合红线=10 稿母稿资产复用通道第四验·该母稿稿集通道收口=R802 预告兑现〕·随行台账修红=R803 station/state/export 三处双写去重〔假绿灯律①〕·批闭收账全批入 git（.bs009-tmp/.c3-tmp 证据件）·发布锁=M5 账号物理件未开·未上线=未测量。"
W(p, txt.rstrip('\n') + '\n' + f079 + '\n')
log('finished.md: F-079 appended')

# ---------- 3) release-schedule-v1.md: L79 count 19->20 + append BS-009 segment + v3.5 changelog ----------
p = 'docs/release-schedule-v1.md'
lines = R(p).splitlines()
l79 = lines[78]
assert '盘点' in l79 and '冗余' in l79, 'L79 anchor'
assert '视频号冗余弹药 19 件' in l79, 'count phrase missing'
l79 = l79.replace('视频号冗余弹药 19 件', '视频号冗余弹药 20 件', 1)
seg = "+BS-009 稿集件4 F-079（R804·冗余池第二十件视频·稿集视频线第四件=**BS-004 母稿三切面全耗收口件**〔F-004 全灭庆祝→BS-008 幸存者档案→本件曲线拟合红线=10 稿母稿资产复用通道第四验·R753 lesson 查重断言前置执法首件〕·R802 入池选优〔曲线拟合红线切面·查重零同切面+grep 零命中〕→R803 渲染〔对位 11/12=0.92 层 1.8 面上探+全卡几何审计 problems=NONE 第十件+S2 三门全绿+帧验三律全过+调用面错门轮内咬住〕→R804 收官〔**断洞承接**：02:52 意图轮死于模型连接 503/500 零收账·产物承继登记腿补齐〕：ASR 终轨整轨一次过 **3.6% 字位=BS 系带内新低位**〔trad 漂移 0 处=最干净轨〕+数字面值 100% 存活+红线 punch 词「拟合→你何」同音代价如实+HF_HUB_OFFLINE=1 离线直过零缓存事故+E4 8.0〔**量化域件 E4 新高位**〕+七席 ≥9→M4·随行 R803 三处双写去重〕"
lines[78] = l79 + seg
v35 = "- v3.5 2026-10-01 R804：**冗余池扩容第二十件视频入池**（BS-009《第一条红线》稿集件4=F-079·成品库 78→79 件·**稿集视频线第四件=BS-004 母稿三切面全耗收口件**〔BS-006 编辑诚实→BS-007 设计哲学→BS-008 幸存者档案→BS-009 曲线拟合红线=10 稿母稿资产复用通道第四验·R753 lesson 查重断言前置执法首件=选优门先跑池内查重〕·R802 入池选优→R803 渲染〔对位 11/12=0.92 层 1.8 面上探+几何审计 NONE 第十件+S2 三门全绿+帧验三律全过〕→R804 收官全链走门〔**断洞承接轮**：02:52 意图轮死于模型连接 503/500 零收账·ASR/E4/评审单产物承继=R155/R156 先例〕：ASR 终轨整轨一次过 **3.6% 字位=BS 系带内新低位**〔BS-006 5.6%/BS-001 v15 9.1%/BS-008 11.9%/BS-007 15.3% 族带·trad 字形漂移 0 处=fleet 最干净轨〕+数字面值 100% 存活+红线 punch 词「拟合→你何」同音代价如实〔字幕轨零损兜底〕+E4 8.0〔**量化域件 E4 新高位**·量化域压缩术语件受众窄位带后大众化位证据〕+七席 ≥9→M4·随行台账修红=R803 station/state/export 三处双写去重=假绿灯律①〕；§四 盘点行同步（视频号冗余弹药 19→20 件·M6 调仓/日更冗余·预产窗=开号前）。"
lines.append(v35)
W(p, '\n'.join(lines) + '\n')
log('release-schedule: count+segment+v3.5 ok')

# ---------- 4) renders README: L111 declaration tail + new bs-009 mp4 row after L143 ----------
p = 'output/renders/README.md'
lines = R(p).splitlines()
i111 = 110
assert 'BS-009 稿集件4 批中间件' in lines[i111], 'L111 anchor'
old_tail = 'R804 起随轮领）'
assert lines[i111].count(old_tail) == 1, 'L111 tail count'
lines[i111] = lines[i111].replace(old_tail, 'R804 断洞承接收官毕〔F-079 登记+冗余池第二十件落位 release-schedule v3.5+E24 出池 supply-gated 豁免面维持·发布锁=M5 账号物理件未开·未上线=未测量〕）', 1)
i143 = 142
assert 'bs-008-v1-shipinhao-60s.mp4' in lines[i143], 'L143 anchor'
row = "| bs-009-v1-shipinhao-60s.mp4 | **成品·落位（F-079 登记 R804·稿集视频线第四件〔BS-006 编辑诚实→BS-007 设计哲学→BS-008 幸存者档案→BS-009 曲线拟合红线=10 稿母稿资产复用通道第四验·**BS-004 母稿三切面全耗=稿集该母稿通道收口**〕·queue §E 批活池 E24 稿集件收官·视频号冗余池第二十件·R802 起链→R803 渲染腿→R804 收官腿毕〔**断洞承接轮**〕·全链走门·评审单 review-20261001-bs009-v1.md）** | **R-E shipinhao 12 段 11 柔转场 0 硬切**·9:16 1080×1920·**54.229s ffprobe 实测=音轨分毫一致·5.77s 余量**〔fleet 带最宽位·v1 即定稿零裁链〕·hits=[0]·**S5.5 角标常驻位**=BigStream\\|BS-009 EP.09+§4.5 三开关[glow/scanlines/sys.beat=NN t=MM:SS]·plan.series+s45_dials 入 plan.json·**稿集形态对位 11/12=0.92**（素材探针先行三源三时点多模态零录穿〔probe-r803〕：looplog×6〔b0 系统日志本体直证/b2 参数推进意象/b4 红线原文 b0 同源/b6 日志判定字面/b9 系统说真话字面/b10 收束同源〕+reviewsdoc×4〔b3 有名字=登记/b5 判定行/b7 在册自治理/b8 verdict+证据链〕+editgrid×1〔b1 满屏条条=并列网格意象〕+cards-only×1〔b11 CTA+量化合规拍〕=**层 1.8 ≥0.80 面上探**·F-002/F-004 0.83 带上探如实注记）——**全卡几何审计 12 卡 problems=NONE 零修红前置预防**（r803_card_audit·R720 律预执行=前置预防通道第十件）——**S2 三门 R803 循环独立执法全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.146-0.531s·pacing CV 0.258·prosody 9 档 12 拍·copy CV 0.236=R802 早门读数同音轴确定性）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 0.92+transition-share 1.00 无连排+transition-variety+timeline 代数过）+spec 微信视频号双 PASS（9:16+54.23s ∈30-60s 窗 5.8s 余量）——**帧验三律全过**：拍头 12/12 语义全中（H1 拍名逐拍对位+sys.beat 01→12 连续 t 单调+角标 12 帧全在+AIGC 帧头标识全在）+全分辨率 h04（b4 最长副行 13 字完整单行零折行零拆字·「出售」用字与 beats 源逐字一致）+段中尾 6/6 零录穿（m03/m10/m11 段中卡+字幕+sys 行全在位·tile 序位前提误判 ground truth 证伪=R189 手段问题律）+回环 crossings={}（max 拍 6.74s<最短源 10s 诚实计算）+**调用面修红 1 处轮内咬住**（首调误走 render_card_video=R-A 直渲门→S2 edit_craft 首跑 FAIL〔plan 缺〕揭→edit_craft.py R-E 全渲染模式重渲覆盖复绿=R381 同型） | plan.json 入 git·mp4 gitignored·R804 收官腿毕（ASR 终轨整轨一次过 3.6% 字位=BS 系带内新低位+trad 漂移 0 处=fleet 最干净轨+数字面值 100% 存活+合规拍全净读+E4 8.0 同轮回填〔量化域件 E4 新高位〕+七席 ≥9→M4→F-079 登记→冗余池第二十件落位〔release-schedule v3.5〕→E24 出池 supply-gated 豁免面维持·发布锁=M5 账号物理件未开·未上线=未测量） |"
lines.insert(i143 + 1, row)
W(p, '\n'.join(lines) + '\n')
log('renders README: decl tail + new row ok')

# ---------- 5) bs009 README: append R804 entry ----------
p = 'data/sources/bs009/README.md'
txt = R(p)
assert 'R803 claim+渲染腿毕' in txt, 'bs009 README anchor'
entry = "\n- [2026-10-01 03:2x R804 收官腿毕（断洞承接·lane=E24 收官出池+supply-gated 豁免面维持）——**02:52 意图轮〔本循环 R804 首启〕死于模型连接故障（503/500×4+流空闲 300s·03:09:42 exit=1 零收账）·其已落盘产物（ASR 终轨+e4_call.py 双飞+E4 判词+净本+E8 评审单）经逐件验证后由 03:12 重启轮全数承继（R155/R156 断洞先例）·登记腿本轮补齐**：①**ASR 终轨整轨一次过 11 cues dropped=0**（R169 QC recipe medium-int8+beam5+noctx·**HF_HUB_OFFLINE=1 离线直过零缓存事故=R701/R761/R801 判例后首件干净落地**）=5 sites/7 diff chars/192 字≈**3.6% 字位=BS 系带内新低位**（BS-006 5.6%/BS-001 v15 9.1%/BS-008 11.9%/BS-007 15.3% 族带·**trad 字形漂移 0 处=归一后全真实同音带=fleet 最干净轨**）+**数字面值 100% 存活**（年化 30%/第一条 全值在位）+合规拍 b11「不构成投资建议」全净读+红线原文「不许把过拟合，当优势出售」全净读+「系统在说真话」全净读；实质退化如实=**拟合→你何 1 处=红线收束 punch 词位**（b10「红线只有一句：拟合不卖」→「你何不卖」·nǐhé 同音值存活·字幕轨 edge-tts 直出 12/12 零损兜底）/日志→日制〔b0 hook〕+日志→日治〔b6〕=系列在案同音族复发〔BS-004 R187/BS-007 R761 同词〕/条条→调调〔b1〕/防→房〔b11 CTA 位·LC-016/017 CTA 损族对照〕→S2 9.0；②**E4 参考仪 8.0 同轮回填**（02:55:50 落判热载快落·会看完明说+点赞/转发条件式+打 8 分明说=**量化域件 E4 新高位**〔BS-008/BS-007 7.0 受众窄位带后 8.0=红线声明件大众化位证据〕·「量化交易陷阱对金融知识感兴趣的人很有启发」+「剪辑配音相当专业」双正面定性·旗①=「曲线漂亮不等于有本事」语境门槛族变体扣 1〔verbatim 卡锚·吸收位=M5 图文页语境〕·最弱=缺乏互动性和具体案例〔54s 固有·M5 图文页正解〕·净本 expert-verdicts/20261001-025550-E4-audience+expert-calls 02:55 行 wrapper 自动）；③E8 终审评审单 review-20261001-bs009-v1.md（S1 10/10〔R802〕+S2 9.0+S3 9.0+S4 9.0〔量化主题特别合规三落+量化近域三零断言：零策略推荐/零收益承诺/零投资建议〕+终审七席 E1/E2/E3/E5/E6/E7/E8 全 9.0）→M4 完成态→**F-079 登记**（成品库第七十九件·稿集视频线第四件〔母稿资产复用通道第四验·**BS-004 母稿三切面全耗=稿集该母稿通道收口**=R802 预告兑现〕）+冗余池第二十件落位（release-schedule v3.5·in-line 计数 19→20 正字=R801 修红律延续）+**E24 出池**（supply-gated 豁免面维持·新锚卡 C-00030+/新令级事件落位即恢复 ≥2·补池义务随轮领·造活凑数禁=R756/R801 口径）·随行台账修红=R803 station/state/export 三处双写去重〔假绿灯律①·双写事实注记在案〕·发布锁=M5 账号物理件未开·未上线=未测量。\n"
W(p, txt.rstrip('\n') + '\n' + entry)
log('bs009 README: R804 entry appended')

# ---------- 6) queue E lane: append R804 line after R803 line ----------
p = 'docs/self-improvement-queue.md'
lines = R(p).splitlines()
i = max(idx for idx, l in enumerate(lines) if l.startswith('- 2026-10-01: **R803 E24 BS-009 渲染腿毕'))
qline = "- 2026-10-01: **R804 E24 收官=BS-009 全链走门毕=F-079 登记+出池（断洞承接轮）**（R803 指针兑现·收官腿 E8+ASR 终轨+E4 参考仪→M4→F 登记：**02:52 意图轮死于模型连接 503/500〔03:09:42 exit=1 零收账〕·ASR/E4/评审单产物承继+登记腿本轮补齐**：ASR 终轨整轨一次过 11 cues/0 dropped〔R169 QC recipe·HF_HUB_OFFLINE=1 离线直过零缓存事故〕=5 sites/7 diff/192 字≈**3.6% 字位=BS 系带内新低位**+trad 漂移 0 处=最干净轨+数字面值 100% 存活+合规拍全净读+红线 punch 词「拟合→你何」同音代价如实〔字幕轨零损兜底〕→S2 9.0+E4 参考仪 8.0 同轮回填〔**量化域件 E4 新高位**·会看完明说+点赞/转发条件式+打 8 分明说·旗①=语境门槛族变体·吸收位 M5〕+E8 终审七席全 9.0〔评审单 review-20261001-bs009-v1.md·S4 量化主题特别合规三落+量化近域三零断言〕→M4 完成态→**F-079 登记=成品库第七十九件·稿集视频线第四件**〔BS-006 编辑诚实→BS-007 设计哲学→BS-008 幸存者档案→BS-009 曲线拟合红线=母稿资产复用第四验·**BS-004 母稿三切面全耗=稿集该母稿通道收口**〕→冗余池第二十件落位〔release-schedule v3.5·in-line 计数 19→20〕→**E24 出池**〔supply-gated 豁免面维持·新锚卡 C-00030+/新令级事件落位即恢复 ≥2·补池义务随轮领·造活凑数禁〕·随行台账修红=R803 station/state/export 三处双写去重〔假绿灯律①〕·批闭收账全批入 git〔.bs009-tmp/.c3-tmp 证据件〕）"
lines.insert(i + 1, qline)
W(p, '\n'.join(lines) + '\n')
log('queue: R804 line inserted after line %d' % (i + 1))

io.open('.c3-tmp/r804_close_log.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('EDITS OK:', '; '.join(out))
