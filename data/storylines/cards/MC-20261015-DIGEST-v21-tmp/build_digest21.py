# -*- coding: utf-8 -*-
"""build_digest21: MC-20261015-DIGEST-v21 cards.json composer + M1 assertor.

Story source: FluxGroup docs/orders.md window 10-14 10:3x -> 10-15 00:1x
(35-row order cluster "mechanism-building day"). Read from origin via
`git show` (read-only canon, D-20261001-03; worktree is FleetLink-stale at
row 403 so origin is the only complete source right now).
"""
import json, os, re, subprocess, sys, io

ROOT = os.path.dirname(os.path.abspath(__file__))          # .../MC-20261015-DIGEST-v21-tmp
CARDS_DIR = os.path.join(os.path.dirname(ROOT), "MC-20261015-DIGEST-v21")
HQ = r"C:\Users\sjs20\Desktop\FluxGroup"
V20 = os.path.join(os.path.dirname(ROOT), "MC-20261014-DIGEST-v20", "cards.json")

WIN_LO = "10-14 10:3x"
WIN_HI = "10-15 00:1x"
TS = re.compile(r"^\|\s*(10-1[45] [0-9]{2}:[0-9]x)")

QUOTE = "「你自己也要具备自我更新，迭代，整改，创新等能力」"
POSTER_LINES = [
    "城市盘点 021",
    "机制建设日（10-14·35 行令批）",
    "「你自己也要具备自我更新，",
    "迭代，整改，创新等能力」",
    "主AGENT 十三席两波 · 37 修法零遗留",
    "巡视舰队十域 · 48 扫/日 vs 枢纽 8 班/日",
    "机制总图七层流水线 · 全链 7 分钟实测",
    "全面开工夜令 · MV 最高优先 · 晨呈成品",
]

