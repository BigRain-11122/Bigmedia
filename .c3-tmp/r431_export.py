# -*- coding: utf-8 -*-
# r431 accounting: state.json task-field refresh (round-trip safe) + status-export.json derived refresh
import io, json, os, datetime

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(repo)

# 1) state.json: refresh task field only (tick/ts/log already updated this round)
sp = os.path.join(repo, "src", "os", "state.json")
with io.open(sp, encoding="utf-8") as f:
    d = json.load(f)
d["task"] = "R431: 生产轮·#69 P-20260926-07 机队大模型自配令 bigstream 份额交付毕（R430 板序"
with io.open(sp, "w", encoding="utf-8", newline="\n") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
    f.write("\n")
with io.open(sp, encoding="utf-8") as f:
    d2 = json.load(f)
print("state ok tick=%s log=%d task=%s..." % (d2["tick"], len(d2["log"]), ascii(d2["task"][:20])))

# 2) status-export.json: export_ts + depts + outs + results derived from R431 actuals
ep = os.path.join(repo, "docs", "status-export.json")
with io.open(ep, encoding="utf-8") as f:
    e = json.load(f)
e["export_ts"] = "2026-09-26T22:08:00+08:00"
append_ceo = "+P-2026-09-26-07 机队大模型自配令 bigstream 份额交付毕（R431 #69 done·serve 常驻复核一致+12GB 模型阶梯分档自查〔7b 全员常驻档 ✓/14b 重判断档=阶梯线外产线在役偏差如实记/bge-m3 ✓/VL 档 N/A 零缺口〕+U187 大件律扫描 2832 追踪件零 >50MB+回执 F-20260926-01·窗 ≤09-28 提前闭）"
for dep in e.get("depts", []):
    if dep.get("n") == "总裁办公室":
        if "P-2026-09-26-07" not in dep.get("t", ""):
            dep["t"] = dep.get("t", "") + append_ceo
    if dep.get("n") == "工程技术部":
        dep["t"] = "OS 循环 R431（生产轮·#69 P-2026-09-26-07 机队大模型自配令 bigstream 份额交付毕：serve 常驻复核一致〔ollama.exe PID 23412·09-24 17:45 起+Startup 自启 lnk+API 四模型应答·零新装配=R306/R307 已验在案〕+12GB 模型阶梯分档自查〔7b 全员常驻档 ✓ qwen2.5:7b-instruct/14b 重判断档=阶梯线外产线在役偏差如实记=S1 门+E4 参考仪判断席/bge-m3 嵌入档 ✓/VL 视觉档 N/A 零任务缺口/阶梯外库存 qwen3-coder:30b 如实注〕+模型大件律=git 2832 追踪件 ls-tree -l 扫描 >50MB=0·U187 绝对禁达标+零 LFS+模型仓外·回执=HQ-FEEDBACK F-20260926-01+backlog #69 done+commit 含令号·窗 ≤09-28 提前闭·轮首五查 ledger 25=锚〔轮首 inline startswith 过滤法误计 0=口径错误当场定谳弃用〕·三探针 board 0 FAIL 5 题 10 稿/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 1 FAIL 在案史实同事件足迹·腿③扫描两次实现 bug 轮内咬住〔cat-file 收路径不收 SHA→ls-tree 单 tab 修正→2832/2832 全解析〕=parsed 行数防假绿守则）·state.ts/task 心跳面刷新"
new_out = "tick 431·R431（生产轮·#69 P-2026-09-26-07 机队大模型自配令 bigstream 份额交付毕：serve 常驻复核一致〔ollama.exe PID 23412·09-24 17:45 起+Startup 自启 lnk+API 四模型应答·零新装配〕+12GB 模型阶梯分档自查〔7b 全员常驻档 ✓ qwen2.5:7b-instruct 4.68GB/14b 重判断档=阶梯线外产线在役偏差如实记=S1 门+E4 参考仪判断席在役实锚〔S1 v1.5 三连 10/10〕·12GB 紧张面=单模型分时纪律/bge-m3 嵌入档 ✓ 1.16GB/VL 视觉档 N/A 零任务缺口/阶梯外库存 qwen3-coder:30b 18.56GB 如实注〕+模型大件律=git 2832 追踪件 ls-tree -l 扫描 >50MB=0·>95MB=0〔U187 绝对禁达标〕+piper 60MB onnx untracked〔check-ignore 命中 .gitignore:9〕+零 LFS+模型仓外=三禁全达标·分治任务承接在役=S1 门+E4 参考仪+P4 调研摘要·回执=HQ-FEEDBACK F-20260926-01+backlog #69 done+commit 含令号·窗 ≤09-28 提前闭·操作红=腿③扫描两次实现 bug 轮内咬住〔cat-file batch-check 收路径不收 SHA=零行解析→ls-tree 单 tab 格式修正→2832/2832 全解析〕=扫描件零解析必查 parsed 行数防假绿灯〔R381 垂直栈同型〕）"
for row in e.get("outs", []):
    if row and row[0] == "OS 循环":
        row[1] = new_out
for row in e.get("results", []):
    if row and row[0] == "430":
        row[0] = "431"
with io.open(ep, "w", encoding="utf-8", newline="\n") as f:
    json.dump(e, f, ensure_ascii=False, indent=1)
    f.write("\n")
with io.open(ep, encoding="utf-8") as f:
    e2 = json.load(f)
print("export ok ts=%s results0=%s" % (e2["export_ts"], e2["results"][0][0]))
