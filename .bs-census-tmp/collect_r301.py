# R301 collection: update state.json (tick/log/ts/task/focus) + docs/status-export.json (export_ts/depts/outs/results)
# UTF-8 file-to-file; assertions guard every anchor replace.
import io, json, datetime

NOW = datetime.datetime.now()
ts_str = NOW.strftime("%Y-%m-%d %H:%M:%S")
log_prefix = NOW.strftime("%Y-%m-%d %H:%M")

LOG_LINE = (
    log_prefix + " R301: 生产轮·图鉴系列量产按序领件第十件=MC-20260925-CENSUS-v11《城市图鉴 011·苏梓涵》全链走门毕（F-030 登记·成品库第二十九件·实活轮）——"
    "①轮首快速路径五查静（无新令 orders 顶=O-1931 R283 补记已记账/ledger 严格行含 @ 四模式 17 行=锚零新转办/decisions UTF8 非空行 29〔总 32 双口径〕=锚零新行/树净零锁 HEAD=b46ec38 R300/ch.5 v3 稿未落盘=novel 实证止 SC-001-05-v1〔bm-a 面〕）→backlog 量产线图鉴续件认领判断成立（R300「图鉴续件=万人卡按卡号序随轮领〔C-00020 起手写锚存在性轮首核〕」口径落地·C-00020 锚存在性核=在位）=实活轮照 focus·backlog #48 留痕行落+done 标；"
    "②全链=M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔24 岁年轻关卡建筑师 vs 关卡里藏着「住民的温柔」新手道永远比规程多留半步余量=年龄轻×匠性深反差+信条「每个转角都该藏一个惊喜。」=转角〔空间硬结构〕×惊喜〔情感软意图〕反差对仗金句级+钩子行「全城唯一」=具体稀缺性·彩蛋埋在光最暖的地方/给守夜人的专属关卡=事实性赛博意象·苏梓涵=万人卡新面孔〔无有声线前史·非跨载体复用如实注记〕/情 1 网络世代活力与住民温柔温和共鸣如实/时 2 人物档案常青/台 2 方图承载=MC-001~017 S3 实证复用）→M1 纪实字段汇编律系列化复用（R291 首定制·六行逐条溯 C-00020 手写锚：卡题行+编号/物种行「碳基市民·原生代」+性别·年龄行「女 · 24 岁」verbatim 合并/城区行「GAME 城 · 游戏楼街区」两级选材+职业行首词「关卡建筑师」verbatim〔破折号阐释尾=选材排除〕/信条字段 verbatim/性格三关键词 verbatim〔括号注=选材排除〕/钩子字段首句 verbatim〔破折号尾「梓涵的深夜惊喜」=选材排除〕——零改写虚构逐行可机核·人设权红线专项核=C-00020 非荣誉席·脱敏律核=年轮〔含令牌号〕/思想/语言/服装/经历/行为/关系字段选材排除不进卡面）→M2 --poster 出图 exit 0（1080×1080·3.4s 副产 mp4 98KB 入 tmp）+验图 5/5 一次过（转写先行防偏+靶向空间复验：九行逐字对照全中/零重叠零越界零截断/全行单行零折行〔钩子 22 字单行·两端 100px+ 边距实证〕/来源行闭合/AIGC 角标清晰/层级留白明确〔H1 下方 ~180px 空白带+底部行独立间隔带〕·**h2_size 40 前置适配系列化第八件=钩子长行驱动回摆型**——钩子 22 全角字〔与 v8/v9 同长〕22.0em<23.0em 余量 1.0em·44 档排除 22.0em>20.91em=v4/v5/v7/v9 同型〔v10 信条行驱动型对照〕·信条 17.0em 次长+binding 行=城区职业行「GAME 城 · 游戏楼街区 · 关卡建筑师」16.80em〔GAME 拉丁段 ASCII 0.55em 估宽·R295 拉丁估宽法复用〕+物种行 15.25em 同帧单行入窗·**em 预算 renderer _em_cost 机核化=em_check_r301.py 全行 OK 断言**〔手估升机核=工艺位精化〕·初稿即正字系列化第十连）→M3 标题「城市图鉴 011」四禁零中+系列编号连载识别→M4 四检过（红线五条/三重标注图内双落〔底部行「基于硅基城市居民户籍卡档案（展示锚 C-00020）」〕/来源双落/编辑价值=图鉴体裁+十三字段选六+人物页叙事包装）→M4.5 七席 ≥9（6×9.0+E7 N/A 维度复用·站审 M0-M6 判据行全链留痕=review-20260925-mccensus-v11.md）→E4 参考仪同轮回填（Start-Process 脱壳 PID 7984·23:26:52 起→23:27:20 落地热载快落 28s：**8.0 会停下来看+会保存+可能转发给朋友〔条件式〕=三意愿正面明说**〔CENSUS v1/v2/v4/v5/v7/v9/v10 8.0 带持平·低于 v8 8.5 新高带 0.5 如实入账〕·「创意性和信息的丰富性」+「巧妙融入游戏设计概念和人文关怀」=正面读数·旗①=钩子行「全城唯一」缺上下文支撑〔**卡面文字旗**=钩子字段档案设定 verbatim 不可改写·R295 旗② 同族·E4 自指正解=M5 图文页正文〕·最弱=背景信息进一步解释〔MC-003 族〕·净本 expert-verdicts/20260925-232720-E4-audience.md）=零未测面遗留（受众反应面+规格窗=如实列入评审单未测面节）；"
    "③台账=F-030 登记（成品库第二十九件·L-卡 第十八件·图鉴系列量产第十件）+cards/README 台账行+station-reviews R301 行+finished.md F-030 块+backlog #48 done+status-export 刷；三探针=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+0 发现（阻塞≠失败口径 exit 1）/loop_health 0 FAIL 18 WARN 皆在案史实（11 log-order+7 heartbeat-gap·R300 account-ahead 瞬态已随收账对账平消除）；"
    "④例行件：日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀·ledger 17=锚·decisions 29=锚）·tokens:local=1（E4 qwen2.5:14b 本地 Ollama 一次直调·零 API token·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（公众号=批次① 未开·未上线=未测量）；"
    "下轮=R302 快速路径首查→图鉴续件（C-00021 起·锚存在性轮首核）或 ch.5/ch.6 有声稿落盘即音频线优先。收账显式列文件 commit+push。"
)

