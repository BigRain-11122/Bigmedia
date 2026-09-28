# -*- coding: utf-8 -*-
# r643 E4 same-round backfill: review v1.1 + clean verdict + finished/README segments + station row + queue P-1 judged + state + status-export
import io, json, os, datetime

R = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
NOW = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
NOWH = datetime.datetime.now().strftime("%H:%M")
NOWISO = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")


def rd(p):
    return io.open(os.path.join(R, p), encoding="utf-8").read()


def wr(p, t):
    io.open(os.path.join(R, p), "w", encoding="utf-8", newline="\n").write(t)
    print("WROTE", p)


VERDICT_CLEAN = u"""# E4 参考仪净本·MC-20260929-REACT-v5《城市速报 005·哈基米肉鸽游戏》

- 起飞=2026-09-29 02:04（Start-Process 脱壳·1500s 窗）→ 落判 02:05:28（90s 热载最快档=R223/R276 同型）
- 模型=qwen2.5:14b（本地 Ollama 直调·零 API token）·材料=MC-20260929-REACT-v5 static card（cards.json + render output）
- 盲评材料律合规（零嵌审计史）·e4_call.py ANSI+盲文段双清洗在位·本件零污染

## 判词（verbatim）

1) 刷到这张卡我会停下来看。这张卡的设计新颖有趣，结合了当前的网络热点和一个虚构城市的反应，具有一定的创意和娱乐性。我会选择保存或转发给朋友，因为它既有当下流行的元素，也有想象的空间，适合和朋友们分享和讨论。我会给这张卡打7分，因为它的创意和趣味性吸引人，但可能对不熟悉背景设定的用户来说，理解起来有一定的门槛。

2) 我一眼就能看出一些地方可能对不熟悉背景设定的读者来说会有些空洞或难以理解，例如「求新轴」和「秩序轴」的反应，这些内容需要一定的背景知识才能完全理解其含义。这样的情况会扣2分，因为虽然这些内容对熟悉背景的人来说有意义，但对普通读者而言，可能缺乏必要的信息来完全领会其意义，从而影响阅读体验。

3) 最弱的一项是它的互动性和实用性。这张卡主要依赖于对特定背景设定的理解，对于那些没有相关背景知识的读者来说，可能难以产生共鸣或感到信息量不足。互动性和实用性较弱，因为这张卡更像是一个创意作品或艺术性表达，而不是实用信息或互动交流的工具，这限制了它的受众范围和传播效果。

## 判读（R643 同轮回填）

- **读数 7.0**：会停下来看+会保存或转发给朋友=三意愿正面明说〔无条件式〕——REACT 带宽如实（v1 7.0/v2 8.0/v3 7.0/v4 7.0/v5 7.0=带持平）
- 旗①（扣 2）=「求新轴」「秩序轴」反应行语境门槛（不熟悉背景读者空洞/难懂）——卡面文字旗·池句 verbatim 不可改写·MC-003 语境门槛族轴位标签变体·吸收位=M5 图文页语境+系列语境
- 最弱=互动性与实用性（静态卡载体固有·M6 校准位）
- **P-1 试点判据判读（试点 1/2）**：①套路化零再现 ✓（v3「套路化扣 2」同位旗未再现·旗型迁移=语境门槛族·三律机制面执行有效）②总分 7.0<8.0 ✗（带持平）——判负留痕合法·终判挂 REACT v6（试点 2/2）
- 判定：非拦截·七席 ≥9 PASS 维持（F-054 登记态不动）
"""

# --- 1: clean verdict file ---
vdir = os.path.join(R, "docs", "reviews", "expert-verdicts")
if not os.path.isdir(vdir):
    os.makedirs(vdir)
wr(os.path.join("docs", "reviews", "expert-verdicts", "20260929-020528-E4-audience.md"), VERDICT_CLEAN)

