# -*- coding: utf-8 -*-
"""R753 closeout fix: S1 verdict landed in-round (10/10) - sync log/task/export."""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

st_path = REPO / "src" / "os" / "state.json"
st = json.loads(st_path.read_text(encoding="utf-8"))
row = st["log"][-1]
row = row.replace(
    "E21 沈佩兰 LC-021 起链三腿毕（渲染腿素材探针先行抓真发现",
    "E21 沈佩兰 LC-021 起链四腿毕（S1 二十连满分轮内落地·渲染腿素材探针先行抓真发现")
row = row.replace(
    "起链三腿毕：拍稿 v1 12 拍 ≈336 字",
    "起链四腿毕：拍稿 v1 12 拍 ≈336 字")
row = row.replace(
    "+S1 v1.5+L18-L20 门 1500s wrapper 脱壳起飞（.lc021-tmp/s1_call.py·r753_s1_launch.ps1 绝对路径启动器=R728 律·判读轮间落地=R712→R713 先例）",
    "+S1 v1.5+L18-L20 门 **10/10 PASS 零违律一次过=拆条系列二十连满分**（1500s wrapper 脱壳 14:17:29 落判热载快落·三段格式全落位〔R735 材料尾格式锚生效第五连〕：总分 10+违律清单「无」+总裁决「PASS·稿件严格遵循母源设定，无新增人格信息，无违律行为」·判词档 20260930-141729-S1-script+expert-calls 行 wrapper 自动+s1-result.json 留档）")
row = row.replace(
    "·tokens:local=0（M1+探针纯脚本零本地模型调用·S1 qwen 在飞未落=落地轮记账·P-54⑤ 计量律）",
    "·tokens:local=1（S1 qwen2.5:14b 本轮落地记账·本地 Ollama 零 API token·P-54⑤ 计量律如实记）")
row = row.replace(
    "下轮=R754 可领序：①LC-021 S1 判读回填+空气预算裁链",
    "下轮=R754 可领序：①LC-021 空气预算裁链")
st["log"][-1] = row
# task: strip timestamp prefix AND round marker, first 60 chars (R752 convention)
stamp = row.split(" ", 1)[0] + " " + row.split(" ", 2)[1]  # "2026-09-30 HH:MM"
body = row[len(stamp) + 1:]
if body.startswith("R753: "):
    body = body[len("R753: "):]
st["task"] = body[:60]
st["focus"] = st["focus"].replace(
    "①LC-021 沈佩兰渲染链续做（S1 判读回填〔wrapper R753 14:3x 起飞·轮间落地〕→空气预算机械裁链",
    "①LC-021 沈佩兰渲染链续做（S1 10/10 二十连满分已落地 R753〔判词档 20260930-141729〕→空气预算机械裁链")
st_path.write_text(json.dumps(st, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

ex_path = REPO / "docs" / "status-export.json"
ex = json.loads(ex_path.read_text(encoding="utf-8"))
ex["results"][0][1] = row
ex["outs"][0][1] = ex["outs"][0][1].replace(
    "LC-021 起链三腿毕（拍稿 v1 336 字+M1 0F2W+S1 门在飞）",
    "LC-021 起链四腿毕（拍稿 v1 336 字+M1 0F2W+S1 10/10 二十连满分轮内落地）")
ex["live"][0] = ["当前活：R753 E20 同锚重复判负修正+E21 沈佩兰 LC-021 起链四腿毕（拍稿 v1 336 字+M1 0F2W+S1 10/10 二十连满分 14:17:29 轮内落地）·下轮=LC-021 空气预算裁链+TTS 定稿音轨→渲染腿"]
ex_path.write_text(json.dumps(ex, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("FIXED task=%s" % st["task"])
