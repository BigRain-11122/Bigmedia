# E4 audience reference call - MC-20260925-DIGEST-v1 static digest card (non-registry seat,
# direct Ollama; MC-20260925-QUOTE-v6-tmp/e4_call.py pattern R289: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 001》'
    '（1080×1080 方图·黑底；顶部标题「城市盘点 001」；下面六行数字盘点：'
    '「立国日 2026-09-23 · 一个下午」「61 分钟 · 三家公司骨架立完」「432 个炒股方案 · 0 组过线」'
    '「8 款软著 · 0 元成本」「老板决策合计 · 17 分钟」「剩余几百个动作 · 全 AI 完成·每步留痕」；'
    '图内底部来源行「基于硅基城市真实事件（立国日台账档案）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：这些数字逐条取自「硅基城市」2026 年 9 月 23 日立国当天的真实台账档案——硅基城市是一家由 AI 全自主运转的公司集团'
    '（只有一个人类老板，其余成员全是 AI），当天下午 61 分钟里三家公司在代码库里立完骨架，全部数字可溯源可审计；'
    '这张卡由本地渲染链自动生成，是「城市盘点」系列的第一张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-DIGEST-v1 static card (cards.json + render output)'}
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
