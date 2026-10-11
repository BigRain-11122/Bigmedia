# -*- coding: utf-8 -*-
# R1953 close: state tick/focus/log/ts/task + queue notes (main#4, tech#92)
import json
import datetime
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AB_RESULT = os.path.join(ROOT, ".c3-tmp", "r1953_score_ab_result.json")

# A/B result absorption (R176->R177 async precedent; file written by r1953_score_ab.py)
ab_note = "A/B 探针两障如实记（首跑 judge stdin str→bytes 型错=脚本 bug 已修 text 编码；14b-8k 当前 VRAM 态 85% CPU offload=单调用分钟级超窗风险→探针 re-gate 真 GPU 窗发射〔fire-window-card 守卫〕·判据面=明日 08:00 生产窗实测 zhihu-hot 头部 ≥3 件 ≥60·FAIL=阈值分层腿递补）"
ab_done = False
if os.path.exists(AB_RESULT):
    try:
        r = json.load(open(AB_RESULT, encoding="utf-8"))
        ab_done = True
        ab_note = "A/B 探针落地（qwen2.5:14b-8k 头部5 候选版重打分·base=DB 59/58/54/54/53·读数=%s·ge60=%d/5·verdict=%s）" % (
            "/".join(str(x.get("cand")) for x in r.get("results", [])),
            r.get("ge60", 0), r.get("verdict", "?"))
    except Exception:
        pass

log_line = (
    "2026-10-11 08:3x R1953: 实活轮·fire GO 即发三修一过=MD-0002 剧本腿 VALIDATION PASS 交付"
    "（08:13:57 GO path=A-hot-resident→08:14:08 即发 11s 消费=R1952 turnkey 教训生效；"
    "attempt1/2 同缺陷=declared 75≠sum 90/89+锚缺开档→prompt 根修三处〔五锚必现清单+total_seconds=sum 纪律+13×6 定分 78〕→"
    "attempt4 13 镜 78s 0 invalid 五锚全中 PASS；shot3「两万零三」事实漂移外科修=archive 一万零三 shot5 已 verbatim·shot3 改「数字洪流里每一个名字被点亮」；"
    "三件落盘=script-content-v1.json+raw+validate 报告·v1 生成缺陷族沉淀=9b think:false 不做算术只仿示例值→定分策略根治）"
    "+tech#92 文本腿落地（selection-score-city.md 增「全城量级锚例」节=四锚例精算 A84/B84/C76/D74 对表实测头部类〔医疗政策/科技产品/食品安全/文化讨论〕"
    "+55-59=中带刻度语义+防膨胀护栏=锚例仅限全城量级）+"
    + ab_note +
    "+fetch_runs 180min 节流轻读复核 PASS（08:04/08:05 后 tech/knowledge 零新跑=15min 节奏已断·08:11 popular 独立节奏=worker 活）"
    "+meme V1 查看位零新到件（15:41:53 锚维持）+explore#24 刀④ 未领承继下轮"
    "——轮首五查静=own orders 12:08:14==R1733 锚+origin_gap QUIET ahead0 behind0+树态=MV sprint 会话域在飞件零接触 R1745 承继；"
    "三探针=board 0 FAIL〔5 题 10 稿·5 in production〕/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17〕0 发现〔78 renders unannot=0〕"
    "/loop_health 2F+240W 皆在案史实（两 outage 已裁定不重触发·drift 17==基线带内）；"
    "例行件=日报在案不重跑+W42 周审 10-12 未到+GB §④ v1.3 下期 10-15 跳过+export 刷新（export_refresh 正典写入器）"
    "+HQ-FEEDBACK 零集团层新 open 不写+tokens:local=本地 ollama 生成飞行如实记（MD-0002 qwen3.5:9b-16k×4 调用+AB 探针 qwen2.5:14b-8k×5——零 API token·P-54⑤）；"
    "队列补货=main#4+tech#92 两既有行注记回写非新增（真无独立新种子·禁凑数律）。"
    "下轮=R1954 tech#92 判据面=08:00 生产窗读数〔锚例版已上线·zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〕+A/B 探针 GPU 窗发射位+MD-0002 下一腿（T2I/配音线）+explore#24 刀④+meme V1 查看位。"
)

focus = (
    "R1954 tech#92 判据面=08:00 生产窗读数（锚例版 selection-score 已上线·zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补）+A/B 探针 GPU 窗发射位（r1953_score_ab.py 已修型错·14b-8k 需真 GPU 窗）+MD-0002 下一腿（T2I/视觉线·剧本件已 PASS）+explore#24 刀④ 承继+meme V1 查看位随轮"
)

sp = os.path.join(ROOT, "src", "os", "state.json")
d = json.load(open(sp, encoding="utf-8"))
d["tick"] = 1953
d["focus"] = focus
d["log"].append(log_line)
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
d["ts"] = now
d["task"] = log_line.split("R1953: ", 1)[1][:60]
json.dump(d, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("state.json: tick=1953 ts=%s task=%.60s" % (now, d["task"]))

# main.md #4 note
mp = os.path.join(ROOT, "state", "queue", "main.md")
t = open(mp, encoding="utf-8").read()
anchor = "——12:00 窗 fire=nvidia-smi 守卫→一条命令（窗内零材料耗时）——下轮领剧本腿（GPU 窗）"
assert anchor in t, "main#4 anchor not found"
t = t.replace(anchor, anchor + (
    "——**[R1953 剧本腿交付 2026-10-11]**：fire GO 即发（08:14:08·11s 消费）→attempt1/2 同缺陷 FAIL（declared 75≠sum）"
    "→prompt 根修（五锚必现+13×6=78 定分）→attempt4 VALIDATION PASS（13 镜 78s·0 invalid·五锚全中）→shot3 事实漂移外科修→"
    "script-content/raw/validate 三件落盘·A/B 探针在飞·余链=T2I→配音→装配→S2+E8→M4→F 登记"))
open(mp, "w", encoding="utf-8").write(t)
print("main.md #4 noted")

# tech.md #92 note
tp = os.path.join(ROOT, "state", "queue", "tech.md")
t = open(tp, encoding="utf-8").read()
anchor = "——gated ollama 生成窗（A/B 探针需真生成）——按认领制随轮领做"
assert anchor in t, "tech#92 anchor not found"
t = t.replace(anchor, anchor + (
    "——**[R1953 文本腿落地]**：锚例注入保守序第一档执行=selection-score-city.md 增「全城量级锚例」节"
    "（四锚例 A84/B84/C76/D74 精算+55-59 中带语义+防膨胀护栏·对表实测头部类）" +
    ("；A/B 探针已落地：" + ab_note if ab_done else "；A/B 探针两障如实记（首跑 stdin 型错已修+14b-8k 当前 VRAM 态 85% CPU offload=分钟级/调用）→re-gate 真 GPU 窗发射·判据面=明日 08:00 生产窗实测（zhihu-hot 头部 ≥3 件 ≥60）·FAIL=阈值分层腿递补")))
open(tp, "w", encoding="utf-8").write(t)
print("tech.md #92 noted; ab_done=", ab_done)
