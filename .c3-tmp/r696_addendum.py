# -*- coding: utf-8 -*-
"""R696 round-end addendum: S1 gate landed 18:21:56, 10/10 PASS one-pass."""
import io, json, time, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
def p(rel): return os.path.join(ROOT, rel)
now = time.strftime("%Y-%m-%d %H:%M:%S")

ADD = ("2026-09-29 18:2x R696 轮末补记（S1 门轮末同窗落地·追加制原行不改写·R682 补记先例）：S1 wrapper 收账 commit 后 18:21:56 落判 exit 0="
 "总分 10·违律清单无·总裁决「PASS（材料合规且亮点突出）」=**10/10 PASS 零违律一次过**（判词档 20260929-182156-S1-script+expert-calls 行 wrapper 自动+"
 "s1-result.json 留档·S1 v1.5 七连满分〔F-002/003/004+LC-003/004/005/006→LC-007〕）——主行「轮末未落=下轮首读」为收账时点真值·落地后如实补记；"
 "R697 续腿面更新=M1 0F0W 已毕+S1 已过门→**空气预算机械裁链为下轮首位**（卡片锚点列零动+信条零动+S1 判 v1 初稿机械裁不回炉=fleet 先例）→TTS light→渲染腿→S2 三门→E8→ASR+E4→M4→F 登记→冗余池第四件落位；"
 "wrapper 产物随本补记 commit（判词档+expert-calls 行+s1-result.json+stdout/stderr）+lc007 README 门禁块/生产记录 S1 行回填+renders 声明行 S1 片段回填+export OS/live 同步。")

# 1. state.json: append addendum + refresh ts
sp = p("src/os/state.json")
st = json.load(io.open(sp, encoding="utf-8"))
st["log"].append(ADD)
st["ts"] = now
io.open(sp, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=1))

# 2. lc007 README: production record + gate block
rp = p("data/sources/lc007/README.md")
rt = io.open(rp, encoding="utf-8").read()
rt = rt.replace(
    "②S1 v1.5+L18-L20 门 wrapper 起飞（.lc007-tmp/s1_call.py=.lc006-tmp 同型·1500s 脱壳）——下轮首读 s1-result.json（R176→R177 先例·≥9 过门→M1 即检→空气预算机械裁链→TTS light；<9 实质旗整改）",
    "②S1 v1.5+L18-L20 门 **10/10 PASS 零违律一次过**（18:21:56 轮末同窗落地·判词档 20260929-182156-S1-script+expert-calls 行 wrapper 自动+s1-result.json 留档·七连满分）")
rt = rt.replace(
    "- S1 编剧官：PENDING（wrapper 在飞·R697 首读回填）",
    "- S1 编剧官：**10/10 PASS 零违律一次过**（18:21:56 轮末同窗落地·判词档 20260929-182156-S1-script）")
io.open(rp, "w", encoding="utf-8").write(rt)

# 3. renders README declaration fragment
pp = p("output/renders/README.md")
pt = io.open(pp, encoding="utf-8").read()
pt = pt.replace(
    "s1-result.json[S1 wrapper 起飞 R696·判分式落档待 R697 首读=R176→R177 先例]",
    "s1-result.json[判分式落档·**R696 轮末同窗落地 10/10 PASS 零违律一次过**·18:21:56·判词档 20260929-182156-S1-script+expert-calls 行 wrapper 自动]")
io.open(pp, "w", encoding="utf-8").write(pt)

# 4. status-export: OS row + results 696 + live line 1 refresh
ep = p("docs/status-export.json")
se = json.load(io.open(ep, encoding="utf-8"))
for k, v in se.items():
    if isinstance(v, list):
        for row in v:
            if isinstance(row, list) and len(row) >= 2 and isinstance(row[1], str):
                if row[0] == "OS 循环" and "S1 wrapper 起飞（PID 55520·R697 首读）" in row[1]:
                    row[1] = row[1].replace(
                        "S1 wrapper 起飞（PID 55520·R697 首读）",
                        "S1 门 18:21:56 轮末同窗落地 10/10 PASS 零违律一次过")
                if row[0] == "696" and "S1 wrapper 起飞（PID 55520·R697 首读）" in row[1]:
                    row[1] = row[1].replace(
                        "S1 wrapper 起飞（PID 55520·R697 首读）",
                        "S1 门 18:21:56 轮末同窗落地 10/10 PASS 零违律一次过（七连满分）")
for line in se["live"]:
    if line and isinstance(line[0], str) and "S1 门 wrapper 在飞=R697 首读" in line[0]:
        line[0] = line[0].replace(
            "S1 门 wrapper 在飞=R697 首读",
            "S1 门 10/10 PASS 一次过（18:21:56 轮末同窗落地）")
io.open(ep, "w", encoding="utf-8").write(json.dumps(se, ensure_ascii=False, indent=1))

# 5. verify
ver = []
st2 = json.load(io.open(sp, encoding="utf-8"))
ver.append("log_tail_addendum=%s" % st2["log"][-1].startswith("2026-09-29 18:2x R696 轮末补记"))
ver.append("log_count=%d (prev 721 + 1)" % len(st2["log"]))
ver.append("ts_fresh=%s" % (st2["ts"] == now))
rt2 = io.open(rp, encoding="utf-8").read()
ver.append("readme_s1_pass=%s" % ("10/10 PASS 零违律一次过" in rt2 and "PENDING" not in rt2))
pt2 = io.open(pp, encoding="utf-8").read()
ver.append("renders_s1=%s" % ("20260929-182156-S1-script" in pt2))
se2 = json.load(io.open(ep, encoding="utf-8"))
ver.append("os_s1=%s" % any(isinstance(r, list) and len(r) >= 2 and r[0] == "OS 循环" and "10/10 PASS" in r[1]
                            for v in se2.values() if isinstance(v, list) for r in v if isinstance(r, list)))
ver.append("live_s1=%s" % any("10/10 PASS" in l[0] for l in se2["live"]))
ver.append("verdict_file=%s" % os.path.exists(p("docs/reviews/expert-verdicts/20260929-182156-S1-script.md")))
io.open(p(".c3-tmp/r696_verify4.txt"), "w", encoding="utf-8").write("\n".join(ver))
print("ADDENDUM_DONE")
