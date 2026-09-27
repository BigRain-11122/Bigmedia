# -*- coding: utf-8 -*-
"""R505: refresh outs row-0 (OS loop row) to R505 live status."""
import io, json, datetime

FP = r"docs\status-export.json"
d = json.load(io.open(FP, encoding="utf-8"))
now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
d["export_ts"] = now

outs = d["outs"]
row0 = outs[0]
row0[1] = ("tick 505→R505 实况：O-1050 议程 3 起链毕——城市叙事首件样片脚本 SC-003-01-v1 落件 "
           "(data/storylines/video/《城市窗面》EP.01《凌晨四点半的灯》：12 拍视频号 60s 位·真实锚卡 C-00010 顾阿凤·"
           "charter 门禁消费毕=纪实线三重标注+T1-T9 自检+赛博语体三问+L18-L20 措辞三律·来源清单 13 条字段级指针·"
           "U243 互聊台账 v2 并入位预留)·四议程=①done R504 ②done R503 ③起链毕本行(生产链下轮续) ④随窗提速位·"
           "探针=board 0 FAIL/readiness 3 阻塞皆外部 0 发现/loop_health 2F+21W 全在案定型(lag+1=尾轮自beat 残差·收账即平)")
json.dump(d, io.open(FP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("row0 refreshed; export_ts ->", now)
