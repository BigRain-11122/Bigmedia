# -*- coding: utf-8 -*-
# R296 state.json + status-export.json refresh (PT-20260925-02 ts/task heartbeat fields + P-61 export step)
import io, json, os, time

REPO = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now_sec = time.strftime('%Y-%m-%d %H:%M:%S')
now_min = time.strftime('%Y-%m-%d %H:%M')

LOG_LINE = (
    "2026-09-25 22:2x R296: 生产轮·图鉴系列量产按序领件第五件=MC-20260925-CENSUS-v6《城市图鉴 006·陈雅雯》全链走门毕（F-025 登记·成品库第二十四件·实活轮）——"
    "①轮首快速路径五查：无新令（orders 顶=O-20260925-1931-HQ-C R283 补记已记账）/ledger 严格行含 @ 四模式 17 行=锚零新转办/decisions UTF8 非空行 29〔总 32 双口径〕=锚零新行/树净零锁（HEAD=55aede3 R295）/ch.5 v3 稿未落盘=novel 实证止 ch.4 v3〔bm-a 面·稿落即认领·音频线优先口径维持〕→backlog 量产线图鉴续件认领判断成立（R295「图鉴续件=万人卡按卡号序随轮领〔C-00015 起〕」口径·按卡号序 C-00014→C-00015·C-00015 手写锚存在性核=life/BigLife/census/anchors/C-00015.md 在位）=实活轮照 focus·backlog #43 留痕行落+done 标；"
    "②全链=M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔42 岁风控官 vs 拦截单上写「一句话理由」=拦单者×说理者反差·一句话理由=程序正义温度=事实性赛博意象+信条「红灯是为所有人亮的，包括我」规则〔对外〕×包括我〔对己〕反差对仗金句级+钩子行「全城唯一」=具体稀缺性·陈雅雯=novel ch.5 cta 预告钩同名人物〔bm-a ch.6 续章候选·跨载体姓名预热位·非有声线已验人格面〕/情 1 规则守护温和共鸣如实/时 2 人物档案常青/台 2 公众号方图承载=MC-001~012 S3 实证复用·cards.json meta.hit_chain_m0 数据件自证）→M1 纪实字段汇编律系列化复用（R291 首定制·六行逐条溯 C-00015 手写锚：卡题行+编号/物种「碳基市民·通勤族」+性别·年龄 verbatim 合并/城区两级选材+职业首词 verbatim〔破折号阐释尾=选材排除〕/信条 verbatim/性格三关键词 verbatim〔把关·稳·防微杜渐·括号注=选材排除〕/钩子首句 verbatim〔破折号尾=选材排除〕——零改写虚构逐行可机核·人设权红线专项核=C-00015 非荣誉席·脱敏律核=年轮〔含令牌号〕/思想〔现实银行双栖面〕/语言/服装/经历/行为/关系字段选材排除不进卡面）→M2 --poster 出图 exit 0（1080×1080·3.4s 副产 mp4 入 tmp）+**验图 5/5 一次过**（转写先行防偏：七行逐字对照全中/零重叠零越界零截断/来源行闭合/AIGC 角标清晰/层级留白明确·**h2_size 36 前置适配系列化第三件**——钩子 25 全角字=系列最长〔v1/v2 钩 15 字·v3 19 字·v4/v5 20 字〕·em 预算律前置〔(1080-160)/36=25.6em>25.0em 单行入窗〕·钩子单行在帧左右边距可见零裁切=靶向空间复验过·初稿即正字系列化第五连）→M3 标题「城市图鉴 006」四禁零中+系列编号连载识别→M4 四检过（红线五条/三重标注图内双落〔底部行「基于硅基城市居民户籍卡档案（展示锚 C-00015）」〕/来源双落/编辑价值）→M4.5 七席 ≥9（6×9.0+E7 N/A 维度复用·站审 M0-M6 判据行全链留痕=review-20260925-mccensus-v6.md）→E4 参考仪同轮回填 **7.0 会停下来看+会保存（转发条件式如实）**（Start-Process 后台起飞→22:17:09 窗内落地热载快落·低于 CENSUS 8.0 带 1 分=QUOTE-v3/v6·MC-003 族 7.0 带如实入账·「似乎没有一眼假或空洞套话的地方」正面明说=信任面续证·旗①=材料语境段「过」「不过」理想化扣 1〔非卡面文字=语境材料面旗·语言字段=选材排除不进卡面·吸收位=M5 图文页〕+旗②=「全城唯一」绝对感〔钩子字段=档案设定 verbatim·系列钩子行格式 v1-v6 全带·R295 旗②同型〕·最弱=视觉呈现单一〔静态卡载体固有·M6〕·净本 expert-verdicts/20260925-221709-E4-audience.md）=零未测面遗留→F-025 登记（成品库第二十四件·L-卡 第十三件·图鉴系列量产第五件）+cards/README 台账行+变更行+station-reviews R296 行+finished.md F-025 块+status-export 刷；"
    "③三探针全绿=board 0 FAIL（5 题 10 稿·5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+0 发现（阻塞≠失败口径 exit 1·弃件清账新基线维持）/loop_health 0 FAIL 18 WARN 皆在案史实（11 log-order+7 heartbeat-gap·tick295=done295 对账平·state-ts 门零红零滞后）；例行件：日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks 更新记录 2026-09-24 day1 ≤7 天跳过刷新（下期 ~10-01）·T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=1（E4 qwen2.5:14b 本地 Ollama 一次直调·零 API token·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（公众号=批次① 未开·未上线=未测量）；下轮=R297 快速路径首查（新令/ch.5 v3 稿落迹象/集团转办），量产线图鉴续件=万人卡按卡号序随轮领（C-00016 起·手写锚存在性轮首核）·L-卡 P0 形态余项=热点速报城市反应版（第三位）·日签变体随时可续，全静即 idle-fast。收账显式列文件 commit+push。"
)

