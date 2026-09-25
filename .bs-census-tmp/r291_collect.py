# R291 collect-step script: state.json tick++ + log append + ts/task refresh (PT-20260925-02 law).
# UTF-8 file channel (encoding law); python json round-trip = no trailing-comma JSON break (R260 lesson).
import json, io, time

P = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
s = json.load(io.open(P, encoding="utf-8"))

s["tick"] = 291
s["focus"] = (
    "R292: **focus=快速路径首查（L-卡 P0 形态扩展次件毕=F-020 登记·成品库十九件·CENSUS 形态立线）**："
    "查新令/ch.5 v3 稿落迹象〔bm-a 面·稿落即认领〕/L-卡 P0 形态余项认领判断"
    "（图鉴续件=万人卡按编号序随轮领〔C-00011 朱鸿奎 起手写锚序列·人设权红线专项核照守〕·"
    "第三位=热点速报城市反应版〔包装层新建+合规流程重在案〕·日签变体随时可续·待随轮认领）/"
    "集团转办（ledger 锚 17/decisions 锚 29〔总 32〕）——全静即 idle-fast 一行收账"
)

row = (
    "2026-09-25 21:3x R291: 生产轮·L-卡 P0 形态扩展次件=MC-20260925-CENSUS-v1《城市图鉴 001·顾阿凤》"
    "全链走门毕（CENSUS 居民卡图鉴形态立线首件·#36 R289 提案「次位=居民卡图鉴」口径落地·F-020 登记·"
    "成品库第十九件·实活轮）——①轮首快速路径五查：无新令（orders 顶=O-1931 R285 已记账）/"
    "ledger 严格行含 @ 四模式 17=锚零新转办/decisions UTF8 非空行 29（总 32 双口径）=锚零新行/"
    "树净零锁（HEAD=4b3c4f9 R290）/ch.5 v3 稿未落盘=novel 实证止 ch.4 v3〔bm-a 面·稿落即认领·"
    "音频线优先口径维持〕→量产线 P0 形态次位认领判断成立=实活轮照 focus；"
    "②全链=M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔68 岁早点摊主 vs 心里整本口味账·"
    "蒸笼升腾的是暖光不是白汽=事实性赛博意象·「全城唯一」钩子行=具体稀缺性〕+"
    "信条句「灶上留一壶，路过的都是客」自带待客之道传播性·顾阿凤=F-009 有声线已验人格面同源人物/"
    "情 1 弄堂烟火温情如实/时 2 人物档案常青/台 2 方图实证复用·cards.json meta.hit_chain_m0 数据件自证）"
    "→M1 **纪实字段汇编律首定**（CENSUS 形态=户籍卡字段 verbatim 汇编·与 QUOTE 同文本律/DIGEST 数字汇编律并行位·"
    "六行逐条溯 life/BigLife census/anchors/C-00010.md 手写展示锚〔跨仓只读〕：卡题行+编号/"
    "物种行+性别·年龄行 verbatim 合并/城区行两级选材+职业行 verbatim/信条字段 verbatim/"
    "性格三关键词 verbatim〔括号注=选材排除不改写〕/钩子字段 verbatim——零改写虚构逐行可机核·"
    "**人设权红线专项核**=只引已登记字段零新增人格·C-00010 非荣誉席〔charter §2.4 荣誉席三卡=大圣/Qiqi/Rain 不涉〕·"
    "避讳律=BigLife 正典虚构居民名非真实人物名照 CODEX §五·脱敏律核=年轮行含令牌号与 CEO 令选材排除不进卡面）"
    "→M2 --poster 出图 exit 0（1080×1080·3.4s 副产 mp4 入 tmp）+验图 5/5 一次过（转写先行防偏："
    "七行逐字对照户籍卡全中/零重叠零越界零截断/来源行闭合/AIGC 角标清晰/层级留白明确=**CENSUS 版式首验**·"
    "QUOTE v2 参数复用+密度适配 H1 模式六行 h2 块·实测零漂移）→M3 标题「城市图鉴 001」四禁零中+"
    "「城市图鉴」系列名首立（与「城市语录」「城市盘点」平行·连载识别面）→M4 四检过（红线五条〔标题=内容即图鉴·"
    "承诺交付一致〕/三重标注图内双落〔AIGC 角标+底部行「基于硅基城市居民户籍卡档案（展示锚 C-00010）」〕/"
    "来源双落/编辑价值=图鉴体裁+十三字段选六+人物页叙事包装）→M4.5 七席 ≥9（6×9.0+E7 N/A 维度复用·"
    "站审 M0-M6 判据行全链留痕=review-20260925-mccensus-v1.md）→E4 参考仪同轮回填 **8.0 会停下来看+"
    "会保存并分享=三意愿正面明说**（QUOTE-v4/v5 同带·低于 DIGEST 9.0 如实入账·"
    "「信息丰富·适合社交媒体分享」=图鉴收集型面正面读数·旗①=「碳基市民·弄堂派」世界观词语门槛扣 2"
    "〔MC-003 同族·verbatim 字段律不可改写·吸收位=M5 图文页语境+系列语境〕·最弱=三词性格标签显单薄"
    "〔吸收位=M5 图文页正文=图鉴卡+文两段式·户籍卡经历/年轮细节有货〕·净本 expert-verdicts/20260925-212511-E4-audience.md）"
    "=零未测面遗留；③台账=F-020 登记（finished.md F-020 块+变更行）+cards/README 台账行+变更行+"
    "backlog #38 留痕行 done 标+station-reviews R291 行+status-export 刷（+CENSUS 纪实字段汇编律 chip·"
    "成品库 19 件）；④三探针全绿=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面"
    "（账号批次①+6/10 GATE+#17）+0 发现（阻塞≠失败口径 exit 1）/loop_health 0 FAIL 18 WARN 皆在案史实"
    "（tick290=done290 对账平·state-ts 门零红零滞后）；⑤例行件：日报 2026-09-25+W39 周审在案不重跑"
    "（Test-Path 实证）·global-benchmarks 更新记录 2026-09-24 day1 ≤7 天跳过刷新（下期 ~10-01）·"
    "T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·"
    "素材窗未探（实活轮生产优先·R283 复核在案·下轮快速路径复核先例）·tokens:local=1"
    "（E4=qwen2.5:14b 本地 Ollama 一次直调 21:25:11 落地热载快落·零 API token·P-54⑤ 计量律如实记）·"
    "发布锁=M5 账号物理件不变（公众号=批次① 未开·未上线=未测量）；L-卡 P0 形态余项=热点速报城市反应版"
    "（第三位·包装层新建+合规流程重排在案）·日签变体随时可续·图鉴续件=万人卡按编号序随轮领·待随轮认领"
    "（ch.5/ch.6 有声稿落盘时音频线优先口径维持）。下轮=R292 快速路径首查（新令/ch.5 v3 稿落迹象/集团转办），"
    "量产线图鉴续件或 REACT 包装层起链·全静即 idle-fast。收账显式列文件 commit+push。"
)
s["log"].append(row)
s["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
prefix_stripped = row.split("R291: ", 1)[1]
s["task"] = prefix_stripped[:60]

json.dump(s, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
chk = json.load(io.open(P, encoding="utf-8"))
print("JSON_OK tick=%s ts=%s" % (chk["tick"], chk["ts"]))
print("task=%s" % chk["task"])