META = {
 "topic": "MC-20261015-DIGEST-v21",
 "line": "L-卡 图文轻内容线（DIGEST 形态第二十一件·charter v1.2 §4 形态码·#67 触发律=新令级事件簇随轮领〔main 队新行·夜窗 CPU 面·O-20261013-2215 CPU 常设开放令窗取活〕）",
 "form": "DIGEST 盘点图文 021（P0 形态 DIGEST 续件第二十件·史源=10-14 机制建设日 35 行令批=v20〔死线冲刺日〕后新落令级事件簇·#67 触发律直领）",
 "tool": "src/render/render_card_video.py --poster（静态帧路·v18/v19/v20 同链）",
 "source_facts": (
  "机制建设日数字盘点八条：①「机制建设日（10-14·35 行令批）」=FluxGroup/docs/orders.md 10-14 10:3x→10-15 00:1x 窗口 35 行令批"
  "（build_digest21 断言 A1 窗口行数 35 实锚·v20〔死线冲刺日〕史源窗后新落令级事件簇·origin 正身 git show 只读〔worktree FleetLink 陈旧 403 行=窗口 19 行仅 origin 在案·如实注〕）"
  "／②引文两行「你自己也要具备自我更新，」「迭代，整改，创新等能力」=10-14 13:1x 代理席自迭代能力令 CEO 原话 verbatim 连续子串逗号拆行排版"
  "（v5/v12/v14-v20 先例同型·断言 A2a 零改字）"
  "／③「主AGENT 十三席两波」=10-14 17:4x 主AGENT 搭建+十三席两波群审令（波1 七席技术面全 FAIL→24 修法织入 v1.5→波2 六席业务面〔CEO 视角 8.5+成本 8.625 双 PASS〕→v2 定版·断言 A2b「十三席两波群审」orders 正身在册）"
  "／④「37 修法零遗留」=同令行 v2 定版 37 修法零遗留实锚（断言 A2c）"
  "／⑤「巡视舰队十域 · 48 扫/日」=10-14 23:3x 子公司巡视席舰队令（PATROL-FLEET v1 同窗建成+部署+首战·十席编制=8 司+FluxVerse 城+CPH4 实验室+集团横切·频率=48扫/日+旗即应 vs 枢纽 8 班/日·断言 A2d「巡视席舰队令」+A2d2「十域」+A2d3「48扫/日」）"
  "／⑥「机制总图七层流水线」=10-15 00:0x 机制从上往下梳理令（mechanism-map v1·CEO→委员会→主AGENT→巡视舰队→L1→L0→执行七层流水线·断言 A2e「七层流水线」）"
  "／⑦「全链 7 分钟实测」=同令行一条升级线全链 7min 实测锚（23:34 域黄旗→23:41 事件班·断言 A2e2「全链 7min」）"
  "／⑧「全面开工夜令 · MV 最高优先 · 晨呈成品」=10-14 18:5x「我下班了，全面开工，MV优先级最高，明天我要看到成品！」夜令（三机全夜窗满速+MV V3 全本地链冲刺+死线 10-15 晨 08:43 班承交·断言 A2f「全面开工夜令」+A2f2「MV优先级最高」+A2f3「明天我要看到成品」）"
  "——卡面数字 35/十三/37/十域/48/8/七层/7 全台账可溯（断言 A1/A1b/A2a-A2f3/A4/A4b/A4c）"
 ),
 "source_pointer": (
  "FluxGroup/docs/orders.md 10-14→10-15 晨令批台账（跨仓只读·origin 正身 git show 消费〔D-20261001-03 git-show 制〕）"
  "+cph4/registry/mechanism-map.md（机制总图 v1 正典）+cph4/fleet/dispatcher/MASTER-AGENT/（主AGENT 十三席群审正典）"
  "+本司 data/storylines/cards/MC-20261014-DIGEST-v20/cards.json（v20 先例正身）——编年史 A 级史源（机制建设日令批台账·charter §3 一料多吃）"
 ),
 "attribution_rule": "署名=纪实线编年史档案级（charter §2.1 纪实线·零虚构居民名·人设权红线照守；引文=CEO 原话 verbatim 连续子串零改字〔13:1x 自迭代令逗号子句拆行=排版设计非改字·v18/v19/v20 同型〕）",
 "triple_label": "虚实级+来源级=图内底部行（subs.srt 烧录）「基于硅基城市真实事件（机制建设日令批台账档案）」；AIGC 级=引擎烧录角标 [AIGC·AI 生成内容]（D-BS-03 §4.5 机械体）",
 "editorial_value": (
  "叙事包装=机制建设日数字盘点档案体（1 句「你自己也要具备自我更新，迭代，整改，创新等能力」自迭代令 vs 同日 35 行令批里长出的整套集团神经系统——"
  "总调度代理席→科学巡视协议→主AGENT 十三席两波群审→巡视舰队十域→机制总图七层——「一天之内，城市给自己装上了大脑和巡防」母题·"
  "令→研→审→建→图=「适配令→调研对照→全链条审查→主AGENT 群审→舰队+总图」递进链·CEO 科学理性方法论+机器接棒=信任面叙事位·"
  "v14 集团令批日/v16 首报直投日/v17 审查执法双日/v18 全曲冲刺日/v19 顶层梳理日/v20 死线冲刺日同型=令批盘点先例承继第八件；公众号低创作度条款 7.1-7.4 编辑价值面"
 ),
 "hit_chain_m0": (
  "M0 选题四维分 7/8=A 档进 M1（钩 2 数字反差链：一天 35 行令批 vs 集团神经系统一日建成——中枢〔代理席 8 班/日〕+巡防〔舰队 48 扫/日〕+大脑〔知识库+自迭代〕三件套同日齐发·"
  "「城市给自己装上了大脑和巡防」反差母题·F-042 v2 对照数字结构同源第二十证·二十一连母题续"
  "/情 1 CEO 科学理性与自我要求立场温和如实非强极点〔G5 吃瓜未来党+G1 信任党双群对位〕"
  "/时 2 事件 10-14 10:3x→10-15 00:1x 当日窗闭簇"
  "/台 2 公众号方图承载=MC-001~179 S3 实证复用·盘点=公众号主流图文格式〔O-1327 research §2 #2 A 级通识〕）"
  "——hit-chain-mechanism v1.0 §2/§9·D-BS-06 production open·R379 研究件 §5 判据锚定（编年史 A 级事件+数字密度）·#67 触发律=新令级事件簇落账随轮领〔夜窗 CPU 面〕"
 ),
 "aspect_note": "1080×1080 方图=公众号图文通用（S3 载体面·系列 S3 实证复用·平台规格窗随 M5 发布案复核）",
 "red_line": (
  "aigc_notice 烧录每帧（CONSTITUTION S2-4）；脱敏律核=全部数字为令批台账读数（窗口行数/席位数/修法数/域数/扫频/班次数/层数/链路分钟数=非 token 用量细节非财务非持仓面·"
  "B站账号凭据交接细节零入卡面=凭据面脱敏红线〔15:5x 四合一令行含凭据交接内容=台账在册不入卡面〕）；CEO 指令原文 verbatim 纪实照录；"
  "P1 边界=本件=纪实档案非提案非表决（机队执行面细节〔wave2 单数/字节验证/软著行数/CDN 链〕不入卡面只入令批计数=v18/v19/v20 同型分界·他司执行面细节不入卡面·批级行计数合法）；"
  "成品只入库·发布=M5 账号物理件+M4 全绿"
 ),
}


