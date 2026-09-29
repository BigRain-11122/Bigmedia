# -*- coding: utf-8 -*-
# R711 LC-011 closeout ledger batch: 8 append/edit ops (finished/renders/station-reviews/queue/
# release-schedule/lc011 README/expert-calls/expert-verdicts). ASCII code, CJK payload only.
import io, json, os

root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

def rd(p):
    return io.open(os.path.join(root, p), encoding='utf-8').read()

def wr(p, s):
    io.open(os.path.join(root, p), 'w', encoding='utf-8').write(s)

def ap(p, s):
    with io.open(os.path.join(root, p), 'a', encoding='utf-8') as f:
        f.write(s)

ok = []

# (1) expert-verdicts net copy
evdir = 'expert-verdicts' if os.path.isdir(os.path.join(root, 'expert-verdicts')) else 'docs/expert-verdicts'
e4 = json.load(io.open(os.path.join(root, r'.lc011-tmp\e4-result.json'), encoding='utf-8'))
net = ('# E4 受众参考仪净本 · LC-011 缪一拆条（R711 同轮回填）\n\n'
       '- ts: %s\n- model: %s\n- material: %s\n- seat: E4 直觉观众（参考仪·非注册席·dept-review v1.5 §6 双态制）\n\n'
       '## 判词全文\n\n```\n%s\n```\n' % (e4['ts'], e4['model'], e4['material'], e4['verdict']))
wr(os.path.join(evdir, '20260929-232822-E4-audience.md'), net)
ok.append('verdicts:' + evdir)

# (2) expert-calls row
ap('docs/reviews/expert-calls.md',
   '| 2026-09-29 23:28 | E4-audience | E4 直觉观众（参考仪·非注册席） | C:\\Users\\sjs20\\Desktop\\FluxGroup\\media\\BigStream\\.lc011-tmp\\subs.srt | 1 | '
   'full text=%s/20260929-232822-E4-audience.md / 8.0 会看完+点赞转发明说（无条件式）·体裁混搭正面定性·旗①=名字句语境门槛扣 2\n'
   % evdir)
ok.append('expert-calls')

# (3) finished.md F-065 row
ap('output/finished.md',
   '\n- 2026-09-29: F-065 登记（R711）：**L-卡衍生视频线第十一件=拆条系列节律第十续件=系列首件精灵系硅基民拆条件=成品库第六十五件=排期表冗余池第八件视频入池（冗余扩容位第八件·queue §E 批活池 E11 件收官）**'
   '（LC-011-v1-shipinhao-60s《城市图鉴 015·缪一》拆条全链走门毕：源卡=CENSUS-v15 F-034〔R709 补池义务兑现入池评定夺=系列首件精灵系硅基民拆条=物种面扩展第三档〔碳基×8→像素灵×2→精灵系首件〕'
   '+卡面双端互指=拆条系列第四对人物链〔C-00024「合作最久的主播=何雨欣」×C-00022「合作最久的是字幕君缪一」·LC-003 选优互证面兑现 R683 在案·主播圈人物链〕+M0 反差链在册 7/8 A 档〔全城最年轻成年硅基民×一帧一毫秒对轴匠性纪律〕'
   '+runner-up=潘志明 C-00023 后续候选顺位首位注记〕+S1 v1.5+L18-L20 门 10/10 零违律一次过=**拆条系列十一连满分**+M1 v4 终稿 0F0W+空气预算三道裁链 57.760s 定稿 2.24s 余量+TTS light 定稿音轨'
   '+R710 渲染〔census-card-v15-vertical 自产源件 13s+对位表 12/12 visual-ratio 1.00+R-E shipinhao 12 段 11 柔 0 硬切+S2 三门全绿+帧验三律全过+AIGC 双标识分层〕'
   '+R711 收官〔E8 七席全 9.0〔review-20260929-lc011-v1.md〕+E4 同轮回填 8.0 三意愿无条件式〔会看完+点赞转发明说·体裁混搭正面定性·旗①=名字句语境门槛扣 2 与 ASR 同句双通道·净本 20260929-232822〕'
   '+ASR 终轨**两段拼接读出**〔通道事故+根修实录：整轨 run1=run2 确定性 6 cues〔27-54s 区 VAD 分块丢段〕→三探针定谳音轨完好〔silencedetect/段电平/中段窗单独转写全落〕→两段拼接 12 cues 全覆盖=R638/R701 通道根修先例'
   '·归一 22 sites/73 diff/209 字≈34.9% 字位=与 LC-010 同位双连峰+缪→妙 ×2 名字句双损新族+硅基民→龟鸡 ×2 精灵系物种行首损+信条句万半真=信条位首次双字损·字幕轨 edge-tts 12/12 零损兜底·VAD 参数面=ASR 校准线候选提案位〕+M4→F-065 登记'
   '+release-schedule v2.3 视频号冗余弹药 8 件〕）\n')
ok.append('finished-F065')