# --- 2: review file v1.1 ---
rp = os.path.join("docs", "reviews", "review-20260929-mcreact-v5.md")
rt = rd(rp)
a1 = u"## E4 参考仪（异步在飞→下轮回填追加制·非拦截·dept-review §6 双态制）"
assert rt.count(a1) == 1, "E4 section header count=%d" % rt.count(a1)
# replace header + two bullets block (up to the next section '## 未测面')
start = rt.index(a1)
end = rt.index(u"## 未测面")
new_sec = (u"## E4 参考仪（同轮回填毕·非拦截·dept-review §6 双态制）\n\n"
           u"- **读数 7.0**（起飞 02:04→02:05:28 落判 90s 热载最快档=R223/R276 同型）：**会停下来看+会保存或转发给朋友=三意愿正面明说〔无条件式〕**——REACT 形态带宽如实（v1 7.0/v2 8.0/v3 7.0/v4 7.0/v5 7.0=带持平）\n"
           u"- **正面读数**：「结合了当前的网络热点和一个虚构城市的反应，具有一定的创意和娱乐性」+「适合和朋友们分享和讨论」=体裁混搭面正面定性五连证+分享动机明说\n"
           u"- **旗①（扣 2）=「求新轴」「秩序轴」反应行对不熟悉背景设定的读者空洞/难懂**：卡面文字旗（池句 verbatim 不可改写·**MC-003 语境门槛族轴位标签变体**·吸收位=M5 图文页语境+系列语境）\n"
           u"- **最弱**：互动性和实用性（静态卡载体固有·M6 校准位）\n"
           u"- **P-1 试点判据判读（试点 1/2·判据三问）**：**①套路化零再现 ✓**——v3「逍遥轴+烟火轴句套路化扣 2」同位旗未再现·旗型迁移=语境门槛族（轴位标签理解门槛=新观察位·非句式套路化·三律机制面执行有效）；**②总分 7.0<8.0 ✗**（REACT 带 v1-v5 带持平非递增）——**判负留痕合法**·③两件后读数带上移=随 REACT v6（试点 2/2）终判\n"
           u"- 判定：非拦截·七席 ≥9 PASS 维持（F-054 登记态不动）·净本 `expert-verdicts/20260929-020528-E4-audience.md`\n\n")
rt = rt[:start] + new_sec + rt[end:]
a2 = u"- E4 参考仪在飞（本件判读=下轮回填·非拦截席）"
assert rt.count(a2) == 1, "untested-face E4 item count=%d" % rt.count(a2)
rt = rt.replace(a2, u"- ~~E4 参考仪在飞~~（**本件销项**=同轮回填毕 7.0·02:05:28 落判 90s 热载最快档）", 1)
a3 = u"→M4.5 终审→E4 参考仪（异步在飞→回填追加制）"
assert rt.count(a3) == 1, "chain line count=%d" % rt.count(a3)
rt = rt.replace(a3, u"→M4.5 终审→E4 参考仪（同轮回填毕 7.0）", 1)
a4 = u"- 2026-09-29: v1.0 首版（R643·"
assert rt.count(a4) == 1, "changelog v1.0 count=%d" % rt.count(a4)
# append v1.1 changelog after the v1.0 line (find end of that line)
idx = rt.index(a4)
eol = rt.index(u"\n", idx)
v11 = (u"- 2026-09-29: v1.1 **E4 同轮回填 7.0**（起飞 02:04→02:05:28 落判 90s 热载最快档·三意愿无条件式明说·旗①=轴位行语境门槛扣 2=P-1 判据①判读「套路化零再现 ✓」旗型迁移〔非 v3/v4 同位套路化旗〕·②7.0<8.0 ✗ 带持平=判负留痕合法·终判挂 REACT v6·净本 expert-verdicts/20260929-020528-E4-audience.md·非拦截·七席 ≥9 PASS 维持）。")
rt = rt[:eol] + u"\n" + v11 + rt[eol:]
wr(rp, rt)

# --- 3: finished.md F-054 backfill segment ---
fp = os.path.join("output", "finished.md")
ft = rd(fp)
fa = u"挂后续热点窗**；发布锁=M5 账号物理件不变（公众号=批次① 未开·未上线=未测量）"
assert ft.count(fa) == 1, "finished F-054 tail count=%d" % ft.count(fa)
seg = (u"+**E4 参考仪同轮回填 7.0**（02:04 起飞→02:05:28 落判 90s 热载最快档：会停下来看+会保存或转发给朋友=三意愿正面明说〔无条件式〕·体裁混搭正面定性五连证·旗①=求新轴/秩序轴反应行语境门槛扣 2"
       u"〔**P-1 判据①判读=套路化零再现 ✓——旗型迁移为 MC-003 语境门槛族·非 v3/v4 同位套路化旗**·池句 verbatim 不可改写·吸收位=M5+系列语境〕·最弱=互动性实用性〔载体固有·M6〕·净本 expert-verdicts/20260929-020528-E4-audience.md·非拦截·七席 ≥9 PASS 维持）；"
       u"**P-1 试点判据判读（试点 1/2）=①套路化零再现 ✓②总分 7.0<8.0 ✗（REACT 带 v1-v5 带持平·判负留痕合法）→终判挂 REACT v6**")
ft = ft.replace(fa, fa + seg, 1)
wr(fp, ft)

