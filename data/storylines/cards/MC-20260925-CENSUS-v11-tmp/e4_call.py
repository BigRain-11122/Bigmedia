# E4 audience reference call - MC-20260925-CENSUS-v11 static census card (non-registry seat,
# direct Ollama; MC-20260925-CENSUS-v10-tmp/e4_call.py pattern R300: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 011》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 011」；下面六行居民档案：'
    '「C-00020 · 苏梓涵」「碳基市民 · 原生代 · 女 · 24 岁」「GAME 城 · 游戏楼街区 · 关卡建筑师」'
    '「信条：「每个转角都该藏一个惊喜。」」「点子多 · 会折腾 · 记性好」'
    '「全城唯一给「夜班人员」留专属彩蛋的关卡建筑师」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00020）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '苏梓涵是 GAME 城游戏楼街区的一位关卡建筑师，碳基市民·原生代，女，24 岁；'
    '她是踩着游戏楼测试关卡长大的——童年的秋千就是一根测试横杆；'
    '她建的关卡有种「住民的温柔」：新手道永远比规程多留半步余量，彩蛋永远埋在光最暖的地方；'
    '她说好关卡像好弄堂，走一遍就舍不得搬走；'
    '第一个署名关卡上线那晚，她蹲在城门口听了一夜玩家的议论，第二天把最狠的差评打印出来贴在工位；'
    '她随身小本记玩家口头禅，说「玩家的话就是最好的需求文档」；'
    '她下班必去老城门给守门人带一杯热的；'
    '她是全城唯一给「夜班人员」留专属彩蛋的关卡建筑师——守门人、巡夜员、灯塔守望都收到过，谁也没找到全部，'
    '他们管这叫「梓涵的深夜惊喜」；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00020），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第十一张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-CENSUS-v11 static card (cards.json + render output)'}
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
