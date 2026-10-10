# -*- coding: utf-8 -*-
# R1932 accounting close (two-segment, tech#27; finalize_state per tech#76)
import os
import sys

sys.path.insert(0, os.path.join("src", "os"))
import close_commit as cc  # noqa: E402

LOG_LINE = (
    "2026-10-11 02:2x R1932: 等待窗取活轮·tech#81 close 脚本本体件自含律交付"
    "（R1931 种子兑现·CPU 面·两段制收账=交付段先行 commit ccce7077+close_commit 末步内嵌·"
    "本尊 dogfood=本收账自动收录 r1932_close.py）——"
    "①交付=close_commit.py 新 autodetect_close_script（state tick 锚定 "
    ".c3-tmp/r{tick}_close.py 存在即自动入清单·严格锚形律=零 glob 零他件裹挟"
    "〔错轮残留=round-debris 守卫域不越界〕·advisory=缺锚/坏 state 永不 fail close）"
    "+run_close_commit 自含步（已列去重+STEP self-include/NOTE 证据行·dry-run 计划行同携）"
    "·6 新测（纯核 2+真 git 集成 4：r1930 锚形复现锁=close 后 status -uall .c3-tmp 零遗留"
    "+错轮残留不扫+已列去重+dry-run）·853 全回归绿 95.0s SUITE_RC=0（847+6·run_suite 正法）"
    "·C-39 升 v1.85；"
    "②五查全静=own orders O-20260908-1105 mtime==R1733 锚+origin_gap_check QUIET ahead0 behind0"
    "+canonical group_scan（tech#50 正典）truly_new=0 水位 136 维持"
    "（C-20261010-01=D-20261011-01 行内内联引用态复证·R1930/R1931 裁定承继）"
    "+ledger @BigStream 4 行==值守锚+HQ orders 00:27:11==R1928 消费锚零新行+无 index.lock"
    "+树态=MV sprint 会话域在飞件零接触（R1745 承继）；"
    "③GPU C-37 tech#75 判断位照新序律双命令=评审腿 gate --samples 6 GO"
    "（worst-case free 5646≥2048+util_max 2%+band 13 稳态=多轮来最优读数）"
    "+剧本腿 gate NO-GO（5653<9216）+ollama 探针=cold-skip 正确执法"
    "（14b-8k 未驻留+free 5659<9000 包络=零生成飞行零自污 face=not-resident）"
    "→非双 GO=四腿（MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/E4 v13）维持 fire-ready gated"
    "（材料 R1870/R1871/R1875 turnkey·探针行 util 86=他 lane 间歇窗读数·gate GO 窗亦瞬时）；"
    "④查看位四根并读（R1762 律·R1926 锚 23:35 后）=meme-daily-v1 零新到件"
    "（V1 成片 mp4 未落=TTS/装配腿在飞维持）+krea2 30s-reel-v1 零新"
    "（44/44 KF 帧+LOOKBOARD==R1926 锚·全曲批在产）+mv0001-handover/shortvideo-dept/h3-local-test 零新；"
    "⑤三探针=probe_capture 紧凑面在带内（board 0 FAIL〔5 题 10 稿 5 in production〕"
    "/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17 needs-CEO〕0 发现"
    "/loop_health 2F+233W 皆在案史实〔两 outage 已裁定不重触发〕）；"
    "⑥例行件=10-11 日报在案不重跑（R1927 00:2x 一份为真相）·W42 周审 10-12 未到"
    "·GB §④ 下期 10-15 跳过·#112 判据窗 10-11 08:00 未到届日即领不预扫"
    "·export_ts 00:23 <24h 零 CEO 可见变化节流不刷（live 三行核读仍实况准确）"
    "·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）"
    "·tokens:local=0（探针 cold-skip 零生成飞行·纯 CPU 工程+套件跑零本地模型产出调用·P-54⑤ 计量律）；"
    "⑦操作红 1 笔如实入账=轮首五查先手搓 ad-hoc group scan（r1932_group_scan.py）"
    "而未先查正典 src/os/group_scan.py（tech#50 R1880 已交付在册）=反重复律违例"
    "·canonical 探针本轮补跑复核读数一致（truly_new=0 静）收口·ad-hoc 件留档不删（op-red 证据）；"
    "队列补货步=真无新种子如实注记零膨胀（五查静+探针零新发现+查看位零新到件·禁凑数律）"
    "——下轮=R1933 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领"
    "〔城市源非回填 ≥60 ≥2 件+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕"
    "+GPU C-37 fresh 四腿点火判断+meme V1 成片查看位）"
)

FOCUS = (
    "R1933 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领"
    "〔城市源非回填 ≥60 ≥2 件+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕"
    "+GPU C-37 fresh 四腿点火判断〔双 GO 连续 ≥2 方飞〕+meme V1 成片查看位）"
)

FILES = [
    "src/os/state.json",
    "data/pipeline/ollama-probe-ledger.jsonl",
    ".c3-tmp/r1932_group_scan.py",
    ".c3-tmp/r1932_group_scan.txt",
    ".c3-tmp/r1932_group_scan_canonical.txt",
    ".c3-tmp/r1932_gate_rev.json",
    ".c3-tmp/r1932_gate_script.json",
    ".c3-tmp/r1932_probe.json",
    ".c3-tmp/r1932_probes.txt",
    ".c3-tmp/r1932_t81_mod.out",
]

MSG = ("R1932 close: tech#81 delivered, 4 legs gated (probe cold-skip), "
       "five-checks quiet, view-ports zero-new [via bm-a]")

summary = cc.finalize_state(LOG_LINE, focus=FOCUS)
rc, lines = cc.run_close_commit(FILES, MSG)
for line in lines:
    print(line)
print("RC=%d" % rc)
sys.exit(rc)
