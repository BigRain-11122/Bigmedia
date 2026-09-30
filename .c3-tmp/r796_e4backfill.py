# -*- coding: utf-8 -*-
"""R796 E4 same-round backfill (landed 00:29:59, hot-load): review v1.1 + verdict archive
+ expert-calls row + F-077/cards/station/export sync + state addendum."""
import io, json, time

TS = "2026-10-01 00:29:59"
VERDICT_PATH = "docs/revexp_placeholder"

# 1) clean verdict archive
res = json.load(io.open("data/storylines/cards/MC-20261001-REACT-v7-tmp/e4-result.json", encoding="utf-8"))
verdict = res["verdict"]
arc = "docs/reviews/expert-verdicts/20261001-002959-E4-audience.md"
with io.open(arc, "w", encoding="utf-8") as f:
    f.write("# E4 参考仪·受众盲评净本（MC-20260930-REACT-v7 系谱=MC-20261001-REACT-v7《城市速报 007·衬衫的价格为 9 镑 15 便士》）\n\n"
            "- 起飞 2026-10-01 00:29:5x（Start-Process 脱壳·绝对路径启动器 R728 律）→ 落判 %s（热载快落·qwen2.5:14b·1500s 窗内）\n"
            "- 材料=静态热点反应卡（cards.json+渲染件·盲评面）\n\n## 判词（净本·ANSI/盲文轮转符已清洗）\n\n%s\n" % (TS, verdict))

# 2) review file v1.1
rv = io.open("docs/reviews/review-20261001-mcreact-v7.md", encoding="utf-8").read()
old_e4 = rv[rv.find("## E4 参考仪"):rv.find("## 未测面")]
new_e4 = """## E4 参考仪（**同轮回填毕 00:29:59·热载快落·非拦截·dept-review §6 双态制**）

- **读数 8.0**（起飞 00:29:5x→00:29:59 落判=热载快落档·R716 11s 同型）：**会停下来看明说+会保存甚至转发给朋友明说=三意愿正面**（「分享这样的内容不仅可以传播信息，还能引发关于记忆、怀旧和城市生活等话题的讨论」=分享对象与话题具明）——**REACT 带内高点回归**（v1 7.0/v2 8.0/v3 7.0/v4 7.0/v5 7.0/v6 7.0→**v7 8.0=带内高点第二件**〔v2 市场直配件同位〕·「内容和形式上都有较高的创新性和吸引力」正面定性）
- **正面读数**：「结合了当前的热点事件和创意的城市速报形式，给人一种新鲜感」+「不仅包含了实际的社会热点，还融入了虚构城市的情感和思想，这种独特的视角」=体裁混搭面正面定性七连证+**记忆/怀旧话题讨论价值明说**（本件主题域=集体记忆=E4 话题价值直接确认位）
- **旗①（扣 2）=信条「城市不会忘记，除非我们偷懒。」过于抽象·未与热点事件建立明显联系**：卡面文字旗（信条字段 verbatim 不可改写·**MC-003 语境门槛族信条位变体第二连**〔v6 同位同型〕——E4 盲评面未接通「满分作文=城市没有偷懒的证词」编辑论证链=语境门槛非句式套路〔P-1 判据①口径维持：句式套路化旗零再现第三连〕·吸收位=M5 图文页语境层）+副旗=标题与内容关联性（反应行情感表达 vs 新闻直解=E4 盲评面对轴位映射律的常规张力=v1-v6 副旗族同型·吸收位=M5+系列语境）
- **最弱**：标题与内容之间的一致性（=副旗同位·双旗轮如实记）
- 判定：非拦截·七席 ≥9 PASS 维持（F-077 登记态不动）·净本 `expert-verdicts/20261001-002959-E4-audience.md`

"""
rv = rv.replace(old_e4, new_e4)
rv = rv.replace("- E4 参考仪在飞（本件如实列·下轮回填销项）",
                "- ~~E4 参考仪在飞~~（**本件销项**=同轮回填毕 8.0·00:29:59 落判热载快落）")
