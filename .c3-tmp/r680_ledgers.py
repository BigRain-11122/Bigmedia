# -*- coding: utf-8 -*-
# R680: ledger updates - renders README (in-chain row + tmp declaration rewrite), station-reviews S2 row,
#       lc002 README production record, backlog #79 note
import io

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'

# ---------- 1. renders README ----------
P = ROOT + r'\output\renders\README.md'
t = io.open(P, encoding='utf-8').read()

OLD_SEG = (u"；渲染腿（对位表 cards-v1-matched+源件派生 census-card-v8-vertical"
           u"[F-027 PNG 派生 R511 法·AIGC 标签避让先例]+S2 三门+帧验三律）=R679+ 随轮扩写。")
NEW_SEG = (u"；**R680 渲染链毕**（批中间件扩写：build_leg_a.py[源件派生+对位表构建件]"
           u"+render_call.py[UTF-8 argv 渲染 wrapper·中文 series-id 防 GBK 坑]+s2_gates.py[S2 三门执法件]"
           u"+fs_extract.py[帧验三律采样件·fs-h00~11+fs-m/t 03/08/09+双 tile+双 labelzone 裁切]"
           u"+probe-v8-mid.png[源件探针帧]+s2-results.md[三门读数]）——同性质非成品·不入本表（R21 声明）；"
           u"正位数据件=`data/sources/lc002/`（**入 git**：voiceover-v1~v5.beats 空气预算裁稿链"
           u"[65.43→61.49→60.12→59.23→58.75s·正位留档·v2 标点位句拆清 M1 长句 WARN]"
           u"+README[R677 M0 选优定谲+R678/R680 生产记录]+s1-review-material-v1.md 评审材料"
           u"[锚 C-00017 逐拍字段级溯源对表+盲评律合规零嵌审计史]+**cards-v1-matched.json 对位表**"
           u"[R680·12/12 逐拍 visual·拆条形态源卡即证据]）；**自产素材源件**="
           u"`data/sources/footage/census-card-v8-vertical`（R680·F-027 成品卡 PNG 派生="
           u"scale 660+pad y=160+zoompan ≤1.04 微动 13s·ffprobe 与 v7 参照逐参数一致 1080×1920@30"
           u"·自产素材合法面=成品库自有件派生·mp4 gitignored 惯例·素材名无扩展名写法=R21/R512 探针防误报律"
           u"·探针帧验过[卡 9 行档案全读+AIGC 标签位=卡面左上定谲+净黑边距]）。")
assert t.count(OLD_SEG) == 1, 'renders README old seg count=%d' % t.count(OLD_SEG)
t = t.replace(OLD_SEG, NEW_SEG)

ROW = (u"| lc-002-v1-shipinhao-60s.mp4 | **在链·渲染腿毕（#79 尾注 D22 缺口续补首件·源卡=CENSUS-v8 F-027 归档者-07"
       u"·R678 起链五腿毕→R680 渲染+S2 三门+帧验三律→E8 终审+ASR 终轨+M4→F 登记+D22 落位=R681 收官待）** | "
       u"**R-E shipinhao 12 段 11 柔转场 0 硬切**（9:16 1080×1920·**58.75s ffprobe 实测·1.2s 余量**·hits=[0,11]"
       u"·**S5.5 角标常驻位**=BigStream\\|拆条 002·源城市图鉴 008+§4.5 三开关[glow/scanlines/sys.beat=NN t=MM:SS]"
       u"·plan.series+s45_dials 入 plan.json）；**拆条形态对位=源卡即证据 12/12**（census-card-v8-vertical 源卡派生件×12"
       u"[逐拍 req=钩子行/档案行/性格行/信条行 verbatim 直引+锚 C-00017 字段展开同源多用注记·b10 徐根福=锚内关系字段+F-026/LC-001 同城人物注记]"
       u"·visual-ratio 1.00·源件=F-027 PNG 派生 scale 660+pad y=160+zoompan ≤1.04·13s=LC-001 R511 法复制·素材探针先行九行全读）；"
       u"S2 三门 R680 循环独立执法**全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.583s·pacing CV 0.167"
       u"·prosody 9 档 12 拍·copy CV 0.170）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00"
       u"+transition-share 1.00 无连排+timeline 代数过）+spec 微信视频号双 PASS（9:16+58.75s ∈30-60s 窗 1.2s 余量）；"
       u"**帧验三律全过**：拍头 12/12 语义全中（源卡 9 行档案全读+拍标题 12 拍逐拍对位+sys.beat 01→12 连续）"
       u"+段中尾 6/6 稳定零录穿+**回环边界 crossings={} 零穿越**（max 拍 6.25s<源 13s·诚实计算）"
       u"+AIGC 双标识分层可读（帧头标识+卡面左上标识垂直错开无叠压·R511 标签避让先例**前置执行零修红**"
       u"·底部区裁切核验零碰撞）；plan.json 入 git；E8 终审+ASR 终轨（R169 QC recipe）+E4 随行→M4→F 登记→**D22 落位**"
       u"（排期表缺口 2→1 档）=R681 收官 |")