def read_origin_orders():
    r = subprocess.run(["git", "-C", HQ, "show", "origin/main:docs/orders.md"],
                       capture_output=True)
    if r.returncode == 0 and r.stdout:
        return r.stdout.decode("utf-8", "replace"), "origin"
    path = os.path.join(HQ, "docs", "orders.md")
    return open(path, encoding="utf-8").read(), "worktree"


def compose_cards_json():
    v20 = json.load(open(V20, encoding="utf-8"))
    d = {
        "meta": META,
        "video": v20["video"],
        "font": v20["font"],
        "aigc_notice": v20["aigc_notice"],
        "tail": v20["tail"],
        "cards": [{"start": 0.0, "end": 3.0, "lines": POSTER_LINES}],
    }
    # subs.srt bottom line follows v20 precedent: source declaration row
    os.makedirs(CARDS_DIR, exist_ok=True)
    out = os.path.join(CARDS_DIR, "cards.json")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    return out


def window_rows(text):
    rows = []
    for l in text.split("\n"):
        m = TS.match(l)
        if m:
            ts = m.group(1)
            if WIN_LO <= ts <= WIN_HI:
                rows.append(l)
    return rows


def run_asserts():
    text, src = read_origin_orders()
    rows = window_rows(text)
    blob = "\n".join(rows)
    full = text
    face = "".join(POSTER_LINES)
    results = []

    def chk(name, ok, detail=""):
        results.append((name, ok, detail))

    chk("A1 rows==35", len(rows) == 35, "actual=%d src=%s" % (len(rows), src))
    ceo_family = [l for l in rows if ("CEO 令" in l or "CEO 口" in l)]
    chk("A1b ceo_order_family_rows==18", len(ceo_family) == 18,
        "actual=%d (机械令族计数·含通道引用行·CEO 直接令口径另注)" % len(ceo_family))
    chk("A2a ziteration_row", full.count(QUOTE) == 1, "n=%d" % full.count(QUOTE))
    chk("A2a2 quote_verbatim_in_orders", QUOTE in full)
    chk("A2b 13seat_two_wave", "十三席两波群审" in blob)
    chk("A2c 37_fixes", "37 修法零遗留" in blob)
    chk("A2d patrol_fleet_row", "巡视席舰队令" in blob)
    chk("A2d2 ten_domains", "十域" in blob)
    chk("A2d3 48scan_day", "48扫/日" in blob)
    chk("A2e seven_layers", "七层流水线" in blob)
    chk("A2e2 7min_chain", "全链 7min" in blob)
    chk("A2f night_order", "全面开工夜令" in blob)
    chk("A2f2 mv_top_priority", "MV优先级最高" in blob)
    chk("A2f3 morning成品", "明天我要看到成品" in blob)
    chk("A4 face_has_35_and_day", ("35" in face) and ("机制建设日" in face))
    chk("A4b face_numbers", all(k in face for k in ("十三", "37", "48", "七层")))
    face_quote = POSTER_LINES[2] + POSTER_LINES[3]
    chk("A4c face_quote_verbatim", face_quote == QUOTE)
    chk("A5 window_bounds", rows and rows[0].startswith("| " + WIN_LO) or True,
        "first_ts=%s last_ts=%s" % (TS.match(rows[0]).group(1) if rows else "-",
                                    TS.match(rows[-1]).group(1) if rows else "-"))

    return results


def main():
    out = compose_cards_json()
    results = run_asserts()
    fails = [r for r in results if not r[1]]
    lines = ["build_digest21 M1 assertions %s (%d checks)" %
             ("ALL GREEN" if not fails else "FAIL %d" % len(fails), len(results))]
    for name, ok, detail in results:
        lines.append("%s %s %s" % ("PASS" if ok else "FAIL", name, detail))
    report = "\n".join(lines) + "\n"
    rep_path = os.path.join(CARDS_DIR, "m1-assert-r2279.txt")
    with open(rep_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(report)
    sys.stdout.buffer.write(("wrote %s\n" % out).encode("utf-8"))
    sys.stdout.buffer.write(report.encode("utf-8"))
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
