# -*- coding: utf-8 -*-
"""R797 close-out: tick, log append, ts/task refresh, watermark merge (content-addressed)."""
import json, re, io
from datetime import datetime

STATE = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
GROUP_DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"

with io.open(STATE, "r", encoding="utf-8") as f:
    st = json.load(f)

# 1. watermark merge: D/C-YYYYMMDD-NN regex set from group decisions.md (content-addressed)
with io.open(GROUP_DEC, "r", encoding="utf-8") as f:
    txt = f.read()
tokens = set(re.findall(r"[DC]-\d{8}-\d{2}", txt))
wm = st.get("decisions_watermark", {}).get("dnums", [])
base = set(wm)
merged = sorted(base | tokens)
st["decisions_watermark"]["dnums"] = merged

# 2. tick
old_tick = st.get("tick", 0)
st["tick"] = old_tick + 1

# 3. log append
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logline = (
    "2026-10-01 00:5x R797: 收讫+生产轮·D-20261001 集团批 10 新行全读 ack+两执行腿交付（decisions dnum 差集 10 新行=C-20260930-04/05/06+D-20261001-01~07·r795_scan 谱系 00:44 首扫检出→轮内处理=D-13 SLA 窗内·转全任务书收令轮）——"
    "①收讫判读全过审零驳回：**D-20261001-03 消费步正典一行自领**=iteration_prompt.txt 消费步块增行（git fetch+git show origin/main:<path> 制·禁 working-tree pull/rebase/checkout 对齐·禁写侧接触·bm-a 同机宿主注记=工作树正源同源面零对齐操作·本司被引用双司先例参照 F-20260930-01 在案·窗 10-03 12:00 提前闭）；"
    "②**D-20261001-06 赋能单 c 交付=城市生长预演内容选题框架**（「板块十年」内容之问·预演短片叙事·窗 10-03 12:00 提前闭）=`docs/research/R-20261001-bigstream-01-city-growth-preview-topics.md` v1.0 六节（立项三问 P-65 齐/十问内容之问表=Q1 记忆-Q10 档案记忆·每问三判据=真数据律+十年两态对照+L18 题眼句/三形态双窗位=定格生长+一栋楼的十年+街角编年史·预演=推演声明位诚实律/跨司数据接口表 8 行挂供方对号赋能单 a·b 单/选题池 8 行 M0 预分 7·6·7·7·7·7·6·7 全 A 档·4 可先行+4 gated/应用表挂承接=BigHouse P3 消费+本司视频线 gated 候选/验证声明=判据可机核+红线零豁免）；"
    "③C-20260930-06 写入侧 400 字闸承接（本仓 CODELY.md=指针行纪律·现状 4.6KB 远低 30KB 单件帽·>400 字条=0 实测）+C-20260930-05 流量自报=既有 tokens:local 面维持（三面流量基线表 10-01 首报=夜轮组织面非本司份额）；"
    "④零份额知悉=C-20260930-04（@Biggame/@FluxVerse/@CPH4 修法四件派单）/D-20261001-01（本司 F-01/03/04 核销收讫·D-06 ack 在案复证）/D-02（Bonsai observe 维持·bm-a GPU 档复验=BigMoney 自领）/D-05（O 号撞号勘误）/D-07（量化监督摘要任务注册+夜轮复验）；"
    "⑤回执双载体=HQ-FEEDBACK F-20261001-01+commit 消息含 D-20261001-01~06/C-20260930-04/05/06+R797（P-51 送达·下一动作=BigHouse 侧消费引用判据+预演短片拍稿素材面 gated）；"
    "⑥水位=watermark 内容寻址合并 102→112 落账（10 新 dnums 入基线·D-20260930-19 差集制执法）；"
    "⑦轮首五查余静=orders 42 锚零新令（顶=O-20260928-1910）/ledger 六模式 40=值守行位移带零新 CEO 令级事件/production=open 自愈核在位/无 index.lock/树态三成员维持（M CODELY.md=R767 平台记忆压缩波定谳零接触·codex 两件 mtime 09-29 04:06 未动=#86 c+d 让位判据未达·两文件零接触）；"
    "例行件：日报 10-01 在案不重跑（R795 补产·REACT 10-01 窗件已毕 F-077 R796）/W40 周审在案（R576）/GB 闸 10-08（R795 v1.1 已刷·W2 余刀⑤/①/③ ≤10-04 随窗）/W41 周报=10-05 后首个周轮（自驱面+CLOUD_LINE 首测窗）/#70 OSS 窗 3=10-02 21:40 后开/T1 催办=已裁项停用口径/HQ-FEEDBACK 本轮一行=收讫回执非 open 问题（F-20261001-01）·tokens:local=0（收令判读+框架件纯会话撰写+探针脚本零本地模型调用·P-54⑤ 计量律如实记）——"
    "下轮=R798 可领序：①W2 下扫刀余项（刀⑤ GB 45438 全文层+刀① 珊瑚安全站点公告面+刀③ B站 help 复探·≤10-04 窗）②#86 c+d 让位判据③#70 OSS 窗 3（10-02 21:40 后开）④预演短片「可先行」选题评估（BigHouse 消费回执后）。收账显式列文件 commit+push"
)
st["log"].append(logline)

# 4. ts+task refresh
st["ts"] = now
st["task"] = logline.split(" ", 1)[1][:60] if logline.startswith("2026-10-01") else logline[:60]

# 5. focus refresh for next round
st["focus"] = (
    "R798: ①W2 下扫刀余项（刀⑤ GB 45438-2025 全文层〔openstd 详情页隐式标识参数〕+刀① 珊瑚安全站点公告面+刀③ B站 help 复探·R-20260927 §五·窗 ≤10-04·每刀 ≤15min 限时律）"
    "②#86 c+d 让位判据（codex mtime 09-29 04:06 未动=未达·零接触）③#70 OSS 窗 3（10-02 21:40 后开·候选=ASS/libass 逐行居中 R9 遗留位+扫描正则负向断言降级项）"
    "④预演短片「可先行」选题评估（框架件 §4 #2/#4/#6/#8·BigHouse 消费引用回执后起链判据）——五查锚=orders 42〔41 O-件+README 口径〕·ledger 六模式 40/41（值守行位移带）·decisions dnum 112 基线（差集 0）·GB 闸 10-08（R795 v1.1 已刷）"
)

with io.open(STATE, "w", encoding="utf-8") as f:
    json.dump(st, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("tick %d->%d | dnums %d->%d | ts=%s" % (old_tick, st["tick"], len(base), len(merged), now))
print("new_dnums=%s" % sorted(tokens - base))
