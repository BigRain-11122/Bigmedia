# -*- coding: utf-8 -*-
# R723 round-end addendum: S1 verdict backfill + TTS v1 reading + v2 launch + README/update + live refresh.
import json, re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
now = datetime.now()
stamp = now.strftime("%Y-%m-%d %H:%M:%S")
short = now.strftime("%H:%M")

r = json.load(open(ROOT / ".lc014-tmp" / "s1-result.json", encoding="utf-8"))
vf = r.get("verdict_file", "")
vfname = vf.split("\\")[-1] if vf else "s1-verdict"

add = ("2026-09-30 %s R723 轮末补记（异步双落地+裁链中段）：①S1 v1.5+L18-L20 门 **10/10 PASS 零违律一次过**"
    "（wrapper 落地·违律清单「无」+总分 10+总裁决 PASS=**拆条系列十三连满分**·判词档 %s+expert-calls 行 wrapper 自动"
    "+s1-result.json 留档）——S1 判 v1 初稿·后续机械裁不回炉=fleet 先例；②TTS v1 实测 73.121s 超窗（274 字预算外推符合预期）"
    "→v2 机械裁 34 字落盘（卡锚列全行零动+信条零动+事实数字全保〔三下/两小时/三十年零十一个月〕·b2 三逗长句句拆收口=M1 v1 "
    "0F1W 的 WARN 销账+「敲门是礼数」「全城调度急得跳脚」「一间老机房」「睁眼第一件事是」等压缩分载归卡锚列=R709 先例"
    "·零漏诊=city-residents 表行 verbatim·「手写记录」=台账 L18 卡口分工维持）+M1 v2 复检 **0 FAIL 0 WARN**+TTS v2 脱壳在飞"
    "（r723_tts_run.py v2·读数轮间落地=R712→R713 先例）——v2 若仍超窗=v3 续裁（R724 首位）；README 生产记录+门禁块同步本轮 commit。"
    "收账补 commit+push（不卷 bm-a codex 未提交件）。" % (short, vfname))

sp = ROOT / "src" / "os" / "state.json"
raw = sp.read_text(encoding="utf-8")
had_nl = raw.endswith("\n")
st = json.loads(raw)
st["log"].append(add)
st["ts"] = stamp
st["task"] = ("生产轮·E14 LC-014 老晶振起链+S1 10/10 十三连满分+TTS v1 73.12s→v2 裁链在飞+")
sp.write_text(json.dumps(st, ensure_ascii=False, indent=2) + ("\n" if had_nl else ""), encoding="utf-8")

ex = ROOT / "docs" / "status-export.json"
raw2 = ex.read_text(encoding="utf-8")
had_nl2 = raw2.endswith("\n")
se = json.loads(raw2)
se["export_ts"] = stamp + "+08:00"
se["live"] = [
    ["当前活：LC-014 老晶振拆条起链（E14 active·光机魂系首拆位）：S1 v1.5 门 10/10 PASS 十三连满分+M1 v2 0F0W——TTS 空气预算裁链中段（v1 73.12s→v2 在飞→R724 定稿）；E15 朱鸿奎 standby=lane ≥2 达标"],
    ["最近实物：data/sources/lc014/（beats v1/v2 裁稿链+s1-review-material+README）+S1 判词档 %s（10/10 PASS）·2026-09-30 %s" % (vfname, stamp)],
    ["下个里程碑：LC-014 定稿音轨+渲染腿+收官（F 登记→冗余池第十一件·窗 ≤10-02）+#70 OSS 窗 2 切片（≤10-02 21:40）+global-benchmarks 7 日刷（10-01=#80 并窗）"],
]
ex.write_text(json.dumps(se, ensure_ascii=False, indent=1) + ("\n" if had_nl2 else ""), encoding="utf-8")

rp = ROOT / "data" / "sources" / "lc014" / "README.md"
t = rp.read_text(encoding="utf-8")
t = t.replace("- S1 v1.5+L18-L20 门 wrapper 脱壳起飞（04:3x·1500s 窗·s1-result.json 轮间异步落地=R712→R713 先例）；TTS light v1 起飞（.c3-tmp/r723_tts_run.py v1·--template=.lc013-tmp/cards.json 链式承继·BGM-A 纯净）——**空气预算机械裁链（v1 实测读数→裁→定稿）+S1 首读=R724 首位**。",
    "- S1 v1.5+L18-L20 门 **10/10 PASS 零违律一次过**（轮末落地·违律清单「无」+总裁决 PASS=**拆条系列十三连满分**·判词档 %s+expert-calls 行 wrapper 自动+s1-result.json 留档）。\n- TTS v1 实测 73.121s 超窗（274 字）→**v2 机械裁 34 字**（卡锚列零动+信条零动+事实数字全保·b2 句拆收口=1W 销账·压缩分载归卡锚列 R709 先例·零漏诊=city-residents 表行 verbatim）+M1 v2 复检 0F0W+TTS v2 在飞——**v2 读数→（如需）v3 续裁→定稿音轨=R724 首位**。" % vfname)
t = t.replace("- S1=in flight（wrapper 异步·R724 首读）·M1 v1=0F1W（b2 句拆收口随 v2）·空气预算=v1 in flight（274 字预算 ~65-70s 超窗预期→机械裁链入 30-60s 窗·fleet 带内目标）。发布锁=M5 账号物理件不变（未上线=未测量）。",
    "- S1=10/10 PASS（十三连满分）·M1 v1 0F1W→v2 0F0W·空气预算=v1 73.121s→v2 in flight（R724 定稿·fleet 带内目标 30-60s）。发布锁=M5 账号物理件不变（未上线=未测量）。")
rp.write_text(t, encoding="utf-8")

print("OK addendum appended; verdict=%s" % vfname)
