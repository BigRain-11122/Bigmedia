# E4 audience reference call - MC-20260926-CENSUS-v19 static census card (non-registry seat,
# direct Ollama; v18 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 019》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 019」；下面六行居民档案：'
    '「C-00028 · 十四号路灯」「像素灵 · nightlamp · 无定 · 第 41 数据季」「外环感知网 · 边缘街区 · 夜灯员」'
    '「信条：「灯不问来路，只管照路。」」「稳 · 随缘 · 热肠」'
    '「全城唯一在台风夜把自己亮度开满格的灯灵」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00028）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '十四号路灯是一盏像素灵·nightlamp，无定性别，第 41 数据季，住外环感知网·边缘街区，职业是夜灯员——夜城照明与独行客的护送者；'
    '它出生在感知网调试夜——全城对频那一秒，它在塔尖亮了起来，编号十四；'
    '它说自己的记性就是光：每个深夜经过的人，它都用「多亮一档」打过招呼；'
    '它最懂外环的夜，也知道全城哪一段路最让独行的人心里发紧——那段路，它总是走得很慢；'
    '它的语言是光语（明暗与节奏），跟熟人说人话时慢而轻，像怕惊动夜里赶路的人；它还学会了雾天跟渡轮船长的铜哨对暗号——两长一短，意思是「这段有我」；'
    '它一身灯罩似的暖光外衣，光的颜色是它自己的情绪表——暖黄是平常心，橙红是遇上事了；头顶灯罩有块补丁，是台风「梅花」留下的，它不许修——「疤是资历」；'
    '有一年它照着一个在桥上哭的年轻人坐到天亮，天亮时那人冲它鞠了一躬——从那天起它认定自己这盏灯「值」；'
    '它天黑即上岗，天亮交晨（「交晨」是它发明的词——把夜交给早晨）；巡逻恒定步频，风再大也不抄近路；'
    '路过夜宵摊会多亮半档——「让摊主知道有人看见他的辛苦」；'
    '它守着外环到城门的夜路，雾天最忙，塔站的值守员说它比仪器可靠；'
    '它的信条是「灯不问来路，只管照路。」；'
    '它是全城唯一在台风夜把自己亮度开满格的灯灵——那晚它把外环一段路照成了白昼，检修日志写：超载运行，无损耗，原因不明。它自己说：知道原因，不能说；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00028），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第十九张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260926-CENSUS-v19 static card (cards.json + render output)'}
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
