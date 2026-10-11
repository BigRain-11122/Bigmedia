# -*- coding: utf-8 -*-
"""R2002 register driver: F-179 ledger appends (finished.md / cards README /
station-reviews / queue marks). Append-only, anchor-guarded, UTF-8 no BOM."""
import io
import sys

FAILURES = []


def append_file(path, text):
    with io.open(path, "r", encoding="utf-8") as f:
        cur = f.read()
    if not cur.endswith("\n"):
        cur += "\n"
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(cur + text)
    print("APPENDED", path, len(text), "chars")


def guarded_replace(path, old, new, expect=1):
    with io.open(path, "r", encoding="utf-8") as f:
        cur = f.read()
    n = cur.count(old)
    if n != expect:
        FAILURES.append("%s: anchor count %d != %d for %r" % (path, n, expect, old[:60]))
        return
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(cur.replace(old, new, 1))
    print("REPLACED", path, "anchor OK")


# 1) finished.md F-179 block
F179 = (
    "\n**F-179 登记（R2002 评审腿兑现轮·tech#112 原子消费器第二单生产窗·断轮承接）**："
    "**L-卡 DIGEST 盘点形态第十八件=成品库第一百七十九件·L-卡 第一百二十八件**——"
    "MC-20261011-DIGEST-v18《城市盘点 018·全曲冲刺日数字盘点》静态卡全链走门毕"
    "（backlog #67 编年史事件随轮领第十七件·bigstream-lcard-pipeline 技能产线第二十五用·"
    "四段链=R1985 预置腿〔CPU 面 M0-M4 全毕·main#16 等待窗取活〕+R1986 e4-material 预载"
    "+R2001 尾发射器预置+**R2002 评审腿〔M4.5+E4+F〕=断轮承接**〔前 body 21:24:24 fire GO "
    "消费派发 E4+净本+评审单三件已落·收账前阵亡=本 body 同轮号承接续账·R155/R806/R1536/R1986 先例〕——"
    "**tech#112 fire_consume 原子消费器第二单生产窗**（21:24:24 卡=fire B-eviction-credit"
    "→同进程派发 e4_call.py PID 69440→21:24:36 落判 12s 热载快落"
    "=R1995/R1999「GO 后中间步耗窗」病族根除生产第二证·fire-consume-ledger 第三行））——"
    "素材源=**编年史 A 级事件簇**：10-11 全曲冲刺日 CEO 令批七行（11:3x 全曲整改冲刺令〔剧本四律 "
    "verbatim 尾链「一定要把故事写好！！！！！！逻辑通顺！！！！自然！！！立意高！！！！」〕"
    "+12:1x 追补令⑦-⑩+12:5x 全机队完整版冲刺令〔30 秒线封存 v4.5 样片终版〕+13:0x 导演席审查硬门"
    "+tw-mv-director skill 立档+13:2x 女主每曲独立选角律〔十曲十面孔〕+13:2x 执行落地机制令"
    "+13:4x MV 评审分层机制定谳令〔卡面主引文「mv的评审要分层级，导演是总控，专家是群审，"
    "我只是最后决定上线与否的。」逗号子句跨两行〕）+D-20261011-06 盘燃减负三帽采纳"
    "+本司单日六件登记 F-170~175——M0 7/8 A 档（十八连母题续 v18 全曲冲刺日·"
    "「1 句放权定谳令 vs 单日 7 令 6 成品」反差链+7/6/6/4/30/10/4/3/10-16 九组数字"
    "·CEO 放权+机器全速=信任面叙事）→M1 纪实汇编 18 断言（r1985_build_digest18.py·"
    "**R2002 复跑 ALL 18 ASSERTIONS GREEN**：A1/A1b 七令标签+10-11 行数 13／A2a-g 六段 CEO "
    "verbatim+卡面拼接==verbatim 等值／A3a-d 四正典件在盘〔skill/CASTING-LAW/EXECUTION-FIX-LEDGER/"
    "CEO-FEEDBACK〕／A4a-b D-20261011-06 在册+F-170..175 六登记／A5a-c em 三断言）"
    "→M2 --poster exit 0+em 32 档（v10/v16 长引文先例带·首跑 40 档 26.00em>23.0 预算 FAIL"
    "→降 32 档全链重跑全绿=R318 em 预算前置适配律执法·budget 28.75em·em costs 19.40/10.10/26.00/"
    "18.15/19.10/19.20/17.80·最长行=引文第二行 26.00em margin +2.75em）+验图五检 5/5"
    "（R1985 多模态十行全对位+R2002 独立转写复核 10/10 全中=双轮验证·零重叠零越界零折行"
    "·四层级留白明确）→M3「城市盘点 018」四禁零中→M4 四检过（红线五条+三重标注图内双落底部行"
    "「基于硅基城市真实事件（全曲冲刺日令批台账档案）」+来源双落+编辑价值=令→审→导→评→产→访"
    "七令递进链·P1 边界=纪实档案非提案非表决·他司执行面细节不入卡面）"
    "→M4.5 七席 6×9.0+E7 N/A=PASS（review-20261011-mcdigest-v18.md）"
    "+**E4 参考仪同轮回填 8.0**（21:24:36 落判·会停下来看+会保存或转发+8 分明说=三意愿正面"
    "·Q2 零扣分旗〔「没有一眼假或空话套话的地方」明说+日期/令数/整改项具体性正面定性=信任面续证〕"
    "·最弱=「盘燃减负三帽生效·判据回访窗 10-16」行晦涩=**语境门槛族四连**〔v15/v16/v17 同族〕"
    "·E4 自注内部受众面可能不算弱点如实注记·吸收位=M5 图文页语境+系列语境"
    "·**DIGEST 带 v15/v16/v17/v18=8.0 四连持平**·净本 expert-verdicts/20261011-212436-E4-audience.md"
    "·非拦截席）→M4 完成态——**F-179 登记**·发布锁=M5 账号物理件（未上线=未测量）"
    "；#67 留痕行维持开板（触发律+反膨胀律照守）\n"
)
append_file("output/finished.md", F179)

