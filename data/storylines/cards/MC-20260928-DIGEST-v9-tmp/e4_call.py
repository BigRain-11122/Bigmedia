# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20260928-DIGEST-v9 static digest card (non-registry seat,
# direct Ollama; v8 pattern R577: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 009》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 009」；下面七行数字盘点：'
    u'「自驱力生态令 2026-09-28 落账 09:20:25」'
    u'「不能有任何闲置资源，还有空转浪费现象」（引号行是老板原话：要求全员拉满、高效、不许闲置）'
    u'「3 缺口：创新无定轨 · 空转无定义 · 拉满张力」'
    u'「闭环 4 件：提案轨·空转禁令·诚实边界·计量回访」'
    u'「提案轨：三句式 · 无需 CEO 令 · 试点 ≤2 周」'
    u'「空转 4 形态定规 · idle-fast 跳轮路径全司废止」'
    u'「8 线点名 · 本司 ack ≤10 分钟 · 回访 10-05」；'
    u'图内底部来源行「基于硅基城市真实事件（集团台账与本司台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'9 月 28 日早上老板在集团台账里下了一句话命令：全面建立自驱力生态机制，工作任务要拉满、要高效，'
    u'不能有任何闲置资源和空转浪费。这条命令点名了集团 8 条线。'
    u'集团台账同时定谳了三个缺口（创新没有固定轨道、空转没有统一定义、拉满指标和诚实汇报之间有张力），'
    u'并立了四件闭环机制：每家公司每个周期必须至少提 1 条自驱提案（三句式：现象+建议+判据，不需要老板批准就能试点 2 周，'
    u'试点判负也要如实留痕）；空转被定义成四种形态并全集团禁止（包括为了凑指标造活——造活本身算空转）；'
    u'拉满指标只许用真活填（GPU 超 70%、队列常备 25 条是目标，但保护态豁免不算违规）；'
    u'每周报新增自驱面一行，10 月 5 日首次回访。'
    u'本卡的制作公司 BigStream 在命令落账后 10 分钟内就完成了响应（检出+两步适配：提案轨上线、旧空转跳轮路径废止），'
    u'这张卡本身就是新机制下当轮产出的盘点件。全部数字可在集团台账与本司台账溯源。这是「城市盘点」系列第九张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260928-DIGEST-v9 static card (cards.json + render output)'}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[\u2800-\u28ff]', '', cleaned)  # braille spinner range (R189 U+2800 lesson)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