# --- 4: cards README backfill segment ---
cp = os.path.join("data", "storylines", "cards", "README.md")
ct = rd(cp)
ca = u"REACT 续件=按日热点随轮领（#59 维持开板·P-1 试点件 2/2=REACT v6）"
assert ct.count(ca) == 1, "README v5 tail count=%d" % ct.count(ca)
cseg = (u"+**E4 同轮回填 7.0**（02:05:28 落判 90s 热载最快档·会停+会保存或转发=无条件式三意愿正面明说·旗①=轴位行语境门槛扣 2〔P-1 判据①套路化零再现 ✓=旗型迁移非套路化·MC-003 族·M5 吸收位〕"
        u"·最弱=互动性实用性〔载体固有〕·净本 expert-verdicts/20260929-020528-E4-audience.md·非拦截）；**P-1 判据判读=①✓②7.0<8.0 ✗（带持平·判负留痕）·终判挂 v6**")
ct = ct.replace(ca, ca + cseg, 1)
wr(cp, ct)

# --- 5: station-reviews backfill row ---
sr = u"| 2026-09-29 | **E4 参考仪同轮回填（mc-react-v5=#59 R643 件·起飞 02:04→02:05:28 落判 90s 热载最快档）** | 7.0 会停下来看+会保存或转发给朋友=三意愿正面明说〔无条件式〕（「结合当前热点与虚构城市反应·创意与娱乐性」=体裁混搭面正面定性五连证·「对不熟悉背景设定的用户理解门槛」如实并录）；旗①=求新轴/秩序轴反应行语境门槛扣 2（**P-1 判据①判读=套路化零再现 ✓——旗型迁移为 MC-003 语境门槛族·非 v3/v4 同位套路化旗**·池句 verbatim 不可改写·吸收位=M5+系列语境）；最弱=互动性与实用性（静态卡载体固有·M6 校准位）；**P-1 试点判据判读（试点 1/2）**=①套路化零再现 ✓②总分 7.0<8.0 ✗〔REACT 带 v1-v5=7.0/8.0/7.0/7.0/7.0 带持平·判负留痕合法〕→终判挂 REACT v6（试点 2/2）；回填六件=review v1.1+净本 20260929-020528+finished F-054 回填段+cards README v5 回填段+queue §D P-1 判读态+本行；非拦截·七席 ≥9 PASS 维持（F-054 登记态不动） |"
sp2 = os.path.join("docs", "reviews", "station-reviews.md")
st = rd(sp2)
if st and not st.endswith("\n"):
    st += "\n"
st += sr + "\n"
wr(sp2, st)

# --- 6: queue P-1 cell judged state ---
qp = os.path.join("docs", "self-improvement-queue.md")
qt = rd(qp)
qa = u"| in-pilot（**试点 1/2 交付毕=REACT-v5 R643 F-054**·三律执行注记全档评审单+cards.json editorial_value·判据①套路化零再现②总分 ≥8.0 待 E4 回填轮判读〔e4 在飞〕·试点 2/2=REACT v6 挂后续热点窗·判负留痕合法） |"
assert qt.count(qa) == 1, "queue P-1 cell count=%d" % qt.count(qa)
qnew = u"| in-pilot（试点 1/2=REACT-v5 R643 F-054 交付毕+**E4 同轮回填 7.0 判读毕**：**判据①套路化零再现 ✓**〔旗型迁移=轴位行语境门槛族扣 2·MC-003 族·非 v3/v4 同位套路化旗·M5 吸收位〕+**判据②总分 7.0<8.0 ✗**〔REACT 带 v1-v5=7.0/8.0/7.0/7.0/7.0 带持平〕——判负留痕合法·**终判挂 REACT v6（试点 2/2·判据③两件后带上移随 v6 判）**） |"
qt = qt.replace(qa, qnew, 1)
qb = u"- 2026-09-29: **P-1 试点件 1/2 交付（R643·REACT-v5 全链走门毕 F-054·三律执行注记在档〔零人称口气句/结构异质/同轴位禁同句式+收束行权重升档〕·判据①②挂 E4 回填轮判读）**。"
assert qt.count(qb) == 1, "queue burn line count=%d" % qt.count(qb)
qt = qt.replace(qb, qb + u"\n- 2026-09-29: **P-1 试点 1/2 判读毕（R643 E4 同轮回填 7.0·判据①套路化零再现 ✓〔旗型迁移=语境门槛族〕②7.0<8.0 ✗ 带持平=判负留痕·终判挂 REACT v6）**。", 1)
wr(qp, qt)

