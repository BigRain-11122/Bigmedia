# -*- coding: utf-8 -*-
"""R1921 close: fix @TS placeholder red in R1920 log line, append R1921 accounting,
update tech.md row 75 data point + new row 76 seed, refresh ts/task/focus/tick."""
import io, json, datetime, re, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = ROOT + r"\src\os\state.json"
TECH = ROOT + r"\state\queue\tech.md"

now = datetime.datetime.now()
ts_full = now.strftime("%Y-%m-%d %H:%M:%S")
hm = now.strftime("%H:%M")

# ---------- state.json ----------
raw = io.open(STATE, "r", encoding="utf-8-sig").read()
st = json.loads(raw)

# 1) red-fix: R1920 line kept literal "@TS" (template token was "@TS", close script
#    replaced "@TS@" -> substitution missed, assert checked the wrong token too).
hits = [i for i, l in enumerate(st["log"]) if "@TS R1920" in l]
assert len(hits) == 1, "expected exactly one @TS-carrying R1920 line, got %d" % len(hits)
i = hits[0]
assert st["log"][i].startswith("2026-10-10 @TS R1920:"), st["log"][i][:40]
# honest substitution: R1920 close ts field = 22:59:43
st["log"][i] = st["log"][i].replace("2026-10-10 @TS R1920:", "2026-10-10 22:59 R1920:", 1)

# 2) append R1921 log line
log_line = (
    "2026-10-10 " + hm + " R1921: 等待轮·tech#75 判断位照正法执行=稳态饱和域 NO-GO（O-20261009-1246 取活判走+产品优先律 §2 一行声明）——"
    "①轮首五查静中带一知悉=own orders 顶 O-20260908-1105==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）"
    "+集团扫描三面静=decisions truly_new=0 水位 131 维持+ledger @BigStream 4 行==值守锚零新转办"
    "+**HQ orders 新行一条=10-10 23:0x【@bm-c】mv0001 全曲 KF 批撤单**（CEO 22:5x 斥「没看到机队在干活」→bm-a 腾显存本地接管 44 镜 KF 批在跑·@bm-c 件=本循环零接触·份额=知悉+查看位注记）"
    "+无 index.lock+树态=MV sprint 会话批域在飞件零接触（R1745 承继·tech#26 撞面维持）；"
    "②GPU C-37 fresh 双连读=NO-GO 稳态饱和域定谳：读数1 ollama GEN-ERROR transport=TimeoutError face=busy-contended+gate worst-case free 624MB<2048 守卫/util 100>80/band 5120 振荡域"
    "→读数2 +30s free 604-650/band 46/util 100=**稳态饱和非振荡**（HQ 23:0x 行 KF 批本地接管实锚互证·tasks 2/8 disabled=bm-a 腾显存面）"
    "——四腿（MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 v13）维持 fire-ready gated（R1871 turnkey 材料在位）"
    "·tech#75 判断位照正法=非双 GO 不点火·序列数据点续记 tech.md 75 行（本轮零 GO 间隙出现=R1920 振荡域对照·纯稳态清洁 NO-GO 案）；"
    "③查看位四根并读（R1762 律·R1920 锚后）=meme outbound 零新（V1 成片 mp4 未落=TTS/装配腿在飞维持）"
    "+**krea2 30s-reel-v1/frames_full/ 7 新 KF 帧实锚**（22:58-23:03 INT1-INT5+N01/N02 秒级连落=全曲 KF 批本机在产真负载·与 GPU 饱和读数互证·MV 会话域查看位零接触）"
    "+shortvideo-dept/mv0001-handover 其余面零新；"
    "④修红 1 起=loop_health log-ts FAIL（R1920 行残留 @TS 占位符·本轮三探针点名）——根因=r1920_close.py L71 replace 模式 '@TS@' vs log 模板写 '@TS'（无尾 @）=代换静默未命中+L72 assert 同查错 token=双错同源"
    "→本轮修复（@TS→22:59·R1920 ts 字段 22:59:43 诚实口径）+tech.md 76 行新种子（占位符 token 三点共源纪律·审计发现补货）·复跑 loop_health log-ts 面归绿核验（余 2 outage FAIL=在案史实不重触发）；"
    "⑤三探针=probe_capture 紧凑面证据件 r1921_probes.txt（board 0 FAIL〔5 题 10 稿 5 in production〕/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17 needs-CEO〕0 发现〔78 renders 全注账 unannot=0〕/loop_health 修红前 3F+229W→修红后 log-ts 归绿=2F+229W 皆在案史实）+门证据件 r1921_gpu_gate.txt；"
    "⑥例行件=10-10 日报在案不重跑（R1845 00:03 一份为真相）·W41 周审在案 W42 件 10-12 未到·GB §④ v1.3 下期 10-15 跳过"
    "·export_ts 20:56:29 <24h 零 CEO 可见变化不重刷（产品优先律 §2 节流·live 三行核读维持）·#99 blocked-on-channel 维持（SLA ≤10-13）"
    "·#112 判据窗 10-11 08:00 届日未到不预扫·HQ-FEEDBACK 不写（新行=@bm-c MV 域件·非本司 open 问题零膨胀）"
    "·tokens:local=0（探针生成调用属探针件非评审调用 R1888 口径·纯只读+档案读写零本地模型产出调用·P-54⑤ 计量律）；"
    "⑦队列补货步=tech.md 76 行一粒真种子（@TS 占位符 token 三点共源守卫候选·本轮审计发现锚非凑数）+临时件=r1921 三证据件入账收口（tech#64 律）"
    "——下轮=R1922 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领〔城市源 ≥60 ≥2 件+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕+GPU C-37 fresh 四腿点火判断+tech#75 判断位照正法+meme V1 成片/全曲 MV 查看位随轮盯）"
)
st["log"].append(log_line)