t = t.rstrip('\n') + '\n' + ROW + '\n'
io.open(P, 'w', encoding='utf-8').write(t)
print('renders README ok')

# ---------- 2. station-reviews ----------
P2 = ROOT + r'\docs\reviews\station-reviews.md'
t2 = io.open(P2, encoding='utf-8').read()
SR = (u"| 2026-09-29 | **S2 三门循环独立执法+帧验三律（lc-002-v1-shipinhao=#79 尾注 D22 缺口续补首件"
      u"·源卡 CENSUS-v8 F-027 归档者-07·R680 渲染腿）** | lc-002-v1-shipinhao-60s.mp4（R-E shipinhao 12 段·11 柔转场 0 硬切·58.75s） "
      u"| 循环独立执法（ai_feel+层 1.8+spec 微信视频号·纯脚本机检零 LLM）+帧验三律（会话内建多模态） | "
      u"—（机检档·E8 终审待 R681） | "
      u"对位表=cards-v1-matched（**拆条形态源卡即证据 12/12**：自产源件 census-card-v8-vertical"
      u"[=F-027 成品卡 PNG 派生·scale 660+pad y=160+zoompan ≤1.04·13s·ffprobe 与 v7 参照逐参数一致]×12 逐拍 req"
      u"[hook/b1/b10/b11=卡面行 verbatim 直引·b2-b9=锚 C-00017 字段展开同源多用注记·b10 徐根福=锚内关系字段+F-026 同城人物注记]"
      u"·visual-ratio **1.00**·素材探针先行=F-027 九行全读+AIGC 标签位卡面左上定谳[与 F-026 底部不同位]）；"
      u"S2 三门=ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.583s·pacing CV 0.167·prosody 9 档 12 拍·copy CV 0.170）"
      u"+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00+variety 无连排+timeline 代数过）"
      u"+spec 微信视频号双 PASS（9:16+58.75s ∈30-60s 窗 1.2s 余量） | "
      u"三门全绿+帧验三律全过：拍头 12/12 语义全中（源卡 9 行档案全读+拍标题逐拍对位+sys.beat 01→12 连续"
      u"+badge BigStream\\|拆条 002·源城市图鉴 008 完整）+段中尾 6/6 稳定零录穿+回环 crossings={}（max 拍 6.25s<源 13s·诚实计算）"
      u"+AIGC 双标识分层可读（帧头+卡面左上垂直错开无叠压·R511 修红先例前置执行=派生前垫底位 y=160+zoompan ≤1.04 零修红） "
      u"| `.lc002-tmp/`s2-results.md+fs-tile-heads.png+fs-tile-midtail.png+fs-h00-labelzone.png+fs-h11-bottomzone.png"
      u"+probe-v8-mid.png+cards-v1-matched.json+plan.json；E8 终审+ASR 终轨+E4 随行→M4→F 登记→D22 落位=R681 收官 |")
t2 = t2.rstrip('\n') + '\n' + SR + '\n'
io.open(P2, 'w', encoding='utf-8').write(t2)
print('station-reviews ok')

# ---------- 3. lc002 README ----------
P3 = ROOT + r'\data\sources\lc002\README.md'
t3 = io.open(P3, encoding='utf-8').read()
OLD3 = (u"- 余腿（随轮领）=对位表 cards-v1-matched（**源卡即证据=LC-001 同型**·源 PNG zoompan vertical 派生 R511 法："
        u"F-027 卡 1080×1080→scale 660+pad y=160+zoompan ≤1.04 微动·AIGC 标签位避让=LC-001 轮内修红先例）"
        u"→R-E shipinhao 渲染（--series-badge/--series-id=拆条 002·源城市图鉴 008+§4.5 三开关·§5.5 角标常驻位）"
        u"→S2 三门→帧验三律→E8 终审（ASR 终轨 R169 QC recipe+E4 随行）→M4→F 登记→**D22 落位**（排期表缺口 2→1 档）"
        u"=R679 起按序领。")
