# -*- coding: utf-8 -*-
"""R2076 close-out: tech#136/#137 delivery marks, seed #138, state
tick/log/ts/task, orders watermark 320 hygiene bump (R2075 consumed
row 320 but left the stored watermark at 319)."""
import io
import json
import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TECH = ROOT + r"\state\queue\tech.md"
STATE = ROOT + r"\src\os\state.json"

now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")
R = "R2076"
DONE_TAG = " [done 2026-10-12 " + R + "]"

LOG_LINE = (
    "2026-10-12 21:0x " + R + ": 工程腿·tech#136/#137 双交付（R2075 种子当轮兑现·1261 全回归绿）——"
    "①tech#136 comfy_activity 波间空窗第三面（wave-gap face：ComfyUI output 树顶层 fresh 条目〔文件+子目录 mtime·kf_bma 实形锚〕≤900s=迭代回炉循环活体证词→active+wave-gap-recent-output 注记·保守单向接线=只添 active 永不强制 quiet·run_probe output_dir=None 默认=测试密闭性·CLI --output-dir/--output-recency-s·ledger 增 output_recent 字段·R2075 20:44 三闲误读面就此闭合：该时点 kf_bma mtime 20:41≈3min→现机制判 active）；"
    "②tech#137 fire_consume workday-block×O-2025 调和（CEO 下班旗=data/pipeline/ceo-off-work-flag.json〔同日旗解除 08:00-23:59 硬阻断·缺失/畸变/跨日一律不解除=fail-closed〕+NOW_FN 测试缝〔修复潜伏缺陷=工作时段跑套件全 CLI 测试被 block 吞〕+当轮按 R2074 消费的 O-20261012-2025 实弹落旗 declared_ts 20:50·活体链验证=无旗 rc1 bm-a-workday-hours-zero-dispatch→落旗后 card 流达 card-no-fire: mv-active）；"
    "③收账卫生=orders_row_watermark 319→320 bump（R2075 消费行 320 未记账缺口）+fire_consume.py 15:0x 工作日阻断实现 4 轮未提交债一并外科提交；"
    "④三探针=board 0 FAIL/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 3 FAIL 皆在案史实（新增=今日 10:57 outage=R2048 案族第五案已录）·F 三件 yield 维持（comfy quiet 读数 newest_age 1354s 波感可见=judgment 层可见面）·夜窗 00:00 F-180 派发窗+tech#92 权威窗 10-13 08:00 维持；"
    "⑤队列=136/137 done 标+138 新种子（output face 深度 2 层覆盖缺口）。"
)

TASK_LINE = LOG_LINE.split("：", 1)[1][:60]

# ---------- 1. tech.md: done marks + seed ----------
with io.open(TECH, encoding="utf-8") as fh:
    tech = fh.read()

h136 = "136. [R2075 补货·本轮真发现种子]"
h137 = "137. [R2075 补货·本轮真发现种子]"
assert tech.count(h136) == 1, "tech 136 anchor not unique"
assert tech.count(h137) == 1, "tech 137 anchor not unique"

d136 = (
    "136. [done 2026-10-12 R2076] [R2075 补货·本轮真发现种子]"
)
d137 = (
    "137. [done 2026-10-12 R2076] [R2075 补货·本轮真发现种子]"
)
tech = tech.replace(h136, d136, 1)
tech = tech.replace(h137, d137, 1)

# delivery evidence continuation lines right after each item line
lines = tech.splitlines(True)
out = []
for ln in lines:
    out.append(ln)
    if ln.startswith("136. [done 2026-10-12 R2076]"):
        out.append(
            "   ——已交付（R2076）：comfy_activity.py 第三面 wave-gap face（read_output_face 顶层文件+子目录 mtime 扫描·默认 900s 覆盖 R2075 实测 6-10min 波距带外裕·compute_verdict 保守单向=只添 active 永不强制 quiet/绝不挡两面 quiet 路径·cpu-empty server-down 也被 fresh output 压制=R1986 GO 秒级再点火族防烧〕·run_probe output_dir=None 默认不触真盘=套件密闭性·ledger output_recent 字段·21 新测〔OutputFaceTests 7+VerdictTests 6+RunProbe 1+Ledger 1+CLI 1+imports〕·活体验证=21:03 读 quiet newest_age=1354s〔波感可见面〕；R2075 20:44 误读时点机制反演=active 判对〕\n")
    if ln.startswith("137. [done 2026-10-12 R2076]"):
        out.append(
            "   ——已交付（R2076）：fire_consume.py CEO 下班旗调和（read_ceo_off_work_flag fail-closed 解析〔缺失/畸变/跨日=不解除〕·workday_dispatch_blocked(dt, flag) 同日旗解除 08:00-23:59 阻断·周末/夜窗照旧·NOW_FN 测试缝〕+ceo-off-work-flag.json 实弹落旗〔O-20261012-2025 按 R2074 消费 declared_ts=2026-10-12 20:50:00·晨窗自愈/CEO 回机=移除步入 main#21 复役位〕+活体链=无旗 rc1 硬阻断→落旗后 card 流达（card-no-fire: mv-active）·10 新测〔WorkdayBlockTests 8+CLI 2〕·随行修复=15:0x workday-block 实现四轮未提交债入库+NOW_FN 修工作时段套件必红潜伏缺陷〕\n")
tech = "".join(out)

# seed 138 append
seed138 = (
    "138. [R2076 补货·tech#136 交付面真发现] **wave-gap output face 深度 2 层覆盖缺口**（缺口锚=read_output_face 只扫顶层〔顶层文件+顶层子目录 mtime〕——单层深批写 output/<sub>/file.png 顶层子目录 mtime 承载〔kf_bma 实形〕·但两层深批写 output/<a>/<b>/file.png 只 bump <b> mtime 顶层全冷=波信号丢失；两层深树非假想=MV 域 kf-demo-20261012/bmc/i2v/ 产物形在册〔他窗只读锚〕·当 MV 会话把 i2v 批落 ComfyUI output 树时本面即盲；候选=顶层 fresh 子目录再下探一层 scandir〔成本 ~N 目录·不 rglob〕+回归锁测试；判据=两层深新鲜批写读 active·判负留痕合法）——观察位：MV i2v 波落 output 树形态确认时领\n"
)
tech = tech.rstrip("\n") + "\n" + seed138
with io.open(TECH, "w", encoding="utf-8", newline="") as fh:
    fh.write(tech)
print("tech.md: 136/137 done-marked + evidence, seed 138 appended")

# ---------- 2. state.json ----------
with io.open(STATE, encoding="utf-8") as fh:
    st = json.load(fh)
st["tick"] = st.get("tick", 0) + 1
st["ts"] = ts
st["task"] = TASK_LINE
st.setdefault("log", []).append(LOG_LINE)
st["orders_row_watermark"] = {"rows": 320, "tail_key": "10-12 20:4x"}
with io.open(STATE, "w", encoding="utf-8", newline="") as fh:
    json.dump(st, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("state.json: tick=%s ts=%s watermark=320" % (st["tick"], ts))
