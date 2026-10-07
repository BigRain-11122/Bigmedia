# -*- coding: utf-8 -*-
# R1689 close: renders row + station-reviews row + bs015 README + backlog #104 note + state.json + status-export.json
import json, io, os, datetime

def read(p):
    return io.open(p, encoding="utf-8").read()

def write(p, s):
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)

ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 0) cleanup stale untracked leftover from R1688 commit-message staging
p = ".c3-tmp/r1688_commit.txt"
if os.path.exists(p):
    os.remove(p)

# 1) renders README row (append at end of table)
RR_ROW = ("| bs-015-v1-shipinhao-60s.mp4 | **生产件·在链（#104「板块十年」系列第四件《台风夜之后》·形态 C 台风梅花三视角·R1687 起链+S1 10/10〔R1688 根因修复后〕→R1689 渲染腿毕→收官腿 E8/M4/F-163 登记=下轮领·render-unannot 在链预期红=F-163 登记即清〔R173/R1686 同型〕）** | "
    "**R-E shipinhao 12 段 11 柔转场 0 硬切**·9:16 1080×1920·**58.51s spec 实测=音轨分毫一致·1.49s 余量**·hits=[0]·**S5.5 角标常驻位**=BigStream\\|BS-015 EP.15+§4.5 三开关[glow/scanlines/sys.beat=NN t=MM:SS]·plan.series+s45_dials 入 plan.json·**形态 C 三视角拆条对位 11/12=0.92**（素材探针=census-card-v18/v19/v20 三时点〔1.3/6.5/11.7s〕多模态核验**全静态·零录穿·零隐私**+全分辨率二验 v18=C-00027 邓建国感知塔站值守员/v19=C-00028 十四号路灯/v20=C-00029 咪喱=BigLife census/anchors 正典锚一致〔tile 3x3 低清首读名称互换误判=读数手段问题如实注记·R189/R1680 tile 失读族〕+looplog/reviewsdoc/editgrid=R808 probe-r808 在案证据复用+citywatch 源裁净窗 4.400s=R188/R197 修红链·拍长于源走 stream_loop 回环）：citywatch×1〔b0 观城台=题眼观测面·BS-012/013/014 b0 同位〕+looplog×2〔b1 系统回事件档案=日志字面直证/b9 真话在册〕+census-v19×1〔b2 灯视角直接证据〕+census-v18×2〔b3 塔视角/b4 塔起名 wink=同源多用注记·C-00027 钩子字段尾段 verbatim 源卡〕+census-v20×1〔b5 猫视角直接证据〕+editgrid×2〔b6 时间轴压条=形态 C 制式位/b10 AI 剪辑自指〕+reviewsdoc×2〔b7 推演声明档案载体/b8 三样在册对账〕+cards-only×1〔b11 CTA=BS-012/013/014 b11 同位〕·**三视角拆条混剪=形态 C 拆条面第二证**（R1685 v13 单卡首证→本件 v18/v19/v20 三卡直接证据面）——"
    "**S2 三门 R1689 循环独立执法全绿**：ai_feel 0F0W〔gaps 11 处 0.220-0.558s varied/pacing CV 0.233/prosody 9 档/copy CV 0.253〕+层 1.8 六面 PASS〔beat-align 11/11+camera 12 段全动+visual-ratio 0.92+transition-share 1.00 无连排+variety+timeline 代数过〕+spec 微信视频号双 PASS〔9:16+58.51s ∈30-60s 窗 1.5s 余量〕——**帧验三律全过（R1689）**：拍头 12/12 语义全中（H1/H2 逐拍对位+sys.beat 01→12 连续+badge 全帧在+AIGC 全帧可读）+回环边界 b0 三帧零录穿（4.400s 穿越点 pre/x/post 全净·净源链继承实证）+全分辨率三帧复核（b2 拆条卡 C-00028 逐字正+补丁无错字/b7 拍中角标+字幕逐字齐/b11 字幕逐字一致·AIGC 括号串净读·无截断无乱码）·**nitpick 三注（诚实律·E8 评审面输入）**：①b2 双层 AIGC 标注=拆条源卡自带 AIGC 行+成片常驻标识合规冗余非缺陷（census 拆条面固有）②b11 H2「台/风夜」跨行断行点 nitpick（内容完整非截断·标点优先断行器候选=字幕 _prefer_punct_break 同型·字幕轨本体逐字完整）③b7 H1/H2 与 reviewsdoc 密集台账背景叠印=系列同构设计（bs012/013/014 b7 同位带·H1/H2 暗色垫底在位） | "
    "空气预算 v4 62.42s→v5 59.54s（-11 字+停顿扫三处·余量 0.46s<1.2s 线=R185 判例再裁）→**v6 微裁四处定稿 58.51s（余量 1.49s·fleet 带内）**〔b4 逗号并句+b6 顿号+b9 照档案推算→是推算〔-2 字〕+b10 逗号并句·卡片锚点列零动·题眼句/三视角独占切面/播报员切面/事实数字/推演声明标签句/自指句/cta 全保·M1 v5 b8 长句 WARN 顿号列表机械拆复扫 0/0+M1 v6 0F0W·v5=59.54s 实测态留档+v6 beats 留档〕·plan.json 入 git·mp4 gitignored·**收官腿=R1690 领**（E8 终审〔ASR 终轨 R169 QC recipe+E4 参考仪〕→M4→F-163 登记）·tmp 批闭收账随本轮 commit·发布锁=M5 账号物理件未开·未上线=未测量 |\n")