rv += "\n- 2026-10-01: v1.1 **E4 同轮回填 8.0**（00:29:59 热载快落·三意愿正面明说=REACT 带内高点回归〔v2 同位第二件〕·旗①=信条语境门槛族变体第二连〔v6 同型·非句式套路旗=P-1 判据①口径第三连〕+副旗=标题-内容关联性〔盲评面对轴位映射律常规张力〕·最弱=一致性〔双旗轮〕·净本 expert-verdicts/20261001-002959-E4-audience.md+expert-calls 00:29 行·非拦截·七席 ≥9 PASS 维持）。\n"
io.open("docs/reviews/review-20261001-mcreact-v7.md", "w", encoding="utf-8").write(rv)

# 3) expert-calls row
ec = io.open("docs/reviews/expert-calls.md", encoding="utf-8").read()
assert "20261001-002959" not in ec
ec += "\n| 2026-10-01 00:29 | E4-audience | MC-20261001-REACT-v7 静态热点反应卡（盲评面=e4_call.py tmp wrapper·qwen2.5:14b·热载快落） | 8.0（三意愿正面·REACT 带内高点回归·旗①=信条语境门槛族变体第二连） | expert-verdicts/20261001-002959-E4-audience.md | 采纳（参考线·非拦截） |\n"
io.open("docs/reviews/expert-calls.md", "w", encoding="utf-8").write(ec)

# 4) finished.md F-077 E4 sentence sync
fin = io.open("output/finished.md", encoding="utf-8").read()
old = "；**E4 参考仪异步在飞**（Start-Process 脱壳 1500s 窗·e4-result.json 轮间落地·下轮回填追加制·非拦截=dept-review §6 双态制）；发布锁"
new = "；**E4 参考仪同轮回填毕 8.0**（00:29:59 落判热载快落=Start-Process 脱壳脱飞即落·三意愿正面明说〔会停+会保存甚至转发〕=REACT 带内高点回归〔v1 7.0/v2 8.0/v3-v6 7.0 后 8.0=带内高点第二件·v2 市场直配件同位〕·「结合热点与虚构城市独特视角」正面定性七连证+记忆/怀旧话题讨论价值明说=本件主题域直接确认位·旗①=信条「城市不会忘记」语境门槛族变体第二连〔v6 同型·verbatim 不可改写·吸收位=M5 图文页语境〕+副旗=标题-内容关联性〔盲评面轴位映射律常规张力〕·非拦截·净本 expert-verdicts/20261001-002959-E4-audience.md+expert-calls 00:29 行）；发布锁"
assert old in fin
fin = fin.replace(old, new)
io.open("output/finished.md", "w", encoding="utf-8").write(fin)

# 5) cards/README v7 row sync
cr = io.open("data/storylines/cards/README.md", encoding="utf-8").read()
old5 = "·M4.5 七席 ≥9（review-20261001-mcreact-v7.md）·**E4 异步在飞（下轮回填）→F-077**"
new5 = "·M4.5 七席 ≥9（review-20261001-mcreact-v7.md）·**E4 同轮回填 8.0（00:29:59 热载快落·三意愿正面=REACT 带内高点回归·旗①=信条语境门槛族变体第二连·非拦截）→F-077**"
assert old5 in cr
cr = cr.replace(old5, new5)
io.open("data/storylines/cards/README.md", "w", encoding="utf-8").write(cr)

