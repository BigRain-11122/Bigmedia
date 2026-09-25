# -*- coding: utf-8 -*-
# R249 close: state.json (tick 249, focus, log, ts+task heartbeat face) +
# status-export.json (export_ts + derived rows per P-61).
import datetime
import json
import os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")

log_line = (
    "2026-09-25 %s R249: 生产轮·BS-005 素材窗解锁实录批第一腿（实活轮·五查四静一异动转全任务书）——"
    "①轮首快速路径五查：orders 顶=O-20260925-1153-BG-C 无新令·ledger 严格行含 @ 四模式 15 行=锚零新转办·"
    "decisions UTF8 非空行 29（总 32）=锚零新行·backlog 顶行 #28 done/#27 ①②③ 毕不可认领·树态=并窗自记账预期态·"
    "**素材窗迹象核=Biggame 总控窗现于枚举（历轮 15+ 零→现 1·R193 呈报前置成立）**→实活轮；"
    "②三探针全绿=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面+2 发现=bs-005/bs005e blocked 在链预期红/loop_health 0 FAIL 17 WARN 在案史实（state-ts 门第八轮零红零滞后）；"
    "③实录批第一腿交付：单帧探针→**窗归属定谳=「Biggame·小游戏公司总控」像素游戏客户端窗**（满画面=像素街景+HUD 状态条〔行动 8 项/待审 4 款/¥0/今日 252 笔〕+集团驾驶舱弹窗〔三子公司汇报·27款小游戏·3/3机并网·决策卡四款·今日 252 笔〕）"
    "≠Edge「硅基生命元宇宙」仪表盘窗（两窗并列·首探针帧误捕上层 Edge=SetForegroundWindow 前台锁实证→前台校验通道加固 foreground==target）→"
    "40s 首录=加载空画布定谳（窗 13:2x 新开场景未渲染完·t20 黑屏帧）→满载后重录 40s=**验图全净**（t5/t35 双帧拼图：HUD/弹窗文字两帧逐字一致·街景 idle 动画=活素材·脱敏四项全无〔密钥/聊天/财务/隐私〕·零录穿）→"
    "biggame-console-raw.mp4 落位（1366×1078·15fps·40s·1.9MB·mp4 gitignored·取证 raw 留档）；gdigrab 两坑在案（负 offset rc=-5 桌面钳位修/最大化窗 SW_RESTORE 复原态定位）；"
    "④素材面新发现：Edge 仪表盘（gaming/MiniGame/硅基生命元宇宙.html 跨仓只读引用）=集团 meta 仪表盘·当前优先级 P0-P5（**P5 服务器端本地测好再买=b4 候选直接证据**）+顶层设计（集团的宪法面）panel below fold（=b9 候选）+令与结果+六家公司+机器和算力 sections=实录第二腿对象（未录）；"
    "⑤诚实定谳：BS-005 visual-ratio 结构性上限复核——总控窗+仪表盘全核**无 软著账本/12条约束/玩法机制面板**（待审 4 款≠8 款软著·27 款小游戏≠8 款软著·「10分钟内消受入册」≠10 分钟快照=数字错位避用律维持）·全解锁上限 5/12≈0.42<0.80 门线→**R192 结构性判断被窗内实况证实：重渲必仍 FAIL**→BS-005 路线待下轮自决（拍稿证据友好化改造=S1 重走 vs 升裁处置）·对位表重构/重渲不烧（预算律）；"
    "⑥例行件：日报 2026-09-25+W39 周审在案不重跑·global-benchmarks day1 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·HQ-FEEDBACK 不写（无集团层新 open 问题·零膨胀）·tokens:local=0（纯脚本+验图零本地模型调用·P-54⑤ 计量律如实记）。"
    "下轮=R250 实录第二腿（Edge 仪表盘 b4/b9 证据面+全源三时点扫描）→对位表重构+BS-005 路线自决（委托决策令面·log 留痕）。收账显式列文件 commit+push。"
) % now.strftime("%H:%M")

task_face = log_line.split("R249: ", 1)[1][:60]

sp = os.path.join(ROOT, "src", "os", "state.json")
with open(sp, encoding="utf-8") as f:
    st = json.load(f)
st["tick"] = 249
st["focus"] = (
    "R250: 实录批第二腿（Edge 仪表盘窗 b4〔P5 服务器端〕/b9〔宪法面 panel〕证据面录制·前台校验通道+全时点扫描防录穿）"
    "→对位表重构（b4/b9 解锁判断·数字错位避用律）→**BS-005 路线自决（委托决策令面·log 留痕）**：visual-ratio 上限 5/12≈0.42<0.80 结构性证实（R192 判断被 R249 窗内实况复核）——"
    "路线A=拍稿证据友好化改造（S1 v1.5 重走·拍面改可对位）vs 路线B=升裁处置（dept-review §5 弃件/降级候选）；bs005e 共享解锁面同裁决；"
    "锚：ledger @15/decisions 29（总 32）/orders 尾 O-20260925-1153-BG-C/总控窗在开=录制优先；readiness 预期=3 blocker+2 finding 同集"
)
st["log"].append(log_line)
st["ts"] = ts
st["task"] = task_face
with open(sp, "w", encoding="utf-8") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
    f.write("\n")

ep = os.path.join(ROOT, "docs", "status-export.json")
with open(ep, encoding="utf-8") as f:
    ex = json.load(f)
ex["export_ts"] = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
for d in ex["depts"]:
    if d["n"] == "工程技术部":
        d["t"] = (
            "OS 循环 R249（实活轮：**Biggame 总控窗 13:2x 开窗=BS-005 素材窗解锁**——实录批第一腿 40s 满画面验图全净"
            "〔脱敏四项全无·零录穿·t5/t35 双帧稳定〕+窗归属定谳〔总控窗=像素游戏客户端≠Edge 硅基生命元宇宙仪表盘=两窗并列〕"
            "+Edge 仪表盘 b4/b9 候选证据面发现（P5 服务器端/宪法面 panel）·BS-005 visual-ratio 上限 5/12<0.80 结构性证实→路线自决下轮〕"
            "·ledger @15/decisions 29（总 32）双锚·orders 顶 O-1153 维持·state.ts/task 心跳面第八轮刷新零红·素材窗在开=录制优先"
        )
for o in ex["outs"]:
    if o[0] == "OS 循环":
        o[2] = (
            "tick 249·R249（实活轮：Biggame 总控窗开窗解锁=实录批第一腿 40s 验图全净落位 biggame-console-raw·"
            "Edge 仪表盘第二腿待录〔b4 P5 服务器端/b9 宪法面〕·BS-005 visual-ratio 上限 0.42<0.80 结构性证实→路线自决=拍稿改造 vs 升裁）"
        )
    if o[0] == "量产产线":
        o[2] = (
            "production open（D-BS-06）·短产线六件在库收官+F-008~F-012 有声五件（成品库十一件）·"
            "**BS-005/bs005e 素材窗已开（R249 总控窗实录第一腿毕·第二腿+路线自决下轮）**；新线=硅基城市三线"
            "（网文连载至 ch.5·有声五件成品=新连载节律运转中·漫画 ep.1/ep.2 产线定栈）"
        )
for r in ex["results"]:
    if r[1] == "OS 轮次":
        r[0] = "249"
with open(ep, "w", encoding="utf-8") as f:
    json.dump(ex, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("closed tick=249 ts=%s" % ts)
