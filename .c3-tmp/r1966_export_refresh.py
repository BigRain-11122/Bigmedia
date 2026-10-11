# -*- coding: utf-8 -*-
"""R1966 export refresh: do row + live three rows (E4 backfill 8.0 + B-pool upgrade verdict)."""
import json, subprocess, sys

DO = "SC-005-03 E4回填毕8.0（audio系列四连8.0）·B池升格=何雨欣+陈雅雯两锚升A·生产序=04何雨欣→05陈雅雯→收尾林之恒（编者位）·tech#92判据窗10-12 08:00"
LIVE = [
    "当前活：SC-005 口述史第三件缪一收官=F-174 登记（单轮全链 57 锚零 MISS→S1 10/10→ASR 43 cues→E8 七席 ≥9）；E4 参考分 8.0 回填毕（系列四连 8.0·会看完会转发）·B 池升格=何雨欣/陈雅雯升 A",
    "最近实物：F-174 SC-005-03-v1.mp3《城市口述史·选段三·字幕君缪一》（3:35.9）+评审单 review-20261011-sc00503-v1.md v1.1（2026-10-11 11:3x）",
    "下个里程碑：SC-005-04《主播何雨欣》拍稿随轮领（F-175·窗 ≤48h）+雷达标定判读窗 10-12 08:00（zhihu-hot 头部 ≥3 件 ≥60）",
]
EXPORT = "docs/status-export.json"

with open(EXPORT, encoding="utf-8") as f:
    data = json.load(f)
data["live"] = LIVE
data.pop("export_ts", None)
patch = ".c3-tmp/r1966_export_patch.json"
with open(patch, "w", encoding="utf-8", newline="\n") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

r = subprocess.run([sys.executable, "src/os/export_refresh.py", "--patch", patch, "--do", DO],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.stdout)
print(r.stderr)
sys.exit(r.returncode)
