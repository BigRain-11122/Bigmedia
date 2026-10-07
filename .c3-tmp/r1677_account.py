# -*- coding: utf-8 -*-
# R1677 accounting: order-receipt round (D-20261008-03 restock dispatch) + watermark advance.
import json, datetime, io, re

SP = "src/os/state.json"
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

log_line = (
    "2026-10-08 00:2x R1677: 收令轮·D-20261008-03 备货池补货派单收讫即执行（点名→回执制第四例·ack+补货+回执同轮闭环·实活轮）——"
    "①轮首五查破静=decisions+ledger mtime 00:09:50 翻新（R1676 锚 12:07:04 后窗内新落=集团 00:10 班批）"
    "→dnum 内容寻址差集 TRULY_NEW=6 行（C-20261007-04+D-20261007-07+D-20261008-01~04·伪差族 D-20260930-008/D-20260930-1 排除不重列）"
    "→转全任务书收令；②判读=本司涉行 1=D-20261008-03 备货池补货 ≥2 条自可执行行+回执行落 HQ-FEEDBACK"
    "（窗 10-09 00:00·T2 否决窗至 10-15·依据=self-drive v2.0 lane 常备 ≥2+真实活面在册点名〔M0 城市生长选题池 4 可先行行+REACT 择优族+周轮件族〕）"
    "·其余=D-01 回执核销批 22+overruled 复扫+D-02 值守报告缺位定谳=HQ 件·D-04 gaming/CODELY 分卷预算=MiniGame 件"
    "·C-20261007-04/D-20261007-07 存量精简与机队同构案过会=HQ 落件零新文件"
    "（D4 记忆瘦身司域预算 ≤80KB 注=本司 CODELY.md 3,219B 远低线零动作·D2 机队同构=集团正典承接自证禁代写·D3 orders 月卷轮转=只读消费正典照守）"
    "→科学判断闸全过审零驳回；③执行=补货两行落板（#101《板块十年·立国日》预演短片首件全链起链+#102《灯亮起来那天》备位"
    "·R-20261001-bigstream-01 §4 选题 #2/#4 可先行行·M0 预打分 7/8 A 档·素材面在册零外锁"
    "·消费面指名=本司视频线新形态+BigHouse P3 苏州吴中叙事规格候选·R-20261001 §5 交付判据=BigHouse 侧引用 ≥1 处）"
    "+#100 执行行+HQ-FEEDBACK F-20261008-01 回执行（对象/判据/窗口一行）+commit 含 D-20261008-03+R1677+下一动作（P-51 送达）"
    "——板面自可执行行 0→2=备货缺货态解除·gated 面清点如实注（#59 日闸/#63 供给闸/#67 derive 闸/#70 21:40 时间闸/#99 通道闸/E30 复市件日窗闸=gated 不入备货数）；"
    "④水位=decisions_watermark dnums 162→168（6 新行入账·伪差族两枚不入=standing practice）+派工板涉司行复核=D-20261008-03 状态 dispatched=本轮回执后按销项面呈集团侧；"
    "⑤生产指针=DAILY v69 复市件=E30 lane 烟火/weekend/13 门控行（10-08 复市日解锁·池行「市场买卖讲价，公平公正正正」=日间市场活动面"
    "·literal 日窗 05:52+ 兑现=R1321 日窗硬闸先例承继·本 00:2x 夜窗不产=诚实 literal 律·R1388 dusk 挂账 49 轮同纪律）"
    "+GB 7 日闸 01:02+OSS w5 21:40+#101 拍稿起链=下轮可领活；"
    "⑥例行件=daily1008 在案不重跑〔一份为真相〕·W41 周审在案·GB day7 到期 10-08 01:02=下窗刷新位"
    "·HQ-FEEDBACK 本轮新行=集团派单回执行（合法载体非膨胀）·export 刷新（实况变化=D-20261008-03 收讫+板面补货 0→2·F3 律）"
    "·tokens:local=0（纯脚本零模型调用·P-54⑤ 计量律）——"
    "下轮=日界批余项（GB 01:02 刷新→#101《板块十年·立国日》拍稿起链→复市 DAILY v69 literal 日窗 05:52+→OSS w5 21:40）；异常=无"
)

task_src = "R1677: " + log_line.split("R1677: ", 1)[1]

with open(SP, encoding="utf-8") as f:
    st = json.load(f)

assert st["tick"] == 1676, "tick moved before accounting"
assert st["log"][-1].startswith("2026-10-08 00:0"), "last log entry unexpected"

st["tick"] = 1677
st["ts"] = now
st["task"] = task_src[:60]
st["focus"] = (
    "R1677 收令轮=D-20261008-03 备货池补货派单收讫即执行毕（ack+补货 2 行+HQ 回执同轮·板面自可执行 0→2=备货缺货态解除）。"
    "五查破静=decisions/ledger 00:09:50 新批·TRULY_NEW=6（C-20261007-04/D-20261007-07/D-20261008-01~04·涉司行=D-20261008-03·余皆他司/HQ 件零动作）"
    "·水位 162→168。补货交付=#101《板块十年·立国日》预演短片首件起链+#102《灯亮起来那天》备位（R-20261001 §4 #2/#4 可先行·消费面=视频线新形态+BigHouse P3 候选）。"
    "生产指针=GB 7 日闸 01:02→#101 拍稿起链（下轮领）→DAILY v69 复市件 literal 日窗 05:52+（烟火/weekend/13 门控行·夜窗不产诚实律）→OSS w5 21:40。"
    "next=R1678 GB 刷新+#101 起链或复市件日窗兑现。"
)

# --- decisions watermark advance (content-addressed, standing pseudo-diff family excluded)
new_dnums = [u"C-20261007-04", u"D-20261007-07", u"D-20261008-01", u"D-20261008-02", u"D-20261008-03", u"D-20261008-04"]
wm = st["decisions_watermark"]
dnums = wm["dnums"]
before = len(dnums)
for d in new_dnums:
    if d not in dnums:
        dnums.append(d)
# machine verify: all six present in group decisions.md
dec_text = io.open(DEC, encoding="utf-8").read()
for d in new_dnums:
    assert d in dec_text, "dnum %s not in decisions.md" % d
wm["ts"] = now
# board_rows: count dispatch-board table rows (| D-xxx / | C-xxx) in the board section
m = re.search(r"派工通告板(.*?)###\s*台账", dec_text, re.S)
board_rows = len(re.findall(r"^\|\s*[DC]-\d{4}-", m.group(1), re.M)) if m else wm.get("board_rows")
wm["board_rows"] = board_rows

st["log"].append(log_line)

with open(SP, "w", encoding="utf-8") as f:
    json.dump(st, f, ensure_ascii=False, indent=2)

print("OK tick=%d ts=%s log_len=%d wm=%d->%d board_rows=%s" % (st["tick"], st["ts"], len(st["log"]), before, len(dnums), board_rows))
print("task=%s" % st["task"])