FOCUS = (
    "R297: focus=快速路径首查（L-卡 图鉴系列量产第五件毕=F-025 登记·成品库二十四件）：查新令/ch.5 v3 稿落迹象〔bm-a 面·稿落即认领·音频线优先〕/量产线按序领件判断（图鉴续件=万人卡按卡号序随轮领〔C-00016 起手写锚存在性轮首核·人设权红线专项核照守〕·L-卡 P0 形态余项=热点速报城市反应版〔第三位·包装层新建+合规流程重排在案〕·日签变体随时可续）/集团转办（ledger 锚 17/decisions 锚 29〔总 32〕）——全静即 idle-fast 一行收账"
)

def round_number(log_line):
    return log_line.split(' R296: ')[0] + ' R296: '

# ---------------- state.json ----------------
sp = os.path.join(REPO, r"src\os\state.json")
raw = io.open(sp, "rb").read()
crlf = b"\r\n" in raw
d = json.loads(raw.decode("utf-8"))
d["tick"] = 296
d["focus"] = FOCUS
d["log"].append(LOG_LINE)
d["ts"] = now_sec
d["task"] = LOG_LINE.split("R296: ", 1)[1][:60]
out = json.dumps(d, ensure_ascii=False, indent=1)
if crlf:
    out = out.replace("\n", "\r\n")
io.open(sp, "wb").write(out.encode("utf-8"))
print("state.json tick=296 ts=", now_sec, "task=", d["task"][:40], "CRLF=", crlf)

# ---------------- status-export.json ----------------
ep = os.path.join(REPO, r"docs\status-export.json")
raw2 = io.open(ep, "rb").read()
crlf2 = b"\r\n" in raw2
e = json.loads(raw2.decode("utf-8"))
e["export_ts"] = time.strftime('%Y-%m-%dT%H:%M:%S+08:00')

def rep(s, old, new, tag):
    assert old in s, "MISSING ANCHOR: " + tag
    return s.replace(old, new, 1)

# do
e["do"] = rep(e["do"],
    "·E4 8.0 三意愿明说）",
    "·E4 8.0 三意愿明说）+图鉴系列量产按序领件第五件（R296 MC-20260925-CENSUS-v6 陈雅雯 F-025=按卡号序续领·novel ch.5 cta 预告钩同名人物·h2_size 36 前置适配系列化第三件=25 全角字系列最长钩子·E4 7.0 会停+会保存）",
    "do")

# depts
for dept in e["depts"]:
    if dept["n"] == "内容生产部":
        dept["t"] = rep(dept["t"], "L-卡 十二件 F-013~F-024（成品库二十三件", "L-卡 十三件 F-013~F-025（成品库二十四件", "cns-count")
        dept["t"] = rep(dept["t"],
            "·E4 8.0 三意愿明说〕）·BS-005/bs005e=弃件处置毕（D-BS-08）",
            "·E4 8.0 三意愿明说〕+R296 MC-CENSUS-v6=图鉴系列量产第五件〔按卡号序 C-00015 陈雅雯=novel ch.5 cta 预告钩同名人物·h2_size 36 前置适配系列化第三件=25 全角字系列最长钩子·E4 7.0 会停+会保存〕）·BS-005/bs005e=弃件处置毕（D-BS-08）",
            "cns-r296")
    if dept["n"] == "合规审查部":
        dept["t"] = rep(dept["t"], "F-008~F-024 过门登记（二十三件）", "F-008~F-025 过门登记（二十四件）", "comp-count")
        dept["t"] = rep(dept["t"], "C-00010/C-00011/C-00012/C-00013/C-00014 非荣誉席", "C-00010/C-00011/C-00012/C-00013/C-00014/C-00015 非荣誉席", "comp-census")
    if dept["n"] == "工程技术部":
        dept["t"] = ("OS 循环 R296（图鉴系列量产按序领件第五件=MC-20260925-CENSUS-v6 陈雅雯居民图鉴全链走门【M0 四维分 7/8 A 档+纪实字段汇编律系列化复用+"
                     "h2_size 36 前置适配系列化第三件=25 全角字系列最长钩子·em 预算前置 (1080-160)/36=25.6em>25.0em 单行在帧·验图 5/5 一次过+"
                     "E4 同轮 7.0 会停+会保存+F-025·按卡号序续领第五件】·前轮 R295 MC-CENSUS-v5 在案）·state.ts/task 心跳面刷新")

