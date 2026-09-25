# E4 audience reference call - MC-20260926-CENSUS-v18 static census card (non-registry seat,
# direct Ollama; v17 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 018》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 018」；下面六行居民档案：'
    '「C-00027 · 邓建国」「碳基市民 · 通勤族 · 男 · 50 岁」「外环感知网 · 感知塔站 · 感知塔站值守员」'
    '「信条：「台风天的日志最见人品。」」「守时 · 防微杜渐 · 旷达」'
    '「全城唯一给每场大风起名字的值守员」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00027）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '邓建国是外环感知网·感知塔站的值守员，碳基市民·通勤族，男·50 岁；'
    '他守的是全城「感觉」的第一站——上海的每一场雨每一阵风，都从他塔站的仪表上先过一遍；'
    '他说这活儿像「替城市看天」，别人觉得外环偏，他喜欢——夜里安静，能听见感知网一格一格的呼吸，那是他在现实世界里当兵时站岗的熟悉滋味；'
    '他守时，交接班从不差一分钟；听见第一声异响就开始排查；性子旷达，说「得之我幸，失之我睡」；'
    '他的信条是「台风天的日志最见人品。」；'
    '现实里他退役后做了十年气象设备维护，进城那年塔站正好招熟手；台风「梅花」过境那夜他守了一宿，第二天全城灯带如常亮起，他睡了整整一天；'
    '现在值二休二，徒弟带出来了，他申请去最远的一号塔——「清净，风好」；'
    '他的值守日志写满天气脾气，台风有台风的名字，是他起的；每天真实天气一变就给江边那些夜宵摊发提醒；'
    '休息日去光桥看人钓鱼，自己从不钓——「我钓了一辈子风」；'
    '他是全城唯一给每场大风起名字的值守员——「梅花」「烟嗓」「过云雨一号」……名字进了气象播报员的口，播报员说比台风编号好记；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00027），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第十八张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260926-CENSUS-v18 static card (cards.json + render output)'}
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