with io.open("output/renders/README.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(RR_ROW)

# 2) station-reviews row
SR_ROW = ("| 2026-10-08 | **渲染腿毕（BS-015《板块十年·台风夜之后》·R1689·backlog #104·「板块十年」系列第四件·形态 C 台风梅花三视角·R1688 S1 过门+空气预算四程之后腿）** | "
    "voiceover-v5/v6.beats.txt+cards-v1-matched.json+bs-015-v1-shipinhao-60s.mp4.plan.json+probe-r1689/+frameverify-r1689/（探针与帧验证据件） | "
    "空气预算收敛两程=v5 59.54s（-11 字+停顿扫·余量 0.46s<1.2s 线 R185 判例再裁）→v6 微裁四处（b4 逗号并句/b6 顿号/b9 照档案推算→是推算 -2 字/b10 逗号并句）=**58.51s 定稿 1.49s 余量 fleet 带内**·M1 v5 b8 长句 1 WARN 顿号列表机械拆复扫 0/0+M1 v6 0F0W·卡片锚点列零动·题眼句/三视角独占切面（风留下的补丁不许修/联络断了/口信一家一家送到/第二天早饭是七家的）/播报员切面/事实数字（三个视角/七家/三年/十年）/推演声明标签句/自指句/cta 全保——"
    "素材探针=census-card-v18/v19/v20 三时点多模态核验（13s 全静态·零录穿·零隐私·[AIGC] 标识在源卡）+**全分辨率二验定谳** v18=C-00027 邓建国感知塔站值守员/v19=C-00028 十四号路灯/v20=C-00029 咪喱=BigLife census/anchors 正典锚一致〔**tile 3x3 低清首读名称互换误判=c18 读作咪喱猫/c20 读作人名=读数手段问题如实注记·R189/R1680 tile 失读族第三例·卡面身份认定必须全分辨率单帧**〕——"
    "对位表 11/12=0.92（citywatch×1/looplog×2/census-v19×1/census-v18×2 同源多用/census-v20×1/editgrid×2/reviewsdoc×2/cards-only×1=**三视角拆条混剪形态 C 拆条面第二证**·R1685 v13 单卡首证→三卡直接证据面）——"
    "S2 三门循环独立执法全绿=ai_feel 0F0W（gaps 11 处 0.220-0.558s varied/pacing CV 0.233/prosody 9 档/copy CV 0.253）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 0.92+share 1.00 无连排+variety+timeline 代数过）+spec 微信视频号双 PASS（9:16+58.51s ∈30-60s 窗 1.5s 余量）——"
    "帧验三律全过=拍头 12/12 语义全中（H1/H2 逐拍对位+sys.beat 01→12+badge+AIGC 全帧可读）+回环 b0 三帧零录穿（4.400s 穿越点 pre/x/post 全净=R188/R197 净源链继承）+全分辨率三帧复核（b2 C-00028 逐字正/b7 拍中角标+字幕逐字齐/b11 字幕逐字一致·无截断无乱码零隐私）——"
    "**nitpick 三注（诚实律·E8 评审面输入）**：①b2 双层 AIGC 标注=源卡自带+成片常驻合规冗余②b11 H2「台/风夜」跨行断行点（内容完整非截断·断行器候选）③b7 大字与台账背景叠印=系列同构设计（H1/H2 垫底在位）——"
    "**操作红两笔如实入账**：①ffmpeg 输出文件名 PS 反引号 `t=tab 两踩（探针帧名两次失败→下划线命名修复）②tile 低清多模态首读卡名误判（全分辨率二验定谳=手段问题律第三例） |\n")
with io.open("docs/reviews/station-reviews.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(SR_ROW)

# 3) bs015 README render-leg section
RM = ("## 渲染腿（R1689·实活轮·产品优先律 2 分位实物=bs-015 成片在链）\n\n"
    "- **空气预算收敛两程**：v5 59.54s（-11 字+停顿扫三处：b3 第二天灯带→灯带/b6 时间轴往前推→时间轴推/b10 十年后台风夜→十年后/b11 评论区说说，你经历过的台风夜→评论区说说你的台风夜+b2 补丁，不许修并句+b8 。→：并句·卡片锚点列零动）——余量 0.46s<1.2s 线=R185 判例再裁→**v6 微裁四处定稿=58.51s（1.49s 余量·fleet 带内）**〔b4 播报员说，比编号好记→播报员说比编号好记/b6 三年，十年→三年、十年（顿号）/b9 挺多久照档案推算→挺多久是推算（-2 字·b7 标签句已含档案锚=L18 释义位承接）/b10 十年后，档案接着记→十年后档案接着记〕·M1 v5 b8 长句 1 WARN（14 字/3 逗）顿号列表机械拆复扫 0/0+M1 v6 0 FAIL 0 WARN·v5（59.54s 实测态）+v6 beats 全留档·S1 判词对 v1 机械裁不回炉=R1678 先例。\n"
    "- **素材探针（三视角拆条源核验）**：census-card-v18/v19/v20-vertical 各 13s 三时点（1.3/6.5/11.7s）多模态核验=全静态·零录穿·零隐私（聊天窗/持仓/密钥全无·[AIGC] 标识在源卡）·**全分辨率二验定谳**：v18=C-00027 邓建国（碳基市民·感知塔站值守员·信条「台风天的日志最见人品」=lc007 close 信条位已消费避让注记在案）/v19=C-00028 十四号路灯（nightlamp·全城唯一在台风夜把自己亮度开满格的灯灵=钩子字段 verbatim 源）/v20=C-00029 咪喱（像素灵·radiocat·全城唯一拥有「巷志」的猫）——与 BigLife census/anchors 正典锚（C-00027 邓建国/C-00028 十四号路灯/C-00029 咪喱）三方一致·**tile 3x3 低清首读名称互换误判（c18 读作咪喱猫/c20 读作人名）=读数手段问题如实注记**（R189/R1680 tile 失读族第三例·卡面身份认定必须全分辨率单帧）。\n"
    "- **对位表 cards-v1-matched.json 11/12=0.92**：citywatch×1〔b0 观城台〕+looplog×2〔b1 系统回事件档案=日志字面/b9 真话在册〕+census-v19×1〔b2 灯视角直接证据〕+census-v18×2〔b3 塔视角/b4 塔起名 wink=同源多用注记·C-00027 钩子字段尾段「播报员说比编号好记」verbatim 源卡〕+census-v20×1〔b5 猫视角直接证据〕+editgrid×2〔b6 时间轴压条=形态 C 制式位/b10 AI 剪辑自指〕+reviewsdoc×2〔b7 推演声明档案载体/b8 三样在册对账〕+cards-only×1〔b11 CTA〕——**三视角拆条混剪=形态 C 拆条面第二证**（R1685 bs014 v13 单卡首证→本件三卡直接证据面）·素材探针=在案证据复用（looplog/reviewsdoc/editgrid=R808 probe-r808+citywatch=R188/R197 净窗链）。\n"
    "- **R-E shipinhao 渲染**：bs-015-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·9:16 1080×1920·58.51s spec 实测=音轨分毫一致·hits=[0]·角标 BigStream|BS-015 EP.15+§4.5 三开关·plan.json 入 git）。\n"
    "- **S2 三门循环独立执法全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.558s varied/pacing CV 0.233/prosody 9 档/copy CV 0.253）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 0.92+transition-share 1.00 无连排+variety+timeline 代数过）+spec 微信视频号双 PASS（9:16+58.51s ∈30-60s 窗 1.5s 余量）。\n"
    "- **帧验三律全过**：拍头 12/12 语义全中（H1/H2 逐拍对位+sys.beat 01→12 连续+badge 全帧在+AIGC 全帧可读）+回环边界 b0 三帧零录穿（4.400s 穿越点 pre/x/post 全净=R188/R197 净源链继承实证）+全分辨率三帧复核（b2 拆条卡 C-00028 逐字正+「补丁」无错字/b7 拍中角标 sys.beat=08+字幕逐字齐「先亮底：往后是推演，基于硅基城市真实档案的十年推演。」/b11 字幕逐字一致「下集：第一块砖。评论区说说你的台风夜。」·AIGC 括号串净读·无截断无乱码零隐私）。**nitpick 三注（诚实律·E8 评审面输入）**：①b2 双层 AIGC 标注=拆条源卡自带 AIGC 行+成片常驻标识合规冗余非缺陷②b11 H2「台/风夜」跨行断行点（内容完整非截断·标点优先断行器候选）③b7 H1/H2 与 reviewsdoc 密集台账背景叠印=系列同构设计（bs012/013/014 b7 同位带·H1/H2 暗色垫底在位）。\n"
    "- **操作红两笔如实入账**：①ffmpeg 输出文件名 PS 反引号 `t=tab 两踩（探针帧命名两次失败→下划线命名修复）②tile 低清多模态首读卡名互换误判（全分辨率二验+正典锚三方定谳）。\n"
    "- **余链（R1690 收官腿领）**：E8 终审〔ASR 终轨 R169 QC recipe+E4 参考仪随行〕→M4→F-163 登记（REACT-v12 顺延 F-164 判例如常）。\n")
with io.open("data/sources/bs015/README.md", "a", encoding="utf-8", newline="\n") as f:
    f.write("\n" + RM)

# 4) backlog #104 note
BL = "src/os/backlog.md"
bl = read(BL)
anchor = "→E8（ASR+E4）→M4→F-163 登记（下轮领）"
assert bl.count(anchor) >= 1, "anchor not found"
note = ("   **[R1689 进展 2026-10-08]**：渲染腿毕=空气预算收敛两程（v5 59.54s 余量 0.46s<1.2s 线 R185 判例再裁→v6 微裁四处=**58.51s 定稿 1.49s 余量 fleet 带内**·M1 v5 1 WARN 顿号机械拆复扫 0/0+M1 v6 0F0W·卡片锚点列零动·v5/v6 beats 留档）+素材探针（census-v18/v19/v20 三时点多模态核验全静态零录穿零隐私·**全分辨率二验定谳 v18=C-00027 邓建国/v19=C-00028 十四号路灯/v20=C-00029 咪喱=正典锚一致**·tile 低清首读名称互换误判=读数手段问题如实注记）+对位表 cards-v1-matched 11/12=0.92（**三视角拆条混剪=形态 C 拆条面第二证**·v18×2 同源多用+v19×1+v20×1 三卡直接证据面）+R-E 渲染 bs-015-v1-shipinhao-60s.mp4（58.51s·12 段 11 柔 0 硬切·角标 BS-015 EP.15+§4.5 三开关·plan.json 入 git）+S2 三门全绿（ai_feel 0F0W+层 1.8 六面 PASS visual-ratio 0.92+spec 微信视频号双 PASS 1.5s 余量）+帧验三律全过（拍头 12/12 语义全中+回环 b0 三帧零录穿+全分辨率三帧复核 AIGC 可读零截断·nitpick 三注如实：b2 双层 AIGC 合规冗余/b11 台/风夜断行点/b7 背景叠印系列同构）——余腿=E8 终审〔ASR 终轨 R169 QC recipe+E4 参考仪〕→M4→F-163 登记（下轮领）\n")
i = bl.find(anchor) + len(anchor)
bl = bl[:i] + "\n" + note.rstrip("\n") + bl[i:]
write(BL, bl)

# 5) state.json
p = "src/os/state.json"
st = json.loads(read(p))
st["tick"] = 1689
st["focus"] = ("R1689 生产轮·#104 BS-015《台风夜之后》渲染腿毕（R1688 S1 过门+空气预算四程之后腿·实活轮·产品优先律 2 分位实物=bs-015 成片在链）："
    "空气预算 v5 59.54s（余量 0.46s<1.2s 线再裁）→v6 微裁四处 58.51s 定稿（1.49s 余量·M1 0F0W·卡片锚点列零动）"
    "+素材探针 census-v18/v19/v20 三时点全静态零录穿零隐私（全分辨率二验=正典锚一致·tile 低清首读误判如实注记）"
    "+对位表 11/12=0.92（三视角拆条混剪=形态 C 拆条面第二证）+R-E 渲染 bs-015 成片（12 段 11 柔 0 硬切·S2 三门全绿·帧验三律全过·nitpick 三注如实）。"
    "next=R1690 收官腿：E8 终审（ASR 终轨 R169 QC recipe+E4 参考仪）→M4→F-163 登记（+OSS w5 21:40 当窗+DAILY v69 literal 日窗 05:52+）。")
log_line = ("2026-10-08 " + ts[11:16] + " R1689: 生产轮·#104 BS-015《台风夜之后》渲染腿毕（R1688 起链+S1 过门续做·实活轮·产品优先律 2 分位实物=bs-015-v1-shipinhao-60s.mp4 在链）——"
    "①轮首五查静（origin_gap_check QUIET fetch 实通 ahead=0 behind=0·own orders 顶 O-20261006-1410-HQ-C mtime==锚·decisions/ledger mtime 00:09:50==R1677 已消费锚·dnum 内容寻址差集 TRULY_NEW=[] 水位 168 承继·ledger @BigStream 2 行==L91/L92 值守锚零新转办·集团 orders 15:13:06==锚·树净零锁·daily1008 在案不重跑·GB v1.3 R1683 刚刷下窗 10-15·W42 周审窗 10-12 未到）+三探针绿（board 0 FAIL 5 题 10 稿/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 2F+153W 皆在案史实·两 FAIL=09-26/09-28 outage 不重触发·drift +14=adjudicated 基线内）→backlog 顶行 #104 在链可领活照走；"
    "②空气预算收敛两程=v5 59.54s（-11 字+停顿扫三处：b3 第二天/b6 往/b10 台风夜/b11 经历过的+并句二·卡片锚点列零动·M1 b8 长句 1 WARN 顿号列表机械拆复扫 0/0）——余量 0.46s<1.2s 线=R185 判例再裁→v6 微裁四处（b4 逗号并句/b6 顿号/b9 照档案推算→是推算 -2 字/b10 逗号并句）=**58.51s 定稿 1.49s 余量 fleet 带内**·M1 v6 0F0W·题眼句/三视角独占切面/播报员切面/事实数字/推演声明标签句/自指句/cta 全保·v5 59.54s 实测态+v6 beats 全留档；"
    "③素材探针=census-card-v18/v19/v20-vertical 各 13s 三时点多模态核验（全静态·零录穿·零隐私·[AIGC] 源卡在位）+**全分辨率二验定谳** v18=C-00027 邓建国感知塔站值守员/v19=C-00028 十四号路灯/v20=C-00029 咪喱=BigLife census/anchors 正典锚三方一致——**tile 3x3 低清首读名称互换误判（c18 读作咪喱猫/c20 读作人名）=读数手段问题如实注记·R189/R1680 tile 失读族第三例·卡面身份认定必须全分辨率单帧**；"
    "④对位表 cards-v1-matched.json 11/12=0.92（citywatch×1+looplog×2+census-v19×1+census-v18×2 同源多用+census-v20×1+editgrid×2+reviewsdoc×2+cards-only×1=**三视角拆条混剪形态 C 拆条面第二证**·R1685 v13 单卡首证→本件三卡直接证据面·素材探针在案证据复用 R808/R188/R197）；"
    "⑤R-E shipinhao 渲染 bs-015-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·9:16 1080×1920·58.51s spec 实测=音轨分毫一致·hits=[0]·角标 BigStream|BS-015 EP.15+§4.5 三开关·plan.json 入 git）；"
    "⑥S2 三门循环独立执法全绿=ai_feel 0F0W（gaps 11 处 0.220-0.558s varied/pacing CV 0.233/prosody 9 档/copy CV 0.253）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 0.92+transition-share 1.00 无连排+variety+timeline 代数过）+spec 微信视频号双 PASS（9:16+58.51s ∈30-60s 窗 1.5s 余量）；"
    "⑦帧验三律全过=拍头 12/12 语义全中（H1/H2 逐拍对位+sys.beat 01→12 连续+badge 全帧在+AIGC 全帧可读）+回环边界 b0 三帧零录穿（4.400s 穿越点 pre/x/post 全净=R188/R197 净源链继承实证）+全分辨率三帧复核（b2 拆条卡 C-00028 逐字正+「补丁」无错字/b7 拍中角标+字幕逐字齐/b11 字幕逐字一致·AIGC 括号串净读·无截断无乱码零隐私）——**nitpick 三注（诚实律·E8 评审面输入）**：①b2 双层 AIGC 标注=源卡自带+成片常驻合规冗余②b11 H2「台/风夜」跨行断行点（内容完整非截断·断行器候选）③b7 大字与台账背景叠印=系列同构设计（H1/H2 垫底在位）；"
    "⑧台账=renders README bs-015 行（在链标注·render-unannot 预期红=F-163 登记即清）+station-reviews R1689 行+bs015 README 渲染腿节+backlog #104 R1689 注+state/export 刷；"
    "⑨操作红两笔如实入账=①ffmpeg 输出文件名 PS 反引号 `t=tab 两踩（探针帧名两次失败→下划线修复·R173 PS 坑同族）②tile 低清多模态首读卡名互换误判（全分辨率二验+正典锚三方定谳）；"
    "例行件=daily1008 在案不重跑（一份为真相）·GB v1.3 下窗 10-15·OSS w5=10-08 21:40 时间闸未到·DAILY v69 复市件=literal 日窗 05:52+ 夜窗不产（R1321 日窗硬闸先例）·W42 周审窗 10-12 未到·HQ-FEEDBACK 不写（无集团层新 open 问题·零膨胀）·tokens:local=0（本轮全纯脚本+会话内建多模态验图零本地模型调用·P-54⑤ 计量律如实记）；"
    "下轮=R1690 BS-015 收官腿（E8 终审〔ASR 终轨 R169 QC recipe+E4 参考仪〕→M4→F-163 登记）+时间闸件照窗（OSS w5 21:40/DAILY v69 05:52+）。收账显式列文件 commit+push。")
st["log"].append(log_line)
st["ts"] = ts
st["task"] = log_line.split("R1689: ", 1)[1][:60]
write(p, json.dumps(st, ensure_ascii=False, indent=2) + "\n")

# 6) status-export.json
p = "docs/status-export.json"
ex = json.loads(read(p))
ex["export_ts"] = ts
ex["live"] = [
    "当前活：2026-10-08 " + ts[11:16] + " R1689 生产轮·#104 BS-015《台风夜之后》渲染腿毕——空气预算 v6 58.51s 定稿+三视角拆条对位 0.92+R-E 渲染成片在链+S2 三门全绿+帧验三律全过",
    "最近实物：bs-015-v1-shipinhao-60s.mp4（58.51s·「板块十年」系列第四件·形态 C 三视角拆条混剪）+cards-v1-matched.json+probe/frameverify 证据件·2026-10-08 " + ts,
    "下个里程碑：BS-015 收官腿 E8 终审（ASR+E4）→M4→F-163 登记（窗 ≤10-08 12:00）+OSS w5 切片 21:40 当窗+DAILY v69 literal 日窗 05:52+·GB 下窗 10-15",
]
write(p, json.dumps(ex, ensure_ascii=False, indent=2) + "\n")

print("R1689 close done:", ts)
