# -*- coding: utf-8 -*-
# r911 close script (close-lineage terminal clause: write -> reload -> line-head ts assertion)
import io, json, os, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ST = os.path.join(ROOT, 'src', 'os', 'state.json')

st = json.loads(io.open(ST, 'r', encoding='utf-8-sig').read())
assert st['tick'] == 910, 'tick pre-close mismatch: %s' % st['tick']

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
hm = now[:16]

line = (
    u"%s R911: 等待态声明收轮·声明轮并窗新窗第 1 轮（R910 收讫轮个体 commit 后窗重置·五查全静=r911_scan 内容寻址复跑留档"
    u"〔r807_scan.py 谱系·r807_scan.txt 写出遇 PermissionError 文件锁=操作红轮内定谳→r911_scan.py 轮次名变体复跑 SCAN-OK 12 行·扫描逻辑零改仅换出文件名〕："
    u"orders 42=锚零新令〔顶=O-20260928-1910〕/ledger_scan_hits=46 基线带内〔task-modes 41+machine-modes 5·R845 re-baseline 维持·r845_regression P-2026-10-01-01 @bm-a dash row caught=True 复证〕/"
    u"decisions dnum 差集 NONE=120 基线〔D-20260930-19 水位差集制·D-13 SLA 无触发·派工通告板涉司行=BigStream 全收讫态维持〕/"
    u"production=open 自愈核 tick910〔pre-close 读数〕/无 index.lock 实测·树态=M CODELY.md〔09-30 18:55:34 R767 平台记忆压缩波定谳零接触〕=R892/R893 批闭后零 bm-a 活跃写盘迹象〕"
    u"+三探针=board 0 FAIL（5 ideas 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）0 发现〔72 renders 全注账·阻塞≠失败口径〕/"
    u"loop_health 3 FAIL+108 WARN 皆在案史实类〔09-26 49min+09-28 609min 两 outage 已裁定不重复触发+account-lag done913>tick910=在轮 beat 瞬态·tick911 收账自平口径"
    u"+新 1 WARN=R909 生产长轮 23:50→00:11 21min 心跳间隙·25min 预算长轮合法 WARN 级=R173/R180 同型〕"
    u"——四查尽维持〔R910 00:16 fresh 同判承接·scan 实核零变化·禁重扫同一等待对象=产品优先律 2〕："
    u"①REACT 10-02 热点窗已占〔F-085·R909〕·10-03 热点窗=届日领件〔10-03 日报缺先补产 daily_brief〕"
    u"②#70 OSS 窗 3=10-02 21:40 后开〔≤3 刀·窗 2 配额 R826+R762 双档在案〕"
    u"③供给闸四路 0/4 未达〔CENSUS C-00030 锚缺 scan 实核 present: False=供给闸闭/新令级事件缺 scan 实核 dnum 差集 NONE/REACT 10-03 未开/新批注缺〕"
    u"④W41 周轮件=10-05〔周报+自驱提案窗+CLOUD_LINE 首测·W40 提案 P-1 已 pilot-closed 判负留痕在案〕"
    u"+queue 顶项 B5=账号期门控〔保护态豁免〕+E-pool 空池豁免在案〔R810 判负留痕定谳〕"
    u"+backlog 顶行复核维持〔#67 DIGEST/#63 CENSUS C-00030/#66 F1=供给闸·#59 REACT 10-03=届日闸·#70=时间闸·#94 记忆梳理=10-04 窗·#15 口吻改写=随量产逐件拍稿折叠在案〕"
    u"+#86 常设腿供给面全闭核〔a=台词池 1440 行两轮筛毕 supply-gated 待 BigLife 池扩容 R893/b=锚池 20 卡全覆盖收官 supply-gated 待 C-00030+ R756/c=章件 ch1-ch5 现役版+ch1/ch2 v4 深采毕·ch6 未落盘 supply-gated R892/d=积累计数周报行随 W41 10-05〕"
    u"=真无活可拉〔P-20260928-02 ②④序·供给侧全闭+全时闸=保护态豁免面在案非违规闲置〕"
    u"——例行件：export R909 00:0x 刷新在 24h 窗内不刷〔产品优先律 2·实况零变化〕·日报 10-02 在案不重跑〔R909 00:00:26 补产·一份为真相·Test-Path True 实核〕/日报 10-01 在案〔R795〕/W40 周审在案〔R576〕/GB 闸 10-08〔R798 v1.2·scan 头行 10-01 读数非到期〕/T1 催办=已裁项停用口径/HQ-FEEDBACK 不写〔无集团层新 open 问题·dnum 差集 NONE 零膨胀〕/tokens:local=0（扫描+探针=纯脚本机检·P-54⑤ 计量律如实记）"
    u"——waiting: supply-gated lane held（卡点=OSS w3 10-02 21:40/REACT 10-03 届日/新锚卡 C-00030+/#94 10-04/W41 10-05，ETA 2026-10-02 21:40）。"
    u"本轮并窗 1/6（不 commit·os-protocol §6 并窗律：窗满 6/跨日界/异常/实活轮即收）·下轮=R912 声明轮同判承接（21:40 后届窗转实活领 #70 OSS w3 ≤3 刀）"
) % hm

st['tick'] = 911
st['log'].append(line)
st['focus'] = (
    u"R911: 等待态声明收轮毕（供给闸四路全闭·扫描/探针全静·并窗 1/6）·下一轮序："
    u"①#70 OSS 窗 3=10-02 21:40 后开（≤3 刀·届窗即领）"
    u"②REACT 10-03 热点窗=届日领件（10-03 日报缺先补产 daily_brief）"
    u"③供给闸维持〔锚 C-00030+/新令级事件/新批注缺〕"
    u"④W41 周轮件=10-05·ETA 2026-10-02 21:40"
)
st['ts'] = now
task_src = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(?::\d{2})?\s*', '', line)
st['task'] = task_src[:60]

io.open(ST, 'w', encoding='utf-8', newline='\n').write(json.dumps(st, ensure_ascii=False, indent=1) + '\n')

# reload + assert (R899 terminal clause)
st2 = json.loads(io.open(ST, 'r', encoding='utf-8-sig').read())
assert st2['tick'] == 911, 'tick post-write mismatch'
assert st2['log'][-1] == line, 'last log line mismatch'
assert re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}', st2['log'][-1]), 'log line-head ts missing'
assert re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', st2['ts']), 'ts format broken'
assert st2['task'] == task_src[:60], 'task mismatch'
print('R911-CLOSE-OK tick=%d ts=%s log_lines=%d' % (st2['tick'], st2['ts'], len(st2['log'])))