# 6) station-reviews row sync
sr = io.open("docs/reviews/station-reviews.md", encoding="utf-8").read()
old6 = "E4 参考（异步在飞·回填位 R797） | 七席 6×9.0+E7 N/A（E4 带参考线挂回填轮）"
new6 = "E4 参考（同轮回填 8.0） | 七席 6×9.0+E7 N/A（E4 8.0 参考=REACT 带内高点回归）"
assert old6 in sr
sr = sr.replace(old6, new6)
sr = sr.replace("review-20261001-mcreact-v7.md+cards.json meta 自证+em-check-r796.txt+MC-20261001-REACT-v7-tmp/e4-result.json（回填位） |",
                "review-20261001-mcreact-v7.md+cards.json meta 自证+em-check-r796.txt+expert-verdicts/20261001-002959-E4-audience.md（E4 8.0 同轮回填毕） |")
io.open("docs/reviews/station-reviews.md", "w", encoding="utf-8").write(sr)

# 7) status-export sync
se = json.load(io.open("docs/status-export.json", encoding="utf-8"))
o = se["outs"][0][1]
se["outs"][0][1] = o.replace(
    "七席 6×9.0+E7 N/A·E4 脱壳在飞下轮回填",
    "七席 6×9.0+E7 N/A·E4 同轮回填 8.0=REACT 带内高点回归（三意愿正面·旗①=信条语境门槛族变体第二连·非拦截）"
).replace("tokens:local=1（E4 qwen 在飞未落=落地轮记账）", "tokens:local=1（E4 qwen2.5:14b 同轮落地记账）")
se["results"][0][1] = se["results"][0][1].replace(
    "⑧E4 参考仪 Start-Process 脱壳在飞（1500s 窗·e4-result.json 轮间落地·R797 回填位·非拦截）",
    "⑧E4 参考仪 Start-Process 脱壳**同轮落地回填 8.0**（00:29:59 热载快落·三意愿正面=REACT 带内高点回归〔v2 同位第二件〕·旗①=信条语境门槛族变体第二连+副旗=标题-内容关联性〔盲评面轴位映射律常规张力〕·非拦截·净本 20261001-002959-E4-audience+expert-calls 00:29 行）"
).replace("下轮=R797：①E4 回填②W2 余刀", "下轮=R797：①W2 余刀")
se["live"][0] = ["当前活：R796 REACT 10-01 热点窗全链一轮毕=F-077 登记第 77 件（E4 参考仪同轮回填 8.0=REACT 带内高点回归）"]
io.open("docs/status-export.json", "w", encoding="utf-8").write(json.dumps(se, ensure_ascii=False, indent=1))

# 8) state.json addendum (追加制·如实记 E4 收账时刻后落地)
st = json.load(io.open("src/os/state.json", encoding="utf-8"))
st["log"].append(
    "2026-10-01 00:3x R796 轮末补记（E4 同轮落地回填·追加制如实记）：收账步后 E4 参考仪 00:29:59 落判（Start-Process 脱壳快落·qwen2.5:14b 热载）=**8.0 三意愿正面明说**（会停+会保存甚至转发=REACT 带内高点回归〔v1 7.0/v2 8.0/v3-v6 7.0 后 8.0=带内高点第二件·v2 市场直配件同位〕·「热点×虚构城市独特视角」正面定性七连证+记忆/怀旧话题讨论价值明说=本件主题域直接确认位·旗①=信条「城市不会忘记」语境门槛族变体第二连〔v6 同型·verbatim 不可改写·吸收位=M5 图文页语境〕+副旗=标题-内容关联性〔盲评面轴位映射律常规张力=v1-v6 副旗族同型〕·最弱=一致性〔双旗轮如实记〕·非拦截·七席 ≥9 PASS 维持）——回填五件=review v1.1（E4 节+未测面销项+变更行）+净本 expert-verdicts/20261001-002959-E4-audience.md+expert-calls 00:29 行+finished.md F-077 段 E4 句+cards/README/station-reviews/export 四同步·tokens:local=1（E4 qwen 同轮落地记账修正：log 行「在飞未落=落地轮记账」为收账时点真值·00:29:59 落地后本笔即落地轮=同轮双记账合一·P-54⑤ 计量律）"
)
st["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
io.open("src/os/state.json", "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=2))
print("E4-BACKFILL-OK")