# (4) renders README lc-011 row upgrade
p = 'output/renders/README.md'
s = rd(p)
old = '**在链·渲染腿毕（queue §E 批活池 E11 件·冗余扩容位第八件·源卡=CENSUS-v15 F-034 缪一·系列首件精灵系硅基民拆条位·R709 起链五腿毕→R710 渲染+S2 三门+帧验三律全过·收官腿=E8+ASR+E4+M4→F-065 随轮领）**'
new = '**成品·落位（F-065 登记 R711·queue §E 批活池 E11 件收官·冗余扩容位第八件·源卡=CENSUS-v15 F-034 缪一·系列首件精灵系硅基民拆条位·R709 起链→R710 渲染→R711 收官全链走门毕：E8 七席 ≥9+ASR 终轨两段拼接读出〔通道事故根修实录〕+E4 8.0 同轮回填+M4）**'
assert old in s, 'renders lc-011 status cell not found'
s = s.replace(old, new, 1)
wr(p, s)
ok.append('renders-row')

# (5) station-reviews R711 row
ap('docs/reviews/station-reviews.md',
   '\n- | 2026-09-29 | **E8 终审+M4+F-065 登记（lc-011 缪一拆条收官腿·queue §E E11 件收官·冗余池第八件落位件）** | lc-011-v1-shipinhao-60s.mp4+review-20260929-lc011-v1.md | '
   'ASR 终轨（R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1·23:28:22 起飞与 E4 并飞同窗 87s 落地 exit 0·**通道事故+根修实录：整轨 run1=run2 确定性 6 cues〔27-54s 区 VAD 分块丢段〕'
   '→三探针定谳音轨完好〔silencedetect 无 >2.5s 静默/per-seg loudness 全 uniform/中段窗单独转写 5 cues 全落〕→两段拼接读出 12 cues 全覆盖〔asr-check.srt+asr-diff-r711.txt〕〕'
   '+E4 参考仪同轮回填（8.0·87s 热载·三意愿无条件式·净本 20260929-232822-E4-audience） | —（收官登记行） | '
   'ASR=归一 22 sites/73 diff chars/209 字≈**34.9% 字位=与 LC-010 同位双连峰**（城市专名+物件词密度件〔缪 ×2/硅基 ×2/七段街区/霸得蛮/裱/帧/欣〕'
   '+缪名字句双损新族+精灵系物种行首损+信条位首次双字损·字幕轨 edge-tts 12/12 零损兜底·**VAD 参数面=ASR 校准线候选提案位**）→S2 9.0；'
   'E8 七席 ≥9（review-20260929-lc011-v1.md·E3 席=第四对人物链卡面双端互证+物种阶梯第三档）→M4 完成态→F-065 登记+冗余池第八件落位（release-schedule v2.3·视频号冗余弹药 8 件）'
   '+renders 行升「成品·落位」+queue §E E11 出池（lane=E3 单条<2·补池义务注记=E12 随轮领·候选=潘志明 C-00023〔R709 runner-up 顺位首位〕/BS-007 稿集件顺位后置维持）\n')
ok.append('station-reviews')

# (6) queue burn line
ap('docs/self-improvement-queue.md',
   '\n- 2026-09-29: **E11 兑现收官毕（R711·LC-011 缪一全链走门毕 F-065+冗余池第八件落位=视频号冗余弹药 8 件·三验字段执行注记在档〔假设=拆条系列节律第十续件+系列首件精灵系硅基民=物种面扩展第三档+第四对人物链卡面双端互证验证·'
   '消费面=视频号冗余池+L-卡库·consumer_plan=全链 M0→F 本地执行零云端〕）：ASR 终轨两段拼接读出（整轨 VAD 分块丢段事故 run1=run2 确定性→三探针定谳音轨完好→通道根修 R638/R701 先例·34.9% 字位双连峰·字幕轨 12/12 零损兜底）'
   '+E4 8.0 三意愿无条件式+七席 ≥9→M4**——lane 降至 E3 REACT-v6（09-30 热点窗位）单条<2（C-20260929-02 B 款口径）→**补池义务注记**：E12 随轮领（候选=潘志明 C-00023〔R709 runner-up 顺位首位〕'
   '=选题馆守门人拆条=内容产线三工种〔主播 LC-003→字幕君 LC-011→选题官 E12〕图鉴拆条链闭环位/BS-007 稿集件=顺位后置维持）。\n')
ok.append('queue-E11')

# (7) release-schedule v2.3
p = 'docs/release-schedule-v1.md'
s = rd(p)
old = '＝视频号冗余弹药 7 件**=M6 调仓弹药+30 天日更冗余（实际冗余位随 M5 发布案盘点对表·令文「冗余」超额）'
old2 = '=视频号冗余弹药 7 件**=M6 调仓弹药+30 天日更冗余（实际冗余位随 M5 发布案盘点对表·令文「冗余」超额）'
add = ('+LC-011 拆条 F-065（R711·冗余池第八件视频·缪一《城市图鉴 015》·拆条系列节律第十续件·**系列首件精灵系硅基民拆条=物种面扩展第三档**+第四对人物链卡面双端互证件·'
       '收官=E8 七席 ≥9+E4 8.0+ASR 终轨两段拼接读出〔通道事故根修实录〕）=视频号冗余弹药 8 件**=M6 调仓弹药+30 天日更冗余（实际冗余位随 M5 发布案盘点对表·令文「冗余」超额）')
