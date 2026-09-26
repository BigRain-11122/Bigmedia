# E4 audience reference call - MC-20260927-REACT-v3 static hot-topic reaction card (non-registry
# seat, direct Ollama; v2 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态热点反应卡《城市速报 003》'
    u'（1080×1080 方图·黑底；顶部标题「城市速报 003」；下面六行：'
    u'「今日热点 · 知乎热榜 2026-09-27」'
    u'「财务自由的感觉是怎样的？」'
    u'「逍遥轴：「交易盘了，咱就图个心宽」」'
    u'「烟火轴：「刚赚的这份钱，得给孩子买点糖」」'
    u'「像素灵池：「喵呜一声，今日利润喜上眉梢」」'
    u'「渡轮船长信条：「船稳，人心才稳。」」；'
    u'图内底部来源行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）虚构 IP，城里住着一万多名虚构居民；'
    u'这张卡是「城市速报」系列的运作方式：当天的真实热点（知乎热榜上关于「财务自由的感觉」的讨论）原样转述，'
    u'然后由虚构城市按自己的方式「反应」——'
    u'三条反应行逐字取自这座城市的居民台词库（按性情分成逍遥、烟火等六个轴），编辑从收市后的情境（market_close 桶）里挑了三个轴位的原句；'
    u'收束行的信条出自城里一位渡轮船长的居民档案——他是全城唯一保留慢班渡轮的船长，他说数据道再快，'
    u'他这条渡轮永远留着慢班，他的信条是「船稳，人心才稳。」；'
    u'像素灵是这座虚构城市里自有的小生灵。'
    u'这张卡由本地渲染链自动生成，是「城市速报」系列的第三张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话、看不懂的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260927-REACT-v3 static card (cards.json + render output)'}
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
