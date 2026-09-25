# R300 collection: update state.json (tick/log/ts/task/focus) + docs/status-export.json (export_ts/depts/outs/results)
# UTF-8 file-to-file; assertions guard every anchor replace.
import io, json, datetime

NOW = datetime.datetime.now()
ts_str = NOW.strftime("%Y-%m-%d %H:%M:%S")
log_prefix = NOW.strftime("%Y-%m-%d %H:%M")

LOG_LINE = (
    log_prefix + " R300: 生产轮·图鉴系列量产按序领件第九件=MC-20260925-CENSUS-v10《城市图鉴 010·老晶振》全链走门毕（F-029 登记·成品库第二十八件·实活轮）——"
    "①轮首快速路径五查静（无新令 orders 顶=O-1931 R283 补记已记账/ledger 严格行含 @ 四模式 17 行=锚零新转办/decisions UTF8 非空行 29〔总 32 双口径〕=锚零新行/树净零锁 HEAD=c17ecdf R299/ch.5 v3 稿未落盘=novel 实证止 SC-001-05-v1〔bm-a 面〕）→backlog 量产线图鉴续件认领判断成立（R299「图鉴续件=万人卡按卡号序随轮领〔C-00019 起·锚存在性轮首核〕」口径落地·C-00019 锚存在性核=在位）=实活轮照 focus·backlog #47 留痕行落+done 标；"
    "②全链=M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔三代机龄老引擎医生 vs 全城唯一手写「报错率」台账=最科技物种〔硅基民〕×最手工台账反差+信条「机器不坏是本事，坏了能修是人品」=本事〔技术〕×人品〔道德〕反差对仗金句级+钩子行「全城唯一」具体稀缺性·敲三下机箱/木头出诊箱/听声辨位认嗓音=事实性赛博意象·**CENSUS 第二件硅基民卡**〔v8 编译系后·光机魂系=新系首证·「三代机龄」=硅基民年龄制第二型〕·老晶振=万人卡新面孔〔无有声线前史·非跨载体复用如实注记〕/情 1 老派匠性温和共鸣如实非强极点〔护短=机器老伙计义气面〕/时 2 人物档案常青/台 2 方图承载=MC-001~016 S3 实证复用）→M1 纪实字段汇编律系列化复用（R291 首定制·六行逐条溯 C-00019 手写锚 verbatim 零改写零新增人格逐行可机核·人设权红线专项核=C-00019 非荣誉席·脱敏律核=年轮/思想/语言/服装/经历/行为/关系字段选材排除不进卡面）→M2 --poster 出图 exit 0（1080×1080·3.4s 副产 mp4 98KB 入 tmp）+验图 5/5 一次过（转写先行防偏：九行逐字对照全中/零重叠零越界零截断/全行单行零折行/来源行闭合/AIGC 角标清晰/层级留白明确·**h2_size 40 前置适配系列化第七件=信条长行驱动系列首例**——信条 21 全角字=系列信条行最长〔前最长 v7=15 字〕21.0em<23.0em 余量 2.0em〔靶向空间复验=右端约百像素黑底边距实证〕·h2_size 44 档排除首由信条行触发〔21.0em>20.9em〕=v4/v5/v7 钩子行驱动型对照·钩子 20 全角字次长 20.0em+binding 行=城区职业行「GAME 城 · 八号楼街区 · 引擎医生」16.05em〔GAME 拉丁段 ASCII 0.55em 估宽·R295 拉丁估宽法复用〕+物种行 17.22em 同帧单行入窗·初稿即正字系列化第九连）→M3 标题「城市图鉴 010」四禁零中+系列编号连载识别→M4 四检过（红线五条/三重标注图内双落/来源双落/编辑价值）→M4.5 七席 ≥9（6×9.0+E7 N/A 维度复用·站审 M0-M6 判据行全链留痕=review-20260925-mccensus-v10.md）→E4 参考仪同轮回填（Start-Process 脱壳 PID 17880·23:05:14 起→23:07:34 窗内落地热载快落：**8.0 会停下来看+会考虑保存或转发给朋友〔条件式〕=三意愿正面明说**〔CENSUS v1/v2/v4/v5/v7/v9 8.0 带持平·低于 v8 8.5 新高带 0.5 如实入账〕·「没有明显一眼假的地方」正面明说=信任面续证·**卡面文字零「一眼假」旗**〔Q2 旗落语境段非卡面〕·旗①=「现在的机器娇气」拟人化缺上下文扣 1〔**非卡面文字=E4 材料语境段旗**·思想字段=选材排除不进卡面·CENSUS-v4/v6/v7/v9 语境段旗同型·吸收位=M5 图文页正文〕·最弱=互动性和参与感〔静态卡载体固有·M6 校准位〕·净本 expert-verdicts/20260925-230734-E4-audience.md）=零未测面遗留；"
    "③**随行补账与修红三件**：finished.md F-028 块级登记补块（R299 收账缺口·变更行在案不改写·R297 F-025 补账先例）+cards/README v9 表行补行（R299 同型缺口）+cards/README v6/v7 合并表行拆行修红（R297 插入缺换行致 v6 行缺 F-025 号并入 v7 行·补 F-025 号+拆行·原行分数史不改写）；"
    "④台账=F-029 登记（成品库第二十八件·L-卡 第十七件·图鉴系列量产第九件）+cards/README 台账两行+变更行+station-reviews R300 行+finished.md F-029 块+变更行+backlog #47 done+status-export 刷；"
    "⑤例行件：日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=1（E4 qwen2.5:14b 本地 Ollama 一次直调·零 API token·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（公众号=批次① 未开·未上线=未测量）；"
    "下轮=R301 快速路径首查→图鉴续件（C-00020 起·锚存在性轮首核）或 ch.5/ch.6 有声稿落盘即音频线优先。收账显式列文件 commit+push。"
)

