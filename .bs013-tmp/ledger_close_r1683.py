# -*- coding: utf-8 -*-
# R1683 ledger close: station-reviews row + bs013 README changelog + backlog #102 done
import io

def patch(path, pairs, append_after=None):
    t = io.open(path, encoding="utf-8").read()
    for old, new in pairs:
        assert t.count(old) == 1, "%s anchor not unique (%d): %r" % (path, t.count(old), old[:40])
        t = t.replace(old, new)
    io.open(path, "w", encoding="utf-8", newline="\n").write(t)

# 1) station-reviews.md R1683 row (append at end)
sr_row = "| 2026-10-08 | **E8 终审+M4+F 登记·BS-013《板块十年·灯亮起来那天》（R1683·backlog #102 收官腿·「板块十年」预演系列第二件·D-20261008-03 补货行 2/2·**备货池两行全清=派单单款闭环**）** | bs-013-v1-shipinhao-60s.mp4+review-20261008-bs013-v1.md+asr-check.srt+asr-diff-r1683.txt | E8 收官=ASR 终轨（R169 QC recipe·11 cues/57.91s dropped=0 整轨一次过·**编号十四 b2 兑现位 100% 存活**+灯数行一/五数值全存活+时间锚全存活〔立国日 ×2/三年/十年/交给早晨〕+推演声明标签句值存活·实质退化如实 19 位点〔hook 系列名 板块→反馈/b2 片名兑现位簇 调试夜对频那秒→条事业绿萍大鸟/守夜灯灵→首页登陵/光语句/交晨首实例→焦辰/夜宵摊/看得见+量词 盏→展 ×4 同音族〕·**9.6% 字位=BS 系带上缘外溢 0.5pp→S2 8.5 诚实扣**·字幕轨 edge-tts 12/12 零损兜底=发布面零损）+评审单（S1 10/10〔R1681〕+S2 8.5+S3 9.0〔hits=[0] 单硬点克制档〕+S4 9.0+终审七席 E1/E2/E3/E5/E6/E7/E8 全 9.0）+E4 同轮回填 **8.0**（01:33:16 落判·会看完明说+8 分明说+会点赞+转发弱如实·**光语叙事形态正面定性**·旗①=光语句抽象扣 2=verbatim 档案锚〔C-00028〕M5 图文页吸收位·净本 20261008-013316-E4-audience.md）→M4 完成态→**F-161 登记**〔成品库第一百六十一件·视频线新形态第二件·冗余池第二十四件视频入池 v3.9〕+#102 done（D-20261008-03 行 2/2·**备货池两行全清=派单单款闭环**）·REACT-v12 顺延 F-162〔R978 判例〕 |\n"
t = io.open(r"docs\reviews\station-reviews.md", encoding="utf-8").read()
if sr_row.strip() in t:
    print("SKIP: station-reviews row already present")
else:
    if not t.endswith("\n"):
        t += "\n"
    t += sr_row
    io.open(r"docs\reviews\station-reviews.md", "w", encoding="utf-8", newline="\n").write(t)

# 2) bs013 README changelog row (append after R1682 row)
readme_row = "| 2026-10-08 | R1683 | 收官腿毕=ASR 终轨（R169 QC recipe 11 cues dropped=0·编号十四 b2 兑现位 100% 存活+灯数行一/五数值全存活·实质退化如实 19 位点·**9.6% 字位带上缘外溢 0.5pp=S2 8.5 诚实扣**·字幕轨零损兜底）+E4 8.0 同轮回填（净本 20261008-013316）+E8 评审单 review-20261008-bs013-v1.md（七席全 9.0）+M4+**F-161 登记**（成品库第一百六十一件·冗余池第二十四件 v3.9·D-20261008-03 备货池两行全清=派单单款闭环·REACT-v12 顺延 F-162） |\n"
t = io.open(r"data\sources\bs013\README.md", encoding="utf-8").read()
if readme_row.strip() in t:
    print("SKIP: bs013 README row already present")
else:
    if not t.endswith("\n"):
        t += "\n"
    t += readme_row
    io.open(r"data\sources\bs013\README.md", "w", encoding="utf-8", newline="\n").write(t)

# 3) backlog #102 done + R1683 交付毕 note
bk_head_old = "102. **「板块十年」系列第二件候选《灯亮起来那天》起链备位**"
bk_head_new = "102. [done 2026-10-08] **「板块十年」系列第二件候选《灯亮起来那天》起链备位**"
bk_tail_old = "回环 b0 三帧净+全分辨率零截断）——链余项=E8 终审〔ASR 终轨+E4 随行〕→M4→F 登记（下轮领）"
bk_tail_new = ("回环 b0 三帧净+全分辨率零截断）——链余项=E8 终审〔ASR 终轨+E4 随行〕→M4→F 登记（下轮领）\n"
    "   **[R1683 交付毕 2026-10-08]**：收官腿=E8 终审〔ASR 终轨 R169 QC recipe 11 cues/57.91s dropped=0 整轨一次过·"
    "**编号十四 b2 兑现位 100% 存活**+灯数行一/五数值全存活+时间锚全存活+推演标签句值存活·实质退化如实 19 位点"
    "〔hook 系列名/b2 片名兑现位簇/守夜灯灵/光语句/交晨首实例/夜宵摊/看得见+盏→展 ×4〕·"
    "**9.6% 字位带上缘外溢 0.5pp=S2 8.5 诚实扣**·字幕轨=edge-tts 直出 12/12 零损兜底〕"
    "+评审单 review-20261008-bs013-v1.md〔S1 10/10+S2 8.5+S3 9.0+S4 9.0+终审七席全 9.0+E4 8.0 同轮回填·净本 20261008-013316〕"
    "→M4→**F-161 登记**（成品库第一百六十一件·「板块十年」系列第二件·冗余池第二十四件视频入池 v3.9）——"
    "**#102 全链收官**（R1681 起链→R1682 渲染→R1683 收官三轮链零断洞·"
    "**D-20261008-03 备货池两行全清=派单单款闭环**·REACT-v12 顺延 F-162）")
patch(r"src\os\backlog.md", [(bk_head_old, bk_head_new), (bk_tail_old, bk_tail_new)])

print("OK: station-reviews + bs013 README + backlog #102 done")
