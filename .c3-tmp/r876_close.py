# -*- coding: utf-8 -*-
# R876 closeout fix+focus: waiting-state declaration round, window 4/6 (no commit per
# os-protocol S6; batch commit at R878 or 10-02 00:00 day-crossing, whichever first).
# Five-checks quiet at 18:12 (r807_scan.txt rerun), probes match baseline (board 0 FAIL /
# readiness 3 external blockers 0 findings / loop_health 3F+107W all in-case historical,
# no new WARN vs R875). Export NOT refreshed: export_ts 17:31:58 < 24h, zero state change.
# This script repairs the manual-edit JSON break (R875 line missing trailing comma -> fixed
# via text edit), then updates the focus field via json round-trip (r875_close lineage)
# and copies the scan evidence r876_scan.txt.
import io, json, shutil, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
shutil.copy(ROOT + r"\.c3-tmp\r807_scan.txt", ROOT + r"\.c3-tmp\r876_scan.txt")

focus = ("R876: 等待态声明收轮·声明轮并窗第 4 轮（五查全静=r807_scan 18:12 留档 r876_scan.txt：orders 42=锚零新令/ledger_scan_hits 46=基线带内 r845_regression caught=True/decisions dnum 差集 NONE=117 基线/production=open 自愈核 tick875/无 index.lock·树态 3 M 成员维持）+三探针=board 0 FAIL/readiness 3 外部阻塞 0 发现/loop_health 3 FAIL+107 WARN 皆在案史实类（account-lag 在轮 beat 瞬态 tick876 收账缺口收窄）——四查尽（R875 同判承接：①REACT 10-02 热点窗②#70 OSS 窗 3=10-02 21:40③补池复活四路 0/4〔C-00030 锚缺/新令级事件缺/REACT 10-02 未开/新批注缺〕④W41 周轮件=10-05·queue B5 账号期门控+E-pool 空池豁免在案）=真无活可拉〔P-20260928-02 ②④序·供给侧全闭+全时闸=保护态豁免面在案〕——waiting: supply-gated lane held（卡点=新锚卡 C-00030+/新令级事件/REACT 10-02 窗/#70 窗 3 10-02 21:40/W41 10-05）ETA 2026-10-02。〔并窗 4/6 不 commit·窗满 R878 或跨日 10-02 00:00 即 batch commit 区间 R873-首触轮〕下轮 R877 可领序（同判维持·实况变化即转全任务书）：①REACT 10-02 热点窗届日领〔10-02 日报缺=先补产 daily_brief·#59〕②#70 OSS 窗 3 切片〔10-02 21:40 后开·≤3 刀〕③五面恢复任两路=补池复活④W41 周轮件〔10-05〕——五查锚=orders 42·ledger_scan_hits 46·decisions_watermark dnum 基线 117 项·供给面=CENSUS C-00030 缺/DIGEST 通道存量清空〔E28/E29 出池〕/REACT 10-02/OSS w3 10-02 21:40/W41 10-05")

sp = ROOT + r"\src\os\state.json"
st = json.loads(io.open(sp, encoding="utf-8-sig").read())
assert st["tick"] == 876, "tick expected 876, got %s" % st["tick"]
assert st["log"][-1].startswith("2026-10-01 18:13 R876:"), "log tail prefix"
assert "R876" in st["log"][-1], "R876 tag in log tail"
assert st["log"][-1].rstrip().endswith("④W41 周轮件〔10-05〕"), "log tail end shape"
assert st["ts"].startswith("2026-10-01 18:1"), "ts shape"
st["focus"] = focus
io.open(sp, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=1))

# verify round-trip
st2 = json.loads(io.open(sp, encoding="utf-8-sig").read())
assert st2["tick"] == 876
assert st2["production"] == "open"
assert "R876" in st2["log"][-1]
assert "R877" in st2["focus"], "R877 next-round pointer in focus"
assert st2["log"][-2].startswith("2026-10-01 18:04 R875:"), "R875 line intact"
print("R876 close ok tick=%d log=%d ts=%s task=%s..." % (st2["tick"], len(st2["log"]), st2["ts"], st2["task"][:24]))
