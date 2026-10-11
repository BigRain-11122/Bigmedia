# -*- coding: utf-8 -*-
"""R1959 close: waiting-window round - tech#95 toonflow cleanup leg + explore#23 gate annotation.

Two-stage commit per os-protocol 6 v1.12 (tech#27):
  stage 1 = deliverables commit (plan + queue annotations)
  stage 2 = state accounting + export refresh + close commit (self-include via tech#81)
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src", "os"))
import close_commit  # noqa: E402
import export_refresh  # noqa: E402

STAGE1_MSG = (
    "R1959 deliverables: tech#95 toonflow leg done - 79MB installers + empty dl logs purged, "
    "data/assets/toonflow/ removed, deployed app re-verified intact (rebuild channel = R1767 "
    "sha256 baseline on file); disk plan II.2 annotated executed; explore#23 gate-opened "
    "annotation (SC-004 F-171 registered R1948 = claimable queue head); queue replenish = "
    "zero-inflation honest note [via bm-a]"
)

LOG = (
    "2026-10-11 09:5x R1959: 等待窗取活轮·tech#95 toonflow 微清腿收官（盘计划 §二.2 候选位"
    "「随下轮清」本轮兑现）——①轮首五查全静：origin_gap QUIET（ahead0 behind0）+own orders 顶="
    "O-20260908-1105 陈锚+group_scan truly_new=0（watermark=137·wm_only=C-20261010-01 瘦水族）"
    "+ledger @BigStream 5 行=R1957 已消费承继+树净零锁（MV 会话在飞件=白名单域预期态）；②三探针绿："
    "board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health "
    "2 FAIL 皆在案史实（09-26/09-28 outage 家族）；③取活=P2 tech#95 toonflow 腿（bonsai 6.1GB "
    "半面维持 owner-confirm open）：双 setup exe 38.8+40.2MB+双 0 字节下载日志全清·data/assets/"
    "toonflow/ 目录移除=-79MB 实得·部署面 C:\\Users\\sjs20\\tools\\ToonFlow\\ 便携件复验在场零影响"
    "（#110 桌面 PoC 继续可用）·盘计划 §二.2 行标已执行+tech#95 toonflow 腿 done 标；④explore#23 "
    "gate-opened 注记：SC-004-01 台风梅花有声纪实 R1948 收官（F-171 登记）=「候选 A 走通」判据"
    "达成→census 人物志番外系列化预研转可即领队头位（16 锚 C-00012~15+C-00018~29 共 61017B "
    "BigLife census/anchors/ 实测·跨仓只读·选型件=下轮领）；⑤例行件全静：日报 2026-10-11 在案+"
    "W41 周审在案+global-benchmarks 10-08 刷新 ≤7 天跳过（下期 10-15）+radar 标定权威判读窗 "
    "10-12 08:00 未到禁重扫+HQ-FEEDBACK 不写（无集团层新 open 问题）；⑥队列补货步=零膨胀如实注记："
    "本轮无真新种子（tech#92-95 盘点面全 gated/owner 面·explore#23 注=既有项状态变化非新项·"
    "禁凑数律照守）。下轮=explore#23 census 番外选型件（可即领队头位）或 10-12 08:00 雷达标定判读"
    "（到点·zhihu-hot 头部 ≥3 件 ≥60=PASS·FAIL=阈值分层腿递补）·MD-0002 T2I 维持 gated CEO 点头。"
    "收账显式列文件 commit+push。"
)

FOCUS = (
    "R1959 explore#23 census 人物志番外选型件=可即领队头位（gate-opened·16 锚跨仓只读）·radar "
    "标定权威判读窗 10-12 08:00（zhihu-hot 头部 ≥3 件 ≥60=PASS·FAIL=阈值分层腿递补）·MD-0002 T2I "
    "维持 gated CEO 点头·tech#95 余面=bonsai 6.1GB owner-confirm open"
)

DELIVERABLES = [
    "docs/disk-reduction-plan-20261011.md",
    "state/queue/tech.md",
    "state/queue/explore.md",
]

# stale-numeric fix round: chips/depts/results derive (F-170/F-169 era counts -> current truth)
PATCH = {
    "do": "等待窗取活：旧安装包清理 79MB 完成；雷达日报评分标定明晨出结果；MV 全曲成品线在跑（查看位）。",
    "live": [
        "当前活：清理旧安装包回收 79MB；等明早八点雷达日报评分结果",
        "最近实物：磁盘减负两项执行（9.2GB 模型源件+79MB 安装包），2026-10-11 09:5x",
        "下个里程碑：雷达日报评分标定判读，10-12 08:00",
    ],
    "chips": [
        ["量产开闸", "live"],
        ["OS 自治", "live"],
        ["成品 171", "live"],
        ["L-卡四形态", "live"],
        ["S2 三门", "live"],
        ["977 测绿", "live"],
        ["专家评审团", "live"],
        ["雷达快照", "live"],
        ["meme 产线", "wip"],
        ["MV 全曲", "wip"],
        ["MD-0002", "wip"],
        ["账号", "wip"],
        ["发布锁", "wip"],
    ],
    "depts": [
        {"n": "总裁办公室", "t": "量产开闸运转（D-BS-06）；OS 循环 1959 轮自治；集团转办零积压；决策件全自决闭环（O-2126 委托决策令）", "s": 1},
        {"n": "品牌文化部", "t": "声线 light 定档+机器叙述者=城市自述视角；四代同声线对照链在册（D-BS-07）", "s": 1},
        {"n": "选题研究部", "t": "情报日报在案；硅基城市四供给源（编年史/文化/居民/台词池）保鲜；雷达日报产品线运维位", "s": 1},
        {"n": "内容生产部", "t": "成品库 171 件；L-卡四形态 QUOTE/DIGEST/CENSUS/REACT 全 live；漫剧 MD-0001 在库·MD-0002 gated", "s": 1},
        {"n": "平台运营部", "t": "账号批次① 未开（CEO 物理件·现状行不催办）；M5 发布锁；三线首发阵地=公众号", "s": 2},
        {"n": "合规审查部", "t": "M4 门机制全绿；三重标注多载体核验过；REACT/CENSUS 形态合规结构在册；AIGC 显著标识红线在役", "s": 1},
        {"n": "数据分析部", "t": "周报/周自审 live；CLOUD_LINE 计量在册；未上线=未测量", "s": 2},
        {"n": "工程技术部", "t": "977 测试全绿（124s）；S2 三门机检+守卫面族 20+ 在役；收账链内嵌+export 正典写入器+chips/depts 胞形守卫", "s": 1},
    ],
    "outs": [
        ["雷达日报评分标定判读（10-12 08:00 权威窗·锚例版已上线）", "wait", "radar"],
        ["MV 全曲成品线在跑（MV 会话域·循环查看位零接触）", "on", "mv0001"],
        ["MD-0002 配音+装配预置毕·T2I 待 CEO 点头", "wait", "drama"],
        ["meme V1《慢慢踩》生产在飞（设计闸 CERTIFIED）", "wait", "meme-v1"],
        ["AIHOT 双新源换装（B站科技/知识端点·流量真实）", "on", "intel"],
        ["census 人物志番外选型件（explore#23 队头位·gate-opened）", "on", "l-audio"],
        ["磁盘减负执行（9.2GB+79MB 已清·bonsai 6.1GB 待 owner 确认）", "on", "ops"],
        ["REACT/CENSUS 图鉴系列量产线（供给门照守）", "on", "l-card"],
        ["W42 周审件窗（10-12 起周内）", "on", "weekly"],
    ],
    "results": [
        ["171", "成品库总数"],
        ["977", "测试全绿"],
        ["1959", "OS 轮次"],
        ["4/10", "M4 门进度"],
    ],
}

EXPORT_PATH = os.path.join(ROOT, "docs", "status-export.json")


def main():
    # stage 1: deliverables commit first (two-stage law)
    close_commit.run_close_commit(files=DELIVERABLES, message=STAGE1_MSG, root=ROOT, push=True)

    # stage 2: state accounting (tick 1958 -> 1959, ts/task refresh, log append)
    close_commit.finalize_state(LOG, focus=FOCUS)

    # export refresh via canonical writer (contract self-check inside; refuse-write on violation)
    rc, lines, violations = export_refresh.refresh_export(EXPORT_PATH, patch=PATCH)
    for line in lines:
        print(line)
    if rc != 0:
        print("EXPORT_REFRESH_RC=%d violations=%s" % (rc, violations))
        raise SystemExit(rc)

    # stage 2 commit: state + export (self-include law auto-adds this script)
    close_commit.run_close_commit(
        files=["src/os/state.json", "docs/status-export.json"],
        message=(
            "R1959 close: waiting-window take - probes green (board 0F / readiness external-only "
            "/ loop_health historical), five checks quiet (origin-gap QUIET, group-scan "
            "truly_new=0); next: explore#23 census spin-off selection (queue head) OR 10-12 "
            "08:00 radar score calibration verdict [via bm-a]"
        ),
        root=ROOT,
        push=True,
    )


if __name__ == "__main__":
    main()
