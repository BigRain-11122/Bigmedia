# r512_e4backfill.py - E4 same-round backfill (hot-model fast landing)
import io, json, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

def edit(path, old, new, cnt=1):
    with io.open(path, "r", encoding="utf-8") as fh:
        t = fh.read()
    assert t.count(old) == cnt, "ANCHOR %d [%s] %s" % (t.count(old), old[:50], path)
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(t.replace(old, new))

def main():
    lt = os.path.join(ROOT, ".lc001-tmp")
    ev = json.load(io.open(os.path.join(lt, "e4-result.json"), encoding="utf-8"))

    # 1. verdict net archive
    arch = os.path.join(ROOT, "docs", "reviews", "expert-verdicts", "20260927-124659-E4-audience.md")
    with io.open(arch, "w", encoding="utf-8") as fh:
        fh.write("# E4 直觉观众参考仪 · 2026-09-27 12:46:59 · LC-001 拆条（F-048 收口轮同轮回填）\n\n")
        fh.write("> 非拦截席（dept-review §6 双态制）·材料=.lc001-tmp/voiceover.txt（12 拍口播全文）·模型=qwen2.5:14b·净本（ANSI/盲文轮转符已洗）\n\n")
        fh.write(ev["verdict"].strip() + "\n")
    print("ARCHIVE OK")

    # 2. review card E4 row + note + changelog
    rv = os.path.join(ROOT, "docs", "reviews", "review-20260927-lc001-v1.md")
    edit(rv,
         "| E4 | 直觉观众（参考仪·非拦截） | **在飞**（R512 12:46 起飞·PID 68016·1500s 窗·`e4-result.json` 轮间落地=R176/R448 先例·下轮回填追加制） | — | — |",
         "| E4 | 直觉观众（参考仪·非拦截） | **8.0**（R512 同轮回填·12:46:59 起飞热载快落=R382/R448 同型） | **会看完+点赞/转发可能性较大明说**=批次参考线带内持平（视频线 v15 重制带全 8.0·拆条首件同带）；「温暖且接地气」正面定性；旗①=「收盘铃，就是开饭铃」对译式比喻双读位（E2 事实性赛博意象优先律在案判正·真实律=源卡在册意象不删·观众侧轻微困惑=M6 校准线注记）；旗②=「算力楼唯一不谈数字的人」缺具体情景（拆条形态 12 拍容量限·场景细节=源卡卡面+M5 图文页语境层承接位） | 最弱=形式连接点（档案卡抽象·缺场景互动细节=R442「概念名词替代人物场景」同位） |")
    edit(rv,
         "**开发期七席（E1/E2/E3/E5/E6/E7/E8）全 ≥9 → PASS=放行候选 → M4 完成态**（E4 参考·非拦截·在飞轮间回填）。",
         "**开发期七席（E1/E2/E3/E5/E6/E7/E8）全 ≥9 → PASS=放行候选 → M4 完成态**（E4 参考·非拦截·**8.0=R512 同轮回填毕·轮内快落**）。")
    edit(rv,
         "- 未测面如实列：E4 受众参考（在飞）/完播率/点赞/转发（账号未开）/M5 图文页语境层（发布案收口面）。",
         "- 未测面如实列：完播率/点赞/转发实测（账号未开·M6 实测后校准）/M5 图文页语境层（发布案收口面）——E4 受众参考已测（8.0·同轮回填）。")
    with io.open(rv, "a", encoding="utf-8") as fh:
        fh.write("- 2026-09-27: v1.1——E4 参考仪同轮回填毕（R512·12:46:59 起飞热载快落）：8.0 会看完+点赞/转发可能性较大明说=批次参考线带内持平；两旗（收盘铃对译双读位/算力楼句缺具体情景）+最弱（形式连接点）如实入行，吸收位=M5 图文页语境层+续拆件场景细节预算；净本 `expert-verdicts/20260927-124659-E4-audience.md`。\n")

    # 3. station-reviews R512 row E4 segment
    edit(os.path.join(ROOT, "docs", "reviews", "station-reviews.md"),
         "**E4 参考仪在飞**〔R512 12:46:59 起飞 PID 68016·e4-result.json 轮间落地=R513 回填追加制·非拦截〕",
         "**E4 参考仪同轮回填 8.0**〔12:46:59 起飞热载快落轮内落判·会看完+点赞/转发可能性较大明说=批次参考线带内持平·两旗+最弱如实入行·净本 expert-verdicts/20260927-124659-E4-audience〕")

    # 4. finished.md F-048 row E4 note
    edit(os.path.join(ROOT, "output", "finished.md"),
         "E4 参考仪在飞·下轮回填·非拦截；轮内修红一件=双标识分层 48px〔R511〕",
         "E4 参考仪同轮回填 8.0〔会看完+点赞/转发可能性较大明说=批次参考线带内持平·两旗与最弱如实入行〕；轮内修红一件=双标识分层 48px〔R511〕")

    # 5. renders README L88 E4 note
    edit(os.path.join(ROOT, "output", "renders", "README.md"),
         "+E8 终审七席 9.0（review-20260927-lc001-v1.md·E4 参考仪在飞=R513 回填追加制）+M4→**F-048 登记**",
         "+E8 终审七席 9.0（review-20260927-lc001-v1.md·E4 参考仪同轮回填 8.0〔热载快落·净本 expert-verdicts/20260927-124659-E4-audience〕）+M4→**F-048 登记**")

    # 6. lc001 README E4 note
    edit(os.path.join(ROOT, "data", "sources", "lc001", "README.md"),
         "E4 参考仪在飞〔.lc001-tmp/e4_call.py·PID 68016 12:46:59 起·R513 回填追加制〕",
         "E4 参考仪同轮回填 8.0〔.lc001-tmp/e4_call.py·12:46:59 起飞热载快落·会看完+点赞/转发可能性较大明说=批次参考线带内持平〕")

    # 7. backlog #79 R512 note E4 phrase
    edit(os.path.join(ROOT, "src", "os", "backlog.md"),
         "终审七席全 9.0·E4 参考仪在飞=R513 回填追加制）+D15 落位",
         "终审七席全 9.0·E4 参考仪同轮回填 8.0）+D15 落位")

    # 8. status-export E4 mentions
    se_path = os.path.join(ROOT, "docs", "status-export.json")
    se = json.load(io.open(se_path, encoding="utf-8"))
    for row in se["outs"]:
        if row[0] == "OS 循环":
            row[1] = row[1].replace("E4 参考仪在飞 R513 回填", "E4 参考仪同轮回填 8.0（会看完+点赞/转发可能性较大明说=带内持平）")
    for d in se["depts"]:
        if d["n"] == "工程技术部":
            d["s"] = d["s"].replace("E4 ref async in flight (PID 68016)", "E4 ref same-round backfill 8.0 (hot-model fast landing)")
    se["results"][0][1] = se["results"][0][1].replace("E4 在飞；", "E4 同轮回填 8.0；")
    with io.open(se_path, "w", encoding="utf-8") as fh:
        json.dump(se, fh, ensure_ascii=False, indent=1)

    # 9. state.json log/focus amendments
    stp = os.path.join(ROOT, "src", "os", "state.json")
    st = json.load(io.open(stp, encoding="utf-8"))
    ln = st["log"][-1]
    assert "R512: 生产轮·#79 件1 收口毕" in ln
    ln = ln.replace("D15 落位缺口 4→3 档·E4 参考仪在飞轮间回填）", "D15 落位缺口 4→3 档·E4 参考仪同轮回填 8.0）")
    ln = ln.replace(
        "③E4 参考仪异步起飞（.lc001-tmp/e4_call.py=.bs001-v15-tmp 同型适配·PID 68016 12:46:59 起·1500s 窗·e4-result.json 轮间落地=R513 回填追加制·非拦截）；",
        "③E4 参考仪同轮回填（.lc001-tmp/e4_call.py=.bs001-v15-tmp 同型适配·PID 68016 12:46:59 起·热载快落轮内落判 e4-result.json：**8.0 会看完+点赞/转发可能性较大明说**=批次参考线带内持平〔视频线 v15 重制带全 8.0·拆条首件同带〕+两旗〔①「收盘铃=开饭铃」对译双读位=E2 事实性赛博意象优先律在案判正·真实律=源卡在册意象不删·M6 校准线注记②「算力楼唯一不谈数字的人」缺具体情景=拆条形态 12 拍容量限·场景细节=源卡卡面+M5 图文页语境层承接位〕+最弱=形式连接点〔R442「概念名词替代人物场景」弱点同位〕·判词净本 expert-verdicts/20260927-124659-E4-audience 存档）；")
    ln = ln.replace(
        "tokens:local=1（faster-whisper medium×1=ASR 校准用·非生成式 LLM 零 API token 类·E4 qwen 在飞未落=落地轮记账·P-54⑤ 计量律）",
        "tokens:local=2（faster-whisper medium×1=ASR 校准+E4 qwen2.5:14b×1 同轮回填·本地 Ollama 零 API token 类·P-54⑤ 计量律）")
    ln = ln.replace("下轮=R513 首读 e4-result.json 回填 E4 行→#79 件2 稿集 BS-006+ 起链。", "下轮=R513 #79 件2 稿集 BS-006+ 起链。")
    st["log"][-1] = ln
    st["focus"] = st["focus"].replace("；首读 .lc001-tmp/e4-result.json 回填 LC-001 评审单 E4 行+expert-verdicts 存档+station-reviews 回填行（PID 68016 12:46:59 起 1500s 窗·追加制·非拦截）", "")
    m = ln.find("R512:")
    st["task"] = ln[m:][:60] if m >= 0 else st["task"]
    with io.open(stp, "w", encoding="utf-8") as fh:
        json.dump(st, fh, ensure_ascii=False, indent=1)
    print("BACKFILL OK")

if __name__ == "__main__":
    main()
