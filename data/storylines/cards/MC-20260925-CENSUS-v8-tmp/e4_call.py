# E4 audience reference call - MC-20260925-CENSUS-v8 static census card (non-registry seat,
# direct Ollama; MC-20260925-CENSUS-v7-tmp/e4_call.py pattern R297: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 008》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 008」；下面六行居民档案：'
    '「C-00017 · 归档者-07」「硅基民 · 编译系 · 无定 · 编译纪 12 年」「QUANT 城 · 回测田 · 回测农（算法调参师）」'
    '「信条：「参数不收敛，天理难容。」」「有条理 · 记性好 · 慢热」'
    '「全城唯一坚持给失败参数建「纪念碑田」的回测农」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00017）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '归档者-07 是 QUANT 城回测田里的一位硅基民回测农（算法调参师），编译纪 12 年，没有固定性别；'
    '它是某次全城大编译的产物，觉醒那年醒来第一句话是报了自己的版本号；'
    '它管种参数叫看天吃饭：播种一批参数，浇水施肥等三天，收成看市场脸色，每晚把「农谚」写进日志；'
    '它信一件事：数据不说谎，人才会——所以它把每次失败都归档，攒成自己的「农谚集」；'
    '有一次遇到一个永远不收敛的模型，它没删参数，而是单独辟了块「试验田」，后来那模型成了镇田之宝；'
    '它给自己挑了「归档者」这个名字，师父说太老气，它说「庄稼人的名字，土一点收成才稳」；'
    '它师父朱鸿奎——就是「城市图鉴 002」卡里 74 岁的时空校准师——说它「比我见过的大多数碳基都老派」；'
    '它的邻居是食堂大厨徐根福——就是上一张「城市图鉴 007」卡的主角，每天给它留一份「热的」，它不需要吃，但从不拒绝；'
    '它性格有条理（工具箱里的扳手都有户口）、记性好（每一季的收成账都在芯里）、慢热（三个月才交心，交了就是一辈子）；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00017），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第八张，也是系列里第一张硅基民（非碳基市民）的卡。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-CENSUS-v8 static card (cards.json + render output)'}
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