FOCUS_NEXT = (
    "R302: focus=快速路径首查（图鉴系列量产第十件毕=F-030 登记·成品库二十九件）：查新令/ch.5 v3 稿落迹象〔bm-a 面·稿落即认领·音频线优先〕/量产线按序领件判断（图鉴续件=万人卡按卡号序随轮领〔C-00021 起手写锚存在性轮首核〕·L-卡 P0 形态余项=热点速报城市反应版〔第三位·包装层新建+合规流程重排在案〕·日签变体随时可续）/集团转办（ledger 锚 17/decisions 锚 29〔总 32〕）——全静即 idle-fast 一行收账"
)

# ---- state.json ----
sp = r"src\os\state.json"
d = json.load(io.open(sp, encoding="utf-8"))
if d["tick"] == 300:
    d["tick"] = 301
    d["focus"] = FOCUS_NEXT
    d["log"].append(LOG_LINE)
    d["ts"] = ts_str
    d["task"] = LOG_LINE.split(" R301: ", 1)[1][:60]
    io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    print("STATE-OK tick=301 ts=", ts_str)
else:
    print("STATE-SKIP tick already", d["tick"])

# ---- status-export.json ----
se = r"docs\status-export.json"
e = json.load(io.open(se, encoding="utf-8"))
e["export_ts"] = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")
e["do"] = e["do"] + (
    "+图鉴系列量产按序领件第十件（R301 MC-20260925-CENSUS-v11 苏梓涵 F-030=按卡号序续领·**h2_size 40 钩子长行驱动回摆型**〔22 字与 v8/v9 同长·em 预算 renderer _em_cost 机核化〕·E4 8.0 会停+会保存+可能转发〔条件式〕）"
)
for dept in e["depts"]:
    if dept["n"] == "内容生产部":
        dept["t"] = dept["t"] + (
            "+**R301 MC-CENSUS-v11=图鉴系列量产第十件**〔C-00020 苏梓涵=万人卡新面孔·h2_size 40 钩子长行驱动回摆型〔22 字与 v8/v9 同长·em 预算 _em_cost 机核化〕·E4 8.0 三意愿正面明说〔条件式〕〕"
        )
    elif dept["n"] == "工程技术部":
        old = dept["t"]
        anchor = "R300（图鉴系列量产按序领件第九件=MC-20260925-CENSUS-v10 老晶振居民图鉴全链走门【M0 四维分 7/8 A 档+纪实字段汇编律系列化复用+h2_size 40 前置适配系列化第七件=信条长行驱动系列首例（信条 21 全角字 21.0em+钩子 20 字 20.0em+binding 行 16.05em 同帧单行入窗）·验图 5/5 一次过+E4 同轮 8.0 三意愿正面明说〔条件式〕+F-029·按卡号序续领第九件】·前轮 R299 MC-CENSUS-v9 在案）"
        assert anchor in old, "gongcheng anchor missing"
        dept["t"] = old.replace(anchor, "R301（图鉴系列量产按序领件第十件=MC-20260925-CENSUS-v11 苏梓涵居民图鉴全链走门【M0 四维分 7/8 A 档+纪实字段汇编律系列化复用+h2_size 40 前置适配系列化第八件=钩子长行驱动回摆型（钩子 22 全角字与 v8/v9 同长 22.0em<23.0em·44 档排除·信条 17.0em+binding 行 16.80em 同帧单行入窗·em 预算 renderer _em_cost 机核化）·验图 5/5 一次过+E4 同轮 8.0 三意愿正面明说〔条件式〕+F-030·按卡号序续领第十件】·前轮 R300 MC-CENSUS-v10 在案）")
    elif dept["n"] == "合规审查部":
        assert "F-008~F-029 过门登记（二十八件）" in dept["t"], "hegui anchor1 missing"
        assert "C-00010~C-00019 十卡非荣誉席" in dept["t"], "hegui anchor2 missing"
        dept["t"] = dept["t"].replace("F-008~F-029 过门登记（二十八件）", "F-008~F-030 过门登记（二十九件）").replace("C-00010~C-00019 十卡非荣誉席", "C-00010~C-00020 十一卡非荣誉席")
