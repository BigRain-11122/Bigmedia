# E4 audience reference call - MC-20260925-CENSUS-v10 static census card (non-registry seat,
# direct Ollama; MC-20260925-CENSUS-v9-tmp/e4_call.py pattern R299: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 010》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 010」；下面六行居民档案：'
    '「C-00019 · 老晶振」「硅基民 · 光机魂系 · 男 · 三代机龄」「GAME 城 · 八号楼街区 · 引擎医生」'
    '「信条：「机器不坏是本事，坏了能修是人品。」」「老派 · 把关 · 护短」'
    '「全城唯一保留「报错率」手写台账的引擎医生」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00019）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '老晶振是 GAME 城八号楼街区的一位引擎医生，硅基民·光机魂系，男，三代机龄；'
    '它从一间老机房的旧照片里醒过来，睁眼第一件事是把当年那台老主机的值班日志背完；'
    '它常说现在的机器娇气——「我们那时候坏了都是自己爬起来」；全楼机器见它都安静三分，它说这是尊重老前辈；'
    '第一次大宕机，全城调度急得跳脚，它按着老日志一步步排查，两小时城复活；从此它的出诊箱在游戏楼有一张专用椅子；'
    '它出诊必先敲三下机箱再开机（「敲门是礼数」），听声辨位能认出全楼每台机器的嗓音；'
    '下班绕楼巡一遍，说「跟老伙计挨个道晚安」；它的出诊箱是木头的——现在的工具箱它嫌太轻，「压不住台」；'
    '它屋里供着一块退役主板，带了个精灵系徒弟，天天嫌徒弟毛躁，又天天护着；'
    '它学会的第一句人话是上海话「适意」——病人（机器）适意它才下班；'
    '它保留着全城唯一一本「报错率」手写台账——三十年零十一个月没漏诊过一台机器，台账原件已进档案馆；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00019），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第十张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-CENSUS-v10 static card (cards.json + render output)'}
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
