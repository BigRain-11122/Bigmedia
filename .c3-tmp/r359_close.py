# -*- coding: utf-8 -*-
# R359 idle-fast close: state.json append + tick/ts/task refresh + status-export export_ts refresh
# single-shot python script per R322 lesson (no multi-line replace anchors)
import io, re, json, datetime, os

MS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
STATE = os.path.join(MS, "src", "os", "state.json")
EXPORT = os.path.join(MS, "docs", "status-export.json")

now = datetime.datetime.now()
stamp_full = now.strftime("%Y-%m-%d %H:%M:%S")
R = "R359"
WINDOW = u"idle-fast 并窗轮 4/6（本轮不 commit·窗 R356-R361 满 6 收账）"

entry = (
    u"2026-09-26 %s %s: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 4/6 不 commit）——"
    u"①无新令（orders 顶=O-20260925-1931-HQ-C·R283 已记账）"
    u"②backlog 顶行不可认领（#63 图鉴续件 C-00030 锚正典位轮首核=仍不在位〔python os.path.exists False+C-00031 同核 False 实证·anchors 尾三=C-00027/C-00028/C-00029 止 C-00029〕supply-gated 维持"
    u"·#59 REACT 当日映射余量耗尽 R314 判定同日维持〔新热点窗=09-27 日报〕"
    u"·#57 替代率首报 10-07 窗挂账·#21 周日立法件届日=明日 09-27 未到〔周日周轮立法流程〕"
    u"·自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕）"
    u"③树态=仅自产预期件（M state.json+M status-export.json=R356-R358 idle-fast 并窗自记账预期态·?? .c3-tmp/r356~r359 自产脚本件随窗满批 commit·无 index.lock python os.path.exists False 实证·HEAD=5a9ee5c）"
    u"④ch.5 v3 稿未落（storylines python walk 扫描 novel/audio/comic 三子域 09-26 零新写盘实证=ch.5 判定口径成立·bm-a 面）"
    u"·日报 2026-09-26 在案不重跑（os.path.exists True）·W39 周审在案；"
    u"集团双锚静=ledger 行含 @ 四模式 21=锚零新转办（python 计数 21 实证）·decisions python 非空行 33=锚〔尾=D-20260926-04〕零新行零动作；"
    u"三探针全绿（board 0 FAIL 5 题 10 稿 5 in production exit 0/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1〔renders 42/42 注账〕"
    u"/loop_health 0 FAIL 19 WARN 皆在案史实〔12 log-order+7 heartbeat-gap〕·tick358=done358 对账平）；"
    u"例行件=global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）"
    u"·tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）"
    u"——一行收账即出（%s·P-61 导出步照刷 export_ts）。"
    u"下轮快速路径首查：#21 周日立法件（09-27 届日即领·周日周轮立法流程）/REACT 09-27 日报热点窗届日即领/图鉴 C-00030 锚/ch.5 v3 稿落迹象/新令/集团转办——全静即 idle-fast（R360 5/6→R361 6/6 窗满 batch commit R356-R361）。"
) % (now.strftime("%H:%M"), R, WINDOW)

assert "R359: idle-fast" in entry

# task = log line minus ts prefix, first 60 chars
task = re.sub(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2} R\d+: ", "", entry)[:60]

with io.open(STATE, "r", encoding="utf-8-sig", newline="") as f:
    raw = f.read()
had_bom = raw.startswith(u"\ufeff")
text = raw.lstrip(u"\ufeff")
eol = u"\r\n" if u"\r\n" in text else u"\n"

# 1. append log entry after the last one
marker = u'"' + eol + u" ],"
idx = text.rfind(marker)
assert idx != -1, "log array end marker not found"
text = text[:idx] + u'",' + eol + u"  \"" + entry + text[idx:]

# 2. tick +1
m = re.search(r'"tick": (\d+),', text)
old_tick = int(m.group(1))
assert old_tick == 358, "unexpected tick %d" % old_tick
text = text[:m.start(1)] + str(old_tick + 1) + text[m.end(1):]

# 3. ts + task refresh
text = re.sub(r'"ts": "[^"]*"', u'"ts": "%s"' % stamp_full, text, count=1)
text = re.sub(r'"task": "[^"]*"', u'"task": "%s"' % task, text, count=1)

data = json.loads(text)
assert data["tick"] == 359, "tick mismatch"
assert data["log"][-1].endswith(u"batch commit R356-R361）。"), "entry tail mismatch"
assert len(data["log"]) == 371, "log count unexpected: %d" % len(data["log"])
assert data["log"][-1] == entry, "entry not appended verbatim"
assert data["ts"] == stamp_full and data["task"] == task, "ts/task mismatch"

with io.open(STATE, "w", encoding="utf-8", newline="") as f:
    if had_bom:
        f.write(u"\ufeff")
    f.write(text)

# 4. status-export export_ts refresh (lightweight per idle-fast precedent)
with io.open(EXPORT, "r", encoding="utf-8-sig", newline="") as f:
    etext = f.read().lstrip(u"\ufeff")
ts_iso = now.astimezone().isoformat(timespec="seconds")
etext = re.sub(r'"export_ts": "[^"]*"', u'"export_ts": "%s"' % ts_iso, etext, count=1)
json.loads(etext)  # validate
with io.open(EXPORT, "w", encoding="utf-8", newline="") as f:
    f.write(etext)

print("OK tick=359 ts=%s task_len=%d export_ts=%s" % (stamp_full, len(task), ts_iso))
