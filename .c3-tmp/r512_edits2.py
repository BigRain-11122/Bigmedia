# r512_edits2.py - sections 9-10 only: status-export + state accounting (sections 1-8 already applied)
import io, json, os, re, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

def main():
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    nowhm = time.strftime("%Y-%m-%d %H:%M")

    # status-export
    se_path = os.path.join(ROOT, "docs", "status-export.json")
    se = json.load(io.open(se_path, encoding="utf-8"))
    se["export_ts"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    for row in se["outs"]:
        if row[0] == "OS 循环":
            row[1] = ("tick 512：R512 件1 收口。（LC-001=E8 终审七席 9.0+ASR 终轨数字面值 100% 存活+M4→F-048 登记=成品库第四十七件·L-卡衍生视频线首件·D15 落位缺口 4→3 档·E4 参考仪在飞 R513 回填；#72 互聊台账到位消费收口〔C-00010 命中 2 条·令牌号脱敏排除·EP.02+ 候位〕；render-stale 尾注假阳性修红毕；探针 board 0 FAIL/readiness 3 外部阻塞 0 发现〔修红后复跑〕/loop_health 2F+22W 在案定型）")
        if row[0] == "量产产线" and len(row) >= 3:
            row[2] = row[2].replace("L-卡 三十五件 F-013~F-047（成品库四十六件", "L-卡 三十五件 F-013~F-047+LC-001 拆条视频 F-048（成品库四十七件")
            row[2] = row[2].rstrip() + "+**F-048=LC-001 拆条（L-卡衍生视频线首件·拆条试投形态立线首件·D15 落位·R512）**"
        if row[0] == "media-self-drive O-20260927-1050":
            row[2] = row[2].rstrip() + "; R512: agenda-2 piece-1 closed (LC-001 clip-cut F-048 registered, D15 slot filled 4->3, piece-2 BS-006+ next round) + interchat ledger consumed (#72 closed, U243 slot adjudicated to EP.02+)"
    for d in se["depts"]:
        if d["n"] == "工程技术部":
            d["s"] = ("R512: #79 piece-1 closeout done - LC-001 E8 final review + M4 + F-048 registered (47th finished piece, first L-card derivative video; D15 slot filled, video-slot gap 4->3); S2-seat ASR final-track (digits 100% alive, 7.3% char-noise in-band); E4 ref async in flight (PID 68016); render-stale tail-note false positive fixed (R147 precedent); interchat ledger arrived & consumed (#72 closed: C-00010 direct hits, internal token numbers excluded per desensitization; SC-003 s7 v1.2). Next R513: piece-2 BS-006+ kickoff + E4 backfill")
    r0 = se["results"][0]
    r0[0] = "512"
    r0[1] = ("R512 件1 收口：（LC-001 E8 终审+M4+F-048 登记·成品库第四十七件·L-卡衍生视频线首件·D15 落位·E4 在飞；#72 互聊台账消费收口）；探针=board 0 FAIL/readiness 3 外部阻塞 0 发现〔render-unannot+stale 双清·修红后复跑〕/loop_health 2F+22W 在案定型（account-lag +1 瞬态收账即平）")
    for row in se["results"]:
        if row[0] == "46":
            row[0] = "47"
            row[1] = row[1].replace("成品库登记件 F-001~F-006+F-008~F-047（短产线 N6 收官", "成品库登记件 F-001~F-006+F-008~F-048（短产线 N6 收官")
            row[1] = row[1].rstrip() + "；**F-048=LC-001 拆条（L-卡衍生视频线首件·D15 落位·R512）**"
        if row[0] == "509":
            row[0] = "511"
            row[1] = "R511 渲染腿收口：（LC-001 源卡即证据对位 12/12+R-E 渲染+S2 三门全绿+帧验三律+修红重渲毕；D-08 委员会件席 6 意见 F-05 窗内出具）；探针=board 0 FAIL/readiness 3 外部阻塞+1 在链预期红（render-unannot lc-001）/loop_health 2F+21W 在案定型（account-lag +1 瞬态）"
    with io.open(se_path, "w", encoding="utf-8") as fh:
        json.dump(se, fh, ensure_ascii=False, indent=1)
    print("STATUS-EXPORT OK export_ts=%s" % se["export_ts"])

    # state.json
    st_path = os.path.join(ROOT, "src", "os", "state.json")
    st = json.load(io.open(st_path, encoding="utf-8"))
    st["tick"] = 512
    st["focus"] = ("R513: #79 件2 稿集 BS-006+ 起链（排期表 §五-1 缺口剩 D18/D22/D25 三档·板源=data/drafts 10 稿 5 in production〔board 探针 09-27 读数〕·拍稿压缩链同 BS-002~004 先例：选稿→S1 v1.5+L18-L20 门→M1 即检→空气预算→TTS light→对位表素材探针先行→R-E shipinhao→S2 三门→E8 终审〔E4 随行〕→M4→F-049 登记→D18 落位）；首读 .lc001-tmp/e4-result.json 回填 LC-001 评审单 E4 行+expert-verdicts 存档+station-reviews 回填行（PID 68016 12:46:59 起 1500s 窗·追加制·非拦截）；窗口件随查（#59 REACT 09-28 届日领·daily_brief 09-28 缺则先补产·W40 周自审 09-28 开周+月度统计注记首件 ≤09-30·#70 OH 下窗 09-29 21:40 后开·#80 global-benchmarks 10-01 并窗·#63 C-00030/31 锚 supply-gated 照守·C-20260927-01 委员会意见窗 ≤09-29 12:00 记票归 HQ 决策轮）；探针执行注=loop_health account-lag +1 瞬态=尾轮自beat 残差既裁定型（lag ≥2 才=新断洞判据）；decisions 锚=56（委员会节并入后口径）；ledger 五模式锚=31（行数口径·大小写敏感·出现次数 34=同行双 @ 不另计）；orders O- 件锚=35（README.md 非令件不计）")
    logline = ("%s R512: 生产轮·#79 件1 收口毕（LC-001 E8 终审+M4+F-048 登记·成品库第四十七件·L-卡衍生视频线首件·D15 落位缺口 4→3 档·E4 参考仪在飞轮间回填）+互聊台账到位消费 #72 收口——①轮首五查：无新令（orders O- 件 35=锚·r512_check 36 含 README.md 计数口径笔误定谳·mtime 零新编辑）+ledger 行数口径 31=锚（34=同行双 @ 出现次数·R171 同型定谳）+decisions UTF8 非空行 56=锚零新行+树净零锁+production=open 自愈核在位；②#79 件1 收口=S2 席 ASR 终轨（R169 QC recipe medium-int8+beam5+noctx·11 cues/58.19s·asr-check.srt+asr-diff-r512.txt 洗净版：数字面值 100% 存活〔66→「66岁」/1980→「1980年」digit 形差分离·值零损〕+徐根福跨 cue 拼合存活+公众号净读+同音噪声 15 sites/205 字≈7.3% 系列带内〔BS-001 v15 9.1% 对照·全城→全程/算力→蒜栗/K线→K县/再绿→在律系 whisper 通道噪声级〕+字幕轨 edge-tts 直出 12/12 零损）→S2 9.0+评审单 review-20260927-lc001-v1.md（环节门 S1 10/10 R510/S2 9.0/S3 9.0/S4 9.0+终审七席 E1/E2/E3/E5/E6/E7/E8 全 9.0——七席 ≥9=PASS 放行候选→M4 完成态）+F-048 登记 finished.md+renders 行升「成品·#79 件1 D15 落位」+station-reviews R512 行+lc001 README 收口行+release-schedule 五处同步（46→47 件/视频号视频 4→5/D15 闭一/盘点 27 投放/§五-1 缺口 3 档+变更记录 v1.2）；③E4 参考仪异步起飞（.lc001-tmp/e4_call.py=.bs001-v15-tmp 同型适配·PID 68016 12:46:59 起·1500s 窗·e4-result.json 轮间落地=R513 回填追加制·非拦截）；④修红=readiness render-stale census-card-v7-vertical 尾注假阳性（盘上实存 data/sources/footage/ 706KB·R147 无扩展名写法先例·renders README L87+station-reviews L133 双改）；⑤#72 互聊台账到位消费收口（BigLife cognition/interchat-ledger.jsonl 08:57 落盘·22 条·早于 09-28 12:00 窗）：C-00010 顾阿凤直接命中 2 条（#19/#20 摊头粢饭对白×林之恒·烟火轴同位）但字面内嵌内部令牌号 O-20260923-2245-bm-a=脱敏律选材排除面→EP.01 v3 锁链不回炉（S1 10/10+定稿音轨）·「居民互聊实录拍」候位转 EP.02+ 续集候选（脱敏改写位）+其余 20 条=续集候选池直供（C-01360/C-01363 例汤夜宵摊=烟火轴强候选）——落件=SC-003-01-v1.md §7 v1.2+变更行+#72 done 标；⑥三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面+2 发现轮内双清复跑核实（render-unannot lc-001=升成品标清+render-stale=尾注修红清）/loop_health 2 FAIL+22 WARN 全定谳在案类零新增（49min=R425 足迹已裁定不重触发·account-lag +1 done512>tick511=尾轮自beat 残差瞬态·lag≥2 未破线·本轮收账 tick512 即平·22 WARN=13 log-order+9 heartbeat-gap 含 12:14→12:38 23min 长轮合法 WARN 级）；⑦例行件：日报 09-27 在案不重跑（09-28 件=明届日随窗补产）·W39 周审在案（W40 明日 09-28 开周+月度统计注记首件 ≤09-30）·global-benchmarks day3 ≤7 跳过（下期 ~10-01=#80 并窗）·T1 催办=已裁项停用口径·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=1（faster-whisper medium×1=ASR 校准用·非生成式 LLM 零 API token 类·E4 qwen 在飞未落=落地轮记账·P-54⑤ 计量律）·发布锁=M5 账号物理件不变（未上线=未测量）·窗口件随查（#59 REACT 09-28 届日领·#70 OH 下窗 09-29 21:40·#63 C-00030/31 supply-gated 照守·C-20260927-01 委员会意见窗 ≤09-29 12:00 记票归 HQ）。下轮=R513 首读 e4-result.json 回填 E4 行→#79 件2 稿集 BS-006+ 起链。收账显式列文件 commit+push。" % nowhm)
    st["log"].append(logline)
    st["ts"] = now
    m = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2} ", logline)
    body = logline[m.end():] if m else logline
    st["task"] = body[:60]
    with io.open(st_path, "w", encoding="utf-8") as fh:
        json.dump(st, fh, ensure_ascii=False, indent=1)
    print("STATE OK tick=512 ts=%s" % now)
    print("task=%s" % st["task"])

if __name__ == "__main__":
    main()
