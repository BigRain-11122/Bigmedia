# -*- coding: utf-8 -*-
# R715 closeout: state.json (R714 killed-round account line + R715 log, tick 713->715) + status-export refresh
import io, json, os, time

root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = time.strftime('%Y-%m-%d %H:%M:%S')
now_iso = now + '+08:00'

killed_line = (
    "2026-09-30 00:5x R714 断洞修复（账目·R715 承办·R155/R689 先例）：00:36 起跑轮 00:56 后被杀零 state 写盘（可见足迹=r714_probe.py 五查 00:36-00:37+渲染腿五步 build/render/framecheck 00:41-00:49+S2 三门+帧验三律+台账落笔 station-reviews/renders/lc012 README/queue 00:50-00:56·round.lock 由启动器硬帽回收）——盘上 WIP=LC-012 渲染腿全部（mp4 58.252s+plan.json+对位表 12/12+S2 三门全绿+帧验三律+台账四件）由 R715 吸收复核零重做，tick 713→715 断洞双记（R689/R690 先例）。"
)

log_line = (
    "2026-09-30 " + time.strftime('%H:%M') + " R715: 生产轮·LC-012 潘志明拆条收官腿毕=F-066 登记+冗余池第九件落位（queue §E 批活池 E12 件收官·R712/R713 claim 兑现·R714 断洞承接·R685/R688/R692/R695/R698/R701/R705/R708/R711 同型·实活轮·产品优先律 P-20260929-07 对位=本轮新实物=LC-012 全链走门 F-066 成品入库）——"
    "①轮首快速路径五查静（正典 r694_probe.py 口径：orders 顶=O-20260928-1910 42 件锚未动/ledger 六模式 CaseSensitive 41=锚零新 CEO 令级事件/decisions UTF8 非空行 75=锚零新行/production=open 自愈核在位/无 index.lock·树态=bm-a codex 批未闭让位维持〔README/city-humanities mtime 09-29 04:06 实读未动=#86 c+d 判据未达·两文件零接触〕+R714 断洞 WIP（.lc012-tmp+lc012 台账+station-reviews+renders+queue M+.c3-tmp r714_*）=自产预期态→断洞承接照走；"
    "②R714 渲染腿吸收复核（断点实况逐项核对零重做）：mp4 58.252s ffprobe 实测=音轨分毫一致+plan.json+cards-v1-matched 12/12 visual-ratio 1.00 在位+station-reviews R714 S2 行+renders 在链行+README 门禁块+queue E12 注全在案→**S2 三门同输入复跑=15 行全 PASS 确定性确认**（ai_feel 0F0W CV 0.304/0.354+层 1.8 六面+spec 微信视频号双 PASS 1.7s 余量=补账渲染件同跑三道机检门铁律执法）；"
    "③收官腿全链毕：ASR 终轨（R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1·01:07:58 与 E4 并飞同窗 45s 落地 exit 0·**整轨一次过** 12 cues dropped=0·R711 型 VAD 分块丢段未再现·asr-diff-r715.txt=24 sites/90 diff/217 字≈**41.5% 字位=系列带上缘之上新峰**〔选题官词域密度件〕：关键事实词存活〔潘志明/选题官/每天毙稿三十/留言墙/三页笔记值存活/信条句值存活/何雨欣→何雨昕值存活/公众号+CTA 尾句净读〕+实质退化如实〔毙稿 ×3 词域全线损=毕搞 ×2/必搞 ×2=hook+close+信条句三连·信条位毙→必核心字同音损=LC-007 见→贱/LC-008 谜→迷/LC-011 慢半帧族后新位/城的心电图室→新店同事=proof 拍核心意象词组大损/MEDIA 城→edia 成=拉丁城区名位损第三例/碳基→探机=物种行同位损族第十证/迫于→不予+不实→故事=punch 拍组损/他抄→她超+他→她=性别代词解码族第二证〔LC-008 逆型同族〕/四十七→47 数字形差值存活/档→大=CTA 档案族新形+繁体内→內单字漂移·字幕轨=edge-tts 直出 12/12 零损兜底〕）→S2 9.0+E4 参考仪同轮回填 **7.0**（e4_call.py 脱壳 11s 热载最快档·会看完+点赞明说+转发条件式=三意愿两明一条件〔拆条带 8.0×9+7.0×3 受众位·LC-007/LC-009 同档=守门人题材窄位如实注〕·「内容新颖有深度和故事性」正面定性·旗①=三重标注声明句被旗生硬扣 2〔「机器叙述者/AIGC 标识」=合规红线+AIGC 依法显著标识+CEO 定档 D-BS-07 皆不可删·E4 材料面框架文本感知旗=M6 校准线·吸收位=M5 简介证据链〕·最弱=传播性互动性〔公众号名称=账号物理件未开如实无名称可引〕·净本 expert-verdicts/20260930-010758-E4-audience+expert-calls 01:07 行）+E8 终审七席全 9.0（review-20260930-lc012-v1.md·环节门 S1 9/10〔R712〕/S2 9.0/S3 9.0/S4 9.0+七席 E1/E2/E3/E5/E6/E7/E8 全 9.0·E3 席=**内容产线三工种图鉴拆条链闭环**〔主播 LC-003→字幕君 LC-011→选题官 LC-012=本司同源职业自指链·MEDIA 城同城三工种同构 R303/R305 在册〕+第五对人物链跨卡互证注记·E6 席=产品优先律对位+R714 断洞吸收如实入账=假绿灯律① 执法面）→PASS 放行候选→M4 完成态；"
    "④**F-066 登记**（成品库第六十六件·L-卡衍生视频线第十二件=拆条系列节律第十一续件）+**冗余池第九件落位=排期表视频号冗余弹药 9 件**（release-schedule v2.4·盘点行同步）+renders 行升「成品·落位」+station-reviews R715 收官行+lc012 README 收口+queue §E E12 出池（lane 降至 E3 热点窗位单条<2·**补池义务注记=候选苏梓涵 C-00020/老晶振 C-00019/BS-007 稿集件随选优轮评估入池**）+tmp 批闭收账（.lc012-tmp/ 全批+asr_call/e4_call+asr-check.srt/asr-diff-r715 随本轮 commit）；"
    "⑤三探针（收账步实跑 r715_probes.py）：board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面 **0 发现**（render-unannot lc-012 随 F-066 登记+成品落位标清零·阻塞≠失败口径）/loop_health 2 FAIL+70 WARN 皆在案史实类（2 outage=09-26 49min+09-28 609min 同事件足迹已裁定不重复触发+account-lag done713=tick713 收账前平·tick715 断洞双记后自平 R689/R690 先例）；"
    "⑥例行件：日报 09-30 在案不重跑（R713 补产）/W40 周审在案（R576）/月度注记在案（R-20260928-03）/global-benchmarks day6 ≤7 跳过（下期 10-01=#80 并窗勿提前触碰）/#70 OSS 窗 2=09-29 21:40 已开（窗关 10-02 21:40·切片 1 已毕 R644=前窗义务足·本窗切片随轮领）/T1 催办=已裁项停用口径/HQ-FEEDBACK 不写（无集团层新 open 问题·ledger/decisions 双锚静）/tokens:local=2 类（ASR faster-whisper medium×1+E4 qwen2.5:14b×1·本地 Ollama/faster-whisper 零 API token·P-54⑤ 计量律）——"
    "下轮=R716 可领序：①E3 REACT-v6 09-30 热点窗（P-1 试点终判件 2/2·当日日报 09-30 在案=R713 补产）②E12 出池后补池义务（候选苏梓涵 C-00020/老晶振 C-00019/BS-007 稿集件随选优轮评估）③#70 OSS 窗 2 切片（≤10-02 21:40）④#86 c+d 让位判据（bm-a codex 批闭 commit 落地随轮首查）。收账显式列文件 commit+push"
)