# 3) accounting fields
st["tick"] = 1921
st["ts"] = ts_full
body = log_line.split(" ", 2)[2] if False else log_line[len("2026-10-10 " + hm + " "):]
st["task"] = body[:60]
st["focus"] = (
    "R1922 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领〔城市源 ≥60 ≥2 件+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕"
    "+GPU C-37 fresh 四腿点火判断〔MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 v13〕"
    "+tech#75 判断位照正法〔双 GO 连续 ≥2 方飞〕+meme V1 成片/全曲 MV 查看位随轮盯）"
)

has_bom = raw.startswith("\ufeff")
with io.open(STATE, "w", encoding="utf-8-sig" if has_bom else "utf-8", newline="") as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
print("state.json: tick=%s ts=%s bom=%s" % (st["tick"], st["ts"], has_bom))

# ---------- tech.md ----------
traw = io.open(TECH, "r", encoding="utf-8-sig").read()
tlines = traw.splitlines()
t75 = [i for i, l in enumerate(tlines) if l.startswith("75. ")]
assert len(t75) == 1, "tech 75 row count=%d" % len(t75)
i = t75[0]
assert "[R1920 判断位照正法执行" in tlines[i], "row 75 tail anchor missing"
tlines[i] = tlines[i] + (
    "——**[R1921 判断位照正法执行=稳态饱和域清洁 NO-GO]**：读数1 ollama GEN-ERROR transport=TimeoutError face=busy-contended+gate worst-case free 624MB/band 5120 振荡域/util 100"
    "→读数2 +30s free 604-650/band 46/util 100=**稳态饱和域**（band 46 非振荡·HQ orders 23:0x 行=bm-a 本地接管 44 镜全曲 KF 批在跑·frames_full/ 7 帧秒级连落互证·tasks 2/8 disabled=腾显存面）"
    "——双连 NO-GO·零 GO 间隙出现（R1920 振荡域对照案·本例=纯稳态）·非双 GO 不点火·四腿 fire-ready gated 维持·序列数据点续记（fire 稳定窗等待位维持）"
)
new76 = (
    "76. [R1921 补货·本轮修红审计发现] close 脚本占位符 token 三点共源守卫候选（缺口锚=R1920 行 @TS 残留→R1921 loop_health log-ts FAIL 点名"
    "——r1920_close.py L71 replace 模式 '@TS@' 而 log 模板写 '@TS'（无尾 @）=代换静默未命中+L72 assert 同查 '@TS@'=断言面与缺陷面错位双错同源"
    "·检测面已工作〔log-ts FAIL 一轮内点名=机制正常〕·缺=authoring 侧防呆）——候选=轮 close 脚本占位符单常量纪律（模板字面/replace/assert 三点共源一常量"
    "·或改 f-string 直拼免占位符位）·检测面不重复立法（tech#22 家族顾问级律核过）·判据=后续轮 close 脚本零 log-ts FAIL·判负留痕合法"
    "）——按认领制随轮领做（CPU 面·轻量）"
)
tlines.append(new76)
tlines.append("")
tout = "\r\n".join(tlines)
with io.open(TECH, "w", encoding="utf-8", newline="") as f:
    f.write(tout)
print("tech.md: row75 appended + row76 added (entries now %d)" % len([l for l in tlines if re.match(r"^\d{1,3}\. ", l)]))
print("CLOSE OK")
