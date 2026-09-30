# -*- coding: utf-8 -*-
"""R696 OS-row fix: the OS row lives in 'outs' as ["OS 循环", "tick NNN,..."]."""
import io, json, os
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
ep = os.path.join(ROOT, "docs", "status-export.json")
se = json.load(io.open(ep, encoding="utf-8"))
short = ("R696 生产轮·queue §E 补池义务兑现=E7 LC-007 邓建国拆条入池+选优定谳+起链（R695 出池注记承接·冗余扩容位第四件）：选优三强对比定谳=邓建国 C-00027（前件点名兑现位=C-00028 十四号路灯经历字段「塔站的值守员说它比仪器可靠」反点名+LC-006 拍内明写台风梅花=共享事件互补叙事→第三对人物链四卡续延）+拍稿 v1 12 拍 232 字+M1 0F0W 一次过+S1 wrapper 起飞（PID 55520·R697 首读）——lane=E3+E7 恢复 ≥2 达标；五查三锚静（orders O-1910/ledger 38/decisions 75·codex 批未闭让位维持）·三探针 board 0F/readiness 3 外部 0 发现/loop 在案类 tick696 收账自平·例行件在案·tokens:local=0（S1 在飞未落=落地轮记账）")
fixed = 0
for k, v in se.items():
    if isinstance(v, list):
        for row in v:
            if isinstance(row, list) and len(row) >= 2 and isinstance(row[1], str) and row[1].startswith("tick "):
                row[1] = "tick 696，" + short
                fixed += 1
io.open(ep, "w", encoding="utf-8").write(json.dumps(se, ensure_ascii=False, indent=1))
# re-verify
se2 = json.load(io.open(ep, encoding="utf-8"))
ok = any(isinstance(r, list) and len(r) >= 2 and isinstance(r[1], str) and r[1].startswith("tick 696")
         for v in se2.values() if isinstance(v, list) for r in v if isinstance(r, list))
io.open(os.path.join(ROOT, ".c3-tmp", "r696_verify2.txt"), "w", encoding="utf-8").write(
    "os_rows_fixed=%d\nos_row_tick696=%s\nresults_tail=%s\nlive_lines=%d\nexport_ts=%s" % (
        fixed, ok, se2["results"][-1][0], len(se2["live"]), se2["export_ts"]))
print("OSFIX_DONE fixed=%d ok=%s" % (fixed, ok))