# 2) cards README line
README = (
    "- 2026-10-11: MC-20261011-DIGEST-v18 登记（R2002 评审腿兑现轮·backlog #67 编年史事件随轮领第十七件·"
    "bigstream-lcard-pipeline 技能产线第二十五用·四段链=R1985 预置腿+R1986 材料预载+R2001 发射器预置"
    "+R2002 评审腿〔断轮承接·**tech#112 fire_consume 原子消费器第二单生产窗**=21:24:24 GO→同进程派发 "
    "e4_call.py→21:24:36 落判 12s 热载快落〕）——素材源=**10-11 全曲冲刺日 CEO 令批七行**"
    "（A1 断言）+六段 CEO verbatim（卡面主引文=13:4x 评审分层令逗号子句跨两行=A2g 拼接等值断言）"
    "+D-20261011-06+F-170~175 单日六登记（A4b）——M0 7/8 A 档（十八连母题·放权定谳 vs 全速冲刺=信任面叙事）"
    "·M1 18 断言（**R2002 复跑 ALL GREEN**）·M2 em 32 档（40 档 26.00em>23.0 FAIL 降档=em 预算前置适配律执法"
    "·budget 28.75em 最长行 26.00em margin +2.75em）+验图五检 5/5 双轮验证（R1985+R2002 独立转写 10/10）"
    "·M3 四禁零中·M4 四检过·七席 6×9.0+E7 N/A（review-20261011-mcdigest-v18.md）"
    "+E4 同轮回填 8.0（三意愿正面+Q2 零扣分旗·旗=回访窗行语境门槛族四连〔v15/v16/v17 同族〕"
    "·**DIGEST 带 v15~v18=8.0 四连持平**·净本 20261011-212436-E4-audience.md）"
    "→**F-179 登记**（成品库第一百七十九件·L-卡 第一百二十八件·DIGEST 形态第十八件）"
    "·#67 留痕行维持开板\n"
)
append_file("data/storylines/cards/README.md", README)