# state.json
sp = os.path.join(root, 'src/os/state.json')
st = json.load(io.open(sp, encoding='utf-8'))
st['tick'] = 715
st['ts'] = now
st['task'] = log_line.split('R715: ', 1)[1][:60]
st['focus'] = ("R716: ①E3 REACT-v6=09-30 热点窗（P-1 试点终判件 2/2·当日日报 09-30 在案·晨窗内择优）②E12 出池后补池义务（候选苏梓涵 C-00020/老晶振 C-00019/BS-007 稿集件随选优轮评估）③#70 OSS 窗 2 切片（≤10-02 21:40）——五查锚=orders 顶 O-20260928-1910·ledger 41（六模式 CaseSensitive=正典 r694_probe.py 口径）·decisions 75")
st['log'].append(killed_line)
st['log'].append(log_line)
io.open(sp, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=1))

# status-export.json
ep = os.path.join(root, 'docs/status-export.json')
ex = json.load(io.open(ep, encoding='utf-8'))
ex['export_ts'] = now_iso
ex['outs'][0][1] = ("tick 715，R715 生产轮·LC-012 潘志明拆条收官腿毕=F-066 登记+冗余池第九件落位（queue §E E12 件收官·R714 断洞承接·实活轮·产品优先律对位=本轮新实物=LC-012 全链走门成品入库）："
                    "R714 渲染腿盘上毕吸收复核+S2 三门同输入复跑 15 行全 PASS 确定性确认"
                    "+ASR 终轨整轨一次过（41.5% 字位选题官词域密度峰如实·字幕轨 12/12 零损兜底）"
                    "+E4 7.0 同轮回填+E8 七席 ≥9→M4→F-066（成品库第六十六件）+release-schedule v2.4（视频号冗余弹药 9 件）——lane=E3 单条<2·补池义务注记（候选苏梓涵/老晶振/BS-007）")
ex['results'].insert(0, ["715", log_line])
ex['results'].insert(0, ["714", killed_line])
ex['live'] = [
    ["当前活：LC-012 收官毕=F-066 登记（成品库 66 件）+冗余池第九件落位（视频号冗余弹药 9 件）——E12 出池·补池义务随轮领（候选苏梓涵 C-00020/老晶振 C-00019/BS-007 稿集件）·lane=E3 REACT-v6 09-30 热点窗位"],
    ["最近实物：lc-012-v1-shipinhao-60s.mp4（F-066 成品·output/renders/·58.252s·12 段 11 柔 0 硬切·角标=拆条 012·源城市图鉴 014·内容产线三工种拆条链闭环件=主播→字幕君→选题官）·" + now],
    ["下个里程碑：E3 REACT-v6 09-30 热点窗（P-1 试点终判件 2/2·当日日报在案）窗 ≤09-30 晚+补池入位（窗 ≤10-01）·#70 OSS 窗 2 切片 ≤10-02 21:40"],
]
io.open(ep, 'w', encoding='utf-8').write(json.dumps(ex, ensure_ascii=False, indent=1))
print('STATE_OK tick715 ts', now, 'task_len', len(st['task']))
print('EXPORT_OK live rows', len(ex['live']), 'results head', ex['results'][0][0], ex['results'][1][0])
