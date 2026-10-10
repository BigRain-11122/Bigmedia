# -*- coding: utf-8 -*-
# R1876 ledger part 2: queue marks + state.json (prefix-based anchoring)
import io, json, datetime

# ---------- queue main.md #1/#2 done ----------
mp = 'state/queue/main.md'
lines = io.open(mp, encoding='utf-8').read().splitlines()
done1 = False
done2 = False
for i, l in enumerate(lines):
    if not done1 and l.startswith('1. '):
        lines[i] = '[R1876 done 2026-10-10] ' + l
        done1 = True
    elif not done2 and l.startswith('2. '):
        lines[i] = '[R1876 done 2026-10-10] ' + l
        done2 = True
assert done1 and done2, (done1, done2)
io.open(mp, 'w', encoding='utf-8', newline='').write('\n'.join(lines) + '\n')
print('queue main #1/#2 marked done')

# ---------- queue tech.md: #5 unlock + #41 new ----------
tp = 'state/queue/tech.md'
lines = io.open(tp, encoding='utf-8').read().splitlines()
hit5 = False
for i, l in enumerate(lines):
    if not hit5 and l.startswith('5. '):
        lines[i] = '5. [R1876 UNLOCKED - gated ollama recovery 2026-10-10] ' + l[3:]
        hit5 = True
assert hit5
lines.append(
    '41. **ollama 服务队列饱和事件监测与恢复判定（R1876 实锚·机器级共享面）**：07:45 起全 ollama 请求 503 '
    '「server busy·maximum pending requests exceeded」（最小探针 14b/7b 双 503 实证·阻塞者=并发会话 codely '
    'PID 54520 07:42:02 长调用·用户级 OLLAMA_NUM_PARALLEL=2）；受害面=E4 v13 重飞 x2+AIHOT worker 32x503 '
    'receipts+一切 12:00 GPU 独占窗 ollama 腿（MD-0002 剧本腿/27b A/B/E4/E1 席）；**判据**=每轮首查最小探针 '
    '（ollama run qwen2.5:14b 单句·503 消失即恢复）→恢复后 1)E4 v13 重飞（CLI 直飞）2)tech#5 prefilter '
    '全热点口径执行+效果测量 3)12:00 窗腿按 R-20261010-01 5 序开窗；**连续 3 轮仍饱和=升级 HQ-FEEDBACK 机器级 '
    'open 行**（多司受害面·不自行重启共享 ollama=让路律+零接触）')
io.open(tp, 'w', encoding='utf-8', newline='').write('\n'.join(lines) + '\n')
print('queue tech #5 unlock + #41 added')