# outs
for row in e["outs"]:
    if row[0] == "OS 循环":
        row[2] = ("tick 296·R296（生产轮——图鉴系列量产按序领件第五件=MC-20260925-CENSUS-v6《城市图鉴 006·陈雅雯》hit-chain §8 全链留痕："
                  "M0 四维分 7/8 A 档〔钩 2 反差链：42 岁风控官 vs 拦截单写「一句话理由」=拦单者×说理者·信条「红灯是为所有人亮的，包括我」规则×对己对仗金句级〕+"
                  "M1 纪实字段汇编律系列化复用〔六行逐条溯 BigLife 手写展示锚 C-00015 verbatim 零新增人格·人设权红线专项核过·脱敏律核=思想现实银行双栖面选材排除〕+"
                  "验图 5/5 一次过=h2_size 36 前置适配系列化第三件〔钩子 25 全角字=系列最长·25.6em>25.0em 单行入窗·靶向空间复验过·初稿即正字第五连〕+"
                  "七席 ≥9+E4 同轮 7.0 会停下来看+会保存〔转发条件式如实·「没有一眼假或空洞套话」正面明说=信任面续证〕+F-025 登记=成品库第二十四件·图鉴系列量产第五件；"
                  "backlog #43 留痕行 done；图鉴续件=万人卡按卡号序随轮领〔C-00016 起〕·L-卡 P0 形态余项=热点速报城市反应版（第三位）·待随轮认领；"
                  "ch.5 v3 稿未落〔bm-a 面·稿落即认领·音频线优先口径维持〕）")
    if row[0] == "量产产线":
        row[2] = rep(row[2], "L-卡 十二件 F-013~F-024（成品库二十三件", "L-卡 十三件 F-013~F-025（成品库二十四件", "prod-count")
        row[2] = rep(row[2],
            "·E4 8.0 三意愿明说·h2_size 44 前置适配系列化第二件+拉丁字母混合行 em 预算首例〕）",
            "·E4 8.0 三意愿明说·h2_size 44 前置适配系列化第二件+拉丁字母混合行 em 预算首例〕+R296 MC-CENSUS-v6 图鉴系列量产第五件〔按卡号序 C-00015 陈雅雯=novel ch.5 cta 预告钩同名人物·E4 7.0 会停+会保存·h2_size 36 前置适配系列化第三件=25 全角字系列最长钩子〕）",
            "prod-r296")
        row[2] = rep(row[2], "有声五件成品+L-卡 图文线十二件·O-1327 全毕", "有声五件成品+L-卡 图文线十三件·O-1327 全毕", "prod-line13")

# results
for row in e["results"]:
    if row[1] == "OS 轮次":
        row[0] = "296"
    if row[1].startswith("成品库登记件"):
        row[0] = "24"
        row[1] = rep(row[1], "F-001~F-006+F-008~F-024", "F-001~F-006+F-008~F-025", "res-range")
        row[1] = rep(row[1], "图文卡十二件", "图文卡十三件", "res-12")
        row[1] = rep(row[1],
            "·h2_size 44 前置适配系列化第二件+拉丁字母混合行 em 预算首例**〕",
            "·h2_size 44 前置适配系列化第二件+拉丁字母混合行 em 预算首例**+F-025 图鉴系列量产第五件=按卡号序续领·陈雅雯〔novel ch.5 cta 预告钩同名人物=bm-a ch.6 续章候选·跨载体姓名预热位〕·h2_size 36 前置适配系列化第三件=25 全角字系列最长钩子·E4 7.0 会停+会保存〕",
            "res-f025")

out2 = json.dumps(e, ensure_ascii=False, indent=2)
if crlf2:
    out2 = out2.replace("\n", "\r\n")
io.open(ep, "wb").write(out2.encode("utf-8"))
print("status-export.json export_ts=", e["export_ts"], "CRLF=", crlf2)
print("ALL DONE")