assert t3.count(OLD3) == 1, 'lc002 README old seg count=%d' % t3.count(OLD3)
NEW3 = (u"- 2026-09-29 R680 渲染腿毕：①素材探针先行=F-027 卡多模态九行全读（AIGC 标签位=卡面左上·与 F-026 底部不同位）"
        u"→②自产源件 `data/sources/footage/census-card-v8-vertical.mp4`（F-027 PNG 派生·scale 660+pad y=160+zoompan ≤1.04 微动 13s"
        u"·ffprobe 与 v7 参照逐参数一致 1080×1920@30·R511 法+标签避让先例**前置执行零修红**）"
        u"→③对位表 `cards-v1-matched.json` **12/12 逐拍 visual**（源卡×12·逐拍 req=钩子/档案/性格/信条行 verbatim 直引"
        u"+锚 C-00017 字段展开同源多用注记·b10 徐根福=锚内关系字段+F-026/LC-001 同城人物注记·visual-ratio 1.00）"
        u"→④R-E shipinhao 渲染 `output/renders/lc-002-v1-shipinhao-60s.mp4`（12 段 11 柔 0 硬切·58.75s ffprobe·1.2s 余量"
        u"·hits=[0,11]·S5.5 角标=BigStream\\|拆条 002·源城市图鉴 008+§4.5 三开关）"
        u"→⑤S2 三门循环独立执法**全绿**（ai_feel 0 FAIL 0 WARN gaps 11 处 0.220-0.583s·CV 0.167/0.170"
        u"+层 1.8 六面 PASS·visual-ratio 1.00+spec 微信视频号双 PASS 9:16+58.75s∈30-60s）"
        u"→⑥帧验三律**全过**（拍头 12/12 语义全中+段中尾 6/6 稳定零录穿+回环 crossings={}·max 拍 6.25s<源 13s"
        u"+AIGC 双标识分层可读垂直错开无叠压）——台账=renders 在链行+station-reviews S2 行+本 README；"
        u"批中间件 `.lc002-tmp/` 扩 build_leg_a.py/render_call.py/s2_gates.py/fs_extract.py+s2-results.md+帧验采样件。\n"
        u"- 余腿（R681 收官）=E8 终审（ASR 终轨 R169 QC recipe+E4 随行）→M4→F 登记→**D22 落位**（排期表缺口 2→1 档）。")
t3 = t3.replace(OLD3, NEW3)
io.open(P3, 'w', encoding='utf-8').write(t3)
print('lc002 README ok')

# ---------- 4. backlog #79 note ----------
P4 = ROOT + r'\src\os\backlog.md'
t4 = io.open(P4, encoding='utf-8').read()
anchor = u"**[R678 起链五腿毕 2026-09-29：LC-002 归档者-07 拆条第二件起链（claim 沿用 R677）"
idx = t4.find(anchor)
assert idx >= 0, 'backlog R678 anchor missing'
line_end = t4.find('\n', idx)
note = (u"\n   **[R680 渲染腿毕 2026-09-29（claim 沿用 R677/R678）：①素材探针先行=F-027 卡多模态九行全读"
        u"（AIGC 标签位=卡面左上定谳·与 F-026 底部不同位）→②自产源件 census-card-v8-vertical.mp4"
        u"（F-027 PNG 派生·scale 660+pad y=160+zoompan ≤1.04·13s·ffprobe 与 v7 参照逐参数一致·R511 法+标签避让先例前置执行零修红）"
        u"→③对位表 cards-v1-matched.json 12/12 逐拍 visual（源卡×12·钩子/档案/性格/信条行 verbatim 直引+锚 C-00017 字段展开同源多用注记"
        u"·b10 徐根福=锚内关系字段+F-026 同城人物·visual-ratio 1.00）→④R-E shipinhao 渲染 lc-002-v1-shipinhao-60s.mp4"
        u"（12 段 11 柔 0 硬切·58.75s ffprobe 1.2s 余量·hits=[0,11]·S5.5 角标=拆条 002·源城市图鉴 008+§4.5 三开关）"
        u"→⑤S2 三门循环独立执法全绿（ai_feel 0F0W·层 1.8 六面 PASS·spec 微信视频号双 PASS）"
        u"→⑥帧验三律全过（拍头 12/12 语义全中+段中尾 6/6 零录穿+回环 crossings={}·max 拍 6.25s<源 13s+AIGC 双标识分层可读）；"
        u"台账=renders 在链行+批中间件声明扩写+自产源件声明+station-reviews S2 行+lc002 README 生产记录；"
        u"R681 收官腿=E8 终审+ASR 终轨 R169 QC recipe+E4 随行→M4→F 登记→D22 落位（缺口 2→1 档）。**")
t4 = t4[:line_end] + note + t4[line_end:]
io.open(P4, 'w', encoding='utf-8').write(t4)
print('backlog ok')
print('ALL DONE')