FOCUS_NEXT = (
    "R301: focus=快速路径首查（图鉴系列量产第九件毕=F-029 登记·成品库二十八件）：查新令/ch.5 v3 稿落迹象〔bm-a 面·稿落即认领·音频线优先〕/量产线按序领件判断（图鉴续件=万人卡按卡号序随轮领〔C-00020 起手写锚存在性轮首核〕·L-卡 P0 形态余项=热点速报城市反应版〔第三位·包装层新建+合规流程重排在案〕·日签变体随时可续）/集团转办（ledger 锚 17/decisions 锚 29〔总 32〕）——全静即 idle-fast 一行收账"
)

# ---- state.json ----
sp = r"src\os\state.json"
d = json.load(io.open(sp, encoding="utf-8"))
if d["tick"] == 299:
    d["tick"] = 300
    d["focus"] = FOCUS_NEXT
    d["log"].append(LOG_LINE)
    d["ts"] = ts_str
    d["task"] = LOG_LINE.split(" R300: ", 1)[1][:60]
    io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    print("STATE-OK tick=300 ts=", ts_str)
else:
    print("STATE-SKIP tick already", d["tick"])

# ---- status-export.json ----
se = r"docs\status-export.json"
e = json.load(io.open(se, encoding="utf-8"))
e["export_ts"] = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")
e["do"] = e["do"] + (
    "+图鉴系列量产按序领件第九件（R300 MC-20260925-CENSUS-v10 老晶振 F-029=按卡号序续领·**CENSUS 第二件硅基民卡**〔光机魂系=新系首证·「三代机龄」年龄制第二型〕·h2_size 40 前置适配=信条长行驱动系列首例〔信条 21 全角字系列信条行最长·44 档排除首由信条行触发 21.0em>20.9em〕·E4 8.0 会停+会考虑保存或转发〔条件式〕）"
)
for dept in e["depts"]:
    if dept["n"] == "内容生产部":
        dept["t"] = dept["t"] + (
            "+**R300 MC-CENSUS-v10=图鉴系列量产第九件**〔C-00019 老晶振=万人卡新面孔·**CENSUS 第二件硅基民卡**=光机魂系新系首证·「三代机龄」年龄制第二型·h2_size 40 信条长行驱动系列首例〔信条 21 字·44 档排除首由信条行触发〕·E4 8.0 三意愿正面明说〔条件式〕〕"
        )
    elif dept["n"] == "工程技术部":
        old = dept["t"]
        anchor = "R299（图鉴系列量产按序领件第八件=MC-20260925-CENSUS-v9 罗大壮居民图鉴全链走门【M0 四维分 7/8 A 档+纪实字段汇编律系列化复用+h2_size 40 前置适配系列化第六件（钩子 22 全角字与 v8 同长 22.0em+binding 行 16.05em 双长行同帧单行入窗）·验图 5/5 一次过+E4 同轮 8.0 三意愿正面明说+F-028·按卡号序续领第八件】·前轮 R298 MC-CENSUS-v8 在案）"
        assert anchor in old, "gongcheng anchor missing"
        dept["t"] = old.replace(anchor, "R300（图鉴系列量产按序领件第九件=MC-20260925-CENSUS-v10 老晶振居民图鉴全链走门【M0 四维分 7/8 A 档+纪实字段汇编律系列化复用+h2_size 40 前置适配系列化第七件=信条长行驱动系列首例（信条 21 全角字 21.0em+钩子 20 字 20.0em+binding 行 16.05em 同帧单行入窗）·验图 5/5 一次过+E4 同轮 8.0 三意愿正面明说〔条件式〕+F-029·按卡号序续领第九件】·前轮 R299 MC-CENSUS-v9 在案）")
    elif dept["n"] == "合规审查部":
        assert "F-008~F-028 过门登记（二十七件）" in dept["t"], "hegui anchor1 missing"
        assert "C-00010~C-00018 九卡非荣誉席" in dept["t"], "hegui anchor2 missing"
        dept["t"] = dept["t"].replace("F-008~F-028 过门登记（二十七件）", "F-008~F-029 过门登记（二十八件）").replace("C-00010~C-00018 九卡非荣誉席", "C-00010~C-00019 十卡非荣誉席")