# ---------- state.json ----------
sp = 'src/os/state.json'
d = json.load(io.open(sp, encoding='utf-8'))
d['tick'] = 1876
d['ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
logline = (
    '2026-10-10 08:0x R1876: 生产轮·#112 门控② 首份城市源雷达日报验收轮届日即领毕（实活轮·R1875 下步指针兑现）——'
    '①**验收读数四件**：日报 id=2 落地=诚实空态（窗 10-09 08:00→10-10 08:00·judged 0/selected 0/sections 0·'
    '「今日安静，无大事发生」·证据 .c3-tmp/r1876_gate2_evidence.json+probe 脚本入 git）+城市源覆盖读数=144 篇'
    '〔blocked 72=50% AI 行业 prefilter 按设计/analyzed 23/failed 34/new 15〕·非回填 pubs 46/scored 7/**max 45<60**/'
    '0 selected=**城市源贡献 0·R1873「0 入刊预判」证实**+requeue 26 净效=净负（城市 failed 7→34·receipts 19:00 后 '
    'TimeoutError x41+llm HTTP 503 x32·R1800「不 re-requeue」处置再证）+窗内非回填 selected 材料=0（唯一 AWS-75='
    '昨日窗内已消费）·weekly W40/monthly 09 compose failed=累积窗预期态 →**tech#5 UNLOCKED**（prefilter.md 全热点口径·'
    '改文本非改码）但执行前置=ollama 队列恢复；②**机器级事故实录=ollama 服务队列饱和**：07:45 起一切 ollama 请求 503 '
    '「maximum pending requests exceeded」（E4 v13 重飞两飞秒败+最小探针 14b/7b 双 503+AIHOT worker 32x503 '
    'receipts）·阻塞者=并发会话 codely PID 54520（07:42:02 起长调用占位·用户级 OLLAMA_NUM_PARALLEL=2）·共享面'
    '零接触不重启（让路律）→tech#41 监测项入队（恢复判据=最小探针 503 消失·连续 3 轮饱和=升 HQ-FEEDBACK 机器级行）；'
    '③E4 v13 重飞=两飞 503 定谳 blocked-on-ollama-queue（非拦截席追加制·e4-result.json 503 铁证留档）；'
    '④12:00 GPU 独占窗排程判断=**窗口门改判 ollama 恢复**（GPU VRAM 已释放 1% util/3.2GB 驻留·但 ollama 腿全 '
    'blocked·MD-0002 剧本腿/27b A/B/E4/E1 席/DIGEST v17 M4.5/E4/F-170 S1=恢复后按 R-20261010-01 5 序开窗）；'
    '⑤轮首五查静（origin_gap_check QUIET ahead0 behind0/own orders O-20261008-1105 mtime 锚零新令/decisions dnum '
    '内容寻址差集 NEW=[] 水位 140/ledger @BigStream 4 行值守锚零新转办/树态=MV sprint 会话域零接触·无 index.lock/'
    'AIHOT 栈三件活 api 3101 {ok,db:ok}+web 3100 200〔首探测 :3000=端口误置操作红·正身=3100/3101〕）；'
    '⑥三队盘点+补货=main#1/#2 done 标注（本轮消费项回写）+tech#5 UNLOCKED 标注+tech#41 新增（补货步 ✓）·'
    '例行件=10-10 日报在案不重跑（R1845 一份为真相）·W41 周审在案 W42 件 10-12 未到·GB §④ v1.3 下期 10-15 跳过·'
    '#99 blocked-on-channel 维持（SLA ≤10-13）·krea2/H3 查看位零新到件（R1875 锚·禁重扫）·HQ-FEEDBACK 不写'
    '（ollama 事故=潜在自愈型·tech#41 3 轮判据后升级·零膨胀）·tokens:local=0（纯探针+DB 读零本地模型产出调用·'
    'E4 两飞 503 秒败无产出不计量·P-54⑤ 如实记）·三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 '
    '阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现/loop_health 2F+史实带内（两 outage 已裁定'
    '不重触发·drift 带内）——下轮=R1877 快速路径首查（**ollama 最小探针恢复判定〔tech#41〕→恢复即 E4 v13 重飞+'
    'tech#5 执行+12:00 窗腿开窗·未恢复则饱和计数**+krea2/H3 查看位增量随轮盯〔R1762 双路径并读律〕）')
d['task'] = logline[logline.index(':') + 2:logline.index(':') + 62]
d['log'].append(logline)
d['focus'] = (
    'R1877 快速路径首查（**ollama 队列恢复判定·tech#41 判据=最小探针 503 消失**〔恢复即①E4 v13 重飞 CLI 直飞'
    '②tech#5 prefilter 全热点口径执行+效果测量③12:00 GPU 窗腿按 R-20261010-01 5 序开窗：MD-0002 剧本腿窗头'
    '→DIGEST v17 M4.5/E4/F+F-170 S1·两件评审材料 R1875 已 turnkey 预置〕+未恢复=tech#41 饱和计数（3 轮=升 '
    'HQ-FEEDBACK 机器级行）+krea2/H3 查看位增量随轮盯〔R1762 双路径并读律〕+三队盘点）')
io.open(sp, 'w', encoding='utf-8', newline='').write(json.dumps(d, ensure_ascii=False, indent=1))
print('state.json updated: tick', d['tick'], 'ts', d['ts'])