# 3) station-reviews row
STATION = (
    "| 2026-10-11 | **DIGEST-v18《城市盘点 018·全曲冲刺日数字盘点》评审腿兑现+F-179 登记"
    "（R2002·#67 编年史事件随轮领第十七件·**断轮承接轮**=前 body 21:24:24 fire GO 消费派发 E4"
    "+净本+评审单三件已落·收账前阵亡·本 body 同轮号承接续账〔R155/R806/R1536/R1986 先例〕"
    "·tech#112 fire_consume 原子消费器第二单生产窗）** | MC-20261011-DIGEST-v18.png+cards.json"
    "+review-20261011-mcdigest-v18.md+净本 20261011-212436-E4-audience.md+fire-consume-ledger 第三行 | "
    "四段链收口=R1985 预置腿（CPU M0-M4·18 断言+验图 5/5）+R1986 材料预载+R2001 发射器预置"
    "+R2002 评审腿（**18 断言复跑 ALL GREEN**+独立转写 10/10 复核+M4.5 七席 6×9.0+E7 N/A=PASS"
    "+E4 8.0 同轮回填 12s 热载快落·三意愿正面+Q2 零扣分旗·旗=回访窗行语境门槛族四连）→M4 完成态"
    "→**F-179 登记**（成品库第 179 件·L-卡 第 128 件·DIGEST 形态第十八件·DIGEST 带 v15~v18=8.0 四连持平"
    "·吸收位=M5）·#67 留痕行维持开板 |\n"
)
append_file("docs/reviews/station-reviews.md", STATION)

# 4) queue main.md line 17 done mark
guarded_replace(
    "state/queue/main.md",
    "17. [R1985 补货·#67 触发律直领]",
    "17. [R2002 done 2026-10-11] [R1985 补货·#67 触发律直领]",
)
# append closure note at end of main.md line 17 (the line ends with F-179 登记
# before the \n) - use guarded replace on the line tail fragment
guarded_replace(
    "state/queue/main.md",
    "→M4.5 七席（评审单撰写）→E4 落判回填→F-179 登记",
    "→M4.5 七席（评审单撰写）→E4 落判回填→F-179 登记——【R2002 done 收口】评审腿兑现=F-179 登记毕"
    "（断轮承接·fire GO 21:24:24 原子消费器派发 E4 12s 快落·18 断言复跑全绿+独立转写 10/10+七席 6×9.0"
    "+E4 8.0 同轮回填·DIGEST 带 8.0 四连）·tech#105 消费序判据同步达成（四件全消费 F-176→179 零跳号）",
)

# 5) queue tech.md item 105 done mark + closure note
guarded_replace(
    "state/queue/tech.md",
    "105. [R1985 补货·本轮真发现]",
    "105. [done 2026-10-11 R2002] [R1985 补货·本轮真发现]",
)
guarded_replace(
    "state/queue/tech.md",
    "③维持现状人工判断；判据=下个 fire 窗消费完读数=四件窗口分配入档+F 号保序零跳号；判负留痕合法",
    "③维持现状人工判断；判据=下个 fire 窗消费完读数=四件窗口分配入档+F 号保序零跳号；判负留痕合法"
    "——【R2002 判据达成收口】四件全消费各窗单件接力（SC-005-04=R1995/F-176·05=R1996/F-177·"
    "06=R2000/F-178·DIGEST-v18 尾=R2002/F-179）+F 号保序零跳号 176→179·候选①序律 SOP=实际执行正身"
    "（SC-005 三连先发+v18 尾后段位）·候选②③未触发零动作",
)

if FAILURES:
    for f in FAILURES:
        print("GUARD-FAIL", f)
    sys.exit(1)
print("REGISTER-OK all appends+marks done")