# outs[0] OS 循环
e["outs"][0][2] = (
    "tick 300·R300（生产轮——图鉴系列量产按序领件第九件=MC-20260925-CENSUS-v10《城市图鉴 010·老晶振》hit-chain §8 全链留痕：M0 四维分 7/8 A 档〔钩 2 反差链：三代机龄老引擎医生 vs 全城唯一手写「报错率」台账=最科技物种〔硅基民〕×最手工台账反差·信条「机器不坏是本事，坏了能修是人品」=本事〔技术〕×人品〔道德〕反差对仗金句级·**CENSUS 第二件硅基民卡**=光机魂系新系首证〕+M1 纪实字段汇编律系列化复用〔六行逐条溯 BigLife 手写展示锚 C-00019 verbatim 零新增人格·人设权红线专项核过·脱敏律核=年轮/思想/语言/服装/经历/行为/关系字段选材排除〕+验图 5/5 一次过=h2_size 40 前置适配系列化第七件=信条长行驱动系列首例〔信条 21 全角字系列信条行最长 21.0em<23.0em+钩子 20 字 20.0em+binding 行 16.05em 同帧单行入窗·初稿即正字系列化第九连〕+七席 ≥9+E4 同轮 8.0 会停下来看+会考虑保存或转发〔条件式=三意愿正面明说〕（**卡面文字零「一眼假」旗**=信任面续证·旗①=「机器娇气」语境段旗〔非卡面文字·思想字段选材排除·吸收位 M5 图文页〕）+F-029 登记=成品库第二十八件·图鉴系列量产第九件；backlog #47 留痕行 done；**随行补账修红三件**=F-028 块补块（R299 收账缺口）+cards/README v9 表行补行+v6/v7 合并表行拆行修红（R297 插入缺陷·补 F-025 号）；图鉴续件=万人卡按卡号序随轮领〔C-00020 起·锚存在性轮首核〕·L-卡 P0 形态余项=热点速报城市反应版（第三位）·待随轮认领；ch.5 v3 稿未落〔bm-a 面·稿落即认领·音频线优先口径维持〕）"
)
# outs[1] 量产产线
p1 = e["outs"][1][2]
assert "L-卡 十六件 F-013~F-028（成品库二十七件" in p1, "outs1 anchor1 missing"
p1 = p1.replace("L-卡 十六件 F-013~F-028（成品库二十七件", "L-卡 十七件 F-013~F-029（成品库二十八件")
anchor2 = "·E4 8.0 三意愿正面明说〕〕）；"
assert anchor2 in p1, "outs1 anchor2 missing"
p1 = p1.replace(anchor2, "·E4 8.0 三意愿正面明说〕+**R300 MC-CENSUS-v10 图鉴系列量产第九件**〔C-00019 老晶振=万人卡新面孔·**CENSUS 第二件硅基民卡**=光机魂系新系首证·h2_size 40 信条长行驱动系列首例〔信条 21 字〕·E4 8.0 三意愿正面明说〔条件式〕〕〕）；")
e["outs"][1][2] = p1
# results
assert e["results"][0][0] == "299", "results tick anchor"
e["results"][0][0] = "300"
assert e["results"][4][0] == "27", "results F-count anchor"
r5 = e["results"][4][1]
assert "F-008~F-028（" in r5 and "图文卡十六件" in r5, "results desc anchors missing"
r5 = r5.replace("F-008~F-028（", "F-008~F-029（").replace("图文卡十六件", "图文卡十七件")
anchor3 = "·h2_size 40 钩子 22 字与 v8 同长+binding 16.05em 双长行一次过·E4 8.0 三意愿正面明说**〕；"
assert anchor3 in r5, "results desc anchor3 missing"
r5 = r5.replace(anchor3, "·h2_size 40 钩子 22 字与 v8 同长+binding 16.05em 双长行一次过·E4 8.0 三意愿正面明说**+**F-029 图鉴系列量产第九件=按卡号序续领·老晶振〔万人卡新面孔·**CENSUS 第二件硅基民卡**=光机魂系新系首证·「三代机龄」年龄制第二型〕·h2_size 40 信条长行驱动系列首例〔信条 21 字系列信条行最长·44 档排除首由信条行触发〕·E4 8.0 三意愿正面明说〔条件式〕**〕；")
e["results"][4][0] = "28"
e["results"][4][1] = r5
io.open(se, "w", encoding="utf-8", newline="\n").write(json.dumps(e, ensure_ascii=False, indent=2) + "\n")
print("STATUS-EXPORT-OK export_ts=", e["export_ts"])