# --- 7: state.json second log line + ts refresh ---
sp3 = os.path.join(R, "src", "os", "state.json")
s_raw = io.open(sp3, encoding="utf-8").read()
s = json.loads(s_raw)
assert s["tick"] == 643
LOG2 = (u"2026-09-29 " + NOWH + u" R643 补记·E4 参考仪同轮回填毕（追加制 R575/R582 同型·实活轮内二段）——起飞 02:04→02:05:28 落判（90s 热载最快档=R223/R276 同型）=**7.0** "
        u"会停下来看+会保存或转发给朋友=三意愿正面明说〔无条件式〕·「结合当前热点与虚构城市反应·创意与娱乐性」=体裁混搭正面定性五连证·旗①=求新轴/秩序轴反应行对不熟悉背景读者"
        u"**语境门槛扣 2**〔**P-1 判据①判读=套路化零再现 ✓——旗型迁移为 MC-003 语境门槛族·非 v3「套路化扣 2」同位旗**·池句 verbatim 不可改写·吸收位=M5 图文页语境+系列语境〕"
        u"·最弱=互动性与实用性〔静态卡载体固有·M6〕；**P-1 试点判据判读（试点 1/2）**=①套路化零再现 ✓（三律机制面执行有效·旗型转向语境门槛=新观察位）②总分 7.0<8.0 ✗"
        u"（REACT 带 v1-v5=7.0/8.0/7.0/7.0/7.0 带持平非递增）——**判负留痕合法**·终判挂 REACT v6（试点 2/2·判据③两件后带上移随 v6 终判）；"
        u"回填六件=review-20260929-mcreact-v5.md v1.1（E4 节落判+链行+未测面销项+变更行）+净本 expert-verdicts/20260929-020528-E4-audience.md+finished.md F-054 回填段+"
        u"cards/README v5 回填段+station-reviews R643 回填行+queue §D P-1 判读态更新；判定=非拦截·七席 ≥9 PASS 维持（F-054 登记态不动）·发布锁=M5 账号物理件不变；"
        u"tokens:local=1（E4 qwen2.5:14b 本轮落地记账·P-54⑤ 计量律）——下轮=R644 #87 whisper.cpp 接线单（HF_HUB_OFFLINE 坑律入单）/#86 b 腿群像建档批随轮序领。收账显式列文件 commit+push")
s["log"].append(LOG2)
s["ts"] = NOW
out = json.dumps(s, ensure_ascii=False, indent=2)
if s_raw.endswith("\n"):
    out += "\n"
io.open(sp3, "w", encoding="utf-8", newline="\n").write(out)
print("STATE2 OK ts=%s" % NOW)

# --- 8: status-export fixes ---
se_path = os.path.join(R, "docs", "status-export.json")
se_raw = io.open(se_path, encoding="utf-8").read()
se = json.loads(se_raw)
se["export_ts"] = NOWISO
n_fix = 0
for entry in se["outs"]:
    if entry and entry[0] == u"OS 循环":
        entry[1] = entry[1].replace(u"E4 异步在飞=下轮回填判 P-1 判据①②）——下轮=R644 可领序=①E4 回填（P-1 判据判读）②#87 whisper.cpp 接线单③#86 b 腿群像建档批",
                                   u"E4 同轮回填 7.0 判读毕=P-1 判据①套路化零再现 ✓〔旗型迁移=语境门槛族〕②7.0<8.0 ✗ 带持平·判负留痕·终判挂 REACT v6）——下轮=R644 可领序=①#87 whisper.cpp 接线单②#86 b 腿群像建档批")
        n_fix += 1
    if entry and entry[0] == u"量产产线":
        entry[2] = entry[2].replace(u"E4 在飞下轮回填·", u"E4 同轮回填 7.0（P-1 判据①✓②✗ 判负留痕·终判挂 v6）·")
        n_fix += 1
for d in se["depts"]:
    if d["n"] == u"内容生产部":
        d["t"] = d["t"].replace(u"验图 5/5 一次过+E4 异步在飞=下轮回填〕", u"验图 5/5 一次过+E4 同轮回填 7.0（P-1 判据①套路化零再现 ✓·②<8.0 判负留痕）〕")
        n_fix += 1
for r0 in se["results"]:
    if r0 and r0[0] == u"643":
        r0[1] = r0[1].replace(u"E4 异步在飞=下轮回填判 P-1 判据①②）", u"E4 同轮回填 7.0 判读毕=P-1 判据①✓②✗ 判负留痕·终判挂 v6）")
        r0[1] = r0[1].replace(u"tokens:local=0（E4 在飞落地轮记账）", u"tokens:local=1（E4 qwen 本轮落地记账）")
        n_fix += 1
assert n_fix == 4, "status-export fix count=%d" % n_fix
se_out = json.dumps(se, ensure_ascii=False, indent=1)
if se_raw.endswith("\n"):
    se_out += "\n"
io.open(se_path, "w", encoding="utf-8", newline="\n").write(se_out)
print("STATUS_EXPORT2 OK")
print("BACKFILL_ALL_DONE")
