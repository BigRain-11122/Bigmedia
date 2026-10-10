# -*- coding: utf-8 -*-
"""R1945 accounting close (tech#76 single writer + tech#65 embedded commit).

Round face: waiting-window P2 production leg -- tech#90 delivery (fire
card readings collected_at / age face, R1944 seed cashed; verdict face
zero drift; 7 new tests, 966 suite green; dogfood real-run gate 40-42s
oldest reading vs 120s TTL archived).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(REPO, "src", "os"))

from close_commit import finalize_state, run_close_commit  # noqa: E402

LOG_LINE = (
    "2026-10-11 06:2x R1945: 等待窗 P2 生产轮·tech#90 交付（fire 卡读数采"
    "集时刻戳面·R1944 种子兑现·判定面零动·两段制收账=close 脚本内嵌）——"
    "①轮首五查全静=own orders 顶 O-20260908-1105 mtime 12:08:14==R1733 锚零"
    "新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan"
    "（tech#50 正典）truly_new=0 水位 137 维持+wm_only=1（C-20261010-01 行内"
    "引用族）+ledger @BigStream 4 行==值守锚零新转办+HQ orders mtime 02:06:"
    "39==R1935 消费锚零新行+无 index.lock+树态=mv0001/mv001/whisper v3/"
    "drama_takt MV sprint 会话批域在飞件零接触（R1745 承继·tech#26 撞面维"
    "持）；②fire_window_card 单命令四腿判断=双跑 no-fire（06:04 卡：gate "
    "静态双闸败 worst-case free 561<2048+band 10047 振荡域 advisory="
    "resident-hot 态族 R1942 承继·mv quiet 388min+probe face=ok GEN-OK 静"
    "态闸关死；06:10 dogfood 跑同判）→SC-004-01 收官腿（E4+E8→F-171）+"
    "MD-0002 剧本腿维持 fire-ready gated（材料 R1870/R1871/R1875 "
    "turnkey）；③meme V1 查看位零新到件（outbound 顶=narration.mp3 15:41:"
    "53==R1899 锚·成片 mp4 未落=TTS/装配腿在飞维持）+krea2 查看位禁重扫"
    "（44/44 KF+LOOKBOARD==R1926 锚）；④tech#90 交付=fire_window_card 读数"
    "采集时刻戳面：orchestrate 增 clock 注入缝+四读数〔gate→mv→probe→"
    "credit 条件〕采集前打 collected_at+slim 读数各加 collected_at/"
    "age_s_at_verdict 两列+卡级 oldest_reading_age_s 键+human render "
    "readings-age 行（oldest=Ns vs fire TTL 120s 消费指引）——R1944 锚定"
    "「序贯采集下最老读数判定时刻已 ~40-70s 陈旧·TTL 消费窗被无声吃掉」读"
    "数侧盲区收口·判定面/classify_fire/rc 契约/既有 slim 字段字节零漂移；"
    "7 新测（ReadingsTimestampTests：路径 B 年龄代数 40/30/20/10 确定性锁+"
    "路径 A 无 credit 支+collected_at 格式锁+now 覆写向后兼容+human 行双态+"
    "no-fire 路径照带年龄列）·966 全回归绿 123.6s SUITE_RC=0（959+7·"
    "run_suite 正法）·判据达成=真跑 dogfood 双跑读数入档可读（gate "
    "collected_at 06:10:05/age_s_at_verdict 40-42s=最老读数 vs TTL 120s·"
    "mv/probe 14-16s·证据 .c3-tmp/r1945_fire_card.txt+.json）；台账=C-42 表"
    "行增面+changelog v1.92+tech#90 done 标；⑤三探针=board 0 FAIL（5 题 10 "
    "稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE "
    "6/10+#17 needs-CEO）0 发现/loop_health 2F+238W 皆在案史实（两 outage="
    "09-26/09-28 已裁定不重触发·drift 17==adjudicated 基线带内）·证据 ."
    "c3-tmp/r1945_probes.txt；⑥例行件=10-11 日报在案不重跑（R1927 00:2x 一"
    "份为真相）·W42 周审 10-12 未到·GB §④ v1.3 下期 10-15 跳过·export_ts "
    "04:35:31 <24h 零 CEO 可见成品态变化节流不刷（tech#90=内部工具件·live "
    "三行核读=SC-004-01 收官链+08:00 雷达窗实况仍准确）·#99 "
    "blocked-on-channel 维持（SLA ≤10-13）·HQ-FEEDBACK 不写（零集团层新 "
    "open 问题零膨胀）·tokens:local=0（fire 卡内探针生成调用=探针件非评审"
    "调用 R1888 口径·纯 CPU 工程+套件跑零本地模型产出调用·P-54⑤ 计量律）；"
    "⑦队列补货步=真无新种子如实注记零膨胀（本轮真发现〔读数陈旧度 40-42s "
    "量化〕已消费进 tech#90 交付面本身=发现即机制·禁凑数律）·临时件=r1945 "
    "探针+dogfood 证据件入账收口（tech#81 自含律）——下轮=R1946 快速路径首"
    "查（10-11 08:00 #112 城市口径判据窗届日即领〔城市源非回填 ≥60 ≥2 件+"
    "tech#53 双新源流量首报+tech#5/#30/#49 判定位〕+fire_window_card 四腿"
    "点火判断〔读数新鲜度面已就位〕+meme V1 成片查看位）"
)

FOCUS = (
    "R1946 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领〔城市源"
    "非回填 ≥60 ≥2 件+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕+"
    "fire_window_card 单命令四腿点火判断〔SC-004-01 收官腿 E4+E8→F-171+"
    "MD-0002 剧本腿·读数新鲜度面就位〕+meme V1 成片查看位）"
)

FILES = [
    "src/os/state.json",
    "src/os/fire_window_card.py",
    "tests/test_fire_window_card.py",
    "docs/capabilities.md",
    "state/queue/tech.md",
    ".c3-tmp/r1945_probes.txt",
    ".c3-tmp/r1945_fire_card.txt",
    ".c3-tmp/r1945_fire_card.json",
]

MESSAGE = (
    "R1945 tech#90 fire card readings collected_at/age face (clock seam, "
    "slim 2 cols + oldest_reading_age_s, human readings-age line, verdict "
    "face zero drift; 7 tests, 966 suite green; dogfood gate 40-42s oldest "
    "vs 120s TTL archived) [via bm-a]"
)


def main():
    summary = finalize_state(log_line=LOG_LINE, focus=FOCUS)
    print("FINALIZE tick=%s ts=%s task=%s wm_added=%s log_len=%s"
          % (summary["tick"], summary["ts"], summary["task"],
             summary["wm_added"], summary["log_len"]))
    rc, lines = run_close_commit(FILES, MESSAGE)
    for line in lines:
        print(line)
    print("CLOSE_RC=%s" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
