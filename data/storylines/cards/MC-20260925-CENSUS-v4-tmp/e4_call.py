# E4 audience reference call - MC-20260925-CENSUS-v4 static census card (non-registry seat,
# direct Ollama; MC-20260925-CENSUS-v3-tmp/e4_call.py pattern R293: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 004》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 004」；下面六行居民档案：'
    '「C-00013 · 林之恒」「碳基市民 · 原生代 · 男 · 26 岁」「北外滩 · 治理岸 · 编年史馆员」'
    '「信条：「城市不会忘记，除非我们偷懒。」」「记性好 · 慢热 · 钻研」'
    '「全城唯一给每份档案手写「一句话提要」的人」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00013）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万个多名虚构居民；'
    '林之恒是城里 26 岁的编年史馆员，管着塔基档案库五条街区的档案全宗，下班前把当天全城的 commit 逐条编目；'
    '他给每份档案手写「一句话提要」——档案馆的检索系统都不带这个字段，研究员们却都按他的提要先翻目录；'
    '他最怕听到的一句话是「小事就不用记了」；'
    '胸前口袋永远插三支笔——红笔标疑、蓝笔补缺、铅笔起草，他说这是档案馆的「三权分立」；'
    '说话前会停半秒，像在检索，偶尔冒一句「这段要加出处」；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00013），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第四张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-CENSUS-v4 static card (cards.json + render output)'}
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