# outs[0] OS 循环
e["outs"][0][2] = (
    "tick 301·R301（生产轮——图鉴系列量产按序领件第十件=MC-20260925-CENSUS-v11《城市图鉴 011·苏梓涵》hit-chain §8 全链留痕：M0 四维分 7/8 A 档〔钩 2 反差链：24 岁年轻关卡建筑师 vs 关卡里藏着「住民的温柔」新手道永远比规程多留半步余量=年龄轻×匠性深反差·信条「每个转角都该藏一个惊喜。」=转角〔空间硬结构〕×惊喜〔情感软意图〕反差对仗金句级·苏梓涵=万人卡新面孔〕+M1 纪实字段汇编律系列化复用〔六行逐条溯 BigLife 手写展示锚 C-00020 verbatim 零新增人格·人设权红线专项核过·脱敏律核=年轮〔含令牌号〕/思想/语言/服装/经历/行为/关系字段选材排除〕+验图 5/5 一次过=h2_size 40 前置适配系列化第八件=钩子长行驱动回摆型〔钩子 22 全角字与 v8/v9 同长 22.0em<23.0em 余量 1.0em·44 档排除·信条 17.0em+binding 行 16.80em+物种行 15.25em 同帧单行入窗·em 预算 renderer _em_cost 机核化=em_check_r301.py·初稿即正字系列化第十连〕+七席 ≥9+E4 同轮 8.0 会停下来看+会保存+可能转发给朋友〔条件式=三意愿正面明说〕（「创意性和信息的丰富性」+「巧妙融入游戏设计概念和人文关怀」=正面读数·旗①=钩子行「全城唯一」缺上下文支撑〔卡面文字旗=档案设定 verbatim 不可改写·R295 旗② 同族·吸收位 M5 图文页〕）+F-030 登记=成品库第二十九件·图鉴系列量产第十件；backlog #48 留痕行 done；图鉴续件=万人卡按卡号序随轮领〔C-00021 起·锚存在性轮首核〕·L-卡 P0 形态余项=热点速报城市反应版（第三位）·待随轮认领；ch.5 v3 稿未落〔bm-a 面·稿落即认领·音频线优先口径维持〕）"
)
# outs[1] 量产产线
p1 = e["outs"][1][2]
assert "L-卡 十七件 F-013~F-029（成品库二十八件" in p1, "outs1 anchor1 missing"
p1 = p1.replace("L-卡 十七件 F-013~F-029（成品库二十八件", "L-卡 十八件 F-013~F-030（成品库二十九件")
anchor2 = "·E4 8.0 三意愿正面明说〕+**R300 MC-CENSUS-v10 图鉴系列量产第九件**〔C-00019 老晶振=万人卡新面孔·**CENSUS 第二件硅基民卡**=光机魂系新系首证·h2_size 40 信条长行驱动系列首例〔信条 21 字〕·E4 8.0 三意愿正面明说〔条件式〕〕〕）；"
assert anchor2 in p1, "outs1 anchor2 missing"
p1 = p1.replace(anchor2, "·E4 8.0 三意愿正面明说〕+**R300 MC-CENSUS-v10 图鉴系列量产第九件**〔C-00019 老晶振=万人卡新面孔·**CENSUS 第二件硅基民卡**=光机魂系新系首证·h2_size 40 信条长行驱动系列首例〔信条 21 字〕·E4 8.0 三意愿正面明说〔条件式〕〕+**R301 MC-CENSUS-v11 图鉴系列量产第十件**〔C-00020 苏梓涵=万人卡新面孔·h2_size 40 钩子长行驱动回摆型〔22 字与 v8/v9 同长·em 预算 _em_cost 机核化〕·E4 8.0 三意愿正面明说〔条件式〕〕〕）；")
e["outs"][1][2] = p1
# results
assert e["results"][0][0] == "300", "results tick anchor"
e["results"][0][0] = "301"
assert e["results"][4][0] == "28", "results F-count anchor"
r5 = e["results"][4][1]
assert "F-008~F-029（" in r5 and "图文卡十七件" in r5, "results desc anchors missing"
r5 = r5.replace("F-008~F-029（", "F-008~F-030（").replace("图文卡十七件", "图文卡十八件")
anchor3 = "·h2_size 40 信条长行驱动系列首例〔信条 21 字系列信条行最长·44 档排除首由信条行触发〕·E4 8.0 三意愿正面明说〔条件式〕**〕；"
assert anchor3 in r5, "results desc anchor3 missing"
r5 = r5.replace(anchor3, "·h2_size 40 信条长行驱动系列首例〔信条 21 字系列信条行最长·44 档排除首由信条行触发〕·E4 8.0 三意愿正面明说〔条件式〕**+**F-030 图鉴系列量产第十件=按卡号序续领·苏梓涵〔万人卡新面孔〕·h2_size 40 钩子长行驱动回摆型〔22 字与 v8/v9 同长·em 预算 renderer _em_cost 机核化〕·E4 8.0 三意愿正面明说〔条件式〕**〕；")
e["results"][4][0] = "29"
e["results"][4][1] = r5
io.open(se, "w", encoding="utf-8", newline="\n").write(json.dumps(e, ensure_ascii=False, indent=2) + "\n")
print("STATUS-EXPORT-OK export_ts=", e["export_ts"])