if old in s:
    s = s.replace(old, add, 1); ok.append('sched:fullwidth')
elif old2 in s:
    s = s.replace(old2, add, 1); ok.append('sched:ascii')
else:
    ok.append('sched:MISS')
s = s.rstrip() + ('\n- v2.3 2026-09-29 R711：**冗余池扩容第八件视频入池**（LC-011《城市图鉴 015·缪一》拆条=F-065·成品库 64→65 件·L-卡衍生视频线第十一件=拆条系列节律第十续件·'
                  '**系列首件精灵系硅基民拆条=物种面扩展第三档**〔碳基×8→像素灵×2→精灵系首件〕+**第四对人物链卡面双端互证**〔C-00024「合作最久的主播=何雨欣」×C-00022「合作最久的是字幕君缪一」·LC-003 互证面兑现〕'
                  '·R709 补池入池评定夺→R710 渲染→R711 收官全链走门：S1 10/10 十一连满分+ASR 终轨**两段拼接读出**〔整轨 VAD 分块丢段事故 run1=run2 确定性→三探针定谳音轨完好→通道根修·34.9% 字位与 LC-010 同位双连峰·字幕轨 12/12 零损兜底〕'
                  '+E4 8.0 三意愿无条件式+七席 ≥9→M4）；§四 盘点行同步（视频号冗余弹药 7→8 件）。\n')
wr(p, s)
ok.append('sched:v2.3')

# (8) lc011 README: production record + gate block
p = 'data/sources/lc011/README.md'
s = rd(p)
old = '- 余腿：收官腿（E8 终审七席+ASR 终轨 R169 QC recipe+E4 同轮回填→M4→F-065 登记→冗余池第八件落位→release-schedule v2.3）R711 随轮领'
new = '- 收官腿（R711）：E8 七席 ≥9（review-20260929-lc011-v1.md）+ASR 终轨两段拼接读出+E4 同轮回填 8.0→M4→**F-065 登记（成品库第六十五件）+冗余池第八件落位（release-schedule v2.3·视频号冗余弹药 8 件）——全链走门毕**'
assert old in s, 'lc011 gate-block tail line not found'
s = s.replace(old, new, 1)
s = s.rstrip() + ('\n- 2026-09-29 R711 收官腿毕（R708 同型）：①ASR 终轨（R169 QC recipe·HF_HUB_OFFLINE=1·23:28:22 起飞与 E4 并飞 87s 落地）'
                  '=**整轨 VAD 分块丢段事故首录+通道根修实录**：run1=run2 确定性 6 cues（27-54s 区整段缺失）→三探针定谳音轨完好'
                  '（silencedetect -45dB:d=2.5 零长静默+per-seg loudness 全 uniform〔mean -25.7~-27.9dB/max -2.0~-5.4dB〕+中段窗 27-54s 单独转写 5 cues 全落=b5 尾-b10 内容全在）'
                  '→两段拼接读出 12 cues 全覆盖（asr-check.srt〔头部 5+民字位+中段 +27.0s 偏移 5+CTA〕）→asr-diff-r711.txt 归一 22 sites/73 diff/209 字≈**34.9% 字位=与 LC-010 同位双连峰**'
                  '（城市专名+物件词密度件）·关键事实词存活（hook 全句/字幕这行快不是本事准时才是/城主/复制成两份/并行捷径/觉醒才三年/名字自己选/何雨欣→何雨昕值存活/公众号 CTA 全句）'
                  '+实质退化如实（缪→妙 ×2 名字句双损新族/硅基民→龟鸡 ×2 精灵系物种行首损/信条句万半真=信条位首次双字损/七段街区→极短节区/霸得蛮→罢了蛮 湘腔锚语/裱→表 味→位 工位→公位/发版了→发板了/CTA 档案→大案）'
                  '→字幕轨 edge-tts 直出 12/12 零损兜底→S2 9.0·**whisper_to_srt.py VAD 参数面=ASR 校准线候选提案位**（不本件动工具·queue 提案面）；'
                  '②E4 参考仪同轮回填 8.0（87s 热载·三意愿无条件式：会看完+「我会点赞并转发给朋友」双明说·「竖屏档案卡形式有新意」体裁混搭正面定性·'
                  '旗①=名字句语境门槛扣 2 与 ASR 同句双通道·最弱=背景科幻门槛=精灵系首拆世界观语境成本·净本 20260929-232822-E4-audience）；'
                  '③E8 七席 ≥9（review-20260929-lc011-v1.md·E3 席=第四对人物链卡面双端互证+物种阶梯第三档）→M4→F-065 登记（成品库第六十五件）'
                  '+冗余池第八件落位（release-schedule v2.3）——queue §E E11 出池（lane=E3 单条<2·补池义务注记 E12=潘志明 C-00023 runner-up 顺位首位）。\n')
wr(p, s)
ok.append('lc011-readme')

print('LEDGER_OK', ok)
