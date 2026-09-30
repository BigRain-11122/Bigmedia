# -*- coding: utf-8 -*-
# R688 LC-004 closeout ledger edits (renders row upgrade + declaration closeout +
# station-reviews row + release-schedule v1.6 + queue E4 exit + lc004 README closeout)
import io, re

def edit(path, old, new, must=True):
    s = io.open(path, encoding='utf-8').read()
    if old not in s:
        print('MISS in %s: %s' % (path, old[:60]))
        if must:
            raise SystemExit(1)
        return
    io.open(path, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
    print('OK %s' % path)

# 1. renders README L96 row: upgrade status marker + note tail
R = 'output/renders/README.md'
edit(R,
     '| lc-004-v1-shipinhao-60s.mp4 | **在链（queue §E 批活池 E4 件·冗余扩容位·源卡=CENSUS-v16 F-035 陆海峰·R686 起链→R687 渲染+S2 三门+帧验三律毕·收官腿 E8/ASR/E4/M4→F-058 随轮）**',
     '| lc-004-v1-shipinhao-60s.mp4 | **成品·冗余池落位（F-058·queue §E 批活池 E4 件收官·源卡=CENSUS-v16 F-035 陆海峰·R686 起链→R687 渲染→R688 收官=E8 终审+ASR 终轨+E4+M4 全链走门毕·拆条系列节律第三续件）**')
edit(R,
     'plan.json 入 git·E8 终审+ASR 终轨+E4→M4→F-058 收官腿下轮（tmp 批闭收账随收官轮 commit） |',
     'plan.json 入 git·**R688 收官**：ASR 终轨（R169 QC recipe 脱壳飞行 15:23 落地·关键事实词存活〔陆海峰/黄浦江/绕船三圈/十四号路灯/高小满/信条〕+海事方言词族退化如实〔慢班→万般×2/摆渡→百渡×2/铜哨/灯灵/靠泊/恒价=海事方言集中度系列最高件〕+同音噪声 20 sites/197 字≈10.2% 字位=系列带上缘之上新峰·字幕轨 edge-tts 12/12 零损兜底）+E4 参考仪同轮回填 8.0 看完明说（净本 expert-verdicts/20260929150358-E4-audience）+环节门 S1 10/10/S2 9.0/S3 9.0/S4 9.0+终审七席全 9.0（review-20260929-lc004-v1.md）→M4→**F-058 登记+冗余池落位（release-schedule v1.6）**·tmp 批闭随 R688 commit |')

# 2. renders README L91 declaration line: append closeout sentence
edit(R,
     '→收官腿（E8+ASR+E4+M4→F-058 登记→冗余池落位）随轮领。',
     '→**R688 收官腿毕（ASR asr_r688.py+asr_diff_r688.py+E4 e4_call.py 全脱壳飞行同窗落地）：F-058 登记+冗余池落位**——E8 评审单 review-20260929-lc004-v1.md（七席 ≥9→M4）+ASR 终轨 10.2% 字位海事方言密度新峰如实入档+E4 同轮回填 8.0+station-reviews 收官行+lc004 README 收口。')

# 3. station-reviews closeout row
SR = 'docs/reviews/station-reviews.md'
row = ('\n| 2026-09-29 | **E8 终审+ASR 终轨+M4 收官（lc-004-v1-shipinhao=queue §E 批活池 E4 件·冗余扩容位收官件·F-058·排期表冗余池首件视频入池·R686 claim 兑现·R688 收官腿）** '
       '| lc-004-v1-shipinhao-60s.mp4（R-E shipinhao 12 段 11 柔 0 硬切·58.68s）+.lc004-tmp/ audio.mp3 '
       '| 循环独立执法（ASR 终轨 R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1 满载机面脱壳飞行 15:01 起·15:23 落地 exit 0→asr-check.srt+asr_diff_r688.py 量化〔R681/R685 先例+繁转简化归计算 BS-006 同型〕）+E8 终审评审单（review-20260929-lc004-v1.md）+E4 参考仪（e4_call.py 脱壳 15:03:58 热载快落·**同轮回填 8.0 看完明说**+文化意义正面定性〔「传统与现代、速度与稳重冲突共存」〕·净本 expert-verdicts/20260929150358-E4-audience） '
       '| E8 终审+M4 '
       '| **ASR 终轨**：关键事实词存活（陆海峰/弄堂派/渡轮船长/三流数据道/活船老大/黄浦江/绕船三圈/一步不少/十四号路灯必到/全船人合唱/一句多谢/高小满开船/沉江/信条/船稳人心才稳/公众号）；海事方言词族实质退化如实（慢班→万般×2 核心梗词双损/摆渡→百渡×2/旧铜哨→就同上/雾→顾+午×2/灯灵→登临/靠泊→拨/恒价→横=**海事方言词集中度系列最高件**·LC-003 方言梗词密度件同族升档）+物种行 碳基市民→探机是民（LC-003 同位损）+CTA 双损（档案→答案/转给→准备）+系统日志→系统日制/全城→全程系列复发族；同音噪声 20 sites/31 diff chars/197 字≈**10.2% 字位=系列带上缘之上新峰**（LC-001 7.3%/LC-002 8.4%/LC-003 9.5% 对照·TTS 读数确定性无损·E4 听音侧引「慢班」句 verbatim=观众侧理解存活直接证据·字幕轨 edge-tts 直出 12/12 零损兜底） '
       '| **环节门**：S1 10/10（R686 一次过）/S2 9.0/S3 9.0/S4 9.0+**终审七席 E1/E2/E3/E5/E6/E7/E8 全 9.0→PASS 放行候选→M4 完成态**（E4 同轮回填 8.0·E3 席拆条系列节律第三续验=四件连载链闭环注记·冗余扩容位首件）；F-058 登记（成品库第五十八件·L-卡衍生视频线第四件）+**冗余池落位=排期表冗余池首件视频入池（release-schedule v1.6·M6 调仓弹药/日更冗余预备）**+renders 行升「成品·冗余池落位」+queue §E E4 出池（lane=E3 窗位单条·补池候选=BS-007 稿集件/陆海峰后顺位随选优轮评估） '
       '| review-20260929-lc004-v1.md+asr-check.srt+asr-diff-r688.txt+e4-result.json+lc004 README 收口行+finished.md F-058 块+tmp 批闭随本轮 commit（.lc004-tmp/） |\n')
s = io.open(SR, encoding='utf-8').read()
if 'F-058' in s:
    print('SKIP station-reviews (F-058 already present)')
else:
    io.open(SR, 'a', encoding='utf-8', newline='').write(row)
    print('OK station-reviews append')

# 4. release-schedule v1.6: redundancy pool line + changelog
RS = 'docs/release-schedule-v1.md'
s = io.open(RS, encoding='utf-8').read()
m_old = '冗余池 v1.0 计 18 件（QUOTE F-015~F-018×4+CENSUS F-031~F-036/F-038~F-040×9+DIGEST F-046/F-047×2+REACT 3 件机动）+F-050~F-056 七件 L-卡后续产（DIGEST-v7~v10/REACT-v4/v5·随产随入池）=M6 调仓弹药+30 天日更冗余'
m_new = '冗余池 v1.0 计 18 件（QUOTE F-015~F-018×4+CENSUS F-031~F-036/F-038~F-040×9+DIGEST F-046/F-047×2+REACT 3 件机动）+F-050~F-056 七件 L-卡后续产（DIGEST-v7~v10/REACT-v4/v5·随产随入池）+**LC-004 拆条 F-058（R688·冗余池首件视频入池·陆海峰《城市图鉴 016》·拆条系列节律第三续件）**=M6 调仓弹药+30 天日更冗余'
if m_old in s:
    io.open(RS, 'w', encoding='utf-8', newline='').write(s.replace(m_old, m_new, 1))
    print('OK release-schedule pool line')
else:
    print('MISS release-schedule pool line')
s = io.open(RS, encoding='utf-8').read()
cl = ('\n- v1.6 2026-09-29 R688：**冗余池扩容首件视频入池**（LC-004《城市图鉴 016·陆海峰》拆条=F-058·成品库 57→58 件·L-卡衍生视频线第四件=拆条系列节律第三续件·R686 入池评定夺→R687 渲染→R688 收官全链走门：S1 10/10+ASR 终轨 10.2% 字位海事方言密度新峰如实+E4 8.0+七席 ≥9→M4）；§五 盘点行同步（冗余池视频弹药+1·M6 调仓/日更冗余预备·预产窗=开号前）。\n')
if 'v1.6 2026-09-29 R688' in s:
    print('SKIP release-schedule changelog (present)')
else:
    io.open(RS, 'a', encoding='utf-8', newline='').write(cl)
    print('OK release-schedule changelog')

# 5. queue §E: E4 exit line
Q = 'docs/self-improvement-queue.md'
s = io.open(Q, encoding='utf-8').read()
q_old = '——收官腿（E8+ASR+E4+M4→F-058→冗余池落位）随轮领。'
q_new = ('——**R688 收官毕：F-058+冗余池落位（E8 七席 ≥9→M4·ASR 终轨 10.2% 字位海事方言密度新峰如实+E4 同轮回填 8.0 看完明说）→E4 出池**。'
         '批活池常备降至 E3 REACT-v6（09-30 热点窗位）单条<2（C-20260929-02 B 款 lane ≥2 口径）→**补池义务注记**：下轮随 E3 窗开同步补位（候选=BS-007 稿集件/陆海峰后顺位拆条〔CENSUS 库 35 卡余量〕·随选优轮评估入池）。')
if q_old in s:
    io.open(Q, 'w', encoding='utf-8', newline='').write(s.replace(q_old, q_new, 1))
    print('OK queue E4 exit')
else:
    print('MISS queue E4 exit line')

# 6. lc004 README closeout line
RM = 'data/sources/lc004/README.md'
s = io.open(RM, encoding='utf-8').read()
if 'R688 收官腿毕' in s:
    print('SKIP lc004 README closeout (present)')
else:
    add = ('\n- 2026-09-29 R688 收官腿毕（E4 件全链走门收官=F-058 登记+冗余池落位）：①ASR 终轨（R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1 满载机面脱壳飞行 15:01-15:23 落地 exit 0·asr-check.srt+asr-diff-r688.txt）——关键事实词存活（陆海峰/弄堂派/黄浦江/绕船三圈/十四号路灯必到/一句多谢/高小满/信条船稳人心才稳/公众号）+海事方言词族实质退化如实（慢班→万般×2 核心梗词双损/摆渡→百渡×2/旧铜哨→就同上/灯灵→登临/靠泊→拨/恒价→横=**海事方言词集中度系列最高件**·LC-003 方言梗词密度件同族升档）+CTA 双损（档案→答案/转给→准备）+同音噪声 20 sites/31 diff/197 字≈**10.2% 字位=系列带上缘之上新峰**（LC-001 7.3/LC-002 8.4/LC-003 9.5 对照·TTS 读数确定性无损·E4 听音侧引「慢班」句 verbatim=观众侧理解存活直接证据·字幕轨 edge-tts 直出 12/12 零损兜底）→S2 9.0；②E4 参考仪同轮回填 **8.0 看完明说**（15:03:58 热载快落·「传统与现代、速度与稳重冲突共存」文化意义正面定性·双旗=慢班宣言句+船票恒价句皆 verbatim 卡锚=MC-003 语境门槛族·吸收位 M5 图文页语境·净本 expert-verdicts/20260929150358-E4-audience）；③E8 终审评审单 review-20260929-lc004-v1.md（环节门 S1 10/10〔R686〕/S2 9.0/S3 9.0/S4 9.0+终审七席全 9.0→PASS 放行候选→M4 完成态）；④**F-058 登记**（成品库第五十八件·L-卡衍生视频线第四件=拆条系列节律第三续件）+**冗余池落位**（release-schedule v1.6·冗余池首件视频入池）+renders 行升「成品·冗余池落位」+queue §E E4 出池。\n')
    io.open(RM, 'a', encoding='utf-8', newline='').write(add)
    print('OK lc004 README closeout')

print('ALL_EDITS_DONE')
